# Summary: NemoClaw Implementation Guide (Synthesis Document)

**Source:** NEMOCLAW_IMPLEMENTATION_GUIDE.md | **Date:** 2026-03-23

- **Implementation-ready guide for the NemoClaw Supervisor-Worker pipeline** (v0.1.4), synthesizing findings from RQ-003, RQ-005, RQ-006, and RQ-007 research reports into actionable architecture decisions.
- **Dual-machine architecture:** Supervisor on Ubuntu/Nodezero (M4 Pro 48GB) generates experiment specs; Worker on Windows/Desktop (RTX 3080 Ti 12GB) claims runs, executes training, evaluates acceptance. File-based queue with no message broker or database.
- **Key protocol elements:** READY/CANCEL sentinel files for signaling, val_bpb as sole acceptance metric, 22 failure codes (ARNC-001 through ARNC-022), circuit breaker (3 consecutive identical failures stops Worker), scope-aware acceptance preventing cross-budget comparisons, 85C GPU thermal threshold.
- **State machine:** queued -> dispatched -> running -> completed -> accepted/rejected, with failed/canceled as terminal states at each transition. Worker owns state.json; Supervisor never writes state directly.
- **Integrates research findings on stigmergic coordination (RQ-005), capability security for delegation (RQ-006), testing strategy for agent systems (RQ-007), and incident response patterns (RQ-003).**
