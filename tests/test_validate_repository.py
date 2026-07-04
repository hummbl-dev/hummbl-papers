#!/usr/bin/env python3
"""Tests for repository metadata validation helpers."""

from __future__ import annotations

import tempfile
from pathlib import Path
import importlib.util
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

_SPEC = importlib.util.spec_from_file_location(
    "validate_repository",
    str(REPO_ROOT / "tools" / "validate_repository.py"),
)
_VALIDATOR = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_VALIDATOR)
_validate_release_artifacts = _VALIDATOR._validate_release_artifacts


def test_release_artifacts_guard_allows_missing_dirs_without_crash() -> None:
    """Missing papers/notebooks directories should produce a clear failure list."""
    with tempfile.TemporaryDirectory() as root:
        repo_root = Path(root)
        failures = _validate_release_artifacts(repo_root=repo_root)

        assert "papers/: no paper artifact exists beyond README.md" in failures
        assert (
            "notebooks/: no notebook artifact exists beyond README.md" in failures
        )


def test_release_artifacts_gate_accepts_real_artifacts() -> None:
    """Release mode passes when each surface has at least one non-README file."""
    with tempfile.TemporaryDirectory() as root:
        repo_root = Path(root)
        papers = repo_root / "papers"
        notebooks = repo_root / "notebooks"
        papers.mkdir()
        notebooks.mkdir()
        (papers / "README.md").write_text("# papers placeholder")
        (notebooks / "README.md").write_text("# notebooks placeholder")
        (papers / "paper.md").write_text("# paper")
        (notebooks / "labbook.md").write_text("# labbook")

        failures = _validate_release_artifacts(repo_root=repo_root)
        assert failures == []


if __name__ == "__main__":
    test_release_artifacts_guard_allows_missing_dirs_without_crash()
    test_release_artifacts_gate_accepts_real_artifacts()
    print("PASS: papers validator guard behavior checks")
