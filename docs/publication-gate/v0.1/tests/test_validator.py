#!/usr/bin/env python3
"""Tests for the Publication Readiness Gate validator."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import validate_record

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


class TestValidRecords(unittest.TestCase):
    def test_valid_internal_report_gate(self):
        errors = validate_record(load_fixture("valid-internal-report-gate.json"))
        self.assertEqual(errors, [], f"Expected no errors: {errors}")


class TestInvalidRecords(unittest.TestCase):
    def test_invalid_self_review(self):
        """Self-review with PREPRINT_READY disposition."""
        errors = validate_record(load_fixture("invalid-self-review.json"))
        self.assertTrue(len(errors) > 0, f"Expected errors: {errors}")
        self.assertTrue(any("reviewer_not_author" in e for e in errors),
                        f"Expected reviewer error: {errors}")
        self.assertTrue(any("reviewer_not_originating_agent" in e for e in errors),
                        f"Expected originating agent error: {errors}")

    def test_invalid_prose_overclaim(self):
        """Polished prose with weak methods claiming PREPRINT_READY."""
        errors = validate_record(load_fixture("invalid-prose-overclaim.json"))
        self.assertTrue(len(errors) > 0, f"Expected errors: {errors}")
        self.assertTrue(any("prior_art_searched" in e for e in errors),
                        f"Expected prior_art error: {errors}")
        self.assertTrue(any("methods_sufficient" in e for e in errors),
                        f"Expected methods error: {errors}")


class TestSemanticRules(unittest.TestCase):
    def _base_record(self) -> dict:
        return {
            "schema_version": "publication_readiness_gate.v0.1",
            "artifact_id": "test-001",
            "artifact_class": "EXPLORATORY_NOTE",
            "gate_dimensions": {
                "contribution_novelty": {
                    "research_question": "test",
                    "prior_art_searched": False,
                    "adjacent_disciplines_searched": False,
                    "narrow_contribution_claim": "test",
                    "non_novel_components": [],
                    "novelty_challenge": {
                        "completed": False,
                        "reviewer_not_author": False,
                        "findings": ""
                    }
                },
                "evidence_methods": {
                    "claim_evidence_map": False,
                    "methods_sufficient": False,
                    "negative_results_preserved": False
                },
                "reproducibility": {
                    "environment_locked": False,
                    "versions_recorded": False,
                    "commands_documented": False
                },
                "authorship_ai": {
                    "human_authors": ["Test"],
                    "corresponding_contact": "test@example.com",
                    "contribution_record": False,
                    "ai_disclosure": False,
                    "no_agent_as_author": True
                },
                "ethics_rights": {
                    "human_subjects_determination": True,
                    "sensitive_data_determination": True,
                    "license_verified": True
                },
                "independent_review": {
                    "reviewer_not_author": True,
                    "scope": ["methods"],
                    "unresolved_objections": []
                },
                "public_communication": {
                    "title_does_not_overstate": True,
                    "limitations_preserved": True,
                    "preprint_status_explicit": True
                }
            },
            "disposition": "BLOCK",
            "disposition_rationale": "test",
            "anti_gaming_checks": {
                "prose_not_substitute_for_methods": True,
                "citation_volume_not_substitute_for_analysis": True,
                "self_review_not_independence": True,
                "tests_not_scientific_validation": True,
                "internal_benchmarks_not_generality": True,
                "synthetic_not_empirical": True,
                "no_hidden_exclusions": True,
                "arxiv_not_peer_review": True,
                "doi_not_quality_validation": True,
                "citations_independently_verified": True
            },
            "reviewer_independence": {
                "reviewer_not_author": True,
                "reviewer_not_originating_agent": True,
                "review_count": 1
            },
            "evaluated_at": "2026-07-10T12:00:00Z",
            "evaluated_by": "test"
        }

    def test_block_disposition_passes_with_minimal_checks(self):
        r = self._base_record()
        errors = validate_record(r)
        self.assertEqual(errors, [], f"Expected no errors for BLOCK: {errors}")

    def test_preprint_ready_requires_all_dimensions(self):
        r = self._base_record()
        r["disposition"] = "PREPRINT_READY"
        errors = validate_record(r)
        self.assertTrue(any("prior_art_searched" in e for e in errors))
        self.assertTrue(any("methods_sufficient" in e for e in errors))
        self.assertTrue(any("environment_locked" in e for e in errors))

    def test_preprint_ready_requires_anti_gaming(self):
        r = self._base_record()
        r["disposition"] = "PREPRINT_READY"
        r["anti_gaming_checks"]["prose_not_substitute_for_methods"] = False
        errors = validate_record(r)
        self.assertTrue(any("prose_not_substitute_for_methods" in e for e in errors))

    def test_self_review_rejected(self):
        r = self._base_record()
        r["reviewer_independence"]["reviewer_not_author"] = False
        errors = validate_record(r)
        self.assertTrue(any("reviewer_not_author" in e for e in errors))

    def test_contradiction_between_review_fields(self):
        r = self._base_record()
        r["reviewer_independence"]["reviewer_not_author"] = True
        r["gate_dimensions"]["independent_review"]["reviewer_not_author"] = False
        errors = validate_record(r)
        self.assertTrue(any("contradiction" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
