# AGENTS.md — HUMMBL-Unified-Tier-Framework

## Project
**HUMMBL-Unified-Tier-Framework** — Problem complexity classification and learning progression framework with quantitative wickedness assessment methodology. Features 5 problem tiers (Simple → Super-Wicked), Base-N architecture (Base6 → BASE120), and empirical validation from HUMMBL mental models research. Python + Markdown, includes automated quality control and community templates.

## Scope
- In scope: the Unified Tier Framework specification (`HUMMBL_Unified_Tier_Framework_v1.0.md`), implementation protocols, decision trees, Base-N architecture docs, governance templates, `mcp_server.py`, empirical validation artifacts
- Out of scope: the Base120 mental models dataset itself (in `mcp-server`), production deployment infrastructure, commercial use (requires explicit licensing)

## Setup
Python 3.11+ for the MCP server; Markdown docs for the framework spec.

```bash
git clone https://github.com/hummbl-dev/HUMMBL-Unified-Tier-Framework.git
cd HUMMBL-Unified-Tier-Framework
python mcp_server.py --help
```

Key directories: `docs/` (framework documentation), `governance/` (governance templates), `hummbl-framework/` (framework implementation), `transformation-workflow/` (workflow docs), `github-repository-architect/`, `mcp-server-developer/`, `sitrep-coordinator/`.

## Testing
```bash
# MCP server smoke check
python mcp_server.py

# Markdown linting
markdownlint '**/*.md'

# Spell check and link checking run in CI
```

Framework validation is primarily documentation quality: markdown lint, spell check, and link integrity.

## Conventions
- Python 3.11+ for `mcp_server.py`; Markdown for all framework documentation
- Markdown linting configured via `.markdownlint.json`
- 5 tiers: Simple → Complicated → Complex → Wicked → Super-Wicked
- Base-N architecture: Base6 → BASE120 (aligned with HUMMBL mental models)
- Citation: see `CITATION.cff` for academic citation format
- Non-commercial use permitted; commercial use requires explicit licensing
- Commit format: Conventional Commits
- Branch naming: type/agent/short-desc

## CI
GitHub Actions: `ci.yml`, `markdown-lint.yml`, `spell-check.yml`, `link-checker.yml`. All badges linked in README. Runs on every push/PR.
