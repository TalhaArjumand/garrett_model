# IRL Mechanical Proxy Spec

## Purpose

This spec defines a **research/helper-layer mechanical proxy** for `IRL`
(`Internal Range Liquidity`) state tracking.

It does **not** change locked doctrine that:

- `IRL = FVG`
- baseline `FVG` geometry is a three-candle imbalance

Its purpose is narrower:

- extract all baseline `FVG` candidates from a candle series
- track whether each candidate is still resting
- track whether price has already reached that gap

## Doctrine Boundary

Current locked doctrine does **not** define a final Garrett rule for:

- mitigation
- fill
- ranking among multiple `FVG` / `IRL` candidates

So this spec must remain:

- research/helper layer
- separate from doctrine

## Candidate Object

At the current project stage, an `IRL` candidate is simply a baseline `FVG`
object with later state tracking.

That means:

- bullish candidate:
  - `low(c3) > high(c1)`
- bearish candidate:
  - `high(c3) < low(c1)`

The doctrinal geometry remains unchanged.

## State Model

### Resting

An `IRL` / `FVG` candidate is `resting` if no later candle range overlaps the
gap zone.

### Reached

An `IRL` / `FVG` candidate is `reached` if a later candle range overlaps the
gap zone.

This is a weaker and safer state model than claiming:

- mitigated
- fully filled
- fully rebalanced

because those stronger terms are not yet locked by doctrine.

## Reach Rule

A later candle reaches the `FVG` if its range overlaps the gap zone.

For zone bounds:

- `zone_low`
- `zone_high`

and later candle:

- `candle_low`
- `candle_high`

the current helper rule is:

- reached if `candle_high >= zone_low` and `candle_low <= zone_high`

This is inclusive on the boundaries because touching the gap counts as reaching
the key level.

## Important Edge Case

If a later candle moves beyond the gap zone **without overlapping it**, the
helper layer should **not** infer that the gap was reached.

This protects the system from overclaiming with candle-only data in cases where
price may have skipped past the zone.

## What Is Locked In This Helper Spec

Locked in this helper/research spec:

- `IRL` candidate extraction can reuse baseline `FVG` detection
- each candidate may be classified as:
  - `resting`
  - `reached`
- reached/resting is a helper state model, not doctrine

## What Is Not Yet Locked

Not yet locked:

1. Garrett-specific mitigation doctrine
2. Garrett-specific fill doctrine
3. active `IRL` selection among multiple `FVG`s
4. ranking weights for `IRL` relevance

## Implementation Status

Implementation status: partially implemented.

Current implementation includes:

- baseline `FVG` candidate extraction across a candle series
- explicit `resting` vs `reached` state tracking
- real-data reporting for those states

## Non-goals

This spec does not yet define:

- the true active `IRL`
- final `IRL` ranking
- doctrine-level mitigation language
- entry or target rules by itself
