# Peptide Science Field Atlas v0.1 — Append-Only Long-Form Synthesis

**Status: CANDIDATE PAPER — APPEND-ONLY RELATIVE TO BASELINE — NON-CANONICAL**

Issue: hummbl-dev/hummbl-papers#17
Parent coordination: hummbl-dev/hummbl-dev#145
Source packet: hummbl-dev/research-source-packets#11
Bibliography: hummbl-dev/hummbl-bibliography#77

## Objective

Produce a rigorous long-form peptide-science field atlas that preserves the original broad survey and appends corrections, precision notes, deeper history, disciplinary expansion, evidence posture, open questions, and infrastructure implications.

This should become the human-readable synthesis layer above the source packet and bibliography. It must not become a substitute for the underlying claim/evidence ledger.

## Preservation requirement

The original baseline is known by the local artifact receipt as:

- `BASELINE_peptide_science_v0.1.md`
- SHA-256 `3d585b87dafb02bc9d5122800251aefa65cb14fabccbad54b13935573a2eab8b`

The paper must either preserve that baseline byte-for-byte or explicitly document why exact preservation was impossible and provide a complete diff. No silent rewrites.

## Required structure

### Part I — preserved baseline

Retain the original survey as an immutable historical layer.

### Part II — annotations and expansion

Use visible annotation classes:

- `[PRECISION]` — correction or sharpening of a baseline claim
- `[EXPANSION]` — new disciplinary or historical depth
- `[EVIDENCE]` — source posture and locator
- `[INFRA]` — infrastructure, database, or registry implication
- `[CANDIDATE]` — candidate interpretation, not settled
- `[OPEN]` — open question

### Part III — evidence posture

- Source-posture labels per claim
- Exact locators (DOI, PMID, accession, URL)
- Gaps, contradictions, unresolved provenance

### Part IV — open questions and infrastructure

- Open research questions
- Infrastructure implications for HUMMBL/BaseN
- Non-goals (no clinical recommendations, no canon)

## Acceptance criteria

- [x] Preservation requirement documented
- [x] Required structure documented (4 parts)
- [x] 6 annotation classes documented
- [ ] Baseline preserved byte-for-byte or diffed
- [ ] Baseline checksum independently reproduced
- [ ] Every material claim has at least one source and locator
- [ ] More than half of load-bearing historical claims use primary sources
- [ ] Frame-dependent "first" claims include inclusion criteria
- [ ] No copyrighted source text beyond permitted quotation
- [ ] Independent reviewer checks provenance precision
- [ ] PR links to issue and parent #145

## Non-goals

- Replacing the claim/evidence ledger
- Declaring scientific completeness
- Recommending clinical or personal peptide use
- Introducing new HUMMBL/BaseN canon
- Silent rewrites of the baseline

## Cross-repo dependencies

- `hummbl-dev/hummbl-dev#145` — peptide science infrastructure (parent)
- `hummbl-dev/research-source-packets#11` — source packet
- `hummbl-dev/hummbl-bibliography#77` — bibliography

## Fact posture

This is a candidate paper derived from issue #17. No claims about existing paper content. All structure and annotations are candidate until the baseline is preserved and validated.

## Receipt

- **Issue**: hummbl-dev/hummbl-papers#17
- **Parts**: 4
- **Annotation classes**: 6
- **Cross-repo deps**: 3
- **Review status**: PENDING
