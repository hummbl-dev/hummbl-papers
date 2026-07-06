# Research Roadmap

Portfolio status, pre-registered backlog, and active work.

> **DOI strategy:** Each paper gets its own Zenodo deposit (Pattern A). The GitHub→Zenodo webhook on this repo is reserved for future code/data releases only. See [docs/method/doi-strategy.md](docs/method/doi-strategy.md).
>
> **Drafting vs publishing:** Papers are drafted privately in founder-mode, then copied to `papers/{slug}/` at publication. Post-publication edits happen in hummbl-papers only. See [docs/method/drafting-to-publishing-convention.md](docs/method/drafting-to-publishing-convention.md).

## Legend

- **Status**: `PROPOSED` → `SCOPED` → `DRAFTING` → `REVIEW` → `SHIPPED`
- **Method**: formal proof · empirical · case study · survey/synthesis
- **Audience**: academic · industry practitioner · regulator

## Shipped (to be populated as papers are seeded)

_Papers enter this table after publication. Each paper receives its own Zenodo deposit, then its own concept DOI._

| # | Title | Claim | Method | arXiv | Zenodo DOI |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Seeded artifacts (pre-publication)

| # | Title | Status | Claim | Method | Notebook |
|---|---|---|---|---|---|
| 1 | [Coordination Bus as Governed Agent Infrastructure](papers/coordination-bus-governed-agent-infrastructure/README.md) | SCOPED | An append-only coordination bus can improve queue control and audit reconstruction when evidence is kept separate from execution authority. | case study | [notebook](notebooks/coordination-bus-governed-agent-infrastructure.notebook.md) |
| 2 | [Experiment Receipt Discipline for Small-Model Autoresearch](papers/experiment-receipt-discipline-small-model-autoresearch/README.md) | PROPOSED | Experiment receipts make small-model autoresearch auditable by separating hypothesis, baseline, noise floor, measured outcome, and KEEP/DISCARD decision; the strongest finding is the governance value of negative-result receipts and baseline discipline, not a new architecture patch. | case study | [notebook](notebooks/experiment-receipt-discipline-small-model-autoresearch.notebook.md) |

## Hardening (in flight, founder-mode paper sprint)

_Active multi-round hardening sweep in progress on the founder-mode workspace as of 2026-04-16. Results will move here once first paper is mirrored._

Papers in the current sweep (see founder-mode `docs/publications/` for drafts):

- AGENTIC_IDENTITY
- AGENTIC_IDENTITY_RECOVERY
- ASHBY_GOVERNANCE
- BASE120_FORMAL
- BENCHMARK_DECAY
- BKI_GOVERNANCE
- COMPLIANCE_THEATER
- COORDINATION_BUS — seeded here as [Coordination Bus as Governed Agent Infrastructure](papers/coordination-bus-governed-agent-infrastructure/README.md)
- DELEGATION_DEPTH
- DEPTH_LAUNDERING
- FRAMEWORK_CROSSWALK
- HCI_GOVERNANCE_RECEIPTS
- KILL_SWITCH_FORMAL
- PHANTOM_AUTHORITY
- TOKEN_BUDGET_GOVERNANCE
- TRACE_EVALUATION
- TUPLE_ATOMIC_RECORD
- VERUM_GOVERNANCE
- (plus 2 additional)

## Pre-registered backlog (next 20+)

_Each backlog entry declares what the paper proves BEFORE drafting begins. Pre-registration discipline from the clinical / open-science tradition._

### Template for a backlog entry

```markdown
### #21 — {Working title}

- **Claim (one sentence):** What the paper proves.
- **Method:** formal proof | empirical | case study | survey/synthesis
- **Audience:** academic | practitioner | regulator
- **Depends on:** {list of shipped papers it builds on}
- **Effort:** S | M | L
- **Status:** PROPOSED | SCOPED | DRAFTING | REVIEW
- **Notebook:** `notebooks/{paper-slug}.notebook.md`
- **Pre-registered:** YYYY-MM-DD
```

_Backlog entries to be added._

### #21 — Experiment Receipt Discipline for Small-Model Autoresearch

- **Claim (one sentence):** Experiment receipts make small-model autoresearch auditable by separating hypothesis, baseline, noise floor, measured outcome, and KEEP/DISCARD decision; the strongest finding is the governance value of negative-result receipts and baseline discipline, not a new architecture patch.
- **Method:** case study
- **Audience:** academic · industry practitioner
- **Depends on:** — (first methods paper; complements #1 coordination-bus case study)
- **Effort:** M
- **Status:** PROPOSED
- **Notebook:** `notebooks/experiment-receipt-discipline-small-model-autoresearch.notebook.md`
- **Pre-registered:** 2026-07-06
- **Source packet:** `hummbl-dev/research-source-packets#9` (first-party experiment receipt corpus, candidate-only)
- **Scope boundary:** Do not claim generality beyond the 26M-parameter / short-training regime until replicated.

## Conventions

- Every paper gets a sibling `.notebook.md` in `notebooks/` (see `notebooks/README.md`)
- Pre-registered backlog entries must declare the claim and method before drafting
- Status transitions are dated in the per-paper notebook, not here — this file shows *current* state only
- Retired / abandoned papers move to a `## Archived` section with a short reason, not deleted

## Cross-cutting synthesis (future)

Once ~30 papers are shipped, this repository will gain a `docs/synthesis/` directory containing a meta-paper that maps the portfolio's connective tissue — the unified thesis across the primitives.
