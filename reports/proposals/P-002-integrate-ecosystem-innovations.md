# Proposal P-002: Integrate Top 4 Ecosystem Innovations into Autoresearch-Pipeline

## Problem

HUMMBL's autoresearch-pipeline has production-grade governance (kill switch, circuit breaker, cost governor, delegation tokens, governance bus) but its experiment selection and learning mechanisms are primitive compared to the broader autonomous research agent ecosystem. Specifically:

1. **Random perturbation** — The supervisor uses `random.choice` to select which hyperparameter to perturb next. This is worse than grid search and far worse than Bayesian optimization.
2. **No failure memory** — When an experiment is discarded, its lessons are lost. The pipeline has no mechanism to capture "this failed because X" for future reference.
3. **Noisy keep/discard decisions** — The supervisor treats a 0.0001 improvement as "keep" and a 0.0001 regression as "discard" without statistical rigor. Measurement noise causes false positives/negatives.
4. **Static agent prompts** — The supervisor and worker behavior never evolves. Unlike Sibyl's self-evolving system, HUMMBL's pipeline runs the same code on week 1 and week 52.

These gaps mean HUMMBL's pipeline optimizes slower, repeats mistakes, and cannot improve its own research strategy over time.

## Proposed Change

Integrate four proven innovations from the autonomous research ecosystem into HUMMBL's pipeline:

### 1. Bayesian Experiment Selection (from `ErikDeBruijn/autoresearcher2`)

Replace the supervisor's `random.choice` perturbation logic with a lightweight Bayesian factor model.

**Implementation:**
- Maintain a `factor_model.json` in the pipeline root that tracks:
  - Each parameter's prior distribution (mean, variance)
  - Observed effect sizes per parameter change
  - Interaction terms between parameters (e.g., LR × batch size)
  - Uncertainty estimates for each factor
- When selecting the next experiment, sample from the posterior rather than uniformly random
- After each experiment, update the model using the observed delta in `val_bpb`
- Use Thompson Sampling or Upper Confidence Bound (UCB) for exploration/exploitation balance

**File changes:**
- `supervisor/supervisor.py`: Replace `choose_perturbation()` with Bayesian factor model
- New: `supervisor/factor_model.py` — lightweight Bayesian update logic (stdlib + numpy)
- New: `supervisor/factor_model.json` — persistent model state

### 2. ASI — Actionable Side Information (from `proyecto26/autoresearch-ai-plugin`)

Add structured annotations to every experiment that survive git reverts and queue resets.

**Implementation:**
- Extend `experiment.json` schema with an `asi` field:
  ```json
  {
    "asi": {
      "hypothesis": "Increasing LR will improve convergence",
      "risk_factors": ["may cause instability", "sensitive to warmup"],
      "expected_effect_size": 0.005,
      "confidence": 0.7,
      "tags": ["optimizer", "lr"]
    }
  }
  ```
- When an experiment is discarded, its ASI is preserved in a `discarded_experiments.jsonl` log
- The supervisor reads this log before proposing new experiments to avoid repeating failed hypotheses
- ASI annotations are queryable: "show me all failed experiments tagged 'batch_size'"

**File changes:**
- `supervisor/supervisor.py`: Add ASI generation to `build_experiment_spec()`
- New: `supervisor/asi_store.py` — append-only JSONL store for discarded experiments
- New: `tests/test_asi_store.py` — unit tests

### 3. MAD Confidence Scoring (from `proyecto26/autoresearch-ai-plugin`)

Use Median Absolute Deviation to separate real improvements from measurement noise before deciding keep/discard.

**Implementation:**
- After each experiment, compute the delta vs baseline
- Calculate the MAD of recent deltas (last 20 experiments)
- A delta is "significant" only if |delta| > 2 × MAD
- If the delta is not significant, the supervisor marks the experiment as `uncertain` rather than `keep` or `discard`
- Uncertain experiments are rerun (with different seeds or small perturbations) before a final decision
- This prevents the pipeline from chasing noise

**File changes:**
- `supervisor/supervisor.py`: Add `evaluate_significance()` function
- New: `supervisor/significance.py` — MAD calculation and significance testing
- `worker/worker.py`: Report MAD and significance in `metrics.json`

### 4. Self-Evolution Outer Loop (from `Sibyl-Research-Team/sibyl`)

After every N experiments (e.g., weekly), analyze the research process itself and update the pipeline's behavior.

**Implementation:**
- Add a `self_evolve.py` script that runs after each weekly batch:
  1. **Classify issues**: Scan `runs/` for failure patterns (OOM, NaN, timeout, crash) and categorize them
  2. **Extract lessons**: For each category, generate a "lesson" (e.g., "LR > 0.01 causes NaN on this hardware")
  3. **Update prompts**: Inject lessons into a `lessons_learned.md` file that the supervisor reads at startup
  4. **Tune strategy**: Adjust exploration rate, time budget, or device selection based on historical success rates
  5. **Post to bus**: Report evolution events to the governance bus
- The `lessons_learned.md` acts as a dynamic "skill" for the supervisor, similar to Karpathy's `program.md`
- Lessons are time-decayed: older lessons have less weight

**File changes:**
- New: `scripts/self_evolve.py` — weekly self-evolution analysis
- New: `supervisor/lessons_learned.md` — dynamic skill document
- `supervisor/supervisor.py`: Load `lessons_learned.md` at startup
- `scripts/weekly_run.py`: Add `self_evolve.py` as the final step

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Weekly Orchestrator                       │
│                   (scripts/weekly_run.py)                    │
└──────────────────┬──────────────────────┬───────────────────┘
                   │                      │
         ┌─────────▼─────────┐   ┌───────▼────────┐
         │  Supervisor Loop  │   │  Self-Evolve   │
         │                   │   │  (after batch) │
         │ ┌───────────────┐ │   │                │
         │ │ Factor Model  │ │   │ 1. Classify    │
         │ │ (Bayesian)    │ │   │    failures    │
         │ └───────────────┘ │   │ 2. Extract     │
         │         │         │   │    lessons     │
         │ ┌───────▼───────┐ │   │ 3. Update      │
         │ │ ASI Generator │ │   │    lessons.md  │
         │ └───────────────┘ │   │ 4. Tune        │
         │         │         │   │    strategy    │
         │ ┌───────▼───────┐ │   │ 5. Post to bus │
         │ │ Significance  │ │   └────────────────┘
         │ │ (MAD scoring) │ │
         │ └───────────────┘ │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │     Worker Loop     │
         │                     │
         │ Runs experiments    │
         │ Reports metrics     │
         └─────────┬───────────┘
                   │
         ┌─────────▼─────────┐
         │   ASI Store       │
         │   (discarded      │
         │    experiments)   │
         └───────────────────┘
```

## Expected Impact

| Dimension | Before | After |
|-----------|--------|-------|
| Experiment selection | Random | Bayesian (faster convergence) |
| Failure memory | None | ASI annotations (avoids repetition) |
| Keep/discard noise | Arbitrary threshold | MAD-based significance (fewer false positives) |
| Agent behavior | Static | Self-evolving (improves weekly) |
| Convergence speed | ~100 experiments/baseline | ~50 experiments/baseline (estimated) |
| Governance | Best-in-class | Still best-in-class + now smartest |

## Risk

| Risk | Mitigation |
|------|------------|
| Factor model overfits to early experiments | Use weak priors and regularization; reset model if no improvement for 20 experiments |
| ASI store grows unbounded | Prune entries older than 90 days; compress similar annotations |
| MAD scoring is too conservative | Make the threshold configurable (default 2× MAD, operator can set 1.5× or 3×) |
| Self-evolution creates drift | Version-control `lessons_learned.md`; operator can revert to previous version |
| Implementation complexity | Ship incrementally: (1) MAD, (2) ASI, (3) Bayesian, (4) Self-evolve |

## Implementation Plan

| Phase | Deliverable | Timeline | Owner |
|-------|-------------|----------|-------|
| 1 | MAD confidence scoring | 1 week | Agent |
| 2 | ASI annotations + store | 1 week | Agent |
| 3 | Bayesian factor model | 2 weeks | Agent |
| 4 | Self-evolution outer loop | 2 weeks | Agent |
| 5 | Integration test + benchmark | 1 week | Agent |
| 6 | Documentation + operator runbook update | 1 week | Agent |

## Acceptance Criteria

- [ ] MAD scoring reduces false-positive keeps by >30% (measure: count of experiments kept then later reverted)
- [ ] ASI store captures >90% of discarded experiments with meaningful annotations
- [ ] Bayesian model converges to better `val_bpb` than random in <50 experiments (benchmark: run 5 A/B campaigns)
- [ ] Self-evolution produces at least 1 actionable lesson per weekly batch
- [ ] All new code has pytest coverage >80%
- [ ] No regression to existing governance primitives
- [ ] Operator can disable any of the 4 features independently via env vars

## Related

- **Finding:** F-005 (Autonomous Research Agent Ecosystem Landscape)
- **Finding:** F-004 (Karpathy autoresearch architecture capture)
- **Repos:** `ErikDeBruijn/autoresearcher2`, `proyecto26/autoresearch-ai-plugin`, `Sibyl-Research-Team/sibyl`
- **Queue IDs:** RQ-2026Q3-006 (agent coordination), RQ-2026Q3-007 (cognitive ledger)

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `NEMOCLAW_BAYESIAN` | `true` | Enable Bayesian experiment selection |
| `NEMOCLAW_ASI` | `true` | Enable ASI annotations |
| `NEMOCLAW_MAD_THRESHOLD` | `2.0` | MAD multiplier for significance threshold |
| `NEMOCLAW_SELF_EVOLVE` | `true` | Enable self-evolution outer loop |
| `NEMOCLAW_LESSONS_FILE` | `supervisor/lessons_learned.md` | Path to dynamic skill document |

---

*Proposal version: 1.0 | Created: 2026-06-21 | Phase: 4+*
*Classification: STRATEGIC — competitive positioning in autonomous research ecosystem*
