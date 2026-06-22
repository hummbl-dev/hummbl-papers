# RQ-001: Effective LLM Tool Use Patterns for Code Generation and Review (2025-2026)

**Research ID:** RQ-001
**Domain:** prompt_engineering
**Date:** 2026-03-23
**Status:** Completed
**Targets:** skills/mtsmu-review, skills/simplify, skills/tdd

---

## Executive Summary

This report synthesizes the state of the art in LLM tool use, code generation, and automated code review as of March 2026. The field has undergone rapid maturation: SWE-bench Verified scores jumped from ~65% (early 2025) to 80.9% (March 2026), AI code review tools now detect ~48% of real-world runtime bugs, and the agentic coding tool market has consolidated into four distinct categories. Key findings include the critical importance of edit format selection (which can swing performance by 2-3x independent of model quality), the emergence of context engineering as the primary bottleneck in agent performance, and persistent weaknesses in LLM security vulnerability detection (~30%+ false positive rates).

---

## 1. LLM Tool Use / Function Calling Best Practices

### 1.1 How Claude, GPT-4, and Gemini Handle Tool Use Differently

The three major providers have converged on similar capabilities but with important architectural differences:

**Claude (Anthropic)**
- Supports "interleaved thinking" where the model alternates between internal reasoning and tool use within a single turn. This allows Claude to reason about a problem, use a tool, analyze results, and continue reasoning without stopping.
- Uses the agent loop pattern for sequential tool calls rather than a direct parallel/sequential flag.
- Claude 4.5 Sonnet demonstrated autonomous rebuilding of Claude.ai's web application over ~5.5 hours with 3,000+ tool uses, establishing a benchmark for sustained agentic tool use.
- Tool Search Tool enables on-demand tool discovery rather than loading all definitions upfront, reducing context bloat.

**GPT-4/GPT-5 (OpenAI)**
- Provides a `parallel_tool_calls` parameter to explicitly disable parallel execution.
- Offers strict mode for function calling that ensures reliable schema adherence (recommended to always enable).
- Integrates reasoning directly into tool use with o-series models.

**Gemini (Google)**
- Supports multiple implementation approaches: OpenAPI JSON Schema or Python function definitions with automatic schema generation from docstrings.
- Provides an OpenAI-compatible API, enabling low-friction migration for existing OpenAI codebases.
- Handles parallel/sequential execution via `tool_config` parameter or agent loop patterns.

**Standardization Trend:** Aggregation gateways now standardize on OpenAI's tool format, allowing define-once-translate-everywhere workflows across providers.

### 1.2 Tool Use Patterns That Maximize Code Quality

Key patterns identified across the literature:

1. **Schema Precision:** Well-defined function schemas with clear descriptions, proper typing, and explicit required/optional field marking. Tool definitions consume tokens on every call, so conciseness matters.
2. **Flat Parameter Structures:** Flatten nested objects into single-depth key-value maps using dot-notation. This dramatically reduces hallucinated parameter nesting errors.
3. **Strict Mode:** Always enable strict schema validation where available. Best-effort parsing leads to subtle failures.
4. **Self-Contained Tool Descriptions:** Each tool should be unambiguous about when to use it. Per Anthropic's guidance: "if a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."
5. **Token-Efficient Tool Design:** Build tools that return structured, minimal outputs. Document return formats clearly since the LLM writes code to parse tool outputs.
6. **On-Demand Tool Loading:** Rather than presenting all tools upfront, use tool search/discovery to present only relevant tools for the current task.

### 1.3 Common Failure Modes in LLM Tool Use

A 2025 taxonomy from the University of Washington (Winston et al., AST 2025) categorizes tool-augmented LLM failures into two primary classes:

**Tool Selection Hallucination:**
- Selecting an incorrect but existing tool (wrong ML domain, similar name confusion)
- Inventing nonexistent tools
- Failing to select any tool when one is needed

**Tool Usage Hallucination:**
- **Hallucinated parameter names:** The model invents keys that "sound right" but don't exist in the schema
- **Wrong nesting depth:** Values placed at incorrect object depth
- **Dropped required fields:** Omission of mandatory parameters
- **Type mismatches:** Strings where integers are expected, etc.

**Execution Instability:**
- Malformed JSON in tool calls
- Loss of structure across multi-turn interactions
- Forgetting earlier decisions in long agent loops
- Inconsistent behavior across runs due to non-determinism

**Mitigation Strategies:**
- Generate tool definitions from OpenAPI/Swagger specs rather than hand-writing them
- Validate all parameters before execution
- Implement retry logic with structured error feedback
- Use constrained decoding / strict mode where available

### 1.4 Academic Papers on Tool-Augmented LLMs (2025-2026)

Key publications:

- **"A Survey on Code Generation with LLM-based Agents"** (arXiv, 2025) -- Comprehensive survey covering planning, memory, tool usage, and reflection components in code-generating agents.
- **"A Taxonomy of Failures in Tool-Augmented LLMs"** (Winston et al., AST 2025) -- Systematic classification of failure modes in tool-augmented systems.
- **"Reducing Tool Hallucination via Reliability Alignment"** (2025) -- Proposes alignment techniques specifically targeting tool selection and usage hallucinations.
- **"RPM-MCTS: Knowledge-Retrieval as Process Reward Model with Monte Carlo Tree Search for Code Generation"** (AAAI 2026) -- Combines retrieval with MCTS for improved code generation.
- **"Secure Code Generation via Online Reinforcement Learning with Vulnerability Reward Model"** (2026) -- Uses RL to optimize for security alongside correctness.
- **LLM4Code 2026** -- Dedicated workshop with multiple accepted papers on tool-augmented code LLMs.

### 1.5 Anthropic's Tool Use Documentation and Best Practices

Anthropic's official guidance emphasizes:

- **Context Engineering as the Bottleneck:** "Claude is already smart enough, but every organization has unique workflows, standards, and knowledge systems that Claude does not inherently know."
- **Just-in-Time Context Loading:** Maintain lightweight identifiers (file paths, links) and dynamically load data at runtime using tools. This mirrors human cognition.
- **Hybrid Context Model:** Combine upfront retrieval (e.g., CLAUDE.md files) with autonomous exploration capabilities (grep/glob navigation).
- **Progressive Disclosure:** Enable agents to incrementally discover relevant context through exploration, assembling understanding layer-by-layer.
- **Compaction for Long Horizons:** Summarize and reinitiate context with condensed message history. Preserve architectural decisions and unresolved issues while discarding redundant tool outputs.
- **Sub-Agent Architecture:** Delegate focused tasks to specialized sub-agents with clean context windows; each returns condensed summaries (1,000-2,000 tokens).
- **Few-Shot Examples:** "For language models, examples are the pictures worth a thousand words." Curate diverse, canonical examples rather than exhaustive edge case lists.

---

## 2. Code Generation Patterns

### 2.1 Agentic Coding Workflows (SWE-bench Results)

**SWE-bench Verified (March 2026 Leaderboard):**

| Rank | System | Score |
|------|--------|-------|
| 1 | Claude Opus 4.5 | 80.9% |
| 2 | Claude Opus 4.6 | 80.8% |
| 3 | Gemini 3.1 Pro | 80.6% |
| 4 | MiniMax M2.5 (open-weight) | 80.2% |
| 5 | GPT-5.2 | 80.0% |
| - | Claude Sonnet 4.6 | 79.6% |

**Important caveat:** OpenAI has stopped reporting Verified scores after finding training data contamination across all frontier models. SWE-Bench Pro (1,865 tasks across 41 repos in Python, Go, TypeScript, JavaScript) is now recommended for rigorous evaluation. Top scores on SWE-Bench Pro are dramatically lower: GPT-5 and Claude Opus 4.1 score only ~23%.

**Live-SWE-agent** achieves 77.4% on SWE-bench Verified without test-time scaling (outperforming all other software agents) and 45.8% on SWE-Bench Pro.

**Verdent** resolves 76.1% pass@1 and 81.2% pass@3 on SWE-bench Verified.

### 2.2 Edit vs. Rewrite Strategies

Five primary edit format approaches have emerged:

**1. Search/Replace Blocks (Aider's default)**
- Uses `<<<<<<< SEARCH` / `>>>>>>> REPLACE` delimiters
- Intuitive before/after transformation
- Best for targeted changes in known locations
- Aider uses layered matching: exact -> whitespace-insensitive -> fuzzy

**2. Unified Diff Format**
- Standard `+`/`-` prefix notation
- Efficient for multi-section modifications
- 70-80% accuracy on complex files due to pattern matching failures
- Works better when line numbers are dropped from hunk headers

**3. Patch Format (OpenAI Codex)**
- Structured syntax with operation markers and context lines
- Avoids direct reliance on line numbers; uses surrounding code for anchoring
- Trainable format (models can be fine-tuned specifically for it)

**4. Full-File Replacement**
- Returns complete modified file content
- Simple but inefficient for large files
- Risk of unintended modifications in untouched sections
- **Key finding:** Outperforms diff-based approaches for files under 400 lines (per Cursor's benchmarks)

**5. Dual-AI Application (Cursor's approach)**
- Primary LLM generates edit intent
- Dedicated "Apply" model (fine-tuned 70B) handles merge logistics
- Higher computational cost but more robust application
- Most production tools have moved toward this pattern

**Critical Insight:** Edit format selection swings performance dramatically independent of model quality. Aider's benchmarks show GPT-4 Turbo went from 26% to 59% solely from format change, but GPT-3.5 scored only 19% with the same format because it couldn't reliably produce valid diffs. "The format matters as much as the model."

### 2.3 Multi-File Code Generation Challenges

Repository-level code generation remains one of the hardest unsolved problems:

- **Cross-file dependency tracking:** Relevant context is spread across dozens or hundreds of files. Generated code must adhere to project-wide naming conventions, reference existing APIs correctly, and respect type hierarchies.
- **DependEval benchmark** (2025): Contains tasks for Repository Construction, Dependency Recognition, and Multi-file Editing. Even closed-source frontier models struggle with cross-file modifications.
- **ReCode-bench:** Multi-language benchmark (7 languages) with three repository-level tasks at varying granularity.
- **InlineCoder** (2025): Context inlining approach achieved average gains of 29.73% in EM, 20.82% in ES, and 49.34% in BLEU over strongest baselines on DevEval and RepoExec.
- **Multi-agent architectures** (MASAI, HyperAgent): Use specialized sub-agents for planning, localization, code generation, and testing, achieving significantly higher success on repository-level challenges.

### 2.4 Structuring Prompts for Reliable Code Edits

Best practices from 2025-2026 research:

1. **Specify the edit scope explicitly:** Tell the model exactly which files and functions to modify.
2. **Provide surrounding context:** Include adjacent code, imports, and type definitions.
3. **Use structured output formats:** Enforce JSON or XML-delimited responses for edit instructions.
4. **Separate planning from execution:** Have the model describe what it will change before generating the edit.
5. **Include test expectations:** Specify what tests should pass after the edit.

### 2.5 Diff-Based vs. Full-File Replacement Decision Framework

| Factor | Use Diff/Search-Replace | Use Full-File |
|--------|------------------------|---------------|
| File size | >400 lines | <400 lines |
| Change scope | Targeted, localized | Widespread restructuring |
| Model capability | Strong models (Opus, GPT-5) | Any model |
| Risk tolerance | Low (preserves untouched code) | Higher (can introduce drift) |
| Token efficiency | High | Low |
| Verification | Easy to review changes | Requires full diff comparison |

---

## 3. Code Review with LLMs

### 3.1 Effectiveness Studies

**Macroscope Code Review Benchmark (Sept 2025):**
- Dataset: 118 real-world runtime bugs across 45 repositories, 8 programming languages
- Methodology: Created PRs with bug-introducing commits; measured detection with default settings

| Tool | Bug Detection Rate | Avg Comments/PR |
|------|--------------------|-----------------|
| Macroscope | 48% | 2.55 |
| CodeRabbit | 46% | 10.84 |
| Cursor Bugbot | 42% | — |
| Greptile | 24% | — |
| Graphite Diamond | 18% | 0.62 |

**Language-specific variance is significant:** Macroscope detected 86% of Go bugs but only 36% of Swift bugs. CodeRabbit excelled in JavaScript (59%) and Rust (45%).

### 3.2 Bug Detection: LLMs vs. Human Reviewers

- Leading AI code review tools detect ~48% of real-world runtime bugs (best case).
- Human reviewers remain superior at detecting logic errors, architectural issues, and subtle concurrency bugs.
- AI reviewers excel at pattern-matching bugs (null checks, off-by-one errors, resource leaks) and maintaining consistency across large PRs.
- The primary value proposition is speed (reviews in <30 seconds) and consistency (no reviewer fatigue).

### 3.3 Security Vulnerability Detection

**Current state (2025-2026):**
- Best LLM-based vulnerability detection tools achieve <70% accuracy with 30%+ false positive rates.
- DeepSeek-R1 achieves 67% accuracy under context-rich evaluation, with F1-scores exceeding 70% for structurally consistent vulnerability categories.
- o1-mini shows the best false positive reduction performance.
- Prior evaluations that omitted contextual information significantly underestimated LLM capabilities.

**GitHub Copilot Code Review (2025-2026):**
- Research reveals Copilot "frequently fails to detect critical vulnerabilities such as SQL injection, cross-site scripting (XSS), and insecure deserialization."
- Feedback primarily addresses low-severity issues (coding style, typos).
- Copilot leaves "Comment" reviews only -- never "Approve" or "Request changes" -- so it cannot block merges.

**Key limitation:** LLMs are better at filtering false positives from static analysis than at primary vulnerability detection. Without strong initial detection from traditional tools, LLMs have nothing reliable to evaluate against.

### 3.4 False Positive Rates

- CodeRabbit generates the most comments (10.84/PR), suggesting higher noise but also higher recall.
- Graphite Diamond is quietest (0.62/PR) but detects fewer bugs (18%).
- The tradeoff between noise and detection remains fundamental; no tool has solved it.
- Datadog's approach of using LLMs specifically to filter false positives from static analysis shows promise as a complementary strategy.

### 3.5 AI Code Review Tools Landscape

| Tool | Strengths | Weaknesses | Pricing |
|------|-----------|------------|---------|
| **CodeRabbit** | Broad language support, 2M+ repos connected, 13M+ PRs reviewed | Verbose/noisy reviews | $24/dev/mo |
| **Macroscope** | Highest bug detection (48%), balanced noise | Newer entrant | $30/mo |
| **Sourcery** | Deep Python expertise, Pythonic refactoring | Narrow language focus, slow | $10/user/mo |
| **Cursor Bugbot** | Strong detection (42%), IDE integration | Tied to Cursor ecosystem | $40/mo |
| **Qodo (formerly Codium)** | Cross-repo context awareness | — | Varies |
| **GitHub Copilot Review** | Massive adoption (1 in 5 GitHub reviews), <30s reviews | Misses critical security issues | Included in Copilot |
| **SonarQube** | Best free/open-source option, deterministic rules | Not LLM-powered (hybrid) | Free tier |

---

## 4. Agentic Coding Tools Landscape (2025-2026)

The market has consolidated into four distinct categories by 2026:

### 4.1 Terminal Agents

**Claude Code (Anthropic)**
- Architecture: Terminal-native agent that reads codebases, edits files, runs commands, and integrates with development tools.
- Uses agentic search to map and understand entire codebases in seconds without manual context selection.
- Built on MCP (Model Context Protocol) for extensible tool integration.
- Agent SDK enables building custom agents with full control over orchestration, tool access, and permissions.
- Reached $1B annualized run rate within 6 months of launch.
- Best practices emphasize CLAUDE.md files for project context and progressive context disclosure.

**Aider**
- Open-source terminal-based AI pair programming tool.
- Diff-first workflow: proposes changes as diffs, shows them for review, auto-commits with descriptive messages.
- Multiple edit format support with automatic selection based on model and task.
- Architect mode for planning before execution.
- Repository map provides compressed whole-codebase representation within context window.
- Works with any LLM provider; best results with Claude 3.7 Sonnet, DeepSeek R1, GPT-4o.

### 4.2 AI-Native IDEs

**Cursor**
- VS Code fork rebuilt around AI-native workflows.
- Multi-model support: GPT-5.2, Claude Opus 4.6, Gemini 3 Pro, Grok Code, and proprietary models.
- Cursor Composer provides multi-file reasoning with step-by-step planning.
- Dedicated "Apply" model (fine-tuned 70B) for robust edit application.
- Background agents for long-running tasks (refactoring, test monitoring, PR reviews).
- Cursor 2.5 (Feb 2026) introduces long-running agents and Composer 1.5.

**Windsurf (formerly Codeium)**
- VS Code-based IDE acquired by Cognition AI for ~$250M (Dec 2025).
- Cascade: agentic AI system for whole-codebase understanding and multi-file edits.
- Ranked #1 in LogRocket AI Dev Tool Power Rankings (Feb 2026).
- $82M ARR at acquisition, 350+ enterprise customers.
- Pricing: Free (25 credits/mo), Pro $15/mo, Teams $30/user/mo, Enterprise $60/user/mo.

### 4.3 IDE Plugins

**GitHub Copilot**
- Largest installed base; added free tier in 2024-2025.
- Code review feature accounts for >1 in 5 GitHub code reviews.
- In 71% of reviews, surfaces actionable feedback; 29% silent.
- Primarily catches low-severity issues; misses critical security vulnerabilities.

### 4.4 Fully Autonomous Agents

**Devin (Cognition AI)**
- Devin 2.0 (April 2025): price dropped from $500 to $20/mo Core plan.
- 83% more junior-level tasks per Agent Compute Unit vs. Devin 1.x.
- SWE-bench: 13.86% end-to-end resolution (7x improvement over previous AI models).
- Goldman Sachs pilot (July 2025) with 12,000 developers; 20% efficiency gains reported.
- Acquired Windsurf to expand from autonomous-only to IDE-assisted workflows.

**OpenHands (formerly OpenDevin)**
- Open-source, model-agnostic platform for cloud coding agents.
- 2.1K contributions from 188+ contributors.
- Deployed across SWE-bench, GPQA (cross-domain QA), and WebArena (web automation).
- Key differentiator: model-agnostic and self-hostable.

### 4.5 What Works and What Doesn't

**What works in practice:**
- Targeted edits to well-defined, isolated functions
- Test generation and boilerplate code
- Bug fixes with clear reproduction steps
- Code review for pattern-matching bugs
- Codebase navigation and understanding
- Commit message and PR description generation

**What doesn't work reliably:**
- Large-scale architectural refactoring across many files
- Security vulnerability detection as a primary tool
- Fully autonomous multi-day development tasks
- Code generation without human review in production
- Understanding implicit business logic not captured in code

---

## 5. Prompt Engineering for Code Tasks

### 5.1 Chain-of-Thought vs. Direct Generation

**Structured Chain-of-Thought (SCoT)** for code generation outperforms direct generation by 15.27% in correctness and 36.08% in bad smells (code quality), per published benchmarks.

Key findings:
- CoT prompting is the state-of-the-art approach for code generation tasks requiring reasoning.
- Combining CoT with few-shot examples yields the best results on complex tasks.
- For simple, well-defined tasks (string manipulation, basic CRUD), direct generation is sufficient and faster.
- For algorithmic or multi-step logic, CoT significantly improves correctness.
- Semantic Chain of Thought (SeCoT) adds semantic understanding to structural reasoning, further improving results.

### 5.2 Few-Shot Examples in Coding Prompts

Best practices:
- Curate diverse, canonical examples rather than exhaustive edge case lists.
- Examples should demonstrate the desired output format, not just the logic.
- 2-3 high-quality examples outperform 10+ mediocre ones.
- Include examples that show common error patterns and their corrections.
- For code editing tasks, show before/after pairs with the edit format you expect.

### 5.3 System Prompt Patterns for Coding Agents

Effective system prompts for coding agents follow a consistent structure:

1. **Identity and Scope:** Define the agent's role, capabilities, and operational boundaries.
2. **Domain Knowledge:** Embed project-specific conventions, required libraries, forbidden patterns, and style guides.
3. **Tool Descriptions:** Self-contained, non-overlapping tool definitions with clear usage criteria.
4. **Structured Organization:** Use XML tags or Markdown headers to separate sections. "Boring prompts are often the most reliable ones."
5. **Output Contracts:** Explicitly specify the expected response format.
6. **Safety Boundaries:** Refusal categories and protocols for out-of-scope requests.
7. **Delimiter Strategy:** XML-like tags separate rules from content, preventing prompt injection and confusion.

**Advanced patterns:**
- ReAct loops (Reasoning + Acting) for multi-step tool use
- Context caching to avoid recomputing embeddings for stable documentation
- Progressive instruction loading based on task type

### 5.4 Context Window Management for Large Codebases

The fundamental challenge: enterprise monorepos span millions of tokens, but even 1M-token context windows have degraded attention at the periphery.

**Strategies ranked by effectiveness:**

1. **Sub-Agent Architecture:** Delegate focused tasks to specialized agents with clean context windows. Each sub-agent explores extensively but returns condensed summaries (1,000-2,000 tokens).

2. **RAG-Based Retrieval:** Vector database of code embeddings enables "perfect recall" of entire codebases. Used by most production tools.

3. **Repository Maps:** Compressed whole-codebase representation (Aider's approach) providing bird's-eye view without full context consumption.

4. **Observation Masking:** Target environment output only while preserving action and reasoning history. Makes sense because agent turns heavily skew toward observation.

5. **LLM Summarization:** Periodically summarize accumulated context. Preserve architectural decisions and unresolved issues while discarding redundant tool outputs.

6. **Structured Context Injection:** Use XML-style tags to separate context sections. Models handle large volumes of structured context better than unstructured.

7. **Just-in-Time Loading:** Maintain file paths and references; load content only when needed. Claude Code's CLAUDE.md + grep/glob pattern exemplifies this.

---

## 6. Evaluation and Benchmarks

### 6.1 Current State of the Art

**SWE-bench Verified (March 2026):**
- Top score: 80.9% (Claude Opus 4.5)
- Contamination concerns: OpenAI stopped reporting Verified scores after finding training data contamination across all frontier models.
- Major scaffold upgrade in February 2026 (environments, token limits).

**SWE-bench Pro (recommended for rigorous evaluation):**
- 1,865 tasks across 41 repos (Python, Go, TypeScript, JavaScript)
- Top score: ~46% (Live-SWE-agent) -- dramatically lower than Verified
- Top model-only scores: ~23% (GPT-5, Claude Opus 4.1)

**SWE-rebench:**
- 21,000+ interactive Python tasks for RL training of SWE agents
- Designed to be contamination-free

**HumanEval / MBPP:**
- Largely saturated: o1-mini achieves 96.2% on HumanEval; Claude Sonnet 4 has only 2 failures across 164 tasks.
- HumanEval Pro and MBPP Pro introduced for more challenging self-invoking code generation, where performance drops significantly (o1-mini: 96.2% -> 76.2%).
- BigCodeBench positioned as "next generation" of HumanEval.

### 6.2 Real-World vs. Benchmark Performance

The gap between benchmarks and reality is substantial:

- **Contamination:** Every frontier model shows training data contamination on SWE-bench Verified (per OpenAI's analysis).
- **SWE-bench Pro gap:** Models scoring 80%+ on Verified score only ~23% on Pro, suggesting Verified significantly overestimates real-world capability.
- **Self-invoking tasks:** When problems require building on previous solutions (HumanEval Pro), performance drops 20+ percentage points.
- **Multi-language gap:** Most benchmarks are Python-heavy. Performance on Go, TypeScript, and JavaScript is generally lower.

### 6.3 Evaluating Code Generation Quality in Production

Recommended evaluation framework:

1. **Functional Correctness:** Does the code pass existing tests? Does it handle edge cases?
2. **Test Generation Quality:** Can the model generate meaningful tests that catch regressions?
3. **Edit Precision:** Does the change modify only what was intended? No collateral damage?
4. **Code Quality Metrics:** Linting scores, type safety, naming conventions.
5. **Review Overhead:** How much human review time is needed post-generation?
6. **Security Posture:** Does generated code introduce vulnerabilities? (Use static analysis as ground truth.)
7. **Time-to-Merge:** Total time from task assignment to merged PR.
8. **Revert Rate:** How often are AI-generated changes reverted after merge?

---

## 7. Key Takeaways for HUMMBL

### 7.1 Immediate Actionable Insights

1. **Edit format matters as much as model selection.** For HUMMBL's coding agents, implement search/replace blocks for files >400 lines and full-file replacement for smaller files. Consider training or using a dedicated apply model for robust edit application.

2. **Context engineering is the primary lever.** Invest in CLAUDE.md files, repository maps, and sub-agent architectures rather than chasing marginally better models. Anthropic's guidance: "Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

3. **Tool definitions should be auto-generated from specs.** Hand-written tool definitions are a top source of hallucinated parameters. Generate from OpenAPI/Swagger specs and validate.

4. **AI code review is complementary, not replacement.** Best tools catch ~48% of runtime bugs. Use AI review for first-pass screening (pattern bugs, style, basic logic) and human review for security, architecture, and business logic.

5. **Security review requires traditional tools.** LLMs alone have >30% false positive rates and miss critical vulnerabilities (SQLi, XSS). Layer LLMs on top of CodeQL/ESLint/SAST for false positive filtering.

### 7.2 Architecture Recommendations

1. **Adopt sub-agent patterns for complex tasks.** Specialized agents (planner, coder, tester, reviewer) with clean context windows outperform single-agent approaches on repository-level tasks.

2. **Implement progressive context disclosure.** Start with high-level codebase maps, drill into relevant files on demand. Claude Code's grep/glob + CLAUDE.md pattern is production-proven.

3. **Use compaction for long-running tasks.** Summarize periodically, preserving architectural decisions and unresolved issues while discarding redundant tool outputs.

4. **Build evaluation pipelines.** Track functional correctness, edit precision, review overhead, and revert rates. SWE-bench Pro is the most credible external benchmark.

### 7.3 Risks and Open Questions

1. **Benchmark contamination is pervasive.** All frontier models show contamination on SWE-bench Verified. Rely on SWE-bench Pro or custom evaluation sets.

2. **Fully autonomous coding is not production-ready.** Even Devin achieves only ~14% on SWE-bench. Human-in-the-loop remains essential.

3. **Multi-file generation is unsolved.** Cross-file modifications remain the hardest challenge. Multi-agent architectures show the most promise but add complexity.

4. **The tool landscape is consolidating rapidly.** Cognition (Devin) acquired Windsurf. GitHub Copilot is ubiquitous but shallow. Claude Code and Cursor are the current leaders for serious development work.

---

## Sources

### Tool Use and Function Calling
- [Function Calling Complete Guide 2026 (oFox)](https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/)
- [Claude Sonnet 4 Tool Calling vs GPT-4 & Gemini (Arsturn)](https://www.arsturn.com/blog/claude-sonnet-4-tool-calling-vs-gpt-4-gemini-a-deep-dive)
- [Function Calling in LLM Agents (Symflower)](https://symflower.com/en/company/blog/2025/function-calling-llm-agents/)
- [Function Calling (OpenAI API)](https://developers.openai.com/api/docs/guides/function-calling)
- [Advanced Tool Calling in LLM Agents (SparkCo)](https://sparkco.ai/blog/advanced-tool-calling-in-llm-agents-a-deep-dive)
- [Implementing Function Calling in LLM Applications (DasRoot)](https://dasroot.net/posts/2026/02/implementing-function-calling-llm-applications/)
- [3 Patterns That Fix LLM API Calling (Dev.to)](https://dev.to/docat0209/3-patterns-that-fix-llm-api-calling-stop-getting-hallucinated-parameters-4n3b)

### Failure Modes
- [Taxonomy of Failures in Tool-Augmented LLMs (UW, AST 2025)](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- [Reducing Tool Hallucination via Reliability Alignment (arXiv)](https://arxiv.org/html/2412.04141v1)
- [LLM Failure Modes in Agentic Scenarios (arXiv)](https://arxiv.org/html/2512.07497v1)
- [Failure Modes in LLM Systems: System-Level Taxonomy (arXiv)](https://arxiv.org/abs/2511.19933)

### Code Generation
- [A Survey on Code Generation with LLM-based Agents (arXiv)](https://arxiv.org/html/2508.00083v1)
- [LLM4Code 2026 Accepted Papers](https://llm4code.github.io/papers/)
- [Code Surgery: How AI Assistants Make Precise Edits (Hertwig)](https://fabianhertwig.com/blog/coding-assistants-file-edits/)
- [AI Code Edit Formats Guide 2025 (Morph)](https://www.morphllm.com/edit-formats)
- [Aider Edit Formats](https://aider.chat/docs/more/edit-formats.html)
- [Unified Diffs Make GPT-4 Turbo 3X Less Lazy (Aider)](https://aider.chat/docs/unified-diffs.html)
- [The Harness Problem (Can.ac)](https://blog.can.ac/2026/02/12/the-harness-problem/)
- [DependEval: Benchmarking LLMs for Repository-Level Code (ACL 2025)](https://aclanthology.org/2025.findings-acl.373.pdf)
- [InlineCoder: Repository-Level Code Generation via Context Inlining (arXiv)](https://arxiv.org/html/2601.00376v1)

### Code Review
- [Code Review Benchmark (Macroscope)](https://macroscope.com/blog/code-review-benchmark)
- [AI-powered Code Review with LLMs: Early Results (arXiv)](https://arxiv.org/html/2404.18496v2)
- [State of AI Code Review Tools 2025 (DevTools Academy)](https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/)
- [GitHub Copilot Code Review: Can AI Spot Security Flaws? (arXiv)](https://arxiv.org/abs/2509.13650)
- [60 Million Copilot Code Reviews (GitHub Blog)](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- [Using LLMs to Filter False Positives (Datadog)](https://www.datadoghq.com/blog/using-llms-to-filter-out-false-positives/)

### Security Vulnerability Detection
- [LLMs Cannot Reliably Identify Security Vulnerabilities (BU)](https://www.bu.edu/peaclab/files/2024/05/saad_ullah_llm_final.pdf)
- [From Large to Mammoth: Comparative Evaluation (NDSS 2025)](https://www.ndss-symposium.org/wp-content/uploads/2025-1491-paper.pdf)
- [Everything You Wanted to Know About LLM-based Vulnerability Detection (arXiv)](https://arxiv.org/pdf/2504.13474)

### Agentic Coding Tools
- [Claude Code Overview (Anthropic)](https://code.claude.com/docs/en/overview)
- [Best Practices for Claude Code (Anthropic)](https://code.claude.com/docs/en/best-practices)
- [Eight Trends Defining How Software Gets Built in 2026 (Claude Blog)](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)
- [Effective Context Engineering for AI Agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Cursor AI Review 2026 (NxCode)](https://www.nxcode.io/resources/news/cursor-review-2026)
- [Windsurf Review 2026 (VibeCoding)](https://vibecoding.app/blog/windsurf-review)
- [Aider - AI Pair Programming](https://aider.chat/)
- [OpenHands: AI-Driven Development (GitHub)](https://github.com/OpenHands/OpenHands)
- [Devin AI Complete Guide (DigitalApplied)](https://www.digitalapplied.com/blog/devin-ai-autonomous-coding-complete-guide)

### Benchmarks
- [SWE-bench Leaderboards](https://www.swebench.com/)
- [SWE-bench Verified (Epoch AI)](https://epoch.ai/benchmarks/swe-bench-verified)
- [SWE-Bench Pro (Scale AI)](https://scale.com/blog/swe-bench-pro)
- [Live-SWE-agent (arXiv)](https://arxiv.org/html/2511.13646v3)
- [HumanEval Pro and MBPP Pro (ACL 2025)](https://aclanthology.org/2025.findings-acl.686/)
- [BigCodeBench (HuggingFace)](https://huggingface.co/blog/leaderboard-bigcodebench)

### Prompt Engineering
- [Structured Chain-of-Thought Prompting for Code Generation (ACM TOSEM)](https://dl.acm.org/doi/10.1145/3690635)
- [Prompt Engineering Guide 2026 (IBM)](https://www.ibm.com/think/prompt-engineering)
- [Context Engineering for Multi-Agent LLM Code Assistants (arXiv)](https://arxiv.org/html/2508.08322v1)
- [Context Window Management at Scale (Thread Transfer)](https://thread-transfer.com/blog/2025-07-11-context-window-at-scale/)
- [The Context Window Problem (Factory.ai)](https://factory.ai/news/context-window-problem)
- [Efficient Context Management (JetBrains Research)](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)
