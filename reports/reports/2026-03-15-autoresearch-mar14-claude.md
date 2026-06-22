# Autoresearch Experiment Report: mar14-claude

**Date:** 2026-03-15
**Repository:** https://github.com/hummbl-dev/autoresearch-win-rtx
**Branch:** `autoresearch/mar14-claude`
**Hardware:** GPU (see commit history for details)
**Framework:** Karpathy Autoresearch (https://github.com/karpathy/autoresearch)

## Summary

- **Total experiments:** 4
- **Kept:** 3 | **Discarded:** 1 | **Crashed:** 0
- **Baseline val_bpb:** 0.836918
- **Best val_bpb:** 0.518628
- **Improvement:** 38.0%

## Experiment Results

| # | Commit | val_bpb | Memory | Status | Description |
|---|--------|---------|--------|--------|-------------|
| 1 | `ed9de37` | 0.836918 | 5.3 GB | keep | baseline (depth=8, batch=16, SSSL pattern) |
| 2 | `70481f8` | 1.213930 | 7.0 GB | discard | increase DEPTH 8 to 12 (135M params, undertrained in 5min) |
| 3 | `d75ad9d` | 0.556402 | 5.3 GB | keep | reduce TOTAL_BATCH_SIZE 2^19 to 2^17 (149 steps vs 46) |
| 4 | `83500c3` | 0.518628 | 5.3 GB | keep | reduce TOTAL_BATCH_SIZE 2^17 to 2^16 (282 steps) |

## Analysis

### Progression of Kept Experiments

- `ed9de37`: 0.836918 (unchanged, delta=+0.000000) — baseline (depth=8, batch=16, SSSL pattern)
- `d75ad9d`: 0.556402 (improved, delta=-0.280516) — reduce TOTAL_BATCH_SIZE 2^19 to 2^17 (149 steps vs 46)
- `83500c3`: 0.518628 (improved, delta=-0.037774) — reduce TOTAL_BATCH_SIZE 2^17 to 2^16 (282 steps)

### Discarded Experiments (what didn't work)

- `70481f8`: increase DEPTH 8 to 12 (135M params, undertrained in 5min) (val_bpb=1.213930)

## Recommendations for Next Session

Based on the experiment trajectory:

- **Learning rate sweep** — not yet explored, likely high-impact
- **Architecture changes** — GQA, embedding width, activation functions not yet tried
- **Optimizer tuning** — AdamW parameters, schedule changes
- **Attention pattern** — sliding window, local attention variants
- **Continue current direction** — 38.0% improvement suggests more gains available

## Experiment Commit Log

- `9f33975` (2026-03-14T19:48) — log: TOTAL_BATCH_SIZE 2^16 KEEP (0.5186 vs 0.5564, another improvement)
- `83500c3` (2026-03-14T19:39) — exp: reduce TOTAL_BATCH_SIZE 2^17 -> 2^16 (double steps again)
- `36f55cd` (2026-03-14T19:39) — log: TOTAL_BATCH_SIZE 2^17 KEEP (0.5564 vs 0.8369 baseline, -33.5%)
- `d75ad9d` (2026-03-14T19:26) — exp: reduce TOTAL_BATCH_SIZE 2^19 -> 2^17 (4x more optimizer steps)
- `3752aa1` (2026-03-14T19:26) — log: DEPTH=12 discard (1.2139 vs 0.8369 baseline)
- `ed9de37` (2026-03-14T19:12) — setup: initialize results.tsv and customize program.md for RTX 3080 Ti

## References

- Experiment repository: https://github.com/hummbl-dev/autoresearch-win-rtx/tree/autoresearch/mar14-claude
- Karpathy Autoresearch framework: https://github.com/karpathy/autoresearch
- TinyStories dataset: https://arxiv.org/abs/2305.07759
