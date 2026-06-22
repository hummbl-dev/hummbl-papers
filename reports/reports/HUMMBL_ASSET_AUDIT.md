# HUMMBL Complete Asset Audit

**Date:** 2026-03-24
**Auditor:** Claude Opus 4.6 (automated)
**Scope:** All GitHub repos (hummbl-dev, hummbl-dev-org, trevin-creator), local machine code, research corpus

---

## Executive Summary

HUMMBL, LLC controls **57 GitHub repositories** across 3 organizations plus local-only assets. The portfolio spans a cognitive AI framework (Base120), agent governance libraries, production infrastructure, research automation, and experimental projects. Key findings:

- **3 published packages** (npm, PyPI) with real external users
- **1 repo with 1,000+ stars** (autoresearch-mlx under trevin-creator)
- **40 research reports** generated overnight by the autoresearch pipeline
- **~20 repos are actively maintained** (commits in March 2026)
- **~15 repos are dormant/abandoned** (no commits since Feb 2026 or earlier)
- **Significant IP concentration** in Base120 framework, governance primitives, and MCP server

---

## 1. GitHub Organizations

### hummbl-dev (Primary) — 55 repos

| # | Repo | Description | Lang | Stars | Visibility | Last Commit | Status |
|---|------|-------------|------|-------|------------|-------------|--------|
| 1 | **mcp-server** | HUMMBL MCP Server — Base120 mental models via MCP | TypeScript | 3 | Public | 2026-03-24 | **ACTIVE — Published on npm** |
| 2 | **hummbl-governance** | Governance runtime: kill switch, circuit breaker, cost governor, delegation tokens, audit log | Python | 0 | Public | 2026-03-24 | **ACTIVE — Published on PyPI, 157 tests** |
| 3 | **base120** | Deterministic governance substrate, v1.0.0 reference implementation | Python | 0 | Public | 2026-03-24 | **ACTIVE — Published on PyPI** |
| 4 | **hummbl-bibliography** | LaTeX bibliography of HUMMBL research | TeX | 1 | Public | 2026-03-24 | ACTIVE |
| 5 | **agentic-patterns** | Stdlib-only safety patterns for agentic AI | Python | 0 | Public | 2026-03-24 | ACTIVE |
| 6 | **governed-iac-reference** | Governed Infrastructure as Code reference | Shell | 1 | Public | 2026-03-24 | ACTIVE |
| 7 | **arbiter** | Agent-aware code quality system | Python | 0 | Public | 2026-03-24 | ACTIVE |
| 8 | **autoresearch-reports** | Raw reports, distilled findings, improvement proposals | Shell | 0 | Public | 2026-03-24 | **ACTIVE — 40 reports** |
| 9 | **hummbl-monorepo** | Monorepo: MCP server + web app + Cloudflare Workers | TypeScript | 0 | Public | 2026-02-15 | MAINTAINED — Audit score 78/100 |
| 10 | **hummbl-production** | Cloudflare Workers stack for hummbl.io (D1, KV, Claude API) | HTML | 0 | Public | 2026-02-27 | MAINTAINED — Production |
| 11 | **hummbl-agent** | Governed agent infrastructure with deterministic control plane | TypeScript | 2 | Public | 2026-02-17 | MAINTAINED |
| 12 | **forge** | Multi-agent factory system, auto-scaling pools, smart routing | Python | 0 | Public | 2026-03-05 | MAINTAINED |
| 13 | **hybrid-inference** | Local+cloud LLM routing with EDR governance | Python | 0 | Public | 2026-03-01 | MAINTAINED |
| 14 | **agent-os** | Shared agent infrastructure: skills, contracts | Python | 0 | Public | 2026-02-22 | MAINTAINED |
| 15 | **founder-mode** | Multi-agent coordination workspace for founders (shared w/ Dan Matha) | Python | 0 | Public | 2026-03-24 | **ACTIVE — Primary dev workspace** |
| 16 | **hummbl** | Python reasoning framework (v0.3) with peptide protocol | Python | 0 | Public | 2026-03-03 | MAINTAINED |
| 17 | **hummbl-dev** | Org profile/meta repo | — | 0 | Public | 2026-03-23 | META |
| 18 | **shared-hummbl-space** | Shared agent workspace | Python | 0 | Public | 2026-02-15 | MAINTAINED |
| 19 | **hummbl-claude-skills** | Claude skills for HUMMBL framework | — | 4 | Public | 2026-03-07 | MAINTAINED |
| 20 | **claude-code-folder** | Claude Code agent workspace config | Python | 0 | Public | 2026-03-23 | MAINTAINED |
| 21 | **kimi-code-folder** | Kimi Code agent workspace | Python | 0 | Public | 2026-03-23 | MAINTAINED |
| 22 | **codex-agent-folder** | Codex agent workspace | Shell | 0 | Public | 2026-02-08 | DORMANT |
| 23 | **hummbl-mobile** | Expo/React Native mobile app | TypeScript | 0 | Public | 2026-02-15 | DORMANT |
| 24 | **hummbl-old-version** | Legacy TypeScript version | TypeScript | 0 | Public | 2026-02-15 | ARCHIVED |
| 25 | **hummbl-systems** | Systems repo | TypeScript | 0 | Public | 2026-02-15 | DORMANT |
| 26 | **hummbl-gpts** | Custom GPT specifications | JavaScript | 0 | Public | 2026-02-15 | DORMANT |
| 27 | **hummbl-research** | Research repo | Python | 1 | Public | 2026-02-15 | DORMANT |
| 28 | **hummbl-prototype** | Transformation algorithm testing | Python | 1 | Public | 2026-02-15 | DORMANT |
| 29 | **engine-ops** | Engine optimization operations | HTML | 1 | Public | 2026-02-15 | DORMANT |
| 30 | **HUMMBL-Unified-Tier-Framework** | Problem complexity classification (Base6-BASE120) | — | 1 | Public | 2026-02-15 | DORMANT |
| 31 | **hummbl-agent-federation** | Agent federation | Python | 0 | Public | 2026-02-15 | DORMANT |
| 32 | **hummbl-infra** | Infrastructure scripts | Shell | 0 | Public | 2026-02-07 | DORMANT |
| 33 | **aaa** | Assured Agentic Architecture | Python | 0 | Public | 2026-03-02 | DORMANT |
| 34 | **hummbl-gaas-platform** | Governance-as-a-Service platform | — | 0 | Public | 2026-03-11 | SPEC ONLY |
| 35 | **ci-governance** | CI governance | — | 0 | Public | 2026-02-15 | DORMANT |
| 36 | **base120-corpus-validator** | System B corpus validation | — | 0 | Public | 2026-03-11 | SPEC ONLY |
| 37 | **identity-root** | Identity root | — | 0 | Public | 2026-03-11 | SPEC ONLY |
| 38 | **discovery** | Discovery | — | 0 | Public | 2026-03-11 | SPEC ONLY |
| 39 | **docs** | Documentation | — | 0 | Public | 2026-03-11 | SPEC ONLY |
| 40 | **games** | Logic games | — | 0 | Public | 2026-03-11 | DORMANT |
| 41 | **god-mode** | God mode | — | 0 | Public | 2026-03-11 | DORMANT |
| 42 | **mirror-agent** | Mirror agent | — | 0 | Public | 2026-03-11 | DORMANT |
| 43 | **rpbx** | Agentic clone of Reuben Bowlby | — | 0 | Public | 2026-03-11 | DORMANT |
| 44 | **sys-arch-testing** | Systems architecture testing | — | 0 | Public | 2026-03-11 | DORMANT |
| 45 | **autoresearch-win-rtx** | Windows RTX autoresearch (fork of Karpathy) | Python | 0 | Public | 2026-03-14 | MAINTAINED |
| 46 | **autoresearch-pipeline** | NemoClaw supervisor-worker pipeline | — | 0 | **Private** | 2026-03-17 | MAINTAINED |
| 47 | **hummbl-cca-f** | (Unknown - private) | — | 0 | **Private** | 2026-03-23 | PRIVATE |
| 48 | **Poe-bots** | Poe bot organization | Python | 0 | **Private** | 2026-03-20 | MAINTAINED |
| 49 | **peptide-checker** | Peptide product checker/database | Python | 0 | **Private** | 2026-03-15 | MAINTAINED |
| 50 | **hummbl-v2** | HUMMBL v2 Next.js 15 platform | TypeScript | 0 | **Private** | 2025-12-06 | ABANDONED |
| 51 | **hummbl-asi** | HUMMBL ASI Framework | JavaScript | 0 | **Private** | 2025-12-06 | ABANDONED |
| 52 | **public-domain-health-corpus** | Historical text to knowledge graph | — | 0 | **Private** | 2025-12-19 | ABANDONED |
| 53 | **init-system** | Init system | Shell | 0 | **Private** | 2026-03-23 | PRIVATE |
| 54 | **caes-tools** | CAES tooling | — | 0 | **Private** | 2026-03-23 | PRIVATE |
| 55 | **workflow** | Workflow DevKit (fork) | TypeScript | 0 | **Private** | 2026-03-23 | FORK |

**Forks (public):**
- everything-claude-code (fork) — Claude Code config collection
- clawdhub (fork) — Skill directory for clawdbot
- claude-code-infrastructure-showcase (fork, 1 star)
- gastown (fork) — Multi-agent workspace manager (Go)
- OpenAgent (fork, private) — Web3 AI agent

### hummbl-dev-org — 1 repo

| Repo | Description | Visibility | Last Commit |
|------|-------------|------------|-------------|
| **hummbl-models** | HUMMBL models (TeX) | **Private** | 2026-03-19 |

### trevin-creator (Nodezero/Mac account) — 3 repos

| Repo | Description | Lang | Stars | Last Commit | Status |
|------|-------------|------|-------|-------------|--------|
| **autoresearch-mlx** | Apple Silicon MLX port of Karpathy's autoresearch | Python | **1,006** | 2026-03-24 | **ACTIVE — FLAGSHIP OPEN SOURCE** |
| **Tiny-Lab** | Apple Silicon ML research tool with control plane | Python | **90** | 2026-03-18 | ACTIVE |
| **lyte-converse** | (Unknown) | Python | 0 | 2026-02-27 | DORMANT |

---

## 2. Local Machine Assets (Desktop — Windows 11, RTX 3080 Ti)

### Git Repositories

| Directory | Remote | Last Commit | Purpose |
|-----------|--------|-------------|---------|
| `~/hummbl/` | hummbl-dev/hummbl | v0.3 with peptide protocol | Python reasoning framework |
| `~/founder-mode/` | hummbl-dev/founder-mode | 2026-03-24 | Primary multi-agent dev workspace |
| `~/autoresearch-reports/` | hummbl-dev/autoresearch-reports | 2026-03-24 | Overnight research corpus |
| `~/autoresearch-win-rtx/` | hummbl-dev/autoresearch-win-rtx | 2026-03-14 | Windows RTX training runner |
| `~/autoresearch-pipeline/` | hummbl-dev/autoresearch-pipeline | NemoClaw v0.1.4 | Supervisor-worker pipeline |
| `~/autoresearch/` | **karpathy/autoresearch** (upstream) | Upstream fork | Original Karpathy autoresearch |
| `~/peptide-checker/` | hummbl-dev/peptide-checker | 2026-03-15 | Consumer peptide product database |

### Non-Git Directories

| Directory | Contents | Purpose |
|-----------|----------|---------|
| `~/ai-stack/` | Golden Ratio Stack benchmarks, 8 experiments | Local inference benchmarking suite |
| `~/agent-bin/` | powershell.cmd, pwsh.cmd | Agent binary shims |
| `~/logs/` | Log files | System logs |

### Research Corpus (autoresearch-reports)

**40 research reports** including:
- AI Incubator Curriculum (12-week program)
- Consulting Revenue Playbook
- Decision Matrix: What to Build
- Healthcare MCP Integration Guide
- HUMMBL 90-Day Roadmap
- HUMMBL Architecture Spec
- HUMMBL GaaS Product Spec
- HUMMBL Bus Protocol Spec
- NemoClaw Implementation Guide
- Overnight Research Service Design
- ThinkPRM Implementation Guide
- SWIRL RLVR Training Guide
- Agent Frameworks Comparison 2026
- AI Governance Compliance 2026
- LLM Cost Optimization 2026
- Various domain-specific research reports

### Founder-Mode Workspace Structure

The `founder-mode` repo is the central orchestration hub containing:
- `founder_mode/cognition/` — Working memory, retrieval, state management, research processor
- `founder_mode/agents/` — Factorio system, The Forge agent runners
- `founder_mode/apps/crm/` — CRM application
- `founder_mode/bus/` — Message bus infrastructure
- `governance/CAES_SPEC.md` — Canonical governance spec
- `PROJECTS/platform/` — Platform project definitions

---

## 3. Published Packages

| Package | Registry | Repo | Status |
|---------|----------|------|--------|
| `@hummbl/mcp-server` | **npm** | mcp-server | Published, listed on glama.ai |
| `hummbl-governance` | **PyPI** | hummbl-governance | Published, 157 tests |
| `base120` | **PyPI** | base120 | Published, v1.0.0 |
| `forge-agent-system` | **PyPI** | forge | Published |

---

## 4. Production Infrastructure

| Asset | Platform | URL | Status |
|-------|----------|-----|--------|
| hummbl.io website | Cloudflare Pages | https://hummbl.io | Live |
| HUMMBL API | Cloudflare Workers | hummbl-api.hummbl.workers.dev | Live |
| D1 Database | Cloudflare D1 | (via Workers) | Active |
| KV Store | Cloudflare KV | (via Workers) | Active |

---

## 5. Monetization Assessment

### Tier 1: Ready to Monetize Now

| Asset | Model | Rationale |
|-------|-------|-----------|
| **MCP Server** (npm) | Freemium / Enterprise license | 3 stars, published, working product on glama.ai. Free tier attracts users, paid tier adds enterprise governance features. |
| **hummbl-governance** (PyPI) | Open-core / Enterprise support | Zero-dep governance primitives with 157 tests. Enterprises need this. Free library + paid support/SLA. |
| **Consulting playbook** | Services revenue | The research reports contain a complete consulting revenue playbook already written. |
| **AI Incubator Curriculum** | Education / cohort model | 12-week program spec with $5K + 2% equity hybrid model already designed. |

### Tier 2: Near-Term Monetization (1-3 months)

| Asset | Model | Rationale |
|-------|-------|-----------|
| **Base120 framework** | Certification / licensing | 120 validated mental models is unique IP. License to consulting firms, integrate into LLM workflows. |
| **Forge** (multi-agent system) | SaaS / managed service | Production-grade orchestration with auto-scaling. Package as managed agent infrastructure. |
| **hybrid-inference** | Enterprise tool | Local-first inference routing with governance is exactly what enterprises want for AI deployment. |
| **Overnight Research Service** | Productized service | The autoresearch pipeline already generates reports. Package as "overnight AI research analyst." |
| **autoresearch-mlx** (1K stars) | Sponsorship / pro features | Strong community traction on trevin-creator. Add premium features, enterprise support. |

### Tier 3: Strategic / Long-Term

| Asset | Model | Rationale |
|-------|-------|-----------|
| **Peptide Checker** | Consumer health SaaS | Private database of peptide products with safety analysis. Niche but defensible. |
| **GaaS Platform** | Governance-as-a-Service | Spec exists but needs implementation. High-value enterprise play. |
| **hummbl-agent** | Platform play | Governed agent infrastructure could become a developer platform. |

---

## 6. Open-Source Assessment

### Already Open Source (Public)
- 42 of 55 hummbl-dev repos are public
- autoresearch-mlx (1,006 stars) is the most successful open-source asset

### Should Consider Open-Sourcing
| Repo | Currently | Recommendation |
|------|-----------|----------------|
| **agentic-patterns** | Public | Already open. Market it more — zero-dep safety patterns have broad appeal. |
| **governed-iac-reference** | Public | Good reference material for enterprise adoption. |
| **hummbl-bibliography** | Public | Builds academic credibility. |

### Should Keep Private
| Repo | Reason |
|------|--------|
| peptide-checker | Commercial potential, proprietary data |
| hummbl-models (hummbl-dev-org) | Core IP — the 120 models dataset |
| autoresearch-pipeline | Competitive advantage in NemoClaw architecture |
| hummbl-cca-f | Unknown but private for a reason |
| hummbl-asi | ASI framework — speculative but sensitive |

---

## 7. Dependency Map

```
                    BASE120 (core framework)
                         |
              +----------+----------+
              |                     |
       hummbl-governance      mcp-server (npm)
              |                     |
    +---------+---------+     hummbl-production
    |         |         |      (hummbl.io)
  forge   hybrid-    agentic-
          inference   patterns
              |
        founder-mode (central hub)
         |         |          |
   agent-os   autoresearch-  peptide-
              pipeline       checker
              |
        autoresearch-win-rtx
        autoresearch-mlx (trevin-creator)
```

---

## 8. Cleanup Recommendations

### Archive (no recent activity, no clear purpose)
- hummbl-old-version
- hummbl-v2 (abandoned Dec 2025)
- hummbl-asi (abandoned Dec 2025)
- public-domain-health-corpus (abandoned Dec 2025)
- god-mode, mirror-agent, rpbx, sys-arch-testing (spec-only, dormant)
- games, discovery, docs (empty or minimal)

### Consolidate
- `hummbl-monorepo` vs `hummbl-production` — both serve hummbl.io, unclear boundary
- `claude-code-folder` / `kimi-code-folder` / `codex-agent-folder` — three separate agent workspace repos could be one
- `hummbl-agent` vs `agent-os` vs `hummbl-agent-federation` — overlapping agent infrastructure

### Rename for Clarity
- `hummbl` (the Python package) is confusingly named same as the org — consider `hummbl-python` or `hummbl-cli`
- `aaa` is too cryptic — rename to `assured-agentic-architecture`

---

## 9. Summary Statistics

| Metric | Count |
|--------|-------|
| Total GitHub repos (hummbl-dev) | 55 |
| Total GitHub repos (hummbl-dev-org) | 1 |
| Total GitHub repos (trevin-creator) | 3 |
| **Total repos** | **59** |
| Public repos | 45 |
| Private repos | 14 |
| Published packages (npm + PyPI) | 4 |
| Total GitHub stars (all repos) | ~1,110 |
| Stars from autoresearch-mlx alone | 1,006 |
| Active repos (commits in last 7 days) | ~12 |
| Dormant repos (no commits 30+ days) | ~20 |
| Research reports generated | 40 |
| Local-only code directories | 2 (ai-stack, agent-bin) |
| Production domains | 1 (hummbl.io) |
| Forks maintained | 6 |

---

*Generated 2026-03-24 by automated audit. Review quarterly.*
