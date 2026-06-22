# Proposal P-001: Implement Secure MCP Profile

## Problem
The Model Context Protocol (MCP) is becoming the standard agent-tool interface, but it has no security model. Tools are trusted implicitly, creating lateral-movement risks that traditional API security cannot detect. See Finding F-002 for full threat analysis.

## Proposed Change
Implement a "Secure MCP Profile" as a HUMMBL governance extension that adds four security layers to any MCP server:

1. **Tool Risk Classification**
   - Every tool declares a risk level: `read`, `write`, `execute`, `network`, `destructive`
   - Agents have a maximum risk level they can invoke (configurable per agent)
   - Override requires delegation token with explicit scope

2. **Agent Identity Attestation**
   - Before tool invocation, the agent presents a signed delegation token
   - The MCP server verifies the token against the HUMMBL identity registry
   - Anonymous or expired tokens are rejected

3. **Immutable Tool-Call Logging**
   - Every tool call is logged to the governance bus as a JSONL event
   - Format: `{timestamp, agent_id, tool_name, params_hash, risk_level, result_hash}`
   - Logs are append-only and signed

4. **Circuit Breaker Integration**
   - Anomalous patterns (e.g., 10x normal call rate, first-ever destructive tool call) trigger HALF_OPEN state
   - HALF_OPEN requires human or high-trust agent approval for subsequent calls
   - OPEN state blocks all tool calls from that agent pending review

## Expected Impact
- **Security**: Reduces MCP lateral-movement risk from "implicit trust" to "explicit capability"
- **Compliance**: Provides audit trail for SOC 2, ISO 42001, and EU AI Act agent governance requirements
- **Market positioning**: Positions HUMMBL as the security layer for the MCP ecosystem

## Risk
- **Adoption friction**: MCP server authors must add risk classification metadata
- **Performance**: Identity attestation adds ~50ms per tool call (token verification)
- **Scope creep**: Could become a full MCP server framework instead of a security profile

## Implementation Plan
| Phase | Deliverable | Timeline |
|-------|-------------|----------|
| 1 | Draft Secure MCP Profile spec (markdown) | 1 week |
| 2 | Implement identity attestation in mcp-server repo | 2 weeks |
| 3 | Add tool-call logging to governance_bus.py | 1 week |
| 4 | Integrate circuit breaker with existing circuit_breaker.py | 1 week |
| 5 | Publish spec + blog post | 1 week |

## Acceptance Criteria
- [ ] All HUMMBL MCP servers pass Secure MCP Profile validation
- [ ] Tool-call logs are queryable via governance bus CLI
- [ ] Circuit breaker triggers correctly on anomalous patterns
- [ ] Performance overhead <100ms per tool call
- [ ] Spec published and shared with MCP community

## Related
- **Finding:** F-002 (MCP Security Landscape)
- **Queue ID:** RQ-2026Q3-002
- **Repos:** mcp-server, hummbl-governance, founder-mode
