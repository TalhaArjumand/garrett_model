# IRL Ranking Proxy V1 Spec

## Purpose

This spec defines the first deterministic ranking proxy for `IRL` candidates.

It belongs to the research layer.

It does **not** claim to identify Garrett's true active `IRL`.

## Core Boundary

The ranker exists to answer:

- which currently detected `FVG` / `IRL` candidates deserve the most attention
  now under explicit research assumptions

It does **not** answer:

- which candidate is the true doctrinal `IRL`

## Inputs

The ranker uses:

- candle series
- `as_of_timestamp`
- `current_price`
- `direction_bias`

It generates candidates from the candle slice ending at `as_of_timestamp`.

This is a hard decision-time safety rule.

## Scored Features

V1 scores exactly four features:

1. `state`
   - resting candidates outrank reached candidates
2. `direction alignment`
   - candidates aligned with directional bias rank higher
3. `proximity`
   - candidates nearer to current price rank higher
4. `recency`
   - more recently confirmed candidates rank higher

## Descriptive But Unscored

V1 includes but does not score:

- `width`

Width is exposed for inspection and later research, but is not part of the v1
ranking formula.

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

- candidate generation is done from the candle slice ending at `as_of_timestamp`
- reached/resting state is only computed from that slice
- recency is measured relative to that same slice

## Exclusions From V1

V1 deliberately excludes:

- active `ERL` interaction
- dealing-range filtering
- manipulation-range influence
- higher-timeframe weighting
- time-of-day/session logic
- mitigation/fill doctrine
- candle-formation confluence
- inversion logic

## Implementation Status

Implementation status: implemented as research-layer code.
