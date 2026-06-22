# Autoresearch Experiment Report: mar14-gemini

**Date:** 2026-03-15
**Repository:** https://github.com/hummbl-dev/autoresearch-win-rtx
**Branch:** `autoresearch/mar14-gemini`
**Hardware:** GPU (see commit history for details)
**Framework:** Karpathy Autoresearch (https://github.com/karpathy/autoresearch)

## Summary

- **Total experiments:** 5
- **Kept:** 4 | **Discarded:** 1 | **Crashed:** 0
- **Baseline val_bpb:** 0.836918
- **Best val_bpb:** 0.507040
- **Improvement:** 39.4%

## Experiment Results

| # | Commit | val_bpb | Memory | Status | Description |
|---|--------|---------|--------|--------|-------------|
| 1 | `ed9de37` | 0.836918 | 5.3 GB | keep | baseline (depth=8, batch=16, SSSL pattern) |
| 2 | `70481f8` | 1.213930 | 7.0 GB | discard | increase DEPTH 8 to 12 (135M params, undertrained in 5min) |
| 3 | `d75ad9d` | 0.556402 | 5.3 GB | keep | reduce TOTAL_BATCH_SIZE 2^19 to 2^17 (149 steps vs 46) |
| 4 | `83500c3` | 0.518628 | 5.3 GB | keep | reduce TOTAL_BATCH_SIZE 2^17 to 2^16 (282 steps) |
| 5 | `c0163cd` | 0.507040 | 5.2 GB | keep | reduce TOTAL_BATCH_SIZE 2^16 to 2^15 (543 steps) |

## Analysis

### Progression of Kept Experiments

- `ed9de37`: 0.836918 (unchanged, delta=+0.000000) — baseline (depth=8, batch=16, SSSL pattern)
- `d75ad9d`: 0.556402 (improved, delta=-0.280516) — reduce TOTAL_BATCH_SIZE 2^19 to 2^17 (149 steps vs 46)
- `83500c3`: 0.518628 (improved, delta=-0.037774) — reduce TOTAL_BATCH_SIZE 2^17 to 2^16 (282 steps)
- `c0163cd`: 0.507040 (improved, delta=-0.011588) — reduce TOTAL_BATCH_SIZE 2^16 to 2^15 (543 steps)

### Discarded Experiments (what didn't work)

- `70481f8`: increase DEPTH 8 to 12 (135M params, undertrained in 5min) (val_bpb=1.213930)

## Recommendations for Next Session

Based on the experiment trajectory:

- **Learning rate sweep** — not yet explored, likely high-impact
- **Architecture changes** — GQA, embedding width, activation functions not yet tried
- **Optimizer tuning** — AdamW parameters, schedule changes
- **Attention pattern** — sliding window, local attention variants
- **Continue current direction** — 39.4% improvement suggests more gains available

## Experiment Commit Log

- `f72bd5f` (2026-03-15T00:07) — exp: reduce TOTAL_BATCH_SIZE 2^15 -> 2^14
- `88696e4` (2026-03-14T23:54) — exp: reduce TOTAL_BATCH_SIZE 2^16 -> 2^15
- `83500c3` (2026-03-14T19:39) — exp: reduce TOTAL_BATCH_SIZE 2^17 -> 2^16 (double steps again)
- `36f55cd` (2026-03-14T19:39) — log: TOTAL_BATCH_SIZE 2^17 KEEP (0.5564 vs 0.8369 baseline, -33.5%)
- `d75ad9d` (2026-03-14T19:26) — exp: reduce TOTAL_BATCH_SIZE 2^19 -> 2^17 (4x more optimizer steps)
- `3752aa1` (2026-03-14T19:26) — log: DEPTH=12 discard (1.2139 vs 0.8369 baseline)
- `ed9de37` (2026-03-14T19:12) — setup: initialize results.tsv and customize program.md for RTX 3080 Ti

## References

- Experiment repository: https://github.com/hummbl-dev/autoresearch-win-rtx/tree/autoresearch/mar14-gemini
- Karpathy Autoresearch framework: https://github.com/karpathy/autoresearch
- TinyStories dataset: https://arxiv.org/abs/2305.07759
