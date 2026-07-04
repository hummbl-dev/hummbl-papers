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


def test_markdown_validation_ignores_legacy_trees() -> None:
    """Only the active papers surface should be link-checked."""
    old_repo_root = _VALIDATOR.REPO_ROOT
    old_markdown_roots = _VALIDATOR.MARKDOWN_ROOTS
    old_json_roots = _VALIDATOR.JSON_ROOTS

    with tempfile.TemporaryDirectory() as root:
        repo_root = Path(root)
        (repo_root / "README.md").write_text(
            "[papers](papers/README.md)\n", encoding="utf-8"
        )
        (repo_root / "papers").mkdir()
        (repo_root / "papers" / "README.md").write_text("# papers\n", encoding="utf-8")
        legacy = repo_root / "frameworks" / "unified-tier"
        legacy.mkdir(parents=True)
        (legacy / "CONTRIBUTING.md").write_text(
            "Broken [link](missing.md)\n", encoding="utf-8"
        )
        (repo_root / ".zenodo.json").write_text("{}", encoding="utf-8")

        try:
            _VALIDATOR.REPO_ROOT = repo_root
            _VALIDATOR.MARKDOWN_ROOTS = (
                repo_root / "README.md",
                repo_root / "ROADMAP.md",
                repo_root / "docs" / "method",
                repo_root / "papers",
                repo_root / "notebooks",
            )
            _VALIDATOR.JSON_ROOTS = (repo_root / ".zenodo.json",)

            failures = _VALIDATOR._validate_markdown_links()
            assert failures == []
        finally:
            _VALIDATOR.REPO_ROOT = old_repo_root
            _VALIDATOR.MARKDOWN_ROOTS = old_markdown_roots
            _VALIDATOR.JSON_ROOTS = old_json_roots


if __name__ == "__main__":
    test_release_artifacts_guard_allows_missing_dirs_without_crash()
    test_release_artifacts_gate_accepts_real_artifacts()
    test_markdown_validation_ignores_legacy_trees()
    print("PASS: papers validator guard behavior checks")
