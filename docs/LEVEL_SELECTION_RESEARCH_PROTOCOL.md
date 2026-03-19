# Level Selection Research Protocol

## Purpose

This protocol standardizes how `IRL` and `ERL` selector research is conducted
in this repo.

It exists because selector work is highly vulnerable to:

- doctrine contamination
- future leakage
- hidden heuristics
- unstable interpretation drift
- overfitting to a small reviewed sample

This is a process-control artifact, not doctrine.

## Scope

This protocol applies to all research that attempts to prioritize:

- `IRL` candidates
- `ERL` candidates

It applies whether the selector is:

- score-based
- rule-based
- heuristic
- later probabilistic or model-assisted

## Core Boundary

There is currently no source-locked Garrett selector for the most relevant:

- `IRL`
- `ERL`

So every selector in this repo is currently:

- research only
- not doctrine
- not Garrett's hidden true model

## Required Separation

Selector work must preserve three separate layers:

### Doctrine Layer

What Garrett explicitly teaches.

### Helper / Detection Layer

Mechanically detected objects such as:

- `FVG` candidates
- `ERL` candidates
- swing points
- liquidity states

### Selector Research Layer

A deterministic or explicitly defined research attempt to prioritize already
detected objects.

Selectors must never silently rewrite lower layers.

## Research Objective

A selector research artifact must answer only this kind of question:

- among currently detected candidates, which ones deserve more attention now
  under explicit assumptions

It must not claim:

- the true doctrinal active level
- final production readiness
- hidden Garrett intent

## Allowed Candidate Inputs

### IRL Selector Inputs

Allowed inputs:

- validated `FVGCandidate` objects
- their known state as of `as_of_timestamp`
- current price
- direction bias
- confirmation timestamps
- descriptive fields such as width

### ERL Selector Inputs

Allowed inputs:

- validated `ERLCandidate` objects
- their known state as of `as_of_timestamp`
- current price
- direction bias
- confirmation timestamps
- candidate kind / side / bounds

### Shared Input Rule

Selectors must only consume:

- already detected candidate objects
- current candle slice context
- explicitly declared research features

Selectors must not consume:

- undocumented discretionary interpretation
- future candles
- post-hoc labels disguised as runtime inputs

## Forbidden Claims

Selector research must not claim:

- "this is Garrett doctrine"
- "this is the true active IRL"
- "this is the true active ERL"
- "this is how Garrett must really select levels"

Allowed phrasing:

- `ranked candidate`
- `research default`
- `current proxy`
- `under explicit assumptions`

## Decision-Time Safety

This is non-negotiable.

Every selector must be decision-time safe.

That means:

- candidates must be generated from candles available at or before
  `as_of_timestamp`
- candidate state must be computed only from candles available at or before
  `as_of_timestamp`
- any contextual distribution or percentile must use only prior eligible
  candles
- right-side confirmation objects must be treated according to when they become
  knowable

If future information leaks in, the selector result is invalid.

## Deterministic Scoring Requirement

V1 selector research must be deterministic.

That means:

- explicit feature list
- explicit weights or priority order
- explicit tie-break rules
- explicit candidate filters

Hidden discretionary overrides are not allowed.

If the selector changes behavior, the cause must be traceable to:

- code changes
- input changes
- parameter changes

## Required Output Contract

Each selector result must be able to expose:

- candidate identity
- score
- rank
- reasons
- raw feature values
- decision-time safety assumptions

Optional later:

- confidence bucket
- research notes
- percentile context

## Manual Review Expectations

Selector research is not accepted on raw counts alone.

Each materially changed selector step should include:

### 1. Candidate Snapshot

Record:

- `as_of_timestamp`
- `current_price`
- direction bias
- candidate universe size

### 2. Top-Ranked Review

Manually inspect at least:

- top `1`
- top `3`
- any surprising opposite-direction result

### 3. Failure Review

If a clearly irrelevant candidate ranks too high:

- record it
- explain whether the issue is:
  - feature choice
  - weight choice
  - state logic
  - candidate-generation breadth

## Acceptance Criteria

A selector research step is useful only if it is:

- explicit
- deterministic
- leakage-safe
- auditable
- manually interpretable

### Useful Research Signal

This means:

- top candidates are structurally plausible
- ranking reasons are understandable
- changed rankings can be explained
- edge cases do not break the API
- repeated use on refreshed samples remains coherent

### Not Useful

This includes:

- unstable rankings with unexplained causes
- future leakage
- doctrine-like claims without source support
- scores without reasons
- heuristics that cannot be audited
- manual review repeatedly contradicting the ranker

## Edge-Case Requirements

These cases must be handled explicitly:

### Empty Candidate Set

- return empty result
- do not crash

### Single Candidate

- still return a ranked result
- do not special-case silently

### Mixed Symbols or Timeframes

- reject as invalid input

### Invalid Bounds

- reject inverted zones
- document zero-width point-candidate behavior explicitly

### State Ambiguity

- if state depends on future candles, the selector must not use it

### Window Rollover

- selector comparisons across refreshed windows must distinguish:
  - left-edge rollover
  - true state change
  - real new candidate arrival

## Change-Control Rules

When selector logic changes:

1. document the changed rule
2. rerun relevant tests
3. rerun the real-data report if selector output is sample-facing
4. manually inspect changed top candidates
5. record whether the change affects:
   - doctrine
   - helper detection
   - research ranking only

## Relationship To Existing Docs

This protocol governs how to work with:

- `LEVEL_SELECTION_RESEARCH_SPEC.md`
- `IRL_RANKING_PROXY_V1_SPEC.md`
- `ERL_RANKING_PROXY_V1_SPEC.md`

The spec defines the research content.
This protocol defines the research discipline.

## Current Repo Policy

Current selector policy in this repo is:

- deterministic first
- leakage-safe first
- manual review required
- doctrine quarantine always preserved
- refreshed real-data coherence matters more than one-off cleverness
