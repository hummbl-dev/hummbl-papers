# HUMMBL Universal Publication Readiness Gate v0.1

**Status: CANDIDATE IMPLEMENTATION GATE — NO AUTOMATIC PUBLICATION AUTHORITY**

Issue: hummbl-dev/hummbl-papers#19
Parent standard: hummbl-dev/hummbl-governance#225

## Purpose

A reusable publication-readiness gate for all HUMMBL scholarly
artifacts, regardless of discipline or project. This gate generalizes
the project-specific publication-gate pattern already used in this
repository. It does not replace project-specific gates; it defines
the minimum common gate they must satisfy.

## Artifact classes

| Class | Meaning |
|-------|---------|
| `EXPLORATORY_NOTE` | Early speculative work |
| `INTERNAL_RESEARCH_MEMO` | Internal analysis |
| `DATED_TECHNICAL_REPORT` | Dated engineering report |
| `REPRODUCIBILITY_PACKET` | Full reproducibility evidence |
| `PREPRINT_CANDIDATE` | Ready for preprint server |
| `VENUE_SUBMISSION_CANDIDATE` | Ready for venue submission |
| `SUBMITTED_MANUSCRIPT` | Under review |
| `PEER_REVIEWED_PUBLICATION` | Accepted and published |
| `CORRECTION` | Correcting a prior artifact |
| `SUPERSESSION` | Replacing a prior artifact |
| `RETRACTION` | Retracting a prior artifact |

A GitHub report, DOI deposit, arXiv preprint, conference submission,
and peer-reviewed article are different states and must not be
conflated.

## Gate dimensions

### A. Contribution and novelty
- Exact research question
- Strongest prior art and nearest neighbors
- Narrow contribution claim
- Explicit non-novel components
- Independent novelty challenge
- Discipline-adjacent search, not keyword-only search

### B. Evidence and methods
- Claim-to-evidence map
- Methods sufficient for scrutiny
- Data/code/source lineage
- Exclusions, assumptions, failure cases
- Negative/null results
- Uncertainty and limitations
- Calculation and figure verification

### C. Reproducibility
- Environment and dependency lock
- Exact artifact versions and commit SHAs
- Commands and expected outputs
- Random seeds and nondeterminism disclosure
- Data availability or justified restrictions
- Independent reproduction attempt where proportionate
- Distinction between reproducibility, replication, and conceptual illustration

### D. Authorship and AI disclosure
- Human authors and accountable corresponding contact
- Contribution record
- Conflicts and funding/incentive disclosure
- Material AI/model/tool assistance record
- Venue-specific authorship and AI policy verification at submission time
- No agent/model represented as human author or legitimacy source

### E. Ethics, privacy, rights, and licenses
- Human-subjects / participant determination
- Sensitive-data determination
- Consent and publication boundaries
- Dataset, code, image, quotation, and figure rights
- Dual-use or harm review where relevant
- Legal/regulatory caveat where relevant

### F. Independent review
- Methods review
- Evidence and calculation review
- Novelty/prior-art review
- Reproducibility review
- Reputational-risk review
- Unresolved objection log

The originating agent or author cannot be the sole reviewer.

### G. Public communication
- Title and abstract do not overstate maturity
- Public summary preserves limitations
- Preprint status is explicit
- No "peer reviewed" claim before actual peer review
- No marketing claim stronger than the artifact
- Correction contact and version history are visible

## Gate dispositions

Every candidate receives exactly one disposition:

| Disposition | Meaning |
|-------------|---------|
| `BLOCK` | Cannot proceed — critical failure |
| `RESEARCH_NOTE_ONLY` | May circulate internally as a note |
| `INTERNAL_REPORT_READY` | Ready as internal technical report |
| `TECHNICAL_REPORT_READY` | Ready as dated technical report |
| `PREPRINT_READY` | Ready for preprint server |
| `SUBMISSION_READY` | Ready for venue submission |
| `PUBLICATION_READY` | Peer reviewed and ready for publication |
| `CORRECTION_REQUIRED` | Must correct before proceeding |
| `SUPERSEDE` | Replace prior artifact |
| `RETRACT` | Retract prior artifact |

The gate must explain the evidence and unresolved risks supporting
the disposition.

## Anti-gaming requirements

The gate must reject:

- Polished prose with weak methods
- Citation volume substituted for prior-art analysis
- Self-review represented as independence
- Passing tests represented as scientific validation
- Internal benchmarks represented as external generality
- Synthetic examples represented as empirical evidence
- Benchmark selection after observing favorable results without disclosure
- Hidden exclusions or failed runs
- arXiv posting represented as peer review
- DOI assignment represented as quality validation
- Agent-generated citations not independently verified

## Gate schema

See `gate-decision.schema.json` for the JSON Schema.

## Migration note

Existing project-specific publication gates (e.g., in `hummbl-papers`)
should be mapped to this gate as a minimum common standard. Projects
may impose stricter requirements but may not relax these.

| Existing gate | Migration action |
|---------------|-----------------|
| `hummbl-papers` release validation | Map release stages to artifact classes |
| `hummbl-governance` admission logic | Map admission to gate disposition |
| `hummbl-research` campaign gates | Map campaign stages to artifact classes |

No existing artifact is grandfathered into compliance without evidence.

## Pilot applications

Apply the candidate gate retrospectively, without grandfathering, to:

1. One existing HUMMBL technical report
2. One blocked publication issue
3. LLL Engineering as a preprint candidate
4. One project that should remain a research note

The pilot should reveal false positives, unnecessary bureaucracy,
and missing controls before organization-wide adoption.

## Acceptance criteria

- [x] Gate is discipline-neutral — dimensions A-G cover engineering, CS, governance, health, biology, humanities, interdisciplinary
- [x] It preserves project-specific stricter requirements — migration note allows stricter
- [x] It requires current venue-policy verification — dimension D, venue_policy_check in schema
- [x] It distinguishes artifact maturity from scientific validity — artifact classes vs dispositions
- [x] It includes independent review and correction paths — dimension F, correction/supersession/retraction dispositions
- [x] It cannot be satisfied solely by an agent reviewing its own output — dimension F requires reviewer_not_author
- [ ] Pilot results and failures are preserved — PENDING
- [ ] Organization-wide enforcement waits for parent-standard review and Reuben approval — PENDING

## Non-goals

- Automating acceptance decisions for journals or conferences
- Treating all useful work as academic work
- Requiring publication for every project
- Optimizing for paper count
- Suppressing speculative work that is honestly labeled

## References

- Issue: hummbl-dev/hummbl-papers#19
- Parent standard: hummbl-dev/hummbl-governance#225
- Related: hummbl-dev/hummbl-papers#20 (LLL Engineering)
