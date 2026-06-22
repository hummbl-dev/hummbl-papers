# Process Reward Models for HUMMBL/NemoClaw: Implementation Guide

**Date:** 2026-03-23
**Goal Reference:** Goal 6 — Process Reward Models for step verification
**Status:** Strategic Specification
**Hardware Target:** RTX 3080 Ti (12GB VRAM), llama3.1:8b default stack

---

## Table of Contents

1. [What Are PRMs and Why They Matter for HUMMBL](#1-what-are-prms-and-why-they-matter-for-hummbl)
2. [Architecture for NemoClaw](#2-architecture-for-nemoclaw)
3. [Training Data Strategy](#3-training-data-strategy)
4. [Model Selection](#4-model-selection)
5. [Implementation Roadmap](#5-implementation-roadmap)
6. [Evaluation](#6-evaluation)
7. [Key Papers and Resources](#7-key-papers-and-resources)

---

## 1. What Are PRMs and Why They Matter for HUMMBL

### 1.1 Step-Level Verification vs Outcome-Only Verification

There are two fundamental approaches to verifying whether an AI agent's reasoning chain is correct:

**Outcome Reward Models (ORMs)** evaluate only the final result. Did val_bpb improve? Did the experiment produce a valid number? ORMs are cheap to label (you only need final correctness) but blind to the process. An experiment might produce a good val_bpb number through a buggy training loop that happened to get lucky, or through a sound methodology that unluckily underperformed. ORMs cannot distinguish these cases.

**Process Reward Models (PRMs)** evaluate every intermediate step. Was the hypothesis well-formed? Was the config valid? Did training converge normally? Was the result interpreted correctly? PRMs provide dense, fine-grained feedback at each reasoning step, enabling:

- **Early error detection**: Catch a bad config before wasting 20 minutes of GPU time
- **Credit assignment**: Know which step in a multi-step experiment pipeline caused failure
- **Interpretable verification**: Each step gets a score with an explanation, creating an audit trail
- **Better search guidance**: Use step-level scores to prune bad experiment branches early, not just after full execution

OpenAI's foundational work ("Let's Verify Step by Step," May 2023, arXiv 2305.20050) demonstrated that process supervision significantly outperforms outcome supervision on the MATH dataset — their process-supervised model solved 78% of problems versus 72% for outcome-supervised. The PRM800K dataset they released contains 800,000 step-level human feedback labels across 101,599 solution samples.

### 1.2 The PRM Landscape in 2025-2026

The field has matured rapidly:

| Approach | Dataset/Method | Labels Required | Key Innovation |
|----------|---------------|----------------|----------------|
| **PRM800K** (OpenAI, 2023) | 800K human step labels | Massive human annotation | First large-scale PRM dataset |
| **Math-Shepherd** (2023) | Auto-annotated, 4x PRM800K size | Zero human labels | Monte Carlo rollout estimation |
| **ThinkPRM** (2025) | 1K synthetic verification CoTs | ~8K step labels (1% of PRM800K) | Generative verification via CoT |
| **ToolPRMBench** (Jan 2026) | Tool-using agent trajectories | Benchmark, not training set | First PRM benchmark for agents |
| **VPRMs** (Jan 2026) | RL with rule-based verifiers | Zero neural labels | Deterministic step verification |

The critical recent insight: **generative PRMs** (which produce a verification chain-of-thought) are catching up to and surpassing **discriminative PRMs** (which output a single score per step). ThinkPRM proved that a generative verifier fine-tuned on just 1K synthetic CoTs can beat discriminative models trained on the full 800K labels.

However, a counterpoint from recent unified evaluations (October 2025 survey, arXiv 2510.08049): across 14 diverse domains, discriminative ORMs actually performed on par with discriminative PRMs, and generative ORMs were the most robust overall. The takeaway is that PRMs shine most in complex multi-step reasoning where intermediate errors compound — exactly the profile of ML experiment pipelines.

### 1.3 Why ThinkPRM's 1% Label Efficiency Is a Game-Changer for Solo Founders

The traditional PRM training path requires massive human annotation: 800K+ step-level labels, each requiring a skilled annotator to judge whether a reasoning step is correct. This is feasible for OpenAI; it is not feasible for a solo founder.

ThinkPRM (arXiv 2504.16828, Khalifa et al., April 2025) breaks this barrier:

1. **Start with a reasoning model** (e.g., DeepSeek-R1-Distill-Qwen-1.5B)
2. **Use a powerful model (QwQ-32B-Preview) to generate synthetic verification CoTs** — the model reasons through each solution step and explains why it is correct or incorrect
3. **Filter these CoTs using only 8K step labels** from PRM800K as ground truth
4. **Fine-tune the reasoning model on ~1K high-quality filtered CoTs**
5. **Result**: ThinkPRM-1.5B outperforms discriminative PRMs trained on the full 800K labels by ~5 F1 points on ProcessBench; ThinkPRM-14B beats LLM-as-a-judge baselines by 8% on GPQA-Diamond

For HUMMBL, this means:
- You can generate synthetic verification data using frontier API models (Claude, GPT-5.4)
- You only need to manually verify ~100-200 experiment steps as ground truth
- A 1.5B model can serve as an effective PRM, running locally on the RTX 3080 Ti
- The entire training pipeline can run on consumer hardware

---

## 2. Architecture for NemoClaw

### 2.1 Where PRM Fits in the Supervisor-Worker Loop

NemoClaw's current architecture (v0.1.3) uses a file-based queue with READY/CANCEL sentinels, where the Worker owns state.json and val_bpb is the sole acceptance metric. The PRM adds a verification layer between experiment execution and acceptance:

```
┌─────────────────────────────────────────────────────────────┐
│                     SUPERVISOR (Nodezero)                     │
│                                                               │
│  1. Generate hypothesis                                       │
│  2. Create experiment config                                  │
│  3. ──► PRM CHECKPOINT A: Score hypothesis + config ◄──       │
│     │   (Is hypothesis well-formed? Is config valid?)         │
│     │   Score < threshold? → Reject, generate new hypothesis  │
│     │   Score >= threshold? → Proceed to execution            │
│  4. Write task to queue (READY sentinel)                      │
│                                                               │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    WORKER (Desktop/RTX 3080 Ti)               │
│                                                               │
│  5. Read task, execute training run                           │
│  6. ──► PRM CHECKPOINT B: Score training trace ◄──            │
│     │   (Did loss converge? Any NaN/explosion? Thermal OK?)   │
│     │   Score < threshold? → Flag anomaly, continue           │
│  7. Record results (val_bpb, metadata)                        │
│  8. Write results to state.json                               │
│                                                               │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   SUPERVISOR (Nodezero)                        │
│                                                               │
│  9. Read results                                              │
│  10. ──► PRM CHECKPOINT C: Score result interpretation ◄──    │
│      │   (Is improvement real? Statistical noise? Overfit?)   │
│      │   Produces confidence score alongside val_bpb delta    │
│  11. Accept/Reject based on val_bpb delta AND PRM confidence  │
│  12. Update experiment tree, select next experiment            │
│      (PRM scores inform tree search priority)                 │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 2.2 Four Verification Dimensions

The PRM scores each experiment step along four dimensions, each producing a score from 0.0 to 1.0:

**Dimension 1: Hypothesis Quality (Checkpoint A)**
- Is the hypothesis falsifiable?
- Does it reference prior experimental evidence?
- Is the proposed change architecturally coherent?
- Does it avoid repeating previously failed approaches?
- Example: "Increase learning rate from 3e-4 to 1e-3 because prior experiment showed loss plateau" → Score 0.85 (references evidence, clear mechanism)
- Example: "Try random architecture change" → Score 0.2 (no rationale, unfalsifiable)

**Dimension 2: Config Validity (Checkpoint A)**
- Are all required fields present and typed correctly?
- Are hyperparameters within sane ranges? (LR between 1e-6 and 1e-1, batch size power of 2, etc.)
- Does the config fit in available VRAM given model size?
- Does it conflict with known-bad configurations from prior experiments?
- This dimension can be partly rule-based (JSON schema validation) with PRM handling soft constraints

**Dimension 3: Training Stability (Checkpoint B)**
- Did loss decrease monotonically (approximately)?
- Any NaN values, loss spikes, or gradient explosions?
- Did training complete within expected wall-clock time?
- GPU temperature remained below thermal threshold (85C per NemoClaw spec)?
- Were checkpoints saved at expected intervals?

**Dimension 4: Result Interpretation (Checkpoint C)**
- Is the reported val_bpb improvement statistically meaningful given noise floor?
- Does improvement generalize or is it specific to one eval batch?
- Is the magnitude consistent with the type of change made? (A LR tweak producing 10% improvement is suspicious)
- Does the result contradict established scaling laws or prior validated results?

### 2.3 Using PRM Scores to Guide Experiment Selection

PRM scores are not just accept/reject gates. They feed back into the experiment tree search:

**Priority scoring for next experiment selection:**
```
priority = (
    0.4 * hypothesis_quality_score +
    0.3 * expected_val_bpb_improvement +
    0.2 * novelty_score +               # How different from prior experiments
    0.1 * estimated_compute_cost_inverse  # Prefer cheaper experiments
)
```

**Experiment branch pruning:**
- If 3 consecutive experiments in a branch all score < 0.4 on hypothesis quality, deprioritize that branch
- If a branch's average result_interpretation score is < 0.3, the improvements may be noise — require higher val_bpb delta for acceptance

**Adaptive thresholds:**
- Early exploration phase: Accept experiments with PRM score >= 0.3 (cast wide net)
- Refinement phase: Require PRM score >= 0.6 (focus on promising directions)
- Threshold auto-adjusts based on experiment budget remaining

### 2.4 Integration with NemoClaw Failure Codes

PRM verification integrates with NemoClaw's 21 failure codes (ARNC-001 through ARNC-021):

| PRM Detection | NemoClaw Code | Action |
|---------------|---------------|--------|
| Config VRAM exceeds 12GB estimate | ARNC-003 (resource) | Reject before execution |
| Training loss NaN detected | ARNC-007 (training) | Terminate early, save compute |
| Hypothesis repeats failed approach | ARNC-015 (duplicate) | Reject, suggest alternative |
| Result interpretation suspicious | ARNC-019 (validation) | Flag for human review |
| Thermal threshold predicted breach | ARNC-012 (thermal) | Delay or reduce batch size |

The circuit breaker (3 consecutive identical failures) now also considers PRM scores: if the PRM flags the same failure mode 3 times, the supervisor changes strategy rather than retrying.

---

## 3. Training Data Strategy

### 3.1 Converting Existing Autoresearch Results into PRM Training Data

Every completed autoresearch experiment already contains the raw material for PRM training data. The experiment trace format (per Goal 5: Reasoning Trace Capture) captures:

```
hypothesis → config → training_log → result → decision
```

To convert this into PRM training data, each trace is decomposed into steps, and each step is labeled as correct (+1) or incorrect (-1):

**Step decomposition for a single experiment:**

```json
{
  "experiment_id": "exp_0047",
  "steps": [
    {
      "step_id": 1,
      "type": "hypothesis",
      "content": "GLA (Gated Linear Attention) may break the val_bpb plateau because it provides a different attention mechanism than the standard softmax attention that has been exhaustively tuned.",
      "label": null,
      "context": {
        "prior_best_val_bpb": 0.4646,
        "prior_approaches_tried": ["sigmoid_gating_init0", "sigmoid_gating_init2", "lr_sweep", "depth_sweep"]
      }
    },
    {
      "step_id": 2,
      "type": "config",
      "content": {"model": "gla_transformer", "lr": 3e-4, "batch_size": 32, "layers": 6, "d_model": 256, "dataset": "TinyStories"},
      "label": null,
      "context": {"vram_estimate_gb": 8.2, "estimated_train_time_min": 18}
    },
    {
      "step_id": 3,
      "type": "training_trace",
      "content": "Step 100: loss=2.31, Step 500: loss=1.45, Step 1000: loss=0.89, Step 2000: loss=0.52, Step 3000: loss=0.48 (converged)",
      "label": null,
      "context": {"gpu_temp_max": 67, "wall_time_min": 16.2, "nan_count": 0}
    },
    {
      "step_id": 4,
      "type": "result_interpretation",
      "content": "val_bpb = 0.4612, improvement of 0.0034 over prior best. Improvement is small but consistent across eval batches.",
      "label": null,
      "context": {"val_bpb": 0.4612, "delta": -0.0034, "eval_batch_std": 0.0008}
    },
    {
      "step_id": 5,
      "type": "decision",
      "content": "ACCEPT: val_bpb improved. New best. Continue exploring GLA variants.",
      "label": null,
      "context": {"accepted": true, "min_delta_threshold": 0.001}
    }
  ]
}
```

### 3.2 Labeling Strategy: Which 1% to Label

Following ThinkPRM's approach, you do not need to label every step of every experiment. The strategy:

**Phase 1: Anchor labels (50-100 experiments, ~250-500 step labels)**

Manually label the steps of experiments that represent clear signal:
- **Definite positives**: Experiments that produced validated val_bpb improvements (e.g., the LR re-tuning that achieved 0.4646)
- **Definite negatives**: Experiments with obvious failures (sigmoid gating failures, NaN explosions, configs that OOM'd)
- **Edge cases**: Experiments where val_bpb improved slightly but the methodology was questionable

Priority for manual labeling:
1. Experiments at branch points in the experiment tree (where a decision led to a new direction)
2. Experiments that contradicted expectations (good hypothesis, bad result or vice versa)
3. The most recent 20 experiments (freshest signal about current frontier)

**Phase 2: Synthetic label generation (bulk)**

Use a frontier model (Claude via API or GPT-5.4) to generate verification CoTs for the remaining experiments:

```
PROMPT: You are a process reward model for ML experiments. For each step
in this experiment trace, generate a detailed verification chain-of-thought
explaining whether the step is correct or incorrect, and assign a score
from 0.0 to 1.0.

[experiment trace here]

For each step, output:
- verification_cot: Your reasoning about whether this step is sound
- score: 0.0 (definitely wrong) to 1.0 (definitely correct)
- label: +1 (correct) or -1 (incorrect)
```

**Phase 3: Filter synthetic labels against anchor labels**

Where synthetic labels disagree with manual anchor labels, discard the synthetic label. This filtering step is critical — ThinkPRM's quality comes from filtering 8K labels down to 1K high-quality CoTs.

**Label budget estimate for HUMMBL:**
- 110+ experiments completed as of March 2026
- ~5 steps per experiment = ~550 total steps
- Manual labels needed: ~100 steps (20% of total, but these are carefully selected anchor points)
- Synthetic labels: remaining ~450 steps
- After filtering: ~200-300 high-quality training CoTs
- This is comparable to ThinkPRM's 1K CoTs — sufficient for fine-tuning

### 3.3 Data Format Specification

**Input format for PRM training (JSONL):**

```json
{
  "experiment_id": "exp_0047",
  "step_id": 2,
  "step_type": "config",
  "step_content": "Config: gla_transformer, lr=3e-4, batch=32, layers=6, d_model=256, dataset=TinyStories. Estimated VRAM: 8.2GB. Estimated train time: 18 min.",
  "context": "Prior best val_bpb: 0.4646. Previous failed approaches: sigmoid_gating (both init schemes). Hypothesis: GLA may break plateau via different attention mechanism.",
  "verification_cot": "Let me verify this configuration step by step.\n\n1. Model architecture (gla_transformer): This is a valid architecture choice. GLA has shown promise in recent literature for efficient attention. The hypothesis connecting it to breaking the plateau is reasonable since all prior attempts used standard softmax attention.\n\n2. Learning rate (3e-4): This is within the standard range for transformer training. Given that the prior best used a similar LR, this is a conservative but reasonable choice for a first GLA experiment.\n\n3. Batch size (32): Standard for this model size on TinyStories. No issues.\n\n4. Model dimensions (layers=6, d_model=256): Comparable to prior experiments, which allows fair comparison. Good experimental design.\n\n5. VRAM estimate (8.2GB): Well within the 12GB budget of the RTX 3080 Ti, leaving headroom for KV cache and overhead.\n\n6. Time estimate (18 min): Reasonable for this configuration.\n\nThis configuration is well-designed: it changes one variable (attention mechanism) while holding others constant, enabling clean comparison. No red flags.",
  "score": 0.88,
  "label": 1
}
```

**Verification CoT format for generative PRM inference:**

```
<|verification_start|>
Step: [step content]
Context: [relevant prior information]

Verification:
[Chain-of-thought reasoning about correctness]

Score: [0.0-1.0]
Verdict: [CORRECT/INCORRECT/UNCERTAIN]
<|verification_end|>
```

---

## 4. Model Selection

### 4.1 Can a Small Model (1-3B) Serve as an Effective PRM?

Yes. ThinkPRM-1.5B (fine-tuned from DeepSeek-R1-Distill-Qwen-1.5B) demonstrated:
- Outperforms discriminative PRMs by ~5 F1 points on ProcessBench
- Surpasses LLM-as-a-judge using the same 1.5B base model
- Gains 70+ F1 points after fine-tuning (from near-random to highly effective)

The key insight is that **verification is easier than generation**. A 1.5B model that cannot write good ML experiment configs can still effectively verify whether a config is sound, because verification requires pattern matching against known good/bad patterns rather than creative generation.

For HUMMBL's domain (ML experiment verification), the reasoning is even simpler than math: configs are structured data with well-defined valid ranges, training curves have known healthy/unhealthy shapes, and result interpretation follows standard statistical reasoning.

### 4.2 What Fits in 12GB VRAM on RTX 3080 Ti

**Inference (PRM verification at runtime):**

| Model Size | Quantization | VRAM Usage | Fits with Training? | Speed Estimate |
|-----------|-------------|-----------|---------------------|---------------|
| 1.5B | Q4_0 | ~1.2 GB | Yes, alongside active training | ~250 tok/s |
| 1.5B | FP16 | ~3.0 GB | Yes, tight during training | ~180 tok/s |
| 3B | Q4_0 | ~2.2 GB | Yes, alongside active training | ~170 tok/s |
| 8B | Q4_0 | ~5.5 GB | Only when training is idle | ~133 tok/s |
| 8B | FP16 | ~16 GB | No — exceeds VRAM | N/A |
| 14B | Q4_0 | ~8.5 GB | No — conflicts with training | ~75 tok/s |

**Recommended inference model**: 1.5B-3B quantized PRM running alongside active training, or 8B PRM running during supervisor planning phase (when GPU is idle between experiments).

**Training (fine-tuning the PRM):**

| Model Size | Method | VRAM Required | Fits RTX 3080 Ti? | Training Time (est.) |
|-----------|--------|--------------|-------------------|---------------------|
| 1.5B | Full fine-tune | ~8 GB | Yes | ~30 min on 1K CoTs |
| 1.5B | QLoRA | ~4 GB | Yes, comfortably | ~20 min on 1K CoTs |
| 3B | QLoRA | ~6 GB | Yes | ~45 min on 1K CoTs |
| 8B | QLoRA | ~10 GB | Yes, tight | ~2 hrs on 1K CoTs |
| 8B | Full fine-tune | ~32 GB | No | N/A |
| 14B | QLoRA | ~14 GB | No | N/A |

**Recommended training approach**: QLoRA fine-tuning of a 1.5B or 3B reasoning model. This fits comfortably in 12GB with room to spare, trains in under an hour, and produces a PRM that runs alongside active experiments.

### 4.3 Using llama3.1:8b as the PRM

Since llama3.1:8b is already the production default on the RTX 3080 Ti (133 tok/s, 6.9GB VRAM with q4_0 KV cache), there are two approaches:

**Approach A: Prompted PRM (Phase 1, no training required)**

Use the existing llama3.1:8b with a carefully designed scoring prompt. The model acts as a "zero-shot PRM" by generating verification reasoning and outputting scores.

Pros:
- Zero additional infrastructure
- Immediate deployment
- Uses existing Ollama setup
- No fine-tuning compute needed

Cons:
- 8B model uses 6.9GB VRAM — cannot run during active training
- Verification quality will be lower than a fine-tuned PRM
- Prompt engineering required to get consistent scoring
- ~133 tok/s means ~3-5 seconds per verification step

**Approach B: Fine-tuned PRM (Phase 2)**

QLoRA fine-tune llama3.1:8b on autoresearch verification CoTs, then serve the adapter through Ollama.

Pros:
- Better verification quality than prompted
- Leverages existing infrastructure
- Ollama supports LoRA adapters

Cons:
- 10GB VRAM for QLoRA training — tight but feasible
- Must schedule training when GPU is idle
- 6.9GB at inference — still cannot run during active training

**Approach C: Dedicated small PRM (Phase 2-3, recommended)**

Fine-tune a 1.5B reasoning model (DeepSeek-R1-Distill-Qwen-1.5B) as a dedicated PRM. Run it alongside llama3.1:8b.

Pros:
- Only 1.2GB VRAM at Q4_0 — runs alongside everything
- Can verify in real-time during training
- ThinkPRM proved 1.5B is effective
- Total VRAM: 6.9GB (8b) + 1.2GB (PRM) = 8.1GB — fits with 3.9GB headroom

Cons:
- New model to manage in the stack
- Requires fine-tuning pipeline setup
- 1.5B may struggle with complex reasoning about novel architectures

### 4.4 Inference Cost per Verification Step

**Per-step verification cost estimate (1.5B Q4_0 PRM):**
- Input tokens: ~200 (step content + context)
- Output tokens: ~300 (verification CoT + score)
- Speed: ~250 tok/s
- Wall time: ~2 seconds per step
- VRAM: 1.2 GB (constant)

**Per-experiment verification cost (5 steps):**
- Wall time: ~10 seconds total
- VRAM: 1.2 GB (constant, running as background service)
- Compared to 15-20 minute experiment runtime: negligible overhead (< 1%)

**Per-experiment verification cost (8B prompted PRM):**
- Wall time: ~15-25 seconds total (5 steps, longer CoTs)
- VRAM: 6.9 GB (must be sole GPU occupant)
- Only viable between experiments, not during training

---

## 5. Implementation Roadmap

### Phase 1: Prompted PRM (Week 1-2)

**Goal:** Get step-level verification running immediately with zero training.

**Implementation:**

1. **Create PRM scoring prompt** (`autoresearch-pipeline/prompts/prm_verify.txt`):
   ```
   You are a Process Reward Model for ML experiments. Your job is to
   verify each step in an experiment trace and assign a correctness score.

   For the given step, analyze:
   - Is the reasoning sound?
   - Are there any red flags or errors?
   - Is this consistent with prior experimental evidence?

   Output format:
   REASONING: [your verification chain-of-thought]
   SCORE: [0.0 to 1.0]
   VERDICT: [CORRECT / INCORRECT / UNCERTAIN]
   FLAGS: [list any specific concerns]
   ```

2. **Add PRM verification to NemoClaw supervisor loop**:
   - Before task dispatch: verify hypothesis + config (Checkpoint A)
   - After result receipt: verify result interpretation (Checkpoint C)
   - Use llama3.1:8b via Ollama API during planning phase (GPU idle)

3. **Log all PRM scores to bus** as structured entries:
   ```json
   {"type": "prm_verification", "experiment_id": "exp_0048",
    "checkpoint": "A", "scores": {"hypothesis": 0.82, "config": 0.91},
    "verdict": "PROCEED", "timestamp": "2026-03-24T02:15:00Z"}
   ```

4. **Collect baseline data**: Run 20-30 experiments with prompted PRM verification, logging scores alongside actual outcomes. This becomes the ground truth for evaluating whether PRM scores correlate with val_bpb improvements.

**Deliverables:**
- `prm_verify.py` — Ollama-based verification module
- `prm_prompts/` — Prompt templates for each checkpoint
- PRM score logs in bus format
- Baseline correlation data (PRM score vs val_bpb outcome)

**Hardware requirements:** None beyond existing stack. Uses llama3.1:8b during idle GPU windows.

### Phase 2: Fine-Tuned PRM on Autoresearch Traces (Week 3-6)

**Goal:** Train a dedicated 1.5B PRM on autoresearch verification data.

**Implementation:**

1. **Prepare training data**:
   - Export all completed experiment traces to JSONL format
   - Manually label anchor set: 100 steps from 20 key experiments
   - Generate synthetic verification CoTs using Claude API (batch of 450+ steps)
   - Filter synthetic CoTs against anchor labels
   - Target: 200-300 high-quality training CoTs

2. **Set up fine-tuning pipeline**:
   - Download DeepSeek-R1-Distill-Qwen-1.5B base model
   - Configure QLoRA: rank=16, alpha=32, target_modules=["q_proj","v_proj"]
   - Training config: batch_size=1, gradient_accumulation=4, lr=2e-4, epochs=3
   - Gradient checkpointing enabled
   - Estimated VRAM: ~4GB, estimated time: ~20-30 minutes

3. **Train the PRM**:
   - Schedule training during overnight idle window
   - Use Unsloth or HuggingFace PEFT for QLoRA
   - Export trained adapter
   - Convert to Ollama-compatible GGUF format

4. **Deploy alongside existing stack**:
   - Register as `prm-1.5b` in Ollama
   - VRAM allocation: 1.2GB (Q4_0) — fits alongside llama3.1:8b (6.9GB), total 8.1GB
   - Update `prm_verify.py` to use fine-tuned model
   - Enable real-time verification during training (Checkpoint B)

5. **A/B test against Phase 1 prompted PRM**:
   - Run 20 experiments with each approach
   - Compare PRM score correlation with val_bpb outcomes
   - Measure false positive/negative rates

**Deliverables:**
- Fine-tuned PRM-1.5B model (Ollama GGUF)
- Training pipeline scripts
- A/B test results
- Updated VRAM packing config (3-model stack: 8b + PRM + moondream)

### Phase 3: Full ThinkPRM with Minimal Labels (Week 7-12)

**Goal:** Implement the complete ThinkPRM approach with continuous improvement.

**Implementation:**

1. **Scale training data**:
   - As more experiments complete, continuously add to training corpus
   - Implement active learning: prioritize labeling experiments where PRM is most uncertain
   - Target: 500+ high-quality CoTs by week 12

2. **Implement hierarchical verification**:
   - Dimension-specific sub-models or prompts for each of the 4 verification dimensions
   - Aggregate scores with learned weights (initially use the 0.4/0.3/0.2/0.1 priority weights from Section 2.3)

3. **Integrate with experiment tree search**:
   - PRM scores feed into experiment priority queue
   - Implement branch pruning based on cumulative PRM scores
   - Adaptive threshold adjustment based on experiment budget

4. **Cross-dataset validation**:
   - Train PRM on TinyStories experiment traces
   - Test on climbmix experiment traces (Nodezero)
   - Measure generalization: does the PRM trained on one dataset's experiments transfer?

5. **Continuous PRM improvement loop**:
   ```
   experiments run → results logged → PRM evaluates →
   PRM predictions compared to outcomes → disagreements flagged →
   human reviews disagreements → new anchor labels →
   PRM retrained → better PRM → repeat
   ```

**Deliverables:**
- Continuously improving PRM with expanding training data
- Experiment tree search guided by PRM scores
- Cross-dataset PRM generalization results
- Automated PRM retraining pipeline

---

## 6. Evaluation

### 6.1 How to Measure PRM Quality

**Primary metric: Step-level accuracy**
- For each manually labeled step, does the PRM agree?
- Measure as F1 score (balancing precision and recall)
- Target: F1 > 0.75 for Phase 2, F1 > 0.85 for Phase 3

**Secondary metric: Ranking quality**
- Given two experiments, does the PRM rank the better one (by val_bpb) higher?
- Measure as Kendall's tau or Spearman's rho correlation
- Target: rho > 0.5 for Phase 2, rho > 0.7 for Phase 3

**Calibration metric: Score reliability**
- When PRM says score = 0.8, is the step correct ~80% of the time?
- Plot calibration curve (predicted score vs actual correctness rate)
- Well-calibrated PRM enables threshold-based decision making

### 6.2 Correlation Between PRM Scores and Actual val_bpb Improvements

The critical test: do high PRM scores predict successful experiments?

**Evaluation protocol:**

1. Run N experiments (target N >= 30 for statistical power)
2. For each experiment, record:
   - PRM score at Checkpoint A (pre-execution)
   - PRM score at Checkpoint C (post-execution)
   - Actual val_bpb delta
   - Whether experiment was accepted/rejected by NemoClaw

3. Compute:
   - Pearson correlation: PRM_score_A vs val_bpb_delta
   - Pearson correlation: PRM_score_C vs val_bpb_delta
   - ROC-AUC: PRM as binary classifier for "experiment improves val_bpb"
   - Precision@K: Among top-K PRM-scored experiments, what fraction actually improved val_bpb?

4. Target metrics:
   - Correlation > 0.3 indicates useful signal (Phase 1)
   - Correlation > 0.5 indicates strong guidance (Phase 2)
   - ROC-AUC > 0.7 indicates reliable binary classification
   - Precision@5 > 0.6 means the PRM's top picks are usually good

**Visualization:**
- Scatter plot: PRM score (x) vs val_bpb delta (y)
- Confusion matrix: PRM verdict vs actual outcome
- Score distribution: histogram of PRM scores for successful vs failed experiments

### 6.3 A/B Test: PRM-Guided vs Random Experiment Selection

The ultimate test of PRM value: does it help you find better experiments faster?

**Protocol:**

1. **Control arm (random):** Supervisor generates experiment candidates and selects uniformly at random
2. **Treatment arm (PRM-guided):** Supervisor generates candidates, PRM scores them, highest-scoring candidate is selected

3. **Run 20 experiments in each arm** (can run interleaved)

4. **Measure:**
   - Average val_bpb improvement per experiment
   - Number of experiments to reach a new best val_bpb
   - GPU-hours to reach a new best val_bpb
   - Fraction of experiments that improved val_bpb (hit rate)

5. **Expected outcome:**
   - PRM-guided should have higher hit rate (fewer wasted experiments)
   - PRM-guided should reach new best val_bpb in fewer experiments
   - If PRM-guided is not significantly better, the PRM needs more training data or the domain is too noisy

**Success criteria:**
- PRM-guided hit rate > 1.5x random hit rate
- PRM-guided reaches new best in < 70% of the experiments random needs
- These translate directly to GPU-hours saved — with 15-20 min per experiment, even a 2x hit rate improvement saves hours of overnight compute

---

## 7. Key Papers and Resources

### Foundational Papers

- **"Let's Verify Step by Step"** (Lightman et al., OpenAI, May 2023) — [arXiv 2305.20050](https://arxiv.org/abs/2305.20050). The foundational PRM paper. Demonstrates process supervision outperforms outcome supervision on MATH. Releases PRM800K dataset.

- **"Math-Shepherd: Verify and Reinforce LLMs Step-by-Step without Human Annotations"** (Wang et al., Dec 2023) — [arXiv 2312.08935](https://arxiv.org/abs/2312.08935). Automatic PRM annotation via Monte Carlo rollouts. 4x larger than PRM800K with no human labels.

- **"Process Reward Models That Think" (ThinkPRM)** (Khalifa et al., April 2025) — [arXiv 2504.16828](https://arxiv.org/abs/2504.16828). The key paper for this implementation. 1% label efficiency via generative verification CoTs. Models released at [github.com/mukhal/ThinkPRM](https://github.com/mukhal/ThinkPRM).

### Recent Advances (2025-2026)

- **"The Lessons of Developing Process Reward Models in Mathematical Reasoning"** (Jan 2025) — [arXiv 2501.07301](https://arxiv.org/abs/2501.07301). Practical lessons from PRM development.

- **"A Survey of Process Reward Models"** (Oct 2025) — [arXiv 2510.08049](https://arxiv.org/abs/2510.08049). Comprehensive survey covering data generation, PRM construction, and applications across math, code, text, multimodal, robotics, and agents.

- **"Beyond Outcome Verification: Verifiable Process Reward Models for Structured Reasoning"** (Jan 2026) — [arXiv 2601.17223](https://arxiv.org/abs/2601.17223). VPRMs with deterministic rule-based verifiers. Relevant for combining PRM with NemoClaw's rule-based validation.

- **"ToolPRMBench: Evaluating and Advancing Process Reward Models for Tool-using Agents"** (Jan 2026) — [arXiv 2601.12294](https://arxiv.org/abs/2601.12294). First benchmark for PRMs on agent trajectories. Code at [github.com/David-Li0406/ToolPRMBench](https://github.com/David-Li0406/ToolPRMBench).

- **"Generalizable Process Reward Models via Formally Verified Training Data"** (May 2025) — [arXiv 2505.15960](https://arxiv.org/abs/2505.15960). Formal verification for cross-task PRM generalization.

### Datasets

- **PRM800K**: [github.com/openai/prm800k](https://github.com/openai/prm800k) — 800K step-level labels on MATH solutions
- **Math-Shepherd**: Auto-annotated, 4x PRM800K — available via paper
- **ThinkPRM training data**: [github.com/mukhal/ThinkPRM](https://github.com/mukhal/ThinkPRM) — 1K filtered verification CoTs

### Tools and Infrastructure

- **Unsloth**: [unsloth.ai](https://unsloth.ai) — Fast QLoRA fine-tuning, recommended for 1.5B-8B models on consumer GPUs
- **HuggingFace PEFT**: LoRA/QLoRA adapter training library
- **Ollama**: Local model serving, supports GGUF models and LoRA adapters
- **vLLM**: High-throughput inference, supports PRM scoring at scale (if upgrading from Ollama)

---

## Appendix A: Quick-Start Checklist

- [ ] Write PRM scoring prompt for llama3.1:8b (Phase 1)
- [ ] Add Checkpoint A verification to supervisor planning loop
- [ ] Add Checkpoint C verification to result acceptance loop
- [ ] Log PRM scores to NemoClaw bus
- [ ] Run 30 experiments with prompted PRM, collect correlation data
- [ ] Export experiment traces to JSONL training format
- [ ] Manually label 100 anchor steps from 20 key experiments
- [ ] Generate synthetic verification CoTs via Claude API
- [ ] Filter synthetic CoTs against anchor labels
- [ ] Download DeepSeek-R1-Distill-Qwen-1.5B
- [ ] QLoRA fine-tune on filtered CoTs
- [ ] Convert to GGUF, deploy as `prm-1.5b` in Ollama
- [ ] A/B test: prompted vs fine-tuned PRM
- [ ] A/B test: PRM-guided vs random experiment selection
- [ ] Measure PRM score correlation with val_bpb improvements

## Appendix B: VRAM Budget

```
Production 3-model stack (Phase 2+):
  llama3.1:8b (Q4_0)      = 6.9 GB   (general inference)
  prm-1.5b (Q4_0)         = 1.2 GB   (verification)
  moondream (vision)       = 1.8 GB   (vision tasks)
  ─────────────────────────────────
  Total                    = 9.9 GB
  Headroom                 = 2.3 GB   (KV cache, overhead)
  RTX 3080 Ti capacity     = 12.0 GB

Training (overnight, exclusive GPU access):
  QLoRA fine-tune 1.5B     = ~4 GB    (20-30 min)
  QLoRA fine-tune 8B       = ~10 GB   (2 hrs, tight)
```

---

*Report generated 2026-03-23 for HUMMBL Autoresearch Pipeline — Goal 6: Process Reward Models*
