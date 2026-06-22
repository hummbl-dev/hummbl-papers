#!/usr/bin/env python3
"""Generate QUEUE_HEARTBEAT.md from research_queue.json."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

QUEUE_PATH = Path("research_queue.json")
HEARTBEAT_PATH = Path("QUEUE_HEARTBEAT.md")


def main() -> int:
    data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    queue = data.get("queue", [])
    statuses = Counter(item.get("status", "unknown") for item in queue)
    pending = [item for item in queue if item.get("status") == "pending"]
    q2_pending = [item for item in pending if str(item.get("id", "")).startswith("RQ-2026Q2-")]

    lines = [
        "# Research Queue Heartbeat",
        "",
        f"Generated: {datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"Queue updated_at: {data.get('updated_at', 'unknown')}",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"| {status} | {count} |")

    lines.extend([
        "",
        "## Current Pending Queue",
        "",
        "| ID | Domain | Tier | Recurrence |",
        "|---|---|---:|---|",
    ])
    for item in pending:
        lines.append(
            f"| {item.get('id')} | {item.get('domain')} | "
            f"{item.get('tier')} | {item.get('recurrence')} |"
        )

    lines.extend([
        "",
        "## Freshness Signal",
        "",
        f"- Q2 2026 pending topics: {len(q2_pending)}",
        f"- Legacy pending topics: {len(pending) - len(q2_pending)}",
        "- If this file is older than the latest queue edit, run "
        "`python tools/update_queue_heartbeat.py` before the next overnight batch.",
        "",
    ])

    HEARTBEAT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {HEARTBEAT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
