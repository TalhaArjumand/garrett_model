# C2 Reversal To Expansion Implementation Notes

## Purpose

This note defines the implementation boundary for the currently reviewed
`C2 reversal to expansion` case.

It exists to keep three things separate:

- doctrine
- runtime-safe primitive detection
- later trade-selection logic

## Doctrine Boundary

Current reviewed doctrine supports:

- `C1` is not the trade candle
- `C2 reversal to expansion` is a second swing-formation case
- a small wick is the key discriminator
- `C2` may itself be the expansion candle in this compressed case

Current reviewed doctrine does **not** yet define:

- an exact numeric wick threshold
- whether near-miss proximity to key level is sufficient
- a merged selector between Case A and Case B

## Runtime Boundary

Case B must be knowable at `C2` close.

So a Case B primitive may only use:

- `C1`
- `C2`

It must not use:

- `C3`
- `C4`
- later candles

## Current Primitive Shape

The narrow v1 primitive is a two-candle candidate detector.

Bullish candidate:

- `low(C2) < low(C1)`
- `close(C2) > open(C2)`
- `close(C2) > low(C1)`
- `lower_wick(C2) / range(C2) <= threshold`

Bearish candidate:

- `high(C2) > high(C1)`
- `close(C2) < open(C2)`
- `close(C2) < high(C1)`
- `upper_wick(C2) / range(C2) <= threshold`

## Wick Threshold Status

The wick threshold is a research parameter, not locked Garrett doctrine.

The current implementation exposes it explicitly as a function argument rather
than hardcoding a hidden selector.

Default research value:

- `0.25`

## Edge-Case Rules

The current implementation should reject:

- zero-range `C2`
- non-consecutive candles
- unclosed candles
- mixed symbol or timeframe inputs
- equality sweeps:
  - `low(C2) == low(C1)` is not enough
  - `high(C2) == high(C1)` is not enough
- non-directional `C2` bodies

## Implementation Status

Implementation status: partially implemented.

Current implementation includes:

- isolated bullish and bearish Case B primitives
- explicit research wick-threshold parameter
- real-data candidate counting

Not implemented yet:

- merged Case A / Case B swing-formation detector
- ranking interaction with key-level context
- trade execution logic
