# Research Roadmap

Portfolio status, pre-registered backlog, and active work.

## Legend

- **Status**: `PROPOSED` → `SCOPED` → `DRAFTING` → `REVIEW` → `SHIPPED`
- **Method**: formal proof · empirical · case study · survey/synthesis
- **Audience**: academic · industry practitioner · regulator

## Shipped (to be populated as papers are seeded)

_First paper will be seeded here once the founder-mode paper-hardening session posts a done-STATUS and a paper is selected for Zenodo release._

| # | Title | Claim | Method | DOI |
|---|---|---|---|---|
| — | — | — | — | — |

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
- COORDINATION_BUS
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

## Conventions

- Every paper gets a sibling `.notebook.md` in `notebooks/` (see `notebooks/README.md`)
- Pre-registered backlog entries must declare the claim and method before drafting
- Status transitions are dated in the per-paper notebook, not here — this file shows *current* state only
- Retired / abandoned papers move to a `## Archived` section with a short reason, not deleted

## Cross-cutting synthesis (future)

Once ~30 papers are shipped, this repository will gain a `docs/synthesis/` directory containing a meta-paper that maps the portfolio's connective tissue — the unified thesis across the primitives.
