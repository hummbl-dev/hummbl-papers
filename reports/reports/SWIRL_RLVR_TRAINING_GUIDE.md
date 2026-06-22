# Training Small Reasoning Models with SWiRL and RLVR: Implementation Guide

**Wave 4 Deep Research Report -- Autoresearch Project**
**Date:** 2026-03-24
**Implements:** Goal 5 (Reasoning Trace Capture) and Goal 6 (Process Reward Models)
**Hardware Target:** RTX 3080 Ti (12GB VRAM), Desktop; M4 Pro 48GB, Nodezero
**Upstream:** REASONING_TRACE_FORMAT_SPEC v0.1, THINKPRM_IMPLEMENTATION_GUIDE, NemoClaw v0.1.3

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [RLVR: Reinforcement Learning with Verifiable Rewards](#2-rlvr-reinforcement-learning-with-verifiable-rewards)
3. [GRPO: Group Relative Policy Optimization](#3-grpo-group-relative-policy-optimization)
4. [SWiRL and Related Approaches](#4-swirl-and-related-approaches)
5. [Can Small Models Reason? Evidence at 1-3B Scale](#5-can-small-models-reason-evidence-at-1-3b-scale)
6. [Practical Implementation on Consumer Hardware](#6-practical-implementation-on-consumer-hardware)
7. [Using Autoresearch Traces as Training Data](#7-using-autoresearch-traces-as-training-data)
8. [Evaluation](#8-evaluation)
9. [Implementation Roadmap](#9-implementation-roadmap)
10. [Key Papers and Resources](#10-key-papers-and-resources)

---

## 1. Executive Summary

This guide lays out how to train a small (1.5B-3B parameter) language model to reason about ML experiments, using the autoresearch trace corpus as training data and reinforcement learning with verifiable rewards as the training signal. The core insight: val_bpb improvement is a *verifiable reward* -- the model either proposes an experiment that beats the baseline or it does not, and the outcome is determined by running the experiment, not by human judgment.

**The pipeline in one paragraph:** Start with a pre-trained small model (Qwen2.5-1.5B or 3B). Fine-tune it on ~2,760 autoresearch reasoning traces using supervised learning (Phase 1). Build preference pairs from accept/reject sibling traces and train with DPO (Phase 2). Then use GRPO with val_bpb as the verifiable reward signal, where the model proposes experiments and receives binary feedback on whether they improved the metric (Phase 3). Finally, close the loop by deploying the model as the NemoClaw hypothesis generator and training online (Phase 4).

**Key finding from the research:** You do not need 800K samples like DeepSeek-R1. SWiRL demonstrates that 1,000 high-quality trajectories produce "solid gains across all datasets." With 2,760 traces/year and synthetic augmentation to ~10K-50K, the autoresearch corpus is sufficient for meaningful reasoning improvement in a 1.5B-3B model.

**Hardware feasibility:** GRPO training of a 1.5B model with QLoRA fits in 12GB VRAM. A 3B model requires aggressive optimization but is achievable. The RTX 3080 Ti can train a reasoning model in 8-24 hours per epoch depending on configuration.

---

## 2. RLVR: Reinforcement Learning with Verifiable Rewards

### 2.1 What Is RLVR?

RLVR replaces the learned reward model in traditional RLHF with a deterministic, programmatic verifier. Instead of training a neural network to predict human preferences (expensive, noisy, hackable), RLVR uses tools that produce binary correctness signals:

| Domain | Verifier | Signal |
|--------|----------|--------|
| Math | Symbolic solver / exact match | 1.0 if answer matches ground truth |
| Code | Unit test execution | 1.0 if all tests pass |
| SQL | Query execution equivalence | 1.0 if result sets match |
| **ML experiments** | **val_bpb comparison** | **1.0 if val_bpb < baseline** |

The "V" in RLVR means the reward is deterministic and trustworthy -- no reward hacking is possible because the verifier is a ground-truth oracle. For autoresearch, this is uniquely powerful: running an experiment and measuring val_bpb *is* the verification step.

### 2.2 The DeepSeek-R1 Approach

DeepSeek-R1 (January 2025, arXiv 2501.12948) demonstrated that pure RL with verifiable rewards can induce reasoning in LLMs without any supervised fine-tuning. The training pipeline:

1. **Start from a pre-trained base model** (DeepSeek-V3-Base)
2. **Apply GRPO** with rule-based rewards: accuracy (binary correct/incorrect) + format (did the model use `<think>` tags?)
3. **No SFT warmup** -- the hypothesis was that human-defined reasoning patterns limit exploration
4. **Result:** The model spontaneously developed self-reflection, verification, and dynamic strategy adaptation

**DeepSeek-R1-Zero** (pure RL, no SFT) demonstrated emergent "aha moment" behaviors -- the model would reconsider its approach mid-reasoning, something never explicitly trained. However, it suffered from readability issues and language mixing.

**DeepSeek-R1** (the full model) added a cold-start SFT phase before RL to stabilize training, then alternated between RLVR and RLHF for polish. The distilled versions used 800K reasoning traces to fine-tune smaller models (Qwen-1.5B through Llama-70B).

### 2.3 What Makes a Reward "Verifiable" for ML Experiments?

For autoresearch, the verifiable reward is constructed from multiple signals:

**Primary reward: val_bpb improvement**
```python
def experiment_reward(proposed_val_bpb: float, baseline_val_bpb: float) -> float:
    delta = baseline_val_bpb - proposed_val_bpb  # positive = improvement
    if delta > 0.001:    # clear improvement beyond noise floor
        return 1.0
    elif delta > 0.0:    # marginal improvement
        return 0.5
    elif delta > -0.005: # marginal regression
        return -0.5
    else:                # clear regression
        return -1.0
```

**Secondary rewards (format and quality):**
```python
def format_reward(trace: dict) -> float:
    """Check structural quality of the proposed experiment."""
    score = 0.0
    # Hypothesis is well-formed (references prior evidence)
    if len(trace["hypothesis"]["prior_evidence"]) > 0:
        score += 0.25
    # Predicted effect has direction and magnitude
    if trace["hypothesis"]["predicted_effect"]["direction"] in ["increase", "decrease"]:
        score += 0.25
    # Code change is minimal (fewer files = cleaner experiment)
    if trace["code_changes"]["lines_changed"] <= 5:
        score += 0.25
    # Config is within sane ranges
    if 1e-6 < trace["config"].get("matrix_lr", 0.01) < 1.0:
        score += 0.25
    return score
```

**Prediction accuracy reward:**
```python
def prediction_reward(predicted_direction: str, predicted_magnitude: float,
                      actual_delta: float) -> float:
    """Reward accurate predictions about experiment outcomes."""
    actual_direction = "decrease" if actual_delta < 0 else "increase"
    if predicted_direction == actual_direction:
        # Direction correct -- reward proportional to magnitude accuracy
        ratio = min(abs(predicted_magnitude), abs(actual_delta)) / max(abs(predicted_magnitude), abs(actual_delta))
        return 0.5 + 0.5 * ratio  # 0.5 to 1.0
    else:
        return 0.0  # Wrong direction
```

### 2.4 The Sampler vs. Thinker Debate

Recent research (2025-2026) raises an important question: does RLVR teach models to *reason better* or merely to *sample more efficiently*?

**Evidence for "sampler" (search compression):**
- Tsinghua research found that pass@k ceiling stays flat while pass@1 improves -- meaning the model already *could* solve the problem, it just needed more attempts
- Most RLVR gains decompose as: majority = search compression, minority = capability expansion
- Random rewards achieved 21.4% improvement on MATH-500, vs. 29.1% for ground-truth rewards -- suggesting training dynamics contribute independent of verifier quality

**Evidence for "thinker" (genuine capability expansion):**
- June 2025 research (arXiv 2506.14245) showed CoT-pass@k improvements and persistence on unseen problem types
- Cross-domain transfer in SWiRL: training on QA improved math performance by 16.9%
- DeepSeek-R1-Zero's emergent self-reflection was never in the training signal

**Practical implication for autoresearch:** Even if RLVR mostly compresses the search space rather than teaching fundamentally new reasoning, *that is still valuable*. A model that proposes good experiments on the first try (high pass@1) instead of requiring many attempts is exactly what NemoClaw needs.

### 2.5 Key RLVR Papers (2024-2026)

| Paper | Year | Key Contribution |
|-------|------|------------------|
| DeepSeek-R1 (arXiv 2501.12948) | Jan 2025 | Pure RL reasoning without SFT; GRPO + verifiable rewards |
| DeepSeekMath (arXiv 2402.03300) | Feb 2024 | Introduced GRPO; 51.7% on MATH benchmark |
| RLVR Implicitly Incentivizes Correct Reasoning (arXiv 2506.14245) | Jun 2025 | Evidence that RLVR teaches genuine reasoning, not just sampling |
| RLVR Makes Models Faster, Not Smarter (Promptfoo) | 2025 | Counterargument: most gains are search compression |
| GRPO Effective Loss and Dynamics (arXiv 2503.06639) | Mar 2025 | Mathematical analysis of GRPO reward dynamics |

---

## 3. GRPO: Group Relative Policy Optimization

### 3.1 How GRPO Works

GRPO (introduced in DeepSeekMath, February 2024) is the RL algorithm behind DeepSeek-R1's reasoning capabilities. It simplifies PPO by eliminating the critic (value) model:

**Step 1: Group sampling.** For each prompt, generate G completions from the current policy.

**Step 2: Reward scoring.** Each completion receives a reward from the verifier.

**Step 3: Group normalization.** Compute the mean and standard deviation of rewards within the group. Each completion's advantage is its reward minus the group mean, divided by the group std.

**Step 4: Policy gradient update.** Update the policy to increase probability of above-average completions and decrease probability of below-average ones, with a KL penalty against the reference model.

**The objective function:**
```
L_GRPO(theta) = E[  1/G * sum_i ( min(
    r_i(theta) * A_hat_i,
    clip(r_i(theta), 1-eps, 1+eps) * A_hat_i
) ) - beta * KL(pi_theta || pi_ref) ]

where:
  r_i(theta) = pi_theta(o_i|q) / pi_old(o_i|q)   # importance ratio
  A_hat_i = (R_i - mean(R)) / std(R)                # group-normalized advantage
  beta = KL coefficient (0.001 in DeepSeek-R1)
  G = group size (64 in DeepSeek-R1, 4-8 for consumer GPU)
```

### 3.2 Why GRPO Over PPO?

| Feature | PPO | GRPO |
|---------|-----|------|
| Critic model | Required (same size as policy) | Not needed |
| VRAM overhead | 2x model for critic | Only reference model (can offload) |
| Reward baseline | Learned value function | Group mean (zero-parameter) |
| Variance | Higher (noisy value estimates) | Lower (relative ranking within group) |
| Implementation complexity | High | Moderate |
| Best for | General RL | Verifiable reward domains |

For consumer hardware with 12GB VRAM, eliminating the critic model is critical. With PPO, training a 1.5B model requires the policy (1.5B) + critic (1.5B) + reference (1.5B) + optimizer states -- far exceeding 12GB even with quantization. GRPO removes the critic, making it feasible.

### 3.3 GRPO Variants and Improvements (2025)

**Dr. GRPO:** Addresses known biases in standard GRPO:
- Response-length bias (GRPO favors longer outputs)
- Difficulty-level bias (easy problems dominate gradients)
- Fix: simplified advantage calculation, explicit length normalization

**Off-Policy GRPO (arXiv 2505.22257):** Uses advantage estimates from a different policy than the current one. Results show off-policy GRPO matches or outperforms on-policy, enabling more efficient data reuse.

**REINFORCE++ (arXiv 2501.03262):** A simplified GRPO alternative with global advantage normalization (across the entire batch, not just within groups). Key advantages:
- Single-sample (k=1) achieves top-tier scores while being more token-efficient
- More stable training compared to GRPO
- Faster than PPO with comparable performance
- Implemented in OpenRLHF

### 3.4 GRPO Configuration for Autoresearch

Recommended GRPO configuration for training on autoresearch traces:

```python
from trl import GRPOConfig

grpo_config = GRPOConfig(
    output_dir="./autoresearch-reasoning-model",
    learning_rate=5e-6,
    per_device_train_batch_size=1,          # Memory constrained
    gradient_accumulation_steps=8,          # Effective batch = 8
    num_generations=4,                       # Group size (DeepSeek uses 64, we use 4 for VRAM)
    max_prompt_length=512,                   # Experiment context
    max_completion_length=1024,              # Hypothesis + reasoning
    temperature=0.7,
    num_train_epochs=3,
    warmup_steps=50,
    max_grad_norm=1.0,
    kl_coef=0.001,                           # Same as DeepSeek-R1
    use_peft=True,                           # QLoRA
    gradient_checkpointing=True,
    bf16=True,
    logging_steps=10,
    save_steps=100,
)
```

---

## 4. SWiRL and Related Approaches

### 4.1 SWiRL: Step-Wise Reinforcement Learning

SWiRL (arXiv 2504.04736, Stanford/Google DeepMind, April 2025) introduces step-level RL for multi-step reasoning and tool use. Unlike traditional RL that rewards only the final answer, SWiRL decomposes each trajectory into sub-trajectories and applies rewards at each intermediate step.

**The SWiRL pipeline:**

**Stage 1: Synthetic data generation and filtering**
1. Generate multi-step trajectories using the base model
2. For each trajectory, evaluate whether each step is "reasonable given all previous steps" (process filtering)
3. Key finding: process-only filtering outperforms outcome-only filtering -- trajectories with incorrect final answers but sound intermediate reasoning are *more valuable* than lucky correct answers with bad reasoning

**Stage 2: Step-wise reinforcement learning**
1. Decompose each filtered trajectory into sub-trajectories (one per action/step)
2. Score each sub-trajectory with a generative reward model (e.g., Gemini 1.5 Pro judges step quality)
3. Apply policy gradients at the step level: `J(theta) = E[R(action | state)]`
4. No golden labels required -- entirely model-based judgments

**Performance (Gemma 2 27B):**

| Dataset | Baseline | SWiRL | Relative Gain |
|---------|----------|-------|---------------|
| GSM8K | 0.65 | 0.79 | +21.5% |
| HotPotQA | 58.6% | 67.8% | +16.3% |
| CofCA | 31.7% | 39.3% | +14.8% |
| MuSiQue | 35.4% | 43.6% | +11.1% |
| BeerQA | 59% | 68% | +15.3% |

**Critical finding for autoresearch:** SWiRL achieves cross-domain generalization. Training on QA improved math by 16.9%, and training on math improved QA by 9.2%. This suggests that learning general multi-step reasoning patterns transfers across domains -- a model trained on ML experiment traces could potentially generalize to other reasoning tasks.

**Data efficiency:** SWiRL shows gains with as few as 1,000 trajectories. At 10,000 trajectories, improvements continue. This directly maps to the autoresearch corpus: 2,760 traces/year is in the productive range.

### 4.2 STaR: Self-Taught Reasoner

STaR (arXiv 2203.14465, Zelikman et al., 2022) bootstraps reasoning through iterative self-improvement:

**The STaR loop:**
1. Prompt the model to solve problems with chain-of-thought reasoning
2. Keep solutions where the model got the correct answer
3. For wrong answers, use "rationalization": prompt the model with the correct answer and ask it to generate a rationale backward
4. Fine-tune the model on the combined dataset (correct solutions + rationalized solutions)
5. Repeat from step 1

**Key innovation:** Rationalization enables learning from failures. The model does not just learn from its successes but also from backward reasoning given the correct answer.

**Results:** On CommonsenseQA, STaR reached 72.5% accuracy, matching models 30x larger. On GSM8K, accuracy nearly doubled from 5.8% to 10.7%.

**Relevance to autoresearch:** The STaR pattern maps directly to the trace corpus. Accepted experiments are "correct solutions." Rejected experiments can be rationalized: "Given that this experiment failed, generate a rationale explaining why and what should have been tried instead."

### 4.3 ReST: Reinforced Self-Training

ReST^EM (arXiv 2308.08998, Google, 2023) is a simpler variant:

1. Generate multiple solutions per problem from the current model
2. Filter: keep only solutions with correct final answers
3. Fine-tune on the filtered dataset
4. Repeat

ReST^EM scales favorably with model size and significantly surpasses fine-tuning on human data alone. The key advance over STaR is the EM (Expectation-Maximization) framing, which provides theoretical grounding.

**ReST-MCTS*** (2024) extends this with Monte Carlo Tree Search for collecting higher-quality reasoning traces and per-step value estimates for training both policy and reward models.

### 4.4 Quiet-STaR

Quiet-STaR (arXiv 2403.09629, Zelikman et al., March 2024) generalizes STaR so the model learns to generate internal reasoning ("thoughts") before *every token*, not just at answer time:

- Tokenwise parallel sampling generates internal rationales
- Learnable tokens mark thought boundaries
- Extended teacher-forcing teaches the model when thinking helps

**Results:** Zero-shot improvements on GSM8K (5.9% to 10.9%) and CommonsenseQA (36.3% to 47.2%) without task-specific fine-tuning. Rationales disproportionately help on difficult tokens.

**Relevance:** Quiet-STaR is more of a pre-training technique than a fine-tuning approach. It is not directly applicable to the autoresearch training pipeline but demonstrates that internal reasoning can be trained at small scale.

### 4.5 Comparison for Training Small Reasoning Models

| Method | Data Needed | RL Required? | Step-Level Reward? | Best For |
|--------|-------------|-------------|-------------------|----------|
| **SFT on traces** | ~1K-10K examples | No | No | Baseline; fast to train |
| **STaR** | Task dataset + model | No (self-play) | No | Bootstrapping from limited correct examples |
| **ReST^EM** | Task dataset + model | Minimal | No | Scaling beyond human data |
| **DPO** | Preference pairs | No (implicit) | No | Learning from accept/reject pairs |
| **GRPO/RLVR** | Verifiable reward | Yes | No (outcome only) | When you have a deterministic verifier |
| **SWiRL** | Multi-step trajectories | Yes | Yes (step-level) | Multi-step reasoning with tools |
| **Quiet-STaR** | General text corpus | No (self-play) | No | Pre-training for general reasoning |

**Recommendation for autoresearch:** Use a staged approach. SFT first (cheapest, establishes baseline), then DPO (uses existing preference pairs), then GRPO with val_bpb as verifiable reward (the core innovation), with SWiRL-style step-level rewards once the PRM (Goal 6) is operational.

---

## 5. Can Small Models Reason? Evidence at 1-3B Scale

### 5.1 The Shifting Size Threshold

The traditional view that reasoning requires 100B+ parameters has been thoroughly debunked by 2025-2026 research:

| Model | Size | GSM8K | Training Approach |
|-------|------|-------|-------------------|
| Qwen2.5-3B-Instruct | 3B | **84.74%** | SFT + multi-stage RL |
| Llama-3.2-3B | 3B | 73.54% | Standard training |
| Qwen2.5-1.5B-Instruct | 1.5B | **70.00%** | SFT + alignment |
| DeepSeek-R1-Distill-Qwen-1.5B | 1.5B | ~63% | Distillation from R1 (800K traces) |
| SmolLM2-1.7B | 1.7B | 46.17% | Weaker training recipe |
| Hymba-1.5B | 1.5B | 53.75% | Novel architecture |

**Key insight:** A well-trained 3B model (Qwen2.5) outperforms a poorly-trained 7B model. Training recipe matters more than raw scale at this range. The gap between Qwen2.5-3B (84.74%) and SmolLM2-1.7B (46.17%) -- nearly 40 percentage points -- is explained entirely by training quality, not architecture.

### 5.2 What Works at Small Scale

**2025 consensus from the literature:**

1. **SFT dominates RL at small scale.** When model capacity is limited, supervised fine-tuning plays a more prominent role. RL can contribute but requires far more data and compute to reach comparable levels, with diminishing returns as model size shrinks. SFT enables compact architectures to efficiently *inherit* problem-solving strategies from more capable teachers.

2. **Distillation is the fastest path.** DeepSeek's 1.5B distilled model, trained on 800K reasoning traces from the full R1 model, achieves competitive reasoning with zero RL. For a solo founder, distilling from a frontier model's outputs is faster and cheaper than running RL from scratch.

3. **RL on top of distilled models produces further gains.** Sebastian Raschka's 2025 survey notes that "RL applied to distilled models yields significant further gains." The optimal pipeline is distill first, then RL for polish.

4. **1,000 carefully curated examples can outperform 100K random ones.** Phi-4-Mini-Reasoning and similar work shows that targeted filtering of training data produces outsized improvements. Quality beats quantity decisively.

5. **Quantization preserves reasoning; pruning destroys it.** Even aggressive 4-bit quantization preserves reasoning capabilities. Pruning is catastrophic -- a pruned Llama-8B drops 32% on GSM8K. This means QLoRA training is safe for reasoning tasks.

### 5.3 The TinyLoRA Extreme

A remarkable 2026 result (arXiv 2602.04118): TinyLoRA scales LoRA adapters down to a single parameter, training Qwen2.5-8B to 91% accuracy on GSM8K with only 13 trained parameters (26 bytes in bf16). While this is an extreme case, it demonstrates that reasoning capability is more about *which* parameters to adjust than *how many*.

### 5.4 Minimum Viable Model for Autoresearch Reasoning

Given the evidence, the recommendation is:

**Tier 1 (RTX 3080 Ti primary):** Qwen2.5-1.5B as base model
- Fits comfortably in 12GB with QLoRA GRPO training
- Already scores 70% on GSM8K with instruction tuning -- reasoning-capable baseline
- DeepSeek-R1-Distill-Qwen-1.5B variant available as a reasoning-warm starting point
- Training time: ~8-12 hours per epoch on RTX 3080 Ti

**Tier 2 (Nodezero or cloud burst):** Qwen2.5-3B as base model
- 84.74% on GSM8K -- significantly more capable
- Fits in RTX 3080 Ti 12GB with aggressive QLoRA (4-bit base + LoRA rank 8)
- More comfortable on Nodezero's 48GB unified memory with MLX
- Training time: ~16-24 hours per epoch on RTX 3080 Ti

**Not recommended at this stage:** Models below 1B parameters. While reasoning is possible at small scale, the capacity for the specialized domain knowledge needed (ML experiment design, hyperparameter intuition, architecture understanding) likely requires at least 1.5B parameters.

---

## 6. Practical Implementation on Consumer Hardware

### 6.1 VRAM Budget for GRPO Training

GRPO training requires maintaining multiple model copies in memory simultaneously:

**Memory components (FP16/BF16):**
| Component | Bytes/Parameter | 1.5B Model | 3B Model |
|-----------|----------------|------------|----------|
| Policy model | 2 | 3.0 GB | 6.0 GB |
| Reference model | 2 | 3.0 GB | 6.0 GB |
| Gradients | 2 | 3.0 GB | 6.0 GB |
| Optimizer states (AdamW) | 8 | 12.0 GB | 24.0 GB |
| **Total (full precision)** | **14** | **21.0 GB** | **42.0 GB** |

This exceeds 12GB VRAM for even the 1.5B model in full precision. The solution is QLoRA:

**Memory with QLoRA (4-bit base + LoRA rank 16):**
| Component | 1.5B Model | 3B Model |
|-----------|------------|----------|
| Base model (4-bit) | 0.75 GB | 1.5 GB |
| Reference model (4-bit) | 0.75 GB | 1.5 GB |
| LoRA parameters (rank 16) | ~0.05 GB | ~0.1 GB |
| LoRA gradients | ~0.05 GB | ~0.1 GB |
| LoRA optimizer states | ~0.2 GB | ~0.4 GB |
| KV cache (4 generations) | ~1.0 GB | ~2.0 GB |
| Activations + overhead | ~2.0 GB | ~3.0 GB |
| **Total** | **~4.8 GB** | **~8.6 GB** |

Both fit within 12GB. The 3B model is tight but feasible with careful configuration.

### 6.2 Recommended Training Configuration

**For Qwen2.5-1.5B on RTX 3080 Ti (12GB):**

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import GRPOConfig, GRPOTrainer

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# Load model
model_id = "Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules="all-linear",     # 2025 best practice
    task_type="CAUSAL_LM",
)

# GRPO training config
training_args = GRPOConfig(
    output_dir="./autoresearch-reasoner-1.5b",
    learning_rate=5e-6,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_generations=4,                 # Group size (4 saves VRAM vs 64)
    max_prompt_length=512,
    max_completion_length=768,
    temperature=0.7,
    num_train_epochs=3,
    warmup_steps=50,
    max_grad_norm=1.0,
    kl_coef=0.001,
    gradient_checkpointing=True,
    bf16=True,
    logging_steps=10,
    save_steps=200,
    report_to="tensorboard",
)

# Reward functions
def val_bpb_reward(completions, **kwargs):
    """Binary reward: did the proposed experiment improve val_bpb?"""
    rewards = []
    for completion in completions:
        # Parse the model's proposed experiment and check against known outcomes
        # In offline training, we look up the actual result from the trace corpus
        reward = lookup_trace_outcome(completion)
        rewards.append(reward)
    return rewards

def format_reward(completions, **kwargs):
    """Structural quality of the experiment proposal."""
    rewards = []
    for completion in completions:
        score = 0.0
        if "<hypothesis>" in completion and "</hypothesis>" in completion:
            score += 0.25
        if "<predicted_effect>" in completion and "</predicted_effect>" in completion:
            score += 0.25
        if "<config>" in completion and "</config>" in completion:
            score += 0.25
        if "<reasoning>" in completion and "</reasoning>" in completion:
            score += 0.25
        rewards.append(score)
    return rewards

# Train
trainer = GRPOTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    processing_class=tokenizer,
    reward_funcs=[val_bpb_reward, format_reward],
    peft_config=peft_config,
)
trainer.train()
```

### 6.3 Framework Comparison

| Framework | Best For | GRPO Support | Consumer GPU? | Ease of Use |
|-----------|----------|-------------|---------------|-------------|
| **trl (HuggingFace)** | Single-GPU, prototyping | Native GRPOTrainer | Excellent | High |
| **OpenRLHF** | Multi-GPU, production | GRPO + REINFORCE++ | Moderate (needs Ray) | Medium |
| **veRL (ByteDance)** | Large-scale distributed | GRPO + PPO | Poor (designed for clusters) | Lower |
| **Minimal-RL (RLHFlow)** | Research, minimal code | REINFORCE variants | Good | High |

**Recommendation:** Start with **trl** for prototyping on the RTX 3080 Ti. It has native GRPOTrainer, built-in PEFT/QLoRA integration, and excellent documentation. Move to OpenRLHF only if scaling to multi-GPU or needing REINFORCE++.

### 6.4 Training Time Estimates

**Qwen2.5-1.5B with QLoRA GRPO on RTX 3080 Ti:**

| Dataset Size | Epochs | Group Size | Est. Time | Notes |
|-------------|--------|------------|-----------|-------|
| 2,760 traces | 3 | 4 | ~10 hours | Full autoresearch corpus |
| 10,000 traces (augmented) | 3 | 4 | ~36 hours | With synthetic augmentation |
| 50,000 traces | 1 | 4 | ~60 hours | Large-scale; use overnight runs |

**Qwen2.5-3B with QLoRA GRPO on RTX 3080 Ti:**

| Dataset Size | Epochs | Group Size | Est. Time | Notes |
|-------------|--------|------------|-----------|-------|
| 2,760 traces | 3 | 4 | ~24 hours | Tight on VRAM |
| 10,000 traces | 1 | 4 | ~28 hours | Single epoch may suffice |

**Warning:** GPU thermal management is critical for long training runs on the RTX 3080 Ti (270W TDP). Per project thermal feedback, sustained GPU load combined with other workloads risks thermal shutdown. Schedule GRPO training overnight when no other GPU tasks are running.

### 6.5 Alternative: SFT + DPO (No RL Required)

If GRPO training proves too memory-constrained or unstable, SFT + DPO is a strong fallback:

```python
from trl import SFTConfig, SFTTrainer, DPOConfig, DPOTrainer

# Phase 1: SFT on accepted traces
sft_config = SFTConfig(
    output_dir="./autoresearch-sft",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    num_train_epochs=3,
    gradient_checkpointing=True,
    bf16=True,
    packing=True,        # Pack short examples for efficiency
)

sft_trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=sft_dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
)
sft_trainer.train()

# Phase 2: DPO on accept/reject preference pairs
dpo_config = DPOConfig(
    output_dir="./autoresearch-dpo",
    learning_rate=5e-7,
    per_device_train_batch_size=2,
    num_train_epochs=1,
    gradient_checkpointing=True,
    bf16=True,
    beta=0.1,            # KL penalty coefficient
)

dpo_trainer = DPOTrainer(
    model=sft_model,     # Start from SFT model
    args=dpo_config,
    train_dataset=preference_dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
)
dpo_trainer.train()
```

SFT + DPO requires less VRAM than GRPO (no generation during training), trains faster, and is more stable. The tradeoff: DPO uses static preference pairs rather than dynamic exploration.

---

## 7. Using Autoresearch Traces as Training Data

### 7.1 Trace Corpus Overview

Per the REASONING_TRACE_FORMAT_SPEC, the autoresearch pipeline produces:

| Source | Traces/Month | Training-Eligible | Annual Total |
|--------|-------------|-------------------|--------------|
| Desktop (RTX 3080 Ti) | ~200 | ~160 (80%) | ~1,920 |
| Nodezero (M4 Pro) | ~100 | ~70 (70%) | ~840 |
| **Combined** | **~300** | **~230** | **~2,760** |

Each trace produces:
- 1 SFT example (instruction + response)
- ~0.36 preference pairs (from sibling accept/reject traces)
- 6 step-level reward annotations (hypothesis, config, training, result, decision, next_action)

**Annual training data yield:**
- ~2,760 SFT examples
- ~1,000 DPO preference pairs
- ~16,500 step-level PRM annotations

### 7.2 Converting Traces to Training Formats

**SFT format (from REASONING_TRACE_FORMAT_SPEC Section 7.3):**

```json
{
  "instruction": "You are an ML experiment planner for TinyStories (5-min budget, RTX 3080 Ti). Given the experiment history, propose the next experiment.\n\nCurrent best: val_bpb 0.5082 (DEPTH=8, WEIGHT_DECAY=0.2)\nRecent results:\n- Increasing depth to 10: REJECTED (0.5378, too slow)\n- Reducing batch size: REJECTED (0.5300, batch too small)\n\nPropose a hypothesis, predict its effect, and justify your reasoning.",

  "response": "<hypothesis>Remove weight decay entirely (0.2 -> 0.0). With only 2200 training steps, the model is severely undertrained. Weight decay penalizes large weights to prevent overfitting, but overfitting requires many passes over the data. At 2200 steps, the model has not fully learned the training distribution -- regularization is actively slowing convergence.</hypothesis>\n\n<predicted_effect>val_bpb decreases by ~0.003 (0.5082 -> ~0.505). Confidence: 0.65.</predicted_effect>\n\n<config>WEIGHT_DECAY = 0.0 (changed from 0.2). All other parameters unchanged.</config>\n\n<reasoning>Category: hyperparameter. This is a minimal change (1 line in train.py) that tests a clear hypothesis about regularization vs. undertrained regime. Prior evidence from warmdown improvements suggests the optimizer frontier is productive.</reasoning>"
}
```

**DPO preference pair format:**

```json
{
  "prompt": "Current best: val_bpb 0.5055 (WEIGHT_DECAY=0). Recent: warmdown 0.7 accepted (+0.004). What next?",
  "chosen": "<hypothesis>Sweep ADAM_BETAS from default (0.9, 0.999). After removing weight decay and adjusting warmdown, the optimizer is the active frontier. Betas control momentum and second-moment averaging -- underexplored in this regime.</hypothesis>\n<predicted_effect>val_bpb decreases by ~0.001. Confidence: 0.5.</predicted_effect>",
  "rejected": "<hypothesis>Increase WARMDOWN_RATIO to 0.9. More warmdown should help convergence.</hypothesis>\n<predicted_effect>val_bpb decreases by ~0.002. Confidence: 0.6.</predicted_effect>"
}
```

**RLVR prompt format (for GRPO training):**

```json
{
  "prompt": "You are an ML experiment planner. Given the experiment state below, propose one experiment.\n\nDataset: TinyStories\nBudget: 5 minutes (2200 steps)\nGPU: RTX 3080 Ti (12GB)\nCurrent best: val_bpb 0.4646\nArchitecture: 56M params, depth=8, n_embd=384, MLP 8x, GELU, NSSL window\nRecent experiments:\n- Muon optimizer: ACCEPTED (0.4650 -> 0.4646)\n- Sigmoid gating (init=0): REJECTED (diverged)\n- Sigmoid gating (init=2.0): REJECTED (no improvement)\n- GLA attention: EXPLORING (promising but needs tuning)\n\nRespond in the format: <hypothesis>...</hypothesis><predicted_effect>...</predicted_effect><config>...</config><reasoning>...</reasoning>"
}
```

### 7.3 Is 2,760 Traces Enough?

**Comparison to known training data sizes:**

| System | Training Traces | Model Size | Performance |
|--------|----------------|------------|-------------|
| DeepSeek-R1-Distill | 800,000 | 1.5B-70B | State-of-the-art reasoning |
| SWiRL (solid gains) | 1,000 | 2B-27B | +12-21% on reasoning benchmarks |
| SWiRL (strong gains) | 10,000 | 27B | Best performance |
| Phi-4-Mini targeted | 1,000 curated | 3.8B | Competitive reasoning |
| **Autoresearch Year 1** | **2,760** | **1.5B-3B** | **TBD** |

**Assessment:** 2,760 traces is *above* the SWiRL threshold for solid gains (1,000) but well below DeepSeek's distillation corpus (800K). The traces are also highly domain-specific (ML experiments on TinyStories/climbmix), which is both a strength (concentrated signal) and a limitation (narrow domain).

**Augmentation strategies to reach 10K-50K traces:**

1. **Paraphrase augmentation (5x multiplier):** Use a frontier model to rephrase each trace's hypothesis and reasoning in different ways while preserving the core logic. A single trace becomes 5 variants with different wording, emphasis, and explanation style.

2. **Counterfactual augmentation (2-3x multiplier):** For each accepted trace, generate a plausible-but-wrong alternative hypothesis that would have been rejected. For each rejected trace, generate the reasoning that explains why it failed. This doubles the preference pair count.

3. **Cross-machine transfer (1.5x):** Traces from Desktop (TinyStories) and Nodezero (climbmix) describe the same *type* of reasoning but in different contexts. Create cross-context variants: "What would this hypothesis look like if applied to climbmix instead of TinyStories?"

4. **Historical experiment mining:** The 110+ existing experiments in results.tsv can be retroactively converted to traces by reconstructing the reasoning from git commits, config diffs, and val_bpb deltas. This adds ~110 traces immediately.

5. **Synthetic trajectory generation:** Use a frontier model (Claude, GPT-5.4) to generate plausible experiment trajectories for hypothetical scenarios: "What experiments would you run if val_bpb was stuck at 0.5?" This is the lowest-quality augmentation but the highest-volume.

**Estimated corpus with augmentation:**

| Source | Traces |
|--------|--------|
| Year 1 raw traces | 2,760 |
| Historical experiment conversion | 110 |
| Paraphrase augmentation (5x) | 14,350 |
| Counterfactual augmentation (2x) | 5,740 |
| Cross-machine variants (1.5x) | 4,305 |
| **Total** | **~27,000** |

This is well within the productive range for fine-tuning a 1.5B-3B model.

### 7.4 Step-Level Rewards from PRM Scores

The ThinkPRM implementation guide (Goal 6) defines four verification dimensions that map directly to SWiRL-style step-level rewards:

| Trace Step | PRM Dimension | Reward Signal |
|------------|---------------|---------------|
| Hypothesis generation | Hypothesis Quality | Well-formed? References evidence? Avoids repeats? |
| Config specification | Config Validity | In sane ranges? Fits VRAM? Consistent? |
| Training execution | Training Stability | Loss converged? No NaN? Thermal OK? |
| Result interpretation | Result Interpretation | Improvement real? Statistically meaningful? |
| Accept/reject decision | (Composite) | Consistent with threshold? |

For SWiRL-style training, these step-level rewards replace the single outcome reward. The model learns not just "propose experiments that improve val_bpb" but "propose well-formed hypotheses, generate valid configs, and interpret results correctly."

---

## 8. Evaluation

### 8.1 Offline Evaluation (Before Deployment)

**Held-out test set:**
- Reserve 20% of traces (~550) as a test set, stratified by:
  - Machine (Desktop vs. Nodezero)
  - Outcome (accept vs. reject)
  - Category (architecture vs. hyperparameter vs. training vs. data)
  - Chain depth (root vs. refinement)

**Metrics:**

1. **Experiment proposal accuracy:** Given the experiment state, does the model propose an experiment that would be accepted? Measure against held-out traces.
   ```
   accuracy = (model_proposals_that_match_accepted_traces) / (total_proposals)
   ```

2. **Prediction calibration:** Does the model's predicted_effect.confidence correlate with actual outcome probability? Plot calibration curve.

3. **Hypothesis quality score:** Use the PRM to score the model's proposals on hypothesis quality, config validity, and reasoning coherence. Compare to human-authored traces.

4. **Diversity:** Does the model propose varied experiments or collapse to a single strategy? Measure entropy of hypothesis.category distribution.

5. **Reasoning trace quality:** BLEU/ROUGE against human-authored reasoning (crude) or frontier model scoring of reasoning quality (better).

### 8.2 Online Evaluation (After Deployment)

**The ultimate test:** Deploy the model as NemoClaw's hypothesis generator and measure:

1. **Accept rate:** What fraction of the model's proposed experiments beat the baseline?
   - Human baseline: ~30-40% of experiments are accepted
   - Target: match or exceed human accept rate

2. **Val_bpb improvement rate:** Average val_bpb delta per accepted experiment
   - If the model proposes smaller but more reliable improvements, that may be acceptable
   - If it proposes wild experiments that rarely work, the RL signal is insufficient

3. **Experiment efficiency:** How many experiments does the model need to find an improvement?
   - Human: ~3-5 experiments per improvement
   - Target: fewer than human

4. **Novel discoveries:** Does the model propose experiments that humans had not considered?
   - Track "out-of-distribution" proposals that succeed

### 8.3 A/B Testing Protocol

Once the model is deployed in NemoClaw:

1. Run 50% of experiments with the model's proposals, 50% with frontier model (Claude/GPT) proposals
2. Compare accept rates, val_bpb deltas, and experiment chain lengths
3. If the small model matches the frontier model, it validates the training pipeline
4. If it underperforms, analyze failure modes: wrong hypotheses? bad configs? incorrect predictions?

---

## 9. Implementation Roadmap

### Phase 1: SFT on Existing Traces (Weeks 1-2)

**Goal:** Establish baseline -- can a fine-tuned 1.5B model generate plausible experiment proposals?

**Steps:**
1. Convert existing 110+ experiments from results.tsv into trace format (retroactive conversion)
2. Format as SFT training data (instruction + response pairs)
3. Fine-tune Qwen2.5-1.5B-Instruct with QLoRA on RTX 3080 Ti
4. Evaluate: generate 50 experiment proposals, have a frontier model score them for quality

**Training config:** QLoRA, rank 16, all-linear targets, 3 epochs, ~2 hours total
**Expected outcome:** Model generates structurally valid experiment proposals but may lack strategic depth

**Data requirements:** ~110-200 SFT examples (existing experiments)
**VRAM:** ~3 GB (SFT is much lighter than GRPO)

### Phase 2: DPO with Preference Pairs (Weeks 3-4)

**Goal:** Teach the model to prefer better experiments over worse ones.

**Steps:**
1. Build preference pairs from sibling traces (same parent, one accepted, one rejected)
2. Augment with counterfactual pairs (frontier model generates alternatives)
3. DPO training on the SFT model
4. Evaluate: compare proposal quality to Phase 1

**Training config:** QLoRA, rank 16, beta=0.1, 1 epoch, ~4 hours
**Expected outcome:** Model avoids repeating known-bad approaches; better ranking of alternatives

**Data requirements:** ~200-500 preference pairs (from ~110 experiments + augmentation)
**VRAM:** ~4 GB (DPO needs policy + reference model, both quantized)

### Phase 3: RLVR with val_bpb as Verifiable Reward (Weeks 5-8)

**Goal:** Train the model with reinforcement learning using experiment outcomes as reward.

**Steps:**
1. Begin trace collection with the new REASONING_TRACE_FORMAT_SPEC (NemoClaw integration)
2. Accumulate 500+ new traces with full structured data
3. Set up GRPO training with val_bpb reward function
4. Train with 4 generations per prompt, KL coefficient 0.001
5. Monitor for reward hacking (model learning to game the format rather than improve val_bpb)

**Training config:** QLoRA GRPO, rank 16, 4 generations, ~10-24 hours per epoch
**Expected outcome:** Model proposes experiments that are more likely to improve val_bpb

**Data requirements:** 500-2,760 traces with verifiable outcomes
**VRAM:** ~5-8 GB (GRPO with QLoRA)

### Phase 4: Online RL with NemoClaw in the Loop (Weeks 9+)

**Goal:** Close the loop -- the model proposes, NemoClaw executes, results feed back into training.

**Steps:**
1. Deploy Phase 3 model as NemoClaw hypothesis generator (replacing frontier model API calls)
2. Each executed experiment generates a new trace with verifiable reward
3. Periodically retrain on accumulated traces (every ~100 new traces)
4. Implement SWiRL-style step-level rewards once PRM (Goal 6) is operational
5. A/B test against frontier model proposals

**Training config:** Periodic retraining, online data accumulation
**Expected outcome:** Self-improving loop -- better proposals lead to better experiments lead to better training data

**Infrastructure requirements:**
- Trace collection running on both Desktop and Nodezero
- Automated reward computation from experiment results
- Periodic model retraining (overnight on RTX 3080 Ti)
- Model serving for NemoClaw hypothesis generation (inference on RTX 3080 Ti or Nodezero)

### Phase 5: SWiRL Step-Level RL (Months 3+)

**Goal:** Move from outcome-only rewards to step-level rewards using the PRM.

**Steps:**
1. Train PRM per THINKPRM_IMPLEMENTATION_GUIDE
2. Decompose each trace into 5-6 steps with PRM scores
3. Apply SWiRL-style step-wise RL: reward each step independently
4. Key SWiRL insight: process-filtered data (good reasoning, any outcome) outperforms outcome-filtered data (correct answer, any reasoning)

**Expected outcome:** Model learns not just *what* experiments to propose but *how* to reason through them correctly at each step

---

## 10. Key Papers and Resources

### Core Papers

| Paper | ArXiv | Year | Relevance |
|-------|-------|------|-----------|
| DeepSeek-R1 | 2501.12948 | Jan 2025 | RLVR + GRPO for reasoning |
| DeepSeekMath (GRPO) | 2402.03300 | Feb 2024 | Original GRPO algorithm |
| SWiRL | 2504.04736 | Apr 2025 | Step-wise RL for multi-step reasoning |
| STaR | 2203.14465 | Mar 2022 | Self-taught reasoner bootstrapping |
| Quiet-STaR | 2403.09629 | Mar 2024 | Learning to think before speaking |
| ReST^EM | 2308.08998 | Aug 2023 | Reinforced self-training |
| ReST-MCTS* | -- | 2024 | Process reward guided tree search |
| ThinkPRM | 2504.16828 | Apr 2025 | 1% label efficiency for PRMs |
| REINFORCE++ | 2501.03262 | Jan 2025 | Simplified GRPO alternative |
| RLVR Correct Reasoning | 2506.14245 | Jun 2025 | Evidence RLVR teaches genuine reasoning |
| GRPO Dynamics | 2503.06639 | Mar 2025 | Mathematical analysis of GRPO |
| Off-Policy GRPO | 2505.22257 | May 2025 | Off-policy GRPO variant |
| Towards Reasoning in SLMs | 2502.11569 | Feb 2025 | Reasoning evidence at 1-3B scale |
| THINKSLM | EMNLP 2025 | 2025 | Reasoning in small language models |
| TinyLoRA | 2602.04118 | Feb 2026 | Extreme parameter efficiency |
| Reasoning Traces for Small Models | 2509.22230 | Sep 2025 | Tailored traces improve small model reasoning |

### Implementation Resources

| Resource | URL | Use |
|----------|-----|-----|
| trl (HuggingFace) | https://huggingface.co/docs/trl | GRPO/DPO/SFT training framework |
| trl GRPOTrainer | https://huggingface.co/docs/trl/grpo_trainer | GRPO implementation docs |
| GRPO Cookbook | https://huggingface.co/learn/cookbook/en/fine_tuning_llm_grpo_trl | Practical GRPO tutorial |
| OpenRLHF | https://github.com/OpenRLHF/OpenRLHF | Scalable RL framework |
| Minimal-RL | https://github.com/RLHFlow/Minimal-RL | Minimal REINFORCE implementation |
| Oxen.ai GRPO VRAM Guide | https://ghost.oxen.ai/grpo-vram-requirements-for-the-gpu-poor/ | Memory optimization |
| Illustrated GRPO | https://abderrahmanskiredj.github.io/the-illustrated-grpo/ | Visual GRPO explanation |
| GRPO Theory (Cameron Wolfe) | https://cameronrwolfe.substack.com/p/grpo | Deep GRPO explainer |

### Pre-trained Base Models

| Model | Size | Starting Point | HF ID |
|-------|------|---------------|-------|
| Qwen2.5-1.5B-Instruct | 1.5B | Reasoning-capable, instruction-tuned | `Qwen/Qwen2.5-1.5B-Instruct` |
| Qwen2.5-3B-Instruct | 3B | Best small reasoning model (84.74% GSM8K) | `Qwen/Qwen2.5-3B-Instruct` |
| DeepSeek-R1-Distill-Qwen-1.5B | 1.5B | Already fine-tuned for reasoning | `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` |
| Llama-3.2-1B-Instruct | 1B | Minimal size, good for rapid prototyping | `meta-llama/Llama-3.2-1B-Instruct` |

---

## Appendix A: GRPO VRAM Reference Table

Empirical measurements from Oxen.ai on H100 (80GB), baseline GRPO with 64 generations:

| Model Size | Peak VRAM (FP16) | With QLoRA (4-bit) | Fits RTX 3080 Ti? |
|------------|-------------------|--------------------|--------------------|
| 1B | ~10-12 GB | ~3-4 GB | Yes (comfortable) |
| 1.5B | ~14-16 GB | ~4-5 GB | Yes |
| 3B | ~20-25 GB | ~7-9 GB | Yes (tight, reduce generations to 4) |
| 7B | ~40-50 GB | ~14-18 GB | No (use Nodezero or cloud) |

**Key optimization levers:**
- Reduce `num_generations` from 64 to 4 (biggest single VRAM save)
- 4-bit NF4 quantization (4x reduction in model weight memory)
- Gradient checkpointing (trades compute for ~30% memory reduction)
- 8-bit optimizer states (halves optimizer memory)
- Reduce `max_completion_length` (less KV cache)
- `per_device_train_batch_size=1` with gradient accumulation

## Appendix B: Quick-Start Checklist

- [ ] Install dependencies: `pip install trl peft bitsandbytes transformers datasets accelerate`
- [ ] Download base model: `Qwen/Qwen2.5-1.5B-Instruct`
- [ ] Convert 110+ existing experiments to trace format
- [ ] Format traces as SFT dataset (instruction/response JSONL)
- [ ] Run Phase 1 SFT training (~2 hours)
- [ ] Evaluate: generate proposals, score with frontier model
- [ ] Build preference pairs from accept/reject sibling traces
- [ ] Run Phase 2 DPO training (~4 hours)
- [ ] Begin structured trace collection (NemoClaw integration)
- [ ] Accumulate 500+ structured traces
- [ ] Run Phase 3 GRPO training (~10-24 hours)
- [ ] Deploy as NemoClaw hypothesis generator
- [ ] Begin Phase 4 online RL loop

---

*Generated by autoresearch Wave 4 deep research agent, 2026-03-24*
