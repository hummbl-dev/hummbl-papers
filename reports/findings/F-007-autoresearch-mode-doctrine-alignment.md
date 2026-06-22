# Finding F-007: Autoresearch-Mode Doctrine — Alignment with *-Mode, Mission-Mode, and the PSI Stack

## Source
- **Brainstorm continuation:** 2026-06-21
- **Alignment target:** `*-Mode General Doctrine` (MODE_GENERAL_DOCTRINE.md), `mission_mode.py`, Base120 cognitive governance
- **Confidence:** Architectural reasoning (doctrine-level, not empirically validated)

## Executive Summary

The autoresearch pipeline is not just a research tool. It is a **mode-bound execution system** that fits naturally into HUMMBL's `*-mode` architecture. Each weekly research batch is a `mission-mode` instance. The pipeline itself should be governed by an `autoresearch-mode` doctrine. And the cognitive stack (`WM.md`, `MM.md`, `Base120`) is the **PSI layer** — the Psychological Safety Infrastructure that prevents the research agent from harming itself, the operator, or the fleet.

This finding maps the four-phase activation plan (unblock → harden → activate → scale) to the `*-mode` anatomy, showing that HUMMBL has already built an `autoresearch-mode` without naming it.

---

## 1. The *-Mode Architecture Recap

Per `MODE_GENERAL_DOCTRINE.md` (approved 2026-06-20):

> **A `*-mode` is a governed Mission-Mode instance that binds purpose, identity, boundaries, authority, tools, rituals, memory, and receipts to a named context.**

The canonical formula:

```txt
*-Mode =
  Named Scope
  + Governing Doctrine
  + Protected Variable
  + Authorized Behaviors
  + Prohibited Behaviors
  + Activation Semantics
  + Receipt Pattern
  + Exit Criteria
```

A mode changes operating state across **seven layers**:
1. **Attention** — what to notice
2. **Authority** — who has decision rights
3. **Behavior** — what actions are appropriate
4. **Boundary** — what must not happen
5. **Memory** — what the mode remembers
6. **Receipt** — what evidence it leaves behind
7. **Exit** — how it ends

---

## 2. The Autoresearch Pipeline as an Unnamed Mode

The four-phase activation plan (unblock → harden → activate → scale) already implements a mode. We just haven't named it or written its doctrine.

| Mode Layer | What a Mode Needs | What the Pipeline Already Has |
|-----------|-------------------|-------------------------------|
| **Named Scope** | `autoresearch-mode` | `autoresearch-pipeline` repo, `autoresearch-reports` depot |
| **Governing Doctrine** | A document saying *how* research happens | Phase 0 baseline + operator runbook (implicit) |
| **Protected Variable** | What must be preserved | Governance primitives (kill switch, circuit breaker, cost ceiling) |
| **Authorized Behaviors** | What the agent can do | Edit `train.py`, run experiments, post to bus, commit findings |
| **Prohibited Behaviors** | What the agent must not do | No secrets in code, no direct pushes to `main`, no agent-to-agent message sending |
| **Activation Semantics** | How the mode starts | `weekly_run.py --pipeline-dir . --repo-dir ~/repo` |
| **Receipt Pattern** | What evidence it leaves | Bus posts (STATUS, MILESTONE, BLOCKED), git commits, `findings/*.md` |
| **Exit Criteria** | How it ends gracefully | All experiments completed or cost/time ceiling reached |

**The gap:** There is no `AUTORESEARCH_MODE_DOCTRINE.md`. The pipeline operates under the *general* `founder-mode` and `mission-mode` rules, but it doesn't have its own mode-level governance.

---

## 3. Each Weekly Run Is a Mission-Mode Instance

Per `mission_mode.py` (v0.2, 2026-06-19), a mission has:
- **MissionPacket** — declarative metadata
- **MissionState** — DECLARED → ACTIVE → COMPLETED | FAILED | ABORTED
- **MissionCloseout** — structured receipt
- **Bus filtering** — only allowed types during active mission

### Mapping: Weekly Autoresearch Run → Mission

| Mission-Mode Concept | Autoresearch Equivalent |
|---------------------|------------------------|
| `MissionPacket.declare()` | `weekly_run.py` startup — selects topic, reads queue |
| `MissionState.ACTIVE` | Experiments running (supervisor + worker loops) |
| `MissionState.PAUSED` | Healthcheck fails, circuit breaker trips |
| `MissionState.ABORTING` | Kill switch engaged or cost ceiling hit |
| `MissionState.COMPLETED` | All experiments done, queue updated, findings written |
| `MissionCloseout` | Bus RECEIPT + `autoresearch-reports` commit |
| Bus type filter | Only STATUS, MILESTONE, BLOCKED during run; QUESTION → QUEUED |

### What Should Change

The `weekly_run.py` script should:
1. **Declare a MissionPacket** at startup with:
   ```python
   MissionPacket.create(
       agent_id="devin",
       mission_statement=f"Weekly autoresearch: {topic_id} ({topic_domain})",
       mission_type=MissionType.RESEARCH,
       expected_duration_minutes=DEFAULT_EXPERIMENT_DURATION_MINUTES * max_experiments,
       risk_level=RiskLevel.P2,  # medium risk: runs code, costs money
   )
   ```
2. **Check `MissionRegistry`** before starting — abort if another research mission is active
3. **Post `WIP_START`** to bus (required per `mission_mode_bus_filter.py`)
4. **Post `WIP_END`** at closeout (required)
5. **Generate `MissionCloseout`** with:
   - Experiments completed
   - `val_bpb` trend
   - Findings produced
   - Queue status updated
   - Lessons learned
   - Operator action items

---

## 4. The PSI Layer — Psychological Safety Infrastructure

**PSI** = the three-layer cognitive governance stack that prevents the research agent from causing harm (to itself, the operator, the fleet, or the budget).

### PSI Layer 1: WM.md — World Model (External Safety)

**Function:** The agent knows what the world looks like so it doesn't make dangerous assumptions.

**Safety role:**
- Hardware constraints prevent OOM (e.g., "depth > 8 causes OOM on nodezero")
- Dataset characteristics prevent overfitting (e.g., "tinystories has low entropy — small models work")
- Research landscape prevents delusion (e.g., "Karpathy's baseline is 0.9979 on climbmix — our 2.5 on tinystories is not comparable")
- Cross-platform reality prevents false comparisons (e.g., "Anvil CUDA is ~3x faster than nodezero MPS")

**Without WM.md:** The agent might try to replicate Karpathy's results on tinystories with an M4, fail, and conclude the pipeline is broken — when in fact the comparison was never valid.

### PSI Layer 2: MM.md — Mental Model (Internal Safety)

**Function:** The agent knows its own biases and limitations so it doesn't deceive itself.

**Safety role:**
- Cognitive bias flags prevent repetitive failure (e.g., "batch_size fixation detected — cooldown enforced")
- Strategy registry with success rates prevents overconfidence (e.g., "architecture changes: 10% success rate")
- Base120 blind spot tracking prevents reasoning gaps (e.g., "never applied IN16 — forcing one per week")
- Self-improvement goals prevent stagnation (e.g., "increase simplification rate to 20%")

**Without MM.md:** The agent keeps making the same mistakes because it has no memory of its own failures — only the `results.tsv` log, which doesn't capture *why* things failed.

### PSI Layer 3: Base120 — Canonical Reasoning (Governance Safety)

**Function:** The agent has a governed set of reasoning operators so it doesn't reason arbitrarily.

**Safety role:**
- **IN7 Premortem** — "What could go wrong?" applied before every architecture change
- **DE5 Root Cause Analysis** — "Why did this fail?" applied before retrying
- **SY14 Leverage Points** — "Is this the highest-impact change?" prevents local optimization
- **CO11 Pattern-Tile** — "What reusable pattern exists?" prevents reinventing
- **RE13 Velocity-Tune** — "Are we getting faster or slower?" detects pipeline degradation

**Without Base120:** The agent uses whatever reasoning pattern the LLM happens to generate, with no audit trail of *which* mental model was applied. This is the OWASP ASI08 "Cascading Cognitive Failure" vector.

### PSI as a Safety Primitive

PSI is the **cognitive complement** to the existing physical safety primitives:

| Primitive Layer | What It Protects | Example |
|---------------|-----------------|---------|
| **Kill switch** | Compute resources | `HALT_ALL` stops all experiments |
| **Circuit breaker** | External services | Open after 3 failures to `nvidia-smi` |
| **Cost governor** | Budget | Halt when API spend > ceiling |
| **Delegation token** | Authority scope | Worker can run experiments but not merge PRs |
| **PSI (NEW)** | Reasoning quality | WM + MM + Base120 prevent cognitive failures |

**PSI is the missing 8th primitive.** The current 7 primitives protect *actions*. PSI protects *thinking*.

---

## 5. *-Mode Anatomy for Autoresearch-Mode

Using the canonical mode skeleton from `MODE_GENERAL_DOCTRINE.md`:

### 5.1 Attention

**What to notice:**
- `val_bpb` trend (improving, flat, or degrading)
- Hardware health (GPU temp, OOM events, disk space)
- Queue freshness (pending topics, stale completed items)
- External research signals (new papers, new forks of Karpathy's repo)
- Cognitive bias triggers (repetitive parameter changes, neglect of IN domain)

### 5.2 Authority

**Decision rights:**
- **Agent** can: propose experiments, run them, log results, draft findings
- **Agent** cannot: merge findings to `main` without operator review; exceed cost ceiling; run experiments on operator-owned machines without approval
- **Operator** must: approve the weekly topic selection; review proposals before they become action items
- **Kill switch** overrides both: emergency halt requires no approval

### 5.3 Behavior

**Authorized:**
1. Select pending topic from queue (prioritized by tier + last_run)
2. Run healthcheck before experiment generation
3. Generate experiment via supervisor
4. Execute via worker
5. Evaluate significance (MAD scoring)
6. Log results to `results.tsv`
7. Draft findings if results are actionable
8. Update queue status
9. Post receipts to coordination bus
10. Commit artifacts to `autoresearch-reports`

**Prohibited:**
1. Never commit directly to `main` of any repo
2. Never send messages on behalf of the operator
3. Never run experiments on Anvil without `--device cuda` override
4. Never modify `prepare.py` (ground truth must be preserved)
5. Never exceed `MAX_EXPERIMENT_DURATION_MINUTES` without operator approval
6. Never ignore a `HALT_ALL` kill switch signal
7. Never propose an experiment that repeats a failed hypothesis (check ASI store first)

### 5.4 Boundary

**Hard boundaries (non-negotiable):**
- Cost ceiling: $X/month for cloud compute; Anvil/nodezero are "free" (owned)
- Time ceiling: Max 4 hours per weekly batch (operator availability)
- Safety ceiling: Any `HALT_NONCRITICAL` or `HALT_ALL` signal stops the mission immediately
- Data ceiling: Never upload proprietary data to external services

**Soft boundaries (advisory):**
- Simplicity preference: favor deletions over additions
- Cross-platform fairness: don't compare MPS and CUDA results directly
- Human-in-the-loop: findings become proposals only after operator review

### 5.5 Memory

**What the mode remembers:**
- `WM.md` — the evolving world model
- `MM.md` — the evolving self-model
- `results.tsv` — raw experiment outcomes
- `findings/*.md` — distilled knowledge
- `proposals/*.md` — proposed actions
- `asi_store.jsonl` — failed hypotheses and their lessons
- `factor_model.json` — Bayesian beliefs about parameter effects
- `lessons_learned.md` — weekly self-evolution output
- CLP ledger entries — reasoning traces for audit

### 5.6 Receipt

**Evidence the mode leaves behind:**
1. **Bus posts:** `WIP_START`, `WIP_END`, `STATUS`, `MILESTONE`, `BLOCKED`
2. **Git commits:** On `feat/devin/*` branches, never `main`
3. **MissionCloseout:** Structured closeout with all metrics
4. **Findings:** Markdown documents with evidence and confidence scores
5. **Proposals:** Markdown documents with implementation plans
6. **CHANGELOG.md:** Versioned record of pipeline changes

### 5.7 Exit Criteria

**Graceful exit:**
- All experiments completed successfully
- Queue updated with new status
- Findings and proposals drafted
- MissionCloseout posted
- `WIP_END` on bus

**Abort exit:**
- Kill switch engaged (DISENGAGED → HALT_NONCRITICAL → HALT_ALL)
- Cost ceiling exceeded
- Hardware failure (GPU OOM, disk full, SSH disconnect)
- Operator sends "abort" signal
- Healthcheck fails 3 consecutive times

**Failure exit:**
- Supervisor crashes and cannot recover
- Worker produces NaN/Inf for 5 consecutive experiments
- Factor model becomes unrecoverable (all parameters have zero variance)

---

## 6. Alignment with Existing HUMMBL Infrastructure

### 6.1 Mission Mode Service (`mission_mode.py`)

The existing mission mode infrastructure should be used for every weekly run:

```python
# In scripts/weekly_run.py, at startup:
from founder_mode.services.mission_mode import MissionPacket, MissionType, RiskLevel

packet = MissionPacket.create(
    agent_id="devin",
    mission_statement=f"Autoresearch weekly batch: {topic_id}",
    mission_type=MissionType.RESEARCH,  # NEW enum value
    expected_duration_minutes=args.max_experiments * args.experiment_duration_minutes,
    risk_level=RiskLevel.P2,
)

# Register with MissionRegistry
registry = MissionRegistry()
registry.declare(packet)

# During execution, check if mission should continue
if registry.active_mission().should_abort():
    log.info("Mission abort signal received, exiting gracefully")
    return 0
```

### 6.2 Bus Filter (`mission_mode_bus_filter.py`)

The existing bus filter restricts message types during missions. Autoresearch missions should:
- **Require:** `WIP_START`, `WIP_END`
- **Allow:** `STATUS`, `MILESTONE`, `BLOCKED`
- **Queue:** `QUESTION`, `PROPOSAL` (deferred to post-mission)
- **Suspend:** `DECISION` (only operator makes decisions during research)

### 6.3 Kill Switch (`kill_switch_core.py`)

The existing kill switch should be wired into the pipeline:
- `HALT_NONCRITICAL`: Finish current experiment, then stop (don't start new ones)
- `HALT_ALL`: Immediately terminate worker process
- `EMERGENCY`: `SIGKILL` the worker, leave supervisor state inconsistent (operator intervention required)

### 6.4 Cost Governor (`cost_tracker.py`)

The existing cost tracker should monitor:
- Cloud API calls (OpenAI, Anthropic, etc.) for proposal drafting
- Local compute time (nodezero M4, Anvil RTX — amortized cost)
- Storage costs (`runs/` directory growth)

### 6.5 CLP / Open Brain (`cognition/`)

The existing cognitive ledger should receive:
- Every experiment start/end as a ledger entry
- Every Base120 model application as a ledger entry
- Every WM.md and MM.md update as a ledger entry
- Queryable via `POST /base120/recommend` for experiment selection

---

## 7. Competitive Implications

### The Autoresearch-Mode Doctrine as Moat

No other system in the ecosystem has:
1. **Mode-level governance** — They have prompts, not constitutions
2. **Mission-mode runtime** — They have scripts, not declarative mission packets
3. **PSI cognitive safety** — They have flat logs, not structured world/self models
4. **Canonical reasoning operators** — They have implicit reasoning, not governed Base120 models

When we publish `AUTORESEARCH_MODE_DOCTRINE.md`, we are not just documenting our pipeline. We are **defining the standard** for how autonomous research agents should be governed.

### The `RESEARCH` MissionType as Category Leader

`mission_mode.py` currently has mission types like `BUILD`, `OPS`, `REVIEW`. Adding `RESEARCH` as a first-class mission type signals that HUMMBL treats research as a governed operational activity, not a toy.

This makes HUMMBL the **only platform** where:
- Research missions are declared, tracked, and closed out like production deploys
- Research agents have cognitive safety infrastructure
- Research outputs (findings, proposals) flow through the same governance pipeline as code changes

---

## 8. Recommendations

### Immediate (this week)

1. **Create `AUTORESEARCH_MODE_DOCTRINE.md`** in `autoresearch-pipeline/docs/` using the mode anatomy above.

2. **Add `MissionType.RESEARCH`** to `founder_mode/services/mission_mode.py`.

3. **Wire `weekly_run.py` to Mission Mode** — declare a MissionPacket at startup, post `WIP_START`/`WIP_END`, generate MissionCloseout.

4. **Add PSI as the 8th primitive** — Document it in `PRIMITIVES.md` as "Cognitive Safety Primitive: WM + MM + Base120."

### Short-term (next 4 weeks)

5. **Create the `autoresearch-mode` skill** in `.claude/skills/autoresearch-mode/` with:
   - `SKILL.md` — trigger: "start autoresearch weekly batch"
   - `MODE_DOCTRINE.md` — the full mode constitution
   - `ACTIVATION.md` — how to enter the mode
   - `RECEIPT.md` — what evidence to leave

6. **Integrate with `mission_mode_bus_filter.py`** — add `RESEARCH` mission type to the filter's allowed types.

7. **Publish the doctrine** — blog post: "Why Autoresearch Needs a Mode, Not Just a Script."

### Medium-term (next quarter)

8. **Propose `RESEARCH` as a standard mission type** across all HUMMBL agent fleets. If `devin` can run research missions, so can `codex`, `apex`, `gemini` — each with their own mode instance but shared PSI layer.

9. **Cross-project PSI federation** — `WM.md` and `MM.md` from the autoresearch pipeline should be queryable by other agents via Open Brain. The founder-mode agent should be able to ask: "What has autoresearch learned about batch_size?"

---

## Appendix: Proposed `AUTORESEARCH_MODE_DOCTRINE.md` Skeleton

```markdown
# Autoresearch-Mode Doctrine

## Status
DRAFT — pending operator ratification

## Canonical Definition
> Autoresearch-Mode is a governed Mission-Mode instance for autonomous
> ML experiment design, execution, and knowledge distillation.

## One-Line Purpose
Run structured, governed, receipt-producing research experiments on a weekly cadence.

## Core Formula
```txt
Autoresearch-Mode =
  Scope: autoresearch-pipeline + autoresearch-reports
  + Doctrine: simplicity-first, evidence-governed, cost-bounded
  + Protected Variable: val_bpb trend + operator trust
  + Authorized: generate, execute, log, distill, propose
  + Prohibited: merge-to-main, exceed-ceiling, ignore-kill-switch
  + Activation: weekly_run.py --pipeline-dir . --repo-dir ~/repo
  + Receipt: bus posts + git commits + MissionCloseout
  + Exit: completed | abort (kill-switch) | failure (crash)
```

## PSI Stack
- **WM.md** — World model (external safety)
- **MM.md** — Mental model (internal safety)
- **Base120** — Canonical reasoning (governance safety)

## Alignment
- Parent mode: `founder-mode`
- Mission type: `RESEARCH`
- Bus identity: `devin`
- Kill switch: respects all 4 modes
- Cost ceiling: integrated with `cost_tracker.py`
```

---

*Brainstorm continuation completed: 2026-06-21*
*Classification: ARCHITECTURAL DESIGN — *-mode doctrine alignment for autonomous research*
*Status: APPROVED by operator for further development*
