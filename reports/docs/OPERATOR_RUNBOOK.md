# Autoresearch Operator Runbook
## Weekly Workflow: Queue → Pipeline → Reports

### Overview
This runbook describes the standard operating procedure for running the HUMMBL autoresearch pipeline on a weekly cadence. It assumes the pipeline is already unblocked (Phase 1) and hardened (Phase 2).

### Prerequisites
- Python 3.11+
- `pytest` installed
- Access to target machine (Anvil for GPU, nodezero for MPS, or local for CPU)
- `NEMOCLAW_TARGET_REPO` and `NEMOCLAW_REPO_NAME` env vars set (if not using defaults)

### Weekly Schedule

| Day | Task | Time | Owner |
|-----|------|------|-------|
| Monday | Review queue, select topic | 15 min | Operator |
| Tuesday-Wednesday | Run pipeline (supervisor + worker) | 2-4h | Pipeline |
| Thursday | Distill raw output into finding | 1h | Operator or agent |
| Friday | Draft proposal (if finding is actionable) | 1h | Operator or agent |
| Friday EOD | Update queue status, commit artifacts | 30 min | Operator |

### Step-by-Step Procedure

#### Step 1: Select Topic (Monday)

1. Open `research_queue.json`
2. Filter for `status: "pending"` items
3. Prioritize by:
   - Tier (1 = highest, 3 = lowest)
   - Recurrence (monthly items should not slip more than 2 weeks)
   - Operator interest / current business need
4. Update selected item:
   ```json
   "status": "in_progress",
   "last_run": "2026-06-20"
   ```
5. Commit the queue update

#### Step 2: Run Pipeline (Tuesday-Wednesday)

On the target machine:

```bash
# 1. Clone or pull latest pipeline
cd ~/autoresearch-pipeline && git pull origin main

# 2. Run healthcheck
python healthcheck.py --pipeline-dir . --repo-dir ~/my-experiment-repo

# 3. Generate experiment
python supervisor/supervisor.py --once --pipeline-dir . --repo-dir ~/my-experiment-repo

# 4. Run worker (single poll)
python worker/worker.py --once --pipeline-root . --repo-dir ~/my-experiment-repo

# 5. Check results
ls runs/
cat runs/<run_id>/state.json
```

For a full loop (supervisor generates, worker executes, supervisor evaluates):

```bash
# Terminal 1: Supervisor loop
python supervisor/supervisor.py --loop --interval 30 --pipeline-dir . --repo-dir ~/my-experiment-repo

# Terminal 2: Worker loop
python worker/worker.py --loop --pipeline-root . --repo-dir ~/my-experiment-repo

# Let run for 2-4 hours, then Ctrl+C both
```

#### Step 3: Distill Finding (Thursday)

1. Read the raw experiment output from `runs/<run_id>/`
2. Extract: key claim, evidence, confidence, gaps, recommendation
3. Write a finding document in `findings/F-XXX-<topic>.md`
4. Use the template from `findings/F-001-ai-governance-q3-2026.md`

#### Step 4: Draft Proposal (Friday, if applicable)

If the finding suggests a concrete change:
1. Draft a proposal in `proposals/P-XXX-<topic>.md`
2. Include: problem, proposed change, expected impact, risk, implementation plan, acceptance criteria
3. Use the template from `proposals/P-001-secure-mcp-profile.md`

#### Step 5: Commit Artifacts (Friday EOD)

```bash
cd ~/autoresearch-reports

# Update queue status
# Edit research_queue.json: status -> "completed" for finished topics

# Add new artifacts
git add findings/ proposals/ research_queue.json

# Commit
git commit -m "research(YYYY-MM-DD): <topic> findings + proposal

- Finding: <one-line summary>
- Proposal: <one-line summary> (if applicable)
- Queue: <topic> marked completed

Generated via autoresearch pipeline"

# Push
git push origin main
```

### Environment Variables

| Variable | Default | When to Set |
|----------|---------|-------------|
| `NEMOCLAW_TARGET_REPO` | `~/autoresearch-pipeline` | When targeting a different experiment repo |
| `NEMOCLAW_REPO_NAME` | `autoresearch-pipeline` | When experiment repo has a different name |
| `NEMOCLAW_SEED` | (none) | When reproducible experiment sequences are needed |

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `healthcheck.py` fails with "repo not found" | `NEMOCLAW_TARGET_REPO` not set or wrong | Set env var or pass `--repo-dir` |
| Supervisor generates no experiments | `results.tsv` missing or empty | Create initial results.tsv with baseline val_bpb |
| Worker crashes on startup | `signal.signal` fails on Windows | Set `NEMOCLAW_SIGNAL_DISABLE=1` (or use Phase 2+ code) |
| Tests fail with import errors | Running tests from wrong directory | `cd ~/autoresearch-pipeline && python -m pytest tests/` |
| Queue JSON invalid after edit | Syntax error in manual edit | Validate with `python -m json.tool research_queue.json` |

### Automation Options

1. **Cron / launchd**: Schedule `supervisor.py --loop` and `worker.py --loop` to run continuously
2. **GitHub Actions**: Trigger pipeline on push to `experiment` branch (requires self-hosted runner for GPU)
3. **Manual trigger**: Use `workflow_dispatch` in `.github/workflows/publish.yml` for one-off runs

### Escalation

- Pipeline bugs: File issue in `hummbl-dev/autoresearch-pipeline`
- Queue content questions: Ask operator (Reuben Bowlby)
- Proposals requiring engineering: Route to `founder-mode` backlog
- Security findings: Route to `hummbl-dev/hummbl-governance`

### Checklist (use before each run)

- [ ] Queue item selected and marked `in_progress`
- [ ] Target machine has available GPU/CPU resources
- [ ] `healthcheck.py` passes
- [ ] `pytest` passes (if code was modified)
- [ ] `NEMOCLAW_TARGET_REPO` set correctly (if needed)
- [ ] Disk space > 10 GB free
- [ ] Operator available for mid-run questions

---

*Version: 1.0 | Date: 2026-06-20 | Phase: 3 (Activation)*
