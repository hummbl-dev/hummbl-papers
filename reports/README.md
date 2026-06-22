# Autoresearch Reports

Shared depot for the Autoresearch → distillation → proposal pipeline.

Learn more at [hummbl.io](https://hummbl.io).

[![License](https://img.shields.io/github/license/hummbl-dev/autoresearch-reports)](https://github.com/hummbl-dev/autoresearch-reports/blob/main/LICENSE)

## Pipeline

```
Windows Desktop (Autoresearch)  →  reports/
nodezero (qwen3.5:9b distill)  →  findings/
nodezero (synthesis + draft)    →  proposals/
MBP (human review + merge)      →  applied/
```

## Directory Structure

- `reports/` — Raw Autoresearch markdown output (pushed from Windows Desktop)
- `findings/` — Distilled structured JSON (generated on nodezero)
- `proposals/` — Draft improvement proposals (generated on nodezero)
- `applied/` — Archive of accepted changes (moved after merge)
- `research_queue.json` — Topic queue with recurrence schedules
- `QUEUE_HEARTBEAT.md` — Generated queue freshness snapshot for overnight runs

## Automation Posture

This repository carries generated research artifacts plus a small amount of
operational configuration. CI should stay narrow and mechanical:

- Parse `research_queue.json`.
- Syntax-check the root shell helper.
- Syntax-check the root PowerShell helpers.

The validation workflow intentionally does not judge report quality, synthesis
quality, or whether generated findings should be adopted. Those remain review
decisions outside CI.

## Naming Convention

- Reports: `reports/YYYY-MM-DD-domain-query-slug.md`
- Findings: `findings/YYYY-MM-DD-domain.json`
- Proposals: `proposals/YYYY-MM-DD-target-description.md`

## Queue Heartbeat

Refresh the queue heartbeat before starting or handing off an overnight batch:

```bash
python tools/update_queue_heartbeat.py
```
