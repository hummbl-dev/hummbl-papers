# Small Language Model Training Techniques and Architectures (2025-2026)

**Wave 4 Deep Research Report -- Autoresearch Project**
**Date:** 2026-03-23
**Context:** 30-60M param models, TinyStories + climbmix datasets, RTX 3080 Ti, current best val_bpb 0.4646 after 110+ experiments

---

## Executive Summary

After surveying the 2025-2026 landscape of small language model training, six high-confidence strategies emerge for breaking the 0.4646 BPB plateau:

1. **Switch to the Muon optimizer** -- 2x compute efficiency over AdamW, proven at small scale
2. **Adopt WSD learning rate scheduling** -- eliminates the need to pre-specify training length, enables continuous improvement and data mixing during decay
3. **Go deeper and thinner** -- 32 layers with hidden_dim 384 beats 12 layers with hidden_dim 512 at ~70M params
4. **Implement knowledge distillation** via MiniPLM-style difference sampling from a larger teacher
5. **Curate and mix data** -- 30% synthetic + 70% natural is the empirically optimal ratio; deduplicate aggressively
6. **Over-train massively** -- MiniCPM finds 192:1 token-to-parameter ratio optimal, far beyond Chinchilla's 20:1

> **Reconciliation note (2026-06-19):** These recommendations are evidence-based targets from the 2025 literature, not yet validated as the default recipe for the local RTX 3080 Ti fleet. A provisional canonical recipe and validation gates are in `founder-mode/docs/research/2026-06-19_slm-recipe-reconciliation.md` (relative to the founder-mode repo). Promote items here only after A/B validation on the 3080 Ti.

---

## 1. Training Techniques

### 1.1 Optimizer: Muon Over AdamW

The Muon optimizer, based on matrix orthogonalization, has emerged as a significant advance for LM training. Key findings from 2025:

- **~2x compute efficiency** over AdamW at compute-optimal training. Muon achieves comparable performance while requiring only ~52% of training FLOPs.
- Muon's superiority comes from better optimization of associative memory parameters (Value/Output attention weights and FFNs), yielding a more isotropic singular spectrum that optimizes tail classes more effectively.
- Two critical techniques for stability: (1) add weight decay, (2) carefully adjust per-parameter update scale.
- The nanoGPT speedrun community has validated Muon extensively -- it is a core ingredient in records that dropped training time from 45 minutes to under 3 minutes.

**Actionable:** Replace AdamW with Muon for hidden layer parameters. Keep AdamW for embedding layers. This is likely the single highest-impact change available.

References:
- [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982)
- [Muon Outperforms Adam in Tail-End Associative Memory Learning](https://arxiv.org/abs/2509.26030)
- [NanoGPT Speedrun](https://github.com/KellerJordan/modded-nanogpt)

### 1.2 Knowledge Distillation

Two paradigms are now practical for small model pre-training:

**MiniPLM (ICLR 2025):** A pre-training distillation framework that refines training data distribution using teacher knowledge. Key innovation is "Difference Sampling" -- selecting training instances where the teacher assigns high probability but a small reference model assigns low probability. This promotes data difficulty and diversity without requiring online teacher inference.

- Offline teacher inference: run once, distill into multiple student models
- Cross-family: no tokenizer matching needed
- Demonstrated improvements on 9 downstream tasks while reducing pre-training compute

**Curriculum-Based Distillation (POCL):** Progressive overload curriculum learning for white-box KD. Ranks training samples by difficulty, introduces subsets from easy to hard. Plug-and-play framework.

**Two-Stage Curriculum SFT:** Stage 1 trains on reasoning-enhanced data with explicit chain-of-thought; Stage 2 shifts to standard prompt-response pairs. The model implicitly applies learned reasoning.

**Actionable:** Use a larger model (e.g., Llama-3-8B) to score TinyStories training data by loss. Prioritize examples where the large model's loss is low but a baseline 33M model's loss is high. This creates a naturally difficulty-weighted curriculum at zero additional training cost.

References:
- [MiniPLM: Knowledge Distillation for Pre-Training Language Models](https://arxiv.org/abs/2410.17215)
- [POCL: Curriculum Learning for Knowledge Distillation](https://arxiv.org/html/2506.05695v1)

### 1.3 Curriculum Learning

Evidence supports data ordering matters:

- **Easy-to-hard scheduling** improves convergence, particularly for small models with limited capacity
- MiniCPM's three-stage approach (stable training on bulk data -> decay with high-quality data -> SFT) is a form of implicit curriculum
- SmolLM2's multi-stage training mixes web text with specialized math/code data at different stages

**Actionable:** For TinyStories, sort by story complexity (sentence count, vocabulary diversity, narrative structure). Train on simple stories first, complex stories later. For climbmix, implement domain-based curriculum.

### 1.4 Data Quality vs. Quantity

Strong evidence that quality dominates at small scale:

- Deduplication reduces memorized text emission by 10x and requires fewer training steps for same accuracy
- SmolLM2-135M trained on 2 trillion tokens with aggressive curation (FineWeb-Edu, DCLM, Stack)
- Phi series pioneered "textbook quality" synthetic data -- but pure synthetic underperforms natural data
- **Optimal mixture: ~30% synthetic + 70% natural data** (validated across scales)
- Textbook-style data works best at <5% of mixture for small configurations
- Key insight: unigram coverage doesn't explain performance; complex diversity-quality tradeoffs matter

**Actionable:** Deduplicate TinyStories aggressively (exact + near-duplicate removal). Consider generating synthetic stories using GPT-4o that target weak spots identified by validation loss analysis.

References:
- [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499)
- [Demystifying Synthetic Data in LLM Pre-training](https://arxiv.org/html/2510.01631v1)

---

## 2. Efficient Training Methods

### 2.1 uP (Maximal Update Parameterization)

uP enables "tune small, train large" by ensuring hyperparameters transfer across model widths. Key implementation rules:

**Initialization:**
- Hidden layers: variance = 1/(3 * d_model), scaled by width multiplier
- Embedding layers: keep base variance unchanged

**Learning Rate Scaling:**
- Hidden layers with Adam: lr_hidden = lr_base / m_d (where m_d = width multiplier)
- Embedding layers: keep base lr unchanged

**Attention:**
- Scale attention logits by 1/d_head (NOT 1/sqrt(d_head)) to account for query-key correlation during training

**Proxy Model Setup:**
- Minimum hidden dimension: 256 (for law of large numbers convergence)
- Match depth to target model (depth-related HP shifts exist)
- Train for ~20 tokens per parameter
- Batch size must exceed critical batch size

**Four tunable scalars:** base init std, base lr, embedding multiplier, output logit multiplier. These transfer directly across widths.

**Verification:** Run "coordinate check" -- train at 4+ widths for 10 steps, confirm activation magnitudes are width-independent.

**Actionable for autoresearch:** If exploring different model widths (e.g., 256 vs 384 vs 512 hidden dim), uP eliminates the need to re-tune hyperparameters for each. Set up a 256-hidden proxy, tune the 4 scalars, then scale to 384 or 512.

References:
- [Cerebras Practitioner's Guide to uP](https://www.cerebras.ai/blog/the-practitioners-guide-to-the-maximal-update-parameterization)
- [EleutherAI uTransfer Guide](https://blog.eleuther.ai/mutransfer/)
- [Microsoft mup GitHub](https://github.com/microsoft/mup)

### 2.2 Learning Rate Scheduling: WSD

The Warmup-Stable-Decay (WSD) scheduler is now the consensus best practice, surpassing cosine:

**Three phases:**
1. **Warmup** (1-2% of steps): Linear increase from 0 to peak LR
2. **Stable** (60-80% of steps): Constant peak LR
3. **Decay** (10-25% of steps): Annealing to 0

**MiniCPM's specific implementation:**
- Exponential annealing: f(s-T) = 0.5^((s-S)/T) where T = 5000 steps
- Peak learning rate: 0.01 (stable across 40M to 2.1B model scales)
- Decay phase: mix in high-quality data and SFT data

**Key advantages over cosine:**
- No need to pre-specify total training steps
- Can resume from any point in stable phase
- Enables continuous training and domain adaptation
- WSD eliminates logarithmic slowdowns
- sqrt and lowered-linear-0.7 are optimal cooldown shapes

**Recent insight (2025):** WSO (Warmup-Stable-Only, removing decay) consistently achieves superior performance after SFT. Consider WSO if planning post-training.

**Actionable:** Replace cosine schedule with WSD. Use peak LR of 0.01 (MiniCPM-validated), warmup for 2% of steps, stable for 80%, decay for 18% with sqrt annealing. During decay phase, mix in the highest-quality subset of training data.

References:
- [MiniCPM Paper](https://arxiv.org/abs/2404.06395)
- [WSD Training Dynamics](https://arxiv.org/abs/2508.01483)
- [Beyond Cosine Decay](https://arxiv.org/html/2503.02844v2)

### 2.3 Batch Size Strategy

MiniCPM derives a batch size formula tied to loss:
- **bs = 1.21 x 10^9 / L^6.24** (where L = validation loss)
- This means batch size should increase as training progresses and loss decreases
- MiniCPM-1.2B starts at 2M tokens/batch, scales to 4M

For small models (30-60M params), the batch size should be large enough that the GPU spends more time on computation than data movement. The critical batch size is the threshold below which training becomes noise-dominated.

**Actionable:** If current batch size is fixed, consider dynamically increasing it during training. Start with a smaller batch (higher noise, better exploration) and scale up as loss decreases.

### 2.4 Mixed Precision Training

RTX 3080 Ti (Ampere) supports both FP16 and BF16 natively via tensor cores:

- **BF16 preferred** over FP16: same dynamic range as FP32, rarely needs loss scaling
- FP16 requires careful gradient scaling to avoid underflow
- Speedups of 2-3x over FP32 are standard
- At 30-60M params, the model fits entirely in GPU memory even in FP32, so the benefit is pure throughput

**Actionable:** Ensure training uses BF16 (torch.autocast with dtype=torch.bfloat16). The RTX 3080 Ti supports it natively. If already using FP16, switch to BF16 to eliminate gradient scaling overhead.

---

## 3. Architecture Innovations for Small Models

### 3.1 Depth vs. Width: The 32-Layer Sweet Spot

Landmark 2025 study on optimal architecture for ~70M parameter models reveals:

**Critical finding: Two-tier performance pattern**
- Models cluster into HIGH tier (~38% avg accuracy) and LOW tier (~32%)
- 6+ percentage point gap with almost nothing in between

**What separates the tiers:**
- Hidden dimension >= 512 OR sufficient depth to compensate
- 32 layers / 384 hidden (77M params) = **38.50%** (best overall)
- 12 layers / 512 hidden (70M params) = 38.15%
- 64 layers / 256 hidden (64M params) = 38.21%
- 4 layers / 768 hidden (68M params) = 31.98% (LOW tier despite similar param count)
- 24 layers / 384 hidden (62M params) = 31.79% (LOW tier -- not deep enough)

**Key insight:** At ~70M params, 32 layers with 384 hidden is the Goldilocks configuration. Deeper models (32-64 layers) beat shallower models on knowledge-intensive tasks.

**Modern architectural innovations have minimal impact at this scale:** RoPE, RMSNorm, GQA, SwiGLU -- all within ~1% of GPT-2 baseline at 70M params. Architecture family matters far less than depth/width ratio.

**Actionable:** If current architecture is shallow (e.g., 8-12 layers), try 32 layers / 384 hidden. This is the highest-impact architectural change supported by evidence. For a 33M model, consider 24 layers / 256 hidden.

References:
- [The Optimal Architecture for Small Language Models](https://huggingface.co/blog/codelion/optimal-model-architecture)
- [Deeper vs Wider: A Revisit of Transformer Configuration](https://arxiv.org/abs/2205.10505v2)

### 3.2 Grouped Query Attention at Small Scale

GQA reduces KV heads while keeping query heads high. MiniCPM-1.2B uses 24 query heads / 8 KV heads.

However, at <100M params, the evidence is mixed:
- GQA's primary benefit is inference KV cache reduction
- At small scale, the parameter savings from GQA are modest
- The optimal architecture study found GQA within noise of MHA at 70M

**Actionable:** GQA is worth trying if inference speed matters, but don't expect training quality improvements at 30-60M scale. The parameter budget is better spent on depth.

### 3.3 Parameter Sharing Across Layers

Several approaches reduce effective parameters while maintaining representational capacity:

- **Recursive/Looped Transformers:** Reuse a block of layers cyclically. Gemma 2B with 18 layers can become recursive with 9 unique layers looped twice.
- **Dictionary-Based Sharing:** Decompose attention matrices into shared dictionary atoms, reducing attention parameters by 66.7% while maintaining performance.
- **Subformer:** Explores weight sharing specifically for parameter-efficient generative transformers.

**Actionable:** At 33M params, try sharing weights between layer pairs (e.g., layers 0-1 share, 2-3 share). This effectively doubles depth without doubling parameters. If using 24 layers with sharing, you get the representational benefit of 24 layers with the parameter count of 12.

References:
- [Dynamic Layer Tying for Parameter-Efficient Transformers](https://arxiv.org/html/2401.12819v1)
- [Share Your Attention: Matrix-based Dictionary Learning](https://arxiv.org/html/2508.04581v1)

### 3.4 Mixture of Depths (MoD)

MoD dynamically allocates compute per token by routing some tokens around transformer blocks via residual connections:

- Sets a static compute budget (e.g., B=0.5 means ~50% of tokens skip a given layer)
- Matches baseline performance for equivalent FLOPs
- Up to **50% faster** during inference
- Lightweight router decides per-token paths

**Related: Mixture of Recursions (MoR)** combines parameter sharing with adaptive depth, reusing shared layers across recursion steps while routing tokens to different depths.

**Actionable:** MoD is primarily an inference optimization. For training throughput, the routing overhead may not pay off at 33M params. Consider MoD only if inference speed is a priority.

### 3.5 Weight Tying

Embedding/unembedding weight tying is essentially universal and should already be implemented. Beyond that:

- **Cross-layer weight tying** (sharing FFN or attention weights across non-adjacent layers) can reduce parameters by 30-50% with manageable quality loss
- Most beneficial when combined with deeper architectures (more layers to share across)

**Actionable:** Verify embedding/unembedding tying is active. If model is 33M params, shared embedding weights are a larger fraction of total parameters and tying is more impactful.

---

## 4. Data Engineering

### 4.1 Deduplication Impact

Landmark findings from Lee et al.:
- C4 dataset contained single sentences repeated 60,000+ times
- Deduplication reduces memorized text emission by 10x
- Fewer training steps needed for same accuracy
- **Caution:** After aggressive dedup, remaining data may be lower quality (more ads, keyword lists) -- combine dedup with quality filtering

**Actionable:** Run exact-match and MinHash near-duplicate detection on TinyStories. Since TinyStories is GPT-generated, there may be significant semantic near-duplicates even without exact matches.

### 4.2 Synthetic Data Strategy

From the comprehensive 2025 scaling law study on synthetic data:

| Configuration | Relative Performance |
|---|---|
| Pure CommonCrawl | Baseline |
| Pure rephrased synthetic | ~= Baseline |
| Pure textbook synthetic | Below baseline |
| **30% rephrased + 70% natural** | **Best overall** |
| 33% textbook + 67% natural | Good |
| 67% textbook + 33% natural | Worse than 33% |

Key nuances:
- Generator model quality matters but plateaus -- 8B generator matches 70B
- Synthetic data benefits diminish with larger models (more impactful for small models)
- Model collapse risk is real for textbook-style data but not for rephrased data

**Actionable for TinyStories:** Generate rephrased versions of existing stories using GPT-4o-mini (cheaper, 8B-class quality sufficient). Mix 30% rephrased with 70% original. This effectively creates a curriculum of slightly varied perspectives on the same content.

### 4.3 Data Mixing Ratios

SmolLM2 training data composition (for 135M model, 2T tokens):
- FineWeb-Edu (filtered web text)
- DCLM (curated web corpus)
- The Stack (code)
- FineMath (mathematical content)
- Stack-Edu (educational code)

For multi-dataset training like TinyStories + climbmix:
- Recommended: 50% primary domain + 30% curated web + 20% specialized
- Adjust ratios based on validation loss curves per domain
- Consider dynamic mixing: increase underperforming domain's share during training

### 4.4 TinyStories State of the Art

The original TinyStories paper (Eldan & Li, 2023) showed models as small as 1M params can produce coherent stories. Recent developments:

- **Multilingual TinyStories** (2026): 132,942 stories, 93.9M tokens across 17 Indian languages
- **Regional TinyStories** (2025): Translation-based expansion to more languages
- **Interpretability research** uses TinyStories models for circuit analysis (ACDC, SAEs)

No published BPB benchmarks surpassing the autoresearch project's 0.4646 were found in the literature. This suggests the project is already at or near state-of-the-art for this model size on TinyStories.

---

## 5. Scaling Laws at Small Scale

### 5.1 Chinchilla Below 100M

The original Chinchilla study included models down to ~70M params. Key findings:

- The 20:1 token-to-parameter ratio was derived primarily from large-scale experiments
- **MiniCPM's finding:** Optimal ratio is **192:1**, nearly 10x Chinchilla
- Modern practice (Llama 3, SmolLM2) uses 100-200+ tokens per parameter
- At small scale, there's evidence of an asymptote below ~20% of the parameter count

**Critical implication:** A 33M model should ideally train on **6.3 billion tokens** (192:1), not 660M tokens (20:1).

### 5.2 Compute-Optimal for 5-Minute Training Budgets

For the autoresearch's ~5-minute runs (~2200 steps):

**Question:** Is 33M params at 2200 steps compute-optimal?

Analysis based on scaling laws:
- 2200 steps x batch_size tokens/step = total training tokens
- If batch size is ~64K tokens: 2200 * 64K = ~140M tokens
- 140M tokens / 33M params = ~4.2 tokens/parameter
- This is **massively under-trained** relative to Chinchilla (20:1) and especially MiniCPM (192:1)

**Options for better compute allocation:**
1. **Smaller model, more steps:** 10M params x 7000 steps = same compute, ~45 tokens/param
2. **Same model, more data:** Run for 20,000 steps (50 min) to reach 20:1
3. **Larger batch size:** Increase tokens per step to improve the ratio

### 5.3 Over-Training Benefits

Strong evidence that over-training (beyond Chinchilla optimal) benefits small models disproportionately:

- Llama 3-70B trained at 200+ tokens/parameter (10x Chinchilla)
- SmolLM2-135M trained on 2 trillion tokens = ~14,800 tokens/parameter
- After accounting for inference cost, smaller over-trained models beat larger compute-optimal ones
- **No evidence of an upper bound** on useful over-training for small models

**Actionable:** For the 5-minute budget, consider: (a) reducing model size to 10-15M and training much longer, or (b) if using the full dataset once, increase the model size to use more parameters per token seen.

---

## 6. Training Infrastructure

### 6.1 torch.compile

PyTorch 2.x compilation provides significant speedups:
- 20-50% speedup with no code changes beyond `torch.compile(model)`
- `mode="reduce-overhead"` automatically enables CUDA graphs
- Triton JIT compilation fuses operations, reducing memory transfers
- Particularly effective for small models where CPU launch overhead is relatively larger

**Actionable:** Ensure `torch.compile` is enabled. Use `mode="reduce-overhead"` for maximum throughput on small models.

### 6.2 FlashAttention on Ampere

RTX 3080 Ti (Ampere) is fully supported by FlashAttention-2:
- 2-4x speedup at sequence lengths 128-4K
- GDDR6X memory bandwidth is lower than HBM (A100), so FlashAttention's memory savings are even more valuable
- At HEAD_DIM=64, FlashAttention is well-optimized (this is the standard dimension)

**FlexAttention (PyTorch 2.5+):** Allows custom attention patterns (sliding window, causal, etc.) compiled into fused kernels. Write attention masks in pure Python, compiler handles fusion.

**Actionable:** Verify FlashAttention-2 is active. At sequence_length=512 with head_dim=64, expect 2-3x speedup over naive attention. FlexAttention enables experimentation with novel attention patterns at no throughput cost.

### 6.3 CUDA Graphs

CUDA graphs capture GPU operation sequences and replay them as single units:
- Eliminate per-kernel CPU launch overhead (~10us per launch vs single launch)
- Most beneficial for small models with many small kernels
- `torch.compile(mode="reduce-overhead")` enables this automatically
- **PyGraph (2025):** Doubles CUDA graph benefit over baseline torch.compile

**When to use:** Check GPU utilization. If <80%, you're CPU-bottlenecked and CUDA graphs will help. Small models (33M params) are prime candidates.

**Actionable:** If not already using CUDA graphs, enable via torch.compile reduce-overhead mode. Monitor GPU utilization -- if it increases significantly, this confirms CPU-bound bottleneck was present.

### 6.4 RTX 3080 Ti Specific Optimizations

- **Ampere architecture:** Full BF16 support, 3rd-gen tensor cores
- **12GB VRAM:** Sufficient for multiple small models simultaneously (useful for distillation)
- **270W TDP:** Thermal management matters for long training runs (reference: project thermal feedback)
- **GDDR6X bandwidth (912 GB/s):** FlashAttention is especially impactful because it reduces memory bandwidth pressure
- **Tensor core utilization:** Ensure matrix dimensions are multiples of 8 (for BF16) for maximum tensor core throughput. Hidden_dim=384 is divisible by 8.

---

## 7. Prioritized Action Plan

### Tier 1: Immediate Impact (try in next 10 experiments)

| Change | Expected Impact | Effort |
|---|---|---|
| **Switch to Muon optimizer** | ~2x compute efficiency (equivalent to doubling training time) | Medium -- need to implement Muon |
| **WSD learning rate schedule** | Better final loss, enables data mixing during decay | Low -- scheduler swap |
| **Increase depth: 32 layers / 384 hidden** | Cross the performance tier threshold | Low -- config change |
| **Aggressive deduplication** of TinyStories | Fewer wasted steps on memorized content | Medium -- preprocessing |

### Tier 2: High-Value Changes (next 20 experiments)

| Change | Expected Impact | Effort |
|---|---|---|
| **MiniPLM-style data curation** | Teacher-guided difficulty sampling | High -- need teacher model inference |
| **Dynamic batch size scaling** | Better noise/signal ratio during training | Medium |
| **Over-train: 10x more tokens** | Exploit scaling law beyond Chinchilla | Requires longer runs |
| **30% synthetic data mixing** | Improved diversity | Medium -- generation cost |

### Tier 3: Exploratory (when plateau persists)

| Change | Expected Impact | Effort |
|---|---|---|
| **uP for hyperparameter transfer** | Systematic HP optimization | High -- framework change |
| **Layer sharing (double depth)** | 24-unique-layer quality at 12-layer cost | Medium |
| **Curriculum learning (easy-to-hard)** | Better convergence trajectory | Medium -- need difficulty scorer |
| **Mixture of Depths** | Faster inference (not training) | High |

---

## 8. Specific Recommendations for Breaking 0.4646 BPB

### The Most Likely Path Forward

Based on the evidence, the plateau at 0.4646 is most likely caused by one or more of:

1. **Optimizer limitation:** AdamW leaves ~2x compute on the table vs Muon
2. **Under-training:** If only seeing each token ~4 times, the model hasn't extracted full signal
3. **Architecture:** If using <16 layers, the model may be in the "low tier" where no amount of training helps
4. **Data saturation:** TinyStories may have been fully learned at this model size; need data augmentation

### Recommended Experiment Sequence

```
Experiment 111: Baseline + Muon optimizer (keep everything else)
Experiment 112: Baseline + WSD schedule (keep AdamW for comparison)
Experiment 113: Muon + WSD combined
Experiment 114: Muon + WSD + deeper architecture (32L/384H)
Experiment 115: Exp 114 + deduplicated TinyStories
Experiment 116: Exp 115 + 30% synthetic data augmentation
Experiment 117: Exp 115 + 2x training tokens (longer run)
Experiment 118: Exp 114 + layer sharing (64 effective layers, 32 unique)
```

Each experiment isolates one variable against the previous best, enabling clean ablation.

### Target BPB Estimates

| Configuration | Estimated BPB | Basis |
|---|---|---|
| Current baseline | 0.4646 | Measured |
| + Muon optimizer | ~0.445 | 2x compute efficiency -> equivalent to doubling training |
| + WSD schedule | ~0.440 | Better final convergence |
| + Deeper architecture | ~0.430 | Cross tier threshold |
| + Data improvements | ~0.420 | Dedup + augmentation |
| + Over-training (10x) | ~0.400 | Scaling law extrapolation |

These estimates are speculative but grounded in the relative improvements reported in the literature.

---

## 9. Key Papers and Resources

### Must-Read Papers
- [MiniCPM: Scalable Training Strategies](https://arxiv.org/abs/2404.06395) -- WSD scheduler, data-model scaling, deeper-thinner architecture
- [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982) -- 2x efficiency optimizer
- [Optimal Architecture for Small Language Models](https://huggingface.co/blog/codelion/optimal-model-architecture) -- 32-layer sweet spot, tier analysis
- [MiniPLM: Knowledge Distillation for Pre-Training](https://arxiv.org/abs/2410.17215) -- Offline distillation framework
- [Demystifying Synthetic Data in LLM Pre-training](https://arxiv.org/html/2510.01631v1) -- 30/70 mixing ratio
- [SmolLM2 Paper](https://huggingface.co/papers/2502.02737) -- Data-centric small model training
- [Deduplicating Training Data](https://arxiv.org/abs/2107.06499) -- 10x memorization reduction

### Implementation Resources
- [Cerebras uP Practitioner's Guide](https://www.cerebras.ai/blog/the-practitioners-guide-to-the-maximal-update-parameterization)
- [EleutherAI uTransfer Guide](https://blog.eleuther.ai/mutransfer/)
- [Microsoft mup Library](https://github.com/microsoft/mup)
- [NanoGPT Speedrun (modded-nanogpt)](https://github.com/KellerJordan/modded-nanogpt) -- Muon implementation, training tricks
- [FlashAttention GitHub](https://github.com/Dao-AILab/flash-attention)

### Additional References
- [WSD Scheduling Analysis](https://arxiv.org/abs/2508.01483)
- [Beyond Cosine Decay for Continual Pre-training](https://arxiv.org/html/2503.02844v2)
- [Scaling Laws and Compute-Optimal Training](https://arxiv.org/html/2405.18392v2)
- [Dynamic Layer Tying](https://arxiv.org/html/2401.12819v1)
- [Mixture of Depths](https://arxiv.org/html/2404.02258v1)
- [Speed Up PyTorch Training by 3x](https://arikpoz.github.io/posts/2025-05-25-speed-up-pytorch-training-by-3x-with-nvidia-nsight-and-pytorch-2-tricks/)
- [Small Language Models Survey](https://arxiv.org/html/2501.05465v1)
- [How to Train a Small Language Model Guide](https://dev.to/jaipalsingh/how-to-train-a-small-language-model-the-complete-guide-for-2026-4p6h)
- [Introduction to Small Language Models 2026](https://machinelearningmastery.com/introduction-to-small-language-models-the-complete-guide-for-2026/)

---

*Generated by autoresearch Wave 4 deep research agent, 2026-03-23*
