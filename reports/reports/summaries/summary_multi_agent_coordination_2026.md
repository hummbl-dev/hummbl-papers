# Summary: RQ-005 -- Multi-Agent Communication Protocols and Coordination

**Source:** multi_agent_coordination_2026.md | **Date:** 2026-03-23

- **Stigmergic (artifact-based) coordination is well-validated for AI agents:** HUMMBL's append-only bus protocol is a textbook implementation of cognitive stigmergy -- agents coordinate by reading/writing shared artifacts rather than direct messaging. This pattern has strong theoretical grounding and growing production adoption.
- **Supervisor-worker pattern dominates production deployments:** Anthropic's own data shows 90.2% improvement over single-agent performance for research tasks. The practical sweet spot for solo operators is 3-5 agents with 5-6 tasks each using file-based coordination.
- **Four interoperability protocols are converging:** MCP (Model Context Protocol) as foundation, ACP (Agent Communication Protocol), A2A (Agent-to-Agent from Google), and ANP (Agent Network Protocol). Layered adoption path with MCP first, then A2A for inter-agent delegation.
- **Multi-agent outperforms single-agent for specific task types:** Parallelizable, breadth-first tasks that exceed single context windows -- exactly the kind of work the autoresearch pipeline targets. Not beneficial for deep, sequential reasoning tasks.
- **HUMMBL's architecture aligns with emerging best practices:** Append-only logs, shared task lists, and blackboard systems are the dominant patterns in production multi-agent systems in 2026.
