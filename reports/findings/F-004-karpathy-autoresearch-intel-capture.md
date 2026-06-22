# Finding F-004: Karpathy Autoresearch — Architecture & Intel Capture

## Source
- **Repository:** https://github.com/karpathy/autoresearch
- **Stars:** 87.8K (as of 2026-06-20)
- **Forks:** 12.7K
- **Author:** Andrej Karpathy (@karpathy)
- **Research Run:** 2026-06-20 (read-only code review + web intelligence)
- **Confidence:** High (0.90) — source code directly inspected

## Executive Summary

Karpathy's `autoresearch` is the canonical upstream that spawned the entire autoresearch ecosystem. It is not a multi-agent pipeline framework — it is a **single-agent, single-GPU, single-file experiment harness** designed for Claude/Codex to autonomously edit `train.py` and run overnight experiments on a small LLM training setup. The entire "orchestration" fits in a Markdown file (`program.md`) that acts as a prompt/skill for the agent.

This is fundamentally different from HUMMBL's `autoresearch-pipeline` (supervisor/worker queue architecture). Karpathy's version is designed for a human+AI pair where the AI is the researcher; HUMMBL's version is designed for autonomous fleet operation with bus integration, cost governance, and multi-machine coordination.

## Architecture Deep Dive

### File Surface (Deliberately Minimal)

| File | Role | Mutable? | Notes |
|------|------|----------|-------|
| `prepare.py` | Data prep, tokenizer, dataloader, evaluation harness | **NO** | Fixed constants. Ground truth metric (`evaluate_bpb`) lives here. |
| `train.py` | Model architecture, optimizer, training loop | **YES** | The only file the agent edits. Contains full GPT model. |
| `program.md` | Agent instructions / research org spec | **YES** | Human edits this to tune the agent's behavior. Acts as a "skill." |
| `results.tsv` | Experiment log | **YES** (untracked) | Tab-separated: `commit val_bpb memory_gb status description` |

### Key Design Decisions

1. **Single File to Modify**
   - Only `train.py` is editable. This keeps diffs reviewable and scope manageable.
   - The agent can change anything inside it: architecture, optimizer, hyperparameters, batch size, model size.

2. **Fixed 5-Minute Time Budget**
   - Training stops after exactly 300 seconds of wall-clock training time (excluding startup/compilation).
   - This makes experiments **directly comparable regardless of what the agent changes** (model size, batch size, architecture).
   - Also means results are **not comparable across different hardware** — a 5-minute run on H100 ≠ 5-minute run on RTX 3080 Ti.
   - Expected throughput: ~12 experiments/hour, ~100 experiments/8-hour sleep cycle.

3. **Single Metric: `val_bpb`**
   - Validation bits per byte. Lower is better.
   - Vocab-size-independent, so architectural changes (that might change vocab size) are fairly compared.
   - Printed at the end of every run in a structured format:
     ```
     val_bpb:          0.997900
     training_seconds: 300.1
     total_seconds:    325.9
     peak_vram_mb:     45060.2
     mfu_percent:      39.80
     total_tokens_M:   499.6
     num_steps:        953
     num_params_M:     50.3
     depth:            8
     ```

4. **Git Branch Isolation**
   - Each experiment run creates a new branch: `autoresearch/<tag>` (e.g., `autoresearch/mar5`).
   - The agent commits its code change, runs the experiment, then either:
     - **Advances** the branch (keeps the commit) if `val_bpb` improved
     - **Resets** (`git reset`) if `val_bpb` is equal or worse
   - This creates a natural experiment history where every commit on the branch is a "keep."

5. **Simplicity Criterion**
   - All else being equal, simpler is better.
   - A 0.001 `val_bpb` improvement that adds 20 lines of hacky code? **Not worth it.**
   - A 0.001 improvement from **deleting code**? **Definitely keep.**
   - This criterion is explicitly encoded in `program.md` to prevent the agent from overfitting to complexity.

6. **Program-as-Prompt (`program.md`)**
   - This is the most novel architectural element. Instead of a Python orchestrator, the orchestration is a Markdown file that serves as a "skill" for the AI agent.
   - The human iterates on `program.md` to improve the agent's research strategy.
   - The default `program.md` is intentionally bare-bones — it's a baseline meant to be evolved.

### Model Architecture (from `train.py`)

Karpathy's model is a cherry-picked, simplified single-GPU implementation of his `nanochat` project:

- **GPT-style transformer** with these notable features:
  - **Flash Attention 3**: Uses `varunneal/flash-attention-3` on Hopper (H100), falls back to `kernels-community/flash-attn3` on non-Hopper GPUs.
  - **Value Embeddings (ResFormer)**: Alternating layers have value embeddings mixed in with an input-dependent gate per head. This is a recent architectural innovation.
  - **Muon + AdamW hybrid optimizer**: `setup_optimizer()` creates separate parameter groups with different learning rates (unembedding: 0.004, embedding: 0.2, matrix: 0.02, scalars: 0.5).
  - **Window patterns**: `"SSSL"` (Short-Short-Short-Long) attention pattern. Short = sequence_len // 2, Long = full sequence_len. The last layer is always Long.
  - **RMSNorm**: `F.rms_norm` used throughout.
  - **ReLU² activation**: In the MLP: `F.relu(x).square()` — this is the SoLU (Squared ReLU) variant.
  - **Rotary embeddings**: Precomputed, stored as buffers.
  - **Per-layer residual scalars**: `resid_lambdas` and `x0_lambdas` are learned per-layer scaling parameters.

- **Default config** (from `prepare.py` / `train.py`):
  - `MAX_SEQ_LEN = 2048`
  - `VOCAB_SIZE = 8192` (BPE tokenizer trained on the fly)
  - `DEPTH = 8` (primary knob for model complexity)
  - `TIME_BUDGET = 300` seconds
  - `EVAL_TOKENS = 40 * 524288` (~21M tokens for validation)

### Data Pipeline

- **Dataset:** `karpathy/climbmix-400b-shuffle` — 400B token shuffle, downloaded as Parquet shards
- **Tokenizer:** BPE trained with `rustbpe` (Rust-based BPE implementation), saved as `tiktoken` encoding
- **Cache:** Everything cached in `~/.cache/autoresearch/`

### Dependencies

Minimal but modern:
```
torch==2.9.1 (cu128)
kernels>=0.11.7 (Flash Attention 3)
rustbpe>=0.1.0
tiktoken>=0.11.0
pyarrow, requests, numpy, pandas, matplotlib
```

Uses `uv` as the project manager. No `requirements.txt` — pure `pyproject.toml`.

## Notable Forks Ecosystem

Karpathy actively links to platform-specific forks in his README:

| Fork | Platform | Author | Notes |
|------|----------|--------|-------|
| `miolini/autoresearch-macos` | macOS | miolini | |
| `trevin-creator/autoresearch-mlx` | macOS (MLX) | trevin-creator | Native Apple Silicon |
| `jsegov/autoresearch-win-rtx` | Windows (RTX) | jsegov | **This is the upstream of hummbl-dev's archived fork** |
| `andyluo7/autoresearch` | AMD GPU | andyluo7 | |

**Important:** `hummbl-dev/autoresearch-win-rtx` was a fork of `jsegov/autoresearch-win-rtx` (which itself forks Karpathy). The hummbl-dev version was archived on 2026-05-13. `hummbl-dev/autoresearch-pipeline` is now the canonical HUMMBL replacement.

## Key Innovations Worth Adopting

### 1. Program-as-Prompt (`program.md`)
**What it is:** A Markdown skill document that tells the agent exactly how to conduct research.
**Why it matters:** It decouples the orchestration logic from the code. A human can iterate on research strategy by editing Markdown, not Python.
**HUMMBL adoption:** HUMMBL's skills system (in `.claude/skills/`) could adopt this pattern. A `research-supervisor.md` skill could define the experimental protocol, and the actual pipeline code just enforces guardrails.

### 2. Fixed Time Budget
**What it is:** Training always runs for exactly 5 minutes, regardless of model changes.
**Why it matters:** Experiments are directly comparable. The agent can change model size, batch size, architecture — and the comparison is still fair because time is fixed.
**HUMMBL adoption:** The current `autoresearch-pipeline` uses a fixed iteration count. Adding a wall-clock time budget option would make cross-platform comparisons more meaningful (e.g., Anvil RTX vs nodezero M4).

### 3. Single Metric (`val_bpb`)
**What it is:** One number that captures everything. Lower is better.
**Why it matters:** No multi-objective optimization confusion. The agent always knows exactly what to optimize.
**HUMMBL adoption:** The current pipeline has multiple metrics. Consider adopting a primary single metric for the auto-optimization loop, even if secondary metrics are logged.

### 4. Simplicity Criterion
**What it is:** Explicit instruction to the agent that simpler code is preferred, and deletions are valued.
**Why it matters:** Prevents the agent from overfitting to complexity. Without this, agents tend to add increasingly hacky optimizations.
**HUMMBL adoption:** Could be encoded in the supervisor's experiment generation or in the worker's acceptance criteria.

### 5. Git Branch Advance/Reset Pattern
**What it is:** Every experiment is a commit. If it improves, keep it. If not, reset.
**Why it matters:** Creates an immutable, auditable experiment history. No state files needed — git IS the state.
**HUMMBL adoption:** The current pipeline uses JSON state files in `queue/` and `runs/`. While more robust for multi-worker fleets, the git-based approach is elegant for single-agent scenarios.

### 6. Minimal File Surface
**What it is:** Only 3 files that matter.
**Why it matters:** Agent context windows are limited. Fewer files = less token overhead = better reasoning.
**HUMMBL adoption:** HUMMBL's pipeline is already modular (supervisor/worker/healthcheck), but for the actual experiment repo (the thing the agent edits), a single-file constraint might improve agent performance.

## Gaps / Limitations

1. **No multi-GPU support:** Single GPU only. No distributed training.
2. **No multi-agent coordination:** One agent, one GPU, one file. No fleet.
3. **No cost governance:** No tracking of compute cost, API spend, or budget limits.
4. **No safety primitives:** No kill switch, circuit breaker, or delegation tokens. The agent has full git access.
5. **NVIDIA-only (upstream):** Karpathy explicitly states he's not supporting CPU/MPS. Forks handle this.
6. **No queue/scheduling:** Human has to manually start the agent each time.
7. **No cross-platform result comparability:** 5 minutes on H100 ≠ 5 minutes on RTX 3080 Ti.
8. **No proposal/finding pipeline:** Raw experiments are in git branches; there's no structured downstream review process.

## Competitive Positioning for HUMMBL

| Dimension | Karpathy's autoresearch | HUMMBL autoresearch-pipeline |
|-----------|------------------------|---------------------------|
| **Scale** | Single agent, single GPU | Multi-machine, multi-worker fleet |
| **Orchestration** | `program.md` (Markdown prompt) | Python supervisor + worker + queue |
| **Safety** | None (full git access) | Kill switch, circuit breaker, delegation tokens |
| **Cost** | No tracking | Cost governor integration |
| **Cross-platform** | NVIDIA only (upstream) | CUDA, MPS, MLX, CPU |
| **Results** | Git branches + `results.tsv` | Structured queue/runs + findings + proposals |
| **Scheduling** | Manual | Weekly automation (launchd/cron) |
| **Bus integration** | None | HUMMBL coordination bus |

**HUMMBL's moat:** Governance, fleet coordination, and safety primitives. Karpathy's version is a research toy (intentionally so — it's meant to be hacked on). HUMMBL's version is production infrastructure.

## Recommendations

1. **Adopt the `program.md` pattern** for HUMMBL's agent research skills. Create a `research-supervisor.md` skill that defines the experimental protocol in Markdown, consumed by both the supervisor and the human operator.

2. **Consider a wall-clock time budget option** in the pipeline, in addition to the current step-based budget. This would make cross-platform experiments more comparable.

3. **Steal the `val_bpb` metric pattern** for the primary optimization target. The current pipeline has multiple metrics — consider having a single primary metric that drives the supervisor's perturbation logic.

4. **Adopt the simplicity criterion** in the supervisor's experiment scoring. Favor experiments that delete code over experiments that add complexity, all else being equal.

5. **Study the `jsegov/autoresearch-win-rtx` fork** for Windows-specific adaptations that HUMMBL might have missed. This fork had 671 stars and was the most popular Windows adaptation before being archived.

6. **Monitor Karpathy's `program.md` evolution.** He explicitly states: "The default `program.md` in this repo is intentionally kept as a bare bones baseline, though it's obvious how one would iterate on it over time to find the 'research org code' that achieves the fastest research progress." This is an active research direction.

## Appendix: Raw Metrics from a Run

From Karpathy's README (`progress.png`):

```
val_bpb:          0.997900  (baseline)
training_seconds: 300.1
total_seconds:    325.9
peak_vram_mb:     45060.2
mfu_percent:      39.80
total_tokens_M:   499.6
num_steps:        953
num_params_M:     50.3
depth:            8
```

---

*Intel capture completed: 2026-06-20*
*Source: direct code review of karpathy/autoresearch + web research of fork ecosystem*
*Classification: OPEN SOURCE INTELLIGENCE — no proprietary information accessed*
