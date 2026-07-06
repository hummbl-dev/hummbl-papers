# Experiment Receipt Discipline for Small-Model Autoresearch

**Status:** PROPOSED
**Date seeded:** 2026-07-06
**Author:** Reuben Bowlby
**Repository:** hummbl-dev/hummbl-papers
**Source packet:** hummbl-dev/research-source-packets#9 (candidate)

## Abstract

Small-model autoresearch loops can generate dozens of experiments per session, but without receipt discipline the results become unauditable: hypotheses blur into outcomes, baselines drift, noise floors go unmeasured, and negative results disappear. This paper scopes a case study of the `autoresearch-pipeline` corpus — 34 governed experiments, 2 kept patches, 32 DISCARD negative results — as a worked example of receipt-bearing autoresearch. The strongest finding is not a new architecture patch; it is the governance value of negative-result receipts and baseline discipline at small scale.

## Claim

Experiment receipts make small-model autoresearch auditable by separating five fields per experiment — hypothesis, baseline, noise floor, measured outcome, and KEEP/DISCARD decision — and preserving negative results as first-class evidence rather than silently dropping them.

## Method

This paper is a case study and methods analysis. The scoped method is:

1. Extract the receipt schema from the `autoresearch-pipeline` public corpus (`program.md`, `results.tsv`, `docs/experiment_receipts/*.md`).
2. Map the receipt fields to the failure modes they prevent (cherry-picking, baseline drift, noise-floor blindness, frontier-feature cargo-culting).
3. Quantify the corpus: 34 governed experiments, 2 kept patches, 32 DISCARD, 2 crash, noise-floor measurements (0.180 untuned → 0.005 tuned).
4. Identify what would be required for external replication beyond the 26M / short-training regime.

## System Boundary

This paper covers the public `autoresearch-pipeline` corpus through Pack 2 (PR #24). It does not cover the private founder-mode runtime that produced the corpus, operator schedules, machine-local paths, or live queue state. It does not assert that the 26M / short-training findings generalize.

## Preliminary Receipt Schema

Each governed experiment records:

- **Hypothesis** — what the experiment tests (e.g., "QK-Norm improves val_bpb at 26M scale").
- **Baseline** — the reference result the experiment is compared against (e.g., val_bpb=0.459677 from the may3 marathon session).
- **Noise floor** — the measured run-to-run variance under control conditions (e.g., 0.180 untuned, 0.005 tuned).
- **Measured outcome** — the val_bpb and step count the experiment produced.
- **Decision** — KEEP or DISCARD, with a bounded reason.

## Draft Outline

### 1. Problem

Autoresearch loops at small scale produce many experiments with small effect sizes. Without receipt discipline, the loop becomes vulnerable to cherry-picking, noise-floor blindness, and frontier-feature cargo-culting imported from large-model regimes where the dynamics differ.

### 2. Prior Art

The analysis will compare the receipt-discipline approach against ML reproducibility checklists (Pineau, NeurIPS), pre-registration standards (OSF, PCI RR), and notebook conventions (Pitt-Wipf observation/interpretation separation). The contribution is not the invention of receipts; it is the application of receipt discipline to a governed agent loop at small scale.

### 3. Receipt Contract

The paper will specify a minimal experiment receipt contract:

- one receipt per governed experiment
- five required fields (hypothesis, baseline, noise floor, outcome, decision)
- negative results preserved, not dropped
- noise floor measured before authorizing architecture experiments
- scale-dependence annotated per experiment idea pack

### 4. autoresearch-pipeline Case Study

The corpus provides the operational case. Candidate observations include:

- 32 of 34 experiments were DISCARD — negative results are the majority of the evidence, not appendix material.
- Two seed-repeat control experiments measured the noise floor before any architecture experiment was authorized.
- The Pack 2 nanochat frontier port (5 experiments, all DISCARD) demonstrates that frontier features do not transfer to 26M scale — a scale-dependence lesson preserved by the receipt discipline rather than silently lost.
- The 2 kept patches (BATCH 2x, BATCH 2x 10min) are improvements within the small-scale regime, not generalizable architecture claims.

### 5. Evaluation Plan

The first empirical pass should test whether receipt-bearing autoresearch reduces:

- silent dropping of negative results
- unmeasured noise floors before architecture experiments
- frontier-feature cargo-culting at scales where it does not apply
- disagreement between local status summaries and the receipt corpus

### 6. Limitations

The seed does not prove generality outside the 26M / short-training regime. The first version should present this as an internal case study with a reproducible public corpus, then identify what would be required for external replication at different scales.

## Public Source Artifacts

- [autoresearch-pipeline repository](https://github.com/hummbl-dev/autoresearch-pipeline)
- [program.md](https://github.com/hummbl-dev/autoresearch-pipeline/blob/main/program.md) — experiment program, baseline receipt, noise floor measurements
- [results.tsv](https://github.com/hummbl-dev/autoresearch-pipeline/blob/main/results.tsv) — 243 result rows, 34 governed experiments
- [docs/experiment_receipts/](https://github.com/hummbl-dev/autoresearch-pipeline/tree/main/docs/experiment_receipts) — 9 per-wave receipt docs
- [research-source-packets#9](https://github.com/hummbl-dev/research-source-packets/pull/9) — candidate source packet for the corpus
- [Research notebook](../../notebooks/experiment-receipt-discipline-small-model-autoresearch.notebook.md)

## Open Questions

- What is the smallest public replay fixture that demonstrates receipt-discipline value without exposing private runtime?
- Should the first version remain a technical report, or target a workshop paper format?
- What scale-dependence thresholds separate "frontier feature applies" from "frontier feature is cargo-culting"?
- Can the receipt schema be validated automatically, or does it require human review?
