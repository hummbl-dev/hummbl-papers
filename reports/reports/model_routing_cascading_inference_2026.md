# RQ-004: Model Routing and Cascading Inference Optimization

**Research Date:** 2026-03-23
**Domain:** model_routing
**Target:** services/inference_agent

---

## Executive Summary

Model routing and cascading inference have matured rapidly from academic curiosities into production-grade infrastructure. The core insight is simple but powerful: not every query needs the most expensive model. By intelligently selecting which model handles each request — whether through learned classifiers, heuristic rules, or confidence-based escalation — systems can achieve 50-98% cost reductions while retaining 90-95%+ of top-model quality. This report synthesizes the current state of the art across frameworks (RouteLLM, FrugalGPT), commercial routers (Martian, Not Diamond, OpenRouter), speculative decoding, and practical patterns for consumer hardware and API-based inference.

**Key takeaway for HUMMBL:** A hybrid routing strategy combining a lightweight heuristic router with confidence-based cascading is the most practical path for the RTX 3080 Ti local stack. Start with llama3.1:8b as the default, escalate to larger local models or API calls based on uncertainty signals, and layer semantic caching on top for repeated patterns.

---

## 1. RouteLLM (LMSYS)

### Architecture and Approach

[RouteLLM](https://github.com/lm-sys/RouteLLM) is an open-source framework (Apache-2.0 license) developed by the LMSYS team that formalizes LLM routing as a binary classification problem: given a query, decide whether to route it to a strong/expensive model or a weak/cheap model. The decision is governed by a cost threshold parameter — higher thresholds favor the cheap model, lower thresholds favor the expensive one.

The framework was published as a conference paper at [ICLR 2025](https://openreview.net/forum?id=8sSqNntaMr).

### Router Models/Classifiers

RouteLLM ships with five router implementations:

| Router | Approach | Recommended? |
|--------|----------|-------------|
| **mf** (Matrix Factorization) | Learns embeddings for prompts and models from preference data | Yes (recommended) |
| **bert** | BERT classifier fine-tuned on preference data | Yes |
| **causal_llm** | LLM-based classifier tuned on preference data | Yes |
| **sw_ranking** | Weighted Elo calculation for routing | Moderate |
| **random** | Random baseline | No (benchmark only) |

All pre-trained routers were trained on the GPT-4-1106-preview vs. Mixtral-8x7B-Instruct-v0.1 model pair, but **generalize well** to other strong/weak model pairs without retraining.

### Performance Benchmarks

- **MT Bench:** Up to 85% cost reduction while maintaining 95% GPT-4 performance
- **MMLU:** 45% cost reduction
- **GSM8K:** 35% cost reduction
- The `router-mf-0.11593` threshold routes only 11% of queries to the expensive model while achieving 95% of GPT-4 quality
- Claimed to be >40% cheaper than commercial routing offerings at equivalent quality

### Current Status (March 2026)

The GitHub repository has 175 commits. The project is **functionally stable but not actively developed** — the LMSYS team shifted focus to Chatbot Arena and related evaluation infrastructure. The pre-trained routers remain effective for their intended model pairs. Installation: `pip install "routellm[serve,eval]"`.

**HUMMBL relevance:** RouteLLM's matrix factorization router is lightweight enough to run locally and could serve as a starting point for routing between local Ollama models and API calls. The preference-data training approach could be adapted using HUMMBL's own usage patterns.

---

## 2. FrugalGPT and Cascading Inference

### Original Paper Findings

[FrugalGPT](https://arxiv.org/abs/2305.05176) (Stanford, 2023; published at ICLR 2025) introduced three complementary strategies for reducing LLM inference costs:

**Strategy 1: Prompt Adaptation**
- Select only the most relevant few-shot examples via semantic similarity
- Batch multiple requests to eliminate redundant context
- Achieves ~70% token cost reduction on classification tasks

**Strategy 2: LLM Approximation**
- Implement caching (exact match + semantic) to avoid redundant API calls
- Fine-tune smaller models to approximate expensive ones
- Semantic caching alone achieves 21% cache hit rate with 95% cost/latency reduction
- Fine-tuned smaller models show 94% cost decreases without significant accuracy loss

**Strategy 3: LLM Cascade**
- Route queries through progressively more capable models
- Start with the cheapest model; escalate only when confidence is below threshold
- A scoring function evaluates whether responses meet quality criteria
- **Headline result:** Up to 98% cost reduction matching GPT-4 performance, or 4% accuracy improvement over GPT-4 at the same cost

### Real-World Implementations

[Portkey.ai's implementation](https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/) demonstrates production results:
- Standard cache: 8% hit rate with 99% cost savings per hit
- Semantic cache: 21% hit rate with 95% cost/latency reduction
- Combined cascade + caching: 80% cost reduction with 1.5% accuracy improvement over GPT-4

**Production deployment guidance:** Partition caches by user/org metadata to prevent data leakage, validate semantic similarity thresholds against 5,000+ test queries, and implement refresh workflows for negative feedback.

### Follow-Up Work

**C3PO (NeurIPS 2025):** [Cost Controlled Cascaded Prediction Optimization](https://arxiv.org/abs/2511.07396) advances FrugalGPT's cascade concept with:
- Conformal prediction to bound cost-exceeding probability
- Label-free cascade optimization using only unlabeled model outputs
- Achieves <20% of most-powerful-model cost with at most 2-10% accuracy gap
- State-of-the-art on GSM8K, MATH-500, BigBench-Hard, and AIME

**GATEKEEPER (2025):** A loss function that fine-tunes smaller models to output high confidence when correct and low confidence when incorrect, directly improving cascade routing accuracy.

**HUMMBL relevance:** The cascade pattern maps directly to the ai-stack architecture. llama3.1:8b handles the bulk of queries; uncertain responses escalate to a larger local model or cloud API. C3PO's label-free optimization is particularly attractive since it doesn't require ground-truth annotations.

---

## 3. Other Model Routing Approaches (2025-2026)

### Martian

[Martian](https://withmartian.com) is the most well-funded pure-play model routing startup:
- **Founded:** 2022, emerged from stealth Nov 2023 with $9M seed (NEA, Prosus, General Catalyst)
- **Technology:** "Model Mapping" — a mechanistic interpretability technique that unpacks LLMs into interpretable components to predict which model handles a given prompt best. This is the first commercial application of mechanistic interpretability for routing
- **Accenture investment** (2024) validates enterprise demand for routing infrastructure
- **Martian Gateway:** Unified access to 200+ AI models through a single API, compatible with OpenAI and Anthropic SDKs
- **2025 addition:** AI model compliance features within the router platform
- Hosted an [interpretability hackathon with Apart Research](https://apartresearch.com/sprints/apart-x-martian-mechanistic-router-interpretability-hackathon-2025-05-30-to-2025-06-01) in May 2025

### Not Diamond

[Not Diamond](https://www.notdiamond.ai/) positions itself as a routing optimization layer:
- **Core product:** AI model router that analyzes input and selects the optimal LLM based on evaluation data
- **Prompt Adaptation feature:** An agentic system that programmatically rewrites and optimizes prompts for each target model. Achieves 5-60% accuracy improvements on enterprise tasks (RAG, data extraction, text-to-SQL)
- **Automation claim:** Tasks requiring 40 hours of manual prompt engineering completed in under 1 hour
- **RouterArena ranking:** #12 overall — penalized for frequently selecting expensive models when cheaper ones suffice. This is a documented failure mode of learned routers
- Maintains [awesome-ai-model-routing](https://github.com/Not-Diamond/awesome-ai-model-routing) — a curated list of routing approaches on GitHub

### OpenRouter

[OpenRouter](https://openrouter.ai/) operates as an LLM gateway with built-in routing:

**Default behavior:** Load-balances across providers, prioritizing by inverse-square of price, with automatic failover for providers with recent outages.

**Routing shortcuts:**
| Modifier | Strategy |
|----------|----------|
| `:nitro` | Sort by throughput (speed-optimized) |
| `:floor` | Sort by price (cost-optimized) |
| `:exacto` | Quality-first signals tuned for tool-calling reliability |

**Auto Router:** Analyzes prompt complexity and task type to select from curated high-quality models automatically.

**Smart features:** Automatic tool-use provider filtering, rate-limit failover, max_tokens-aware routing, response length-aware provider selection.

### Anthropic's Model Selection Guidance

Anthropic structures Claude around three tiers with clear use-case mapping:
- **Haiku:** High-volume, simple tasks (customer service, moderation, quick answers). Not suitable for complex coding
- **Sonnet:** The daily driver for most workloads. Sonnet 4.6 preferred over Sonnet 4.5 by 70% of developers and over Opus 4.5 by 59%
- **Opus:** Complex reasoning, architectural decisions, debugging. Reserve for tasks that genuinely need it

**Strategic pattern:** Default to Sonnet, escalate to Opus for hard tasks, use Haiku for automation. This three-tier structure maps naturally to cascade architectures.

### Academic Papers on Learned Routers

**RouterArena (2025):** The first [open evaluation platform](https://routeworks.github.io/) for LLM routers. Key findings:
- Evaluates across 8,400 queries in 9 domains at 3 difficulty levels
- Metrics: accuracy, cost, routing optimality, robustness, latency
- CARROT performs well on accuracy + latency; RouterDC excels on cost-ratio
- **Commercial routers do not necessarily outperform open-source ones**
- GPT-5-as-router ranks #7 due to restricted model pool

**Router-R1 (2025):** RL-based framework using an LLM as the router itself, with "think" actions (deliberation) and "route" actions (model invocation). Treats multi-model routing as a sequential decision process.

**Universal Model Routing (2025):** Represents each LLM as a feature vector from predictions on representative prompts, enabling routing without per-pair training.

**Key empirical finding:** Models with learned routing often **underperform** parameter-matched dense models and heuristic-routing baselines. Learned routers suffer from a systematic failure mode: as budget increases, they default to the most expensive model even when cheaper ones suffice. This suggests **hybrid approaches combining heuristics with learned components** are the most promising direction.

---

## 4. Speculative Decoding and Draft Models

### Current State in Production (2026)

Speculative decoding has gone from research experiment to **production standard**, now built into vLLM (v0.8.5+), SGLang, TensorRT-LLM, and all major serving frameworks. The core idea: a lightweight draft model proposes several tokens, and the target model verifies them in parallel, producing multiple tokens per forward pass.

### Key Approaches

**EAGLE-3 (State of the Art):**
- Lightweight autoregressive prediction head attached to target model layers
- Eliminates need for separate draft model
- Training-time testing simulates inference conditions, addressing distribution mismatch
- **Performance:** 4.0-4.8x speedup for LLaMA-3.3-70B; 2.5x on 4xA100 in practice
- Realistic acceptance rates: 0.75-0.85 on general queries
- Minimal memory overhead (hundreds of millions of parameters)

**Medusa:**
- Adds multiple extra language model heads to predict future tokens
- Each head predicts progressively further tokens
- Base model remains unchanged — only heads are trained
- Lower speedup than EAGLE-3 but simpler to integrate

**Other Notable Approaches:**
- **PEARL (ICLR 2025):** Parallel speculative decoding with adaptive draft length
- **Apple's Recurrent Drafter:** Recurrent architecture for fast draft generation
- **Judge Decoding (ICLR 2025):** Alternative verification schemes beyond standard logits
- **Speculative Speculative Decoding (ICLR 2026):** Meta-level speculation optimization

### Framework Support Matrix

| Framework | EAGLE-3 | External Draft | N-gram |
|-----------|---------|----------------|--------|
| vLLM | v0.8.5+ | Yes | Yes |
| SGLang | Native | Yes | Yes |
| TensorRT-LLM | Yes | Yes | Yes |

### Interaction with Model Routing

**SpecRouter (2025):** A novel framework that [combines routing with speculative decoding](https://arxiv.org/abs/2505.07680):
- Dynamically constructs inference "paths" (chains of draft + verifier models)
- Adaptive model chain scheduling based on performance profiling and token distribution divergence
- Multi-level collaborative verification reduces burden on the target model

**R2R (Roads to Rome):** Token-level routing that selectively uses large models only for "path-divergent" tokens during small-model generation. Eliminates rollback overhead, especially beneficial in batch serving.

**Faster Cascades via Speculative Decoding (ICLR 2025):** Directly applies speculative decoding principles to cascade systems, using the small cascade model as a draft for the large one.

**HUMMBL relevance:** Speculative decoding is most impactful at low batch sizes (the consumer hardware scenario). For the RTX 3080 Ti, EAGLE-3 with llama3.1:8b as the draft model for a larger 27B+ model could deliver 2-3x latency reduction without quality loss. Ollama does not yet natively support speculative decoding, but vLLM does.

---

## 5. Practical Routing for Consumer Hardware

### Routing Between Local Models (RTX 3080 Ti Context)

The ai-stack runs llama3.1:8b at 133 tok/s with 4.8 quality score on the RTX 3080 Ti. Routing options for this setup:

**LiteLLM + Ollama:** LiteLLM provides routing logic, fallbacks, and observability while Ollama runs local models. Semantic routing uses embeddings to match queries against predefined utterances, selecting the best model based on similarity scores.

**Configuration approach:**
- Define routing rules mapping query types to models
- Set confidence thresholds (start conservative at 0.70, lower to 0.30 as accuracy data builds)
- Log all routing decisions with confidence scores for iterative improvement
- Auto-router can detect task complexity and escalate to cloud models when needed

### Heuristic vs. Learned Routers at Small Scale

**The evidence favors heuristics at small scale:**
- Learned routers require substantial training data (thousands of labeled routing decisions)
- They suffer from systematic failure modes: defaulting to expensive models as budgets increase
- At small scale, simple rules (keyword matching, prompt length, task-type classification) are more predictable
- Heuristic-guided RL approaches outperform pure learned routing (11% lower latency)

**Recommended progression:**
1. **Start:** Simple heuristic rules (prompt length, keyword patterns, task classification)
2. **Grow:** Add confidence-based escalation from model log-probabilities
3. **Mature:** Train a lightweight learned router (BERT classifier or matrix factorization) on accumulated routing data
4. **Optimize:** Hybrid approach using heuristic pre-filtering with learned fine-tuning

### Confidence-Based Cascading

The most practical approach for consumer hardware:

1. **Small model first:** llama3.1:8b handles all incoming queries
2. **Uncertainty estimation:** Extract log-probabilities or entropy from the response
3. **Escalation threshold:** If confidence < threshold, escalate to next tier
4. **Cascade tiers:**
   - Tier 0: llama3.1:8b (local, 133 tok/s, free)
   - Tier 1: Larger local model if VRAM allows (model swap overhead ~2-5s on Ollama)
   - Tier 2: Cloud API (Claude Sonnet for balanced tasks)
   - Tier 3: Cloud API (Claude Opus for hard reasoning)

**GATEKEEPER approach:** Fine-tune the small model's confidence calibration so high confidence = actually correct, low confidence = actually wrong. This directly improves cascade accuracy.

### Latency vs. Quality Tradeoffs

| Configuration | Latency | Quality | Cost |
|--------------|---------|---------|------|
| Always 8b local | ~50ms/tok | Baseline | Free |
| 8b + escalate to cloud | 50ms-2s | +15-25% | Low |
| Always cloud Sonnet | 200-500ms | +20-30% | Moderate |
| Always cloud Opus | 500ms-2s | +25-40% | High |
| Cascade (8b → Sonnet → Opus) | Variable | Near-Opus | 70-85% savings vs always-Opus |

Key consideration: Ollama model swapping adds 2-5 seconds of latency. For local cascading, keep the primary model loaded and use API calls for escalation rather than swapping local models.

---

## 6. Cost Optimization Patterns for API-Based Inference

### Token-Efficient Prompting Techniques

**Prompt Compression:**
- [LLMLingua](https://llmlingua.com/llmlingua.html): Uses a smaller LM to rank and preserve key tokens. Achieves up to 20x compression with minimal performance loss
- Variants: LongLLMLingua (long-context), AdaComp (adaptive), PCRL/TACO-RL (RL-based)
- **Practical impact:** A 5x compressed prompt at 95% quality retention directly translates to 5x cost reduction on input tokens

**Few-Shot Optimization:**
- Semantic similarity selection of examples instead of fixed sets
- Reducing 20 examples to 5 most relevant: 70% token cost reduction (per FrugalGPT)
- Dynamic example selection based on query embedding distance

**Structured Output:**
- Request JSON/structured responses to reduce verbose explanations
- Specify exact output format to minimize wasted tokens
- Use stop sequences aggressively

### Caching Strategies

**Multi-Tier Caching (recommended architecture):**

| Tier | Type | Hit Rate | Latency | Cost Savings |
|------|------|----------|---------|-------------|
| L1 | Exact match | 5-15% | <1ms | 99%+ per hit |
| L2 | Semantic cache | 15-25% | 10-50ms | 95% per hit |
| L3 | Prefix/KV cache | Variable | Minimal | 30-70% on matching prefixes |

**Semantic cache implementation notes:**
- GPTSemCache reports 61.6-68.8% cache hit rates across query categories
- Embedding similarity threshold: start at 0.95 cosine similarity, tune down carefully
- Partition by user/org to prevent data leakage
- Implement TTL and negative-feedback invalidation
- Cache invalidation is the hard problem — stale cached answers degrade quality silently

**KV Cache optimization (relevant to local inference):**
- q8_0 KV cache quantization is active on the ai-stack (per memory notes)
- q4_0 validated as feasible for even more memory savings
- ChunkKV (2025): Treats semantic chunks as compression units rather than individual tokens, preserving linguistic structure. Reduces KV cache memory by up to 70%

### Batch vs. Streaming Tradeoffs

| Dimension | Batch | Streaming |
|-----------|-------|-----------|
| Cost | 50% discount (most providers) | Full price |
| Latency | Minutes to hours | Sub-second TTFT |
| Throughput | 10-20x higher with continuous batching | Per-request |
| Use case | Classification, extraction, enrichment | Chat, real-time interaction |

**Anthropic-specific:** Claude 3 with continuous batching increased throughput from 50 to 450 tok/s, lowered latency from 2.5s to 0.8s, cut GPU costs by 40%.

**Recommendation:** Use batch APIs for all non-interactive workloads. For HUMMBL's autoresearch pipeline, batch processing research queries through the API at 50% cost reduction is a straightforward win.

### Prompt Compression Techniques

**Active techniques in production (2026):**
1. **LLMLingua family:** Coarse-to-fine compression, budget controller for semantic integrity
2. **Token merging:** Dynamically reduce sequence length during decoding
3. **Context distillation:** Pre-process long contexts into compressed summaries
4. **Mixture-of-Depths:** Route only subset of tokens through full transformer blocks

**Practical savings stack:**
- Prompt compression (3-5x) + semantic caching (20% hit rate) + batch APIs (50% discount) = **75-90% total cost reduction** compared to naive streaming with full prompts.

---

## 7. Synthesis: Recommended Architecture for HUMMBL

### Immediate Actions (Week 1-2)

1. **Implement heuristic routing in the inference agent:**
   - Classify queries by type (code, reasoning, simple Q&A, creative)
   - Route simple queries to llama3.1:8b (local, free)
   - Route complex reasoning to Claude Sonnet via API
   - Reserve Claude Opus for architectural decisions and hard debugging

2. **Add exact-match caching:**
   - Hash-based cache for identical prompts
   - Minimal implementation effort, immediate savings on repeated patterns

3. **Use batch APIs for autoresearch:**
   - All research queries processed via batch endpoints at 50% discount
   - Non-interactive pipeline is ideal for batch processing

### Medium-Term (Month 1-2)

4. **Implement confidence-based cascading:**
   - Extract log-probabilities from llama3.1:8b responses
   - Calibrate escalation thresholds on 500+ labeled examples
   - Track routing accuracy and adjust thresholds

5. **Add semantic caching:**
   - Embedding-based similarity cache with 0.95 cosine threshold
   - Partition by task type and user context
   - Target: 15-20% cache hit rate

6. **Prompt compression:**
   - Integrate LLMLingua for long-context API calls
   - 3-5x compression = 3-5x input token cost reduction

### Longer-Term (Month 3+)

7. **Train a lightweight learned router:**
   - Collect routing decision data from heuristic phase
   - Train RouteLLM-style matrix factorization model on accumulated data
   - A/B test against heuristic router

8. **Explore speculative decoding:**
   - If migrating local serving from Ollama to vLLM, enable EAGLE-3
   - Potential 2-3x latency improvement for local inference
   - Most impactful for the single-user, low-batch scenario

9. **Cross-machine routing:**
   - Route between Desktop (RTX 3080 Ti, PyTorch/CUDA) and Nodezero (MLX)
   - LiteLLM can manage both as backend providers
   - Latency-aware routing based on LAN conditions

### Expected Impact

| Optimization | Estimated Savings | Implementation Effort |
|-------------|-------------------|----------------------|
| Heuristic routing (local vs API) | 60-70% API cost reduction | Low |
| Exact-match caching | 5-15% additional savings | Low |
| Batch API for research | 50% on batch workloads | Low |
| Confidence cascading | 10-20% quality improvement at same cost | Medium |
| Semantic caching | 15-25% additional savings | Medium |
| Prompt compression | 60-80% input token reduction | Medium |
| Learned router | 5-10% improvement over heuristics | High |
| Speculative decoding | 2-3x latency reduction (local) | High (requires vLLM migration) |

**Conservative total estimate:** 75-85% cost reduction on API spend with <5% quality degradation, plus 2-3x latency improvement on local inference with speculative decoding.

---

## 8. Key Papers and Resources

### Foundational Papers
- **RouteLLM** — Ong et al., ICLR 2025. [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)
- **FrugalGPT** — Chen et al., ICLR 2025. [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)
- **C3PO** — Valk et al., NeurIPS 2025. [arXiv:2511.07396](https://arxiv.org/abs/2511.07396)

### Surveys
- **Dynamic Model Routing and Cascading Survey** — March 2026. [arXiv:2603.04445](https://arxiv.org/abs/2603.04445)
- **Efficient Multi-LLM Inference** — June 2025. [arXiv:2506.06579](https://arxiv.org/html/2506.06579v1)
- **Doing More with Less: Routing Strategies Survey** — Feb 2025. [arXiv:2502.00409](https://arxiv.org/html/2502.00409)

### Evaluation
- **RouterArena** — Oct 2025. [arXiv:2510.00202](https://arxiv.org/abs/2510.00202)
- **RouterBench** — March 2024. [arXiv:2403.12031](https://arxiv.org/abs/2403.12031)

### Speculative Decoding
- **EAGLE-3** — 2025. [Project page](https://sites.google.com/view/eagle-llm)
- **SpecRouter** — May 2025. [arXiv:2505.07680](https://arxiv.org/abs/2505.07680)
- **Speculators (Red Hat)** — Nov 2025. [Article](https://developers.redhat.com/articles/2025/11/19/speculators-standardized-production-ready-speculative-decoding)

### Confidence and Uncertainty
- **GATEKEEPER** — Feb 2025. [arXiv:2502.19335](https://arxiv.org/html/2502.19335v3)
- **Router-R1** — Oct 2025. [OpenReview](https://openreview.net/forum?id=DWf4vroKWJ)
- **When Routing Collapses** — Feb 2026. [arXiv:2602.03478](https://arxiv.org/pdf/2602.03478)

### Commercial Platforms
- [RouteLLM GitHub](https://github.com/lm-sys/RouteLLM) — Open-source, Apache-2.0
- [Martian](https://withmartian.com) — Model routing startup, $9M+ funded
- [Not Diamond](https://www.notdiamond.ai/) — Routing optimization layer
- [OpenRouter](https://openrouter.ai/) — LLM gateway with routing
- [LiteLLM](https://docs.litellm.ai/) — Open-source routing + observability

### Caching and Compression
- [LLMLingua](https://llmlingua.com/llmlingua.html) — Prompt compression (up to 20x)
- [Portkey FrugalGPT Implementation](https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/) — Production caching patterns
- **ChunkKV** — 2025. [arXiv:2502.00299](https://arxiv.org/html/2502.00299v5)

---

*Report generated by autoresearch pipeline. Next scheduled review: 2026-04-23.*
