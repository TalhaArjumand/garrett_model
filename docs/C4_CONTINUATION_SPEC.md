# C4 Continuation Spec

## Purpose

This spec defines the next Garrett-specific doctrine layer after a qualifying
predecessor state that activates `EQ(C3)`: `C4 continuation`.

At this layer, `C4` is not treated as an independent pattern. It is evaluated
only after a reviewed predecessor path has already made `EQ(C3)` the active
boundary.

## Locked Predecessor Context

The following predecessor doctrine is already locked:

- Type A predecessor:
  - bullish / bearish `C2` closure
  - `C3` support relative to `EQ(C2)`
  - `C3` expansion confirmation beyond `C2`
- Type C predecessor:
  - no valid `C2` closure
  - strong `C3` closure over the body of `C2`
  - `EQ(C3)` becomes active only after `C3` closes

This means:

- `C4` is always downstream of an already-qualified predecessor state
- `EQ(C3)` is the active continuation boundary at this layer
- current code coverage is still narrower than full doctrine coverage

## Direct Transcript Evidence

Relevant transcript statement:

> "Once we have a strong candle 3 closure, mechanically defined as closing over
> the body of candle 2. This is where we can mark out equilibrium of candle 3's
> range seeking expansion or continuation in candle 4 where the low is formed
> in the upper half of candle 3's range."

Previously reviewed transcript statement:

> "So after candle 3 expands, seeking continuation in candle 4 is if we close
> candle 3 above candle 2's high. Once we have that closure, mark a equilibrium
> of the candle 3 expansion. This is where we seek a candle for continuation
> forming a low in the upper half of candle 3's range."

Together, these reviewed statements support:

- `C4` continuation is judged relative to `EQ(C3)`
- `C4` is sought only after the relevant predecessor closure / expansion event
  exists
- the active midpoint reference at this layer is `EQ(C3)`

## Inputs

This doctrine unit uses:

- `c1`
- `c2`
- `c3`
- `c4`

All inputs must be valid `Candle` objects.

## Bullish C4 Continuation Candidate

After a qualifying bullish predecessor has activated `EQ(C3)`:

- mark `EQ(C3) = (high(C3) + low(C3)) / 2`
- seek a `C4` that forms its low in the upper half of `C3` range

For the current doctrine candidate, that means:

- `low(C4) > EQ(C3)`

## Bearish Mirror

Under the locked generalized symmetry rule, the bearish mirror is also locked:

- after a qualifying bearish predecessor has activated `EQ(C3)`
- mark `EQ(C3)`
- seek `C4` with:
  - `high(C4) < EQ(C3)`

## What This Unit Is Measuring

`EQ(C3)` is not used merely as a midpoint marker.

At this layer, it functions as a mechanical wick-quality boundary for `C4`,
just as `EQ(C2)` functioned as a wick-quality boundary for `C3` in Type A.

The purpose is to distinguish:

- continuation / expansion-like behavior with controlled wick structure

from:

- deeper retracement or unstable behavior that does not preserve clean
  continuation

## Open Questions

The following remain unresolved and are not yet locked:

1. Is `C4` only a continuation candidate, or already a confirmed continuation?
2. Does `C4` require its own close-based expansion rule?
3. Are invalidation rules different between the Type A and Type C predecessor
   branches?
4. Is `C4` in Type C best treated as a continuation candle only, or also as a
   reviewed actionable candle?

## Implementation Status

Implementation status: partially implemented.

Current code implements:

- Type A-derived `C4` candidate primitives
- Type C-derived `C4` candidate primitives

Not implemented yet:

- a unified top-level `C4` detector across multiple predecessor branches

## Non-goals

This spec does not yet define:

- a final `C4` confirmation rule
- full continuation sequence doctrine beyond the current candidate
- aligned / reversal sequence doctrine
- higher-order context, driver, or SMT logic
