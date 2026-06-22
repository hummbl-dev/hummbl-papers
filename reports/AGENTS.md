# AGENTS.md — autoresearch-reports

## Project
**autoresearch-reports** — Shared depot for the Autoresearch → distillation → proposal pipeline. Collected outputs and handoff reports from HUMMBL autoresearch pipeline runs. Shell + PowerShell helpers, Python tools, JSON queue. Generated artifacts plus operational configuration.

## Scope
- In scope: raw research reports (`reports/`), distilled findings (`findings/`), draft proposals (`proposals/`), applied change archive (`applied/`), research queue (`research_queue.json`), queue heartbeat (`QUEUE_HEARTBEAT.md`), operational shell/PowerShell helpers
- Out of scope: research execution itself (handled in `autoresearch-pipeline`), judging report/synthesis quality or adoption decisions (review decisions outside CI)

## Setup
No runtime install — artifacts depot with small operational scripts.

```bash
git clone https://github.com/hummbl-dev/autoresearch-reports.git
cd autoresearch-reports
```

Pipeline flow:
```
Windows Desktop (Autoresearch)  →  reports/
nodezero (qwen3.5:9b distill)   →  findings/
nodezero (synthesis + draft)    →  proposals/
MBP (human review + merge)      →  applied/
```

## Testing
CI is intentionally narrow and mechanical:
- Parse `research_queue.json`
- Syntax-check the root shell helper (`watchdog.sh`)
- Syntax-check the root PowerShell helpers (`health_check.ps1`, `high_cpu_procs.ps1`)

```bash
# Refresh queue heartbeat before overnight batch
python tools/update_queue_heartbeat.py

# Shell syntax check
bash -n watchdog.sh

# PowerShell syntax check
pwsh -NoProfile -Command "Invoke-ScriptAnalyzer health_check.ps1"
```

## Conventions
- Naming: Reports `reports/YYYY-MM-DD-domain-query-slug.md`; Findings `findings/YYYY-MM-DD-domain.json`; Proposals `proposals/YYYY-MM-DD-target-description.md`
- Shell + PowerShell helpers for cross-platform operations
- CI does NOT judge report quality, synthesis quality, or adoption — those are review decisions
- `QUEUE_HEARTBEAT.md` is generated — refresh before handoff
- Commit format: Conventional Commits
- Branch naming: type/agent/short-desc

## CI
GitHub Actions: `validate.yml`. Parses `research_queue.json`, syntax-checks shell and PowerShell helpers. Intentionally does not evaluate content quality.
