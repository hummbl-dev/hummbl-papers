# Summary: RQ-006 -- Capability-Based Security for Agent Systems

**Source:** capability_security_agent_systems_2026.md | **Date:** 2026-03-23

- **93% of popular AI agent projects in 2026 still rely on unscoped API keys, 0% implement per-agent identity, and 100% lack granular revocation.** Capability-based authorization directly addresses all three gaps. This is the security model that maps most naturally to multi-agent architectures.
- **Object-capability model (OCap) treats authority as transferable, attenuable, cryptographically verifiable tokens** rather than identity-checked policy lookups. Holding a reference to an object is the sole way to exercise authority over it. No ambient authority -- programs cannot access anything not explicitly granted.
- **Historical lineage from Dennis & Van Horn (1966) through CHERI hardware.** Practical implementations include Cap'n Proto (RPC), Hardened JavaScript (SES), Capsicum (FreeBSD), and WASI (WebAssembly). Mark Miller's 2006 "Robust Composition" thesis formalized the relationship between capabilities and least authority.
- **Directly applicable to HUMMBL's governance bus and delegation tokens.** The delegation token service should implement capability attenuation (a delegated token can have fewer rights than its parent, never more) and time-bounded revocation.
- **Minimum viable capability architecture proposed** for HUMMBL: per-agent identity tokens, capability attenuation chains, cryptographic verification, and audit trail integration with the governance bus.
