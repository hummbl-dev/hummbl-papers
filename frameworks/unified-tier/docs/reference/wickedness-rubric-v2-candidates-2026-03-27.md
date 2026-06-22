# Wickedness Rubric v2 Candidates

Date: 2026-03-27
Status: draft

## Purpose

Capture the most defensible refresh directions for the HUMMBL wickedness rubric based on:

- current local framework artifacts
- local code and classifier behavior
- recent external literature from 2024-2026

## Why Refresh

The current framework still has a solid conceptual backbone, but the evidence gathered in this review suggests:

- the public rubric and runtime classifier drift from each other
- the current five dimensions compress too many distinct concerns
- recent literature repeatedly points to interdependence and governance capacity as missing first-class variables

## What The Literature Adds

Recent external sources consistently support keeping wickedness grounded in:

- contestation
- uncertainty
- emergence
- urgency

But they also push harder on:

- interdependence and system coupling
- governance, authority, and implementation capacity
- separating problem structure from response-system readiness

Particularly useful sources:

- Cechvala (2024), *Business Horizons*: systems mapping, participatory inquiry, causal loops
- Wiarda et al. (2024), *EIST*: complexity, uncertainty, contestation, and governance responsibilities
- Sydelko, Espinosa, Midgley (2024), *EJOR*: interagency coordination and viable-system framing
- McHugh et al. (2024), *npj Climate Action*: divergence over solutions despite agreement on the problem
- Chudnovsky & Fernandez (2024), *npj Climate Action*: state and organizational capacity
- Nachtigall et al. (2024), *Environmental and Resource Economics*: profile-style measurement rather than one collapsed latent score
- OECD (2025): mission governance through structure, coordination, execution, and resources
- Dettwiler et al. (2026): reflexive, relational, and power-aware capacity at the science-policy interface

## Candidate Refresh Paths

## Option A: Refined 5-Dimension Rubric

Keep the five-question format, but tighten the dimensions.

Possible dimensions:

1. stakeholder and solution contestation
2. uncertainty and information incompleteness
3. interdependence and system coupling
4. learning while acting and emergent response behavior
5. urgency, irreversibility, and governance weakness

Pros:

- preserves the simplicity of the current framework
- easiest migration path for existing docs and tools

Cons:

- still compresses multiple constructs into single dimensions

## Option B: 7-Dimension Structural Rubric

Separate the major concerns more explicitly.

Candidate dimensions:

1. problem-definition contestation
2. solution contestation
3. uncertainty / information incompleteness
4. interdependence / system coupling
5. emergence / learning during intervention
6. urgency / irreversibility
7. governance / authority / implementation capacity

Pros:

- best alignment with the refresh literature
- cleaner separation of different failure modes

Cons:

- breaks compatibility with the current 0-30 framing
- requires new calibration work

## Option C: Dual-Layer Framework

Keep a wickedness score for the problem itself, and add a second layer for response-system readiness.

Layer 1: problem structure

- contestation
- uncertainty
- interdependence
- emergence
- urgency / irreversibility

Layer 2: response system

- governance / authority
- implementation capacity
- coordination capability
- representation quality

Pros:

- best conceptual separation
- matches the strongest external measurement signal
- likely most useful for HUMMBL in practice

Cons:

- more complex to explain
- requires explicit decision rules for combining or comparing layers

## Recommended Direction

Current best candidate: `Option C`

Reason:

- the strongest external signal is that problem wickedness and response feasibility are not the same thing
- the current local framework already strains under trying to make one scalar score do too much
- this separation also fits local exploratory work around BaseN, Meta-Model Selection, and composition posture

## Transitional Approach

If a full dual-layer redesign is too disruptive now:

1. keep the current five-question manual rubric as the canonical v1 method
2. explicitly mark it as `v1`
3. start calibrating a `v2` design in parallel
4. add an auxiliary governance/capacity screen immediately, even before the full v2 redesign lands

## Immediate v2 Candidate Questions

### Problem Layer

1. How contested is the problem definition?
2. How contested are the candidate solutions?
3. How incomplete or uncertain is the information base?
4. How tightly coupled and interdependent is the system?
5. How much must we learn while intervening?
6. How urgent and irreversible are the stakes?

### Response Layer

7. How weak or fragmented is governance authority?
8. How strong is implementation capacity?
9. How difficult is cross-actor coordination?

## Implication For The MCP Classifier

The classifier should not be presented as if it implements the canonical rubric unless:

- its dimensions are aligned to the public method
- it is calibrated against a gold set
- its limitations are explicitly documented

Until then, it should be labeled as:

- heuristic
- proxy-based
- draft

## Open Decision

The next design choice is not only which dimensions to keep.

It is whether HUMMBL wants:

- a simple one-score teaching tool
- a more diagnostic research-grade profile
- or both, with different interfaces for different use cases
