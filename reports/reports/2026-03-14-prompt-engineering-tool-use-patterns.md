# Effective LLM Tool Use Patterns for Code Generation and Review (2025-2026)

**Research Report RQ-001** | Date: 2026-03-14

## Executive Summary

The period from mid-2025 through early 2026 has seen a decisive shift in how LLMs are applied to software engineering tasks. The field has moved from simple code completion toward agentic architectures where models reason about tasks, invoke tools iteratively, and validate their own outputs. This report surveys the key patterns, benchmarks, and production systems that define the current state of the art.

## 1. The ReAct Pattern and Its Evolution

The ReAct (Reasoning + Acting) framework, originally introduced by Yao et al. (2022), has become the foundational architecture for tool-augmented code generation agents. The core loop is straightforward: the model generates a reasoning trace, selects and executes a tool action, observes the result, and repeats until the task is complete.

In code generation specifically, the ReAct pattern manifests as:

1. **Thought**: The model reasons about the current state of the codebase, the task requirements, and what information it needs.
2. **Action**: The model invokes a tool -- reading a file, running a search, executing a test suite, or writing code to a file.
3. **Observation**: The tool output is fed back into the model's context.
4. **Iteration**: The model decides whether to continue (more information needed, tests failing) or terminate (task complete).

This pattern has proven more reliable than single-shot code generation because it grounds the model's decisions in actual codebase state rather than relying purely on parametric knowledge. Simon Willison's widely-referenced implementation (https://til.simonwillison.net/llms/python-react-pattern) demonstrates the simplicity of the core loop in under 100 lines of Python.

A significant evolution in 2025 has been the emergence of **Plan-and-Execute** as a complement to ReAct. Where ReAct interleaves planning and execution at every step, Plan-and-Execute separates the two phases: the model first generates a complete plan, then executes each step sequentially. Production systems increasingly use hybrid approaches -- planning at the macro level, then using ReAct loops for individual step execution. LangGraph has formalized this into a graph-based execution model where nodes represent different agent states and edges represent transitions (https://www.promptingguide.ai/techniques/react).

## 2. Tool-Augmented Code Generation Architectures

The dominant tool set for agentic code generation has converged around a small number of primitives:

- **File read/write/edit**: Direct filesystem operations with diff-based editing to minimize token consumption.
- **Shell execution**: Running tests, linters, build commands, and git operations.
- **Code search**: Grep-style content search and glob-based file discovery across repositories.
- **Web search/fetch**: Retrieving documentation, API references, and error resolution guidance.

The Trae system, which achieved state-of-the-art performance on SWE-bench, exemplifies this architecture. It uses a `str_replace_editor` tool for browsing and editing files, a `Bash` tool for executing arbitrary commands, and a Code Knowledge Graph (CKG) component that enables semantic `search_class` and `search_function` operations across the repository (https://www.zenml.io/llmops-database/ai-powered-automated-issue-resolution-achieving-state-of-the-art-performance-on-swe-bench).

Anthropic's approach to tool use has evolved substantially. The Claude API now supports programmatic tool calling, where the model writes code that calls tools within a sandboxed execution container rather than requiring round trips through the model for each invocation. This reduces both latency and token consumption for multi-step tool workflows. Additionally, the Tool Search feature allows agents to access thousands of tools without consuming context window space, addressing a key scaling bottleneck in complex agent architectures (https://www.anthropic.com/engineering/advanced-tool-use).

Multi-model orchestration has also emerged as a production pattern. Rather than relying on a single LLM, systems like Trae leverage multiple commercial models (Claude, Gemini, OpenAI) for generation, providing resilience against single-model failures and exploiting the complementary strengths of different architectures.

## 3. Code Review Automation: Benchmarks and Findings

A comprehensive survey by researchers covering 99 papers from 2015-2025 (https://arxiv.org/abs/2602.13377) documents the shift from pre-LLM to LLM-era code review. The field has moved from rule-based static analysis toward end-to-end generative peer review, with increasing multilingual coverage.

Key benchmarks in this space include:

**SWR-Bench** introduces 1,000 manually verified Pull Requests from GitHub with PR-centric review and full project context. Its LLM-based evaluation method achieves approximately 90% agreement with human judgment. A notable finding: LLMs trained with reasoning-focused approaches exhibit better code review capabilities, and current tools are more adept at detecting functional errors than non-functional issues like outdated documentation (https://arxiv.org/abs/2509.01494).

**ContextCRBench** (https://arxiv.org/abs/2511.07017) evaluates three scenarios: hunk-level quality assessment, line-level defect localization, and line-level comment generation. A critical finding is that textual context (commit messages, PR descriptions, issue text) yields greater performance gains than additional code context alone. Current LLMs remain far from human-level review ability.

**SWE-bench Pro** (https://arxiv.org/html/2509.16941) extends the original SWE-bench with long-horizon tasks requiring hours to days for professional engineers. LLM agents achieve only 17.8-23.3% resolution rates on these tasks, compared to over 70% on simpler SWE-bench Verified instances, underscoring the gap between benchmark performance and real-world software engineering complexity.

A study evaluating LLMs for code review directly (https://arxiv.org/html/2505.20206v1) found significant error rates: regression rates reaching 23.79% and inaccurate approval decisions at 44.44%. Incorporating problem descriptions into prompts consistently improved performance, highlighting that code review quality depends heavily on the contextual information provided to the model.

## 4. Production Patterns That Work

Based on the research literature and the trajectory of production tools, several patterns have proven effective:

### 4.1 Test-Driven Validation Loops

The most reliable pattern for agentic code generation is the test-driven validation loop. The agent writes or identifies relevant tests, generates code, runs the tests, and iterates until they pass. This is a direct application of ReAct to the red-green-refactor cycle. The Trae system's "Tester agent" component automatically retrieves regression tests from the project codebase relevant to the issue description and validates them against both the original and patched code.

### 4.2 Repository-Scale Context Management

Claude Code, which achieved a 72.5% score on autonomous task completion benchmarks in 2025 and commands a 46% "most loved" rating among developers (https://render.com/blog/ai-coding-agents-benchmark), was designed specifically for repository-scale changes: API migrations, dependency upgrades, and pattern enforcement across hundreds of files. Its approach of supporting up to 1M tokens of context, combined with targeted file search rather than whole-repository ingestion, represents the current best practice for managing large codebases.

### 4.3 Multi-Tool Composition

Production agents now routinely compose 5-10 tools in a single task. The pattern of parallel tool invocation -- reading multiple files simultaneously, running independent searches in parallel -- has become standard. Claude Code's architecture, for example, supports parallel tool calls within a single response turn, reducing the number of round trips required for information gathering (https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

### 4.4 Diff-Based Editing Over Full Rewrites

Token efficiency demands that agents edit files using targeted string replacements rather than rewriting entire files. This pattern also reduces the risk of unintended changes and makes the agent's modifications easier to review. The `str_replace_editor` pattern used by multiple SWE-bench-competitive agents has become the de facto standard.

### 4.5 Guardrails and Circuit Breakers

Production deployments increasingly wrap agentic loops with safety mechanisms: token budgets, iteration limits, file-write restrictions, and human-in-the-loop checkpoints for destructive operations. The Anthropic Agent SDK provides these primitives out of the box, reflecting lessons learned from early deployments where unconstrained agents could enter expensive infinite loops or make cascading destructive changes.

## 5. Open Challenges

Despite rapid progress, several challenges remain:

- **Long-horizon tasks**: The drop from 70%+ on SWE-bench Verified to under 24% on SWE-bench Pro indicates that current agents struggle with tasks requiring sustained reasoning across many files and steps.
- **Non-functional review**: LLMs are significantly better at catching functional bugs than identifying documentation staleness, performance regressions, or security vulnerabilities during code review.
- **Context window limits**: Even with 1M token contexts, large repositories exceed what can be ingested. Effective retrieval and search strategies remain critical and under-researched relative to their importance.
- **Evaluation methodology**: Human agreement with LLM-based evaluation proxies sits around 90%, meaning 1 in 10 judgments diverges -- a meaningful error rate for automated code review at scale.

## 6. Conclusions

The effective patterns for LLM tool use in code generation have converged: ReAct-style reasoning loops, a small set of well-defined tools (file ops, shell, search), test-driven validation, and diff-based editing. The gap between benchmark performance and real-world utility remains significant, particularly for long-horizon tasks and non-functional code review. The most productive current approach is human-agent collaboration -- using LLM agents for exploration, initial generation, and mechanical refactoring, while retaining human judgment for architectural decisions and nuanced review.

## References

1. Yao, S., et al. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. https://arxiv.org/abs/2210.03629
2. Jimenez, C.E., et al. "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" ICLR 2024. https://arxiv.org/abs/2310.06770
3. "A Survey of Code Review Benchmarks and Evaluation Practices in Pre-LLM and LLM Era." 2025. https://arxiv.org/abs/2602.13377
4. "Benchmarking and Studying the LLM-based Code Review." 2025. https://arxiv.org/abs/2509.01494
5. "Benchmarking LLMs for Fine-Grained Code Review with Enriched Context in Practice." 2025. https://arxiv.org/abs/2511.07017
6. "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" 2025. https://arxiv.org/html/2509.16941
7. "Evaluating Large Language Models for Code Review." 2025. https://arxiv.org/html/2505.20206v1
8. "Introducing Advanced Tool Use on the Claude Developer Platform." Anthropic, 2025. https://www.anthropic.com/engineering/advanced-tool-use
9. "Tool Use with Claude." Anthropic API Documentation. https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
10. "Testing AI Coding Agents (2025): Cursor vs. Claude, OpenAI, and Gemini." Render Blog, 2025. https://render.com/blog/ai-coding-agents-benchmark
11. Willison, S. "A Simple Python Implementation of the ReAct Pattern for LLMs." https://til.simonwillison.net/llms/python-react-pattern
12. "AI Tooling for Software Engineers in 2026." Pragmatic Engineer. https://newsletter.pragmaticengineer.com/p/ai-tooling-2026
