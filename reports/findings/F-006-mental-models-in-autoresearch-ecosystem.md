# Finding F-006: Where WM.MD, MM.MD, and Base120 Mental Models Live in the Autoresearch Ecosystem

## Source
- **Brainstorm session:** 2026-06-21
- **Scope:** Map HUMMBL cognitive primitives (WM, MM, Base120) to 10+ autonomous research systems
- **Confidence:** Architectural reasoning (not empirically validated)

## TL;DR

| Primitive | What It Is | Where It Lives Now | Where It Should Live |
|-----------|-----------|-------------------|---------------------|
| **WM.MD** | World Model — what the agent believes about the external research space | Scattered: `factor_model.json` (proposed), `research_queue.json`, `results.tsv` | Unified: `WM.md` as both human-readable prose and machine-parseable YAML frontmatter |
| **MM.MD** | Mental Model — what the agent believes about itself | Scattered: `lessons_learned.md` (proposed), CLP ledger, `program.md` | Unified: `MM.md` as self-model + strategy registry + Base120 usage history |
| **Base120** | 120 canonical reasoning operators | `lattice_advisor.py`, `base120_registry.json` | Embedded in supervisor reasoning, experiment selection, failure classification, and self-evolution |

---

## 1. WM.MD — The World Model

### Definition
A **WM.MD** (World Model / Working Memory) is the agent's explicit, inspectable, and updatable model of the external world it operates in. For autoresearch, this means: what do we know about the parameter space? Which experiments have been tried? What hardware constraints exist? What is the current SOTA? What is the research landscape telling us?

### Where WM.MD Lives in the Ecosystem

#### In HUMMBL's Pipeline (Current + Proposed)

| Component | WM Content | Format | Human-Readable? |
|-----------|-----------|--------|-----------------|
| `research_queue.json` | What topics are pending/completed | JSON | Partially |
| `results.tsv` | Raw experiment outcomes | TSV | Yes |
| `findings/*.md` | Distilled knowledge from experiments | Markdown | Yes |
| `factor_model.json` (P-002) | Bayesian beliefs about parameter effects | JSON | No |
| `discarded_experiments.jsonl` (P-002) | Failed hypotheses and their ASI | JSONL | No |
| `docs/DUAL_MACHINE_SETUP.md` | Hardware topology and constraints | Markdown | Yes |

**The problem:** World knowledge is fragmented across JSON, TSV, Markdown, and JSONL. There is no single source of truth that a human can read and an agent can parse.

#### In Other Ecosystem Repos

| Repo | Their WM Equivalent | What's Missing |
|------|---------------------|----------------|
| `karpathy/autoresearch` | `results.tsv` + git branch history | No structured parameter-interaction model; no cross-run learning |
| `SakanaAI/AI-Scientist` | Template files (`template_nano_gpt/` etc.) | Templates are static; no dynamic world model updates from experiment results |
| `Sibyl` | Time-weighted memory + literature search cache | No explicit, inspectable world model file; everything is implicit in prompts |
| `ErikDeBruijn/autoresearcher2` | Bayesian factor model (in code) | Not human-readable; no markdown representation |

### Where WM.MD Should Live: A Unified `WM.md`

**Proposal:** Create `WM.md` at the root of the pipeline directory as the canonical world model document.

```markdown
---
# Machine-parseable frontmatter
last_updated: 2026-06-21T00:15Z
hardware_profile: nodezero_m4_mps + anvil_rtx3080ti_cuda
dataset: tinystories
baseline_val_bpb: 2.500
experiments_run: 47
experiments_kept: 12
experiments_discarded: 35
---

# World Model: Autoresearch Pipeline

## Parameter Landscape

| Parameter | Current Belief | Uncertainty | Best Value Found | Trend |
|-------------|---------------|-------------|------------------|-------|
| lr | Higher is better up to ~0.003 | Medium | 0.0025 | ↑ |
| batch_size | 64-128 is optimal for MPS | Low | 96 | → |
| depth | 4-6 is sweet spot for 5-min budget | Medium | 5 | ↓ |
| window_pattern | "L" outperforms "SSSL" on MPS | Low | "L" | ↑ |

## Hardware Constraints

- **nodezero (M4/MPS)**: Max VRAM ~24GB. `depth > 8` causes OOM.
- **Anvil (RTX 3080 Ti)**: Max VRAM ~12GB. `depth > 6` causes OOM.
- **Cross-platform**: Results are not directly comparable. Anvil CUDA is ~3x faster than nodezero MPS.

## Active Hypotheses

1. **H-001**: "Smaller models with higher LR converge faster on tinystories"
   - Status: PARTIALLY CONFIRMED (3/5 experiments showed improvement)
   - Confidence: 0.6
   - Next test: Try depth=3, lr=0.005

2. **H-002**: "Window pattern 'L' is universally better than 'SSSL' on small GPUs"
   - Status: CONFIRMED on MPS; UNTESTED on CUDA
   - Confidence: 0.8
   - Next test: Run 'L' baseline on Anvil

## Failed Hypotheses (from ASI store)

- **FH-001**: "Doubling embedding dimension improves BPB" → Actually made it worse (-0.02). Likely cause: too many parameters for 5-min budget.
- **FH-002**: "GeLU is better than ReLU²" → No significant difference (within MAD). Simpler code wins.

## Research Landscape (External)

- Karpathy's autoresearch baseline: val_bpb 0.9979 (H100, climbmix-400b, 5 min)
- HUMMBL tinystories baseline: val_bpb 2.500 (M4/MPS, 5 min)
- **Note**: Different datasets make direct comparison impossible.
```

**Why this is powerful:**
- **Human reads it** to understand what the agent knows about the research space
- **Machine parses the YAML frontmatter** for structured queries
- **Agent reads the Markdown body** for context when generating hypotheses
- **Version controlled** — world model evolves with the research

---

## 2. MM.MD — The Mental Model

### Definition
A **MM.MD** (Mental Model / Meta-Model) is the agent's explicit model of itself. What strategies has it used? What is its track record? What cognitive biases does it exhibit? Which Base120 mental models has it applied successfully? What is its "research style"?

### Where MM.MD Lives in the Ecosystem

#### In HUMMBL's Pipeline (Current + Proposed)

| Component | MM Content | Format |
|-----------|-----------|--------|
| `program.md` (Karpathy pattern) | Agent instructions | Markdown |
| `lessons_learned.md` (P-002) | Extracted lessons from failures | Markdown |
| CLP ledger (`_state/cognition/ledger.jsonl`) | Past reasoning traces | JSONL |
| `agent_intent.py` | Current agent intent model | Python |
| `base120_registry.json` usage history | Which mental models were applied | JSON |

**The problem:** There is no explicit self-model. The agent doesn't "know" that it tends to over-optimize batch_size, or that it hasn't tried Inversion-based (IN domain) hypotheses in 20 experiments.

#### In Other Ecosystem Repos

| Repo | Their MM Equivalent | What's Missing |
|------|---------------------|----------------|
| `karpathy/autoresearch` | `program.md` (human-written, static) | No self-updating; no track record of agent behavior |
| `Sibyl` | Self-evolution prompts (updated weekly) | Implicit in prompt engineering; no inspectable self-model |
| `raja21068/AutoResearch` | Memory system + meta-learning | Not a single document; distributed across modules |
| `MaximeRobeyns/self_improving_coding_agent` | Benchmark results archive | Only tracks performance, not reasoning strategies |

### Where MM.MD Should Live: A Unified `MM.md`

**Proposal:** Create `MM.md` at the root of the pipeline directory as the canonical self-model.

```markdown
---
# Machine-parseable frontmatter
last_updated: 2026-06-21T00:15Z
agent_identity: autoresearch-pipeline-supervisor
base120_models_applied_this_week: [DE5, RE13, IN7, P2]
base120_models_never_applied: [IN16, CO11, SY14]
cognitive_bias_flags: ["over-optimizes_batch_size", "under-explores_optimizer_changes"]
---

# Mental Model: Autoresearch Supervisor

## Strategy Registry

| Strategy | Success Rate | Times Used | Last Used | Notes |
|----------|-------------|------------|-----------|-------|
| Random perturbation | 0.23 (12/52) | 52 | 2026-06-20 | Default; being replaced by Bayesian |
| LR sweep | 0.40 (6/15) | 15 | 2026-06-18 | High success rate; should use more |
| Architecture change | 0.10 (2/20) | 20 | 2026-06-15 | Low success; agent overestimates impact |
| Simplification (delete code) | 0.60 (3/5) | 5 | 2026-06-10 | High success; Karpathy was right |

## Base120 Model Usage

### Frequently Applied (Last 30 Days)
- **DE5** Root Cause Analysis: Used 12 times. Success rate 0.33. Good for debugging NaN/Inf.
- **RE13** Velocity-Tune: Used 8 times. Success rate 0.50. Good for identifying slow experiments.
- **IN7** Premortem: Used 5 times. Success rate 0.40. Good for predicting OOM before running.

### Never Applied (Blind Spots)
- **IN16** Worst-Case Optimization: Never used. Could help identify parameter combinations that always fail.
- **CO11** Pattern-Tile: Never used. Could extract reusable templates from successful experiments.
- **SY14** Leverage Points: Never used. Could identify which single parameter change has the highest impact.

## Known Cognitive Biases

1. **Batch Size Fixation**: Agent tends to perturb batch_size repeatedly even when it has marginal effect.
   - Detected: 8 of last 20 experiments modified batch_size
   - Mitigation: Add a "batch_size cooldown" — don't touch for 5 experiments after a batch_size change

2. **Architecture Overestimation**: Agent believes architectural changes (depth, width, attention pattern) will have large impact. Data shows they rarely do within 5-min budget.
   - Detected: 20 architecture changes, only 2 kept
   - Mitigation: Apply IN7 (Premortem) before any architecture change

3. **Recency Bias**: Agent overweights recent experiments when proposing new ones.
   - Detected: 70% of new hypotheses reference experiments from last 3 days
   - Mitigation: Force 1 "archive dig" per week — sample from experiments >30 days old

## Self-Improvement Goals

1. **Increase simplification rate**: Target 20% of experiments are "delete code" attempts.
2. **Explore IN domain more**: Apply at least 1 IN-domain mental model per week.
3. **Reduce batch_size fixation**: Cap at 1 batch_size experiment per 10-experiment window.
```

**Why this is powerful:**
- **Agent reads its own MM.md** before proposing experiments to avoid cognitive biases
- **Human reads it** to understand what the agent thinks about itself
- **Self-evolution script updates it** after each weekly batch
- **Base120 advisor queries it** to recommend underused mental models

---

## 3. Base120 — The Cognitive Governance Layer

### Where Base120 Already Lives in HUMMBL

| Module | Role | How Base120 Is Used |
|--------|------|-------------------|
| `lattice_advisor.py` | Recommends mental models from query | `Base120Advisor.recommend("debug NaN")` → DE5, IN7, etc. |
| `cognition/server.py` | Open Brain HTTP API | `POST /base120/recommend` |
| `agent_intent.py` | Agent reasoning governance | Tags intent with Base120 model codes |
| `huaomp_loop.py` | HUAOMP analytical lenses | Maps HUAOMP questions to Base120 domains |

### Where Base120 Should Live in the Research Pipeline

#### A. Experiment Selection: `choose_perturbation()` (supervisor)

Before selecting a perturbation, the supervisor should query the Base120 advisor:

```python
# Pseudocode for supervisor.py
def choose_perturbation_with_base120(current_params, results, asi_store):
    # Build a query from the current situation
    query = f"""
    I have run {len(results)} experiments. The best val_bpb is {get_best_val_bpb(results)}.
    Recent experiments have focused on {get_recent_param_changes(results)}.
    I keep failing with {get_common_failure_modes(asi_store)}.
    What mental model should I apply for the next experiment?
    """

    # Query Base120 advisor
    advisor = Base120Advisor()
    recommendations = advisor.recommend(query, limit=3)

    # Use the top recommendation to guide perturbation selection
    top_model = recommendations[0]
    if top_model["id"] == "IN7":  # Premortem
        # Before running, ask: what could go wrong?
        return generate_premortem_perturbation(current_params)
    elif top_model["id"] == "DE5":  # Root Cause Analysis
        # Analyze why recent failures happened
        return generate_root_cause_perturbation(current_params, asi_store)
    elif top_model["id"] == "CO11":  # Pattern-Tile
        # Extract reusable pattern from best experiment
        return generate_pattern_tile_perturbation(results)
    # ... etc
```

This replaces the current `random.choice` with **reasoning-governed selection**.

#### B. Failure Classification: `self_evolve.py` (scripts)

When the self-evolution script classifies failures, it should use Base120 models as classification dimensions:

```python
FAILURE_CLASSIFICATION_BASE120 = {
    "P": "Perspective failures — wrong framing of the problem",
    "IN": "Inversion failures — missed edge cases, worst cases",
    "CO": "Composition failures — incompatible component combinations",
    "DE": "Decomposition failures — wrong root cause identified",
    "RE": "Recursion failures — infinite loops, non-terminating experiments",
    "SY": "Systems failures — emergent behavior, feedback loops",
}
```

Sibyl classifies failures into 8 categories, but they invented their own taxonomy. HUMMBL should use the canonical Base120 6-domain taxonomy.

#### C. Proposal Evaluation: `proposal_drafter.py` (scripts)

When evaluating whether a finding should become a proposal, apply Base120 models:

- **P1** First Principles: Does the proposal address a foundational truth?
- **IN7** Premortem: What could go wrong if we implement this?
- **SY14** Leverage Points: Is this the highest-impact change we could make?
- **RE13** Velocity-Tune: How fast can we implement and validate this?

#### D. ASI Annotation: `asi_store.py` (supervisor)

Each ASI annotation should tag which Base120 model was "active" during the experiment's design:

```json
{
  "asi": {
    "hypothesis": "Increasing LR will improve convergence",
    "base120_guidance": ["DE5", "RE13"],
    "reasoning": "Applied DE5 (Root Cause) to identify slow convergence as the bottleneck. Applied RE13 (Velocity-Tune) to choose the fastest intervention."
  }
}
```

This creates a **traceable cognitive audit trail** — every experiment knows which mental model guided it.

---

## 4. Integration Architecture: The Cognitive Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    COGNITIVE LAYER (Base120)                 │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  WM.md       │  │  MM.md        │  │  Base120      │    │
│  │  World Model │  │  Mental Model │  │  Registry     │    │
│  │              │  │               │  │  (120 models)  │    │
│  │  "What I     │  │  "What I      │  │               │    │
│  │   know about │  │   know about  │  │  "How I       │    │
│  │   the world" │  │   myself"     │  │   should      │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘    │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘         │
│                            │                               │
│                   ┌─────────▼─────────┐                    │
│                   │  Lattice Advisor   │                    │
│                   │  (recommends       │                    │
│                   │   mental models)   │                    │
│                   └─────────┬─────────┘                    │
└───────────────────────────┼─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                 RESEARCH LAYER (Pipeline)              │
│                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │  Supervisor  │  │  Worker      │  │  Self-Evolve ││
│  │              │  │              │  │              ││
│  │  - Queries   │  │  - Runs      │  │  - Classifies││
│  │    advisor   │  │    exp       │  │    failures  ││
│  │  - Reads     │  │  - Reports   │  │  - Updates   ││
│  │    WM.md     │  │    metrics   │  │    MM.md     ││
│  │  - Avoids    │  │  - Writes    │  │  - Extracts  ││
│  │    biases    │  │    ASI       │  │    lessons   ││
│  │    from      │  │              │  │              ││
│  │    MM.md     │  │              │  │              ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
└───────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                 MEMORY LAYER (CLP + Open Brain)          │
│                                                        │
│  ledger.jsonl  →  experiment events  →  searchable       │
│  state.json    →  current cogstate   →  boot context     │
│  intent.md     →  sprint intent      →  governs scope    │
└───────────────────────────────────────────────────────┘
```

---

## 5. Competitive Implications

### Why This Is HUMMBL's Moat

| System | Has World Model? | Has Self-Model? | Has Canonical Reasoning? |
|--------|:--------------:|:---------------:|:------------------------:|
| Karpathy autoresearch | ❌ (flat log) | ❌ (static program.md) | ❌ |
| SakanaAI AI-Scientist | ❌ (templates) | ❌ | ❌ |
| Sibyl | ⚠️ (implicit) | ⚠️ (implicit) | ❌ |
| autoresearcher2 | ✅ (Bayesian) | ❌ | ❌ |
| autoresearch-ai-plugin | ✅ (ASI) | ❌ | ❌ |
| **HUMMBL (with this proposal)** | **✅ (WM.md)** | **✅ (MM.md)** | **✅ (Base120)** |

**No other system in the ecosystem has all three.** Karpathy has the best single-file engineering. SakanaAI has the best paper generation. Sibyl has the most agents. But none of them have:
1. An explicit, inspectable world model
2. An explicit, introspectable self-model
3. A canonical, governed set of reasoning operators

This is the **cognitive governance gap** that Base120 was designed to fill.

---

## 6. Recommendations

### Immediate (this week)

1. **Create `WM.md` and `MM.md` scaffolds** in `autoresearch-pipeline/` as living documents. Start them empty and let the pipeline populate them.

2. **Tag the first ASI annotation with Base120 models** — even if it's manual. Prove the traceability pattern works.

3. **Query Base120 advisor from `choose_perturbation()`** — replace one `random.choice` call with a `lattice_advisor` recommendation. Measure if it changes outcomes.

### Short-term (next 4 weeks)

4. **Add `WM.md` and `MM.md` parsing to `scripts/weekly_run.py`** — the weekly orchestrator should read both files at startup and update both files at shutdown.

5. **Add Base120 classification to `scripts/self_evolve.py`** — use the 6-domain taxonomy for failure classification, not ad-hoc categories.

6. **Publish a public blog post** — "Why Autoresearch Agents Need Mental Models." Position HUMMBL as the only system with cognitive governance. Reference this finding.

### Medium-term (next quarter)

7. **Propose a Base120 extension for autoresearch** — a Domain120 lattice specifically for ML experiment design. This becomes a public, ratified standard that the ecosystem can adopt.

8. **Integrate WM.md with Open Brain** — make the world model queryable over HTTP so external agents (e.g., a Claude Code plugin) can read HUMMBL's research state.

---

## Appendix: Proposed File Locations

```
autoresearch-pipeline/
├── WM.md                          ← NEW: World model (human + machine)
├── MM.md                          ← NEW: Mental model (human + machine)
├── supervisor/
│   ├── supervisor.py              ← MODIFIED: reads WM.md, MM.md, queries advisor
│   ├── factor_model.py            ← NEW: Bayesian model (from P-002)
│   ├── asi_store.py               ← NEW: ASI annotations (from P-002)
│   └── significance.py            ← NEW: MAD scoring (from P-002)
├── scripts/
│   ├── weekly_run.py              ← MODIFIED: reads/writes WM.md, MM.md
│   ├── self_evolve.py             ← NEW: updates MM.md (from P-002)
│   └── proposal_drafter.py        ← MODIFIED: applies Base120 evaluation
└── docs/
    └── DUAL_MACHINE_SETUP.md
```

---

*Brainstorm completed: 2026-06-21*
*Classification: ARCHITECTURAL DESIGN — conceptual integration of HUMMBL cognitive primitives with autonomous research ecosystem*
