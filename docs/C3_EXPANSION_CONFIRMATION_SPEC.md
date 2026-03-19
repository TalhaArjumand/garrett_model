# C3 Expansion Confirmation Spec

## Purpose

This spec defines the next Garrett-specific doctrine primitive after `C2
closure` and `C3 support`: `C3 expansion confirmation`.

At this layer, support is no longer enough. `C3` must prove expansion with a
strict close beyond the relevant extreme of `C2`.

Current reviewed execution interpretation:

- `C3` is not only a confirmation candle in the abstract
- `C3` is the expansion candle Garrett wants to trade in the currently reviewed
  material

## Inputs

This primitive uses:

- `c2`
- `c3`

Both inputs must be valid `Candle` objects.

## Preconditions

All of the following must be true:

1. `c2` and `c3` are `Candle` objects.
2. Both candles are closed.
3. Both candles have the same symbol.
4. Both candles have the same timeframe.
5. `c3.timestamp > c2.timestamp`
6. `c3` is the immediate next candle after `c2` for that timeframe.

## Bullish C3 Expansion Confirmation

A bullish `C3 expansion confirmation` exists when:

- `close(c3) > high(c2)`

The inequality is strict.

## Bearish C3 Expansion Confirmation

A bearish `C3 expansion confirmation` exists when:

- `close(c3) < low(c2)`

The inequality is strict.

## Rejection Conditions

Reject the primitive if any of the following are true:

- mixed symbols
- mixed timeframes
- malformed candle objects
- either candle is unclosed
- wrong timestamp order
- non-consecutive candles
- equality at the confirmation boundary

## Composition Note

This primitive is intended to remain atomic.

Full sequence validity is defined later by composing:

- `C2 closure`
- `C3 support`
- `C3 expansion confirmation`

But current reviewed execution logic treats the composed result as:

- key level reached
- swing formation qualified
- `C3` expansion becomes the tradeable event

## Research Quality Layer

The repo also tracks a stricter research-only quality path for this `Type A`
expansion candle in
[C3_EXPANSION_QUALITY_RESEARCH.md](/Users/njap/Downloads/garrett-trading-research/docs/C3_EXPANSION_QUALITY_RESEARCH.md).

That stricter path is not doctrine. It adds directional body consistency and
the shared small same-side wick helper on top of the base `Type A` sequence.

## Non-goals

This spec does not define:

- `C4` continuation
- full continuation sequence doctrine
- reversal / aligned sequence doctrine
- higher-order context interpretation
- all later Garrett trade-entry variants outside the currently reviewed
  material
