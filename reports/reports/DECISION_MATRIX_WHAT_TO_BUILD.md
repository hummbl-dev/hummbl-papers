# Decision Matrix: What to Build First

**Date:** 2026-03-23
**Author:** Reuben Bowlby + Claude Strategic Synthesis
**Status:** Active Decision Document
**Sources:** Peptide Checker Business Plan, HUMMBL Architecture Spec v1.0, HUMMBL 90-Day Roadmap, NemoClaw Implementation Guide, ThinkPRM Implementation Guide, AI-Native Solo Founder Models Report, Local vs API Cost Analysis, Project Goals, Last Economy Analysis

---

## 1. All Candidate Projects/Features

Every buildable thing identified across all reports, organized by parent project:

### Peptide Checker (Revenue Path)

| # | Feature | Source | Current State |
|---|---------|--------|---------------|
| P1 | **Vendor quality database (web)** | Business Plan Phase 1 | peptide_db.py exists with 30 vendors, 2 peptides; needs web API + frontend + DB migration |
| P2 | **COA verification tool** | Business Plan Phase 1 | Not started; requires OCR pipeline + red-flag rule engine |
| P3 | **Regulatory status tracker** | Business Plan Phase 1 | Not started; needs scraping/manual tracking of FDA, WADA, state AG sources |
| P4 | **Storage calculator** | Business Plan Phase 1 | Not started; degradation models available from RQ-PEP-004 data |
| P5 | **Consumer education hub** | Business Plan Phase 1 | consumer_guide.md exists for 5 peptides; needs web conversion |
| P6 | **Subscription billing (Stripe)** | Business Plan Phase 2 | Not started; depends on P1 being live |
| P7 | **Vendor certification program** | Business Plan Phase 3 | Not started; depends on traffic + lab partnerships |
| P8 | **Testing lab referral partnerships** | Business Plan Phase 3 | No outreach yet; Janoshik, Finnrick, Peptide Test, TruLab identified |
| P9 | **AI COA document analyzer (ML)** | Business Plan Phase 2 | Not started; OCR + ML classification |
| P10 | **Community batch testing program** | Business Plan Phase 3 | Not started; depends on audience |

### HUMMBL Framework (Strategic Positioning)

| # | Feature | Source | Current State |
|---|---------|--------|---------------|
| H1 | **Governance bus protocol** | Architecture Spec Phase 1 | Not started; append-only JSONL writer/reader with schema validation |
| H2 | **Supervisor agent** | Architecture Spec Phase 1 | Not started; task decomposition + worker spawning |
| H3 | **Worker agent** | Architecture Spec Phase 1 | Not started; subtask execution + bus reporting |
| H4 | **Heuristic inference router** | Architecture Spec Phase 2 | Not started; task-type -> model selection rules |
| H5 | **Confidence-based cascading** | Architecture Spec Phase 2 | Not started; log-prob extraction + escalation thresholds |
| H6 | **Exact-match cache (L1)** | Architecture Spec Phase 2 | Not started; hash-based cache |
| H7 | **Semantic cache (L2)** | Architecture Spec Phase 4 | Not started; embedding similarity cache |
| H8 | **Capability-based security model** | Architecture Spec Phase 3 | Not started; delegation tokens, permission enforcement |
| H9 | **Open source HUMMBL release** | Solo Founder Report | Not started; requires stable bus + docs + GitHub packaging |
| H10 | **Code review pipeline (Semgrep + LLM)** | Architecture Spec Phase 4 | Not started |

### NemoClaw (Autonomous ML Pipeline)

| # | Feature | Source | Current State |
|---|---------|--------|---------------|
| N1 | **Core data models (Pydantic schemas)** | Implementation Guide Phase 1 | Not started; shared models package |
| N2 | **Worker module (queue scanner + executor)** | Implementation Guide Phase 2 | Not started; polls queue, executes train.py |
| N3 | **Supervisor module (experiment generator)** | Implementation Guide Phase 3 | Not started; generates specs, evaluates results |
| N4 | **Cross-machine coordination** | Implementation Guide Phase 3 | Not started; Nodezero supervisor + Desktop worker over LAN |
| N5 | **Circuit breaker + failure codes** | Implementation Guide Phase 2 | Not started; ARNC-001 through ARNC-022 |

### Reasoning / Verification

| # | Feature | Source | Current State |
|---|---------|--------|---------------|
| R1 | **Reasoning trace format** | Project Goals (Goal 5) | REASONING_TRACE_FORMAT_SPEC.md exists; capture not yet automated |
| R2 | **ThinkPRM prompted verifier** | ThinkPRM Guide Phase 1 | Not started; prompt-only PRM using frontier models |
| R3 | **ThinkPRM fine-tuned verifier** | ThinkPRM Guide Phase 2 | Not started; fine-tune 1.5B model on synthetic verification CoTs |

### Autoresearch Experiments

| # | Feature | Source | Current State |
|---|---------|--------|---------------|
| A1 | **GLA (Gated Linear Attention) experiments** | Project Goals (Goal 1) | Queued; next architectural frontier |
| A2 | **Hymba-style hybrid architecture experiments** | Project Goals (Goal 1) | Not started; depends on GLA results |
| A3 | **Big model configs (57M-200M) on Nodezero** | Project Goals (Goal 2) | big_model_configs.md exists; not run |
| A4 | **Cross-dataset validation pipeline** | Project Goals (Goal 3) | cross_pollinate.py exists; not automated |

### AI Stack Improvements

| # | Feature | Source | Current State |
|---|---------|--------|---------------|
| S1 | **KV cache migration to q4_0** | Memory (kv_cache) | Validated but not yet production; +44% speed |
| S2 | **Vision model replacement** | Memory (golden_ratio_stack) | moondream in stack; may need upgrade |
| S3 | **LiteLLM gateway setup** | Architecture Spec Phase 2 | Not started; cost tracking + multi-backend routing |

---

## 2. Scoring Criteria

Each project scored 1-5 on six dimensions:

| Criterion | Weight | Definition |
|-----------|--------|------------|
| **Revenue potential** | **3.0x** | Does this make money in the next 6 months? (Per Last Economy: revenue now) |
| **Time to value** | **2.0x** | How fast can it ship and deliver value? (1 = months, 5 = days) |
| **Strategic positioning** | **1.5x** | Does this build a moat, brand, or compounding advantage? |
| **Technical risk (inverted)** | **1.0x** | How likely to succeed? (5 = very likely, 1 = likely to fail) |
| **Dependency** | **1.5x** | Does other stuff depend on this being done? |
| **Solo founder feasibility** | **2.0x** | Can one person do this in the time available? |

**Total weight: 11.0x** (composite score out of 55 max)

Revenue weighted highest per the Last Economy analysis: "Revenue now, position later." Time to value and solo feasibility weighted second because the bottleneck is one person's bandwidth.

---

## 3. Weighted Score Matrix

### Peptide Checker Features

| # | Feature | Rev (3x) | Time (2x) | Strat (1.5x) | Risk-inv (1x) | Dep (1.5x) | Solo (2x) | **Composite** |
|---|---------|----------|-----------|---------------|----------------|------------|-----------|---------------|
| P1 | Vendor database (web) | 4 (12) | 4 (8) | 5 (7.5) | 4 (4) | 5 (7.5) | 5 (10) | **49.0** |
| P3 | Regulatory tracker | 3 (9) | 4 (8) | 5 (7.5) | 5 (5) | 3 (4.5) | 5 (10) | **44.0** |
| P5 | Consumer education hub | 3 (9) | 5 (10) | 4 (6) | 5 (5) | 3 (4.5) | 5 (10) | **44.5** |
| P4 | Storage calculator | 2 (6) | 5 (10) | 3 (4.5) | 5 (5) | 2 (3) | 5 (10) | **38.5** |
| P2 | COA verification tool | 4 (12) | 3 (6) | 5 (7.5) | 3 (3) | 3 (4.5) | 4 (8) | **41.0** |
| P8 | Lab referral partnerships | 5 (15) | 3 (6) | 4 (6) | 3 (3) | 2 (3) | 4 (8) | **41.0** |
| P6 | Subscription billing | 5 (15) | 4 (8) | 3 (4.5) | 4 (4) | 2 (3) | 5 (10) | **44.5** |
| P7 | Vendor certification | 5 (15) | 2 (4) | 5 (7.5) | 3 (3) | 1 (1.5) | 3 (6) | **37.0** |
| P9 | AI COA analyzer (ML) | 3 (9) | 2 (4) | 4 (6) | 2 (2) | 2 (3) | 3 (6) | **30.0** |
| P10 | Community batch testing | 3 (9) | 1 (2) | 4 (6) | 2 (2) | 1 (1.5) | 2 (4) | **24.5** |

### HUMMBL Features

| # | Feature | Rev (3x) | Time (2x) | Strat (1.5x) | Risk-inv (1x) | Dep (1.5x) | Solo (2x) | **Composite** |
|---|---------|----------|-----------|---------------|----------------|------------|-----------|---------------|
| H1 | Governance bus protocol | 1 (3) | 3 (6) | 5 (7.5) | 4 (4) | 5 (7.5) | 4 (8) | **36.0** |
| H2 | Supervisor agent | 1 (3) | 3 (6) | 4 (6) | 3 (3) | 4 (6) | 4 (8) | **32.0** |
| H3 | Worker agent | 1 (3) | 3 (6) | 4 (6) | 3 (3) | 4 (6) | 4 (8) | **32.0** |
| H4 | Heuristic inference router | 2 (6) | 4 (8) | 4 (6) | 4 (4) | 3 (4.5) | 5 (10) | **38.5** |
| H6 | Exact-match cache (L1) | 2 (6) | 5 (10) | 3 (4.5) | 5 (5) | 2 (3) | 5 (10) | **38.5** |
| H5 | Confidence cascading | 1 (3) | 3 (6) | 4 (6) | 3 (3) | 2 (3) | 4 (8) | **29.0** |
| H7 | Semantic cache (L2) | 1 (3) | 2 (4) | 3 (4.5) | 3 (3) | 1 (1.5) | 3 (6) | **22.0** |
| H8 | Capability security | 1 (3) | 2 (4) | 4 (6) | 3 (3) | 2 (3) | 3 (6) | **25.0** |
| H9 | Open source release | 2 (6) | 1 (2) | 5 (7.5) | 3 (3) | 1 (1.5) | 2 (4) | **24.0** |
| H10 | Code review pipeline | 1 (3) | 2 (4) | 3 (4.5) | 3 (3) | 1 (1.5) | 3 (6) | **22.0** |

### NemoClaw Features

| # | Feature | Rev (3x) | Time (2x) | Strat (1.5x) | Risk-inv (1x) | Dep (1.5x) | Solo (2x) | **Composite** |
|---|---------|----------|-----------|---------------|----------------|------------|-----------|---------------|
| N1 | Core data models | 1 (3) | 4 (8) | 3 (4.5) | 5 (5) | 5 (7.5) | 5 (10) | **38.0** |
| N2 | Worker module | 1 (3) | 3 (6) | 4 (6) | 4 (4) | 4 (6) | 4 (8) | **33.0** |
| N3 | Supervisor module | 1 (3) | 2 (4) | 4 (6) | 3 (3) | 3 (4.5) | 3 (6) | **26.5** |
| N4 | Cross-machine coordination | 1 (3) | 2 (4) | 4 (6) | 2 (2) | 3 (4.5) | 3 (6) | **25.5** |
| N5 | Circuit breaker | 1 (3) | 4 (8) | 3 (4.5) | 4 (4) | 3 (4.5) | 5 (10) | **34.0** |

### Reasoning / Verification

| # | Feature | Rev (3x) | Time (2x) | Strat (1.5x) | Risk-inv (1x) | Dep (1.5x) | Solo (2x) | **Composite** |
|---|---------|----------|-----------|---------------|----------------|------------|-----------|---------------|
| R1 | Reasoning trace format | 1 (3) | 4 (8) | 4 (6) | 4 (4) | 3 (4.5) | 5 (10) | **35.5** |
| R2 | ThinkPRM prompted | 1 (3) | 3 (6) | 4 (6) | 3 (3) | 2 (3) | 4 (8) | **29.0** |
| R3 | ThinkPRM fine-tuned | 1 (3) | 1 (2) | 5 (7.5) | 2 (2) | 1 (1.5) | 2 (4) | **20.0** |

### Autoresearch Experiments

| # | Feature | Rev (3x) | Time (2x) | Strat (1.5x) | Risk-inv (1x) | Dep (1.5x) | Solo (2x) | **Composite** |
|---|---------|----------|-----------|---------------|----------------|------------|-----------|---------------|
| A1 | GLA experiments | 1 (3) | 4 (8) | 4 (6) | 3 (3) | 3 (4.5) | 5 (10) | **34.5** |
| A4 | Cross-dataset validation | 1 (3) | 3 (6) | 3 (4.5) | 4 (4) | 2 (3) | 5 (10) | **30.5** |
| A3 | Big model configs (Nodezero) | 1 (3) | 3 (6) | 3 (4.5) | 3 (3) | 1 (1.5) | 4 (8) | **26.0** |
| A2 | Hymba hybrid experiments | 1 (3) | 2 (4) | 4 (6) | 2 (2) | 1 (1.5) | 4 (8) | **24.5** |

### AI Stack Improvements

| # | Feature | Rev (3x) | Time (2x) | Strat (1.5x) | Risk-inv (1x) | Dep (1.5x) | Solo (2x) | **Composite** |
|---|---------|----------|-----------|---------------|----------------|------------|-----------|---------------|
| S1 | KV cache q4_0 migration | 1 (3) | 5 (10) | 2 (3) | 5 (5) | 2 (3) | 5 (10) | **34.0** |
| S3 | LiteLLM gateway | 2 (6) | 4 (8) | 3 (4.5) | 4 (4) | 3 (4.5) | 5 (10) | **37.0** |
| S2 | Vision model replacement | 1 (3) | 3 (6) | 2 (3) | 4 (4) | 1 (1.5) | 5 (10) | **27.5** |

---

## 4. Ranked Results

| Rank | ID | Feature | Composite | Category |
|------|----|---------|-----------|----------|
| **1** | P1 | **Vendor quality database (web)** | **49.0** | Peptide Checker |
| 2 | P5 | Consumer education hub | 44.5 | Peptide Checker |
| 3 | P6 | Subscription billing (Stripe) | 44.5 | Peptide Checker |
| 4 | P3 | Regulatory status tracker | 44.0 | Peptide Checker |
| 5 | P2 | COA verification tool | 41.0 | Peptide Checker |
| 6 | P8 | Lab referral partnerships | 41.0 | Peptide Checker |
| 7 | H4 | Heuristic inference router | 38.5 | HUMMBL |
| 8 | H6 | Exact-match cache (L1) | 38.5 | HUMMBL |
| 9 | P4 | Storage calculator | 38.5 | Peptide Checker |
| 10 | N1 | NemoClaw core data models | 38.0 | NemoClaw |
| 11 | S3 | LiteLLM gateway | 37.0 | AI Stack |
| 12 | P7 | Vendor certification program | 37.0 | Peptide Checker |
| 13 | H1 | Governance bus protocol | 36.0 | HUMMBL |
| 14 | R1 | Reasoning trace format | 35.5 | Reasoning |
| 15 | A1 | GLA experiments | 34.5 | Autoresearch |
| 16 | N5 | Circuit breaker | 34.0 | NemoClaw |
| 17 | S1 | KV cache q4_0 migration | 34.0 | AI Stack |
| 18 | N2 | Worker module | 33.0 | NemoClaw |
| 19 | H2 | Supervisor agent | 32.0 | HUMMBL |
| 20 | H3 | Worker agent | 32.0 | HUMMBL |
| 21 | A4 | Cross-dataset validation | 30.5 | Autoresearch |
| 22 | P9 | AI COA analyzer (ML) | 30.0 | Peptide Checker |
| 23 | H5 | Confidence cascading | 29.0 | HUMMBL |
| 24 | R2 | ThinkPRM prompted | 29.0 | Reasoning |
| 25 | S2 | Vision model replacement | 27.5 | AI Stack |
| 26 | N3 | Supervisor module | 26.5 | NemoClaw |
| 27 | A3 | Big model configs (Nodezero) | 26.0 | Autoresearch |
| 28 | H8 | Capability security model | 25.0 | HUMMBL |
| 29 | N4 | Cross-machine coordination | 25.5 | NemoClaw |
| 30 | P10 | Community batch testing | 24.5 | Peptide Checker |
| 31 | A2 | Hymba hybrid experiments | 24.5 | Autoresearch |
| 32 | H9 | Open source HUMMBL release | 24.0 | HUMMBL |
| 33 | H7 | Semantic cache (L2) | 22.0 | HUMMBL |
| 34 | H10 | Code review pipeline | 22.0 | HUMMBL |
| 35 | R3 | ThinkPRM fine-tuned | 20.0 | Reasoning |

---

## 5. Recommended Build Order

### Phase A: Weeks 1-4 -- "Ship the Revenue Product"

**Primary track (60% of daytime hours): Peptide Checker MVP**

```
P1 (Vendor database web)          Weeks 1-2: FastAPI + frontend + DB migration
  |
  +-- P3 (Regulatory tracker)     Week 2-3: Add to the same web app
  |
  +-- P5 (Education hub)          Week 2-3: Convert consumer_guide.md to web pages
  |
  +-- P4 (Storage calculator)     Week 3-4: Add as a tool page
  |
  v
P2 (COA verification)             Week 4-5: Upload + red-flag rules (basic, no ML)
```

**Secondary track (30% of daytime hours): HUMMBL Foundation**

```
H1 (Governance bus protocol)      Weeks 1-3: JSONL writer/reader + schema + unit tests
  |
  +-- N1 (NemoClaw data models)   Week 2: Pydantic schemas (shared with bus)
  |
  v
H2 + H3 (Supervisor + Worker)    Weeks 3-4: Basic agent loop on bus
```

**Overnight track (automated, 0% active daytime): Autoresearch**

```
A1 (GLA experiments)              Queue nightly starting Week 1
S1 (KV cache q4_0 migration)     One-time change, Week 1 (15 minutes)
R1 (Reasoning trace format)       Begin capturing traces from GLA experiments
```

### Phase B: Weeks 5-8 -- "Launch + Integrate"

**Primary track (40%): Peptide Checker Launch + Revenue Prep**

```
Soft launch on Reddit r/Peptides                      Week 5
P8 (Lab referral partnership outreach)                 Weeks 5-6
P6 (Stripe subscription billing)                       Weeks 7-8
Content marketing push (forum posts, newsletter)       Ongoing
```

**Secondary track (40%): HUMMBL Inference + NemoClaw**

```
H4 (Heuristic inference router)    Week 5-6
H6 (Exact-match cache L1)         Week 5 (quick win, ship alongside router)
S3 (LiteLLM gateway)              Week 6 (cost tracking)
N2 (Worker module)                 Week 7 (wire to bus protocol)
N5 (Circuit breaker)              Week 7 (ship with worker)
```

**Overnight track:**

```
A1/A2 (Continue GLA, begin Hymba if GLA shows promise)
A4 (Cross-dataset validation on any wins)
```

### Phase C: Weeks 9-12 -- "Validate + Decide"

**Primary track (50%): Peptide Checker Revenue Validation**

```
Analyze user data, iterate on what users actually use
P7 (Vendor certification program design)              If traffic > 5,000/mo
P8 (Formalize lab referral agreements)                 If initial outreach positive
```

**Secondary track (40%): NemoClaw Autonomous Operation**

```
N3 (Supervisor module)                                 Week 9-10
N4 (Cross-machine coordination)                        Week 11-12
First fully autonomous overnight NemoClaw run          Week 12 target
```

**Parking lot evaluation (Week 12):**

Review all "Phase D and beyond" items against actual revenue and traction data.

### Dependency Map

```
                    S1 (KV cache) ---- immediate, no deps

P1 (Vendor DB) --> P3 (Regulatory) --> P5 (Education) --> P2 (COA)
      |                                                        |
      +---> P6 (Billing) ---> P7 (Certification)              |
      |                                                        |
      +---> P8 (Lab referrals) <-------------------------------+

H1 (Bus) --> H2/H3 (Agents) --> H4 (Router) --> H5 (Cascade)
  |                  |
  +-- N1 (Models) ---+---> N2 (Worker) --> N3 (Supervisor) --> N4 (Cross-machine)
                           |
                           +-- N5 (Circuit breaker)

A1 (GLA) --> A2 (Hymba)      [overnight, parallel to everything]
A4 (Cross-validation)        [after any wins]
R1 (Traces) --> R2 (ThinkPRM prompted) --> R3 (ThinkPRM fine-tuned)
```

### Parallel Execution Strategy

| Time Block | Machine | Activity |
|-----------|---------|----------|
| **Morning (30 min)** | Desktop | Review overnight autoresearch results + bus logs |
| **Daytime focus (3-4 hrs)** | Desktop + Claude Code | Peptide Checker OR HUMMBL (never both in one session) |
| **Afternoon (1-2 hrs)** | Phone (GPT-5.4) | Content marketing, spec design, partnership outreach |
| **Evening (15 min)** | Desktop | Queue overnight experiments, verify NemoClaw state |
| **Overnight** | Desktop (GPU) + Nodezero | Autoresearch training runs, NemoClaw experiments |

**Critical path:** P1 (Vendor database web) is the single highest-priority item. Everything in Peptide Checker depends on it. It must ship in Weeks 1-2 or the entire revenue timeline slips.

---

## 6. What NOT to Build (Yet)

### Parking Lot -- Defer to Q3 2026 or Later

| ID | Feature | Composite | Why Defer |
|----|---------|-----------|-----------|
| R3 | ThinkPRM fine-tuned verifier | 20.0 | Requires training data from 100+ reasoning traces that do not exist yet. ThinkPRM prompted (R2) delivers 80% of the value at 10% of the effort. Wait until you have the traces. |
| H7 | Semantic cache (L2) | 22.0 | L1 exact-match cache gets you the easy wins. Semantic caching adds complexity (embedding model, similarity thresholds, cross-domain contamination risks) for marginal gain at current query volume. Revisit when API spend exceeds $500/month. |
| H10 | Code review pipeline | 22.0 | You are the only developer. Semgrep + LLM post-filter solves a team-scale problem. Run Semgrep manually on security-critical paths; skip the automated pipeline until there is a team or open-source contributors. |
| H9 | Open source HUMMBL release | 24.0 | HUMMBL needs a working bus protocol + stable agent loop + documentation before release. Premature open-sourcing of an unstable framework damages credibility. Target Q4 2026 at earliest after NemoClaw is running autonomously. |
| P10 | Community batch testing | 24.5 | Requires an active user community that does not exist yet. Ship the MVP, build the audience, then launch community features. |
| P9 | AI COA analyzer (ML) | 30.0 | The basic rule-based COA red-flag checker (P2) handles the MVP case. ML-based analysis needs training data from hundreds of real COA uploads. Build the upload pipeline first, collect data, then train. |
| A2 | Hymba hybrid experiments | 24.5 | Only relevant if GLA experiments (A1) show the architectural direction is promising. Conditional on A1 results. |
| A3 | Big model configs on Nodezero | 26.0 | Interesting research question but does not generate revenue or unblock anything. Run these when you have idle Nodezero cycles and curiosity, not as a priority. |
| H8 | Capability security model | 25.0 | Security model matters when agents have real autonomy. Currently there are no autonomous agents running. Build this when NemoClaw is actually operating overnight (Phase C). |
| S2 | Vision model replacement | 27.5 | moondream works. It is not blocking anything. Replace only if a specific use case demands better vision. |
| H5 | Confidence cascading | 29.0 | Requires log-probability extraction and calibration data. The heuristic router (H4) handles 90% of the routing value. Add cascading after accumulating 1,000+ routing decisions to calibrate thresholds. |
| N4 | Cross-machine coordination | 25.5 | This is the hardest NemoClaw feature (networking, state sync across OS boundaries). Get single-machine NemoClaw working first (N1+N2+N3+N5), then add cross-machine. |

### Explicitly Killed

| Feature | Why |
|---------|-----|
| Learned router (BERT/RouteLLM) | Premature optimization. Need 1,000+ routing decisions as training data. Heuristic router is validated at current scale. |
| A2A protocol integration | v0.3, pre-stable. No external agent systems to interoperate with. Monitor only. |
| At-home peptide testing hardware (Phase 5) | 5-10 years from consumer readiness per the business plan. Strategic positioning only, zero near-term action. |
| Dedicated apply model (Cursor dual-AI) | Over-engineering for current scale. Standard search/replace works. |
| vLLM migration | Ollama is working fine. Migrate only when speculative decoding becomes a bottleneck, which it is not at current throughput. |

---

## 7. The One-Page Answer

**If Reuben reads one paragraph:**

Build the Peptide Checker vendor database as a web application this week. It scored highest (49/55) across all dimensions because it is the foundation for every revenue stream: subscriptions, lab referrals, vendor certification, and content marketing all depend on a live, searchable vendor quality database. The existing peptide_db.py with 30 vendors and the 5 research reports are a head start that no competitor has. Migrate the data to a proper database, wrap it with FastAPI, put a minimal frontend on it, and deploy it to Cloudflare. Simultaneously, start the HUMMBL governance bus protocol in your secondary time blocks (it is the foundation that NemoClaw, the agent framework, and the open-source release all depend on), and queue GLA experiments to run overnight on the GPU. Do not touch ThinkPRM fine-tuning, semantic caching, the open-source release, or Hymba experiments -- they all have prerequisites that do not exist yet. The sequence is: revenue product first (Peptide Checker MVP in 4 weeks), infrastructure second (bus protocol + NemoClaw in 8 weeks), research continuously in the background (overnight experiments from Day 1). Every other item on this list either feeds into these three tracks or should wait until Week 12 when you have real user data to inform the next decision.

---

*Decision matrix generated 2026-03-23 | Review at Week 4 gate (April 20) and Week 12 gate (June 15)*
*Scores are directional, not precise. The ranking matters more than the exact numbers.*
*Update this document during Friday retrospectives as new information changes the calculus.*
