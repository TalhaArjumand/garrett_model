# C4 Continuation Spec

## Purpose

This spec defines the next Garrett-specific doctrine layer after a valid
`C1 -> C2 -> C3` sequence: `C4 continuation`.

At this layer, `C4` is not treated as an independent pattern. It is evaluated
only after `C3` has already qualified as a valid expansion candle.

## Locked Predecessor Context

The following predecessor doctrine is already locked:

- bullish `C2` closure back inside `C1` range
- bullish `C3` support relative to `EQ(C2)`
- bullish `C3` expansion confirmation:
  - `close(C3) > high(C2)`
- bearish mirror for the above

This means:

- `C2` is the reversal / swing-formation-side event
- `C3` is the candidate expansion candle
- `EQ(C2)` is the wick-quality boundary used to qualify `C3`

## Direct Transcript Evidence

Relevant transcript statement:

> "So after candle 3 expands, seeking continuation in candle 4 is if we close
> candle 3 above candle 2's high. Once we have that closure, mark a equilibrium
> of the candle 3 expansion. This is where we seek a candle for continuation
> forming a low in the upper half of candle 3's range."

This directly supports:

- `C4` continuation is evaluated only after valid `C3` expansion
- the active midpoint reference shifts from `EQ(C2)` to `EQ(C3)`
- bullish continuation is judged by whether `C4` forms its low in the upper
  half of `C3`

Additional doctrine clarification:

- Garrett states a generalized symmetry rule, so conditions that are locked for
  bullish continuation can be mirrored into bearish continuation unless a later
  doctrine unit explicitly overrides them

## Inputs

This doctrine unit uses:

- `c1`
- `c2`
- `c3`
- `c4`

All inputs must be valid `Candle` objects.

## Preconditions

Before evaluating `C4`, all of the following must already be true:

1. `c1`, `c2`, `c3`, and `c4` are valid `Candle` objects.
2. All four candles are closed.
3. All four candles have the same symbol.
4. All four candles have the same timeframe.
5. The candles are in strict timestamp order.
6. Each candle is consecutive for the timeframe.
7. `c1 -> c2 -> c3` already forms a valid predecessor sequence.

## Bullish C4 Continuation Candidate

After a valid bullish `C3` expansion has been confirmed:

- mark `EQ(C3) = (high(C3) + low(C3)) / 2`
- seek a `C4` that forms its low in the upper half of `C3` range

For the current doctrine candidate, that means:

- `low(C4) > EQ(C3)`

This is a strong doctrinal candidate supported by the transcript.

## Bearish Mirror

Under the locked generalized symmetry rule, the bearish mirror is also locked:

- after valid bearish `C3` expansion
- mark `EQ(C3)`
- seek `C4` with:
  - `high(C4) < EQ(C3)`

## What This Unit Is Measuring

`EQ(C3)` is not used merely as a midpoint marker.

At this layer, it functions as a mechanical wick-quality boundary for `C4`,
just as `EQ(C2)` functioned as a wick-quality boundary for `C3`.

The purpose is to distinguish:

- continuation / expansion-like behavior with controlled wick structure

from:

- deeper retracement or unstable behavior that does not preserve clean
  continuation

## Open Questions

The following remain unresolved and are not yet locked:

1. Is `C4` only a continuation candidate, or already a confirmed continuation?
2. Does `C4` require its own close-based expansion rule?
   - for example: `close(C4) > high(C3)` in the bullish case
3. Are there invalidation rules beyond midpoint violation?

## Implementation Status

Implementation status: in progress.

This spec exists to preserve the doctrinal boundary before code is written.

## Non-goals

This spec does not yet define:

- a final `C4` confirmation rule
- full continuation sequence doctrine beyond the current candidate
- aligned / reversal sequence doctrine
- higher-order context, driver, or SMT logic
