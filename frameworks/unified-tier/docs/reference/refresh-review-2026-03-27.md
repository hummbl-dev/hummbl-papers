# Unified Tier Framework Refresh Review

Date: 2026-03-27
Status: draft

## Question

What parts of the HUMMBL Unified Tier Framework and wickedness scoring should be refreshed now, and what evidence currently supports or weakens the framework?

## Findings

### 1. The public wickedness rubric and the runtime classifier are not the same system

Severity: high

Published docs describe a 5-question rubric based on:

- stakeholder agreement
- information completeness
- solution finality
- learning dynamics
- time pressure

See:

- [wickedness-scoring.md](../core/wickedness-scoring.md)
- [problem-complexity-tiers.md](../core/problem-complexity-tiers.md)

But the MCP classifier in [mcp_server.py](/Users/others/PROJECTS/HUMMBL-Unified-Tier-Framework/mcp_server.py) uses a different dimension set:

- stakeholder diversity
- solution reversibility
- problem definition clarity
- temporal dynamics
- interconnectedness

This is not a wording tweak. It is a material change in the scoring model.

Implication:

- claims of reproducible quantitative wickedness scoring are currently overstated unless the framework explicitly distinguishes:
  - manual rubric
  - heuristic text classifier

### 2. The automatic classifier does not reproduce the framework’s own worked examples

Severity: high

Using the current `_classify_problem_text()` implementation on text versions of the public examples produced:

| Example | Doc tier | Classifier tier | Score |
| --- | --- | --- | --- |
| flat tire | 1 | 1 | 8 |
| CRM implementation | 2 | 2 | 10 |
| organizational culture change | 4 | 2 | 12 |
| climate change mitigation | 5 | 3 | 18 |

This matters because the two most important examples for wicked and super-wicked behavior are currently under-classified by the runtime heuristic.

Implication:

- the heuristic classifier is currently too weak to stand in for the published framework
- public docs should not imply that the text classifier faithfully reproduces the official rubric without calibration evidence

### 3. Internal empirical evidence is thinner than the current documentation suggests

Severity: medium-high

[validation-evidence.md](validation-evidence.md) says:

- expert evaluation
- peer review
- practical testing
- documentation review

But it does not currently provide:

- rater counts
- assessment protocol
- sample sizes for the tier framework itself
- inter-rater agreement
- calibration of rubric vs classifier
- observed predictive value of tier-to-Base mapping

The strongest empirical evidence currently appears to be:

- Base120 model validation claims
- local case-study narratives
- runtime classifier behavior

The weakest empirical claims are:

- reproducibility of wickedness scoring
- tier-to-Base-N mapping
- claim that the 5-question method is already quantitatively validated beyond worked examples

### 4. The framework should separate normative theory from operational heuristics

Severity: medium

Right now, several distinct things are blended together:

- foundational theory of wicked and super-wicked problems
- HUMMBL’s manual scoring rubric
- Base-N selection recommendations
- MCP text classification heuristics

These should be separated so the user understands what is:

- theory-backed
- HUMMBL-designed
- heuristic
- empirically tested
- still hypothetical

### 5. Adjacent local artifacts show taxonomy and metadata drift beyond the wickedness rubric itself

Severity: medium

Additional inconsistencies found in nearby local artifacts:

- Base120 validation metadata drifts across repos:
  - framework docs say October 31, 2025 and 9.1/10
  - nearby production or MCP artifacts use October 16, 2025 and 9.2/10
- priority taxonomy drifts:
  - one framework section references 7 priority levels
  - nearby production tests appear to allow only priority levels 1-5
- transformation taxonomy drifts:
  - one framework section uses a different transformation naming set than the validation page and nearby code artifacts

Implication:

- the framework needs a stronger canonical-source rule
- otherwise users cannot tell which structure is normative versus historical or implementation-specific

### 6. The latest literature supports refreshing the dimensions around uncertainty, contestation, urgency, governance, and evaluation

Severity: medium

Recent work strengthens the importance of:

- imperfect knowledge under urgency
- evaluation methods that avoid both paralysis and overclaiming
- governance capability and authority structure
- practice-level and street-level implementation

Useful external anchors:

- Rittel & Webber (1973): foundational wicked-problem characteristics
- Levin et al. (2012): super-wicked structure
- O’Connor & Douguet (2024), *Futures*: high stakes, urgency, imperfect knowledge, multi-actor deliberation
  <https://doi.org/10.1016/j.futures.2024.103436>
- Termeer et al. small-wins evaluation framework: wicked-problem evaluation should avoid paralysis and overestimation; standard target-based evaluation is often misleading
  [PDF](https://openresearch.amsterdam/image/2023/11/22/a_small_wins_framework_to_overcome_the_evaluation_paradox_of_governing_wicked_pr.pdf)
- Howlett et al. on pandemics as super-wicked problems: urgency plus weak authority and reflexive institutional adaptation
  <https://link.springer.com/article/10.1007/s11077-021-09442-2>
- Gale et al. (2025), *Social Science & Medicine*: AMR as a wicked problem handled through deliberative practice, trust, and street-level diplomacy
  <https://doi.org/10.1016/j.socscimed.2025.118629>

## Evidence

### Local primary evidence

- Public rubric: [wickedness-scoring.md](../core/wickedness-scoring.md)
- Public tier definitions: [problem-complexity-tiers.md](../core/problem-complexity-tiers.md)
- Validation claims: [validation-evidence.md](validation-evidence.md)
- Runtime heuristic classifier: [mcp_server.py](/Users/others/PROJECTS/HUMMBL-Unified-Tier-Framework/mcp_server.py)
- Internal case study claiming quantitative wickedness scoring and Base42 fit for wicked problems: [case-study-01-framework-development.md](/Users/others/PROJECTS/mcp-server/docs/case-study-01-framework-development.md)
- Canonical Base120 integrity reference: [consuming-base120.md](/Users/others/PROJECTS/base120/docs/consuming-base120.md)

### Empirical evidence gathered in this review

I executed the current `_classify_problem_text()` function locally against text approximations of the framework’s own worked examples. Two low-tier examples matched. Two high-tier examples did not.

Observed mismatches:

- organizational culture change: documented as Tier 4, classified as Tier 2
- climate change mitigation: documented as Tier 5, classified as Tier 3

## Inference

The framework is still viable, but it needs a cleaner evidence hierarchy.

The strongest refresh path is:

1. keep the underlying wicked and super-wicked framing
2. explicitly separate the manual rubric from the keyword classifier
3. refresh the dimension story so it better reflects:
   - contestation
   - uncertainty
   - interdependence
   - temporality
   - reversibility or path dependence
   - governance or authority weakness
4. downgrade claims that imply current empirical validation where only heuristic evidence exists
5. establish a canonical source of truth for:
   - transformation taxonomy
   - priority taxonomy
   - Base120 validation metadata
6. gather a real gold set for calibration

## Recommended Changes

### Immediate doc changes

- mark the current text classifier as heuristic
- state clearly that the published 5-question rubric is the canonical assessment method
- add a note that the automated classifier uses proxy dimensions and is not yet calibrated to the manual rubric
- revise validation pages to separate:
  - Base120 content validation
  - tier framework theory basis
  - rubric validation status
  - classifier validation status

### Near-term empirical work

- build a gold dataset of 25 to 50 problems manually scored by at least 2 raters
- measure agreement between:
  - rater A vs rater B
  - manual rubric vs MCP classifier
- record tier-to-Base recommendation outcomes on real cases
- collect outcome notes on whether chosen Base-N level felt:
  - insufficient
  - appropriate
  - excessive

### Dimensional refresh candidates

The current framework likely needs a clearer position on whether the 5 dimensions are:

- stakeholder contestation
- uncertainty / knowledge incompleteness
- solution finality / reversibility / path dependence
- learning while acting / adaptive pressure
- urgency / governance / authority weakness

At minimum, the public docs and the classifier should stop drifting across different dimension sets.

## Uncertainty

- I have not yet completed a larger-scale calibration study.
- The classifier test used text approximations of the public worked examples, not an official benchmark corpus.
- Some empirical evidence may exist in older private validation artifacts not inspected in this pass.

## Confidence

High on the existence of the code/doc mismatch.
High on the mismatch between the classifier and the published high-tier examples.
Medium on the exact dimensional refresh that will best fit HUMMBL long term.
