# Summary: RQ-008 -- LLM Inference Cost Optimization

**Source:** llm_cost_optimization_2026.md | **Date:** 2026-03-23

- **LLM inference costs falling at median 50x/year, accelerating to 200x/year since Jan 2024** (Epoch AI). Despite this, cost optimization remains critical because usage scales faster than prices drop. Combined techniques can reduce costs 80-95% vs naive implementations.
- **Prompt caching is the single highest-ROI optimization:** Anthropic offers 90% discount on cached prompt reads. Batch APIs provide guaranteed 50% savings for non-real-time workloads. These two alone can halve costs with minimal engineering effort.
- **Prompt compression (LLMLingua) achieves up to 20x compression with only 1.5% performance loss** on reasoning tasks. LongLLMLingua boosts performance by 21.4% with 4x fewer tokens on long-context scenarios. Practical for production use.
- **Speculative decoding (EAGLE-3) delivers 2-3x latency reduction in production.** AWQ quantization retains 95% quality at 4-bit precision. Both directly relevant to the RTX 3080 Ti local inference stack.
- **Local inference on RTX 3080 Ti breaks even vs API at ~3,500 active hours for small models.** Budget governors with hierarchical controls are now table-stakes for production LLM systems. HUMMBL's cost tracker service should implement per-agent budgets with automatic model downgrades at threshold.
