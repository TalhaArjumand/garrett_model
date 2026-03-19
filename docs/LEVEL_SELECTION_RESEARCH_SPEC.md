# Level Selection Research Spec

## Purpose

This spec defines a research-layer approach for ranking:

- `IRL` candidates
- `ERL` candidates

It exists because the current Garrett-reviewed doctrine does **not** provide a
source-locked selector for the most relevant internal or external level when
multiple candidates exist.

## Core Boundary

There is currently no source-locked Garrett selector for the most relevant
`IRL` or `ERL` among multiple candidates.

Any mechanical ranking introduced here is a research hypothesis, not doctrine.

The ranking engine is not attempting to infer Garrett's hidden true selector.
It is only approximating relevance under explicit research assumptions.

## Layer Placement

This artifact belongs to:

- research layer

It does not belong to:

- doctrine layer
- helper geometry layer

It may use outputs from both of those lower layers.

## Current Inputs From Locked Layers

### Doctrine Inputs

Currently locked:

- `IRL = FVG`
- `ERL = swing high / swing low in buy-side / sell-side liquidity form`
- `IRL -> ERL`
- `ERL -> IRL`

### Helper / Research Inputs

Currently available helper or research concepts:

- baseline `FVG` geometry
- local swing points
- swing-derived liquidity
- old highs / old lows
- relatively equal highs / lows
- ERL mechanical proxy ideas

## Research Goal

For a given chart state and model direction:

1. generate plausible `IRL` candidates
2. generate plausible `ERL` candidates
3. compute explicit features for each candidate
4. score and rank those candidates
5. return both:
   - score
   - explanation

## IRL Candidate Ranking

### Candidate Generation

Potential `IRL` candidates may include:

- visible fair value gaps
- unmitigated fair value gaps
- recently formed fair value gaps
- fair value gaps inside the currently relevant range context

### Candidate Features

Candidate `IRL` features may include:

- freshness / mitigation state
- proximity to current price
- displacement quality of the creating move
- position inside current range context
- alignment with current universal-model direction
- overlap with key-level reaction behavior
- overlap with other future confluences

## ERL Candidate Ranking

### Candidate Generation

Potential `ERL` candidates may include:

- obvious swing highs / swing lows
- old highs / old lows
- relatively equal highs / lows
- range boundaries
- manipulation-range boundaries

### Candidate Features

Candidate `ERL` features may include:

- external swing obviousness
- old high / low vs relatively equal highs / lows
- untouched vs already taken status
- outside-of-range prominence
- nearest valid target in model direction
- manipulation-range relevance
- narrative alignment with the current model direction

## Output Contract

For each ranked candidate, the engine should return:

- `candidate_type`
- `direction`
- `price_level` or `zone`
- `score`
- `rank`
- `reasons`

Optional later:

- feature breakdown
- confidence bucket
- decision-time availability flag

## Decision-Time Boundary

The ranking engine must explicitly record whether a feature is:

- decision-time safe
  or
- only known after later confirmation

This matters because some helper constructs, such as confirmed local swing
points, are only known after right-side confirmation.

## Validation Standard

This engine should be validated as research, not doctrine.

That means it should be judged by:

- explicit assumptions
- consistency
- falsifiability
- usefulness on reviewed examples

It should not be described as:

- Garrett doctrine
- Garrett's hidden true model

## What Is Not Yet Locked

Not yet locked:

1. final candidate-generation rules
2. final feature list
3. final scoring weights
4. final dealing-range selection
5. whether different timeframes need different ranking logic
6. whether later doctrine reduces the need for ranking

## Implementation Status

Implementation status: partially implemented.

Current implementation status:

- `IRL` ranking proxy v1 is implemented as a research-layer ranker
- `ERL` ranking is still open

This implementation remains clearly separated from:

- doctrine detectors
- helper geometry primitives

## Non-goals

This spec does not yet define:

- final production ranking code
- machine-learned ranking
- backtesting logic
- trade execution logic
