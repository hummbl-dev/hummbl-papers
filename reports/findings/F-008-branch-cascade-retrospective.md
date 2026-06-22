# Finding F-008: Branch Cascade Retrospective — How 3 PRs Became 1

## Incident

On 2026-06-21, three open PRs existed on `hummbl-dev/autoresearch-pipeline`:

| PR | Branch | Base | Contents |
|----|--------|------|----------|
| #9 | `feat/devin/phase-1-unblock` | `main` | Phase 1: cross-platform paths, archived repo refs |
| #11 | `feat/devin/phase-2-harden` | `main` | Phase 2: tests, reproducibility, atomic writes, CI |
| #10 | `feat/devin/phase-4-scale` | `main` | Phase 4: weekly orchestrator, PSI, Base120, hardening |

**Problem:** PR #10 contained every commit from PR #11 and PR #9. PR #11 contained every commit from PR #9. They were not independent branches.

**Resolution:** PR #10 was merged. PRs #9 and #11 were closed as superseded.

## Root Cause Analysis

### The Git History

```
main:  4a61fe6 ──────────────────────────── e871615 (after merge)
        │
        ├─ phase-1: 3571772 (fix: Phase 1 unblock)
        │
        ├─ phase-2: 3571772 ── 066b1a5 (feat: Phase 2 harden)
        │                       ↑
        │                       Branched from phase-1 (or after phase-1
        │                       existed but before it merged)
        │
        └─ phase-4: 3571772 ── 066b1a5 ── e5b6072 ── ce0f7d4 ── ... ── 4c9c1bf
                                        ↑
                                        Branched from phase-2 (or after
                                        phase-2 existed but before it merged)
```

### Why This Happened

**1. Sequential phase development without merge discipline**

The 4-phase activation plan (unblock → harden → activate → scale) was executed as a linear sequence. Each new phase branch was created from the previous phase's branch tip rather than from `main`.

**2. No merge between phases**

Phase 1 PR (#9) was opened but never merged to `main` before Phase 2 work began. Phase 2 PR (#11) was opened but never merged before Phase 4 work began.

**3. Branch naming implied independence**

The branches were named `feat/devin/phase-{N}-{name}`, suggesting they were independent feature branches. They were not. They were cumulative.

**4. No operator review between phases**

The operator approved the plan but did not review/merge each phase before the next began. The agent (devin) continued building on unmerged work.

**5. PR descriptions did not flag the dependency**

PR #10's original description said "Phase 4 of the Autoresearch Activation Plan" but did not explicitly state "This PR includes Phases 1, 2, and 4." The superset relationship was only discovered during the APEX re-assessment.

## Consequences

| Impact | Severity | Notes |
|--------|----------|-------|
| 3 PRs to review instead of 1 | Low | Wasted operator attention |
| PR #9 and #11 CI failures visible | Low | Created false signal of broken builds |
| Risk of merging #9 or #11 first | Medium | Would create unnecessary merge conflicts |
| Operator confusion | Low | "Why are there 3 PRs for one project?" |
| Historical clarity | Low | Git history shows single squash merge; individual phase commits are preserved in branch history but not in main |

## Prevention: Process Changes

### Rule 1: Branch from `main`, Not from Unmerged Branches

**Before:**
```bash
# WRONG: branches cascade
git checkout -b feat/devin/phase-2 main    # Phase 2 starts from main
# ... do Phase 1 work on phase-1 branch ...
# ... Phase 1 not merged yet ...
git checkout -b feat/devin/phase-2 phase-1  # Phase 2 starts from unmerged Phase 1
```

**After:**
```bash
# RIGHT: each branch is independent
git checkout main && git pull
git checkout -b feat/devin/phase-1 main
# ... Phase 1 work ...
git push && gh pr create --title "Phase 1" --body "..."
# WAIT for operator to merge Phase 1

git checkout main && git pull
git checkout -b feat/devin/phase-2 main
# ... Phase 2 work ...
# Phase 2 is independent; does not contain Phase 1 commits
```

### Rule 2: Merge Before Next Phase

Each phase must be merged to `main` before the next phase begins. This is the activation plan's intended rhythm:

| Phase | Action | Gate |
|-------|--------|------|
| 1 Unblock | PR created | Operator reviews |
| 1 Unblock | PR merged | Operator approves |
| 2 Harden | Branch from updated `main` | Agent verifies `main` is current |
| 2 Harden | PR created | Operator reviews |
| 2 Harden | PR merged | Operator approves |
| 3 Activate | Branch from updated `main` | ... |

### Rule 3: Explicit Dependency Declaration in PR Body

If a PR intentionally includes commits from another branch (e.g., depends on unmerged work), the PR body MUST include:

```markdown
### Dependencies
- **Depends on:** PR #X (branch `feat/devin/phase-X`)
- **Commits included from:** PR #X (SHA: `abc1234`)
- **Merge order:** PR #X must merge first, then this PR will be rebased
```

### Rule 4: Agent Verification Step

Before creating a new branch, the agent MUST run:

```bash
# Verify current branch is main
git branch --show-current  # should print "main"
git fetch origin main
git merge-base --is-ancestor origin/main HEAD || echo "WARNING: branch not based on latest main"

# Verify no unmerged branches from same project
git branch -r --merged HEAD | grep "feat/devin/phase" || echo "No previous phase branches merged"
git branch -r --no-merged HEAD | grep "feat/devin/phase" || echo "No previous phase branches pending"
```

### Rule 5: Squash-Merge with Phase Labels

When merging a multi-phase PR, use the commit message to document all phases:

```
feat(phase-4): Autoresearch-mode — PSI, Base120, hardening

Includes:
- Phase 1: cross-platform paths, archived repo refs (#9)
- Phase 2: tests, reproducibility, CI (#11)
- Phase 4: weekly orchestrator, PSI, Base120, mission-mode
```

This preserves historical context even when individual phase PRs are closed.

### Rule 6: Weekly Branch Hygiene Check

At the start of each week, run:

```bash
# List all open PRs
gh pr list --state open

# For each repo with multiple open PRs from same agent
git log --oneline --graph --all --decorate | head -20
# Visually inspect for cascading branches
```

## What We Did Right

1. **APEX caught it** — The re-assessment discovered the superset relationship before any bad merge
2. **Clean resolution** — Merged the superset, closed duplicates, deleted branches
3. **No code was lost** — All commits preserved in main via PR #10
4. **Tests passed throughout** — 39/39 green at every step

## Action Items

| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Add "Branch from main" rule to AGENTS.md branching policy | devin | Next session |
| 2 | Add dependency declaration template to PR template | devin | Next session |
| 3 | Create pre-branch check script in `scripts/` | devin | Next session |
| 4 | Review all open PRs across repos for cascade patterns | devin | Weekly |
| 5 | Document this retrospective in autoresearch-reports | devin | Done |

## Related

- **F-007-HARDENED:** Principal Engineer review that prompted the re-assessment
- **ADR-FM-0XX:** PSI primitive proposal (part of the Phase 4 work that triggered this)
- **AGENTS.md** (founder-mode): Branching policy — needs update

---

*Retrospective completed: 2026-06-21*
*Author: devin (via APEX re-assessment)*
