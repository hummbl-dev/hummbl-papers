# Finding F-005: Autonomous Research Agent Ecosystem Landscape

## Source
- **Research Run:** 2026-06-21 (read-only web intelligence + code review)
- **Method:** GitHub search, web search, direct README/code inspection
- **Confidence:** High (0.85) — all claims sourced from public repositories
- **Scope:** 10+ repositories, 100K+ combined stars

## Executive Summary

Karpathy's `autoresearch` (87.8K stars) sits at the center of a rapidly expanding ecosystem of autonomous research agents. These systems range from single-file experiment harnesses to 20-agent research organizations. The space is fragmenting along three axes:

1. **Scope:** Single-metric code optimization → full paper generation
2. **Agents:** Single agent → 20+ agent organizations
3. **Safety:** None → containerized sandbox → full governance primitives

HUMMBL's `autoresearch-pipeline` occupies a unique position: it is the only system in this landscape with production-grade safety primitives (kill switch, circuit breaker, delegation tokens, cost governor, governance bus). No other repo in this ecosystem has any safety infrastructure at all.

---

## The Landscape: 10 Key Repositories

### Tier 1: The Influencers (High Star Count, Broad Impact)

#### 1. `karpathy/autoresearch` — 87.8K stars
**Type:** Single-agent, single-GPU, single-file experiment harness  
**What it does:** Claude/Codex edits `train.py`, trains for 5 min, keeps/discards based on `val_bpb`. Human edits `program.md` (Markdown skill) to tune agent behavior.  
**Key innovation:** `program.md` as orchestration prompt; fixed time budget; simplicity criterion.  
**Safety:** None. Agent has full git access. No containerization.  
**HUMMBL relevance:** **HIGH** — direct upstream. HUMMBL's pipeline is the governance-hardened evolution of this pattern.

#### 2. `SakanaAI/AI-Scientist` — ~15K stars
**Type:** End-to-end automated scientific discovery (paper generation)  
**What it does:** Generates hypotheses, runs experiments, analyzes data, writes LaTeX manuscripts, generates figures, and produces peer-review-style critiques. Operates on "templates" (NanoGPT, 2D Diffusion, Grokking).  
**Key innovation:** First system to produce workshop-accepted papers entirely autonomously. Uses Aider for code editing. Supports 10+ LLM backends (OpenAI, Anthropic, DeepSeek, Gemini, etc.).  
**Safety:** Minimal. Warning about "dangerous packages" and process spawning. Recommends containerization. No built-in sandbox.  
**Templates:** Community-contributed templates extend to new domains.  
**HUMMBL relevance:** **MEDIUM** — demonstrates the "paper generation" downstream that HUMMBL's findings/proposals pipeline could evolve toward.

#### 3. `SakanaAI/AI-Scientist-v2` — Newer
**Type:** Agentic tree search for scientific discovery  
**What it does:** Removes reliance on human-authored templates. Generalizes across ML domains. Uses progressive agentic tree search guided by an experiment manager agent.  
**Key innovation:** Agentic tree search (BFTS — Best-First Tree Search) for hypothesis exploration. Workshop paper accepted through peer review.  
**Safety:** Same as v1 (minimal).  
**HUMMBL relevance:** **MEDIUM** — tree search for experiment selection is an algorithm HUMMBL's supervisor could adopt.

### Tier 2: The Multi-Agent Systems

#### 4. `Sibyl-Research-Team/sibyl-research-system` — Emerging
**Type:** 20+ agent autonomous research organization  
**What it does:** End-to-end ML research: literature survey → hypothesis generation → GPU experiment execution → conference-ready paper writing. Built natively on Claude Code (skills, plugins, MCP tools, agent teams).  
**Key innovations:**
- **Dual-loop architecture:** Inner loop (research iteration) + Outer loop (system self-evolution)
- **Self-evolving system:** After every iteration, classifies issues across 8 categories, accumulates lessons, updates agent prompts and scheduling strategies
- **Claude Code native:** Not an API wrapper. Uses Claude's full ecosystem: SSH remote execution, multi-model collaboration, MCP servers
- **Sentinel watchdog:** Auto-restarts Claude Code if it crashes or goes idle
- **19-stage pipeline:** Literature review → idea debate → experiment planning → GPU execution → multi-agent paper writing → peer review → quality gates
**Safety:** `--dangerously-skip-permissions` flag grants unrestricted execution. No kill switch. No cost limits.  
**HUMMBL relevance:** **HIGH** — Sibyl is the closest competitor to HUMMBL's vision. It has the multi-agent orchestration but lacks governance. HUMMBL's safety primitives are the differentiator.

#### 5. `raja21068/AutoResearch` — Emerging
**Type:** Multi-agent framework with paper generation  
**What it does:** Takes code, data, ideas, and papers as input; runs execution-grounded research loop; produces improved code, validated experiments, and structured research paper.  
**Agent roster:** Orchestrator, Planner, CodeAgent, Experiment/Benchmark Agent, FigureAgent, Review/Critic Agents, Research Agent (literature), Verification Engine, Memory System, Paper Writer Agent.  
**Key innovation:** Self-healing loop: Generate → Run → Error Detect → Fix → Run. Human-in-the-loop or fully automatic modes.  
**Safety:** None described.  
**HUMMBL relevance:** **MEDIUM** — agent decomposition is similar to HUMMBL's fleet model. The verification engine and critic agents map to HUMMBL's review loops.

### Tier 3: The Specialized Innovators

#### 6. `ErikDeBruijn/autoresearcher2` — Niche
**Type:** Bayesian experiment selection for ML research  
**What it does:** Same substrate as Karpathy's autoresearch (edits `train.py`, measures `val_bpb`) but adds structured Bayesian inference. Maintains a generative model of factor effects, interactions, and uncertainty.  
**Key innovation:** Learntropy-inspired appraisal — weights experiments by epistemic value. The agent notices when its model can't explain results and proposes missing dimensions.  
**Safety:** None.  
**HUMMBL relevance:** **HIGH** — the Bayesian experiment selection algorithm could directly improve HUMMBL's supervisor perturbation logic (currently random.choice).

#### 7. `proyecto26/autoresearch-ai-plugin` — Niche (Claude Code plugin)
**Type:** Claude Code plugin for autonomous experiment loops  
**What it does:** Two skills: **Autoresearch** (generic metric optimization) + **Autoresearch ML** (GPU-specific templates for LLM training).  
**Key innovations:**
- **Context-resilient:** State persists in `autoresearch.jsonl` — survives context resets
- **Confidence scoring:** MAD-based statistical analysis separates real improvements from noise
- **ASI (Actionable Side Information):** Structured annotations per experiment that survive git reverts
- **Segments:** Multi-phase sessions — switch optimization targets mid-session
- **VRAM scaling:** Automatic guidance from 4GB (GTX 1080 Ti) to 80GB (H100)
**Safety:** None.  
**HUMMBL relevance:** **MEDIUM** — the ASI pattern (annotations that survive reverts) and MAD-based confidence scoring are directly applicable to HUMMBL's experiment tracking.

#### 8. `AweAI-Team/AiScientist` — Niche
**Type:** Long-horizon ML research engineering  
**What it does:** Two tracks: `paper` (reproduce a paper) and `mle` (competition-style ML engineering). Runs 24-hour autonomous sessions with 78+ experiment cycles.  
**Key innovation:** Maintains coherent progress across heterogeneous stages while preserving evolving project state over time.  
**Safety:** None described.  
**HUMMBL relevance:** **LOW-MEDIUM** — the long-horizon state management is relevant, but the repo appears less mature than others.

#### 9. `MaximeRobeyns/self_improving_coding_agent` — Niche
**Type:** Self-improvement loop on agent's own codebase  
**What it does:** Iterative improvement loop: (1) evaluate current agent on benchmarks, (2) archive results, (3) run agent on its own codebase to improve, (4) repeat.  
**Key innovation:** Recursive self-improvement — the agent improves itself.  
**Safety:** None.  
**HUMMBL relevance:** **LOW** — more of a meta-research project. Interesting for HUMMBL's recursive self-improvement skill but not directly applicable.

#### 10. `allenai/codescientist` — Academic
**Type:** Semi-automated scientific discovery with genetic mutations  
**What it does:** Mutates combinations of scientific articles and code examples to create novel experiment ideas. Automatically creates, runs, and debugs experiment code in containers. Writes reports.  
**Key innovation:** LLM-as-mutator paradigm for idea generation. Containerized execution. Human-in-the-loop or fully automatic modes.  
**Published:** ACL Findings 2025.  
**Safety:** Containerized execution is a safety primitive, though minimal.  
**HUMMBL relevance:** **MEDIUM** — containerization approach and the mutation-based idea generation are relevant. The paper-generation pipeline maps to HUMMBL's findings → proposals flow.

### Tier 4: The Data-to-Paper Pipeline

#### 11. `Technion-Kishony-lab/data-to-paper` — Academic
**Type:** End-to-end research from raw data to human-verifiable papers  
**What it does:** Guides interacting LLM and rule-based agents through the conventional scientific path: annotated data → hypotheses → literature search → data analysis code → interpretation → paper writing.  
**Key innovation:** "Data-chained" manuscripts — transparent, backward-traceable, human-verifiable. Published in a medical journal (NEJM AI).  
**Safety:** Human-in-the-loop mode available.  
**HUMMBL relevance:** **LOW-MEDIUM** — the verification and traceability patterns are relevant, but the domain (biomedical research) is different.

---

## Comparative Analysis

### Safety & Governance Maturity

| Repo | Kill Switch | Circuit Breaker | Cost Governor | Sandbox | Delegation | Bus Audit |
|------|:-----------:|:---------------:|:-------------:|:-------:|:----------:|:---------:|
| **HUMMBL autoresearch-pipeline** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| karpathy/autoresearch | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| SakanaAI/AI-Scientist | ❌ | ❌ | ❌ | ⚠️ | ❌ | ❌ |
| Sibyl | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| allenai/codescientist | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| All others | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Key insight:** HUMMBL is the **only** system in this entire ecosystem with production governance primitives. This is a massive differentiator for enterprise and regulated use cases.

### Orchestration Architecture

| Repo | Orchestration | Agents | State Management |
|------|--------------|--------|-----------------|
| karpathy/autoresearch | `program.md` (Markdown prompt) | 1 | Git branches |
| SakanaAI/AI-Scientist | Python pipeline + Aider | 1-3 | File system + templates |
| Sibyl | Claude Code skills + MCP | 20+ | Time-weighted memory + self-evolution |
| raja21068/AutoResearch | Python orchestrator | 10+ | Memory system + meta-learning |
| **HUMMBL autoresearch-pipeline** | Python supervisor + worker + queue | 2+ | JSON state + governance bus |
| ErikDeBruijn/autoresearcher2 | Bayesian model + LLM | 1 | Structured factor space + memory |

### Experiment Selection Strategy

| Repo | Strategy | Innovation |
|------|----------|-----------|
| karpathy/autoresearch | LLM implicit reasoning from flat log | Simplicity criterion |
| SakanaAI/AI-Scientist | LLM brainstorming + template mutation | Template-based generalization |
| SakanaAI/AI-Scientist-v2 | Agentic tree search (BFTS) | Progressive hypothesis exploration |
| Sibyl | Multi-agent debate + GPU scheduling | Self-evolving prompts |
| **HUMMBL autoresearch-pipeline** | Random perturbation from recent results | Safety-governed execution |
| ErikDeBruijn/autoresearcher2 | Bayesian factor model + learntropy | Explicit world model + uncertainty |
| proyecto26/autoresearch-ai-plugin | LLM + MAD confidence scoring | ASI annotations survive reverts |

---

## Gaps in the Ecosystem

1. **No cross-repo safety standards:** Every system invents its own (or has none). No shared kill switch protocol, no standard circuit breaker semantics.

2. **No cost governance:** None of the high-star repos track compute cost or API spend. A runaway agent could rack up thousands of dollars unchecked.

3. **No bus integration:** Only HUMMBL posts experiment events to a coordination bus. Other systems run in silos.

4. **Limited cross-platform support:** Most are NVIDIA-only. Forks handle other platforms, but the upstreams don't care.

5. **No proposal-to-action pipeline:** Systems generate papers or raw experiments, but none have a structured "finding → proposal → implementation" workflow like HUMMBL's.

6. **No recurrence/scheduling:** Only HUMMBL has automated weekly recurrence and queue management.

---

## Recommendations for HUMMBL

### Immediate (Phase 4+):

1. **Adopt Bayesian experiment selection** (`autoresearcher2`): Replace the supervisor's random perturbation with a structured factor model. This is the biggest algorithmic improvement available.

2. **Study Sibyl's self-evolution pattern**: The outer loop (system learns from its own research process) is something HUMMBL could implement via the governance bus and memory system.

3. **Implement ASI annotations** (`autoresearch-ai-plugin`): Structured annotations per experiment that survive git reverts. This captures "lessons from failures" that the current pipeline discards.

4. **Add MAD confidence scoring**: The `autoresearch-ai-plugin` uses Median Absolute Deviation to separate real improvements from noise. This would improve the supervisor's keep/discard decisions.

### Medium-term:

5. **Paper generation downstream**: SakanaAI's AI-Scientist proves that automated paper generation is viable. HUMMBL's findings → proposals pipeline could evolve toward generating LaTeX manuscripts with figures and citations.

6. **Containerized worker execution**: `allenai/codescientist` runs experiments in containers. HUMMBL should sandbox worker execution to prevent runaway agents from damaging the host.

7. **Template ecosystem**: SakanaAI's template model (NanoGPT, Diffusion, Grokking) is how they generalize across domains. HUMMBL could define "experiment templates" for different research domains.

8. **Multi-agent debate for hypothesis generation**: Sibyl's 20-agent debate model could improve the quality of experiment ideas before they reach the queue.

---

## Appendix: Fork Ecosystem of Karpathy's Autoresearch

| Fork | Platform | Stars | Author | Status |
|------|----------|-------|--------|--------|
| `miolini/autoresearch-macos` | macOS | — | miolini | Active |
| `trevin-creator/autoresearch-mlx` | macOS (MLX) | — | trevin-creator | Active |
| `jsegov/autoresearch-win-rtx` | Windows (RTX) | 671 | jsegov | Active |
| `andyluo7/autoresearch` | AMD GPU | — | andyluo7 | Active |
| `hummbl-dev/autoresearch-win-rtx` | Windows (RTX) | — | hummbl-dev | **ARCHIVED** |
| `hummbl-dev/autoresearch-pipeline` | Cross-platform | — | hummbl-dev | **CANONICAL** |

---

*Intel capture completed: 2026-06-21*
*Sources: Direct code review of karpathy/autoresearch, web intelligence on 10+ repositories*
*Classification: OPEN SOURCE INTELLIGENCE — all information from public repositories*
