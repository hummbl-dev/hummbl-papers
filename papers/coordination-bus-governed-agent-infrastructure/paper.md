# Coordination Bus as Governed Agent Infrastructure

**Status:** SCOPED
**Date seeded:** 2026-07-06
**Author:** Reuben Bowlby
**Repository:** hummbl-dev/hummbl-papers

## Abstract

Agentic engineering systems need a coordination substrate that supports work routing without turning every message into hidden authority. This paper scopes an append-only coordination bus as a governance primitive: a durable event surface where agents post status, blockers, decisions, milestones, and review receipts while separate gates decide which actions can execute. The paper will analyze the bus as infrastructure for queue control, audit reconstruction, and operational containment, using public-safe artifacts from the HUMMBL research portfolio and the founder-mode hardening sprint.

## Claim

A coordination bus becomes a governance primitive when it is append-only, typed, identity-scoped, and paired with explicit action gates. In that shape, it can improve review throughput and post-hoc auditability without granting ambient execution authority.

## Method

This paper is a case-study and systems analysis. The scoped method is:

1. Extract the bus invariants from public HUMMBL source artifacts.
2. Map those invariants to queue-control failure modes found during the founder-mode hardening sprint.
3. Separate coordination evidence from execution authority.
4. Identify measurable outcomes that future empirical work can test, including review-lane latency, blocked-work recovery time, and receipt completeness.

## System Boundary

This public seed deliberately excludes private runtime contents, operator schedules, machine-local paths, secrets, and live queue state. It treats the bus as an architectural pattern and cites only public-safe repository artifacts.

## Preliminary Invariants

- **Append-only event surface:** historical coordination records are added as new entries instead of silently rewritten.
- **Typed messages:** status, blocker, decision, question, proposal, and milestone records are distinguishable at read time.
- **Identity-scoped senders:** message authorship is constrained to an approved sender vocabulary.
- **Evidence/action separation:** posting a message records coordination evidence; it does not itself grant authority to invoke tools, spend budget, merge code, or alter production systems.
- **Receipt linkage:** high-risk actions are expected to leave a source-linked receipt that a reviewer can inspect without trusting the agent's summary alone.

## Draft Outline

### 1. Problem

Agentic engineering work tends to fail at the boundary between communication and authority. Without a shared coordination surface, work fragments into chat transcripts, PR comments, local notes, and implied state. With an overpowered coordination surface, a message bus can become an ambient authority channel. The paper frames that tension as the central design problem.

### 2. Prior Art

The analysis will compare the HUMMBL coordination bus against message buses, capability security, append-only logs, and cognitive stigmergy. The goal is not to claim novelty for append-only logging; the contribution is the governance interpretation of a bus in an agentic engineering loop.

### 3. Bus Contract

The paper will specify a minimal bus contract:

- one durable record per coordination event
- typed message classes
- canonical sender identity
- timestamped entries
- no destructive historical edits
- no implicit execution rights

### 4. Hardening-Sprint Case Study

The founder-mode hardening sprint provides the operational case. The public version will summarize the queue-control lessons without copying private bus contents. Candidate observations include:

- review debt needs first-class state, not scattered comments
- a blocker should not count as productive last activity forever
- local test claims should remain distinct from CI receipts
- merge readiness needs evidence from checks, reviews, and scope boundaries

### 5. Evaluation Plan

The first empirical pass should test whether bus-backed receipts reduce:

- time to reconstruct why a PR was or was not merged
- disagreement between local status summaries and GitHub CI state
- stale blocked work in active lanes
- unsourced claims in public artifacts

### 6. Limitations

The seed does not prove generality outside HUMMBL systems. The first version should present this as an internal case study with reproducible artifacts, then identify what would be required for an external replication.

## Public Source Artifacts

- [HUMMBL Coordination Bus Protocol Specification](../../reports/reports/HUMMBL_BUS_PROTOCOL_SPEC.md)
- [Multi-Agent Coordination Research Report](../../reports/reports/multi_agent_coordination_2026.md)
- [Capability Security for Agent Systems](../../reports/reports/capability_security_agent_systems_2026.md)
- [CAES Coordination Bus Spec](../../frameworks/unified-tier/governance/CAES_SPEC.md)
- [Research notebook](../../notebooks/coordination-bus-governed-agent-infrastructure.notebook.md)

## Open Questions

- Which bus invariants are necessary for audit reconstruction, and which are implementation details?
- What is the smallest public replay fixture that demonstrates queue-control value without exposing internal operations?
- Should the first version remain a technical report, or should it target a workshop paper format?
