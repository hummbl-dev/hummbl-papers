# Summary: RQ-007 -- Mutation Testing, Property-Based Testing, Chaos Engineering for Agent Systems

**Source:** test_strategy_agent_systems_2026.md | **Date:** 2026-03-23

- **"Code coverage is a vanity metric; mutation score is a quality metric."** Mutation testing introduces deliberate code changes and checks whether tests catch them. MSI (Mutation Score Indicator) above 80% is considered strong. Correlates more strongly with fault-detection capability than line/branch coverage.
- **Property-based testing is particularly valuable for agent systems** where input/output spaces are vast and example-based tests cannot cover edge cases. Tools like Hypothesis (Python) generate randomized inputs that satisfy declared properties.
- **Chaos engineering adapted for AI agents:** Injecting failures (dropped messages, delayed responses, model hallucinations) into multi-agent systems tests resilience. Directly relevant to HUMMBL's bus protocol -- what happens when an agent crashes mid-task?
- **Testing LLM/agent outputs requires new strategies:** Traditional assertions fail for non-deterministic outputs. LLM-as-judge, semantic similarity thresholds, and behavioral contract testing are emerging patterns.
- **Solo developer test strategy recommendation:** Focus mutation testing on critical business logic, use property-based testing for data transformation pipelines, and reserve chaos engineering for the coordination bus.
