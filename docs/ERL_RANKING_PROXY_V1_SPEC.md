# ERL Ranking Proxy V1 Spec

## Purpose

This spec defines the first deterministic ranking proxy for `ERL` candidates.

It belongs to the research layer.

It does **not** claim to identify Garrett's true active `ERL`.

## Core Boundary

The ranker exists to answer:

- which currently detected `ERL` candidates deserve the most attention now under
  explicit research assumptions

It does **not** answer:

- which candidate is the true doctrinal `ERL`

## Inputs

The ranker uses:

- candle series
- `as_of_timestamp`
- `current_price`
- `direction_bias`
- optional `equal_tolerance`

It generates candidates from the candle slice ending at `as_of_timestamp`.

This is a hard decision-time safety rule.

## Candidate Shapes

`ERL` candidates may be:

- point-like
  - old highs
  - old lows
- zone-like
  - equal highs
  - equal lows

V1 must therefore allow zero-width point candidates while still rejecting
inverted bounds.

## Scored Features

V1 scores exactly four features:

1. `state`
   - resting candidates outrank taken candidates
2. `direction alignment`
   - sell-side candidates align with bullish bias
   - buy-side candidates align with bearish bias

This is because `ERL` is treated here as the reaction location in the
`ERL -> IRL` model:

- bullish reaction bias watches `old_low` / sell-side liquidity
- bearish reaction bias watches `old_high` / buy-side liquidity
3. `proximity`
   - candidates nearer to current price rank higher
4. `recency`
   - more recently confirmed candidates rank higher

## Descriptive But Unscored

V1 includes but does not score:

- `width`
- `candidate_kind`
- `candidate_side`

These are exposed for inspection and later research, but are not part of the
v1 ranking formula.

## Default Weights

Research default weights:

- `state = 0.35`
- `direction = 0.25`
- `proximity = 0.25`
- `recency = 0.15`

These are explicit research defaults, not doctrine.

## Output Contract

For each ranked candidate, the engine returns:

- candidate
- score
- rank
- reasons
- feature values

## Decision-Time Safety

This is non-negotiable.

The ranker must not use future candles beyond `as_of_timestamp`.

So:

- candidate generation is done from the candle slice ending at
  `as_of_timestamp`
- resting/taken state is only computed from that slice
- recency is measured relative to that same slice

## Exclusions From V1

V1 deliberately excludes:

- active `IRL` interaction
- dealing-range filtering
- manipulation-range influence
- higher-timeframe weighting
- time-of-day/session logic
- key-level confluence weighting
- swing-obviousness scoring
- equal-high/equal-low priority scoring beyond raw candidate generation

## Implementation Status

Implementation status: implemented as research-layer code.
