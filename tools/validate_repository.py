#!/usr/bin/env python3
"""Validate HUMMBL Papers repository metadata and documentation links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REMOTE_SCHEMES = ("http://", "https://", "mailto:")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _iter_files(suffix: str) -> list[Path]:
    return sorted(
        path
        for path in REPO_ROOT.rglob(f"*{suffix}")
        if ".git" not in path.parts
    )


def _validate_json() -> list[str]:
    failures: list[str] = []
    for path in _iter_files(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}")
    return failures


def _validate_citation() -> list[str]:
    path = REPO_ROOT / "CITATION.cff"
    if not path.exists():
        return ["CITATION.cff is missing"]

    text = path.read_text(encoding="utf-8")
    required_prefixes = (
        "cff-version:",
        "title:",
        "message:",
        "authors:",
        "license:",
    )
    failures: list[str] = []
    for prefix in required_prefixes:
        if not re.search(rf"(?m)^{re.escape(prefix)}", text):
            failures.append(f"CITATION.cff: missing {prefix}")
    if "orcid:" not in text:
        failures.append("CITATION.cff: missing author ORCID")
    return failures


def _validate_markdown_links() -> list[str]:
    failures: list[str] = []
    for path in _iter_files(".md"):
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or target.startswith(REMOTE_SCHEMES):
                continue
            if "{" in target or "}" in target:
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if Path(target).is_absolute():
                failures.append(f"{path.relative_to(REPO_ROOT)}: absolute local link {target!r}")
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(REPO_ROOT)
            except ValueError:
                failures.append(f"{path.relative_to(REPO_ROOT)}: link escapes repo {target!r}")
                continue
            if not resolved.exists():
                failures.append(f"{path.relative_to(REPO_ROOT)}: missing linked file {target!r}")
    return failures


def main() -> int:
    failures = [
        *_validate_json(),
        *_validate_citation(),
        *_validate_markdown_links(),
    ]
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    print("HUMMBL Papers repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
