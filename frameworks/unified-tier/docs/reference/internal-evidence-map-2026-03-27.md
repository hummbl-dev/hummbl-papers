# Internal Evidence Map

Date: 2026-03-27
Status: draft

## Purpose

Map the local artifacts that are most relevant to the Unified Tier Framework refresh.

## Highest-Confidence Internal Artifacts

### 1. Canonical Base120 corpus integrity

Best source:

- [consuming-base120.md](/Users/others/PROJECTS/base120/docs/consuming-base120.md)

Why it matters:

- strongest local evidence that the Base120 corpus itself is a real, sealed artifact with verifiable integrity anchors

### 2. Runtime framework implementation

Best source:

- [mcp_server.py](/Users/others/PROJECTS/HUMMBL-Unified-Tier-Framework/mcp_server.py)

Why it matters:

- shows the framework is operational, not just descriptive
- includes:
  - `classify_problem`
  - `tier_assessment`
  - `recommend_models`

### 3. Nearby production usage of Base120

Best source:

- [models.test.ts](/Users/others/PROJECTS/hummbl-production/api/tests/endpoints/models.test.ts)

Why it matters:

- confirms the model corpus is consumed in adjacent product code

## Medium-Confidence Artifacts

### 4. Framework documentation

Best sources:

- [README.md](/Users/others/PROJECTS/HUMMBL-Unified-Tier-Framework/README.md)
- [wickedness-scoring.md](/Users/others/PROJECTS/HUMMBL-Unified-Tier-Framework/docs/core/wickedness-scoring.md)
- [problem-complexity-tiers.md](/Users/others/PROJECTS/HUMMBL-Unified-Tier-Framework/docs/core/problem-complexity-tiers.md)

Why they matter:

- canonical public expression of the framework

Why confidence is only medium:

- some sections drift from code and nearby artifacts

### 5. Case-study narratives

Best source:

- [case-study-01-framework-development.md](/Users/others/PROJECTS/mcp-server/docs/case-study-01-framework-development.md)

Why it matters:

- gives practical claims about how the framework was used

Why confidence is only medium:

- references some evidence paths not present locally
- uses a different wickedness dimension set than the official framework docs

## Lowest-Confidence Claims Right Now

These claims are not yet well-supported by checked-in local evidence:

- reproducibility of the wickedness rubric
- calibration of the auto-classifier against manual assessment
- tier-to-Base-N mapping as empirically validated rather than heuristically designed
- some validation-process claims such as peer review and practical testing, because they are asserted but not fully evidenced on disk

## Refresh Priority

1. Keep Base120 artifact integrity claims.
2. Cleanly separate manual rubric, runtime heuristic, and Base-N recommendation logic.
3. Build measured evidence around the weakest claims instead of weakening the strongest artifacts with loose wording.
