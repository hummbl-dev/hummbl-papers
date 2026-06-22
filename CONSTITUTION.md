# CONSTITUTION.md — hummbl-papers

**Status:** v0.1
**Steward:** HUMMBL Research Institute
**Approving human:** Reuben Bowlby
**Standard:** HUMMBL Repo Standard v0.1
**Source of record:** git

## 1. Identity

`hummbl-dev/hummbl-papers` — HUMMBL Research — governance infrastructure papers and reproducibility artifacts

- **Class:** library
- **Visibility:** public
- **Standard:** HUMMBL Repo Standard v0.1

## 2. Scope

This constitution operates under the HUMMBL Repo Standard (`hummbl-dev/hummbl-governance/docs/standards/HUMMBL_REPO_STANDARD.md`). This constitution may be stricter, never weaker.

## 3. Protected invariants

1. **Receipt integrity.** The Krineia chain is append-only and SHA-256-chained. No operator may rewrite history except via documented cut.
2. **No secrets in code.** No API keys, tokens, or credentials may be committed to tracked files.
3. **Standard compliance.** This repo adheres to the HUMMBL Repo Standard v0.1 as declared in hummbl.repo.yaml.
4. **Test gate.** CI must be green before any merge to a protected branch.

## 4. Normative files

- `CONSTITUTION.md`
- `KRINEIA.md`
- `hummbl.repo.yaml`
- `CODEOWNERS`
- `AGENTS.md`

## 5. Authority

- **Steward:** HUMMBL Research Institute
- **Approving human:** Reuben Bowlby

## 6. Receipt-triggering changes

- Any edit to `CONSTITUTION.md`, `KRINEIA.md`, `hummbl.repo.yaml`, or `CODEOWNERS`
- Any change to a protected invariant
- Any release or version bump

## 7. Amendment

Changes require: a PR, an ADR, a KRINEIA receipt, and human approval (Reuben Bowlby).
