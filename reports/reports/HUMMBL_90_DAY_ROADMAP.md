# HUMMBL 90-Day Strategic Roadmap

**Period:** March 24 -- June 22, 2026
**Author:** Reuben Bowlby + Claude Strategic Synthesis
**Version:** 1.0
**Date:** 2026-03-23
**Status:** Active
**Sources:** HUMMBL Architecture Spec v1.0, Peptide Checker Business Plan, RQ-004/005/008/009, NemoClaw v0.1.3 Spec, Project Goals, Last Economy Analysis

---

## 1. Strategic Framework

### The Three-Product Pipeline

```
Autoresearch (Engine)         HUMMBL (Framework)          Peptide Checker (Revenue)
  |                              |                              |
  | ML experiments               | Bus protocol                 | Vendor database
  | val_bpb improvements         | Agent orchestration          | COA verification
  | Architecture search          | Inference routing            | Regulatory tracker
  |                              |                              |
  +--- builds expertise ---->----+--- powers agents ---->-------+--- generates revenue
```

**The logic:** Autoresearch produces ML expertise and validates the agent orchestration patterns that become HUMMBL. HUMMBL's reasoning framework powers Peptide Checker's AI features. Peptide Checker generates revenue that funds continued R&D. Each product feeds the others.

### Strategic Posture

Drawn from the Last Economy analysis, three principles govern this roadmap:

1. **Revenue now, position later.** Peptide Checker works regardless of AI timeline scenarios. It does not depend on breaking val_bpb plateaus or perfecting multi-agent coordination. Ship it first.

2. **Build things that compound.** The governance bus, inference routing, and reasoning traces are valuable whether AI capability accelerates or plateaus. Do not optimize for one timeline.

3. **The messy middle is the market.** HUMMBL's reasoning framework is most valuable in the current era where agents are capable but unreliable. Structured governance, quality gates, and audit trails are the gap. Fill it.

### Solo Founder Constraints

- **Time budget:** 4-6 focused hours/day, 5-6 days/week = 20-36 hours/week
- **Hardware:** Desktop (RTX 3080 Ti, CUDA) + Nodezero (M4 Pro, 48GB MLX) + Phone (GPT-5.4 for spec design)
- **AI leverage:** Claude Code for implementation, Aider for pair programming, autoresearch overnight, batch API for non-interactive work
- **Cost discipline:** Target $350-960/month total API spend (per RQ-008 cost model). Local inference at $0.04/hr electricity is essentially free.
- **Cognitive load:** No more than two active projects per week. Context switching is the real enemy.

---

## 2. Month 1: Foundation (March 24 -- April 23)

### Week 1-2 (March 24 -- April 6): Infrastructure Sprint

**Peptide Checker (60% of time):**
- [ ] Register domain (peptidechecker.com or similar)
- [ ] Set up Cloudflare Workers project with D1 database
- [ ] Migrate peptide_db.py data from JSON files to D1/PostgreSQL schema
- [ ] Design expanded database schema: add `last_test_date`, `endotoxin_result`, `ms_confirmed`, `coa_on_file`, `regulatory_status` fields
- [ ] Build FastAPI backend: `/peptides`, `/vendors`, `/search`, `/stats` endpoints
- [ ] Draft Terms of Service, Privacy Policy, Disclaimer (attorney review)
- [ ] Publish 5 existing research reports as web content (markdown to HTML)

**HUMMBL Bus Protocol (30% of time):**
- [ ] Implement governance bus: append-only JSONL writer/reader with schema validation
- [ ] Define bus entry schema v1.0 (per Architecture Spec Section 2.4)
- [ ] Write unit tests for bus operations: append, read, filter by event_type, replay
- [ ] Implement basic agent loop skeleton: read bus -> decide -> act -> write bus

**Autoresearch (10% of time -- overnight runs only):**
- [ ] Queue GLA (Gated Linear Attention) experiments on Desktop
- [ ] Run overnight; review results each morning
- [ ] Begin logging experiment results as structured reasoning traces (hypothesis -> code -> result -> decision)

**Deliverables by April 6:**
- Peptide Checker backend running locally with API endpoints serving vendor data
- Governance bus library with append/read/filter/replay, passing unit tests
- 7+ autoresearch experiments completed with GLA variants

### Week 3-4 (April 7 -- April 23): Product + Protocol

**Peptide Checker (50% of time):**
- [ ] Build minimal web frontend: vendor search, peptide info pages, regulatory status tracker
- [ ] Populate database with full Finnrick dataset (expand from 30 to 182+ vendors across 15 peptides)
- [ ] Add JMIR semaglutide study data and publicly available Janoshik results
- [ ] Build regulatory status page for all 19 Category 2 peptides (FDA + WADA + state)
- [ ] Implement storage calculator using degradation models from RQ-PEP-004

**HUMMBL Bus Protocol (40% of time):**
- [ ] Implement Supervisor agent: task decomposition from natural language spec into bounded subtasks
- [ ] Implement Worker agent: execute subtask, report result to bus
- [ ] Implement kill switch: CANCEL sentinel file + `system_halt` bus event
- [ ] Integration test: supervisor decomposes a research task into 3 subtasks, spawns 3 workers, collects results, synthesizes output -- all via bus

**Autoresearch (10% of time):**
- [ ] Continue overnight GLA experiments
- [ ] If GLA shows promise, begin Hymba-style hybrid experiments
- [ ] Test 57M-200M param configs on Nodezero (exploit 48GB)

**Deliverables by April 23:**
- Peptide Checker MVP feature-complete (vendor search, regulatory tracker, storage calculator)
- Supervisor-worker pipeline passing integration tests with bus coordination
- 15+ additional autoresearch experiments with architectural variants

### Month 1 Success Criteria

| Criterion | Target | How to Measure |
|-----------|--------|----------------|
| Peptide Checker MVP functional | All 5 core features working | Manual smoke test of each endpoint/page |
| Bus protocol stable | Zero data corruption in 100+ test operations | Unit test pass rate |
| Supervisor-worker round trip | End-to-end task completion via bus | Integration test passing |
| Autoresearch experiments | 20+ new experiments queued and completed | results.tsv row count |
| val_bpb improvement | Any improvement below 0.4646 | Best experiment result |

---

## 3. Month 2: Build (April 24 -- May 23)

### Week 5-6 (April 24 -- May 7): Verification + Routing

**Peptide Checker (40% of time):**
- [ ] Build COA upload interface (accept images and PDFs)
- [ ] Implement basic COA validation rules (red flags checklist from RQ-PEP-001)
- [ ] Cross-reference uploaded COA data against database averages
- [ ] Add COA Red Flags educational content
- [ ] User accounts and email-based authentication
- [ ] Soft launch preparation: deploy to Cloudflare, SSL, basic analytics

**HUMMBL Inference Layer (40% of time):**
- [ ] Implement heuristic router: task-type classification -> model selection (per Architecture Spec Section 3.2)
- [ ] Route simple queries to llama3.1:8b (local), code/analysis to Sonnet (API), architecture decisions to Opus (API)
- [ ] Implement exact-match cache (L1): hash-based, <1ms lookup
- [ ] Enable Anthropic prompt caching on all Claude API calls with static system prompts
- [ ] Set up LiteLLM as AI gateway for cost tracking
- [ ] Implement budget governors: hard cap at org level, soft caps per agent
- [ ] Log all routing decisions with confidence scores

**Autoresearch (20% of time):**
- [ ] Implement confidence-based cascading: extract log-probabilities from llama3.1:8b responses
- [ ] Begin calibrating escalation thresholds (start conservative at 0.70)
- [ ] Configure batch API for all non-interactive autoresearch queries (50% discount)
- [ ] Cross-dataset validation: run winning Desktop configs on Nodezero's climbmix dataset

**Deliverables by May 7:**
- COA verification tool functional with basic red-flag detection
- Heuristic routing operational, 60-70% of inference requests handled locally
- Exact-match cache reducing redundant API calls
- Cost tracking dashboard showing spend by feature/agent

### Week 7-8 (May 8 -- May 23): Launch Prep + NemoClaw

**Peptide Checker (40% of time):**
- [ ] Soft launch on Reddit r/Peptides with "State of the Peptide Market 2026" post
- [ ] Post in GLP-1 Forum, Iron Den, PeptideDeck
- [ ] Set up email newsletter for regulatory updates
- [ ] Create 5-10 short-form video scripts for TikTok/YouTube
- [ ] Reach out to 5 podcast hosts in biohacking/health optimization space
- [ ] Analyze initial user behavior: which peptides searched, which vendors, feature usage

**HUMMBL NemoClaw Integration (50% of time):**
- [ ] Wire NemoClaw spec into bus protocol: map READY/CANCEL sentinels to bus events
- [ ] Implement NemoClaw state machine on bus: IDLE -> QUEUED -> RUNNING -> EVALUATING -> ACCEPTED/REJECTED
- [ ] Implement val_bpb acceptance gate as deterministic bus event
- [ ] Circuit breaker: 3 consecutive identical failures -> QUARANTINED state
- [ ] Cross-machine coordination: Supervisor (Nodezero) writes experiment config to bus, Worker (Desktop) claims and executes
- [ ] Thermal kill switch: GPU temp > 85C -> automatic pause with bus event

**Autoresearch (10% of time):**
- [ ] First NemoClaw-orchestrated overnight run (if bus protocol is stable)
- [ ] Target: 5+ autonomous experiments in a single overnight session
- [ ] Morning review of bus audit trail to validate coordination

**Deliverables by May 23:**
- Peptide Checker live with real users and initial traffic data
- NemoClaw running on the HUMMBL bus, executing overnight experiments autonomously
- Bus protocol handling cross-machine supervisor-worker coordination

### Month 2 Success Criteria

| Criterion | Target | How to Measure |
|-----------|--------|----------------|
| Peptide Checker live | Deployed, accessible, receiving traffic | Analytics dashboard |
| COA uploads | 10+ uploads in first 2 weeks | Upload count |
| Heuristic routing | 60-70% local inference rate | Routing decision logs |
| API cost reduction | 50%+ vs. always-API baseline | LiteLLM cost tracking |
| NemoClaw on bus | End-to-end autonomous experiment | Bus event replay |
| Cross-machine coordination | Supervisor on Nodezero, Worker on Desktop | Bus audit trail |

---

## 4. Month 3: Launch (May 24 -- June 22)

### Week 9-10 (May 24 -- June 7): Iterate + Scale

**Peptide Checker (50% of time):**
- [ ] Analyze user behavior data from first 2-4 weeks
- [ ] Add user feedback mechanism (upvote/downvote vendor entries, submit corrections)
- [ ] Expand peptide coverage based on user demand (likely: PT-141, GHK-Cu, Selank, Semax)
- [ ] Begin Finnrick API integration for automated data updates (if API available)
- [ ] Draft vendor certification program structure ("Peptide Checker Verified" badge)
- [ ] Reach out to 3-5 testing labs about referral partnerships (Janoshik, Finnrick, Peptide Test, TruLab)

**HUMMBL Observability + Quality (40% of time):**
- [ ] Deploy Monitor agent: continuous health probes, GPU thermal monitoring, experiment stall detection
- [ ] Set up $0 observability stack: OpenTelemetry + Grafana Cloud free tier
- [ ] Implement SLO-based burn-rate alerting (fast burn: 14.4x rate -> page immediately; slow burn: ticket only)
- [ ] Implement semantic caching (L2): embedding-based similarity with 0.95 cosine threshold
- [ ] Add prompt compression via LLMLingua for long-context API calls
- [ ] Begin collecting routing decision data for future learned-router training

**Autoresearch (10% of time):**
- [ ] NemoClaw running nightly with increasing autonomy
- [ ] Target: 10+ experiments per overnight session
- [ ] Analyst agent prototype: cross-run pattern detection on accumulated experiment data

**Deliverables by June 7:**
- User feedback loop operational, database expanding based on real demand
- Monitor agent running continuously with SLO-based alerting
- Semantic caching operational with 15-20% hit rate target
- NemoClaw averaging 10+ overnight experiments

### Week 11-12 (June 8 -- June 22): Revenue + Decisions

**Peptide Checker (50% of time):**
- [ ] Implement Stripe billing integration
- [ ] Build subscription tier structure: Free (basic search) vs. Premium ($9.99/mo: alerts, unlimited COA scans, detailed vendor reports)
- [ ] Design and implement vendor alert system (email notifications on rating changes, new test data, regulatory actions)
- [ ] Publish first "Quarterly State of the Peptide Market" report
- [ ] Formalize testing lab referral partnerships (target: signed agreements with 2+ labs)
- [ ] Set 6-month goals based on 90 days of data

**HUMMBL Framework Polish (40% of time):**
- [ ] Capability token schema and issuance (supervisor -> worker delegation)
- [ ] Permission enforcement: agents only perform operations matching their token
- [ ] Audit trail validation tooling: replay and verify complete decision chains from bus
- [ ] Direct messaging mailbox for time-critical supervisor-worker coordination (per Architecture Spec Section 2.3)
- [ ] Code review pipeline prototype: Semgrep SAST + LLM post-filter for PR triage

**Autoresearch (10% of time):**
- [ ] Full week of autonomous NemoClaw operation
- [ ] Assess val_bpb trajectory: any breakthrough from GLA/hybrid experiments?
- [ ] Decision: continue current architecture search or pivot to longer time budgets / bigger models

**Deliverables by June 22:**
- Subscription billing live with at least 1 paid tier
- Testing lab referral partnerships signed
- Capability-based security model operational
- Full audit trail replay capability
- 90-day retrospective document written

### Month 3 Success Criteria

| Criterion | Target | How to Measure |
|-----------|--------|----------------|
| Unique monthly visitors | 5,000+ | Analytics |
| Email subscribers | 500+ | Newsletter platform |
| Paid subscribers | 10+ (proof of willingness to pay) | Stripe dashboard |
| Lab referral partnerships | 2+ signed | Signed agreements |
| Database coverage | 200+ vendors, 10+ peptides | Database query |
| COA uploads | 100+ total | Upload count |
| NemoClaw overnight runs | 10+ experiments/night, 5+ nights/week | Bus event count |
| API cost | <$500/month total | LiteLLM dashboard |
| Semantic cache hit rate | 15-20% | Cache metrics |
| Agent failure rate | <5% | Bus error event analysis |

---

## 5. Weekly Rhythm

### The Ideal Week

```
Monday     PLAN        Review weekend autoresearch results. Set 3-5 weekly goals.
                       Write task specs for the week. Phone (GPT-5.4) for spec design.

Tuesday    BUILD       Deep implementation work. Desktop (Claude Code) for HUMMBL/Peptide Checker.
                       Longest focused block of the week (aim for 5-6 hours).

Wednesday  BUILD       Continue implementation. Aider for pair programming on complex refactors.
                       Nodezero for larger model experiments if needed.

Thursday   SHIP        Integration testing. Deploy changes. Write content for Peptide Checker
                       (forum posts, research summaries, regulatory updates).

Friday     REVIEW      Review the week's autoresearch results. Update experiment queue.
                       Friday retrospective: what worked, what didn't, what to change.
                       Queue weekend overnight runs.

Saturday   OPTIONAL    Light review of overnight results. Content creation if energy allows.
                       Do not push hard -- protect against burnout.

Sunday     OFF         Full rest day. Do not check autoresearch results.
```

### Daily Cadence

1. **Morning (30 min):** Review overnight autoresearch results. Skim bus logs for anomalies. Check GPU thermals. Triage any alerts.
2. **Focus block (3-4 hours):** Deep work on the day's primary deliverable. No interruptions. No context switching between projects.
3. **Afternoon (1-2 hours):** Secondary tasks, communication, content creation, experiment queue management.
4. **Evening (15 min):** Queue overnight autoresearch runs. Verify NemoClaw state. Confirm thermal headroom.

### Machine Allocation

| Machine | Primary Use | When |
|---------|------------|------|
| **Desktop (RTX 3080 Ti)** | CUDA training, local inference (llama3.1:8b), Peptide Checker development, HUMMBL bus implementation | Daytime: development. Overnight: autoresearch training. |
| **Nodezero (M4 Pro, 48GB)** | NemoClaw supervisor, larger model inference (up to ~30B quantized), MLX experiments | Daytime: supervisor orchestration. Overnight: experiment coordination. |
| **Phone (GPT-5.4)** | Spec design, strategic thinking, task decomposition, morning review | Commute, walking, low-energy periods. Idea capture. |
| **API (Claude Sonnet/Opus)** | Code generation, PR review, complex analysis, research synthesis | During focused work sessions. Batch API for non-interactive. |

### Autoresearch Overnight Protocol

1. **Before bed:** Verify experiment queue has 5-10 configs ready. Check GPU temp is <65C at idle. Confirm NemoClaw state is IDLE.
2. **NemoClaw runs:** Supervisor on Nodezero coordinates. Worker on Desktop executes training. Bus logs everything.
3. **Morning review:** Check bus for ACCEPTED/REJECTED events. Review any FAILED events with ARNC codes. Check thermal log for any throttle events.
4. **Decision:** If new best val_bpb, update baseline. If circuit breaker activated, diagnose and adjust before next run.

---

## 6. Decision Points

### Week 4 Gate: Peptide Checker MVP Ready?

**Question:** Is the MVP ready for beta testers?

**Go criteria (all must be true):**
- [ ] Vendor search returns accurate results for BPC-157 and semaglutide
- [ ] Regulatory tracker shows current FDA status for all 19 Category 2 peptides
- [ ] Storage calculator produces reasonable degradation estimates
- [ ] No critical bugs in 48 hours of testing
- [ ] Terms of Service and Disclaimer reviewed by attorney

**If NO:** Extend MVP development by 1 week. Reduce HUMMBL bus work to 20% to reallocate. Do not skip legal review.

**If YES:** Proceed to COA verification in Month 2. Begin soft launch planning.

### Week 8 Gate: HUMMBL Bus Protocol Stable?

**Question:** Is the bus protocol stable enough for NemoClaw overnight runs?

**Go criteria (all must be true):**
- [ ] Zero data corruption in 500+ bus operations
- [ ] Supervisor-worker round trip completes reliably across machines (Desktop <-> Nodezero)
- [ ] Kill switch halts all workers within 5 seconds
- [ ] Circuit breaker activates correctly on 3 consecutive failures
- [ ] Bus replay reconstructs the complete decision chain for any task

**If NO:** NemoClaw integration slips to Month 3. Continue manual overnight experiments. Focus Month 3 HUMMBL time on bus stability instead of security model.

**If YES:** Begin NemoClaw overnight runs. Target 5+ autonomous experiments per night.

### Week 12 Gate: Revenue or Pivot?

**Question:** Is there evidence of willingness to pay?

**Evaluate these signals:**
- **Strong signal (proceed to Phase 2):** 10+ paid subscribers, 2+ lab referral partnerships signed, 5,000+ monthly visitors, organic Reddit/forum mentions
- **Moderate signal (continue but adjust):** Traffic growing but <5,000/month, 1-5 paid subscribers, 1 lab partnership. Adjust: double down on content marketing and community presence. Extend Phase 1 free period.
- **Weak signal (pivot):** <1,000 monthly visitors, 0 paid subscribers, no lab interest. Pivot options:
  - A: Narrow focus to GLP-1 only (largest audience, clearest pain point)
  - B: Pivot to B2B (compounding pharmacy verification instead of consumer-facing)
  - C: Pause Peptide Checker, redirect all time to HUMMBL framework as an open-source developer tool

**The decision framework:** Revenue is the forcing function. Without evidence of willingness to pay by Week 12, the Peptide Checker business model needs revision -- not necessarily abandonment, but revision. The 90-day data determines the next 90-day plan.

---

## 7. Risk Mitigation

### Risk 1: FDA Reclassification Changes the Peptide Market

**Probability:** Moderate (20-30% of meaningful change within 90 days)
**Impact:** Could shift demand from gray-market verification to legitimate compounding pharmacy evaluation

**Mitigation:**
- Build the regulatory tracker as a first-class feature -- become the authoritative source on what has *actually* changed vs. what has been announced
- Design the database schema to accommodate compounding pharmacy entries (not just gray-market vendors)
- If Category 1 reclassification happens during the 90 days: this is a *tailwind*, not a headwind. Pivot messaging from "is this real?" to "is this pharmacy trustworthy?"
- The verification value proposition is stronger, not weaker, in a regulated market

### Risk 2: val_bpb Plateau Does Not Break

**Probability:** High (60-70%). 110+ experiments have already explored the obvious hyperparameter space.
**Impact:** Autoresearch demonstrates diminishing returns; HUMMBL reasoning framework lacks a showcase breakthrough

**Mitigation:**
- GLA and Hymba-style hybrid architectures are the next frontier -- genuinely different from what has been tried
- Test bigger models on Nodezero (57M-200M params with 48GB). The step-count disadvantage may reverse at larger scale.
- Longer time budgets (10-15 min instead of 5 min) may unlock improvements that are inaccessible at current budget
- If plateau persists after 30+ new experiments: the val_bpb number is not the product. The *process* (autonomous experimentation with structured reasoning) is the product. Pivot HUMMBL narrative from "we beat the benchmark" to "we built the system that runs 1,000 experiments autonomously"
- Cross-dataset validation (TinyStories wins validated on climbmix) matters more than absolute number

### Risk 3: Solo Founder Bandwidth is the Bottleneck

**Probability:** High (80%+). This is the most likely risk to materialize.
**Impact:** Features ship late, quality suffers, burnout risk

**Mitigation:**
- **Ruthless prioritization:** If bandwidth is tight, Peptide Checker ships first. HUMMBL bus work pauses before Peptide Checker does. Revenue > infrastructure.
- **AI leverage is the multiplier:** Every task should be evaluated for AI delegation. Claude Code for implementation, batch API for research, NemoClaw for overnight experiments. The goal is 3-5x effective output through AI assistance.
- **Burnout indicators to watch:** Dreading Monday mornings. Skipping morning autoresearch review for 3+ days. Working Sundays. Shipping without testing. Ignoring bus error logs.
- **Circuit breaker for the human:** If 2+ burnout indicators persist for a week, take 3 full days off. No exceptions. A week of recovery is cheaper than a month of diminished output.
- **When to hire/contract:** NOT in this 90 days unless revenue from Peptide Checker exceeds $2,000/month by Week 10. The only exception: a one-time contract ($500-1,500) for web design/frontend if the Peptide Checker UI is blocking user adoption.
- **Dan Matha:** Peptide Checker is under Founder Mode. If Dan can contribute to content marketing, community management, or partnership outreach, delegate those tasks. Reuben's time is best spent on engineering and technical strategy.

### Risk 4: Thermal Shutdowns During Overnight Runs

**Probability:** Low-Moderate (15-20%, given 270W cap and documented history)
**Impact:** Lost overnight experiment time, potential data corruption if shutdown is ungraceful

**Mitigation:**
- 270W power cap is non-negotiable. Already validated at 52-68C sustained.
- 85C thermal kill switch in NemoClaw spec. Implemented as bus event, not just process kill.
- Do NOT run games on Desktop while overnight experiments are queued. (Per memory: Nancy Drew, Ghost Master are on this machine.)
- Monitor agent checks GPU temp every 60 seconds via nvidia-smi.
- If thermal shutdown occurs: NemoClaw state machine handles it via FAILED state with ARNC code. Experiment resumes from last checkpoint on next cycle.

### Risk 5: Protocol/Framework Churn

**Probability:** High (certainty over 90 days -- something will change in the AI landscape)
**Impact:** Architectural decisions may need revision

**Mitigation:**
- The bus abstraction layer is thin by design. JSONL files, not a database. If MCP evolves or A2A becomes relevant, the protocol layer can be swapped without rewriting agents.
- "Compose, don't commit" principle (per RQ-009): use direct API calls + lightweight orchestration. No deep framework dependency.
- Monitor A2A protocol development (Linux Foundation, v0.3). Do not adopt until v1.0 or clear ecosystem convergence.

---

## 8. Resource Allocation

### Time Allocation by Month

| Project | Month 1 | Month 2 | Month 3 |
|---------|---------|---------|---------|
| **Peptide Checker** | 55% | 40% | 50% |
| **HUMMBL Framework** | 35% | 40% | 40% |
| **Autoresearch** | 10% | 20% | 10% |

**Rationale:** Peptide Checker gets the plurality of time because it is the revenue path. Month 2 shifts toward HUMMBL as the bus protocol needs integration testing with NemoClaw. Month 3 returns focus to Peptide Checker for launch and revenue validation. Autoresearch is always 10-20% because it runs overnight -- the time allocation is for *reviewing* results and *queuing* experiments, not sitting and watching training runs.

### Budget Allocation

| Category | Monthly Budget | Notes |
|----------|---------------|-------|
| Claude API (Sonnet + Opus) | $200-500 | Prompt caching + routing reduces this significantly |
| Batch API | $50-150 | Non-interactive autoresearch and content generation |
| Local inference (electricity) | $3-5 | RTX 3080 Ti at 270W, ~$0.04/hr |
| Peptide Checker hosting | $0-50 | Cloudflare Workers free/starter tier |
| Domain + legal | $200-600 | One-time in Month 1 |
| Testing samples | $100-300 | Purchase peptide samples for content/validation |
| Contingency | $200 | Unexpected costs |
| **Monthly total** | **$350-700** | Rising to ~$960 if all features active |

### When to Contract Help

**Within 90 days -- only if these conditions are met:**
- Frontend design is blocking user adoption (users bounce because the UI is confusing) AND Peptide Checker has 1,000+ monthly visitors --> Contract a UI/UX designer ($500-1,500 one-time)
- Legal review is blocking launch --> Attorney for ToS/Privacy/Disclaimer ($1,000-3,000 one-time)

**NOT within 90 days:**
- Do not hire a developer. The codebase is too early and too fluid for someone else to contribute effectively. AI leverage is the better multiplier at this stage.
- Do not contract content writers. Reuben's domain expertise is the differentiator. AI assists with drafting, Reuben provides judgment and credibility.

### AI Agent Utilization Strategy

| Agent Type | Tool | Use For | Estimated Time Savings |
|-----------|------|---------|----------------------|
| **Implementation** | Claude Code (Desktop) | HUMMBL bus, Peptide Checker backend, NemoClaw integration | 3-5x vs. manual coding |
| **Pair programming** | Aider | Refactoring existing code, exploring unfamiliar codebases | 2-3x on refactoring tasks |
| **Spec design** | GPT-5.4 (Phone) | Task decomposition, feature specs, strategic thinking | Captures ideas during low-energy periods |
| **Research** | Claude Batch API | Autoresearch queries, competitive analysis, regulatory monitoring | 50% cost savings, async processing |
| **Overnight ML** | NemoClaw (Desktop + Nodezero) | Autonomous experiment execution | Turns 0 human hours into 8+ experiment hours |
| **Content** | Claude + domain expertise | Research reports, forum posts, newsletter drafts | 2-3x on writing tasks |
| **Code review** | Semgrep + LLM post-filter (future) | PR triage, vulnerability detection | Reduces manual review by 60-80% |

**The leverage equation:** A solo founder with AI agents working overnight on two machines has the effective output of a 3-5 person team for engineering and research tasks. The bottleneck is not execution capacity -- it is *decision quality* and *prioritization*. Invest human time in thinking, reviewing, and deciding. Delegate execution to agents.

---

## 9. Metrics to Track

### Peptide Checker Metrics

| Metric | Week 4 | Week 8 | Week 12 | How to Measure |
|--------|--------|--------|---------|----------------|
| Unique monthly visitors | -- | 1,000 | 5,000 | Cloudflare Analytics |
| Database vendors | 100+ | 150+ | 200+ | `SELECT COUNT(*) FROM vendors` |
| Database peptides | 5 | 8 | 10+ | `SELECT COUNT(DISTINCT peptide) FROM vendors` |
| COA uploads | -- | 10+ | 100+ | Upload event count |
| Email subscribers | -- | 100 | 500+ | Newsletter platform |
| Reddit/forum mentions | -- | 5+ | 20+ | Manual tracking + alerts |
| Paid subscribers | -- | -- | 10+ | Stripe dashboard |
| Lab referral partnerships | -- | -- | 2+ | Signed agreements |
| Revenue | $0 | $0 | $0-500 | Stripe + referral commissions |

### HUMMBL Metrics

| Metric | Week 4 | Week 8 | Week 12 | How to Measure |
|--------|--------|--------|---------|----------------|
| Bus operations (total) | 500+ | 5,000+ | 20,000+ | Bus JSONL line count |
| Bus corruption events | 0 | 0 | 0 | Checksum validation |
| Supervisor-worker round trips | 10+ | 100+ | 500+ | Bus event type filter |
| Agent failure rate | <10% | <5% | <5% | Bus error events / total events |
| Local inference rate | -- | 60-70% | 70-80% | Routing decision logs |
| API cost / month | -- | <$500 | <$500 | LiteLLM dashboard |
| Cache hit rate (L1) | -- | 5-10% | 10-15% | Cache metrics |
| Cache hit rate (L2 semantic) | -- | -- | 15-20% | Cache metrics |
| NemoClaw experiments/night | -- | 5+ | 10+ | Bus event count per overnight session |

### Autoresearch Metrics

| Metric | Week 4 | Week 8 | Week 12 | How to Measure |
|--------|--------|--------|---------|----------------|
| Total experiments (Desktop) | 130+ | 160+ | 200+ | results.tsv row count |
| Best val_bpb (Desktop) | <0.4646 (aspirational) | -- | -- | Best experiment result |
| Total experiments (Nodezero) | 40+ | 55+ | 70+ | results.tsv row count |
| Best val_bpb (Nodezero) | <1.488 | -- | -- | Best experiment result |
| Architectural variants tested | GLA, 2+ hybrids | 5+ variants | 8+ variants | Experiment config diversity |
| Cross-dataset validations | 0 | 3+ | 5+ | Configs tested on both datasets |
| Reasoning traces captured | 20+ | 60+ | 100+ | Structured trace file count |

### Personal / Founder Health Metrics

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Weekly focused hours | 20-30 | 15-20 | <15 or >36 |
| Days off per week | 1-2 | 0.5 | 0 for 2+ weeks |
| Morning autoresearch review | Daily | 4-5x/week | Skipped 3+ days |
| Sunday work | None | Light review only | Full work day |
| Excitement about Monday | High | Neutral | Dreading it |
| Shipping without testing | Never | Occasional | Regular |
| Ignoring bus error logs | Never | Occasional | "I'll check tomorrow" |

**If Red on 2+ indicators for 1 week:** Take 3 full days off. Reassess prioritization. Consider reducing scope.

---

## 10. 90-Day Summary View

```
MARCH 24          APRIL 24          MAY 24           JUNE 22
|--- FOUNDATION ---|---- BUILD ------|---- LAUNCH -----|
|                  |                  |                 |
| PC: Backend      | PC: COA verify   | PC: Iterate     |
| PC: Frontend     | PC: Soft launch  | PC: Subscriptions|
| PC: Database     | PC: Content push | PC: Lab partners |
|                  |                  |                 |
| Bus: Schema      | Bus: Routing     | Bus: Security   |
| Bus: Agent loop  | Bus: Caching     | Bus: Observability|
| Bus: Sup-Worker  | Bus: NemoClaw    | Bus: Mailbox    |
|                  |                  |                 |
| AR: GLA exps     | AR: Cascade test | AR: Autonomous  |
| AR: Traces       | AR: Cross-data   | AR: Full NemoClaw|
|                  |                  |                 |
| GATE: MVP ready? | GATE: Bus stable?| GATE: Revenue?  |
```

**The North Star:** By June 22, 2026, Peptide Checker has paying users, HUMMBL's bus protocol runs NemoClaw overnight autonomously, and the autoresearch pipeline has tested 100+ new architectural variants. Three products, one pipeline, one founder with AI leverage.

---

*Roadmap generated 2026-03-23 | Next review: 2026-04-07 (Week 2 checkpoint)*
*This is a living document. Update weekly during Friday retrospectives.*
