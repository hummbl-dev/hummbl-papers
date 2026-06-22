# NemoClaw Implementation Guide

**Version:** Based on NemoClaw v0.1.4 (v0.1.3 + amendment)
**Date:** 2026-03-23
**Sources:** RQ-005 (Multi-Agent Coordination), RQ-006 (Capability Security), RQ-007 (Test Strategy), RQ-003 (Incident Response), NemoClaw Spec v0.1.3 + v0.1.4 Amendment
**Purpose:** Implementation-ready guide for building the NemoClaw Supervisor-Worker pipeline

---

## 1. Architecture Recap

NemoClaw is the protocol governing autonomous ML experimentation across two machines:

- **Supervisor** (Ubuntu/Nodezero, M4 Pro 48GB) -- generates experiment specs, enqueues runs, reads results, makes strategic decisions
- **Worker** (Windows/Desktop, RTX 3080 Ti 12GB VRAM) -- claims runs, applies patches, executes training, evaluates acceptance, writes results

### Core Design Principles

| Principle | Implementation |
|-----------|---------------|
| File-based queue | No message broker, no database -- filesystem directories are the queue |
| READY/CANCEL sentinels | Atomic signaling without POSIX guarantees |
| Worker owns state.json | Supervisor signals via sentinel files only, never writes state directly |
| val_bpb sole acceptance metric | `val_bpb_after < baseline - min_delta` |
| 22 failure codes | ARNC-001 through ARNC-022 (v0.1.4 added ARNC-022) |
| Circuit breaker | 3 consecutive identical failures OR 3 consecutive NaN rejections stops the Worker |
| Scope-aware acceptance | `scope_tag` prevents cross-budget comparisons (300s vs 3600s) |
| Thermal threshold | `execution.gpu_temp_limit_c` default 85C |

### State Machine

```
queued --> dispatched --> running --> completed --> accepted  (terminal)
                                               --> rejected  (terminal)
                                  --> failed                  (terminal)
                                  --> canceled                (terminal)
                      --> failed                              (terminal)
                      --> canceled                            (terminal)
          --> canceled                                        (terminal)
```

Eight states. Four terminal: `accepted`, `rejected`, `failed`, `canceled`. One transient: `completed` (must immediately resolve to accepted/rejected).

### Filesystem Layout

```
autoresearch-pipeline/
  queue/{run_id}/          # Supervisor writes here
    experiment.json
    patch.diff
    state.json
    READY                  # Last file written -- Worker waits for this
    CANCEL                 # Optional -- Supervisor cancellation signal
  runs/{run_id}/           # Worker writes here after execution
    experiment.json
    patch.diff
    state.json
    result.json
    metrics.json
    artifacts.json
    logs/stdout.log
    logs/stderr.log
  supervisor/              # Supervisor module
  worker/                  # Worker module
  tests/                   # Test suite
  spec/                    # Spec documents and JSON schemas
```

---

## 2. Implementation Plan (Ordered Tasks)

### Phase 1: Core Data Models (Both Machines) -- Week 1

**Task 1.1: Pydantic models for all schemas**
- `ExperimentSpec` (from `experiment.schema.json`)
- `StateFile` (from `state.schema.json`)
- `ResultFile` (from `result.schema.json`)
- `MetricsFile` (from `metrics.schema.json`)
- `ArtifactsManifest` (from `artifacts.schema.json`)
- `LineageRecord` (from `lineage.schema.json`)
- These models are shared between Supervisor and Worker -- ship as a `nemoclaw.models` package

**Task 1.2: State machine implementation**
- Enum for all 8 states
- Transition validator enforcing the state graph from section 9.2
- `transition(current, target)` raises `InvalidTransition` for illegal moves
- Every transition writes `updated_at` timestamp

**Task 1.3: Run ID generation**
- `{ISO8601_UTC_truncated}_{sha256_first_8}` format
- Hash computed over minified, sorted-keys JSON of experiment spec with `run_id` field omitted
- Uniqueness check against existing `queue/` and `runs/` directories

### Phase 2: Worker Module (Windows/RTX 3080 Ti) -- Weeks 2-3

**Task 2.1: Queue scanner**
- Poll `queue/` directory at configurable interval (default 10s)
- Skip entries without READY sentinel
- Skip entries whose run_id already exists under `runs/`
- Skip entries with CANCEL sentinel (transition to canceled)

**Task 2.2: Claim protocol**
- Write `state.json` to `dispatched` with `worker_id`, `hostname`, `pid`
- Wait 2 seconds (filesystem sync delay)
- Re-read `state.json` and verify own `worker_id` still present
- For single-worker v0.1, the verify step is recommended but not blocking

**Task 2.3: Execution engine**
- Validate experiment spec against Pydantic model
- Resolve baseline val_bpb (scope-aware per v0.1.4 amendment)
- Git checkout `base_commit`, apply `patch.diff`, create candidate commit
- Set `env_overrides` (with blocklist enforcement)
- Set `gpu_power_limit_w` if specified (record original, restore after)
- Set `training_time_budget_s` via env var
- Execute `execution.command` with `timeout_seconds` enforcement
- Capture stdout/stderr to log files
- Heartbeat: update `state.json.updated_at` every 60 seconds during execution

**Task 2.4: Metrics extraction**
- Parse training script output for val_bpb
- Handle NaN/Infinity: set `val_bpb: null`, `val_bpb_nonfinite: true`
- Extract optional telemetry fields (gpu_temp, power, throughput, steps, tokens, vram, mfu, training_seconds)

**Task 2.5: Acceptance evaluation**
- `val_bpb_after < baseline - min_delta` => accepted
- Null val_bpb with `require_metric_present: true` => rejected
- NaN val_bpb => rejected (with `val_bpb_nonfinite: true`)

**Task 2.6: Artifact collection and cleanup**
- Copy all artifacts to `runs/{run_id}/`
- Verify all files present and non-zero length
- Write `artifacts.json` manifest
- Write terminal `state.json` as LAST operation
- Delete or archive `queue/{run_id}/`

**Task 2.7: Thermal monitoring**
- Poll GPU temperature during training (nvidia-smi)
- Pause/fail if `gpu_temp_limit_c` exceeded (default 85C, matches existing train.py behavior at 88C)
- Record `gpu_temp_max_c` in result.json
- Fail with `ARNC-015` on thermal shutdown

**Task 2.8: Circuit breaker**
- Track consecutive failures by `failure_code`
- Track consecutive NaN rejections
- Stop claiming after 3 consecutive identical failures or 3 consecutive NaN rejections
- Resume on RESUME sentinel file or scope_tag change
- Log prominent alert on trip

### Phase 3: Supervisor Module (Ubuntu/Nodezero) -- Weeks 3-4

**Task 3.1: Experiment spec generator**
- Strategy interface: `generate_next(run_history, frontiers) -> ExperimentSpec | StopSignal`
- Built-in strategies: `hyperparameter_sweep`, `scaling_sweep`, `architecture_search`, `ablation`
- Strategy composition: sequential chaining with transition conditions

**Task 3.2: Queue writer**
- Create `queue/{run_id}/` directory
- Write experiment.json, patch.diff, state.json (queued)
- Write READY sentinel LAST
- Atomic write protocol: write to .tmp, rename

**Task 3.3: Result reader**
- Poll `runs/` directory for completed runs
- Read result.json and metrics.json
- Update frontiers per scope_tag
- Feed results back to strategy for next experiment generation

**Task 3.4: Cancellation**
- Write CANCEL sentinel to appropriate directory
- Do NOT write state.json directly

**Task 3.5: Staleness detection**
- Check `updated_at` against `2 * timeout_seconds`
- Supervisor MAY transition stale runs to failed with ARNC-019
- Supervisor MUST NOT modify repository state

**Task 3.6: Cross-machine file transfer**
- SCP/rsync-based sync between Nodezero and Desktop
- See section 3 for protocol details

### Phase 4: Integration and Testing -- Week 5

**Task 4.1: End-to-end smoke test**
- Supervisor enqueues a trivial run, Worker claims and completes

**Task 4.2: 10-run chained test**
- Sequential chained runs with lineage propagation
- Validates duplicate rejection, terminal states, lineage, artifact completeness, base commit propagation

**Task 4.3: Failure injection tests**
- Simulate ARNC-003 (bad patch), ARNC-004 (non-zero exit), ARNC-005 (timeout)

---

## 3. Communication Protocol

### File-Based Signaling via SSH/SCP

The two machines communicate exclusively through the filesystem. For cross-machine operation:

**Primary transport: rsync over SSH (LAN preferred)**

```
# Supervisor (Nodezero) pushes experiment to Worker (Desktop)
rsync -avz queue/{run_id}/ owner@192.168.1.X:autoresearch-pipeline/queue/{run_id}/

# Worker (Desktop) pushes results back to Supervisor
rsync -avz runs/{run_id}/ owner@192.168.1.5:autoresearch-pipeline/runs/{run_id}/
```

Per the memory file `desktop_ssh_key.md`: use LAN IPs first (MBP=192.168.1.5), Tailscale is unreliable.

**Alternative: SMB share from the Worker**
- Worker exposes `autoresearch-pipeline/` via SMB
- Supervisor mounts it on Nodezero
- Simpler polling but adds SMB reliability dependency

**Recommended approach for v0.1: rsync polling loop**

```python
# Supervisor sync loop (runs on Nodezero)
SYNC_INTERVAL = 15  # seconds
WORKER_HOST = "192.168.1.X"  # Desktop LAN IP
REMOTE_PATH = "autoresearch-pipeline"

# Push new queue entries to Worker
rsync_push(f"queue/", f"{WORKER_HOST}:{REMOTE_PATH}/queue/")

# Pull completed results from Worker
rsync_pull(f"{WORKER_HOST}:{REMOTE_PATH}/runs/", f"runs/")
```

### state.json Schema and Ownership Rules

```json
{
  "spec_version": "0.1.4",
  "run_id": "20260323T120000Z_a1b2c3d4",
  "state": "queued|dispatched|running|completed|accepted|rejected|failed|canceled",
  "worker_id": "{hostname}_{pid}_{start_timestamp}",
  "hostname": "DESKTOP-RTX3080",
  "pid": 12345,
  "created_at": "2026-03-23T12:00:00Z",
  "updated_at": "2026-03-23T12:05:33Z",
  "reason": "accepted: val_bpb improved by 0.012",
  "failure_code": null,
  "original_gpu_power_limit_w": null
}
```

**Ownership rule:** Only the Worker writes state.json. The Supervisor writes ONLY sentinel files (READY, CANCEL). This eliminates race conditions on the state file.

### Sentinel File Format

| File | Written By | Content | Purpose |
|------|-----------|---------|---------|
| `READY` | Supervisor | Empty (0 bytes) | Signals queue entry is complete and ready for processing |
| `CANCEL` | Supervisor | Empty (0 bytes) | Signals the Worker should abort the run |
| `RESUME` | Operator (manual) | Empty (0 bytes) | Resets the circuit breaker |

### Polling Intervals

| Component | What It Polls | Interval | Notes |
|-----------|--------------|----------|-------|
| Worker queue scanner | `queue/` for READY sentinels | 10 seconds | Configurable |
| Worker cancel checker | CANCEL sentinel | Before each major step | Not time-based -- checked at phase boundaries |
| Worker heartbeat | Writes `state.json.updated_at` | 60 seconds | During `running` state |
| Supervisor result reader | `runs/` for new results | 15 seconds | After rsync pull |
| rsync sync loop | Both directions | 15 seconds | Configurable |

### Stigmergic Coordination Mapping

This protocol is a direct implementation of **cognitive stigmergy** (RQ-005 finding):

| Stigmergy Concept | NemoClaw Implementation |
|-------------------|------------------------|
| Environmental trace | Files in queue/ and runs/ directories |
| Pheromone deposit | Supervisor writes experiment.json + READY |
| Agent reads environment | Worker polls queue/ for READY sentinels |
| Agent modifies environment | Worker writes result.json, transitions state |
| Emergent coordination | No direct messaging -- all communication through filesystem artifacts |
| Decoupling | Supervisor and Worker need no knowledge of each other's internal state |

---

## 4. Testing Strategy

Based on RQ-007 findings. Priority order reflects highest ROI per hour invested.

### P0: Schema Validation (Immediate)

**Pydantic models for all message schemas.** This is the single highest-ROI testing investment.

```python
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class RunState(str, Enum):
    QUEUED = "queued"
    DISPATCHED = "dispatched"
    RUNNING = "running"
    COMPLETED = "completed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    FAILED = "failed"
    CANCELED = "canceled"

class StateFile(BaseModel):
    spec_version: str
    run_id: str
    state: RunState
    worker_id: Optional[str] = None
    hostname: Optional[str] = None
    pid: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    reason: Optional[str] = None
    failure_code: Optional[str] = None
    original_gpu_power_limit_w: Optional[int] = None

    @field_validator('failure_code')
    @classmethod
    def valid_failure_code(cls, v):
        if v is not None:
            assert v.startswith('ARNC-'), f"Invalid failure code: {v}"
            code_num = int(v.split('-')[1])
            assert 1 <= code_num <= 22, f"Unknown failure code: {v}"
        return v
```

### P0: Property-Based Testing with Hypothesis

**State machine transitions (highest-risk logic):**

```python
from hypothesis import given, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

class NemoClawStateMachine(RuleBasedStateMachine):
    """Property-based test: no invalid state transitions are possible."""

    def __init__(self):
        super().__init__()
        self.state = RunState.QUEUED

    VALID_TRANSITIONS = {
        RunState.QUEUED: {RunState.DISPATCHED, RunState.CANCELED},
        RunState.DISPATCHED: {RunState.RUNNING, RunState.FAILED, RunState.CANCELED},
        RunState.RUNNING: {RunState.COMPLETED, RunState.FAILED, RunState.CANCELED},
        RunState.COMPLETED: {RunState.ACCEPTED, RunState.REJECTED},
    }
    TERMINAL = {RunState.ACCEPTED, RunState.REJECTED, RunState.FAILED, RunState.CANCELED}

    @rule()
    def try_dispatch(self):
        if self.state == RunState.QUEUED:
            self.state = RunState.DISPATCHED

    @rule()
    def try_run(self):
        if self.state == RunState.DISPATCHED:
            self.state = RunState.RUNNING

    @rule()
    def try_complete(self):
        if self.state == RunState.RUNNING:
            self.state = RunState.COMPLETED

    @rule()
    def try_accept(self):
        if self.state == RunState.COMPLETED:
            self.state = RunState.ACCEPTED

    @rule()
    def try_reject(self):
        if self.state == RunState.COMPLETED:
            self.state = RunState.REJECTED

    @rule()
    def try_fail(self):
        if self.state in {RunState.DISPATCHED, RunState.RUNNING}:
            self.state = RunState.FAILED

    @rule()
    def try_cancel(self):
        if self.state in {RunState.QUEUED, RunState.DISPATCHED, RunState.RUNNING}:
            self.state = RunState.CANCELED

    @invariant()
    def terminal_states_are_final(self):
        # Once terminal, no further transitions should be possible
        if self.state in self.TERMINAL:
            pass  # Rules above guard against this

TestNemoClawStateMachine = NemoClawStateMachine.TestCase
```

**Serialization round-trips:**

```python
from hypothesis import given
from hypothesis.strategies import builds, text, integers, floats, none

@given(builds(StateFile, ...))
def test_state_roundtrip(state: StateFile):
    """state.json survives write-read cycle."""
    json_str = state.model_dump_json()
    recovered = StateFile.model_validate_json(json_str)
    assert recovered == state
```

### P1: Mutation Testing for Acceptance Logic

The acceptance gate is critical-path code. Run `mutmut` on:
- Acceptance evaluation (`val_bpb_after < baseline - min_delta`)
- Scope-aware baseline resolution
- NaN detection logic
- Circuit breaker counter

Target: MSI > 80% on these modules.

```bash
mutmut run --paths-to-mutate=worker/acceptance.py,worker/circuit_breaker.py
```

### P2: Chaos Engineering -- Fault Injection

| Fault | How to Inject | What It Tests |
|-------|--------------|---------------|
| Network failure | Block rsync for N seconds | Graceful timeout, staleness detection |
| Thermal event | Mock nvidia-smi returning 90C | ARNC-015 handling, training pause |
| OOM | Set `max_vram_gb` below model requirement | ARNC-007 handling |
| Stale run | Kill Worker process mid-execution | Staleness detection, repo cleanup |
| Corrupt state.json | Write invalid JSON to state file | Worker error handling |
| CANCEL during execution | Write CANCEL sentinel during training | Clean abort, state transition |
| NaN output | Training script emits `val_bpb: nan` | NaN circuit breaker |

### P2: Contract Testing Between Supervisor and Worker

The contract is the filesystem directory structure. Test that:
1. Supervisor output (queue entry) validates against Worker's Pydantic input models
2. Worker output (result files) validates against Supervisor's Pydantic input models
3. Schema changes are backward-compatible (v0.1.3 queue entries work with v0.1.4 Worker)

```python
def test_supervisor_output_is_valid_worker_input():
    """Contract: Supervisor produces what Worker consumes."""
    spec = supervisor.generate_experiment_spec(...)
    # Must not raise ValidationError
    ExperimentSpec.model_validate(spec)
    StateFile.model_validate(supervisor.create_initial_state(spec))

def test_worker_output_is_valid_supervisor_input():
    """Contract: Worker produces what Supervisor consumes."""
    result = load_mock_result()
    ResultFile.model_validate(result)
    MetricsFile.model_validate(load_mock_metrics())
```

---

## 5. Security Model

Based on RQ-006 findings. NemoClaw v0.1 operates in a trusted environment (same user, private network), but the security model should be designed for future tightening.

### Trust Boundaries

```
+---------------------------------+     SSH/rsync     +---------------------------+
| Nodezero (Supervisor)           | <--------------> | Desktop (Worker)          |
| Ubuntu, M4 Pro, 48GB           |     LAN only      | Windows 11, RTX 3080 Ti   |
| Generates specs                 |                   | Executes arbitrary code   |
| Reads results                   |                   | Owns state.json           |
| Makes strategic decisions       |                   | Makes acceptance decision |
+---------------------------------+                   +---------------------------+
```

**Boundary 1: Machine boundary.** Supervisor on Nodezero, Worker on Desktop. Communication only via rsync/SSH over LAN.

**Boundary 2: Write ownership.** Supervisor writes queue entries. Worker writes run results. Neither crosses the other's write boundary (except Supervisor writes CANCEL sentinels, which are zero-byte signal files).

**Boundary 3: Code execution.** Only the Worker executes training code from patches. The Supervisor never executes untrusted code.

### Capability Tokens (Future -- Phase 2+)

For v0.1, trust is implicit (same user, same network). For future versions:

```python
@dataclass
class WorkerCapabilityToken:
    """Per-run authorization token from Supervisor to Worker."""
    run_id: str                    # Bound to specific run
    tool_scopes: list[str]         # ["git:checkout", "gpu:execute", "fs:write:runs/"]
    issuer_key: str                # Supervisor's public key
    holder_key: str                # Worker's public key
    expires_at: datetime           # run timeout + margin
    epoch: int                     # Emergency revocation counter
```

### Audit Trail -- Append-Only JSONL

Implement from day one. Every state transition and significant event appends to a JSONL log:

```
autoresearch-pipeline/
  audit/
    audit_2026-03-23.jsonl
```

Each line:

```json
{"ts":"2026-03-23T12:00:00Z","event":"state_transition","run_id":"20260323T120000Z_a1b2c3d4","from":"queued","to":"dispatched","actor":"worker","worker_id":"DESKTOP_12345_20260323","details":null}
{"ts":"2026-03-23T12:05:33Z","event":"acceptance_decision","run_id":"20260323T120000Z_a1b2c3d4","accepted":true,"val_bpb_before":0.4646,"val_bpb_after":0.4534,"delta":-0.0112,"scope_tag":"300s_tinystories"}
```

**Integrity:** Each line includes a SHA-256 hash of the previous line (hash chain). Tampering with any record breaks the chain.

### Kill Switch

Two mechanisms:

1. **CANCEL sentinel** -- Per-run cancellation. Supervisor writes `CANCEL` file; Worker checks before each major step.

2. **Epoch-based emergency stop** -- Global halt. A file `autoresearch-pipeline/EPOCH` contains an integer. All in-flight runs check the epoch matches their dispatch epoch. Incrementing the epoch invalidates all outstanding work.

3. **Circuit breaker** -- Automatic stop after 3 consecutive identical failures. Prevents overnight resource burn.

### Environment Override Blocklist

The Worker MUST reject these keys in `execution.env_overrides` (prevents privilege escalation via environment manipulation):

```
PATH, HOME, USER, SHELL, PYTHONPATH, PYTHONHOME, LD_LIBRARY_PATH,
DYLD_LIBRARY_PATH, LD_PRELOAD, CUDA_VISIBLE_DEVICES, TMPDIR, TEMP, TMP
```

---

## 6. Observability

### What to Log at Each State Transition

| Transition | Log Level | Fields |
|-----------|-----------|--------|
| queued (created) | INFO | run_id, hypothesis, parent_run_id, scope_tag |
| queued -> dispatched | INFO | run_id, worker_id, hostname, pid |
| dispatched -> running | INFO | run_id, command, device, training_time_budget_s |
| running (heartbeat) | DEBUG | run_id, updated_at, gpu_temp_c, elapsed_s |
| running -> completed | INFO | run_id, val_bpb, wall_seconds, throughput_tok_per_sec |
| completed -> accepted | INFO | run_id, val_bpb_before, val_bpb_after, delta, scope_tag |
| completed -> rejected | INFO | run_id, val_bpb_before, val_bpb_after, delta, reason |
| * -> failed | WARNING | run_id, failure_code, reason, wall_seconds |
| * -> canceled | INFO | run_id, reason |
| circuit_breaker_trip | ERROR | failure_code, consecutive_count, last_3_run_ids |
| thermal_warning | WARNING | run_id, gpu_temp_c, limit_c |

### Metrics to Track

| Metric | Computation | Target |
|--------|------------|--------|
| Experiments/hour | Completed runs / wall hours | >10 at 300s budget |
| Acceptance rate | Accepted / (Accepted + Rejected) | 10-30% (healthy exploration) |
| Failure rate | Failed / Total | <5% |
| Thermal events | Count of ARNC-015 per day | 0 |
| NaN rate | NaN rejections / Total | <2% |
| Circuit breaker trips | Count per day | 0 (ideal) |
| Frontier val_bpb | Best val_bpb per scope_tag over time | Monotonically decreasing |
| GPU utilization | avg gpu_power_avg_w / gpu_power_limit_w | >80% |
| Queue depth | Count of queued entries | 1-3 (pipeline not starved or overloaded) |

### Alert Conditions

| Condition | Severity | Action |
|-----------|----------|--------|
| Circuit breaker tripped | CRITICAL | Notify immediately. Manual intervention required. |
| GPU temp > 85C | WARNING | Log warning. Worker pauses training. |
| GPU temp > 90C | CRITICAL | Fail run with ARNC-015. Consider reducing power limit. |
| 5+ consecutive rejections | WARNING | Strategy may be exhausted. Review experiment direction. |
| Queue empty for >30 min | INFO | Supervisor may have stopped or be in decision phase. |
| Worker unreachable (staleness) | WARNING | Check SSH connectivity and Worker process. |
| Failure rate > 20% over 10 runs | WARNING | Systemic issue. Review recent failure codes. |

### Dashboard Design

A single Grafana-style dashboard with four panels:

1. **Run Timeline** -- Gantt chart of runs over time. Color-coded: green=accepted, red=rejected, orange=failed, gray=canceled. Shows experiment hypotheses on hover.

2. **Frontier Tracker** -- Line chart of best val_bpb per scope_tag over time. The primary success metric.

3. **Health Panel** -- GPU temperature (line), power draw (line), throughput (bar), thermal events (counter), circuit breaker status (indicator light).

4. **Strategy Summary** -- Table of recent runs: run_id, hypothesis, val_bpb, delta, decision, failure_code. Sortable and filterable.

Implementation: Parse the JSONL audit log and `runs/*/result.json` files. For v0.1, a Python script generating a static HTML report is sufficient. Grafana integration is Phase 2.

---

## 7. Error Handling

### All 22 Failure Codes with Handling Logic

| Code | Description | Recovery | Retry? |
|------|-------------|----------|--------|
| `ARNC-001` | Experiment spec validation failed | Fix spec. Check schema version match. Check timeout formula: `timeout_s >= budget * 1.2 + 120` | No -- Supervisor must fix spec |
| `ARNC-002` | Base commit not found | Verify git remote is reachable. `git fetch`. | Yes -- after fetch |
| `ARNC-003` | Patch application failed | Patch was generated against wrong commit or conflicts exist. Regenerate patch. | No -- Supervisor must regenerate |
| `ARNC-004` | Training command non-zero exit | Check stderr.log. Common: syntax error in patched code, import failure. | No -- Supervisor must fix patch |
| `ARNC-005` | Execution timeout exceeded | Training took longer than `timeout_seconds`. Increase timeout or reduce model size. | Maybe -- with adjusted timeout |
| `ARNC-006` | Metrics extraction failed | Training script did not emit val_bpb in expected format. Check stdout.log. | No -- Supervisor must fix |
| `ARNC-007` | Out of memory | Model too large for 12GB VRAM. Reduce model size, batch size, or enable gradient checkpointing. | No -- needs smaller config |
| `ARNC-008` | GPU/device not available | CUDA device not found. Check nvidia-smi. May need driver restart. | Yes -- after manual check |
| `ARNC-009` | Repository state corruption | Git repo in bad state. `git reset --hard`. `git clean -fd`. | Yes -- after repo cleanup |
| `ARNC-010` | Artifact write failure | Disk full or permissions error. Check `runs/` directory. | Yes -- after fixing disk/perms |
| `ARNC-011` | State transition violation | Bug in Worker logic. Invalid transition attempted. | No -- fix Worker code |
| `ARNC-012` | Queue entry incomplete | Missing experiment.json, patch.diff, or state.json. Supervisor bug. | No -- Supervisor must re-enqueue |
| `ARNC-013` | Duplicate run ID | Run ID collision. Extremely rare with SHA-256 hash. | No -- generate new run ID |
| `ARNC-014` | Worker internal error | Unhandled exception in Worker code. Check Worker logs. | Maybe -- depends on root cause |
| `ARNC-015` | Thermal shutdown | GPU exceeded temp limit. Wait for cooldown. Consider reducing power limit. | Yes -- after cooldown + power reduction |
| `ARNC-016` | Filesystem permission error | Cannot read/write required files. Check ownership and permissions. | Yes -- after fixing permissions |
| `ARNC-017` | Network/share unreachable | Cannot access shared filesystem. Check SSH, LAN connectivity. | Yes -- after network recovery |
| `ARNC-018` | Invalid patch format | patch.diff is not a valid unified diff. Regenerate. | No -- Supervisor must regenerate |
| `ARNC-019` | Stale or interrupted run | Worker crashed or was killed during execution. Detected by staleness check. | Yes -- Supervisor can re-dispatch |
| `ARNC-020` | Patch violates mutability constraints | Patch modifies files outside `mutable_paths` or in `immutable_paths`. | No -- Supervisor must fix |
| `ARNC-021` | Parent run result unavailable | Parent run not found or not in accepted state. Lineage chain broken. | No -- fix lineage |
| `ARNC-022` | GPU power limit change failed | Insufficient permissions or value out of range for nvidia-smi -pl. | No -- fix permissions or value |

### Circuit Breaker Logic

```python
class CircuitBreaker:
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.consecutive_failures: list[str] = []  # failure_codes
        self.consecutive_nan_rejections: int = 0
        self.tripped = False

    def record_failure(self, failure_code: str):
        self.consecutive_nan_rejections = 0
        self.consecutive_failures.append(failure_code)
        # Check if last N are identical
        if len(self.consecutive_failures) >= self.threshold:
            last_n = self.consecutive_failures[-self.threshold:]
            if len(set(last_n)) == 1:
                self.trip(f"3 consecutive {last_n[0]} failures")

    def record_nan_rejection(self):
        self.consecutive_failures.clear()
        self.consecutive_nan_rejections += 1
        if self.consecutive_nan_rejections >= self.threshold:
            self.trip("3 consecutive NaN rejections")

    def record_success(self):
        self.consecutive_failures.clear()
        self.consecutive_nan_rejections = 0

    def record_rejection(self, is_nan: bool = False):
        if is_nan:
            self.record_nan_rejection()
        else:
            # Normal rejection resets failure counter but not NaN counter
            self.consecutive_failures.clear()

    def trip(self, reason: str):
        self.tripped = True
        log.error(f"CIRCUIT BREAKER TRIPPED: {reason}")

    def reset(self):
        self.tripped = False
        self.consecutive_failures.clear()
        self.consecutive_nan_rejections = 0
        log.info("Circuit breaker reset")

    def check_scope_reset(self, new_scope_tag: str, tripped_scope_tag: str):
        """Reset if new run has different scope_tag than what tripped the breaker."""
        if new_scope_tag != tripped_scope_tag:
            self.reset()
```

### Recovery Procedures by Category

**Category A: Automatic recovery (Worker handles)**
- ARNC-005 (timeout): Worker kills process, collects partial logs, transitions to failed
- ARNC-015 (thermal): Worker pauses, waits for cooldown, fails the run
- ARNC-019 (stale): Worker detects on restart, cleans up

**Category B: Supervisor regenerates**
- ARNC-001, ARNC-003, ARNC-004, ARNC-006, ARNC-018, ARNC-020: Supervisor generates a new experiment with a corrected spec or patch

**Category C: Manual intervention**
- ARNC-008, ARNC-009, ARNC-010, ARNC-016, ARNC-017, ARNC-022: Infrastructure issues requiring operator attention

### Graceful Degradation

If the Worker encounters a non-fatal issue during a run:
1. **GPU temp approaching limit**: Log warning, continue. Fail only if limit exceeded.
2. **Partial metrics**: If val_bpb is present but optional telemetry fields are missing, proceed with acceptance evaluation. Missing telemetry is not a failure.
3. **rsync partial failure**: Retry with exponential backoff (1s, 2s, 4s). After 3 retries, log error and skip this sync cycle.

---

## 8. Cross-Machine Coordination

### Machine Capabilities

| Machine | Role | Hardware | Throughput | VRAM/RAM | Best For |
|---------|------|----------|-----------|----------|----------|
| Desktop | Worker | RTX 3080 Ti, 12GB VRAM | ~122K tok/sec | 12GB VRAM | PyTorch/CUDA training, fast iteration |
| Nodezero | Supervisor | M4 Pro, 48GB unified | ~44K tok/sec | 48GB unified | Strategy generation, result analysis, MLX training |

### Transfer Protocol: Hypothesis Format

When Desktop findings seed Nodezero experiments (or vice versa), the transfer uses `export_results.py` (already built). The format:

```json
{
  "source_machine": "desktop",
  "source_framework": "pytorch",
  "best_config": {
    "model": { "depth": 6, "head_dim": 64, "aspect_ratio": 64, ... },
    "training": { "total_batch_size": 16384, ... },
    "val_bpb": 0.4646,
    "scope_tag": "300s_tinystories"
  },
  "hypotheses_for_target": [
    {
      "hypothesis": "HEAD_DIM 64->32 may help on MLX where memory bandwidth is the bottleneck",
      "priority": "high",
      "rationale": "HEAD_DIM 128->64 was the biggest single win on Desktop (-0.017 val_bpb)"
    }
  ],
  "exported_at": "2026-03-23T12:00:00Z"
}
```

### Results Synchronization

```
Nodezero (Supervisor)                    Desktop (Worker)
    |                                         |
    |-- rsync push: queue/{run_id}/ --------->|
    |                                         |-- Claims run
    |                                         |-- Executes training
    |                                         |-- Writes runs/{run_id}/
    |<-- rsync pull: runs/{run_id}/ ----------|
    |                                         |
    |-- Reads result.json                     |
    |-- Updates frontier                      |
    |-- Generates next experiment             |
    |-- rsync push: queue/{next_run_id}/ ---->|
    |                                         |
```

Sync interval: 15 seconds. A full cycle (enqueue -> execute -> read result) takes approximately `training_time_budget_s + 60s overhead + 30s sync`.

### Cross-Pollination Strategy

1. **Desktop trains fast iterations** (300s budget, ~122K tok/sec). Explores hyperparameters and small architecture changes.
2. **Nodezero analyzes results** and generates hypotheses. Also runs its own MLX experiments for validation.
3. **When Desktop finds a breakthrough** (accepted run with significant delta), the Supervisor generates a corresponding MLX experiment for Nodezero to validate on a different framework.
4. **When Nodezero identifies a pattern** across multiple Desktop runs (e.g., "all depth-8 models are worse"), it adjusts the strategy to avoid wasted experiments.

The append-only audit log on both machines serves as the coordination bus -- each machine reads the other's results through rsync and uses them to inform future experiments.

---

## 9. Code Scaffolding

### Directory Structure

```
autoresearch-pipeline/
  nemoclaw/                    # Shared library (pip-installable)
    __init__.py
    models.py                  # Pydantic models for all schemas
    state_machine.py           # State enum, transition validator
    run_id.py                  # Run ID generation
    audit.py                   # Append-only JSONL audit logger
    config.py                  # Configuration schema (Pydantic Settings)
  supervisor/
    __init__.py
    main.py                    # Entry point: nemoclaw-supervisor
    queue_writer.py            # Creates queue entries
    result_reader.py           # Reads completed runs
    strategy/
      __init__.py
      base.py                  # Strategy interface
      hyperparameter_sweep.py
      scaling_sweep.py
      architecture_search.py
      ablation.py
    sync.py                    # rsync push/pull to Worker
    staleness.py               # Stale run detection
  worker/
    __init__.py
    main.py                    # Entry point: nemoclaw-worker
    queue_scanner.py           # Polls queue/ for READY entries
    claim.py                   # Two-phase claim protocol
    executor.py                # Git ops, patch apply, run training
    metrics_parser.py          # Extract val_bpb and telemetry from output
    acceptance.py              # Acceptance gate evaluation
    artifact_collector.py      # Copy artifacts to runs/
    thermal_monitor.py         # GPU temperature monitoring
    circuit_breaker.py         # Consecutive failure detection
    power_manager.py           # GPU power limit management
  tests/
    test_models.py             # Schema validation tests
    test_state_machine.py      # Hypothesis state machine tests
    test_acceptance.py         # Acceptance logic + mutation targets
    test_circuit_breaker.py    # Circuit breaker logic
    test_roundtrip.py          # Serialization round-trip properties
    test_contract.py           # Supervisor-Worker contract tests
    test_e2e.py                # End-to-end 10-run chained test
    conftest.py                # Shared fixtures
  spec/                        # Spec documents (existing)
  queue/                       # Queue directory (runtime)
  runs/                        # Results directory (runtime)
  audit/                       # Audit logs (runtime)
  pyproject.toml
```

### Key Interfaces

```python
# === nemoclaw/models.py ===

class ExperimentSpec(BaseModel):
    spec_version: str
    run_id: str
    repo: RepoConfig
    model: ModelConfig
    training: TrainingConfig
    objective: ObjectiveConfig
    constraints: ConstraintsConfig
    execution: ExecutionConfig
    acceptance: AcceptanceConfig
    lineage: LineageConfig

class ExecutionConfig(BaseModel):
    command: str
    timeout_seconds: int
    device: Literal["cuda", "mlx", "mps", "cpu"]
    max_vram_gb: Optional[float] = None
    gpu_temp_limit_c: float = 85.0
    training_time_budget_s: Optional[int] = None
    env_overrides: Optional[dict[str, str]] = None
    gpu_power_limit_w: Optional[int] = None

class AcceptanceConfig(BaseModel):
    min_delta: float
    require_metric_present: bool
    scope_tag: str = "default"


# === nemoclaw/state_machine.py ===

class StateMachine:
    TRANSITIONS: dict[RunState, set[RunState]] = {
        RunState.QUEUED: {RunState.DISPATCHED, RunState.CANCELED},
        RunState.DISPATCHED: {RunState.RUNNING, RunState.FAILED, RunState.CANCELED},
        RunState.RUNNING: {RunState.COMPLETED, RunState.FAILED, RunState.CANCELED},
        RunState.COMPLETED: {RunState.ACCEPTED, RunState.REJECTED},
    }

    def transition(self, current: RunState, target: RunState) -> None:
        allowed = self.TRANSITIONS.get(current, set())
        if target not in allowed:
            raise InvalidTransition(f"{current} -> {target} not allowed")


# === supervisor/strategy/base.py ===

class Strategy(ABC):
    @abstractmethod
    def generate_next(
        self,
        run_history: list[RunResult],
        frontiers: dict[str, float],  # scope_tag -> best val_bpb
    ) -> ExperimentSpec | StopSignal:
        """Return next experiment or signal to stop."""
        ...


# === worker/main.py ===

class NemoClawWorker:
    def __init__(self, config: WorkerConfig):
        self.scanner = QueueScanner(config.queue_dir)
        self.executor = Executor(config)
        self.circuit_breaker = CircuitBreaker(threshold=3)
        self.thermal_monitor = ThermalMonitor(default_limit=85.0)
        self.audit = AuditLogger(config.audit_dir)

    def run_loop(self):
        while True:
            if self.circuit_breaker.tripped:
                if self.check_resume_sentinel():
                    self.circuit_breaker.reset()
                else:
                    sleep(self.config.poll_interval)
                    continue

            entry = self.scanner.next_ready_entry()
            if entry is None:
                sleep(self.config.poll_interval)
                continue

            self.process_run(entry)
```

### Configuration Schema

```python
# === nemoclaw/config.py ===

class WorkerConfig(BaseSettings):
    # Paths
    pipeline_dir: Path = Path("autoresearch-pipeline")
    queue_dir: Path = Field(default=None)  # Derived from pipeline_dir
    runs_dir: Path = Field(default=None)
    audit_dir: Path = Field(default=None)
    repo_dir: Path  # Path to the training repo

    # Polling
    poll_interval_seconds: int = 10
    heartbeat_interval_seconds: int = 60
    sync_delay_seconds: int = 2  # Claim verification delay

    # Thermal
    default_gpu_temp_limit_c: float = 85.0
    thermal_poll_interval_seconds: int = 5

    # Circuit breaker
    circuit_breaker_threshold: int = 3

    class Config:
        env_prefix = "NEMOCLAW_"


class SupervisorConfig(BaseSettings):
    # Paths
    pipeline_dir: Path = Path("autoresearch-pipeline")
    queue_dir: Path = Field(default=None)
    runs_dir: Path = Field(default=None)
    audit_dir: Path = Field(default=None)

    # Remote Worker
    worker_host: str = "192.168.1.X"  # Desktop LAN IP
    worker_user: str = "Owner"
    remote_pipeline_dir: str = "autoresearch-pipeline"

    # Sync
    sync_interval_seconds: int = 15

    # Strategy
    default_scope_tag: str = "300s_tinystories"
    max_consecutive_rejections: int = 5

    class Config:
        env_prefix = "NEMOCLAW_"
```

### CLI Commands

```bash
# Worker (run on Desktop)
nemoclaw-worker start                   # Start the Worker loop
nemoclaw-worker status                  # Show current state, circuit breaker, GPU temp
nemoclaw-worker reset-breaker           # Reset circuit breaker (writes RESUME sentinel)

# Supervisor (run on Nodezero)
nemoclaw-supervisor start               # Start the Supervisor loop
nemoclaw-supervisor enqueue <spec.json> # Manually enqueue an experiment
nemoclaw-supervisor cancel <run_id>     # Cancel a run
nemoclaw-supervisor frontier            # Show best val_bpb per scope_tag
nemoclaw-supervisor history             # Show recent run history
nemoclaw-supervisor sync                # Force rsync cycle

# Shared utilities
nemoclaw-audit show                     # Display audit log
nemoclaw-audit verify                   # Verify hash chain integrity
nemoclaw-validate <file.json>           # Validate any NemoClaw JSON file against schema
```

---

## Appendix: Implementation Priority Summary

| Priority | Task | Effort | Dependency |
|----------|------|--------|------------|
| P0 | Pydantic models (`nemoclaw/models.py`) | 1 day | None |
| P0 | State machine (`nemoclaw/state_machine.py`) | 0.5 day | Models |
| P0 | Run ID generation (`nemoclaw/run_id.py`) | 0.5 day | Models |
| P1 | Worker queue scanner + claim | 1 day | State machine |
| P1 | Worker executor (git ops, training) | 2 days | Queue scanner |
| P1 | Worker metrics parser + acceptance | 1 day | Executor |
| P1 | Worker thermal monitor | 0.5 day | Executor |
| P1 | Worker circuit breaker | 0.5 day | Acceptance |
| P1 | Worker artifact collector | 0.5 day | Metrics parser |
| P2 | Supervisor queue writer + sync | 1 day | Models |
| P2 | Supervisor result reader | 0.5 day | Models |
| P2 | Supervisor strategy interface | 1 day | Result reader |
| P2 | Audit logger (JSONL + hash chain) | 0.5 day | None |
| P3 | Hypothesis state machine tests | 1 day | State machine |
| P3 | Contract tests | 0.5 day | Models |
| P3 | Mutation testing setup | 0.5 day | Acceptance tests |
| P3 | E2E 10-run chained test | 1 day | All components |
| P4 | Chaos fault injection tests | 1 day | E2E working |
| P4 | Dashboard / reporting | 1 day | Audit logger |
| P4 | Capability tokens | 2 days | Audit logger |

**Total estimated effort: ~18 days for a complete v0.1 implementation.**

Worker-first development is recommended -- get the Worker processing runs locally on the Desktop before adding cross-machine coordination. The Supervisor can initially be a manual script that creates queue entries.
