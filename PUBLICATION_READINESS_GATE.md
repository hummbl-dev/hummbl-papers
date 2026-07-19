# Universal Publication Readiness Gate — Draft v0.1

## Status

**CANDIDATE IMPLEMENTATION GATE — NO AUTOMATIC PUBLICATION AUTHORITY**

## Purpose

A reusable publication-readiness gate for all HUMMBL scholarly artifacts,
regardless of discipline or project. This gate generalizes the
project-specific publication-gate pattern. It does not replace
project-specific gates; it defines the minimum common gate they must
satisfy.

## Artifact classes

| Class | Description |
|-------|-------------|
| `EXPLORATORY_NOTE` | Early-stage exploration, not yet a research memo |
| `INTERNAL_RESEARCH_MEMO` | Internal research memorandum |
| `DATED_TECHNICAL_REPORT` | Dated technical report |
| `REPRODUCIBILITY_PACKET` | Reproducibility evidence packet |
| `PREPRINT_CANDIDATE` | Candidate for preprint submission |
| `VENUE_SUBMISSION_CANDIDATE` | Candidate for venue submission |
| `SUBMITTED_MANUSCRIPT` | Submitted manuscript |
| `PEER_REVIEWED_PUBLICATION` | Peer-reviewed publication |
| `CORRECTION` | Correction to a prior artifact |
| `SUPERSESSION` | Supersession of a prior artifact |
| `RETRACTION` | Retraction of a prior artifact |

A GitHub report, DOI deposit, arXiv preprint, conference submission, and
peer-reviewed article are different states and must not be conflated.

---

## Gate dimensions

### A. Contribution and novelty

- [ ] Exact research question stated
- [ ] Strongest prior art and nearest neighbors identified
- [ ] Narrow contribution claim stated
- [ ] Explicit non-novel components listed
- [ ] Independent novelty challenge performed
- [ ] Discipline-adjacent search performed (not keyword-only)

### B. Evidence and methods

- [ ] Claim-to-evidence map complete
- [ ] Methods sufficient for scrutiny
- [ ] Data/code/source lineage documented
- [ ] Exclusions, assumptions, and failure cases listed
- [ ] Negative/null results reported
- [ ] Uncertainty and limitations stated
- [ ] Calculation and figure verification complete

### C. Reproducibility

- [ ] Environment and dependency lock documented
- [ ] Exact artifact versions and commit SHAs recorded
- [ ] Commands and expected outputs documented
- [ ] Random seeds and nondeterminism disclosed
- [ ] Data availability documented or restrictions justified
- [ ] Independent reproduction attempt performed (where proportionate)
- [ ] Reproducibility vs replication vs conceptual illustration distinguished

### D. Authorship and AI disclosure

- [ ] Human authors and accountable corresponding contact identified
- [ ] Contribution record complete
- [ ] Conflicts and funding/incentive disclosure complete
- [ ] Material AI/model/tool assistance recorded
- [ ] Venue-specific authorship and AI policy verified at submission time
- [ ] No agent/model represented as human author or legitimacy source

### E. Ethics, privacy, rights, and licenses

- [ ] Human-subjects/participant determination made
- [ ] Sensitive-data determination made
- [ ] Consent and publication boundaries verified
- [ ] Dataset, code, image, quotation, and figure rights verified
- [ ] Dual-use or harm review performed (where relevant)
- [ ] Legal/regulatory caveat added (where relevant)

### F. Independent review

- [ ] Methods review performed
- [ ] Evidence and calculation review performed
- [ ] Novelty/prior-art review performed
- [ ] Reproducibility review performed
- [ ] Reputational-risk review performed
- [ ] Unresolved objection log maintained

The originating agent or author cannot be the sole reviewer.

### G. Public communication

- [ ] Title and abstract do not overstate maturity
- [ ] Public summary preserves limitations
- [ ] Preprint status is explicit
- [ ] No "peer reviewed" claim before actual peer review
- [ ] No marketing claim stronger than the artifact
- [ ] Correction contact and version history are visible

---

## Gate output

Every candidate receives exactly one disposition:

| Disposition | Description |
|-------------|-------------|
| `BLOCK` | Artifact is blocked from advancement |
| `RESEARCH_NOTE_ONLY` | Artifact may be a research note only |
| `INTERNAL_REPORT_READY` | Artifact is ready as an internal report |
| `TECHNICAL_REPORT_READY` | Artifact is ready as a technical report |
| `PREPRINT_READY` | Artifact is ready for preprint submission |
| `SUBMISSION_READY` | Artifact is ready for venue submission |
| `PUBLICATION_READY` | Artifact is ready for publication |
| `CORRECTION_REQUIRED` | Artifact requires correction |
| `SUPERSEDE` | Artifact should be superseded |
| `RETRACT` | Artifact should be retracted |

The gate must explain the evidence and unresolved risks supporting the
disposition.

---

## Anti-gaming requirements

The gate must reject:

| Anti-gaming rule | Description |
|-----------------|-------------|
| Polished prose with weak methods | Prose quality does not substitute for methods rigor |
| Citation volume as prior-art | Citation count does not substitute for prior-art analysis |
| Self-review as independence | Self-review is not independent review |
| Tests as scientific validation | Passing tests is not scientific validation |
| Internal benchmarks as generality | Internal benchmarks are not external generality |
| Synthetic examples as empirical | Synthetic examples are not empirical evidence |
| Benchmark selection after results | Selecting benchmarks after observing favorable results without disclosure |
| Hidden exclusions | Exclusions and failed runs must be disclosed |
| arXiv as peer review | arXiv posting is not peer review |
| DOI as quality validation | DOI assignment is not quality validation |
| Unverified agent citations | Agent-generated citations must be independently verified |

---

## Pilot applications

Apply the candidate gate retrospectively, without grandfathering, to at
least:

1. One existing HUMMBL technical report
2. One blocked publication issue
3. LLL Engineering as a preprint candidate
4. One project that should remain a research note rather than advance

The pilot should reveal false positives, unnecessary bureaucracy, and
missing controls before organization-wide adoption.

---

## Migration note

Existing project-specific publication gates (e.g., in `hummbl-papers`,
`hummbl-research`) should:

1. Continue to enforce their project-specific stricter requirements
2. Adopt this gate as the minimum common baseline
3. Map their existing dispositions to the gate dispositions
4. Document any project-specific extensions
5. Not grandfather existing artifacts — apply the gate retrospectively

---

## Non-goals

- Automating acceptance decisions for journals or conferences
- Treating all useful work as academic work
- Requiring publication for every project
- Optimizing for paper count
- Suppressing speculative work that is honestly labeled

## Unresolved questions

1. Should the gate schema be JSON Schema, YAML, or both?
2. What is the minimum required for a "proportionate" reproduction attempt?
3. How should multi-disciplinary artifacts be handled?
4. What is the timeline for organization-wide enforcement?

## Rollback instructions

This is a specification document. Rollback = revert the commit. No runtime
impact.

## Related

- `hummbl-dev/hummbl-papers#19` — this issue
- `hummbl-dev/hummbl-governance#225` — parent standard
