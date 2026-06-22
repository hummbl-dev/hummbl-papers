# HUMMBL Agent Architecture Specification v1.0

**Date:** 2026-03-23
**Status:** Draft
**Author:** Reuben Bowlby + Claude Strategic Synthesis
**Sources:** RQ-001 through RQ-005 autoresearch reports, NemoClaw v0.1.3 spec, Golden Ratio AI Stack benchmarks

---

## 1. System Overview

### 1.1 What HUMMBL Is

HUMMBL is a **reasoning framework for autonomous agent orchestration** -- a coordination layer that enables multiple AI agents to collaborate on research, code generation, and operational tasks across heterogeneous hardware. It is not a chatbot, not a single-agent tool, and not a framework library. It is the bus protocol, inference routing, and governance model that turns individual agents into a functioning team.

HUMMBL connects three operational domains:

| Domain | Function | Current State |
|--------|----------|---------------|
| **Autoresearch** | Autonomous ML experimentation (train.py loops, hyperparameter sweeps, architecture search) | 110+ experiments, val_bpb 0.4646, dual-machine |
| **Peptide-Checker** | Research report generation and vendor database for peptide therapeutics | 2 reports complete, 5 queued, 30-vendor DB |
| **AI Stack** | Local inference infrastructure (Ollama, model routing, caching, benchmarks) | llama3.1:8b at 133 tok/s, 20-experiment suite |

### 1.2 Design Philosophy

Three principles govern all architectural decisions:

1. **Solo-founder-first.** Every design choice must be operable by one person. No component should require a team to maintain. If it needs a dedicated operator, it does not belong here.

2. **Local-first, cloud-escalate.** Local inference handles the bulk of work (target: 75-85% of all queries). Cloud APIs are an escalation path, not a default. Cost discipline is a survival constraint.

3. **Append-only governance.** All coordination happens through an immutable, append-only log. No hidden state, no message-passing side channels. If it did not get written to the bus, it did not happen.

### 1.3 Architectural Context

```
                    +---------------------------+
                    |      Human Operator       |
                    |   (Reuben / Phone GPT)    |
                    +------------+--------------+
                                 |
                         Task Specs / Review
                                 |
                    +------------v--------------+
                    |     HUMMBL Governance Bus  |
                    |   (append-only JSONL log)  |
                    +--+------+------+------+---+
                       |      |      |      |
              +--------+  +---+--+ +-+----+ +-------+
              |Supervisor| |Worker| |Worker| |Monitor|
              |  Agent   | |  #1  | |  #2  | | Agent |
              +----+-----+ +--+---+ +--+---+ +---+---+
                   |           |        |         |
          +--------+-----------+--------+---------+--------+
          |                  Inference Layer                |
          |  [llama3.1:8b] --> [Sonnet] --> [Opus]         |
          |  Heuristic Router + Confidence Cascade          |
          +--------+-----------+--------+---------+--------+
                   |           |        |         |
          +--------+-----------+--------+---------+--------+
          |               Hardware Layer                   |
          |  Desktop: RTX 3080 Ti (CUDA, 12GB VRAM)        |
          |  Nodezero: Mac Mini M4 Pro (MLX, 48GB unified) |
          +------------------------------------------------+
```

---

## 2. Agent Architecture

### 2.1 Agent Types

HUMMBL defines four agent roles. Every agent is a stateless process that reads from and writes to the governance bus. Agents do not message each other directly -- all coordination is stigmergic (artifact-mediated through the shared bus).

| Role | Responsibility | Model Tier | Concurrency |
|------|---------------|------------|-------------|
| **Supervisor** | Task decomposition, worker spawning, result synthesis, quality gates | Opus-class (API) or strong local | 1 per task group |
| **Worker** | Execute bounded subtasks (research, code gen, analysis, training runs) | Sonnet-class or local 8b | 3-5 per supervisor |
| **Monitor** | Health probes, SLO tracking, alert correlation, circuit breaker enforcement | Local 8b (low-cost, continuous) | 1 per deployment |
| **Analyst** | Cross-run pattern detection, retrospective synthesis, improvement proposals | Sonnet-class (periodic batch) | 1, runs on schedule |

**Scaling constraints (validated by Anthropic production data):**
- 3-5 workers per supervisor (empirical sweet spot; >5 hits coordination overhead that cancels parallelism)
- 5-6 tasks per worker (below 3: spawning overhead unjustified; above 8: agent loses coherence)
- Practical ceiling: 4 workers x 5 tasks = 20 focused work units per supervisor cycle
- Token cost reality: multi-agent uses ~15x tokens vs. single-agent; only activate for tasks worth the cost

### 2.2 Agent Lifecycle

```
SPAWNED --> INITIALIZING --> ACTIVE --> COMPLETING --> TERMINATED
                |                         |
                |                    (on failure)
                |                         |
                +-----> FAILED -----------+
                                          |
                                   (circuit breaker)
                                          |
                                    QUARANTINED
```

Every state transition is recorded on the governance bus. An agent that fails 3 consecutive times on the same failure code enters QUARANTINED state (NemoClaw circuit breaker pattern, codes ARNC-001 through ARNC-021).

### 2.3 Communication Model: Stigmergic Bus + Direct Messaging Hybrid

**Primary channel: Governance Bus (stigmergic)**
- All task assignments, results, state transitions, and decisions flow through the append-only JSONL bus
- Agents read the bus to understand system state (consumer offset pattern -- each agent tracks its own read position)
- No agent needs to know about any other agent's existence or interface
- Natural audit trail; replay-capable for debugging (validated by OpenHands event-sourcing model)

**Secondary channel: Direct Messaging (mailbox)**
- For time-critical coordination only (e.g., supervisor needs immediate worker status for synthesis deadline)
- Implemented as per-agent mailbox files (Claude Agent SDK pattern)
- All direct messages are also echoed to the bus for audit completeness
- Use sparingly -- if more than 20% of coordination is direct messaging, the task decomposition is wrong

**Why hybrid?** Pure stigmergy has latency limitations (the bus must be polled). Pure direct messaging creates tight coupling and N-squared connection complexity. The hybrid gives fast coordination when needed while preserving the audit and decoupling benefits of the bus. This matches Anthropic's production agent teams architecture: shared task list (stigmergic) + mailbox (direct).

### 2.4 State Management: The Governance Bus

The governance bus is an append-only JSONL file that serves as the single source of truth for all system state.

**Bus entry schema:**

```json
{
  "id": "uuid-v4",
  "timestamp": "2026-03-23T14:30:00.000Z",
  "agent_id": "supervisor-001",
  "agent_role": "supervisor",
  "event_type": "task_assigned | result_submitted | state_change | health_probe | decision | error",
  "payload": {},
  "parent_id": "uuid-of-triggering-event | null",
  "schema_version": "1.0"
}
```

**Design patterns for the bus:**
- **Topic-based routing:** Agents filter events by `event_type` and `agent_role` to read only relevant entries
- **Compaction:** Periodic summarization of older entries to manage log growth (analyst agent responsibility)
- **Schema versioning:** Forward-compatible message formats; `schema_version` field enables migration
- **Deterministic replay:** Full event history enables debugging by replaying the exact sequence of agent actions

**Storage:** Plain JSONL files on local filesystem. No database, no message broker, no infrastructure dependency. This is intentional -- minimal infrastructure means minimal failure modes for a solo operator.

---

## 3. Inference Layer

### 3.1 Local Inference: The Default Path

**Production default: llama3.1:8b on RTX 3080 Ti**

| Metric | Value |
|--------|-------|
| Throughput | 133 tok/s sustained (30-min thermal soak validated) |
| TTFT | Sub-200ms |
| VRAM | 6.9 GB (with q4_0 KV cache) |
| Quality | 4.8/5 on founder tasks |
| Thermals | 52-68C at 270W power cap, zero throttle events |
| Reliability | 99.5% (426/428 runs) |
| Batch throughput | 364 prompts/hr sustained |

**KV cache configuration:**
- q8_0 active (current production)
- q4_0 validated: +44% speed, no quality loss -- pending migration
- Full 3-model stack fits on GPU: llama3.1:8b + llama3.2:1b + moondream = 11.3 GB

**Cross-machine inference:**
- Desktop (RTX 3080 Ti): CUDA/PyTorch, primary inference and training
- Nodezero (M4 Pro, 48GB): MLX, secondary inference, can run larger models (up to ~30B quantized)
- Connection: LAN IP 192.168.1.5 (Nodezero), SSH-based coordination
- LiteLLM can manage both as backend providers with latency-aware routing

### 3.2 Heuristic Routing

**Why heuristics over learned routers:** At small scale (solo operator, <1000 routing decisions/day), heuristic rules outperform learned routers. Learned routers suffer from a documented systematic failure: as budget increases, they default to the most expensive model even when cheaper ones suffice. The Golden Ratio experiment suite validated this -- the heuristic router achieved 100% accuracy with 0ms overhead, and the LLM router was retired.

**Routing rules (current):**

```
IF task_type IN (email_triage, brief_drafting, simple_qa, formatting)
  THEN route → llama3.1:8b (local, free)

IF task_type IN (code_generation, pr_review, analysis, research_synthesis)
  THEN route → Claude Sonnet (API)

IF task_type IN (architecture_decision, complex_debugging, security_review, strategic_planning)
  THEN route → Claude Opus (API)

IF task_type == batch_research
  THEN route → Claude Sonnet batch API (50% discount)
```

**Routing progression roadmap:**
1. **Now:** Heuristic rules (keyword, task-type classification, prompt length)
2. **Month 2:** Add confidence-based escalation from log-probabilities
3. **Month 4:** Train lightweight BERT classifier or RouteLLM matrix factorization model on accumulated routing data
4. **Month 6:** Hybrid approach -- heuristic pre-filter + learned fine-tuning

### 3.3 Confidence-Based Cascading

When the local model handles a query, its confidence determines whether to escalate:

```
Tier 0: llama3.1:8b (local, 133 tok/s, free)
    |
    | confidence < 0.70 (conservative start; lower to 0.30 as calibration data builds)
    v
Tier 1: Larger local model on Nodezero OR llama3.1:8b with extended context
    |
    | confidence < threshold OR task exceeds local capability
    v
Tier 2: Claude Sonnet API (balanced cost/quality)
    |
    | task requires deep reasoning, architecture decisions, or security review
    v
Tier 3: Claude Opus API (maximum capability)
```

**Key implementation detail:** Avoid Ollama model swapping for local cascading (2-5 second overhead per swap). Keep the primary model loaded; use API calls for escalation rather than swapping local models.

**GATEKEEPER pattern (future):** Fine-tune the local model's confidence calibration so high confidence correlates with actual correctness. This directly improves cascade routing accuracy without changing the model itself.

### 3.4 Caching Strategy

**Multi-tier cache architecture:**

| Tier | Type | Expected Hit Rate | Latency | Savings Per Hit |
|------|------|-------------------|---------|-----------------|
| L1 | Exact match (hash-based) | 5-15% | <1ms | 99%+ |
| L2 | Semantic cache (embedding similarity) | 15-25% | 10-50ms | 95% |
| L3 | Prefix/KV cache (Ollama native) | Variable | Minimal | 30-70% on matching prefixes |

**Semantic cache configuration:**
- Cosine similarity threshold: 0.95 (start conservative)
- Partition by task type to prevent cross-domain contamination
- TTL-based invalidation + negative feedback loop
- Target: 15-20% overall cache hit rate

**Cost target:** 75-85% API cost reduction through the combined stack of heuristic routing (60-70% savings) + caching (15-25% additional) + batch APIs for non-interactive workloads (50% discount).

---

## 4. Security Model

### 4.1 Capability-Based Permissions

> **Note:** Full capability-based security findings are pending from RQ-006 (capability_security_agent_systems_2026.md). The following is the preliminary design informed by RQ-001 through RQ-005 findings. This section will be revised when RQ-006 completes.

Each agent receives a capability token at spawn time that defines its permitted operations:

```json
{
  "agent_id": "worker-research-003",
  "capabilities": [
    "bus:read",
    "bus:write:result_submitted",
    "bus:write:state_change",
    "filesystem:read:/autoresearch-reports/**",
    "filesystem:write:/autoresearch-reports/reports/**",
    "inference:local:llama3.1:8b",
    "inference:api:sonnet",
    "network:outbound:api.anthropic.com"
  ],
  "denied": [
    "filesystem:write:/autoresearch-win-rtx/train.py",
    "inference:api:opus",
    "network:outbound:*",
    "process:exec:*"
  ],
  "expires": "2026-03-23T15:30:00.000Z",
  "issuer": "supervisor-001"
}
```

**Principle of least privilege:** Workers get only the capabilities needed for their specific subtask. A research worker can read the codebase and write reports but cannot modify training code or execute arbitrary processes.

### 4.2 Delegation Tokens

When a supervisor spawns a worker, it issues a delegation token that is a subset of its own capabilities. No agent can grant capabilities it does not possess. This creates a monotonically decreasing trust chain:

```
Human Operator (full capabilities)
  └─ Supervisor (broad read/write, API access, worker spawning)
       └─ Worker (narrow read/write, limited API, no spawning)
            └─ Sub-worker (minimal, single-task scope)
```

### 4.3 Audit Trail

The governance bus IS the audit trail. Every agent action, every capability exercise, every state transition is recorded with:
- Agent identity
- Timestamp
- Capability token used
- Action taken
- Result

This satisfies the auditability requirement without any additional infrastructure.

### 4.4 Kill Switch and Circuit Breaker Patterns

**Kill switch (immediate halt):**
- A CANCEL sentinel file (NemoClaw pattern) stops all workers in the current task group
- Supervisor can issue a `system:halt` bus event that all agents must respect within one poll cycle
- Human operator can write directly to the bus or touch the sentinel file
- Thermal threshold: GPU temp > 85C triggers automatic pause (configurable via `execution.gpu_temp_limit_c`)

**Circuit breaker (graduated response):**
- 3 consecutive identical failures on the same failure code --> agent enters QUARANTINED state
- Exponential backoff between retries (1s, 2s, 4s, 8s, max 60s)
- Supervisor can spawn replacement worker if one enters QUARANTINED
- Partial result synthesis: supervisor assembles best-effort response from successful workers if some fail
- All circuit breaker activations are logged to bus with failure codes (ARNC-001 through ARNC-021)

**Adversarial considerations:** The "When AIOps Become AI Oops" paper (arXiv 2508.06394) demonstrates that attackers can manipulate telemetry to mislead AI agents. Mitigation: integrity checks on monitoring data, never auto-execute destructive actions without human confirmation, graduated trust escalation.

---

## 5. Quality Assurance

### 5.1 Code Review Pipeline

The hybrid static analysis + LLM triage pipeline achieves the highest validated detection rates while minimizing false positive noise:

```
PR / Code Change
  |
  v
[Stage 1: Semgrep SAST] ---------> Block on critical vulns
  | (free, <10s, 35+ languages)     74.8% raw FP rate
  |
  v
[Stage 2: LLM Post-Filter] ------> Triage SAST findings
  | (reduces FP from 92% to 6.3%)   Validated by research
  |
  v
[Stage 3: LLM Contextual Review] -> Comment with suggestions
  | (CodeRabbit-style, 46% bug      Never auto-block
  |  detection rate)
  |
  v
[Stage 4: Human Review] ----------> Required for:
  | (architecture, security,         - Auth/crypto code
  |  business logic)                 - Cross-service changes
  |                                  - API contract changes
  v
Merge (with governance bus entry recording the review chain)
```

**Key metrics to track:**
- AI suggestion acceptance rate (target: >80% within 4 weeks; below 60% means too much noise)
- False positive rate per stage
- Time-to-merge with and without AI review
- Revert rate for AI-reviewed changes

### 5.2 Step-Level Verification with Process Reward Models

**ThinkPRM** provides step-by-step verification of agent reasoning chains:
- Generates verification chain-of-thought for every solution step
- Uses only 1% of the labels needed by discriminative PRMs while outperforming them
- Applicable to NemoClaw worker output verification: each worker's result verified step-by-step before the supervisor accepts it

**Application in HUMMBL:**
- Workers submit results with reasoning traces to the bus
- Supervisor (or a dedicated verifier agent) applies ThinkPRM-style verification
- Steps flagged as low-confidence trigger re-execution or escalation
- This is more reliable than simple pass/fail validation

### 5.3 NemoClaw val_bpb Acceptance Gate

For autoresearch experiments specifically, the acceptance criterion is deterministic and non-negotiable:

```
IF new_val_bpb < (best_val_bpb - min_delta)
  THEN accept patch, update baseline
  ELSE reject patch, log failure code
```

- `val_bpb` is the sole acceptance metric
- `min_delta` is configurable (prevents noise-level improvements from being accepted)
- Current best: 0.4646 (Desktop, after 110+ experiments)
- All acceptance/rejection decisions logged to bus with full experiment metadata

### 5.4 Multi-Agent Cross-Validation

For critical outputs (security reviews, architectural decisions, research conclusions):
- Two workers independently produce results for the same task
- Supervisor compares outputs; agreement raises confidence, disagreement triggers deeper review
- Adversarial review pattern: a dedicated reviewer agent challenges findings before acceptance
- Cost: 2x token usage for cross-validated tasks; reserve for high-stakes decisions only

---

## 6. Observability

### 6.1 The $0 Observability Stack

| Layer | Tool | Cost | Function |
|-------|------|------|----------|
| Instrumentation | OpenTelemetry (auto-instrumentation) | Free | Traces, metrics, logs collection |
| Metrics | Grafana Cloud free tier | $0 | 10K metrics series |
| Logs | Grafana Cloud free tier | $0 | 50GB/month |
| Traces | Grafana Cloud free tier | $0 | 50GB/month |
| Visualization | Grafana | Free | Dashboards, exploration |
| Alerting | Grafana Alerting | Free | SLO-based burn rate alerts |
| On-call | PagerDuty free tier | $0 | Escalation, scheduling |
| Uptime | UptimeRobot free tier | $0 | 50 monitors |

**Total cost: $0/month** for the foundation. Upgrade to Grafana Cloud Pro ($29-50/month) only when free tier limits are hit.

**Alternative (self-hosted):** SigNoz on a small VM ($20-50/month infrastructure) for unlimited volume. OpenTelemetry-native, unified logs/metrics/traces.

### 6.2 SLO-Based Burn-Rate Alerting

**Only alert on error budget burn rate, never on individual metric thresholds.** This is the single most impactful practice for eliminating alert fatigue as a solo operator.

**Configuration:**

| Alert Type | Burn Rate | Window | Action |
|------------|-----------|--------|--------|
| Fast burn | 14.4x | 5% budget in 1 hour | Page immediately |
| Slow burn | 1.0x | Normal rate over days | Ticket, do not page |
| Budget exhausted | N/A | 0% remaining | Block deployments |

**SLO definitions (initial):**
- Autoresearch pipeline: 95% experiment completion rate (5% error budget)
- Inference service: 99% availability, p95 latency < 500ms for local, < 2s for API
- Bus integrity: 100% -- any corruption is a P0

### 6.3 Agent-Level Metrics and Health Probes

The Monitor agent continuously tracks:

| Metric | Collection Method | Alert Threshold |
|--------|-------------------|-----------------|
| Agent heartbeat | Bus write every 60s | Missing 3 consecutive beats |
| Task completion rate | Bus event analysis | < 80% over rolling 1hr window |
| Average task latency | Bus timestamps | > 2x rolling average |
| Error rate by failure code | Bus error events | Circuit breaker threshold (3 consecutive) |
| GPU temperature | nvidia-smi polling | > 85C (configurable) |
| GPU VRAM usage | nvidia-smi polling | > 95% |
| Inference throughput | Ollama metrics | < 100 tok/s (degradation signal) |
| API cost accumulation | Inference layer logging | Daily budget threshold |

### 6.4 Topology-Aware Alert Correlation

Inspired by BigPanda's 95%+ noise reduction approach, but built for HUMMBL's scale:

1. **Service dependency map:** Autoresearch pipeline stages, inference endpoints, bus, filesystem
2. **Temporal windowing:** Alerts within 60s of each other from related components are grouped
3. **Causal ordering:** Upstream failures (bus, inference) suppress downstream symptom alerts
4. **Deduplication:** NLP-based semantic similarity groups alerts with different wording but same root cause

At HUMMBL's current scale, this is implementable as a simple rules engine in the Monitor agent. Graph neural networks and ML-based correlation are premature.

---

## 7. NemoClaw Integration

### 7.1 NemoClaw Within HUMMBL

NemoClaw is HUMMBL's first production implementation of the supervisor-worker pattern, specialized for autonomous ML experimentation. It is not a separate system -- it is a domain-specific instantiation of the HUMMBL agent architecture.

```
HUMMBL Governance Bus
  |
  +-- NemoClaw Supervisor (runs on Nodezero/Ubuntu)
  |     |
  |     +-- Worker: Experiment Runner (runs on Desktop/RTX 3080 Ti)
  |     |     - Reads experiment config from queue
  |     |     - Executes train.py with specified hyperparameters
  |     |     - Reports val_bpb and training metrics to bus
  |     |
  |     +-- Worker: Analyzer (runs on either machine)
  |     |     - Reads experiment results from bus
  |     |     - Runs statistical analysis (propose_changes.py)
  |     |     - Generates improvement hypotheses
  |     |
  |     +-- Worker: Patch Generator (runs on Nodezero)
  |           - Takes analyzer hypotheses
  |           - Generates code patches for next experiment
  |           - Submits patches to acceptance gate
  |
  +-- Monitor Agent (continuous)
        - GPU thermal monitoring
        - Experiment stall detection
        - Circuit breaker enforcement
```

### 7.2 File-Based Queue and State Machine

NemoClaw uses a file-based coordination protocol that maps onto the HUMMBL bus:

| NemoClaw Concept | HUMMBL Bus Mapping |
|------------------|--------------------|
| READY sentinel file | `event_type: task_assigned` bus entry |
| CANCEL sentinel file | `event_type: system_halt` bus entry |
| state.json | Agent state tracked via bus `state_change` events |
| Worker owns state.json | Worker writes `state_change`; other agents read-only |
| Experiment results JSON sidecar | `event_type: result_submitted` bus entry with full payload |

**State machine (NemoClaw v0.1.3):**

```
IDLE --> QUEUED --> RUNNING --> EVALUATING --> ACCEPTED/REJECTED
                     |                            |
                     +--- FAILED (with ARNC code) |
                                                  |
                                           (update baseline if accepted)
```

### 7.3 Cross-Machine Coordination

| Machine | Role | Hardware | Connection |
|---------|------|----------|------------|
| Desktop (Windows) | Worker: experiment execution, GPU training | RTX 3080 Ti, 12GB VRAM | LAN primary, Tailscale fallback |
| Nodezero (macOS) | Supervisor: orchestration, analysis, larger model inference | M4 Pro, 48GB unified | LAN IP 192.168.1.5 |

**Coordination protocol:**
1. Supervisor (Nodezero) writes experiment config to shared bus location
2. Worker (Desktop) polls bus, claims experiment via state_change event
3. Worker executes training (PyTorch/CUDA), streams metrics to bus
4. Worker writes final result (val_bpb, training curves, config) to bus
5. Supervisor evaluates against acceptance gate
6. Supervisor either queues next experiment or escalates to Analyst for hypothesis revision

**File transfer:** Experiment configs and results are JSONL on the bus (small payloads). Model checkpoints and large artifacts use direct filesystem access over LAN mount or rsync.

---

## 8. Implementation Roadmap

### Phase 1: Bus Protocol + Basic Agent Loop (Weeks 1-3)

**Deliverables:**
- [ ] Governance bus: append-only JSONL writer/reader with schema validation
- [ ] Bus entry schema v1.0 (as specified in Section 2.4)
- [ ] Basic agent loop: read bus -> decide -> act -> write bus
- [ ] Supervisor agent: task decomposition from natural language spec into bounded subtasks
- [ ] Worker agent: execute subtask, report result to bus
- [ ] Kill switch: CANCEL sentinel + system_halt bus event
- [ ] Unit tests for bus operations (append, read, filter, replay)

**Success criteria:** A supervisor can decompose a research task into 3 subtasks, spawn 3 workers, collect results, and synthesize a report -- all coordinated through the bus with a complete audit trail.

### Phase 2: Inference Routing + Caching (Weeks 4-6)

**Deliverables:**
- [ ] Heuristic router: task-type classification -> model selection
- [ ] Confidence-based cascading: log-probability extraction from llama3.1:8b responses
- [ ] Exact-match cache (L1): hash-based, immediate savings on repeated patterns
- [ ] Batch API integration: route non-interactive workloads to Claude batch endpoints
- [ ] Routing decision logging: every route recorded with confidence score for later analysis
- [ ] Cross-machine inference: LiteLLM managing Desktop (Ollama) + Nodezero (MLX) backends

**Success criteria:** 60-70% of inference requests handled locally. API cost reduced by 60%+ compared to always-API baseline. All routing decisions logged for future learned-router training.

### Phase 3: Security Model + Governance (Weeks 7-10)

**Deliverables:**
- [ ] Capability token schema and issuance (supervisor -> worker delegation)
- [ ] Permission enforcement: agents can only perform operations matching their token
- [ ] Audit trail validation: tooling to replay and verify the complete decision chain
- [ ] Circuit breaker: 3-consecutive-failure quarantine with ARNC failure codes
- [ ] Thermal kill switch integration (GPU temp > 85C -> pause all GPU workers)
- [ ] Incorporate RQ-006 findings on capability-based security when available

**Success criteria:** No agent can exceed its granted capabilities. Circuit breaker prevents runaway failure loops. Complete audit trail for any sequence of events can be reconstructed from the bus.

### Phase 4: Full Multi-Agent Orchestration (Weeks 11-16)

**Deliverables:**
- [ ] NemoClaw integration: supervisor-worker pipeline running overnight experiments autonomously
- [ ] Monitor agent: continuous health probes, SLO tracking, alert correlation
- [ ] Analyst agent: periodic cross-run analysis, improvement hypothesis generation
- [ ] Semantic caching (L2): embedding-based similarity cache with 0.95 cosine threshold
- [ ] Direct messaging mailbox for time-critical supervisor-worker coordination
- [ ] Prompt compression (LLMLingua integration) for long-context API calls
- [ ] Code review pipeline: Semgrep + LLM post-filter integrated into PR workflow

**Success criteria:** NemoClaw runs autonomously overnight, executing experiments, evaluating results, and queuing follow-up experiments without human intervention. Monitor agent catches and auto-remediates known failure patterns. Full 75-85% API cost reduction target achieved.

---

## 9. Technology Decisions

### 9.1 Framework: Direct API + Custom Orchestration

**Decision:** Build custom orchestration on direct API calls. Do not adopt CrewAI, AutoGen, LangGraph, or any multi-agent framework.

**Rationale:**
- Frameworks add abstraction that a solo founder must maintain and debug
- CrewAI has known delegation bugs (#4783); AutoGen broke backward compatibility in v0.4
- HUMMBL's bus protocol is a better fit than any framework's built-in coordination model
- The overhead of learning and maintaining a framework exceeds the overhead of building purpose-fit coordination
- Direct API calls with custom orchestration gives maximum control over routing, caching, and cost management

**Validated by:** Anthropic's own agent teams use direct orchestration (Claude Agent SDK), not a third-party framework. The best developers in 2026 are the best at decomposing problems, not the best at configuring frameworks.

### 9.2 Protocol: MCP Foundation, A2A for Inter-Agent (Emerging)

**Now:** MCP (Model Context Protocol) for all agent-tool communication. Already in use via Claude Code.

**Watch:** A2A (Google's Agent-to-Agent Protocol) for future inter-agent interoperability. Version 0.3 with Linux Foundation governance. Relevant if HUMMBL needs to coordinate with external agent systems.

**Skip:** ACP and ANP -- premature for solo-founder scale. NLIP (Ecma International) -- too early, not yet adopted.

**Protocol adoption roadmap (from survey arXiv 2505.02279):**
1. Stage 1 (MCP): Foundational tool invocation -- **current**
2. Stage 2 (A2A): Enterprise task orchestration between agents -- **monitor**
3. Stage 3 (ACP/ANP): Decentralized open-internet collaboration -- **skip for now**

### 9.3 Storage: Append-Only JSONL

**Decision:** All bus state stored as append-only JSONL files on local filesystem.

**Rationale:**
- Zero infrastructure dependency (no database, no message broker)
- Immutable history enables deterministic replay and debugging
- Natural causal ordering through append semantics
- Easy to implement, easy to backup, easy to inspect manually
- Aligns with OpenHands' event-sourced model (validated at ICLR 2025)
- Results stored in `autoresearch-reports/` as JSON sidecars (already in use)

**Growth management:**
- Compaction: Analyst agent periodically summarizes older entries
- Archival: Completed task groups archived to compressed JSONL after synthesis
- Expected volume: ~1-5 MB/day at current experiment throughput; manageable for years without infrastructure changes

### 9.4 Edit Format: Search/Replace + Full-File Hybrid

For code generation agents, the edit format matters as much as the model (GPT-4 Turbo: 26% -> 59% from format change alone):

- Files >400 lines: search/replace blocks (Aider-style, preserves untouched code)
- Files <400 lines: full-file replacement (higher reliability, per Cursor benchmarks)
- Layered matching: exact -> whitespace-insensitive -> fuzzy (Aider pattern)
- Future: dedicated apply model for robust edit application (Cursor's dual-AI pattern)

### 9.5 Local Serving: Ollama (Now), vLLM (Future)

**Now:** Ollama for local model serving. Simple, reliable, well-integrated with the stack.

**Future:** Migration to vLLM when speculative decoding becomes critical:
- EAGLE-3 delivers 2-3x latency reduction at low batch sizes (the consumer hardware scenario)
- vLLM v0.8.5+ supports EAGLE-3 natively
- Ollama does not support speculative decoding
- Migration deferred until Phase 4 or later -- Ollama's simplicity is the right tradeoff now

---

## 10. Open Questions and Future Work

### 10.1 Pending Research Dependencies

| Item | Source | Impact on Architecture |
|------|--------|----------------------|
| RQ-006: Capability-based security | Queued research | Will refine Section 4 permission model |
| Speculative decoding on consumer GPU | Phase 4+ | May require Ollama -> vLLM migration |
| Learned router training | After 1000+ routing decisions | Will augment heuristic router in Section 3.2 |
| GLA / Hymba hybrid architectures | Next autoresearch phase | May change NemoClaw experiment parameters |

### 10.2 Risks

1. **Token cost at scale.** Multi-agent systems use 15x tokens. Cost discipline requires constant monitoring and routing optimization. The 75-85% cost reduction target must be validated, not assumed.

2. **Coordination overhead for solo operator.** Debugging multi-agent systems is harder than single-agent. The bus audit trail is designed to mitigate this, but novel failure modes will emerge.

3. **Hallucination in autonomous loops.** Zalando reported 40% hallucination rates with smaller models. HUMMBL's local 8b model is in this category. Mitigation: deterministic acceptance gates (val_bpb), never auto-execute destructive actions, graduated trust escalation.

4. **Hardware thermal limits.** GPU training + heavy inference can trigger thermal shutdowns (documented history). The 270W power cap and 85C thermal threshold are guardrails, not guarantees.

5. **Protocol churn.** MCP, A2A, ACP are all pre-1.0. Architectural decisions should be protocol-portable. The bus abstraction layer must be thin enough to swap underlying protocols without rewriting agents.

### 10.3 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| API cost reduction | 75-85% vs. always-API | Monthly API spend tracking |
| Overnight experiment throughput | 20+ experiments/night | Bus event count |
| Experiment acceptance rate | >10% of patches improve val_bpb | NemoClaw acceptance gate logs |
| Agent failure rate | <5% of task executions | Bus error event analysis |
| Alert noise | <1 false positive page per week | PagerDuty analytics |
| Time-to-first-result | <5 min for research tasks | Bus timestamp analysis |
| Bus integrity | 0 corruption events | Checksum validation |

---

*This specification synthesizes findings from five autoresearch reports (RQ-001 through RQ-005), the NemoClaw v0.1.3 spec, and the Golden Ratio AI Stack benchmark suite. It represents the architectural foundation for HUMMBL as of 2026-03-23. Revisions will be driven by RQ-006 findings and implementation learnings from Phase 1.*
