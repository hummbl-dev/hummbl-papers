# Summary: RQ-004 -- Model Routing and Cascading Inference Optimization

**Source:** model_routing_cascading_inference_2026.md | **Date:** 2026-03-23

- **Core insight validated across multiple frameworks:** Not every query needs the most expensive model. RouteLLM (LMSYS/ICLR 2025) achieves 85% cost reduction on MT Bench while maintaining 95% GPT-4 quality by routing only 11% of queries to the expensive model via matrix factorization classifiers. FrugalGPT (Stanford/ICLR 2025) demonstrated complementary cascading strategies.
- **RouteLLM's matrix factorization router is lightweight enough for local deployment:** Pre-trained routers generalize across model pairs without retraining. The framework ships 5 router implementations (mf, bert, causal_llm, sw_ranking, random). Functionally stable but not actively developed as of March 2026 -- LMSYS shifted focus to Chatbot Arena.
- **Commercial routers exist (Martian, Not Diamond, OpenRouter)** but add dependency and cost. For HUMMBL's RTX 3080 Ti local stack, a hybrid approach is recommended: lightweight heuristic router + confidence-based cascading, with llama3.1:8b as default and escalation to larger models or API calls based on uncertainty signals.
- **Speculative decoding** enables faster inference by having a small draft model generate candidate tokens that a larger model verifies, achieving 2-3x speedup without quality loss. Relevant for the local inference stack.
- **Semantic caching** can layer on top of routing for repeated query patterns, further reducing cost for predictable workloads.
