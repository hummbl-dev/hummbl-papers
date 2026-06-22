# Summary: RQ-002 -- Automated Code Review and LLM-Based Defect Detection

**Source:** automated_code_review_2026.md | **Date:** 2026-03-23

- **Best tools detect 42-48% of real-world runtime bugs** and reduce manual review time by 40-60%. False positive rates as low as 1-2% in controlled studies. CodeRabbit leads with 2M+ repos and 46% bug detection accuracy on the Macroscope benchmark.
- **Hybrid pipeline is optimal:** Combining deterministic static analysis (Semgrep, CodeQL, SonarQube) with LLM-based contextual review achieves up to 94% detection effectiveness. Neither approach alone matches the combined result.
- **Critical blind spots remain:** Business logic errors, subtle security vulnerabilities, and cross-repository architectural issues are poorly handled by all current tools. GitHub Copilot Code Review cannot block merges or count toward required approvals by design.
- **Recommended HUMMBL strategy:** Tiered review pipeline -- static analysis as gate, LLM review for contextual feedback, human review reserved for architectural and security-critical changes.
- **Market pricing:** CodeRabbit Free-$24/dev/month; GitHub Copilot at 300-1,000 premium requests/month with fallback to base model. Both tools are generally available and production-ready.
