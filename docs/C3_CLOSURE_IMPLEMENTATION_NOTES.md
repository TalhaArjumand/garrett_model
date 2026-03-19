# C3 Closure Implementation Notes

## Purpose

This note defines the implementation boundary for the currently reviewed
`C3 closure` swing-formation type.

It exists to keep separate:

- doctrine
- runtime-safe primitive detection
- later trade-selection logic

## Doctrine Boundary

Current reviewed doctrine supports:

- `C3 closure` is a third swing-formation type
- `C2` still sweeps the relevant edge of `C1` in this type
- it begins where the Type A `C2` closure does not occur
- reversal is not knowable before `C3` closes
- a strong `C3` closure is defined as closing over the body of `C2`
- after that closure, `EQ(C3)` becomes the active `C4` continuation boundary

Current reviewed doctrine does **not** yet define:

- a final machine-ready bullish formula
- a final machine-ready bearish formula
- whether `C4` here is best treated finally as continuation-only or as the
  actionable candle

## Runtime Boundary

The `C3 closure` primitive must be knowable at `C3` close.

So the primitive may only use:

- `C1`
- `C2`
- `C3`

The downstream Type C continuation candidate may only use:

- `C1`
- `C2`
- `C3`
- `C4`

No later candles may leak into either decision.

## Current Primitive Shape

The current v1 implementation is a doctrine-safe but still research-bounded
machine form.

Bullish primitive:

- `low(C2) < low(C1)`
- no valid Type A bullish `C2` closure exists
- `C3` is bullish
- `low(C3) > low(C2)`
- `close(C3) > body_top(C2)`

Bearish primitive:

- `high(C2) > high(C1)`
- no valid Type A bearish `C2` closure exists
- `C3` is bearish
- `high(C3) < high(C2)`
- `close(C3) < body_bottom(C2)`

## Why This Stays Research-Bounded

These machine rules are the current best implementation reading of the reviewed
material, but they still contain explicit symmetry assumptions.

They now intentionally do not require a fixed `C2` body color in Type C,
because the current reviewed reading is that sweep + absence of Type A closure +
strong `C3` body close are the decisive conditions.

So they should be treated as:

- implementation-safe
- runtime-safe
- reviewable

but not yet as final locked Garrett formulas.

## Type C C4 Candidate

After a valid Type C `C3 closure`, the current candidate continuation rule is:

- bullish:
  - `low(C4) > EQ(C3)`
- bearish:
  - `high(C4) < EQ(C3)`

This mirrors the already reviewed `EQ(C3)` continuation boundary logic.

## Stricter Type C C4 Quality Layer

A stricter research-only layer can sit on top of the base Type C `C4`
candidate:

- bullish:
  - base bullish Type C `C4` candidate
  - bullish `C4` body
  - small lower wick by explicit research threshold
- bearish:
  - base bearish Type C `C4` candidate
  - bearish `C4` body
  - small upper wick by explicit research threshold

This should be treated as:

- research quality filter
- not replacement doctrine
- runtime-safe only at `C4` close

## Edge-Case Rules

The current implementation should reject:

- malformed candles
- unclosed candles
- mixed symbol or timeframe inputs
- non-consecutive candles
- zero-range `C2`
- equality at the decisive boundaries:
  - `low(C2) == low(C1)` is not enough for bullish
  - `high(C2) == high(C1)` is not enough for bearish
  - `close(C3) == body_top(C2)` is not enough for bullish
  - `close(C3) == body_bottom(C2)` is not enough for bearish
  - `low(C3) == low(C2)` is not enough for bullish
  - `high(C3) == high(C2)` is not enough for bearish

## Implementation Status

Implementation status: partially implemented.

Current implementation includes:

- isolated bullish and bearish `C3 closure` primitives
- separate bullish and bearish Type C `C4` continuation candidates
- real-data candidate counting

Not implemented yet:

- merged Type A / Type B / Type C swing-formation selection
- higher-level trade ranking
- SMT integration
