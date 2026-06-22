# RQ-006: Capability-Based Security and Object-Capability Models for Agent Systems

**Research ID**: RQ-006
**Domain**: capability_security
**Date**: 2026-03-23
**Target Components**: `services/delegation_token`, `services/governance_bus`
**Status**: Completed

---

## Executive Summary

Capability-based security provides the most natural authorization model for multi-agent systems because it treats authority as a transferable, attenuable, cryptographically verifiable token rather than an identity-checked policy lookup. This report surveys the foundations of capability security (from Dennis & Van Horn 1966 through modern CHERI hardware), maps existing capability systems (Cap'n Proto, Hardened JavaScript, Capsicum, WASI) to agent system design, analyzes how leading AI platforms handle permissions today, and proposes a minimum viable capability architecture for HUMMBL's governance bus and delegation token services.

**Key finding**: 93% of popular AI agent projects in 2026 still rely on unscoped API keys, 0% implement per-agent identity, and 100% lack granular revocation. Capability-based authorization directly addresses all three gaps.

---

## 1. Capability-Based Security Fundamentals

### 1.1 Object-Capability Model (OCap) — Principles and History

The capability concept originates from Dennis and Van Horn's 1966 paper "Programming Semantics for Multiprogrammed Computations," which introduced a **C-list** (capability list) per process — each capability naming an object and specifying permitted access rights. A capability is "a token, ticket, or key that gives the possessor permission to access an entity or object in a computer system."

The object-capability model (ocap) refines this into a programming paradigm where:

1. **Capabilities are unforgeable references** — holding a reference to an object is the sole way to exercise authority over it
2. **No ambient authority** — programs cannot access anything they were not explicitly granted
3. **Authority flows through message passing** — capabilities are transferred by sending object references between communicating parties
4. **Encapsulation is security** — standard information hiding and modularity directly enforce access control

Mark S. Miller's 2006 PhD thesis "Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control" (Johns Hopkins) formalized the relationship between object capabilities and least authority across four layers of abstraction. Miller's earlier work on the **E programming language** demonstrated that capability security could be built into a practical, distributed programming environment with promise pipelining and cryptographic references.

Key papers in the lineage:
- Dennis & Van Horn, 1966 — original capability concept
- Lampson, 1971 — protection and access control matrices
- Miller, Yee & Shapiro, 2003 — "Capability Myths Demolished"
- Miller, 2006 — "Robust Composition" (ocap as unifying model)
- Murray, 2008 — "Analysing Object-Capability Security" (formal analysis)
- Stefan & Mitchell, 2011 — "Analysing Object-Capability Patterns with Murphi"

### 1.2 CHERI (Capability Hardware Enhanced RISC Instructions)

CHERI extends conventional ISAs with hardware-enforced capabilities for memory safety and compartmentalization. Developed at the University of Cambridge Computer Laboratory, CHERI encodes capabilities as fat pointers that carry bounds, permissions, and an integrity tag enforced by the CPU.

**ARM Morello** is the evaluation platform for CHERI on ARMv8.2-A:
- Fabricated in 7nm with four out-of-order cores at 2.5 GHz
- Shipped as evaluation boards in January 2022
- Runs CheriBSD (modified FreeBSD)
- CHERI Alliance now distributes boards for research

**Current status (2025-2026)**:
- ARM has **no roadmap** to include Morello/CHERI in production architectures — it remains a research platform
- UKRI announced GBP 21 million in November 2025 to support CHERI technology transition
- A CHERI Research Centre was founded at Cambridge in 2025 with UK government support
- Genode OS Framework (release 25.02, February 2025) extends multi-monitor capabilities with least-authority scoping
- Google Fuchsia F24 (January 2025) reinforces least-authority in observability tooling

**Relevance to agent systems**: CHERI demonstrates that capability enforcement at the hardware level eliminates entire classes of memory-safety vulnerabilities. For agent systems running on untrusted infrastructure, hardware-backed capabilities would provide a root of trust for capability tokens. While production CHERI is not yet available, the design principles inform software-level capability token design.

### 1.3 Principle of Least Authority (POLA) in Practice

POLA (also called Principle of Least Privilege / PoLP) requires that every module access only the information and resources necessary for its legitimate purpose. In capability systems, POLA emerges naturally:

- **No ambient authority**: A process cannot open arbitrary files, network connections, or observe global state unless it holds the specific capability
- **Authority is explicit**: Every permission is traceable to a delegation act
- **Attenuation by default**: Delegating a subset of authority is the natural operation; expanding authority is structurally impossible

Miller's insight is that POLA fails in traditional systems because programs inherit the full authority of the user who runs them. Object capabilities fix this by making authority a first-class data structure that must be explicitly passed, never implicitly inherited.

**For agent systems**: An agent should receive precisely the capabilities required for its current task — not the union of all capabilities its human principal possesses. Every delegation hop should narrow scope.

### 1.4 Capabilities vs ACLs — When Each Is Appropriate

| Dimension | Access Control Lists (ACLs) | Capabilities |
|-----------|---------------------------|-------------|
| **Organization** | Per-object: who can access this resource? | Per-subject: what can this entity access? |
| **Authority source** | Identity + policy lookup | Possession of unforgeable token |
| **Delegation** | Requires admin intervention | Holder can delegate (with attenuation) |
| **Revocation** | Centralized, immediate | Distributed; via expiration or revocation lists |
| **Ambient authority** | Present (user identity grants access) | Eliminated (only held tokens grant access) |
| **Confused deputy** | Vulnerable | Structurally prevented |
| **Administration** | Easier with few users, many objects | Easier with many users, dynamic delegation |
| **Audit** | Centralized logs | Requires explicit logging at use sites |

**When ACLs are appropriate**:
- Stable organizational hierarchies with relatively static permissions
- Systems where centralized revocation is critical
- Cases requiring "who accessed this resource?" queries
- Traditional enterprise IT with well-defined roles

**When capabilities are appropriate**:
- Dynamic delegation between autonomous agents
- Cross-organizational interactions without shared identity providers
- Systems requiring offline authorization (no policy server needed)
- Preventing confused-deputy attacks in complex call chains
- Multi-agent workflows where authority must attenuate at each hop

**For HUMMBL**: Capability-based authorization is the correct model for the governance bus and delegation tokens. The coordination bus mediates between autonomous agents that may be running different models on different machines — a fundamentally decentralized scenario where ACLs would require a centralized policy server bottleneck.

---

## 2. Capabilities in Agent/AI Systems

### 2.1 Constraining Agent Permissions with Capability Tokens

The 2026 "State of Agent Security" report (Grantex) auditing 30 popular AI agent projects found:
- **93%** rely exclusively on unscoped API keys
- **0%** implement per-agent identity systems
- **97%** lack user consent mechanisms
- **100%** have no granular revocation capabilities

This represents a critical security gap. The recommended capability token structure for agents:

```
CapabilityToken {
  scope:       [tool:file_read, resource:/data/project-x/*.csv]
  holder:      <agent_public_key>
  issuer:      <delegating_agent_or_human_public_key>
  issued_at:   2026-03-23T14:00:00Z
  expires_at:  2026-03-23T14:05:00Z
  chain:       [signature_of_parent_token, ...]
  caveats:     [max_calls:10, environment:staging]
}
```

Key properties:
- **Holder-bound**: Cryptographic binding to the agent's key prevents token theft from granting authority
- **Time-bounded**: Short expiration windows (seconds to minutes for high-risk operations)
- **Scope-bounded**: Specific tools, resources, and actions enumerated
- **Chain-verifiable**: Each delegation hop signed, proving lineage back to the human principal

### 2.2 Delegation Tokens — Safe Authority Transfer

Authority must be "constructed, passed, and monotonically reduced as data." The **monotonic reduction principle** states that derived capabilities cannot exceed parent scope across any dimension:

```
Human Principal
  └─ Agent A: [read, write] on /project-x/ (expires 1h)
       └─ Agent B: [read] on /project-x/data/ (expires 5m)
            └─ Agent C: [read] on /project-x/data/summary.csv (expires 30s)
```

Each delegation hop:
1. Signs the new token with the delegator's key
2. Narrows scope (fewer tools, narrower resource paths)
3. Shortens expiration
4. Adds caveats (rate limits, environment restrictions)
5. Cannot add tools, widen paths, or extend expiration

### 2.3 Revocation Patterns

Four primary revocation strategies for agent capabilities:

1. **Short-lived tokens with no refresh** — the simplest approach; authority expires automatically. Appropriate for task-scoped operations.

2. **Revocation lists** — a centralized (or replicated) list of revoked token IDs. Adds latency but enables immediate revocation of compromised tokens.

3. **Epoch-based revocation** — tokens are valid only within a numbered epoch; incrementing the epoch invalidates all outstanding tokens. Useful for emergency stops.

4. **Capability-specific kill switches** — the issuer retains a revocation handle that can signal downstream holders. Requires a communication channel.

**For HUMMBL's governance bus**: Combine (1) short-lived tokens for routine operations with (3) epoch-based emergency revocation. The bus maintains an epoch counter; all token validation checks the current epoch.

### 2.4 Anthropic's Approach to Agent Permissions and Safety

Anthropic's "Framework for Developing Safe and Trustworthy Agents" (2025) outlines five principles:

1. **Human control with autonomy balance** — humans retain control over high-stakes decisions
2. **Transparency** — agents show reasoning for verification
3. **Value alignment** — ongoing evaluation of behavioral alignment
4. **Privacy protection** — no information leakage between interaction contexts
5. **Security against manipulation** — defenses against prompt injection and tool exploitation

Claude Code implements:
- **Read-only by default** — analysis without approval, consent required for modifications
- **Layered permission rules** — `allowed_tools` and `disallowed_tools` with project-level overrides
- **Hooks for programmatic control** — `PreToolUse` hooks can approve, deny, or modify tool calls at runtime
- **MCP tool scoping** — MCP tools follow `mcp__<server>__<tool>` naming; permission config is the final gate regardless of server-advertised capabilities

**Key design principle**: "If a tool is denied at any level, no other level can allow it" — deny-wins semantics prevent privilege escalation through configuration layering.

### 2.5 OpenAI's Approach to Tool Permissions

OpenAI's Agent Builder safety guidance recommends:

- **Risk-tiered tools**: Classify each tool as low/medium/high risk based on read-only vs write, reversibility, account permissions, and financial impact
- **Guardrails as agents**: Input and output guardrails can be LLM-powered agents or rule-based functions
- **Tripwire mechanism**: Guardrail violations raise exceptions, halting the agent
- **Tool-level guardrails**: Run on every custom function-tool invocation, pre- and post-execution
- **Human escalation**: High-risk operations pause for human approval

The OpenAI Agents SDK is provider-agnostic with documented paths for non-OpenAI models, focusing on tool use, handoffs, guardrails, and tracing.

### 2.6 Google's A2A Protocol Security Model

The Agent2Agent (A2A) protocol, launched April 2025 and now under the Linux Foundation, provides:

- **Enterprise-grade auth**: Parity with OpenAPI authentication schemes
- **Agent Cards**: Signed metadata describing agent capabilities and security requirements (v0.3 adds card signing)
- **gRPC support** (v0.3): Enables bidirectional streaming with built-in TLS
- **OpenTelemetry integration**: Every request/response carries trace IDs; agents emit structured logs and metrics in OTLP format
- **Resource-scoped tokens**: Agents request tokens specifying the intended recipient, preventing token reuse across services

A2A is designed to complement MCP (Model Context Protocol), with A2A handling agent-to-agent communication and MCP handling agent-to-tool communication. The protocol now has 50+ technology partners.

---

## 3. Existing Capability Systems

### 3.1 Cap'n Proto — Capability-Based RPC

Cap'n Proto implements capability-based RPC based on the CapTP protocol from the E language:

- **Capabilities as first-class types**: Interface references can be passed as parameters, embedded in structs, or included in lists
- **Promise pipelining**: Chained method calls collapse into single network round trips ("time travel"), eliminating latency from sequential object interactions
- **Designation = permission**: Only object creators initially hold capabilities; network transmission grants receivers permission while excluding others
- **Connection-specific IDs**: Host-assigned IDs prevent capability forging
- **Confused deputy prevention**: Capabilities combine designation and permission, structurally preventing misuse
- **Distributed object introduction**: If Alice (machine A) sends Bob (machine B) a reference to Carol (machine C), Bob forms a direct connection to Carol

**Limitations**: Not robust against resource exhaustion / DoS attacks. TLS is the application's responsibility.

**Cloudflare Workers** uses Cap'n Proto's capability model for multi-tenant isolation, preventing privilege escalation by confining access to explicitly shared stubs and methods.

**Agent system mapping**: Cap'n Proto's RPC model is directly applicable to a coordination bus. Each agent endpoint is a capability object; delegation means passing a reference. The bus never needs a centralized permission table — holding the reference *is* the permission.

### 3.2 Secure EcmaScript (SES) / Hardened JavaScript

Hardened JavaScript (SES), a TC39 standards track proposal, provides three mechanisms:

1. **Lockdown**: Freezes and hardens shared JavaScript intrinsics (Array, Object, Date, Math), making them safe to share and immune to prototype pollution
2. **Compartments**: Sandboxes with isolated global objects but shared intrinsics. A compartment is "endowed with" specific capabilities through its `globals` parameter
3. **Harden**: `harden(object)` transitively freezes an object graph, making capabilities safe for multi-party sharing

The ocap principle applies directly: authority derives from object references, not naming. Confined code can only access what it was explicitly given through compartment endowments.

**Production usage**: Agoric (smart contracts) and MetaMask (plugin sandboxing) use Hardened JavaScript in production.

**Limitation**: Cannot protect against denial-of-service through resource exhaustion within a realm.

**Agent system mapping**: If agents are implemented in JavaScript/TypeScript (as with many MCP servers), Hardened JavaScript provides process-level capability isolation. Each agent runs in a Compartment with only the capabilities it needs, enforced by the language runtime.

### 3.3 CloudABI (Deprecated)

CloudABI was "POSIX with capability-based security and everything incompatible removed." Processes could not open files by absolute path, open network connections, or observe global system state.

Based on FreeBSD's Capsicum framework, CloudABI was implemented for FreeBSD (x86-64, arm64), with patches for NetBSD and Linux.

**Deprecated in October 2020** in favor of WebAssembly System Interface (WASI), which achieves similar goals with broader adoption.

**Historical significance**: CloudABI proved that capability-based POSIX was feasible and influenced WASI's design.

### 3.4 Capsicum (FreeBSD)

Capsicum is a lightweight capability framework built into FreeBSD (9.0+, default in 10.0+):

- **File descriptors as capabilities**: Once a process enters capability mode, it can only derive new file descriptors from existing ones
- **`cap_enter()`**: Irreversibly enters capability mode, eliminating access to global namespaces
- **`cap_rights_limit()`**: Restricts rights on a file descriptor (e.g., read-only)
- **Casper daemon**: Provides services to sandboxed components that lack the rights to implement those services

FreeBSD base-system applications using Capsicum: tcpdump, auditdistd, hastd, dhclient, kdump, rwhod, ctld, iscsid, uniq.

As described: "Capsicum eliminates ambient authority, while seccomp restricts it. One locks the door and removes it from the hinges. The other hires a bouncer and hopes the guest list is complete."

**Agent system mapping**: Capsicum's approach of "enter sandbox after acquiring needed resources" maps directly to agent initialization: an agent opens its required tool connections and data sources, then enters a restricted mode where it cannot acquire new capabilities without explicit delegation.

### 3.5 WebAssembly WASI — Capability-Oriented System Interface

WASI (WebAssembly System Interface) is the most active capability-based system interface in 2026:

- **Capability-based by design**: Wasm modules can only access explicitly granted resources — no global filesystem, network, or environment access by default
- **WASI Preview 2** (stable): Modular APIs defined with Wit IDL, broader language support, more expressive type system, virtualizability
- **WASI 0.3.0** (February 2026): Significant milestone with async support and expanded networking
- **WASI Sockets**: TCP/UDP, HTTP client/server, TLS — all standardized in 2025-2026
- **Inspired by CloudABI and Capsicum**: Draws directly from the capability-security lineage

**Agent system mapping**: WASI is the strongest candidate for agent sandboxing in 2026. Each agent runs as a Wasm module with explicitly granted capabilities:
- File access scoped to specific directories
- Network access scoped to specific endpoints
- Tool access mediated by the host runtime
- Near-native performance with strong isolation guarantees

### 3.6 Capability System Comparison for Agent Design

| System | Language/Runtime | Capability Granularity | Production Ready | Agent Fit |
|--------|-----------------|----------------------|-----------------|-----------|
| Cap'n Proto | C++/Rust/others | Object-level RPC | Yes | Bus protocol |
| Hardened JS | JavaScript | Object-level | Yes | MCP server isolation |
| Capsicum | C (FreeBSD) | File descriptor | Yes | Process sandboxing |
| WASI | Any → Wasm | Module-level I/O | Yes (Preview 2) | Agent runtime |
| CloudABI | C (deprecated) | Process-level | No | Historical reference |
| CHERI | Hardware | Memory pointer | Research only | Future hardware trust |

---

## 4. Agent Permission Patterns

### 4.1 Claude Code's Permission Model

Claude Code implements a layered permission system:

- **Default deny for writes**: Read/analysis operations proceed without approval; modifications require explicit consent
- **Static rules**: `allowed_tools` and `disallowed_tools` in project and user settings
- **Deny-wins semantics**: If denied at any level, no other level can override
- **Hooks**: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` hooks enable programmatic control
- **MCP scoping**: Each MCP server has its own permission scope; tools follow `mcp__<server>__<tool>` naming
- **Persistent grants**: Users can grant one-time or permanent access for trusted routine tasks

This is effectively a **static capability system** — permissions are defined at configuration time, not dynamically delegated. It works well for single-agent developer tool use but would need extension for multi-agent delegation.

### 4.2 MCP Server Authorization

The MCP specification has evolved significantly:

- **Original (2025-03)**: MCP servers could be both resource servers and authorization servers
- **June 2025 revision**: MCP servers classified as OAuth Resource Servers, separate from Authorization Servers
- **OAuth 2.1 + PKCE**: The core authentication model
- **Resource Indicators (RFC 8707)**: Clients must specify the intended MCP server, preventing token reuse
- **November 2025 update**: Explicit guidance addressing security risks

**Key issues identified**:
- Early spec coupled authorization and resource serving, creating complexity
- Token reuse across MCP servers was possible without Resource Indicators
- SSRF vulnerabilities: 7,000+ MCP servers found vulnerable, 492 with zero authentication
- Best practice: Separate resource server from authorization server; MCP server validates tokens, does not issue them

### 4.3 OAuth 2.0 Scopes as Capabilities

OAuth scopes approximate capabilities but fall short:

**Similarities**:
- Define specific access levels (e.g., `read:transactions`, `write:payments`)
- Can be narrowed during delegation (requesting fewer scopes)
- Time-bounded via token expiration

**Limitations**:
- Scopes were never designed as an authorization mechanism — they control delegation, not access
- Fine-grained systems create hundreds of scopes, exceeding JWT size limits
- Cannot express resource-instance-level restrictions (e.g., "this specific file" vs "all files")
- No support for attenuation chains or cryptographic delegation lineage
- Bearer tokens: possession equals access (no holder binding)

**Best practice**: Use OAuth scopes as a coarse outer boundary, with a policy engine making fine-grained decisions within scope boundaries.

### 4.4 Fine-Grained vs Coarse-Grained Permissions

| Aspect | Coarse-Grained | Fine-Grained |
|--------|----------------|-------------|
| Example | "Agent can use filesystem" | "Agent can read /data/project-x/*.csv" |
| Security | Higher blast radius | Minimal blast radius |
| Usability | Simpler to configure | Requires careful specification |
| Performance | Fewer checks | More checks per operation |
| Maintenance | Easier to manage | Can become complex |
| Agent fit | Acceptable for trusted, local agents | Required for cross-trust-boundary delegation |

**Recommendation for HUMMBL**: Start with coarse-grained tool-level capabilities (can/cannot use a tool), then add resource-level restrictions as the system matures. The governance bus should enforce tool-level capabilities from day one.

### 4.5 Time-Bounded and Scope-Bounded Capabilities

Best practices from 2025-2026 agent security research:

- **Risk-tiered expiration**: High-risk scopes (write, delete, execute) expire in seconds to minutes; low-risk scopes (read) can last hours
- **Task-scoped lifecycle**: Authority appears when delegation occurs and disappears when task completes
- **No refresh for high-risk tokens**: Require re-delegation rather than automatic refresh
- **Context-aware bounds**: Permissions can include environment restrictions (staging vs production), rate limits, and time-of-day windows
- **Bound tokens**: Kubernetes-style binding where the token is valid only for a specific agent identity and audience

---

## 5. Governance and Audit Trails

### 5.1 Logging Capability Use for Audit

Every capability exercise should produce an audit record:

```
AuditRecord {
  timestamp:       2026-03-23T14:02:33.847Z
  agent_id:        agent-b-7f3a
  capability_id:   cap-9x2k
  tool:            file_read
  resource:        /data/project-x/summary.csv
  result:          success
  delegation_chain: [human-reuben -> agent-a-4d1e -> agent-b-7f3a]
  epoch:           42
}
```

Key requirements:
- **Reconstruct the "why"**: Inputs, intermediate reasoning, tool invocations, and state changes
- **Link actions to authorization grants**: Every audit record references the capability that authorized it
- **Structured format**: Machine-parseable for automated compliance checking

### 5.2 Append-Only Audit Logs (HUMMBL Governance Bus)

Append-only logs are the strongest guarantee for audit integrity:

- **No update/delete operations**: The API physically cannot modify past records
- **Periodic integrity hashing**: Hash chains (each record includes the hash of the previous) create tamper evidence
- **Architecture**: Collection (OpenTelemetry SDK) → Processing (OTel Collector with integrity hashing) → Append-only storage backend

**Implementation options for HUMMBL**:
1. **SQLite in WAL mode with append-only table** — simplest for solo-founder stack
2. **File-based JSONL with hash chain** — each line is a JSON record; each includes SHA-256 of the previous line
3. **OpenTelemetry pipeline** — if the system already uses OTel for observability

**Recommended for HUMMBL**: Option 2 (JSONL with hash chain) aligns with the existing `system_health_log.jsonl` pattern and requires no additional infrastructure.

### 5.3 Capability Attenuation Through Delegation Chains

Attenuation is the core security property of capability delegation:

- Each delegation hop **intersects** the parent's scope with the requested scope — never unions
- Token formats supporting attenuation:

**Macaroons** (Google, 2014):
- Chained HMAC construction: each caveat is a new HMAC layer
- Adding caveats is trivial (one HMAC); removing is cryptographically impossible
- Third-party caveats enable cross-domain authorization
- Limitation: Shared-secret model; verifier needs the root secret

**Biscuit tokens** (Clever Cloud):
- Public-key cryptography (unlike macaroons' shared secret)
- Datalog-based authorization language for expressive policies
- Offline delegation: create valid attenuated tokens without contacting any server
- Any holder of the root public key can verify (no shared secrets)

**Wafers** (emerging):
- Combines macaroon-style caveats with public-key verification
- Designed specifically for multi-agent delegation chains

**Recommendation for HUMMBL**: Biscuit tokens are the best fit. Public-key verification means the governance bus can validate tokens without holding secrets for every agent. The Datalog policy language can express complex attenuation rules.

### 5.4 Formal Verification of Capability Systems

Approaches to proving capability system properties:

- **Model checking with Murphi**: Stefan & Mitchell (2011) verified object-capability patterns against safety properties
- **Zero-Infrastructure Capability Graphs** (ZI-CG, 2026): All trust-relevant information as self-contained, cryptographically signed statements; correctness verifiable without online infrastructure
- **Datalog-based verification**: Biscuit tokens use Datalog, which is decidable and can be formally verified
- **Type-system enforcement**: Capability-safe languages (E, Monte) use the type system to enforce capability properties at compile time

For a solo-founder stack, formal verification of the full system is impractical. However, using a well-studied token format (Biscuit) and keeping the capability model simple enough for manual reasoning provides adequate assurance.

---

## 6. Practical Patterns for Multi-Agent Systems

### 6.1 How a Coordination Bus Should Enforce Capabilities

The HUMMBL governance bus should act as a **capability mediator**, not a policy engine:

```
┌─────────────────────────────────────────────┐
│              Governance Bus                   │
│                                               │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  │
│  │ Token     │  │ Audit     │  │ Epoch    │  │
│  │ Validator │  │ Logger    │  │ Manager  │  │
│  └──────────┘  └───────────┘  └──────────┘  │
│                                               │
│  Validates: signature chain, scope, expiry,   │
│  epoch, holder binding                        │
│  Logs: every capability exercise              │
│  Revokes: epoch increment for emergency stop  │
└─────────────────────────────────────────────┘
         ▲                    ▲
         │ cap token          │ cap token
    ┌────┴────┐          ┌───┴────┐
    │ Agent A │──deleg──▶│ Agent B│
    │ (write) │          │ (read) │
    └─────────┘          └────────┘
```

The bus does NOT:
- Store a master permission table (no ACL)
- Look up agent identity in a directory
- Make authorization decisions based on "who is calling"

The bus DOES:
- Validate that the presented capability token is cryptographically valid
- Verify the delegation chain traces back to a trusted root
- Check that the token's scope covers the requested operation
- Check that the token has not expired and the epoch is current
- Log the capability exercise to the append-only audit trail

### 6.2 Preventing Privilege Escalation in Agent Chains

The 2025 arxiv paper "Open Challenges in Multi-Agent Security" identifies several escalation vectors:

**Agent session smuggling**: A sub-agent embeds hidden instructions in responses that parent agents execute. Mitigation: sanitize inter-agent messages; treat agent output as untrusted input.

**Cross-agent privilege escalation**: Compromised agents modify peer configuration. Mitigation: agents cannot modify each other's configuration; capability tokens are the only way to exercise authority.

**Heterogeneous attacks**: Multiple "safe" agents with complementary capabilities coordinate to bypass individual safeguards (43% success vs <3% individually). Mitigation: defense in depth; the bus enforces capability boundaries regardless of agent behavior.

**Cascade failures**: One compromised agent infects others through shared communication channels. Research shows infectious jailbreaks can spread to one million agents in logarithmic hops. Mitigation: network partitioning; the bus limits which agents can communicate.

**Six recommended authorization primitives** (from the State of Agent Security 2026 report):
1. Scoped tokens
2. Per-agent identity
3. User consent flows
4. Granular revocation
5. Immutable audit trails
6. Delegation controls with scope narrowing

### 6.3 Trust Boundaries Between Agents

Trust boundaries should align with three dimensions:

1. **Model provider boundary**: Agents running different model providers (Claude, GPT, Gemini, local Ollama) should not share credentials or raw capability tokens across providers
2. **Execution environment boundary**: Agents on different machines (Desktop RTX vs Nodezero MBP) require network-verifiable capabilities, not shared-memory references
3. **Task boundary**: Even within one model/machine, agents working on different tasks should hold separate, non-transferable capabilities

The Cloud Security Alliance's "Securing the Agentic Control Plane" (March 2026) framework emphasizes:
- Identity-first design with formal agent identity structures
- Runtime authorization (not just configuration-time)
- Continuous assurance rather than point-in-time audits
- Classification of agent capabilities by risk level
- Real-time visibility into inter-agent activity

### 6.4 Minimum Viable Capability System for a Solo-Founder Agent Stack

For HUMMBL's current stage (solo founder, experimental agent stack), a pragmatic MVP:

**Phase 1 — Token Foundation**:
```python
# Biscuit-inspired token structure (simplified)
@dataclass
class CapabilityToken:
    tool_scopes: list[str]        # ["file:read", "llm:query"]
    resource_patterns: list[str]  # ["/data/project-x/*"]
    issuer_key: str               # Public key of delegator
    holder_key: str               # Public key of agent
    expires_at: datetime          # Short-lived
    epoch: int                    # Must match bus epoch
    parent_signature: str         # Signature of parent token
    caveats: dict                 # {"max_calls": 10, "env": "staging"}
```

**Phase 2 — Bus Enforcement**:
- Token validation on every tool call through the bus
- Append-only JSONL audit log with hash chain
- Epoch counter for emergency revocation
- Simple CLI to inspect and revoke tokens

**Phase 3 — Delegation**:
- Agent-to-agent delegation with mandatory attenuation
- Delegation depth limit (e.g., max 3 hops)
- Automated expiration without refresh for delegated tokens

**Phase 4 — Maturation**:
- Migrate to proper Biscuit token library
- Add Datalog policy language for complex rules
- WASI-based agent sandboxing
- OpenTelemetry integration for audit pipeline

---

## 7. Recommendations for HUMMBL

### 7.1 Immediate Actions (This Sprint)

1. **Define the capability vocabulary** for the governance bus: enumerate all tools and resource types that agents will access
2. **Implement a minimal token validator** in the bus: signature check, expiry check, scope check
3. **Start the append-only audit log**: JSONL with hash chain, one file per day, recording every tool invocation with the authorizing capability

### 7.2 Near-Term (Next Month)

4. **Assign per-agent identity**: Each agent instance gets a keypair; the public key is its identity
5. **Implement delegation with attenuation**: When Agent A delegates to Agent B, the new token's scope is the intersection of A's scope and the requested scope
6. **Add epoch-based emergency stop**: A single counter in the bus that, when incremented, invalidates all outstanding tokens

### 7.3 Medium-Term (Next Quarter)

7. **Adopt Biscuit tokens**: Replace the simplified token with a proper Biscuit implementation for Datalog-based policies
8. **Integrate with MCP authorization**: Ensure MCP server tools are subject to the same capability checks as bus-mediated tools
9. **WASI sandboxing evaluation**: Test running agents as Wasm modules with WASI capability restrictions

### 7.4 Design Principles (Permanent)

- **Deny by default**: No agent has any capability until explicitly granted
- **Attenuate always**: Every delegation narrows scope; the system structurally prevents widening
- **Log everything**: Every capability exercise hits the append-only audit trail
- **Expire aggressively**: Short-lived tokens; re-delegation rather than refresh
- **Fail closed**: If the bus cannot validate a token, deny the operation

---

## 8. Key Threats Specific to HUMMBL's Architecture

| Threat | Vector | Mitigation |
|--------|--------|-----------|
| Confused deputy | Agent A tricks Agent B into using B's capabilities for A's purposes | Capability tokens are holder-bound; B's tokens only work with B's key |
| Token theft | Compromised agent leaks its tokens | Short expiration + holder binding; stolen tokens expire before use |
| Privilege escalation | Agent requests broader capabilities than delegated | Bus validates scope is subset of parent; Biscuit Datalog enforces |
| Cascade compromise | One compromised agent infects others | Per-agent identity + epoch revocation; bus can isolate any agent |
| Audit tampering | Attacker modifies logs to hide actions | Append-only with hash chain; any modification breaks the chain |
| Ambient authority | Agent inherits human's full permissions | Capability model eliminates ambient authority by design |

---

## Sources

### Foundational Papers and Projects
- [Dennis & Van Horn, 1966 — Programming Semantics for Multiprogrammed Computations](https://dl.acm.org/doi/10.1145/365230.365252)
- [Object-Capability Model — Wikipedia](https://en.wikipedia.org/wiki/Object-capability_model)
- [Capability-Based Security — Wikipedia](https://en.wikipedia.org/wiki/Capability-based_security)
- [Awesome Object Capabilities (GitHub)](https://github.com/dckc/awesome-ocap)
- [POLA — erights.org](http://www.erights.org/talks/nps/slides/img2.html)

### CHERI and Hardware Capabilities
- [CHERI — University of Cambridge](https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/)
- [ARM Morello Board](https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/cheri-morello.html)
- [CHERI Alliance — Morello](https://cheri-alliance.org/discover-cheri/cheri-products/morello/)
- [CHERI Research Centre](https://cheri.cst.cam.ac.uk/)
- [ARM Morello Program](https://www.arm.com/architecture/cpu/morello)

### Capability Systems
- [Cap'n Proto RPC Protocol](https://capnproto.org/rpc.html)
- [Hardened JavaScript (SES)](https://hardenedjs.org/)
- [Endo / SES (GitHub)](https://github.com/endojs/endo)
- [Capsicum — University of Cambridge](https://www.cl.cam.ac.uk/research/security/capsicum/)
- [Capsicum Sandboxing Tutorial](https://cdaemon.com/posts/capsicum)
- [WASI Capability-Based Security](https://marcokuoni.ch/blog/15_capabilities_based_security/)
- [WASI and WebAssembly Component Model Status (2025)](https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/)
- [CloudABI (GitHub, deprecated)](https://github.com/NuxiNL/cloudabi)
- [Cloudflare Workers RPC Visibility Model](https://developers.cloudflare.com/workers/runtime-apis/rpc/visibility/)

### Token Formats
- [Macaroons — Google Research (2014)](https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/)
- [Biscuit — Clever Cloud](https://www.clever.cloud.com/blog/engineering/2021/04/12/introduction-to-biscuit/)
- [Biscuit Auth (Rust docs)](https://docs.rs/biscuit-auth)
- [libmacaroons (GitHub)](https://github.com/rescrv/libmacaroons)

### AI Agent Security
- [Anthropic — Framework for Safe and Trustworthy Agents](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents)
- [OpenAI — Safety in Building Agents](https://platform.openai.com/docs/guides/agent-builder-safety)
- [OpenAI Agents SDK — Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Google A2A Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [A2A Protocol Upgrade (Google Cloud Blog)](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade)
- [State of Agent Security 2026 — Grantex](https://grantex.dev/report/state-of-agent-security-2026)
- [Token Security 2026 Predictions](https://www.token.security/blog/token-security-2026-ai-agent-identity-security-predictions)
- [ISACA — The Looming Authorization Crisis](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-looming-authorization-crisis-why-traditional-iam-fails-agentic-ai)

### Delegation and Attenuation
- [Capabilities Are the Only Way to Secure Agent Delegation](https://niyikiza.com/posts/capability-delegation/)
- [Okta — Control the Chain, Secure the System](https://www.okta.com/blog/ai/agent-security-delegation-chain/)
- [On-Behalf-Of Authentication for AI Agents (Scalekit)](https://www.scalekit.com/blog/delegated-agent-access)
- [Oso — AI Agent Permissions](https://www.osohq.com/learn/ai-agent-permissions-delegated-access)
- [DelegateOS (GitHub)](https://github.com/newtro/delegateos)
- [Vouchsafe — Zero-Infrastructure Capability Graph (arxiv, 2026)](https://arxiv.org/html/2601.02254v1)

### Multi-Agent Security
- [Open Challenges in Multi-Agent Security (arxiv, 2025)](https://arxiv.org/html/2505.02077v1)
- [CSA — Securing the Agentic Control Plane (2026)](https://cloudsecurityalliance.org/blog/2026/03/20/2026-securing-the-agentic-control-plane)
- [Microsoft — Secure Agentic AI End-to-End (2026)](https://www.microsoft.com/en-us/security/blog/2026/03/20/secure-agentic-ai-end-to-end/)
- [NIST AI Agent Standards Initiative](https://www.pillsburylaw.com/en/news-and-insights/nist-ai-agent-standards.html)

### Permission Models and MCP
- [Claude Code Permissions Documentation](https://platform.claude.com/docs/en/agent-sdk/permissions)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [MCP Authorization Specification (2025-03-26)](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)
- [MCP Spec Auth Updates (June 2025)](https://auth0.com/blog/mcp-specs-update-all-about-auth/)
- [MCP Audit Logging (Tetrate)](https://tetrate.io/learn/ai/mcp/mcp-audit-logging)
- [Immutable Audit Log Pipeline with OpenTelemetry](https://oneuptime.com/blog/post/2026-02-06-immutable-audit-log-pipeline-otel/view)

### OAuth and Capabilities Comparison
- [Storj — Capability-Based vs ACL Access Control](https://storj.dev/learn/concepts/access/capability-based-access-control)
- [OAuth2 Scopes Are Not Permissions (Aserto)](https://www.aserto.com/blog/oauth2-scopes-are-not-permissions)
- [OAuth for AI Agents (MintMCP)](https://www.mintmcp.com/blog/oauth-ai-agents)
