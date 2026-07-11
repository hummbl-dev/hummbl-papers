#!/usr/bin/env python3
"""Publication Readiness Gate validator v0.1.

Validates gate decisions against the schema and enforces semantic rules:

- PREPRINT_READY or higher requires all gate dimensions to pass
- Self-review cannot satisfy independent review
- Anti-gaming checks must all pass for PREPRINT_READY or higher
- Disposition must be consistent with dimension outcomes
- Reviewer independence is mandatory

Uses only Python stdlib.
"""

import json
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "schema_version", "artifact_id", "artifact_class",
    "gate_dimensions", "disposition", "disposition_rationale",
    "anti_gaming_checks", "reviewer_independence", "evaluated_at"
]

VALID_DISPOSITIONS = {
    "BLOCK", "RESEARCH_NOTE_ONLY", "INTERNAL_REPORT_READY",
    "TECHNICAL_REPORT_READY", "PREPRINT_READY",
    "SUBMISSION_READY", "PUBLICATION_READY",
    "CORRECTION_REQUIRED", "SUPERSEDE", "RETRACT"
}

VALID_ARTIFACT_CLASSES = {
    "EXPLORATORY_NOTE", "INTERNAL_RESEARCH_MEMO",
    "DATED_TECHNICAL_REPORT", "REPRODUCIBILITY_PACKET",
    "PREPRINT_CANDIDATE", "VENUE_SUBMISSION_CANDIDATE",
    "SUBMITTED_MANUSCRIPT", "PEER_REVIEWED_PUBLICATION",
    "CORRECTION", "SUPERSESSION", "RETRACTION"
}

DISPOSITION_ORDER = [
    "BLOCK", "RESEARCH_NOTE_ONLY", "INTERNAL_REPORT_READY",
    "TECHNICAL_REPORT_READY", "PREPRINT_READY",
    "SUBMISSION_READY", "PUBLICATION_READY"
]

ANTI_GAMING_KEYS = [
    "prose_not_substitute_for_methods",
    "citation_volume_not_substitute_for_analysis",
    "self_review_not_independence",
    "tests_not_scientific_validation",
    "internal_benchmarks_not_generality",
    "synthetic_not_empirical",
    "no_hidden_exclusions",
    "arxiv_not_peer_review",
    "doi_not_quality_validation",
    "citations_independently_verified",
]


def _check_required(record: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"Missing required field: {field}")
    return errors


def _check_enums(record: dict) -> list[str]:
    errors = []
    if record.get("disposition") not in VALID_DISPOSITIONS:
        errors.append(f"Invalid disposition: {record.get('disposition')}")
    if record.get("artifact_class") not in VALID_ARTIFACT_CLASSES:
        errors.append(f"Invalid artifact_class: {record.get('artifact_class')}")
    return errors


def _check_reviewer_independence(record: dict) -> list[str]:
    errors = []
    ri = record.get("reviewer_independence", {})
    if not ri.get("reviewer_not_author"):
        errors.append("reviewer_independence.reviewer_not_author must be true")
    if not ri.get("reviewer_not_originating_agent"):
        errors.append("reviewer_independence.reviewer_not_originating_agent must be true")
    if ri.get("review_count", 0) < 1:
        errors.append("reviewer_independence.review_count must be >= 1")

    dim_review = record.get("gate_dimensions", {}).get("independent_review", {})
    if not dim_review.get("reviewer_not_author"):
        errors.append("gate_dimensions.independent_review.reviewer_not_author must be true")
    return errors


def _check_anti_gaming(record: dict) -> list[str]:
    errors = []
    checks = record.get("anti_gaming_checks", {})
    disposition = record.get("disposition", "")
    if disposition in DISPOSITION_ORDER:
        idx = DISPOSITION_ORDER.index(disposition)
    else:
        idx = -1

    for key in ANTI_GAMING_KEYS:
        val = checks.get(key)
        if val is None:
            errors.append(f"Missing anti_gaming_checks.{key}")
        elif not val and idx >= DISPOSITION_ORDER.index("PREPRINT_READY"):
            errors.append(
                f"anti_gaming_checks.{key} is false but disposition is {disposition} "
                f"(>= PREPRINT_READY)"
            )
    return errors


def _check_disposition_consistency(record: dict) -> list[str]:
    """Disposition must be consistent with dimension outcomes."""
    errors = []
    dims = record.get("gate_dimensions", {})
    disposition = record.get("disposition", "")

    if disposition in DISPOSITION_ORDER:
        idx = DISPOSITION_ORDER.index(disposition)
    else:
        return errors  # CORRECTION_REQUIRED, SUPERSEDE, RETRACT have different semantics

    # PREPRINT_READY or higher requires all critical dimensions
    if idx >= DISPOSITION_ORDER.index("PREPRINT_READY"):
        cn = dims.get("contribution_novelty", {})
        if not cn.get("prior_art_searched"):
            errors.append("disposition >= PREPRINT_READY but prior_art_searched is false")
        if not cn.get("adjacent_disciplines_searched"):
            errors.append("disposition >= PREPRINT_READY but adjacent_disciplines_searched is false")
        nc = cn.get("novelty_challenge", {})
        if not nc.get("completed"):
            errors.append("disposition >= PREPRINT_READY but novelty_challenge.completed is false")

        em = dims.get("evidence_methods", {})
        if not em.get("claim_evidence_map"):
            errors.append("disposition >= PREPRINT_READY but claim_evidence_map is false")
        if not em.get("methods_sufficient"):
            errors.append("disposition >= PREPRINT_READY but methods_sufficient is false")

        rep = dims.get("reproducibility", {})
        if not rep.get("environment_locked"):
            errors.append("disposition >= PREPRINT_READY but environment_locked is false")
        if not rep.get("versions_recorded"):
            errors.append("disposition >= PREPRINT_READY but versions_recorded is false")

        pc = dims.get("public_communication", {})
        if not pc.get("title_does_not_overstate"):
            errors.append("disposition >= PREPRINT_READY but title_does_not_overstate is false")
        if not pc.get("limitations_preserved"):
            errors.append("disposition >= PREPRINT_READY but limitations_preserved is false")

    # BLOCK should not have a positive disposition
    if disposition == "BLOCK":
        # BLOCK is valid — no consistency check needed
        pass

    return errors


def _check_self_review_anti_gaming(record: dict) -> list[str]:
    """Self-review represented as independence is explicitly rejected."""
    errors = []
    ri = record.get("reviewer_independence", {})
    dim_review = record.get("gate_dimensions", {}).get("independent_review", {})

    if ri.get("reviewer_not_author") and not dim_review.get("reviewer_not_author"):
        errors.append(
            "reviewer_independence says reviewer_not_author=true but "
            "gate_dimensions.independent_review.reviewer_not_author is false — contradiction"
        )
    return errors


def validate_record(record: dict) -> list[str]:
    errors = []
    errors.extend(_check_required(record))
    if errors:
        return errors
    errors.extend(_check_enums(record))
    errors.extend(_check_reviewer_independence(record))
    errors.extend(_check_anti_gaming(record))
    errors.extend(_check_disposition_consistency(record))
    errors.extend(_check_self_review_anti_gaming(record))
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate.py <record.json> [...]", file=sys.stderr)
        return 2
    all_valid = True
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        errors = validate_record(record)
        if errors:
            all_valid = False
            print(f"INVALID: {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"VALID: {path}")
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
