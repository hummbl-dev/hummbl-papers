# RQ-009: Agent Framework Comparison (2025-2026)

**Research ID:** RQ-009
**Domain:** Agent Frameworks
**Date:** 2026-03-23
**Status:** Completed

---

## Executive Summary

The AI agent framework landscape has matured rapidly between 2025-2026, consolidating around a handful of serious contenders while spawning dozens of niche tools. This report compares the major frameworks across architecture, production readiness, community adoption, pricing, and suitability for solo founders and small teams.

**Key findings:**
- **CrewAI** leads in time-to-production for role-based multi-agent workflows (45.9k stars, 12M+ daily executions)
- **LangGraph** is the most battle-tested for production stateful pipelines, with best-in-class observability via LangSmith
- **Microsoft Agent Framework** (AutoGen + Semantic Kernel merger) targets enterprise GA by Q1 2026 end, but the transition creates adoption risk
- **Claude Agent SDK** provides the most powerful coding-agent runtime, leveraging MCP for tool interoperability
- **OpenAI Agents SDK** offers the lightest abstraction with only 4 core primitives
- **For solo founders:** Direct API calls + lightweight orchestration often beats heavy frameworks. When a framework helps, CrewAI or Pydantic AI offer the best effort-to-value ratio
- **The "no framework" approach** remains viable and sometimes superior, especially for teams with strong Python fundamentals

---

## Table of Contents

1. [Multi-Agent Orchestration Frameworks](#1-multi-agent-orchestration-frameworks)
2. [Autonomous Coding Agents](#2-autonomous-coding-agents)
3. [Other Notable Frameworks](#3-other-notable-frameworks)
4. [Comparison Matrix](#4-comparison-matrix)
5. [For Solo Founders and Small Teams](#5-for-solo-founders-and-small-teams)
6. [HUMMBL-Specific Recommendations](#6-hummbl-specific-recommendations)
7. [Sources](#7-sources)

---

## 1. Multi-Agent Orchestration Frameworks

### 1.1 CrewAI

**GitHub:** 45,900+ stars | **Version:** 1.10.1 | **Language:** Python
**License:** MIT (open source) + Commercial platform (CrewAI AMP)

#### Architecture
CrewAI operates on a dual-architecture model:
- **Crews:** Collaborative teams of role-playing agents with defined roles, goals, and backstories. Each agent has specialized expertise and delegates tasks within a structured workflow
- **Flows:** Enterprise/production architecture for building and deploying multi-agent systems with HITL support

Core primitives: Agents, Tasks, Crews, Processes (sequential or hierarchical). Built entirely from scratch -- no LangChain dependency (despite early versions using it). Native MCP and A2A (Agent-to-Agent) protocol support as of v1.10.

#### Strengths
- **Fastest time-to-production:** Deploys multi-agent teams ~40% faster than LangGraph for standard business workflows
- **Intuitive mental model:** Role-based metaphor maps naturally to organizational thinking
- **Strong community:** 100,000+ developers certified through learn.crewai.com
- **Production scale:** 12M+ daily agent executions across the platform
- **Low boilerplate:** Minimal code to get started

#### Weaknesses
- **Managerial overhead:** Consumes ~3x the tokens of LangChain for simple tasks due to deliberation layer
- **Less mature monitoring:** Observability tooling trails LangSmith
- **Cannot disable deliberation:** No option for direct tool-calling bypass
- **Opinionated:** The role-based metaphor can feel forced for non-team workflows

#### Pricing
| Tier | Price | Executions/mo | Features |
|------|-------|---------------|----------|
| Open Source | Free | Unlimited (self-hosted) | Core framework |
| Starter | Free | 50 | Hosted platform |
| Professional | $25/mo | 100 | + analytics |
| Enterprise | Custom | Up to 30,000 | Self-hosted K8s/VPC, SOC2, SSO, PII masking |

#### Production Deployments
Goldman Sachs, among others, has been cited in enterprise adoption discussions. The platform handles 12M+ daily executions in production environments.

---

### 1.2 AutoGen / Microsoft Agent Framework

**GitHub:** ~38,000 stars (AutoGen) | **Version:** AutoGen 0.4+ / Agent Framework RC
**Language:** Python, .NET | **License:** MIT

#### Architecture
AutoGen v0.4 (January 2025) was a ground-up rewrite with:
- **Asynchronous messaging:** Event-driven and request/response patterns
- **Layered architecture:** Core layer, Agent Chat layer, First-party Extensions
- **Modular design:** Pluggable agents, tools, memory, and models
- **Group chat patterns:** Multi-party conversations, consensus-building, nested chat

**Major shift (October 2025):** Microsoft merged AutoGen with Semantic Kernel into the unified **Microsoft Agent Framework**, targeting 1.0 GA by end of Q1 2026. This introduces:
- Graph-based workflow API for multi-step, multi-agent orchestration
- Sequential, parallel, and custom orchestration patterns
- Enterprise features: OpenTelemetry, Azure Monitor, Entra ID, CI/CD support

#### AutoGen Studio
No-code/low-code interface for building and testing multi-agent workflows. Useful for prototyping but limited for production customization.

#### Strengths
- **Research backing:** Microsoft Research origin with strong academic foundation
- **Conversation patterns:** Most diverse multi-party conversation support of any framework
- **Enterprise integration:** Deep Azure/Microsoft ecosystem integration
- **Type safety:** Strong typing in both Python and .NET SDKs
- **Flexibility:** Supports the widest range of agent interaction patterns

#### Weaknesses
- **Transition risk:** AutoGen is in maintenance mode; migration to Agent Framework required
- **Highest latency:** Chat-heavy "consensus-building" approach adds overhead
- **Steep learning curve:** Complex abstractions, especially for the new Agent Framework
- **Breaking changes:** v0.4 was a complete rewrite; Agent Framework is another shift
- **Fragmented documentation:** Multiple overlapping docs (AutoGen v0.2, v0.4, Semantic Kernel, Agent Framework)

#### Pricing
Fully open source (MIT). Enterprise support through Azure services and Microsoft support contracts.

---

### 1.3 LangGraph (LangChain)

**GitHub:** ~20,000+ stars | **Language:** Python, TypeScript
**License:** MIT (open source) + Commercial (LangSmith/Cloud)

#### Architecture
LangGraph treats agent workflows as **state machines** (directed graphs):
- **Nodes:** Functions or agent steps
- **Edges:** Transitions between nodes (including conditional routing)
- **State:** Persistent, reducer-driven state management with checkpointing
- **Cycles:** First-class support for loops and iterative refinement

This is a fundamentally different paradigm from CrewAI's role-based approach or AutoGen's conversation-based approach. You explicitly define the control flow graph.

#### LangGraph vs Pure LangChain
| Aspect | LangChain | LangGraph |
|--------|-----------|-----------|
| Paradigm | Linear chains/sequences | Directed graphs with cycles |
| State | Implicit | Explicit, persistent |
| Branching | Limited | First-class conditional routing |
| Debugging | Basic | Full state inspection at every node |
| Use case | Simple RAG/chains | Complex multi-step agents |

#### LangSmith / LangGraph Cloud Integration
- **LangSmith:** Observability platform with step-by-step traces, token counts per node, run replay. Best-in-class debugging for agent systems
- **Deployment:** Rebranded as "LangSmith Deployment" -- runs billed at $0.005 each
- **Pricing:**
  - Developer: Free (5,000 traces/mo, 14-day retention)
  - Plus: $39/seat/mo (10,000 traces, 400-day retention available at $5/1k)
  - Enterprise: Custom (SSO, custom retention, self-hosted options)

#### When Graph Abstraction Helps vs. Creates Overhead
**Helps when:**
- Workflows have conditional branching, loops, or parallel paths
- You need deterministic, debuggable control flow
- State persistence and checkpointing are required
- Production observability is critical

**Creates overhead when:**
- Simple linear pipelines (use plain LangChain or direct API calls)
- Rapid prototyping where the graph structure is unknown
- Small teams that don't need enterprise observability
- Single-agent scenarios with straightforward tool use

#### Strengths
- **Best observability:** LangSmith provides unmatched debugging and tracing
- **Predictable control flow:** Explicit graph means no surprises in production
- **State management:** Reducer-driven design with safe parallel execution
- **Production-tested:** Most battle-tested framework for complex stateful pipelines
- **Sub-millisecond overhead:** Direct tool execution, negligible framework tax

#### Weaknesses
- **Steepest learning curve:** Requires understanding graph theory concepts
- **Verbose for simple tasks:** Significant boilerplate for straightforward workflows
- **LangChain coupling:** While improving, still tied to the LangChain ecosystem
- **Cost:** LangSmith pricing can escalate quickly at scale ($2.50-5.00/1k traces)

---

### 1.4 Claude Agent SDK (Anthropic)

**GitHub:** anthropics/claude-agent-sdk-python | **Version:** Python 0.1.48, TypeScript 0.2.71
**Language:** Python, TypeScript | **License:** MIT

#### Architecture and Design Philosophy
Renamed from "Claude Code SDK" in late 2025 to reflect its evolution into a general-purpose agent runtime. Core architecture:

- **MCP-native:** Built around the Model Context Protocol (MCP) for tool interoperability
  - MCP Hosts (applications)
  - MCP Clients
  - MCP Servers (wrap REST APIs into uniform format)
- **Agent loop:** Same loop, tools, and context management that powers Claude Code
- **Built-in capabilities:** File operations, shell commands, web search, MCP integration
- **Skills system:** Filesystem-based configuration via SKILL.md files

#### Tool Use Patterns
- Custom Skills as directories with SKILL.md configuration
- MCP servers for external tool integration
- Built-in tools: file read/write, bash execution, web search, notebook editing
- Multi-agent orchestration through nested agent calls

#### How It Differs
- **MCP-first:** Only framework where MCP is the foundational architecture, not an add-on
- **Opinionated toward Claude:** Optimized for Anthropic models (though MCP is model-agnostic)
- **Runtime, not framework:** Provides the execution environment rather than abstract orchestration patterns
- **Production-proven:** Powers Claude Code, which is used by thousands of developers daily

#### Production Readiness
Active development with frequent releases (v0.x indicates pre-1.0, but widely used in production through Claude Code). The SDK is battle-tested through Claude Code's massive user base.

---

### 1.5 OpenAI Agents SDK

**GitHub:** openai/openai-agents-python | **Language:** Python
**License:** MIT

#### Architecture
Production-ready evolution of OpenAI's experimental Swarm project (March 2025). Deliberately minimalist with only **4 core primitives:**

1. **Agents:** LLMs with instructions and tools
2. **Handoffs:** Agent-to-agent delegation
3. **Guardrails:** Input/output validation
4. **Tracing:** Built-in visualization and debugging

#### Strengths
- **Minimal abstraction:** Lightest framework overhead of any production option
- **Provider-agnostic:** Works with 100+ LLMs via Chat Completions API
- **Built-in tracing:** Visualization, debugging, evaluation, and fine-tuning support
- **Realtime agents:** Voice agent support with gpt-realtime-1.5
- **Low learning curve:** 4 primitives to learn vs. dozens in other frameworks

#### Weaknesses
- **Limited orchestration patterns:** No graph-based workflows, limited to handoffs
- **OpenAI-optimized:** While provider-agnostic, best experience is with OpenAI models
- **Young framework:** Less production track record than LangGraph or CrewAI
- **No persistent state:** Less sophisticated state management than LangGraph

---

### 1.6 Pydantic AI

**GitHub:** 15,000+ stars | **Language:** Python
**License:** MIT

A rising contender that deserves attention alongside the "big three."

#### Architecture
- **Type-safe agents:** Leverages Python's type system to catch agent logic errors at development time
- **Model-agnostic:** 25+ model providers supported
- **Graph support:** Type-hint-driven graph definitions for complex workflows
- **Durable execution:** Preserves progress across API failures and restarts

#### Key Differentiators
- MCP, A2A, and UI event stream standards support
- Built-in evals via Pydantic Logfire
- Streamed structured output with immediate validation
- Human-in-the-loop workflow support
- Best-in-class type safety for catching bugs before production

#### Market Position
"LangGraph for complexity, CrewAI for speed, Pydantic AI for stability" -- this positioning has emerged as community consensus in early 2026.

---

## 2. Autonomous Coding Agents

### 2.1 Devin (Cognition)

**Type:** Commercial SaaS | **Founded:** 2024

#### Pricing (as of 2026)
| Tier | Price | Features |
|------|-------|----------|
| Core | $20/mo | Individual developers, basic ACUs |
| Team | $500/mo | Team features, higher ACU limits |
| Enterprise | Custom | SSO, compliance, dedicated support |

The dramatic price drop from $500 to $20/mo (Devin 2.0, April 2025) opened access to individual developers.

#### Effectiveness
- **Task completion:** ~15% success rate on complex tasks without assistance in independent testing
- **Sweet spots:** Web scraping, API integrations, boilerplate generation
- **Weak areas:** Complex recursive functions, ambiguous specifications
- **Enterprise claims:** Goldman Sachs pilot reported 20% efficiency gains (hybrid workforce model)
- **Improvement:** 83% more junior-level tasks per ACU vs. v1 (Cognition's internal benchmarks)

#### Assessment
Devin works best as a junior developer handling well-scoped, repetitive tasks with experienced engineers reviewing output. Not yet a replacement for senior engineering judgment.

---

### 2.2 OpenHands (formerly OpenDevin)

**GitHub:** 69,580 stars | **Language:** Python
**License:** MIT

#### Architecture
Full platform for AI software development:
- Web UI with multi-agent architecture
- SDK for composable Python agents
- Docker-based sandboxed execution
- Cloud scaling to 1000s of parallel agents
- Browser interaction, shell access, code editing

#### Performance (SWE-bench evaluations)
- SWE-bench Lite: 26% success rate
- HumanEvalFix: 79%
- WebArena: 15%
- GPQA (graduate-level QA): 53%

#### Strengths
Largest open-source coding agent community (3.7x SWE-agent's stars). Enterprise-ready features, active development, AMD partnership for local workstation deployment.

---

### 2.3 SWE-agent (Princeton)

**GitHub:** 18,817 stars | **Language:** Python
**License:** MIT

Research-focused coding agent with innovative Agent-Computer Interface (ACI). Set state-of-the-art on full SWE-bench when released (April 2024). Minimal footprint, designed for academic research and benchmarking rather than production use.

**Best for:** Research, benchmarking, understanding agent-code interaction patterns. Not recommended as a production tool.

---

### 2.4 Aider

**GitHub:** 41,000+ stars | **Installs:** 4.1M+ | **Language:** Python
**License:** Apache 2.0

#### Architecture
Git-first AI pair programming in the terminal:
- Every AI edit becomes a git commit with descriptive message
- Sessions can run on own branches
- Supports 100+ coding languages and 100+ LLM providers
- Read/write access to repository files
- Multi-file editing in a single conversation turn

#### Strengths
- **Most established CLI option** for open-source AI coding
- **Git-native:** Complete audit trail of all AI changes
- **Model flexibility:** Works with local models (Ollama) and all major providers
- **Human-in-the-loop:** Conversational pair-programming, not fully autonomous
- **Lightweight:** No complex setup, just `pip install aider-chat`

#### Best For
Developers who want AI assistance while maintaining control. Excellent for refactoring, adding features to existing codebases, and learning new codebases.

---

### 2.5 Codex CLI (OpenAI)

**GitHub:** openai/codex | **Language:** Rust
**License:** Open source

#### Architecture
Terminal-based coding agent built in Rust for speed:
- Reads, changes, and runs code in the selected directory
- Subagent support for parallel task execution
- Web search integration
- MCP support for third-party tools
- Scriptable via `exec` command

#### Key Details
- GPT-5.2-Codex is the latest model, optimized for long-horizon work
- Included with ChatGPT Plus/Pro/Business/Edu/Enterprise
- macOS and Linux native; Windows support experimental (WSL recommended)
- Context compaction for large codebases
- Strong cybersecurity capabilities

---

## 3. Other Notable Frameworks

### 3.1 MetaGPT

**GitHub:** 66,000 stars | **Version:** 0.8.1 | **Language:** Python

Role-based multi-agent framework simulating a software company:
- Product managers, architects, project managers, engineers as agents
- Takes a one-line requirement, outputs user stories, APIs, documentation
- Launched MGX (MetaGPT X) in Feb 2025 -- "world's first AI agent development team"
- Best for startups and lean product teams shipping fast

**Assessment:** High GitHub stars but last release was April 2024 (v0.8.1). Active research but may have stalled on framework development in favor of MGX product.

---

### 3.2 CAMEL

**GitHub:** 16,000 stars | **Language:** Python

Research-focused framework for studying agent scaling laws:
- Simulate up to 1M agents for emergent behavior studies
- OWL (Optimized Workforce Learning) -- accepted NeurIPS 2025
- OASIS -- million-agent social simulations
- 100+ researchers in the community

**Assessment:** Primarily a research tool. Valuable for understanding multi-agent dynamics but not designed for production deployment.

---

### 3.3 Smolagents (HuggingFace)

**GitHub:** ~10,000+ stars | **Language:** Python

Lightweight, code-first agent framework:
- **Code Agents:** Actions written as Python code (not JSON/text)
- Natural composability through code generation
- Multi-agent collaboration for complex tasks
- Deep HuggingFace ecosystem integration
- Agents Course on HuggingFace Learn

**Assessment:** Best for teams already in the HuggingFace ecosystem who want lightweight agents without framework overhead. The "actions as code" paradigm is elegant and powerful.

---

### 3.4 DSPy (Stanford NLP)

**GitHub:** 33,100 stars | **Version:** 3.1.3 | **Language:** Python

Not an agent framework per se, but a framework for **programming** (not prompting) language models:
- Declarative, composable modules for LM programs
- Automatic prompt optimization (MIPROv2, BetterTogether, LeReT)
- Works for classifiers, RAG pipelines, and agent loops
- Active development toward DSPy 3.0

**Assessment:** Complementary to agent frameworks rather than competitive. Use DSPy to optimize the prompts/weights inside your agents, regardless of orchestration framework. Powerful for teams investing in systematic prompt optimization.

---

### 3.5 Semantic Kernel / Microsoft Agent Framework

**GitHub:** ~25,000 stars (SK) | **Language:** .NET, Python, Java
**License:** MIT

Now being merged into Microsoft Agent Framework (see Section 1.2). Key enterprise features:
- Session-based state management
- OpenTelemetry native observability
- Azure Monitor, Entra ID integration
- CI/CD via GitHub Actions and Azure DevOps

**Status:** Semantic Kernel will be maintained for at least 1 year after Agent Framework GA (expected Q1 2026 end), with critical bugs and security fixes only. All new features go to Agent Framework.

---

## 4. Comparison Matrix

### 4.1 Multi-Agent Orchestration Frameworks

| Criterion | CrewAI | LangGraph | AutoGen/MS Agent Framework | Claude Agent SDK | OpenAI Agents SDK | Pydantic AI |
|-----------|--------|-----------|---------------------------|-----------------|-------------------|-------------|
| **Setup Time** | Minutes | Hours | Hours-Days | Minutes | Minutes | Minutes |
| **Learning Curve** | Low | High | High | Medium | Low | Medium |
| **Flexibility** | Medium (opinionated) | High (explicit graphs) | High (conversation patterns) | Medium (MCP-native) | Low (minimal primitives) | Medium-High |
| **Production Readiness** | High | Highest | Medium (in transition) | High (via Claude Code) | Medium | Medium-High |
| **Community Size** | 45.9k stars | ~20k stars | ~38k stars | Growing | Growing | 15k stars |
| **Activity Level** | Very Active | Very Active | Transitioning | Very Active | Active | Very Active |
| **Framework Cost** | Free (OSS) / $25-custom | Free (OSS) / $39+/seat | Free (OSS) | Free (OSS) | Free (OSS) | Free (OSS) |
| **Observability** | Basic | Best (LangSmith) | Good (OpenTelemetry) | Built-in | Built-in tracing | Logfire |
| **Token Efficiency** | Low (3x overhead) | High | Low (chat overhead) | High | Highest | High |
| **State Management** | Basic | Best (reducers) | Good (sessions) | Basic | Basic | Good (durable) |
| **MCP Support** | Native (v1.10+) | Via integration | Via integration | Native (foundational) | Via integration | Native |
| **Best Use Case** | Rapid prototyping, team workflows | Complex stateful pipelines | Conversational multi-agent | Coding agents, MCP ecosystems | Simple agents, voice apps | Type-safe production agents |

### 4.2 Autonomous Coding Agents

| Criterion | Devin | OpenHands | SWE-agent | Aider | Codex CLI | Claude Code |
|-----------|-------|-----------|-----------|-------|-----------|-------------|
| **Type** | Commercial | Open Source | Research | Open Source | Semi-Open | Commercial |
| **Stars/Adoption** | N/A (closed) | 69.6k | 18.8k | 41k | Open source | Massive |
| **Autonomy Level** | High (but ~15% complex success) | High | High | Medium (pair programming) | Medium-High | High |
| **Cost** | $20-500/mo | Free | Free | Free + API costs | ChatGPT subscription | Anthropic subscription |
| **Local Models** | No | Yes | Yes | Yes (Ollama) | No | No |
| **Git Integration** | Basic | Good | Research | Best (git-first) | Good | Good |
| **Best For** | Well-scoped repetitive tasks | Full-stack automation | Research/benchmarks | Interactive pair programming | OpenAI ecosystem devs | Anthropic ecosystem devs |

### 4.3 Supplementary Frameworks

| Framework | Stars | Primary Use | Production Ready | Solo-Friendly |
|-----------|-------|-------------|-----------------|---------------|
| MetaGPT | 66k | End-to-end software dev simulation | Moderate | Yes |
| DSPy | 33.1k | Prompt/weight optimization | Yes | Yes |
| CAMEL | 16k | Agent scaling research | No (research) | No |
| Smolagents | ~10k+ | Lightweight code agents | Moderate | Yes |
| Semantic Kernel | ~25k | Enterprise .NET/Azure agents | Yes (transitioning) | No |

---

## 5. For Solo Founders and Small Teams

### 5.1 Best Effort-to-Value Ratio

**Tier 1 -- Start here:**
1. **Direct API calls + custom orchestration** -- For developers comfortable with Python, a simple loop calling Claude/GPT with tool use often outperforms any framework for straightforward agent tasks. Zero framework overhead, complete control, no abstraction leaks.
2. **Pydantic AI** -- If you need structure beyond raw API calls, Pydantic AI adds type safety, model-agnosticism, and durable execution without heavy abstraction. The "Pythonic" feel makes it natural for experienced developers.
3. **CrewAI** -- When you genuinely need multi-agent collaboration, CrewAI gets you to production fastest. The role-based metaphor is intuitive and the community resources are excellent.

**Tier 2 -- When you need more:**
4. **LangGraph** -- When your workflows grow complex enough to need explicit state machines, conditional routing, and production observability. The learning curve investment pays off for long-lived, stateful agent systems.
5. **Claude Agent SDK** -- If you're building on Anthropic's ecosystem, this gives you the same runtime that powers Claude Code with MCP interoperability.

**Tier 3 -- Specialized:**
6. **OpenAI Agents SDK** -- Lightest abstraction if you're primarily using OpenAI models
7. **DSPy** -- When you need to systematically optimize prompts across your pipeline
8. **Smolagents** -- If you're deep in the HuggingFace ecosystem

### 5.2 Build vs. Buy vs. Compose

| Approach | When to Choose | Cost Profile | Control |
|----------|---------------|-------------|---------|
| **Build (no framework)** | You have strong Python skills, simple agent needs, want zero abstraction tax | API costs only | Maximum |
| **Compose (lightweight framework)** | You need multi-agent or stateful workflows but want to stay lean | API costs + minimal overhead | High |
| **Buy (managed platform)** | You need to ship fast and don't want to manage infrastructure | Subscription + API costs | Lower |

**For HUMMBL as a solo project:** The "compose" approach is most appropriate. Use direct API calls for simple tasks, bring in CrewAI or Pydantic AI when multi-agent patterns genuinely help, and avoid paying for managed platforms until revenue justifies it.

### 5.3 When a Framework Helps vs. Gets in the Way

**Framework HELPS when:**
- You have 3+ agents that need to coordinate
- Workflows require conditional branching or loops
- You need persistent state across agent interactions
- Observability and debugging are becoming pain points
- You're building for production reliability (retries, checkpointing)

**Framework GETS IN THE WAY when:**
- You're making a single agent with tool use (just use the API directly)
- The framework's abstractions don't match your mental model
- You spend more time fighting the framework than building features
- Simple tasks bloat to 3x token consumption (CrewAI's deliberation overhead)
- You're prototyping and the workflow shape isn't clear yet

### 5.4 The Case for No Framework

**Arguments for direct API calls:**
- **Zero abstraction tax:** No framework overhead on latency or tokens
- **Full control:** You understand every line of your agent loop
- **No breaking changes:** Framework version bumps can't break your code
- **Simpler debugging:** No framework internals to reason through
- **Faster iteration:** Change behavior by editing code, not fighting configuration

**A minimal agent loop in ~50 lines of Python** (system prompt + tool definitions + while loop + API call + tool execution) handles 80% of single-agent use cases. Multi-agent coordination can be added incrementally with simple function calls between agents.

**When this breaks down:**
- At scale (>10 agents, complex state), you're reimplementing framework features
- Team collaboration suffers without shared abstractions
- Observability and debugging become ad-hoc
- Production concerns (retries, checkpointing, HITL) require significant custom code

---

## 6. HUMMBL-Specific Recommendations

Given HUMMBL's architecture (solo project, experimental hummbl-dev repos, NemoClaw supervisor-worker pipeline, local inference on RTX 3080 Ti):

### Immediate (Now)
1. **Continue with direct API calls + Claude Agent SDK** for core development workflows
2. **Use Aider** for interactive pair programming on existing codebases
3. **Keep the "no framework" approach** for NemoClaw's supervisor-worker pipeline -- the custom orchestration gives you the control needed for experimental architecture

### Medium-term (When needed)
4. **Evaluate Pydantic AI** when type safety and durable execution become important for production HUMMBL services -- it aligns well with Python-first development
5. **Consider CrewAI** if/when HUMMBL needs customer-facing multi-agent workflows (e.g., GaaS platform agents)
6. **Use DSPy** to systematically optimize prompts for the dialectical analysis pipeline

### Avoid (For now)
- **LangGraph:** Overhead not justified until HUMMBL has complex stateful workflows at scale
- **Microsoft Agent Framework:** Enterprise-focused, in transition, too heavy for solo development
- **Devin:** $20/mo is cheap but 15% complex task success rate doesn't justify the dependency
- **MetaGPT:** Stalled development, better to build custom

### Architecture Principle
**Compose, don't commit.** Use lightweight wrappers that call frameworks when helpful but don't marry your architecture to any single framework. The agent framework landscape is moving too fast (2+ major breaking changes per year for most frameworks) to build deep dependencies.

---

## 7. Sources

### Framework Official Sources
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI Changelog](https://docs.crewai.com/en/changelog)
- [AutoGen - Microsoft Research](https://www.microsoft.com/en-us/research/project/autogen/)
- [AutoGen v0.4 Announcement](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)
- [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [LangGraph Official](https://www.langchain.com/langgraph)
- [LangSmith Pricing](https://www.langchain.com/pricing)
- [Claude Agent SDK Docs](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK Python GitHub](https://github.com/anthropics/claude-agent-sdk-python)
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [Pydantic AI](https://ai.pydantic.dev/)
- [Pydantic AI GitHub](https://github.com/pydantic/pydantic-ai)
- [DSPy GitHub](https://github.com/stanfordnlp/dspy)
- [DSPy Official](https://dspy.ai/)
- [MetaGPT GitHub](https://github.com/FoundationAgents/MetaGPT)
- [CAMEL GitHub](https://github.com/camel-ai/camel)
- [Smolagents Docs](https://huggingface.co/docs/smolagents/en/index)
- [OpenHands GitHub](https://github.com/OpenHands/OpenHands)
- [SWE-agent GitHub](https://github.com/SWE-agent/SWE-agent)
- [Aider GitHub](https://github.com/Aider-AI/aider)
- [Devin Pricing](https://devin.ai/pricing)

### Analysis and Comparison Articles
- [Definitive Guide to Agentic Frameworks in 2026 - SoftmaxData](https://softmaxdata.com/blog/definitive-guide-to-agentic-frameworks-in-2026-langgraph-crewai-ag2-openai-and-more/)
- [LangGraph vs CrewAI vs OpenAI Agents SDK 2026 - Particula](https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026)
- [Top 7 Agentic AI Frameworks in 2026 - AlphaMatch](https://www.alphamatch.ai/blog/top-agentic-ai-frameworks-2026)
- [CrewAI's 44k Stars - The Agent Times](https://theagenttimes.com/articles/44335-stars-and-counting-crewais-github-surge-maps-the-rise-of-the-multi-agent-e)
- [Microsoft Agent Framework Convergence - European AI Cloud Summit](https://cloudsummit.eu/blog/microsoft-agent-framework-production-ready-convergence-autogen-semantic-kernel)
- [Semantic Kernel + AutoGen - Visual Studio Magazine](https://visualstudiomagazine.com/articles/2025/10/01/semantic-kernel-autogen--open-source-microsoft-agent-framework.aspx)
- [CrewAI vs LangGraph vs AutoGen - DataCamp](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [AI Agent Framework Landscape 2025 - Medium](https://medium.com/@hieutrantrung.it/the-ai-agent-framework-landscape-in-2025-what-changed-and-what-matters-3cd9b07ef2c3)
- [2026 AI Agent Framework Decision Guide - DEV Community](https://dev.to/linou518/the-2026-ai-agent-framework-decision-guide-langgraph-vs-crewai-vs-pydantic-ai-b2h)
- [Devin 2.0 Price Drop - VentureBeat](https://venturebeat.com/programming-development/devin-2-0-is-here-cognition-slashes-price-of-ai-software-engineer-to-20-per-month-from-500)
- [Devin AI Review - Trickle](https://trickle.so/blog/devin-ai-review)
- [OpenHands vs SWE-Agent - Local AI Master](https://localaimaster.com/blog/openhands-vs-swe-agent)
- [Claude Code vs OpenAI Codex - Northflank](https://northflank.com/blog/claude-code-vs-openai-codex)
- [Choosing Agent Framework 2026 Data-Driven Guide - DEV Community](https://dev.to/lukaszgrochal/choosing-an-agent-framework-in-2026-a-data-driven-decision-guide-1mkk)
- [Top 11 AI Agent Frameworks - Vellum](https://vellum.ai/blog/top-ai-agent-frameworks-for-developers)
- [Best AI Coding Agents 2026 - Faros AI](https://www.faros.ai/blog/best-ai-coding-agents-2026)
- [SWE-bench Leaderboard](https://www.swebench.com/)

---

*Report generated 2026-03-23 for HUMMBL Project RQ-009*
