# After Action Report: autoresearch mar14 session

**Date:** 2026-03-14
**Repo:** hummbl-dev/autoresearch-win-rtx
**Hardware:** NVIDIA RTX 3080 Ti (12GB VRAM), Windows desktop
**Dataset:** TinyStories

---

## Summary

Two AI models were tasked with running Karpathy's autoresearch framework autonomously on an RTX 3080 Ti. Claude (Opus) ran first and was interrupted by a thermal shutdown. Gemini 2.5 Pro (via Vertex AI) was launched to continue. Gemini underperformed significantly — producing only 2 new experiments before stopping, and failing to set up infrastructure correctly.

## Timeline

### Claude session (autoresearch/mar14-claude)

| # | Commit | val_bpb | Status | Description |
|---|--------|---------|--------|-------------|
| 1 | ed9de37 | 0.8369 | keep | Baseline (depth=8, batch=16, SSSL) |
| 2 | 70481f8 | 1.2139 | discard | Depth 8->12 (undertrained in 5min) |
| 3 | d75ad9d | 0.5564 | keep | TOTAL_BATCH_SIZE 2^19 -> 2^17 |
| 4 | 83500c3 | 0.5186 | keep | TOTAL_BATCH_SIZE 2^17 -> 2^16 |

**Outcome:** 4 experiments, 3 kept. Best val_bpb: **0.5186**. Session ended by thermal shutdown (GPU training + game running simultaneously overloaded CPU thermals).

### Gemini 2.5 Pro session (autoresearch/mar14-gemini)

| # | Commit | val_bpb | Status | Description |
|---|--------|---------|--------|-------------|
| 5 | c0163cd | 0.5070 | keep | TOTAL_BATCH_SIZE 2^16 -> 2^15 |
| 6 | f72bd5f | ??? | not logged | TOTAL_BATCH_SIZE 2^15 -> 2^14 |

**Outcome:** 2 experiments, 1 kept, 1 incomplete. Best val_bpb: **0.5070**. Session ended on its own — Gemini stopped autonomously despite instructions to never stop.

## Issues identified

### 1. Gemini stopped autonomously (critical)

`program.md` explicitly states: *"NEVER STOP... The human might be asleep, or gone from a computer and expects you to continue working indefinitely until you are manually stopped."* Gemini stopped after 2 experiments. This is a fundamental failure to follow the core instruction.

### 2. No strategy diversity (major)

Gemini only continued the batch size reduction pattern that Claude had already started. It never attempted:
- Learning rate sweeps (Phase 1)
- Window pattern changes (Phase 1)
- Architecture changes — GQA, embedding width, activations (Phase 2)
- Optimizer tuning (Phase 3)
- Any creative/radical ideas (Phase 4)

It pattern-matched "batch size was going down" and did the obvious next step twice.

### 3. Incomplete experiment logging (moderate)

Experiment 6 (2^14) was committed to git but never evaluated or logged to `results.tsv`. The `train.py` was left pointing at `2^14` with no record of whether it improved or regressed.

### 4. Failed to set up git remote (moderate)

Origin was still pointing at `jsegov/autoresearch-win-rtx` (the source fork). Gemini never forked the repo or updated the remote, making it impossible to push results. Claude Code had to fix this after the fact — forking to `hummbl-dev/autoresearch-win-rtx` and pushing both branches.

## Final state

- **Best val_bpb across both sessions:** 0.5070 (Gemini exp 5)
- **Improvement over baseline:** 39.4% (0.8369 -> 0.5070)
- **Both branches pushed to:** github.com/hummbl-dev/autoresearch-win-rtx
- **Thermal shutdown cause:** GPU training + game running concurrently exceeded CPU thermal limits. BIOS v1.50 update may help with thermal management going forward.

## Recommendations

1. **Do not use Gemini 2.5 Pro for long-running autonomous agentic loops.** It does not reliably follow "never stop" instructions and lacks strategy diversity.
2. **Resume with Claude.** The experiment is only through early Phase 1. Significant gains likely remain in LR tuning, architecture changes, and optimizer experiments.
3. **Close the game before starting training runs.** The thermal shutdown was avoidable.
4. **Fork repos before starting autoresearch sessions** so results can be pushed immediately.
