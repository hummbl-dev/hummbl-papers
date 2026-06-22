# RQ-007: Mutation Testing, Property-Based Testing, and Chaos Engineering for Agent Systems

**Research ID:** RQ-007
**Domain:** test_strategy
**Date:** 2026-03-23
**Status:** Completed
**Targets:** skills/tdd, skills/test-run, skills/coverage

---

## Table of Contents

1. [Mutation Testing](#1-mutation-testing)
2. [Property-Based Testing](#2-property-based-testing)
3. [Chaos Engineering for Agent Systems](#3-chaos-engineering-for-agent-systems)
4. [Testing LLM/Agent Outputs](#4-testing-llmagent-outputs)
5. [Contract Testing for Agent Systems](#5-contract-testing-for-agent-systems)
6. [Testing Strategy for Solo Developers](#6-testing-strategy-for-solo-developers)
7. [Synthesis: HUMMBL Test Strategy Recommendations](#7-synthesis-hummbl-test-strategy-recommendations)
8. [Sources](#sources)

---

## 1. Mutation Testing

### 1.1 What Is Mutation Testing and Why Does It Matter?

Mutation testing is a fault-based testing technique that evaluates the quality of a test suite by introducing small, deliberate changes (mutants) into source code and checking whether existing tests detect them. If a test fails when a mutant is introduced, the mutant is "killed." If all tests pass despite the mutation, the mutant "survives," indicating a gap in test coverage.

The core insight: **code coverage is a vanity metric; mutation score is a quality metric.** A codebase can have 95% line coverage while its tests fail to catch meaningful bugs. Mutation testing reveals whether your tests actually assert meaningful behavior.

The **Mutation Score Indicator (MSI)** is computed as:

```
MSI = (killed mutants) / (killed mutants + survived mutants) * 100
```

An MSI above 80% is generally considered strong. Research consistently shows mutation score correlates more strongly with fault-detection capability than line or branch coverage alone.

### 1.2 Tools Landscape (2025-2026)

| Tool | Language | Speed | Detection Rate | Notes |
|------|----------|-------|---------------|-------|
| **mutmut** | Python | ~1,200 mutants/min | 88.5% | Most actively maintained Python tool. AST-based generation avoids JVM overhead. Handles Python-specific operators (dict mutations, f-strings). |
| **cosmic-ray** | Python | Slower than mutmut | 82.7% | Distributed execution model, good for large codebases. Plugin architecture for custom operators. |
| **Stryker** | JS/TS/.NET | ~5,000 mutants/hr (.NET) | 92% (.NET) | Best-in-class for TypeScript/JavaScript. Incremental mode for CI. Dashboard for tracking scores over time. |
| **PIT (Pitest)** | Java/JVM | ~800 mutants/min | High | Gold standard for JVM. Bytecode-level mutation. Integrates with Maven/Gradle. |

**Key finding from IEEE 2025 benchmark:** Mutmut achieves 1.5x faster mutant generation than PIT with 20% less overhead on comparable codebases. For HUMMBL's Python-heavy stack, mutmut is the recommended starting point.

### 1.3 Mutation Testing for ML/AI Systems

Mutation testing for ML/AI introduces unique challenges due to non-determinism and the continuous nature of model outputs. Specialized approaches emerging in 2025-2026:

**Meta's ACH (Automated Compliance Hardening):** The landmark development in this space. Presented at FSE 2025 and EuroSTAR 2025, ACH uses LLMs to generate problem-specific mutants rather than generic syntactic changes. Engineers describe faults in plain text, and the system generates both mutants and tests. Key results:
- Applied to 10,795 Android Kotlin classes across Facebook, Instagram, WhatsApp, Messenger
- Generated 9,095 mutants and 571 privacy-hardening test cases
- 73% of generated tests accepted by engineers; 36% judged privacy-relevant
- Dramatically reduced computational overhead vs. traditional exhaustive mutation

**muPRL (2025):** A mutation testing pipeline specifically for Deep Reinforcement Learning, built on a taxonomy of real RL faults derived from repository mining. Addresses the gap between traditional mutants and the kinds of faults that actually occur in RL systems.

**DRLMutation (2025):** A comprehensive framework for mutation testing in deep RL systems, published in ACM TOSEM. Provides DRL-specific mutation operators targeting reward functions, state spaces, and action selection.

**Key challenge:** Crash mutants (mutants that cause runtime errors rather than semantic changes) average 38.79% of generated mutants in ML projects, wasting execution time. Filtering these is essential for cost-effective mutation testing of AI code.

### 1.4 Cost-Benefit Analysis

**When mutation testing is worth the compute:**
- Critical path code (payment processing, safety logic, agent decision-making)
- After reaching >80% line coverage and needing to assess actual test quality
- Before major refactors to validate test suite adequacy
- For compliance-sensitive code (Meta's primary use case)

**When to skip it:**
- Rapid prototyping phases where code changes daily
- UI/presentation layers with low defect cost
- Codebases under 500 lines where manual review suffices

**Cost reduction strategies:**
- Use mutmut's `--use-patch` mode for incremental mutation on changed files only
- Filter equivalent/crash mutants before execution (LLM-based filtering, as Meta demonstrated)
- Run mutation testing nightly rather than on every commit
- Focus on high-risk modules rather than entire codebase

### 1.5 Academic Papers of Note (2024-2026)

1. **"Mutation-Guided LLM-based Test Generation at Meta"** (FSE 2025) -- Foundational paper on ACH. Demonstrates mutation-guided test gen at industrial scale.
2. **"LLMorpheus: Mutation Testing Using Large Language Models"** (IEEE TSE, 2025) -- LLMs generate semantically meaningful mutants that better approximate real faults.
3. **"MutGen: On Mutation-Guided Unit Test Generation"** (2025) -- Proposes maximizing mutation score as the objective for LLM-based test generation. SPARC achieves 31.36% improvement in line coverage and 20.78% in mutation score.
4. **"Empirical Study on Machine Learning Testing Based on Mutation Testing"** (ACM AICI 2025) -- Surveys ML-specific mutation operators and their effectiveness.
5. **"An Analysis and Comparison of Mutation Testing Tools for Python"** (IEEE 2024) -- Head-to-head comparison of MutPy, Mutmut, Mutatest, Cosmic Ray on open-source projects.
6. **"muPRL: A Mutation Testing Pipeline for Deep Reinforcement Learning"** (ICST 2026) -- Real-fault-based mutation operators for RL systems.

---

## 2. Property-Based Testing

### 2.1 The QuickCheck Lineage

Property-based testing (PBT) originated with Haskell's QuickCheck (Claessen & Hughes, 2000) and has since been ported to virtually every language. The core idea: instead of writing individual test cases with specific inputs and expected outputs, you define **properties** that should hold for all valid inputs, and the framework generates hundreds or thousands of random inputs to verify them.

**Key frameworks by language:**

| Framework | Language | Stateful Testing | Shrinking | Notes |
|-----------|----------|-----------------|-----------|-------|
| **Hypothesis** | Python | Yes (RuleBasedStateMachine) | Excellent | Gold standard for Python. Database of previous failures. |
| **fast-check** | JS/TS | Yes | Excellent | Test-runner agnostic (Jest, Vitest, Mocha). Found bugs in React, io-ts, Jest. |
| **QuickCheck** | Haskell/Erlang | Yes | Original | The progenitor. Erlang version used extensively in telecom. |
| **PropEr** | Erlang/Elixir | Yes | Good | Popular in BEAM ecosystem. Book by Fred Hebert. |
| **jqwik** | Java/JVM | Yes | Good | Modern PBT for JUnit 5. |

### 2.2 Writing Good Properties for Agent/LLM Systems

Writing properties for non-deterministic agent systems requires a shift in thinking. Effective property categories:

**Invariant properties:** Things that must always be true regardless of LLM output.
```python
# Agent response must always include required fields
@given(st.text())
def test_agent_response_has_required_fields(user_input):
    response = agent.process(user_input)
    assert "action" in response
    assert "reasoning" in response
    assert response["action"] in VALID_ACTIONS
```

**Round-trip properties:** Encode-decode, serialize-deserialize, send-receive cycles.
```python
# Bus messages survive serialization round-trip
@given(bus_message_strategy())
def test_bus_message_roundtrip(msg):
    serialized = msg.serialize()
    deserialized = BusMessage.deserialize(serialized)
    assert deserialized == msg
```

**Metamorphic properties:** If input changes in a predictable way, output should change predictably.
```python
# Adding context should not reduce relevance score
@given(query=st.text(min_size=1), extra_context=st.text())
def test_more_context_not_less_relevant(query, extra_context):
    score_base = agent.relevance(query, context="")
    score_with = agent.relevance(query, context=extra_context)
    assert score_with >= score_base * 0.9  # Allow small tolerance
```

**Commutativity/idempotency properties:** Operations that should be order-independent or repeatable.
```python
# Processing the same message twice should be idempotent
@given(bus_message_strategy())
def test_idempotent_processing(msg):
    result1 = processor.handle(msg)
    result2 = processor.handle(msg)
    assert result1 == result2
```

### 2.3 Stateful Property Testing for Multi-Step Workflows

Stateful PBT is particularly powerful for agent systems because agents maintain state across interactions. Hypothesis's `RuleBasedStateMachine` generates sequences of operations and verifies invariants at each step.

```python
class AgentWorkflowMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.expected_state = {}

    @rule(task=task_strategy())
    def assign_task(self, task):
        self.agent.assign(task)
        self.expected_state[task.id] = "assigned"

    @rule(data=st.data())
    def complete_task(self, data):
        if not self.expected_state:
            assume(False)
        task_id = data.draw(st.sampled_from(list(self.expected_state.keys())))
        self.agent.complete(task_id)
        self.expected_state[task_id] = "completed"

    @invariant()
    def state_consistency(self):
        for task_id, expected in self.expected_state.items():
            assert self.agent.get_status(task_id) == expected
```

When a failure is found, Hypothesis shrinks the sequence of operations to the minimal reproducing case. Real-world experience shows shrinking reduces 13-step failures down to 3 steps, dramatically simplifying debugging.

### 2.4 Shrinking Strategies for Complex Inputs

Shrinking is PBT's killer feature. When a test fails, the framework systematically reduces the failing input to find the minimal counterexample.

**How shrinking works in practice:**
1. Framework finds a failing input (e.g., a 500-character string)
2. It tries smaller variations (remove characters, simplify structure)
3. Each variation is re-tested; if it still fails, the simpler version is kept
4. Process repeats until no further simplification causes failure

**Strategies for complex agent inputs:**
- **Structured shrinking:** fast-check and Hypothesis both support shrinking through composed strategies, so a complex JSON message shrinks its fields independently.
- **Stateful shrinking:** For operation sequences, the shrinker removes steps and re-runs, finding minimal failing sequences.
- **Custom shrinkers:** For domain-specific types (e.g., bus messages with interdependent fields), write custom shrink functions that maintain structural validity.

### 2.5 Property-Based Testing for API Contracts

PBT excels at API contract testing by generating diverse payloads that explore edge cases:
- Boundary values (empty strings, max-length strings, Unicode, null bytes)
- Type coercion bugs (numbers as strings, nested nulls)
- Schema violations that pass validation but cause downstream failures

Hypothesis's `from_schema()` strategy can generate valid inputs directly from JSON Schema or OpenAPI specs, automatically testing that your API handles all valid inputs correctly.

### 2.6 Real-World Bugs Found by PBT

**Agentic Property-Based Testing (2025):** A landmark study used Claude Opus 4.1 as an autonomous agent to discover bugs via Hypothesis across 100 popular Python packages (933 modules tested). Results:
- 984 bug reports generated; 56% confirmed as valid bugs
- Top 21 ranked bugs: 86% valid
- Cost: ~$9.93 per confirmed valid bug
- **NumPy bug found:** `numpy.random.wald` produced negative values for large mean parameters (>= 1e8), violating the mathematical definition of the Wald distribution. Patch merged by maintainers.
- **AWS Lambda Powertools:** Dictionary slicing function returning duplicate chunks
- **Tokenizers:** Missing closing parenthesis in HSL color format strings

**fast-check ecosystem finds:** Bugs discovered in React, io-ts, and Jest itself -- libraries with extensive traditional test suites.

**Security bug via PBT:** A property-based test generated `"__proto__"` as a random string for a provider name field, exposing a prototype pollution vulnerability after just 75 test runs.

---

## 3. Chaos Engineering for Agent Systems

### 3.1 The Netflix Chaos Monkey Lineage

Chaos engineering originated at Netflix in 2011 with Chaos Monkey, which randomly terminated production instances to verify resilience. The discipline has evolved significantly:

- **2011:** Chaos Monkey (random instance termination)
- **2014:** Simian Army (Latency Monkey, Conformity Monkey, etc.)
- **2016:** Gremlin founded as first commercial chaos engineering platform
- **2018-2020:** Kubernetes-native tools emerge (LitmusChaos, Chaos Mesh)
- **2024-2025:** Chaos engineering meets LLM/agent systems
- **2025:** ChaosEater -- fully LLM-automated chaos engineering

### 3.2 Current Tools (2025-2026)

| Tool | Type | Best For | Observability Integration |
|------|------|----------|--------------------------|
| **Gremlin** | Commercial SaaS | Enterprise, multi-cloud | Datadog, Prometheus, PagerDuty, New Relic. SLO-based auto-halt. Reliability Management Dashboard. |
| **LitmusChaos** | Open-source (CNCF) | Kubernetes-native, CI/CD integration | Prometheus. Rich API for pipeline automation. Steep learning curve. |
| **Chaos Mesh** | Open-source (PingCAP) | Kubernetes, database systems | Grafana dashboard, Prometheus. Strong network fault injection. |
| **Steadybit** | Commercial | Platform engineering | Built-in experiment insights. Team collaboration features. |

**Market positioning:** LitmusChaos and Chaos Mesh dominate startups and cloud-native teams. Gremlin leads enterprise adoption with audit logs, team management, and support SLAs. For a solo developer, LitmusChaos or Chaos Mesh with a local Kubernetes cluster is the practical starting point.

### 3.3 Chaos Engineering for LLM-Based Systems

Two landmark papers define the state of the art:

**"Assessing and Enhancing the Robustness of LLM-based Multi-Agent Systems Through Chaos Engineering" (CAIN 2025)**

This paper proposes a chaos engineering framework specifically for LLM-based multi-agent systems (LLM-MAS), identifying fault types unique to agent architectures:
- **Agent failures:** Individual agents crashing or becoming unresponsive
- **Communication breakdowns:** Messages lost, delayed, or corrupted between agents
- **Cascading failures:** One agent's failure triggering downstream agent failures
- **Hallucinations:** LLM-specific errors generating false information
- **Task reassignment challenges:** Failures during dynamic work redistribution
- **Resource exhaustion:** Memory/compute limits under load

Safety mechanisms recommended:
- Sandboxed isolation of fault injection
- Real-time monitoring for early detection
- Automated recovery mechanisms
- Quantitative metrics (response time, fault detection rates, error rates, CPU/memory)
- Qualitative metrics (user experience, business impact, system behavior)

**"ChaosEater: LLM-Powered Fully Automated Chaos Engineering" (November 2025)**

ChaosEater automates the entire chaos engineering cycle using LLMs, targeting Kubernetes-based systems. The LLM agent:
1. Analyzes system architecture
2. Designs chaos experiments
3. Injects faults
4. Observes results
5. Replans experiments based on findings

Supports automated experiment replanning to update fault injection scopes as systems evolve.

### 3.4 Fault Injection Patterns for Agent Systems

| Fault Type | Implementation | What It Tests |
|------------|---------------|---------------|
| **Network partition** | Block inter-agent communication | Graceful degradation, timeout handling |
| **Slow responses** | Add latency to LLM API calls (500ms-10s) | Timeout logic, user experience under load |
| **Wrong outputs** | Inject hallucinated/corrupted agent responses | Input validation, error handling, guardrails |
| **Token exhaustion** | Simulate hitting API rate limits or token caps | Fallback strategies, queue management |
| **Partial failures** | Kill one agent in a multi-agent pipeline | Task reassignment, pipeline resilience |
| **State corruption** | Corrupt shared state/memory between agents | State validation, recovery procedures |
| **Clock skew** | Desynchronize agent timestamps | Ordering guarantees, timeout calculations |

### 3.5 Safely Chaos Testing a Multi-Agent Pipeline

**Progressive approach for HUMMBL:**

1. **Start in staging/dev:** Never inject faults in production until you have confidence from lower environments.
2. **Single-fault injection first:** Test one fault type at a time before combining.
3. **Blast radius control:** Limit experiments to one agent or one communication channel.
4. **Automated rollback:** Define SLO-based circuit breakers that halt experiments if key metrics degrade.
5. **Game day exercises:** Schedule periodic chaos experiments with defined scope and duration.
6. **Hypothesis-driven:** Always state what you expect to happen before injecting a fault.

### 3.6 Observability Requirements

Minimum observability stack for chaos experiments:
- **Distributed tracing:** Track requests across agent boundaries (OpenTelemetry)
- **Structured logging:** JSON logs with correlation IDs for every agent interaction
- **Metrics:** Latency percentiles, error rates, throughput per agent
- **Alerting:** Automated alerts on SLO violations during experiments
- **Dashboards:** Real-time visualization of experiment impact
- **Audit trail:** Record what was injected, when, and what happened

---

## 4. Testing LLM/Agent Outputs

### 4.1 Testing Non-Deterministic Systems

LLM outputs are inherently non-deterministic, even under "deterministic" settings. Research from NAACL 2025 shows that even with identical prompts, random seeds, and greedy decoding, outputs vary due to:
- Floating-point arithmetic non-associativity
- Continuous batching and prefix caching optimizations
- Hardware differences (FP32 provides near-perfect determinism; BF16 exhibits substantial variance)

**Practical strategies:**

1. **Semantic evaluation over exact matching:** Use embedding similarity or LLM-based judges rather than string comparison.
2. **Statistical testing:** Run inputs 10-20 times; report mean, variance, and min/max scores.
3. **Pin model snapshots:** Use exact model version IDs to reduce one source of variance.
4. **Prefer greedy decoding for tests:** Set temperature=0 and use greedy decoding for reproducible baselines.
5. **Tolerance bands:** Assert that outputs fall within acceptable ranges rather than matching exactly.
6. **Structural assertions:** Verify output format, required fields, and constraints rather than content.

### 4.2 Evaluation Frameworks

| Framework | Focus | Metrics | Best For |
|-----------|-------|---------|----------|
| **DeepEval** | General LLM testing | 60+ metrics (faithfulness, relevance, hallucination, toxicity, bias) | Comprehensive test suites. Self-explaining metrics. pytest integration. |
| **RAGAS** | RAG evaluation | Faithfulness, answer relevancy, context precision/recall | RAG pipeline quality. Now supports agentic workflows and tool use. |
| **promptfoo** | Prompt engineering | Basic RAG + safety metrics. YAML config. | Quick iteration. A/B testing. CI integration. Red-teaming. |
| **Braintrust** | Production eval + observability | Factuality, helpfulness, custom scorers | Production monitoring. GitHub Action CI/CD. Turn traces into eval datasets. |
| **LangWatch** | Agent simulation | Agent-specific metrics | Simulating multi-turn agent conversations. |

**Recommendation for HUMMBL:** Start with DeepEval for its breadth and pytest integration. Add promptfoo for quick prompt iteration. Use Braintrust patterns for production monitoring when deploying.

### 4.3 LLM-as-Judge Patterns and Reliability

LLM-as-judge uses a strong model (GPT-4, Claude) to evaluate the output of another model. Research shows:

**Accuracy:** State-of-the-art LLMs align with human judgment up to 85% for both pairwise and single-output scoring -- higher than inter-human agreement (81%).

**Known biases:**
- **Position bias:** GPT-4 shows ~40% inconsistency when swapping the order of compared outputs
- **Verbosity bias:** Longer responses receive ~15% inflated scores
- **Self-preference bias:** Models tend to rate their own outputs higher

**Reliability improvements:**
- **Chain-of-thought judging:** Prompt the judge to explain reasoning before scoring (10-15% reliability improvement)
- **Few-shot examples:** Provide calibration examples with known scores
- **Multi-judge ensemble:** Use multiple models as judges and aggregate
- **Swap testing:** Run pairwise comparisons in both orders to detect position bias
- **Human calibration:** Validate a subset with human judges to establish ground truth

### 4.4 Regression Testing for Prompt Changes

Every prompt change is a potential regression. Strategies:

1. **Golden dataset:** Maintain a curated set of 50-200 input-output pairs that represent critical behaviors.
2. **Automated eval on PR:** Run golden dataset through new prompt, compare scores to baseline.
3. **Threshold-based gates:** Define minimum acceptable scores (e.g., faithfulness > 0.85) that block merges.
4. **Diff visualization:** Show side-by-side output comparisons for changed prompts.
5. **Braintrust pattern:** GitHub Action runs experiments and posts results to PRs automatically.

### 4.5 Snapshot Testing for LLM Outputs

Adapted from UI snapshot testing, but with semantic comparison:

```python
def test_agent_response_snapshot():
    response = agent.process("Summarize the project status")
    # Don't assert exact match -- assert semantic similarity
    snapshot = load_snapshot("project_status_summary")
    similarity = semantic_similarity(response, snapshot)
    assert similarity > 0.8, f"Response drifted from snapshot: {similarity}"
    # Also assert structural properties
    assert len(response) < 500  # Not too verbose
    assert "status" in response.lower()
```

**Update strategy:** Review and approve snapshot updates manually during prompt changes. Automate detection but not approval.

### 4.6 A/B Testing Prompts in Production

**Key principles:**
- Route a percentage of traffic to variant prompts
- Measure business metrics (task completion, user satisfaction) not just eval scores
- Run for statistical significance (typically 1-2 weeks with sufficient volume)
- Use Braintrust or promptfoo for automated scoring and comparison
- Mine production data: every user interaction becomes a potential eval case

---

## 5. Contract Testing for Agent Systems

### 5.1 Tools and Approaches

| Tool | Approach | Best For |
|------|----------|----------|
| **Pact** | Consumer-driven contracts | HTTP/message-based service interactions. Broker coordinates lifecycle. |
| **Protovalidate** | Protobuf schema validation | gRPC-based agent communication |
| **JSON Schema** | Schema validation | REST APIs, message bus payloads |
| **Zod** | TypeScript runtime validation | Type-safe agent interfaces in TS |
| **Pydantic** | Python data validation | Python agent message schemas |

### 5.2 Contract Testing Between Agents

In a multi-agent system, each agent is both a consumer and provider of messages. Contract testing ensures:

1. **Producer guarantees:** Each agent's output conforms to its declared schema
2. **Consumer expectations:** Each agent can handle the range of valid inputs it might receive
3. **Backward compatibility:** Schema changes don't break existing consumers

**Pact for agent systems (2025-2026):**
- Pact v4.0+ supports message-based contracts (not just HTTP)
- Central Pact Broker coordinates contract lifecycle across agents
- Consumer-driven: the agent consuming a message defines what fields it needs
- Provider verification: the producing agent runs verification to prove it meets consumer expectations

**Emerging pattern -- PACT (Contracts Before Code):**
A 2025 project proposes using contracts as the foundation for multi-agent software engineering: architecture is decided before implementation, tests are created first, and agents iterate until tests pass. The pipeline monitors coordination health and detects cascade failures.

### 5.3 Schema Evolution and Backward Compatibility

Critical for long-running agent systems where agents may be at different versions:

**Additive changes (safe):** Adding optional fields, adding new message types
**Breaking changes (dangerous):** Removing fields, changing field types, renaming fields

**Strategies:**
- **Schema versioning:** Include version in every message (`"schema_version": "1.2"`)
- **Tolerant reader pattern:** Agents ignore unknown fields
- **Schema registry:** Central registry of all message schemas with compatibility checks
- **Deprecation workflow:** Mark fields deprecated in schema, remove after all consumers migrate

### 5.4 Application to HUMMBL Coordination Bus

For HUMMBL's bus-protocol, contract testing should enforce:

```python
# Example: Bus message contract
class BusMessage(BaseModel):
    schema_version: str = "1.0"
    message_type: str
    source_agent: str
    target_agent: Optional[str] = None  # None = broadcast
    payload: dict
    correlation_id: str
    timestamp: datetime

    @validator('message_type')
    def valid_message_type(cls, v):
        assert v in REGISTERED_MESSAGE_TYPES
        return v
```

**Testing approach:**
1. Define Pydantic models for all bus message types
2. Use Hypothesis to generate valid messages and verify handling
3. Use Pact-style consumer-driven contracts between agent pairs
4. Run schema compatibility checks in CI when message definitions change
5. Property-test serialization round-trips for all message types

---

## 6. Testing Strategy for Solo Developers

### 6.1 Minimum Viable Test Suite for a Bootstrapped Project

For a solo developer building an agent system, the priority is **maximum confidence per hour invested**. The recommended minimum:

**Phase 1 -- Foundation (Week 1):**
- Unit tests for pure functions (data transformers, validators, parsers)
- Smoke test for each agent (can it start and process a basic message?)
- Schema validation tests for all message types (Pydantic/Zod)

**Phase 2 -- Core Quality (Weeks 2-4):**
- Integration tests for agent-to-agent communication
- Property-based tests for serialization round-trips and invariants
- Golden dataset eval for LLM-dependent components (10-20 examples)

**Phase 3 -- Hardening (Month 2+):**
- Mutation testing on critical path modules (agent decision logic)
- Stateful property tests for multi-step workflows
- Contract tests between agents
- Basic chaos tests (agent crash, slow LLM response)

### 6.2 Test Pyramid for Agent Systems

The traditional 70/20/10 pyramid needs adaptation for agent systems:

```
                    /\
                   /  \
                  / E2E \ ............... 5%  Full pipeline tests
                 /  Tests \                   (expensive, slow, flaky)
                /----------\
               / Integration \ ........... 25% Agent-to-agent,
              /    Tests      \               bus communication,
             /                 \              LLM API integration
            /-------------------\
           /   Property-Based    \ ....... 20% Invariants, round-trips,
          /       Tests           \           stateful workflows
         /-------------------------\
        /      Unit Tests           \ .... 40% Pure functions, validators,
       /                             \        parsers, transformers
      /-------------------------------\
     /        Eval/LLM Tests           \ . 10% Golden datasets, prompt
    /                                   \     regression, LLM-as-judge
   /-------------------------------------\
```

**Key differences from traditional pyramid:**
- Property-based tests get their own layer (not just "unit tests with random inputs")
- Eval/LLM tests are a distinct category requiring specialized tooling
- E2E tests are minimized because multi-agent pipelines are expensive to run end-to-end
- Integration tests are proportionally larger because agent interactions are the primary failure mode

### 6.3 When to Invest in Each Testing Type

| Testing Type | Invest When | Skip Until |
|-------------|-------------|------------|
| Unit tests | Immediately | Never skip |
| Schema validation | As soon as you define message types | Never skip |
| Property-based tests | When you have >3 data transformations | You have stable interfaces |
| Integration tests | When 2+ agents communicate | You have 2+ agents |
| LLM eval tests | When prompts affect user-facing output | You have stable prompts |
| Mutation testing | When you have >80% coverage and need confidence | Coverage is below 60% |
| Contract tests | When agents are developed/deployed independently | Single-process deployment |
| Chaos engineering | When running in production or staging | Pre-MVP |
| E2E tests | When you have a complete pipeline | Pipeline is still changing daily |

### 6.4 Automating Test Generation with LLMs

LLM-based test generation is rapidly maturing and is highly relevant for solo developers:

**Current capabilities (2025-2026):**
- GPT-4o achieves 35.2% line coverage on real-world code without guidance
- With mutation-guided approaches (MutGen/SPARC), coverage improves by 31% and mutation score by 21%
- Meta's ACH generates tests that are accepted by engineers 73% of the time

**Practical workflow for solo devs:**

1. **Write the first test manually** for each module to establish patterns
2. **Use LLM to generate additional test cases** based on your patterns
3. **Run mutation testing** to identify gaps in LLM-generated tests
4. **Iterate:** Feed surviving mutants back to LLM for targeted test generation
5. **Review all generated tests** -- LLMs produce plausible-looking tests that may not assert meaningful behavior

**Tools:**
- Claude Code / Copilot for inline test generation
- CoverUp (2025): Coverage-guided LLM test generation that iteratively improves coverage
- MuTAP: Mutation-guided test generation achieving 93.57% mutation score on synthetic code

**Warning:** LLM-generated tests often have high coverage but low mutation score. Always validate with mutation testing.

---

## 7. Synthesis: HUMMBL Test Strategy Recommendations

### 7.1 Recommended Test Stack

| Layer | Tool | Priority |
|-------|------|----------|
| Schema validation | Pydantic (Python), Zod (TS) | P0 -- implement immediately |
| Unit tests | pytest + Hypothesis | P0 |
| Property-based tests | Hypothesis (Python), fast-check (TS) | P1 -- within first month |
| LLM evaluation | DeepEval + promptfoo | P1 |
| Integration tests | pytest + test containers | P1 |
| Mutation testing | mutmut | P2 -- after 80% coverage |
| Contract tests | Pydantic contracts + Hypothesis | P2 |
| Chaos engineering | Custom fault injection (no K8s needed) | P3 -- post-MVP |
| E2E tests | Playwright or custom pipeline runner | P3 |

### 7.2 Quick Wins for HUMMBL

1. **Add Pydantic models for all bus messages today.** This is the highest-ROI testing investment -- it catches malformed messages at the boundary.

2. **Write 5 Hypothesis property tests for bus message serialization.** Round-trip properties will catch encoding bugs that unit tests miss.

3. **Set up a golden dataset of 20 prompt-response pairs.** Run DeepEval on every prompt change to catch regressions.

4. **Run mutmut on agent decision logic once per week.** Focus on the modules where bugs have the highest cost.

5. **Implement basic fault injection in test helpers.** A simple decorator that randomly delays or fails LLM API calls will reveal timeout and retry bugs without needing Kubernetes chaos tools.

### 7.3 Cost Budget for Solo Developer

Assuming limited compute budget (RTX 3080 Ti local + limited cloud API):

- **Property-based testing:** Free (runs locally, CPU-only)
- **Mutation testing:** Free but compute-intensive. Run weekly on critical modules only. ~30 min for 1000-line module.
- **LLM evaluation:** API costs. Budget ~$5-10/month for golden dataset evals. Use local models (Ollama) for high-volume eval.
- **Chaos engineering:** Free if using custom fault injection. LitmusChaos if you move to Kubernetes.

### 7.4 Integration with NemoClaw Pipeline

For the NemoClaw Supervisor-Worker pipeline specifically:

1. **Contract test supervisor-worker messages** using Pydantic models
2. **Property-test task assignment invariants** (every task assigned exactly once, no orphaned tasks)
3. **Chaos test worker failures** (what happens when a worker dies mid-task?)
4. **Eval test worker outputs** against golden datasets per task type
5. **Stateful property test** the full supervisor state machine using Hypothesis RuleBasedStateMachine

---

## Sources

### Mutation Testing
- [Meta: LLMs Are the Key to Mutation Testing](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)
- [Meta: Revolutionizing Software Testing with LLM-Powered Bug Catchers](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/)
- [Mutation-Guided LLM-based Test Generation at Meta (arXiv)](https://arxiv.org/abs/2501.12862)
- [LLMorpheus: Mutation Testing Using Large Language Models (IEEE)](https://ieeexplore.ieee.org/iel8/32/11048386/10977824.pdf)
- [muPRL: Mutation Testing Pipeline for Deep RL (IEEE)](https://ieeexplore.ieee.org/document/11029852/)
- [DRLMutation Framework (ACM TOSEM)](https://dl.acm.org/doi/10.1145/3721978)
- [MutGen: On Mutation-Guided Unit Test Generation (arXiv)](https://arxiv.org/html/2506.02954v2)
- [Analysis and Comparison of Python Mutation Testing Tools (IEEE)](https://ieeexplore.ieee.org/document/10818231/)
- [Stryker Mutator](https://stryker-mutator.io/)
- [Mutation Testing with Mutmut](https://johal.in/mutation-testing-with-mutmut-python-for-code-reliability-2026/)
- [Awesome Mutation Testing (GitHub)](https://github.com/theofidry/awesome-mutation-testing)
- [Mutation 2026 Workshop at ICST](https://conf.researchr.org/home/icst-2026/mutation-2026)

### Property-Based Testing
- [Agentic Property-Based Testing: Finding Bugs Across the Python Ecosystem (arXiv)](https://arxiv.org/html/2510.09907v1)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Hypothesis Stateful Testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- [fast-check GitHub](https://github.com/dubzzz/fast-check)
- [fast-check Documentation](https://fast-check.dev/)
- [Property-Based Testing Caught a Security Bug (Kiro)](https://kiro.dev/blog/property-based-testing-fixed-security-bug/)
- [LLM-Based Property-Based Test Generation for CPS (Springer)](https://link.springer.com/chapter/10.1007/978-3-032-07132-3_3)
- [Can LLMs Write Good Property-Based Tests? (arXiv)](https://arxiv.org/pdf/2307.04346)

### Chaos Engineering
- [Chaos Engineering for LLM Multi-Agent Systems (arXiv)](https://arxiv.org/abs/2505.03096)
- [ChaosEater: LLM-Powered Automated Chaos Engineering (arXiv)](https://arxiv.org/abs/2511.07865)
- [Gremlin: Chaos Engineering Tools Comparison](https://www.gremlin.com/community/tutorials/chaos-engineering-tools-comparison)
- [Steadybit: Top Chaos Engineering Tools 2025](https://steadybit.com/blog/top-chaos-engineering-tools-worth-knowing-about-2025-guide/)
- [LitmusChaos and Chaos Mesh Comparison](https://blog.container-solutions.com/comparing-chaos-engineering-tools)
- [Chaos Engineering Tooling Overview](https://system-design.space/en/chapter/chaos-engineering-tooling/)

### LLM Evaluation
- [DeepEval: RAGAS Metrics](https://deepeval.com/docs/metrics-ragas)
- [Braintrust: A/B Testing LLM Prompts](https://www.braintrust.dev/articles/ab-testing-llm-prompts)
- [Braintrust: LLM Evaluation Metrics Guide](https://www.braintrust.dev/articles/llm-evaluation-metrics-guide)
- [Top LLM Evaluation Frameworks 2026 (dev.to)](https://dev.to/guybuildingai/-top-5-open-source-llm-evaluation-frameworks-in-2024-98m)
- [Evidently AI: LLM-as-a-Judge Guide](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [Survey on LLM-as-a-Judge (arXiv)](https://arxiv.org/abs/2411.15594)
- [Confident AI: LLM Testing Methods 2026](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies)
- [Pragmatic Engineer: Guide to LLM Evals](https://newsletter.pragmaticengineer.com/p/evals)
- [Non-Determinism of Deterministic LLM Settings (ACL)](https://aclanthology.org/2025.eval4nlp-1.12.pdf)
- [LLM Evaluation Should Not Ignore Non-Determinism (NAACL 2025)](https://aclanthology.org/2025.naacl-long.211.pdf)
- [Langfuse: Testing LLM Applications](https://langfuse.com/blog/2025-10-21-testing-llm-applications)

### Contract Testing
- [Pact Documentation](https://docs.pact.io/)
- [Pact Contract Testing Best Practices 2025](https://www.sachith.co.uk/contract-testing-with-pact-best-practices-in-2025-practical-guide-feb-10-2026/)
- [PACT: Contracts Before Code (GitHub)](https://github.com/jmcentire/pact)
- [Best Contract Testing Tools 2026](https://www.testsprite.com/use-cases/en/the-best-contract-testing-tools)
- [Contract Testing vs Schema Testing (Pactflow)](https://pactflow.io/blog/contract-testing-using-json-schemas-and-open-api-part-1/)

### Testing Strategy
- [Test Pyramid 2.0: AI-Assisted Testing (Frontiers, 2025)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1695965/full)
- [CoverUp: Coverage-Guided LLM Test Generation (arXiv)](https://arxiv.org/html/2403.16218v3)
- [Automated Structural Testing of LLM-Based Agents (arXiv)](https://www.arxiv.org/pdf/2601.18827)
- [MuTAP: Mutation-Guided Test Generation (GitHub)](https://github.com/ExpertiseModel/MuTAP)
