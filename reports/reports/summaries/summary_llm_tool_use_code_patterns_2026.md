# Summary: RQ-001 v2 -- LLM Tool Use Patterns for Code Generation and Review

**Source:** llm_tool_use_code_patterns_2026.md | **Date:** 2026-03-23

- **SWE-bench Verified scores jumped from ~65% (early 2025) to 80.9% (March 2026).** AI code review tools now detect ~48% of real-world runtime bugs. The agentic coding tool market has consolidated into four distinct categories.
- **Edit format selection is a critical lever:** Can swing performance by 2-3x independent of model quality. Context engineering has emerged as the primary bottleneck in agent performance, more important than model selection.
- **Provider convergence with important differences:** Claude supports "interleaved thinking" (reasoning + tool use in single turns); GPT-4/5 offers strict mode for schema adherence; Gemini supports OpenAPI JSON Schema or Python function definitions. Aggregation gateways are standardizing on OpenAI's tool format.
- **Key patterns:** Flat parameter structures (dot-notation instead of nested objects), on-demand tool loading vs upfront definitions, schema precision with explicit required/optional marking, and self-contained tool descriptions.
- **Persistent weakness in security vulnerability detection:** ~30%+ false positive rates. LLMs struggle with business logic errors, subtle security vulnerabilities, and cross-repository architectural issues.
