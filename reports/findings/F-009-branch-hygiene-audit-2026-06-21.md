# Finding F-009: Branch Hygiene Audit — 2026-06-21

## Trigger

Operator opened PR #984 (`feat/devin/doctrine-ontology-constellation`) in `founder-mode`. Post-F-008 retrospective mandated a proactive branch audit across all repos.

## Repos Audited

| Repo | Remote Branches | Local Branches | Cascade Risk | Action Required |
|------|-----------------|----------------|--------------|-----------------|
| `autoresearch-pipeline` | 2 | 0 | None | **Cleanup** |
| `autoresearch-reports` | 3 | 1 | Low | **Review** |
| `founder-mode` (origin) | 51 | N/A | Medium | **Major cleanup** |
| `founder-mode` (gitea) | 100+ | N/A | Low | **Major cleanup** |

---

## 1. autoresearch-pipeline

### Status: MERGED, needs branch deletion

| Branch | Status | Action |
|--------|--------|--------|
| `origin/feat/devin/phase-4-scale` | **Merged to main** (PR #10) | **Delete remote** |
| `origin/ci/codex/autoresearch-pipeline-syntax` | Unknown — codex CI branch | Review with codex |

**No cascade risk.** PR #10 was the only active branch and is now on `main`.

---

## 2. autoresearch-reports

### Status: Active work, no cascade

| Branch | Commits vs main | Status | Action |
|--------|-----------------|--------|--------|
| `feat/devin/phase-3-activate` | 9 | **Active** — current work (F-004 through F-008) | Keep |
| `origin/feat/devin/slm-reconciliation-note-2026-06-19` | 1 | Draft/note branch | Ask devin if still needed |
| `origin/feat/codex/repo-health-autoresearch-reports` | Unknown | Codex work | Ask codex |

**No cascade risk.** `phase-3-activate` is independent of `main`.

---

## 3. founder-mode (origin) — PR #984 Analysis

### PR #984: `feat/devin/doctrine-ontology-constellation`

| Field | Value |
|-------|-------|
| Files changed | 23 |
| Lines | +6340 / -1 |
| Commits vs main | 26 |
| Based on | `main` (not a cascade) |
| Contains all of main? | Yes |
| Conflicting branches by same agent? | None found |
| **Verdict** | ✅ **Legitimate large feature branch** — NOT a cascade |

### Stale Branches (>14 days old)

| Branch | Last Commit | Status | Recommendation |
|--------|-------------|--------|----------------|
| `origin/fix/lexicon-ci-runner` | 2026-06-06 | Stale (15d) | Delete or revive |
| `origin/feat/apex/governance-topology-canon-v1` | 2026-06-06 | **MERGED** | **Delete** |
| `origin/feat/devin/1780435738-mtsmu-package-sprint-w1` | 2026-06-06 | Stale (15d) | Ask devin |
| `origin/docs/codex/mcp-fleet-intel` | 2026-06-02 | Stale (19d) | Ask codex |
| `origin/feat/opencode/payment-primitives` | 2026-05-31 | Stale (21d) | Ask opencode |
| `origin/chore/codex/new-ops-artifacts-2026-05-28` | 2026-05-29 | **MERGED** | **Delete** |
| `origin/feat/codex/billing-system-implementation` | 2026-05-29 | **MERGED** | **Delete** |
| `origin/docs/codex/phase-governance` | 2026-05-28 | **MERGED** | **Delete** |
| `origin/feat/codex/local-model-security-hardening` | 2026-05-28 | **MERGED** | **Delete** |
| `origin/feat/codex/skills-fleet-expansion` | 2026-05-28 | **MERGED** | **Delete** |
| `origin/docs/codex/rate-limit-diagnostic-monitor` | 2026-05-28 | **MERGED** | **Delete** |
| `origin/fix/codex/lex-016-remediate` | 2026-05-28 | **MERGED** | **Delete** |
| `origin/feat/codex/wargame-harness-adoption` | 2026-05-26 | Stale (26d) | Ask codex |
| `origin/feat/codex/promotion-replay-verifier` | 2026-05-26 | Stale (26d) | Ask codex |
| `origin/park/codex/founder-mode-dirt-20260526` | 2026-05-26 | Explicitly parked | Keep or delete |
| `origin/feat/gemini/verderer-brand-refresh` | 2026-05-25 | Stale (27d) | Ask gemini |
| `origin/feat/gemini/agy-promotion-gates` | 2026-05-24 | **MERGED** | **Delete** |
| `origin/docs/codex/memory-project-portfolio` | 2026-05-22 | Stale (30d) | Ask codex |
| `origin/fix/codex/python-ld-library-path` | 2026-05-20 | Stale (32d) | Ask codex |
| `origin/fix/codex/minimal-services-init-env` | 2026-05-20 | Stale (32d) | Ask codex |

### Already-Merged Branches (safe to delete)

The following origin branches are already ancestors of `main` but still exist:

```
chore/codex/new-ops-artifacts-2026-05-28
docs/codex/phase-governance
docs/codex/rate-limit-diagnostic-monitor
feat/apex/governance-topology-canon-v1
feat/codex/billing-system-implementation
feat/codex/local-model-security-hardening
feat/codex/secret-broker-policy-and-nodezero-bridge
feat/codex/skills-fleet-expansion
feat/gemini/agy-promotion-gates
fix/codex/lex-016-remediate
fix/devin/ci-founder-mode-paths-v2
```

**Total: 11 branches already merged.** Deleting them would reduce origin clutter by ~20%.

---

## 4. founder-mode (gitea) — Artifact Branches

### Split Branches (likely sync artifacts)

6 branches with `split-2026-06-05` suffix:

```
gitea/chore/codex/fleet-keepalive-loop-split-2026-06-05
gitea/ci/codex/docs-only-scan-skip-split-2026-06-05
gitea/docs/codex/ai-factory-simulation-governance-split-2026-06-05
gitea/docs/codex/mcp-fleet-intel-proposals-split-2026-06-05
gitea/feat/codex/ai-factory-simulation-runtime-split-2026-06-05
gitea/feat/codex/model-hash-verification-split-2026-06-05
```

These appear to be backup copies created during a sync operation on 2026-06-05. They are likely safe to delete if the original branches are still present.

### Review Branches

Many `gitea/review/pr-*` and `gitea/pr-*` branches exist. These are review artifacts that should be deleted after the reviewed PR is merged or closed.

### Stash-Park Branches

4 branches explicitly named as stash-parks:

```
gitea/stash-park/autoresearch-engine-fix
gitea/stash-park/ci-skip-windows-tests
gitea/stash-park/exception-docs-remediation
gitea/stash-park/timeline-fn-fix-tests
gitea/stash-park/timeline-fn-scheduler
```

These should be reviewed by their owners. If the work was merged elsewhere, delete. If not, consider reviving or documenting.

---

## Cascade Risk Assessment

| Repo | Cascade Found? | Evidence |
|------|---------------|----------|
| autoresearch-pipeline | ❌ No | PR #10 contained #9 and #11, but all are now merged. No open branches cascade. |
| autoresearch-reports | ❌ No | `phase-3-activate` (9 commits) and `slm-reconciliation` (1 commit) are independent. |
| founder-mode (origin) | ⚠️ Medium | Many branches by same agent (codex has ~15 open branches). Risk of codex starting a new branch from an unmerged codex branch. |
| founder-mode (gitea) | ⚠️ Low | Many branches but most are review artifacts or backups. |

**PR #984 is NOT a cascade.** It is a legitimate 26-commit feature branch from `main` with no commit overlap with other devin branches.

---

## Immediate Actions (No Operator Approval Needed)

| # | Action | Repo |
|---|--------|------|
| 1 | Delete `origin/feat/devin/phase-4-scale` | autoresearch-pipeline |
| 2 | Delete 11 already-merged origin branches | founder-mode |
| 3 | Delete 6 `split-2026-06-05` artifact branches | founder-mode (gitea) |

## Deferred Actions (Need Owner Approval)

| # | Action | Owner |
|---|--------|-------|
| 4 | Review `origin/ci/codex/autoresearch-pipeline-syntax` | codex |
| 5 | Review `origin/feat/codex/repo-health-autoresearch-reports` | codex |
| 6 | Review `origin/feat/devin/slm-reconciliation-note-2026-06-19` | devin |
| 7 | Review 15+ stale origin branches (>14d) | Various |
| 8 | Review `gitea/review/pr-*` branches | Various |
| 9 | Review `gitea/stash-park/*` branches | Various |

---

## Prevention (from F-008)

1. **Branch from `main`** — never from unmerged branches
2. **Merge before next phase** — each PR merged before next branch created
3. **Declare dependencies in PR body** — if a PR includes unmerged work
4. **Agent pre-branch check** — verify `main` is current, check for open PRs
5. **Weekly branch hygiene** — run `git branch -r` and inspect for staleness

---

*Audit completed: 2026-06-21*
*Auditor: devin*
*Scope: autoresearch-pipeline, autoresearch-reports, founder-mode (origin + gitea)*
