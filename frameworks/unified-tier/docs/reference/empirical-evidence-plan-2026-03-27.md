# Empirical Evidence Plan

Date: 2026-03-27
Status: draft

## Purpose

Move the HUMMBL Unified Tier Framework from:

- theory-backed
- heuristically operationalized

to:

- calibrated
- measured
- reproducible

## Core Validation Questions

1. Do human raters agree when using the manual wickedness rubric?
2. Does the MCP text classifier approximate the manual rubric well enough to be useful?
3. Does tier classification improve Base-N selection in practice?
4. Does the recommended Base-N level correlate with better outcomes than too-small or too-large selections?

## Study 1: Manual Rubric Reliability

### Goal

Measure inter-rater agreement on the canonical 5-question rubric.

### Design

- Create a gold set of 25 to 50 problem descriptions.
- Include clear examples across:
  - Tier 1
  - Tier 2
  - Tier 3
  - Tier 4
  - Tier 5
- Have at least 2 independent raters score each problem on all 5 dimensions.

### Metrics

- exact tier agreement
- adjacent-tier agreement
- per-dimension disagreement rates
- average score spread by problem

### Output

- reliability table
- rubric clarification list
- examples that consistently confuse raters

## Study 2: Classifier Calibration

### Goal

Measure how well `_classify_problem_text()` approximates manual scoring.

### Design

- Use the same gold set as Study 1.
- Compare classifier outputs against:
  - average manual score
  - consensus tier

### Metrics

- tier accuracy
- adjacent-tier accuracy
- mean absolute error on total score
- per-dimension alignment where proxy mapping exists

### Immediate Known Failure Cases

- organizational culture change
- climate change mitigation

These should be retained in the benchmark set.

## Study 3: Tier-to-Base Recommendation Fit

### Goal

Test whether the recommended Base-N range is practically useful.

### Design

- Run comparable tasks at:
  - recommended Base-N
  - one smaller Base-N
  - one larger Base-N
- Score:
  - task quality
  - path quality
  - cognitive overhead
  - user trust

### Metrics

- underfit rate
- overfit rate
- "just right" rate
- average outcome delta relative to recommended Base-N

## Study 4: Case-Based External Validity

### Goal

Ground the framework in real applied cases rather than only worked examples.

### Candidate cases

- HUMMBL framework self-development case
- operational planning cases
- debugging / architecture cases
- public policy or governance case studies

### Output

- annotated casebook
- scored case corpus
- lessons on where tiering is most and least predictive

## Evidence Artifacts To Create

- benchmark corpus of problem descriptions
- scoring worksheet with rater instructions
- calibration script for rubric vs classifier
- tier/Base outcome log
- versioned worked examples with evidence receipts

## Claim Discipline

After these studies, claims should be split into:

- theory-supported
- manually reliable
- classifier-supported
- outcome-supported

This is stricter and more defensible than a single undifferentiated label of "validated."
