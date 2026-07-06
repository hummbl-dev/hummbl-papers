# Experiment Receipt Discipline for Small-Model Autoresearch — Research Notebook

## Question (pre-registered, dated)

[2026-07-06] What does experiment receipt discipline add to small-model autoresearch when every governed experiment records hypothesis, baseline, noise floor, measured outcome, and KEEP/DISCARD decision — and negative results are preserved as first-class evidence?

## Method (pre-declared, before any data/derivation)

Case study plus methods analysis. Start from the public `autoresearch-pipeline` corpus, then extract the receipt schema, map it to failure modes it prevents, and quantify the corpus. Keep the scope bounded to the 26M / short-training regime unless a replication extends it.

## Predictions (timestamped BEFORE observations)

[2026-07-06] The strongest contribution will be the negative-result preservation claim: 32 of 34 experiments were DISCARD, and the governance value is in keeping them rather than silently dropping them.

[2026-07-06] The most likely reviewer objection is scale-dependence — that the 26M / short-training findings do not generalize. The first draft should not overclaim beyond the corpus's own regime.

[2026-07-06] The cleanest measurable outcome will be receipt completeness: what fraction of governed experiments have all five receipt fields populated, and what fraction of negative results are preserved in the corpus.

[2026-07-06] The Pack 2 nanochat frontier port (5 experiments, all DISCARD) will be the most instructive negative-result case: it demonstrates that frontier features do not transfer to 26M scale, a lesson that receipt discipline preserves rather than silently loses.

## Observations (append-only, dated)

[2026-07-06] Issue hummbl-dev/hummbl-papers#14 asks for a candidate paper on experiment receipt discipline for small-model autoresearch. The coordination-bus seed (#13) has already landed, clearing the gate ("do not draft until the coordination-bus seed PR lands").

[2026-07-06] The `autoresearch-pipeline` repository has a public experiment receipt corpus suitable as the worked example: `program.md`, `results.tsv` (243 data rows), and `docs/experiment_receipts/*.md` (9 receipt docs through Pack 2).

[2026-07-06] Corpus quantification at main commit `f39a3ee`:
- 34 governed experiments (PRs #16, #18-#24)
- 2 kept patches: BATCH 2x (PR #20), BATCH 2x 10min (PR #22)
- 32 DISCARD negative results
- 2 crash results
- Noise floor measured twice: 0.180 (untuned config, PR #16) → 0.005 (tuned config, PR #18)
- Pack 2 nanochat frontier port: 5 experiments, all DISCARD (PR #24)

[2026-07-06] The candidate source packet (research-source-packets#9) describes the corpus as a first-party experiment receipt source. It is candidate-only and bounds claims to the 26M / short-training regime.

[2026-07-06] The ROADMAP now lists this paper as seeded artifact #2 (PROPOSED) and pre-registered backlog entry #21.

## Interpretation (separated from Observations)

[2026-07-06] This paper is a methods paper, not an architecture paper. The contribution is the receipt discipline, not the 2 kept patches. The 32 DISCARD results are the evidence that the discipline works — they were preserved rather than silently dropped.

[2026-07-06] The noise-floor measurements (PR #16, PR #18) are the strongest example of receipt discipline preventing a failure mode: without measuring the noise floor first, the QK-Norm experiment would have been authorized against an untuned config where the noise floor (0.180) was 36-90x larger than the expected improvement. The receipt discipline caught this before any architecture experiment ran.

[2026-07-06] The Pack 2 frontier port is the strongest scale-dependence case: 5 frontier features tested at 26M scale, all DISCARD. This is not a failure of the features; it is a success of the receipt discipline in preserving the negative result so future work does not re-test them at the same scale.

## Dead ends (failed attempts, also first-class)

- [2026-07-06] Considered drafting a full paper before the source packet landed. Rejected because the source packet (research-source-packets#8/#9) is the prerequisite — the paper needs a bounded source contract before it can cite the corpus.

- [2026-07-06] Considered claiming generality beyond the 26M / short-training regime. Rejected because the corpus has not been replicated at other scales. The paper must bound its claims to the regime it has evidence for.

## Open questions

- What is the smallest public replay fixture that demonstrates receipt-discipline value without exposing private runtime?
- Should the first version remain a technical report, or target a workshop paper format?
- What scale-dependence thresholds separate "frontier feature applies" from "frontier feature is cargo-culting"?
- Can the receipt schema be validated automatically, or does it require human review?
- Should the paper propose a formal receipt schema (JSON Schema or similar), or keep the five-field description informal?

## Cross-references

- Source packet: hummbl-dev/research-source-packets#9 (candidate)
- Source corpus: hummbl-dev/autoresearch-pipeline (main commit `f39a3ee`)
- Parent issue: hummbl-dev/hummbl-papers#14
- Batch receipt: hummbl-dev/hummbl-papers#15
- Sibling paper: hummbl-dev/hummbl-papers#13 (coordination-bus seed, SCOPED)
- Evidence graph: hummbl-dev/hummbl-dev#104 (Cross-Repo Evidence Graph v0.1)
