# Summary: RQ-009 -- Agent Framework Comparison (2025-2026)

**Source:** agent_frameworks_comparison_2026.md | **Date:** 2026-03-23

- **CrewAI leads for time-to-production in role-based multi-agent workflows** (45.9k stars, 12M+ daily executions). LangGraph is the most battle-tested for production stateful pipelines with best-in-class observability via LangSmith.
- **Microsoft Agent Framework (AutoGen + Semantic Kernel merger) targets enterprise GA by Q1 2026 end** but the transition from AutoGen 0.2 to 0.4 is a breaking change, creating adoption risk. Claude Agent SDK provides the most powerful coding-agent runtime via MCP. OpenAI Agents SDK is the lightest abstraction (4 core primitives).
- **For solo founders: direct API calls + lightweight orchestration often beats heavy frameworks.** When a framework helps, CrewAI or Pydantic AI offer the best effort-to-value ratio. The "no framework" approach remains viable for teams with strong Python fundamentals.
- **Key differentiator is state management and observability.** LangGraph's checkpoint-based persistence and LangSmith tracing create debuggable agent pipelines. Most other frameworks treat state as an afterthought.
- **HUMMBL-specific recommendation:** Given existing bus protocol architecture and append-only coordination model, avoid full framework lock-in. Use Claude Agent SDK for coding tasks, lightweight orchestration for the research pipeline, and maintain the ability to swap model providers without rewriting agent logic.
