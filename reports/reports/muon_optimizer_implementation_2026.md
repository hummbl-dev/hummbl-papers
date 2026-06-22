# Muon Optimizer: Deep Technical Research & Implementation Guide

**Wave 4 Deep Research Report -- Autoresearch Project**
**Date:** 2026-03-24
**Context:** Breaking the 0.4646 BPB plateau, 33M param models, RTX 3080 Ti (12GB), current config already uses MuonAdamW

---

## Executive Summary

The Muon optimizer is **already implemented** in the autoresearch codebase (`train.py`, lines 752-904). The current `MuonAdamW` class applies Muon to 2D matrix parameters and AdamW to embeddings, scalars, and the LM head. This report provides the theoretical foundation, scaling insights from MoonshotAI, comparison to alternative optimizers, and -- critically -- an experiment plan to **tune the existing Muon implementation** for maximum plateau-breaking potential.

Key finding: The current config uses `WEIGHT_DECAY=0.0` for Muon parameters, which contradicts MoonshotAI's scaling paper finding that weight decay is **essential** for Muon stability and performance. This is likely the single highest-leverage change available.

---

## 1. Muon Optimizer: Origin & Theory

### 1.1 Who Created It, When

Muon was created by **Keller Jordan** and collaborators (Yuchen Jin, Vlado Boza, You Jiacheng, Franz Cesista, Laker Newhouse, Jeremy Bernstein) in **October 2024**, initially developed for the nanoGPT speedrun competition. The original writeup is at [kellerjordan.github.io/posts/muon](https://kellerjordan.github.io/posts/muon/).

The name "Muon" stands for **M**atrix **U**pdate **O**rthogonalizatio**N**.

### 1.2 Mathematical Formulation

Muon's core idea: replace standard gradient updates with their **nearest orthogonal matrix** (the polar factor from polar decomposition).

**Standard SGD-Momentum update:**
```
G_t = β * G_{t-1} + (1 - β) * ∇L(W_t)     # momentum accumulation
W_{t+1} = W_t - η * G_t                      # parameter update
```

**Muon update:**
```
G_t = β * G_{t-1} + (1 - β) * ∇L(W_t)       # Nesterov momentum
Ĝ_t = (1 - β) * ∇L(W_t) + β * G_t           # Nesterov lookahead
U Σ V^T = SVD(Ĝ_t)                           # SVD decomposition
W_{t+1} = W_t - η * √(fan_out/fan_in) * U V^T  # orthogonalized update
```

The key operation `U V^T` discards the singular values Σ, keeping only the directions. This is equivalent to finding the **nearest orthogonal matrix** to the momentum update in Frobenius norm.

### 1.3 Why Orthogonalization Works (Jeremy Bernstein's Derivation)

The theoretical justification comes from **steepest descent under the spectral norm** (see [jeremybernste.in/writing/deriving-muon](https://jeremybernste.in/writing/deriving-muon)):

1. **RMS-to-RMS operator norm**: Defines how much a weight matrix amplifies input magnitudes. The spectral norm `σ_max(W)` controls this.

2. **Constrained optimization**: Instead of unconstrained gradient descent, Muon solves:
   ```
   minimize ⟨∇L, ΔW⟩  subject to  ‖ΔW‖_spectral ≤ η
   ```
   The solution is exactly `ΔW = -η * UV^T`.

3. **Automatic muP scaling**: The `√(fan_out/fan_in)` factor emerges naturally from the RMS-to-RMS metric and provides **built-in width-invariant learning rate transfer** -- no need to retune LR when scaling model width.

4. **Better tail class optimization**: Muon produces updates with an **isotropic singular spectrum** (all singular values equal to 1), which allocates equal optimization pressure to all directions. AdamW's updates have a skewed spectrum that under-optimizes rare/tail directions.

### 1.4 Newton-Schulz Orthogonalization (Practical Implementation)

Computing the full SVD is O(n³) and expensive. Muon instead uses **Newton-Schulz (NS) iterations** -- an iterative polynomial that converges singular values toward 1:

**Quintic polynomial per iteration:**
```
φ(X) = aX + bX³ + cX⁵
```
where `(a, b, c) = (3.4445, -4.7750, 2.0315)` are optimized coefficients.

**Implementation (5 steps):**
```python
# Normalize by Frobenius norm
X = G / (‖G‖_F * 1.02 + ε)

# 5 Newton-Schulz iterations
for (a, b, c) in coefficients[:5]:
    if tall_matrix:
        A = X^T @ X       # d_out × d_out
        B = b*A + c*(A@A)
        X = a*X + X@B
    else:
        A = X @ X^T        # d_in × d_in
        B = b*A + c*(A@A)
        X = a*X + B@X
```

The autoresearch codebase uses an even more refined set of 5 coefficient tuples called `polar_express_coeffs` (train.py line 755-761), which are optimized to converge faster than the standard NS coefficients.

**Computational overhead**: `6nm² × T` FLOPs per parameter matrix, where T=5 iterations. For batch size B and model dim m, overhead is `Θ(m/B)` -- typically **0.5-3%** of total training FLOPs.

### 1.5 Comparison to AdamW

| Property | AdamW | Muon |
|---|---|---|
| **Optimizer states** | 2 (first + second moment) | 1 (momentum only) + 1 (second moment for normalization) |
| **Memory per param** | 2× param size | ~2× param size (momentum + second moment buffer) |
| **Update direction** | Scaled gradient (per-element adaptive) | Orthogonalized gradient (spectral-norm steepest descent) |
| **Singular spectrum** | Skewed (favors large-gradient directions) | Isotropic (equal pressure all directions) |
| **Width scaling** | Requires muP or manual tuning | Built-in width-invariant LR |
| **Compute efficiency** | Baseline | ~2× (reaches same loss in ~52% FLOPs) |
| **Best for** | Embeddings, 1D params, classification heads | 2D weight matrices (attention, FFN) |
| **Weight decay** | Standard decoupled | Critical for scaling (prevents weight growth) |

---

## 2. Empirical Results

### 2.1 nanoGPT Speedrun Results

The nanoGPT speedrun trains GPT-2-124M to 3.28 validation loss on FineWeb using 8× H100s. Muon's impact:

- **Pre-Muon record (Oct 2024):** ~4.5 minutes
- **First Muon record (Oct 15, 2024):** 35% faster than prior record
- **Record #19 (Jan 13, 2025):** 3.142 minutes
- **Record #20 (Jan 16, 2025):** 2.992 minutes
- **Record #21 (Jan 26, 2025):** 2.933 minutes
- **Record #27 (Jul 2025):** 2.817 minutes
- **Record #29 (Sep 2025):** 2.731 minutes

Muon has been the optimizer of choice for **all 12+ records since its introduction**, set by 7 different researchers. The competition's total training time dropped from 45 minutes (original baseline) to under 3 minutes.

### 2.2 MoonshotAI Scaling Results (arxiv 2502.16982)

MoonshotAI's **Moonlight** project scaled Muon to a 3B-active/16B-total MoE model trained on 5.7T tokens:

**Scaling law finding:** Muon achieves ~2× compute efficiency -- it requires only **~52% of training FLOPs** to match AdamW at compute-optimal settings.

**Two critical techniques for scaling:**
1. **Weight decay** (standard decoupled, λ=0.1): Prevents weight magnitudes from growing unboundedly during extended training. Without it, Muon degrades in the over-training regime.
2. **Per-parameter update scale**: Scale updates by `√max(rows, cols)` to maintain consistent update RMS across different matrix shapes. Match Muon's update RMS to AdamW's typical range of 0.2-0.4.

**Moonlight benchmark results (5.7T tokens):**

| Benchmark | Moonlight-16B-A3B | DeepSeek-V2-Lite (same tokens) |
|---|---|---|
| MMLU | 70.0 | 58.3 |
| GSM8K | 77.4 | 41.1 |
| HumanEval | 48.1 | 29.9 |

**Key quote:** "Muon can directly reuse the learning rate and weight decay tuned for AdamW" when using the 0.2√n rescaling constant.

### 2.3 Essential AI Practical Efficiency Results (arxiv 2505.02222)

Essential AI validated Muon at 100M-4B parameter scale:

- **Memory**: Lighter footprint than AdamW (1 momentum buffer vs 2 moment estimates)
- **Data efficiency**: Muon requires **10-15% fewer tokens** than AdamW to reach identical loss
- **Wall-clock**: Faster than AdamW even with a basic (non-optimized) implementation
- **LR relationship**: Using `0.2√n` normalization, the same LR and weight decay work for both Muon and AdamW groups
- **MFU**: ~50% model FLOP utilization on TPU v5p

---

## 3. Current Autoresearch Implementation Analysis

### 3.1 What's Already Implemented

The codebase at `C:/Users/Owner/autoresearch-win-rtx/train.py` already contains a complete MuonAdamW optimizer:

**Parameter group separation (lines 657-716):**
- **Muon groups**: All 2D transformer parameters (attention Q/K/V/O, FFN), chunked in groups of 8 by shape
- **AdamW groups**: LM head, embeddings, value embeddings, residual lambdas, x0 lambdas, scalar-like params

**Muon hyperparameters (current config, lines 917-924):**
```python
MATRIX_LR = 0.032          # Muon learning rate for 2D params
WEIGHT_DECAY = 0.0          # ← PROBLEM: MoonshotAI says this should be > 0
ADAM_BETAS = (0.9, 0.99)    # For AdamW groups
# Muon momentum: warmup from 0.85 to 0.95 over first 300 steps
# Muon beta2: 0.95 (second moment for normalization)
# NS steps: 5
```

**Per-component LR scaling (lines 679-696):**
```python
dmodel_lr_scale = (model_dim / 768) ** -0.5   # muP-like width scaling
lm_head_params:       lr = UNEMBEDDING_LR * dmodel_lr_scale    # 0.0064 * scale
embedding_params:     lr = EMBEDDING_LR * dmodel_lr_scale       # 0.32 * scale
value_embeds_params:  lr = EMBEDDING_LR * dmodel_lr_scale       # 0.32 * scale
resid_params:         lr = SCALAR_LR * 0.01                     # 0.004
x0_params:            lr = SCALAR_LR                            # 0.4
scalar_like_params:   lr = SCALAR_LR * dmodel_lr_scale          # 0.4 * scale
matrix_params (Muon): lr = MATRIX_LR                            # 0.032 (no width scaling -- Muon has built-in)
```

**Newton-Schulz implementation (lines 755-793):**
Uses 5 "polar express" coefficient sets (more refined than standard NS coefficients), with automatic handling of tall vs wide matrices.

**LR schedule (lines 1219-1225):**
- Warmup: `WARMUP_RATIO = 0.0` (currently disabled)
- Stable phase: constant LR
- Warmdown: `WARMDOWN_RATIO = 0.7` (70% of training is cooldown)
- Final LR: `FINAL_LR_FRAC = 0.05` (5% of peak)

**Muon momentum warmup (lines 1227-1229):**
```python
def get_muon_momentum(step):
    frac = min(step / 300, 1)
    return (1 - frac) * 0.85 + frac * 0.95
```

### 3.2 Identified Gaps vs. Literature Best Practices

| Issue | Current Config | Literature Recommendation | Impact |
|---|---|---|---|
| **Weight decay = 0** | `WEIGHT_DECAY=0.0` | 0.01-0.1 (MoonshotAI uses 0.1) | **HIGH** -- prevents weight growth, critical for stability in over-training |
| **No LR warmup** | `WARMUP_RATIO=0.0` | 1-2% warmup standard | Medium -- momentum warmup partially compensates |
| **Very long warmdown** | `WARMDOWN_RATIO=0.7` | WSD recommends 10-25% decay | Medium -- could leave performance on table during stable phase |
| **No per-param update scaling** | Not present | `√max(rows, cols)` normalization | Medium -- may cause inconsistent update magnitudes across layers |
| **Muon LR vs. literature** | 0.032 | 0.02 (Keller Jordan), 4.2e-4 with rescaling (MoonshotAI) | Needs validation |
| **Selective weight decay** | Decays only during training, linearly to 0 | Constant weight decay throughout | Low-Medium |

---

## 4. Other Promising Optimizers

### 4.1 SOAP (Shampoo-like, NeurIPS 2024)

**Paper:** "SOAP: Improving and Stabilizing Shampoo using Adam" (Vyas et al., Harvard)
**How it works:** Shows Shampoo is equivalent to running Adafactor in the eigenbasis of its preconditioner. SOAP simplifies this into a practical algorithm.

**Key results:**
- Outperforms both AdamW and Shampoo at 360M and 660M parameter scale
- Better wall-clock time AND iteration efficiency
- Minimal extra hyperparameter tuning vs AdamW

**For autoresearch (33M):** SOAP requires periodic eigendecompositions which add overhead. At 33M params the overhead fraction is larger. **Verdict: Muon is simpler and proven at this scale. Try SOAP only if Muon plateaus.**

### 4.2 ScheduleFree (Meta, 2024)

**Paper:** "The Road Less Scheduled" (Defazio et al., arxiv 2405.15682)
**How it works:** Replaces momentum with interpolation + averaging, eliminating the need for a learning rate schedule. No need to specify total training steps in advance.

**Key results:**
- Won the MLCommons 2024 AlgoPerf Algorithmic Efficiency Challenge
- Implementations: `SGDScheduleFree`, `AdamWScheduleFree`, `RAdamScheduleFree`
- `pip install schedulefree`

**For autoresearch (33M):** Very interesting because the current config dedicates 70% of training to warmdown. ScheduleFree could recover that compute for actual training. **Verdict: High potential. Could combine with Muon -- use ScheduleFree for AdamW groups, Muon for matrix groups.**

### 4.3 Prodigy / D-Adaptation

**Paper:** "Prodigy: An Expeditiously Adaptive Parameter-Free Learner" (Mishchenko & Defazio, arxiv 2306.06101)
**How it works:** Automatically estimates the distance to the optimal solution D, which determines the optimal learning rate. Set `lr=1.0` and Prodigy finds the right scale.

**Key results:**
- Matches hand-tuned Adam across VGG, ResNet, ViT, LSTM, GPT, RoBERTa
- Already the default optimizer for HuggingFace Diffusers DreamBooth LoRA
- `prodigy-plus-schedule-free` combines both approaches

**For autoresearch (33M):** Could eliminate the LR sweep entirely. However, Prodigy's automatic LR estimation adds overhead and may not outperform a well-tuned Muon. **Verdict: Useful for exploration/sweep reduction, but unlikely to beat tuned Muon for final performance.**

### 4.4 Recommendation Ranking for 33M Scale

1. **Muon (already implemented)** -- Tune weight decay and LR, highest confidence
2. **ScheduleFree for AdamW groups** -- Eliminate warmdown overhead, medium effort
3. **SOAP** -- Try if Muon + ScheduleFree plateau, high effort
4. **Prodigy** -- Use for automatic HP search to find good starting points, low effort

---

## 5. Practical Integration Details

### 5.1 Memory Overhead on RTX 3080 Ti (12GB)

Current VRAM usage: ~2.5 GB for 33M param model.

**Muon memory breakdown (per 2D parameter matrix of shape [m, n]):**
- Parameter: `m × n × dtype_size`
- Momentum buffer: `m × n × dtype_size`
- Second moment buffer: small (per-row or per-col mean)
- Stacked computation: temporary `[chunk_size, m, n]` tensor

**Comparison:**
- AdamW: 2 state tensors per param (exp_avg + exp_avg_sq) = 2× param memory
- Muon: 1 momentum buffer + 1 small second moment = ~1× param memory + small overhead

**Net effect:** Muon uses **less** optimizer state memory than AdamW. At 33M params (~130MB in bf16), optimizer states are ~130MB for Muon vs ~260MB for AdamW. The NS iteration adds temporary memory proportional to the chunk size (8 matrices stacked), but this is freed after each step.

**Conclusion:** No VRAM concerns. The RTX 3080 Ti has ~9.5GB headroom.

### 5.2 Throughput Impact

NS iteration overhead formula: `5 × model_dim / batch_size_tokens`

For autoresearch config:
- `model_dim = 384` (6 layers × 64 aspect ratio)
- `batch_size = 2^14 = 16,384 tokens`
- Overhead: `5 × 384 / 16384 = 0.117 = ~12%`

This is higher than the nanoGPT speedrun (0.7%) because the autoresearch batch size is much smaller. However, the NS iteration runs in bfloat16 and is highly parallelizable on the GPU.

**Measured throughput:** The current codebase already runs Muon at ~122k tok/sec, so the overhead is already baked in. Switching to pure AdamW would gain ~12% throughput but lose ~2× compute efficiency -- a net loss.

### 5.3 Per-Component LR Compatibility

Muon's built-in muP scaling means the matrix LR does **not** need the `dmodel_lr_scale` correction that AdamW groups use. The current implementation correctly applies:
- `dmodel_lr_scale` to all AdamW groups (embeddings, scalars, LM head)
- Raw `MATRIX_LR` to Muon groups (no width correction)

This is exactly correct per the literature. The per-component LR structure is fully compatible with Muon.

### 5.4 Weight Decay Integration

The current code applies weight decay with a **partial gradient masking** strategy (train.py line 808-809):
```python
mask = (g * stacked_params) >= 0
stacked_params.sub_(lr * g + lr * wd * stacked_params * mask)
```

This only applies weight decay when the gradient and parameter have the **same sign** -- a form of signed weight decay that prevents decay from fighting useful gradient directions. This is a custom choice that differs from MoonshotAI's standard decoupled weight decay.

**Recommendation:** Test both standard decoupled WD (remove the mask) and the current signed WD with `WEIGHT_DECAY > 0`.

---

## 6. Code Snippets

### 6.1 Standalone Muon Optimizer Class (Ready to Use)

The following is a clean, self-contained Muon optimizer that can be dropped into any PyTorch training loop. It is equivalent to the autoresearch implementation but simplified for clarity:

```python
import torch
import torch.nn as nn

# Newton-Schulz coefficients (optimized "polar express" variant)
POLAR_COEFFS = [
    (8.156554524902461, -22.48329292557795, 15.878769915207462),
    (4.042929935166739, -2.808917465908714, 0.5000178451051316),
    (3.8916678022926607, -2.772484153217685, 0.5060648178503393),
    (3.285753657755655, -2.3681294933425376, 0.46449024233003106),
    (2.3465413258596377, -1.7097828382687081, 0.42323551169305323),
]

def newton_schulz_orthogonalize(G, ns_steps=5, dtype=torch.bfloat16):
    """Approximate polar decomposition via Newton-Schulz iteration.

    Input:  G of shape [..., m, n]  (gradient or momentum matrix)
    Output: Orthogonalized G, same shape, all singular values ≈ 1
    """
    X = G.to(dtype=dtype)
    X = X / (X.norm(dim=(-2, -1), keepdim=True) * 1.02 + 1e-6)

    if X.size(-2) > X.size(-1):  # tall matrix
        for a, b, c in POLAR_COEFFS[:ns_steps]:
            A = X.mT @ X          # [n, n]
            B = b * A + c * (A @ A)
            X = a * X + X @ B
    else:  # wide or square matrix
        for a, b, c in POLAR_COEFFS[:ns_steps]:
            A = X @ X.mT          # [m, m]
            B = b * A + c * (A @ A)
            X = a * X + B @ X
    return X


class MuonOptimizer(torch.optim.Optimizer):
    """Muon optimizer for 2D weight matrices.

    Args:
        params: Iterable of 2D parameters (attention, FFN weights)
        lr: Learning rate (default: 0.02)
        momentum: Nesterov momentum coefficient (default: 0.95)
        weight_decay: Decoupled weight decay (default: 0.01)
        ns_steps: Newton-Schulz iteration count (default: 5)
        beta2: Second moment coefficient for update normalization (default: 0.95)
    """

    def __init__(self, params, lr=0.02, momentum=0.95, weight_decay=0.01,
                 ns_steps=5, beta2=0.95):
        defaults = dict(lr=lr, momentum=momentum, weight_decay=weight_decay,
                       ns_steps=ns_steps, beta2=beta2)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            lr = group['lr']
            momentum = group['momentum']
            wd = group['weight_decay']
            ns_steps = group['ns_steps']
            beta2 = group['beta2']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                state = self.state[p]

                # Initialize state
                if not state:
                    state['momentum_buffer'] = torch.zeros_like(p)
                    state['v'] = torch.zeros(1, device=p.device, dtype=torch.float32)

                buf = state['momentum_buffer']

                # Nesterov momentum
                buf.lerp_(grad, 1 - momentum)
                g = grad.lerp_(buf, momentum)  # Nesterov lookahead

                # Newton-Schulz orthogonalization
                g = newton_schulz_orthogonalize(g.unsqueeze(0), ns_steps).squeeze(0)

                # Update normalization (optional, from MoonshotAI scaling)
                scale = (max(p.shape[0], p.shape[1]) ** 0.5)
                g = g * scale

                # EMA-based adaptive scaling
                v_new = g.float().square().mean()
                state['v'].lerp_(v_new, 1 - beta2)
                step_scale = state['v'].clamp_min(1e-10).rsqrt()
                g = g * step_scale.to(g.dtype)

                # Weight decay + parameter update
                p.mul_(1 - lr * wd)
                p.add_(g.to(p.dtype), alpha=-lr)
```

### 6.2 How to Modify train.py for Experiments

The current `train.py` already has Muon. To experiment with the key changes identified:

**Change 1: Enable weight decay (highest priority)**
```python
# Line 921 in train.py -- change from:
WEIGHT_DECAY = 0.0
# To:
WEIGHT_DECAY = 0.04  # Start with 0.04, sweep [0.01, 0.02, 0.04, 0.08, 0.1]
```

**Change 2: Make weight decay constant (not decaying)**
```python
# Line 1231-1232 -- change from:
def get_weight_decay(progress):
    return WEIGHT_DECAY * (1 - progress)
# To:
def get_weight_decay(progress):
    return WEIGHT_DECAY  # Constant throughout training
```

**Change 3: Add LR warmup**
```python
# Line 923 -- change from:
WARMUP_RATIO = 0.0
# To:
WARMUP_RATIO = 0.02  # 2% warmup (standard recommendation)
```

**Change 4: Shorten warmdown (try WSD-style)**
```python
# Line 924 -- change from:
WARMDOWN_RATIO = 0.7
# To:
WARMDOWN_RATIO = 0.2  # 20% decay (WSD recommendation)
```

**Change 5: Try standard decoupled weight decay (remove gradient-sign masking)**
```python
# In muon_step_fused, lines 808-809 -- change from:
mask = (g * stacked_params) >= 0
stacked_params.sub_(lr * g + lr * wd * stacked_params * mask)
# To:
stacked_params.mul_(1 - lr * wd)  # Standard decoupled weight decay
stacked_params.sub_(lr * g)        # Gradient step
```

### 6.3 Per-Component LR Adaptation (Already Correct)

The current implementation correctly separates concerns:

```python
# Muon groups: no width scaling needed (built into orthogonalization)
dict(kind="muon", params=matrix_params, lr=MATRIX_LR, momentum=0.95, ns_steps=5)

# AdamW groups: width-scaled LRs
dict(kind="adamw", params=embedding_params, lr=EMBEDDING_LR * dmodel_lr_scale)
dict(kind="adamw", params=lm_head_params, lr=UNEMBEDDING_LR * dmodel_lr_scale)
dict(kind="adamw", params=scalar_like_params, lr=SCALAR_LR * dmodel_lr_scale)
```

No changes needed here. The MATRIX_LR controls Muon's learning rate independently from the AdamW groups.

---

## 7. Experiment Plan

### 7.1 Experiments (5 total, ~25 minutes via sweep.py)

All experiments use the current best config as baseline: DEPTH=6, HEAD_DIM=64, ASPECT_RATIO=64 (33.4M params), MuonAdamW optimizer.

**Experiment A: Weight Decay Sweep (Control)**
```bash
uv run sweep.py --param WEIGHT_DECAY --values 0.0,0.01,0.02,0.04,0.08
```
- **Control:** WEIGHT_DECAY=0.0 (current best, expected ~0.4646 BPB)
- **Hypothesis:** WD=0.02-0.04 will outperform WD=0 based on MoonshotAI findings
- **Expected improvement:** 0.005-0.015 BPB (based on MoonshotAI's "Muon with WD outperforms both vanilla Muon and AdamW")

**Experiment B: WSD Schedule (Shorten Warmdown)**
```bash
uv run sweep.py --param WARMDOWN_RATIO --values 0.1,0.2,0.3,0.5,0.7
```
- **Control:** WARMDOWN_RATIO=0.7 (current)
- **Hypothesis:** Shorter warmdown (0.2-0.3) keeps LR high longer, enabling more learning
- **Expected improvement:** 0.005-0.010 BPB

**Experiment C: Muon LR Sweep (with best WD from Exp A)**
First apply best WD from Experiment A, then:
```bash
uv run sweep.py --param MATRIX_LR --values 0.016,0.024,0.032,0.040,0.048
```
- **Control:** MATRIX_LR=0.032 (current)
- **Hypothesis:** Optimal LR may shift when weight decay is enabled
- **Expected improvement:** 0.003-0.008 BPB

**Experiment D: Constant vs. Decaying Weight Decay**
Requires a code change (see Section 6.2, Change 2). Run two configurations:
1. `WEIGHT_DECAY=best_from_A` with linear decay (current behavior)
2. `WEIGHT_DECAY=best_from_A` with constant WD

This needs a manual code toggle, not sweep.py.

**Experiment E: Combined Best Settings**
Apply all winners from A-D simultaneously:
- Best WEIGHT_DECAY
- Best WARMDOWN_RATIO
- Best MATRIX_LR
- Best WD schedule (constant vs decaying)

**Expected combined improvement: 0.010-0.025 BPB** (reaching ~0.440-0.455 BPB)

### 7.2 sweep.py Integration

All single-parameter sweeps work directly with `sweep.py` since WEIGHT_DECAY, WARMDOWN_RATIO, and MATRIX_LR are all top-level constants. For the WD constant-vs-decaying experiment, add a new top-level constant:

```python
# Add to train.py hyperparameters section:
WEIGHT_DECAY_SCHEDULE = "constant"  # "constant" or "linear_decay"
```

Then modify `get_weight_decay`:
```python
def get_weight_decay(progress):
    if WEIGHT_DECAY_SCHEDULE == "constant":
        return WEIGHT_DECAY
    else:  # linear_decay
        return WEIGHT_DECAY * (1 - progress)
```

Now sweep.py can sweep it:
```bash
uv run sweep.py --param WEIGHT_DECAY_SCHEDULE --values constant,linear_decay
```

### 7.3 Expected Improvement Range

| Scenario | Expected BPB | Basis |
|---|---|---|
| Current baseline | 0.4646 | Measured |
| + Weight decay 0.04 | ~0.455 | MoonshotAI finding, conservative estimate |
| + Shorter warmdown (0.2) | ~0.450 | More time at peak LR |
| + Re-tuned Muon LR | ~0.447 | LR-WD interaction |
| + All combined | ~0.440-0.445 | Compound effect with diminishing returns |

These are conservative estimates. The MoonshotAI paper reports ~2× compute efficiency, which at constant compute would translate to reaching a loss level that normally requires double the training -- potentially a much larger improvement.

---

## 8. Advanced Topics for Future Work

### 8.1 Muon + ScheduleFree Hybrid

Replace the warmdown schedule entirely by using `ScheduleFreeAdamW` for the AdamW parameter groups while keeping Muon (with its own schedule) for matrix params. This eliminates the need to specify `WARMDOWN_RATIO` and `FINAL_LR_FRAC` for embeddings/scalars.

```python
# Future experiment: hybrid Muon + ScheduleFree
from schedulefree import AdamWScheduleFree

# For AdamW groups only:
adamw_optimizer = AdamWScheduleFree(adamw_params, lr=0.003, betas=(0.9, 0.99))

# For Muon groups:
muon_optimizer = MuonOptimizer(matrix_params, lr=0.032, weight_decay=0.04)
```

### 8.2 Deeper Architecture + Muon

MoonshotAI showed Muon's advantage grows with model depth (more 2D matrices to optimize). If Experiment E succeeds, the next move is:
- Increase to DEPTH=8 or DEPTH=12 with proportionally smaller ASPECT_RATIO
- Muon's ~2× efficiency could offset the throughput loss from deeper models
- This aligns with the small_lm_training report's "go deeper and thinner" recommendation

### 8.3 PyTorch Native Muon (torch.optim.Muon)

As of PyTorch 2.11, Muon has been added to the official `torch.optim` module. When the autoresearch environment upgrades to PyTorch 2.11+, the custom `MuonAdamW` class could be replaced with the native implementation, potentially benefiting from future PyTorch-level optimizations.

---

## 9. Key References

### Core Muon Papers & Posts
- [Muon: An optimizer for hidden layers](https://kellerjordan.github.io/posts/muon/) -- Keller Jordan's original writeup
- [Deriving Muon](https://jeremybernste.in/writing/deriving-muon) -- Jeremy Bernstein's theoretical derivation
- [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982) -- MoonshotAI scaling paper
- [Practical Efficiency of Muon for Pretraining](https://arxiv.org/abs/2505.02222) -- Essential AI validation at 100M-4B scale

### Implementations
- [KellerJordan/Muon (GitHub)](https://github.com/KellerJordan/Muon) -- Official standalone implementation
- [KellerJordan/modded-nanogpt (GitHub)](https://github.com/KellerJordan/modded-nanogpt) -- nanoGPT speedrun with Muon
- [MoonshotAI/Moonlight (GitHub)](https://github.com/MoonshotAI/Moonlight) -- Distributed Muon for large-scale training
- [torch.optim.Muon (PyTorch 2.11)](https://docs.pytorch.org/docs/stable/generated/torch.optim.Muon.html) -- Native PyTorch implementation
- [NVIDIA NeMo Emerging Optimizers](https://docs.nvidia.com/nemo/emerging-optimizers/latest/apidocs/orthogonalized-optimizers.html) -- NeMo integration

### Alternative Optimizers
- [SOAP: Improving and Stabilizing Shampoo](https://arxiv.org/abs/2409.11321) -- Harvard, NeurIPS 2024
- [The Road Less Scheduled (ScheduleFree)](https://arxiv.org/abs/2405.15682) -- Meta, 2024
- [Prodigy: Adaptive Parameter-Free Learner](https://arxiv.org/abs/2306.06101) -- Automatic LR selection
- [ScheduleFree GitHub](https://github.com/facebookresearch/schedule_free) -- Meta implementation
- [Prodigy GitHub](https://github.com/konstmish/prodigy) -- Prodigy implementation

### nanoGPT Speedrun
- [NanoGPT Speedrun Records (CSV)](https://github.com/hansgundlach/SpeedRunAnalysis/blob/main/nanogpt_speedrun_records.csv) -- All historical records
- [Prime Intellect Speedrun Leaderboard](https://app.primeintellect.ai/speedrun/nanogpt) -- Live leaderboard

---

*Generated by autoresearch Wave 4 deep research agent, 2026-03-24*
