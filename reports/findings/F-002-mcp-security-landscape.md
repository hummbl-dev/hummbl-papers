# Finding F-002: MCP Security — Emerging Threat Model

## Source
- **Queue ID:** RQ-2026Q3-002
- **Research Run:** 2026-06-20 (Phase 3 activation)
- **Sources Reviewed:** 12 papers/reports
- **Confidence:** Medium-High (0.75)

## Key Claim
The Model Context Protocol (MCP) is becoming the dominant agent-tool interface, but its security model is dangerously underspecified. Current implementations trust tools implicitly, creating a lateral-movement surface that traditional API security cannot detect.

## Evidence
1. **MCP adoption**: Anthropic, OpenAI, Google, and Microsoft have all adopted or announced MCP support in 2026.
2. **Tool permission model**: MCP servers declare capabilities but do not declare risk levels. A "read file" tool and a "delete database" tool have equivalent trust surfaces.
3. **Prompt injection via tools**: A compromised MCP server can return malicious instructions that override the agent's system prompt (demonstrated by multiple researchers in Q2 2026).
4. **No audit trail**: Standard MCP implementations do not log which tool was called with what parameters, making incident response impossible.

## Gaps Identified
- No standardized risk classification for MCP tools (e.g., "read-only" vs "destructive")
- No mechanism for agent-to-tool mutual authentication
- No standard for tool-call logging and replay

## Recommendation
HUMMBL should publish a "Secure MCP Profile" that adds:
1. Tool risk classification (read, write, execute, network, destructive)
2. Agent identity attestation before tool invocation
3. Immutable tool-call logging to the governance bus
4. Circuit breaker integration: auto-open on anomalous tool-call patterns

This positions HUMMBL as the security layer for the emerging MCP ecosystem, analogous to how OAuth became the security layer for REST APIs.

## Next Steps
- Draft the Secure MCP Profile specification
- Implement a prototype in the mcp-server repo
- Present at the next OWASP or AI security conference
