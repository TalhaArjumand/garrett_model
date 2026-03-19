# C2 Closure Spec

## Purpose

This spec defines the first Garrett-specific doctrine primitive after the candle
layer: `C2 closure`.

The earlier generic three-candle swing-point primitive has been removed because
it does not belong to Garrett's teaching as the primary doctrine unit.

## Sequence Scope

This spec covers the first part of the bullish and bearish swing-formation
sequence:

1. `C1` establishes the reference range.
2. `C2` sweeps beyond the relevant edge of `C1`.
3. `C2` closes back inside `C1`'s range.
4. `EQ(C2)` is marked.
5. `C3` must respect the correct half of `C2`'s range.

Continuation into `C4` is not implemented yet.

Current reviewed execution interpretation:

- `C2` is the swing-formation / closure-side event
- `C2` is not the primary trade candle
- the tradeable event is the later expansion candle if the structure continues
  to qualify

## Inputs

The primitive uses:

- `c1`
- `c2`
- `c3`

All inputs must be valid `Candle` objects.

## Preconditions

All of the following must be true:

1. `c1`, `c2`, and `c3` are `Candle` objects.
2. All three candles are closed.
3. All three candles have the same symbol.
4. All three candles have the same timeframe.
5. The timestamps are strictly ordered as `c1 < c2 < c3`.
6. The candles are consecutive for their timeframe.

## C2 Range Equilibrium

`EQ(C2)` is the midpoint of `C2`'s full range:

- `eq(c2) = low(c2) + (high(c2) - low(c2)) / 2`

This is used mechanically to measure wick size and the acceptable half of the
range for the next candle.

## Bullish C2 Closure

A bullish `C2 closure` exists when:

1. `low(c2) < low(c1)`  (C2 sweeps below C1 low)
2. `low(c1) < close(c2) < high(c1)`  (C2 closes fully back inside C1 range)

The inequalities are strict.

## Bullish C3 Support

After a valid bullish `C2 closure`, bullish support for `C3` requires:

1. `low(c3) > eq(c2)`

At the current implementation stage, this is strict and wick interaction with
`EQ(C2)` is not allowed.

## Bearish C2 Closure

A bearish `C2 closure` exists when:

1. `high(c2) > high(c1)`  (C2 sweeps above C1 high)
2. `low(c1) < close(c2) < high(c1)`  (C2 closes fully back inside C1 range)

The inequalities are strict.

## Bearish C3 Support

After a valid bearish `C2 closure`, bearish support for `C3` requires:

1. `high(c3) < eq(c2)`

At the current implementation stage, this is strict and wick interaction with
`EQ(C2)` is not allowed.

## Rejection Conditions

Reject the sequence if any of the following are true:

- mixed symbols
- mixed timeframes
- any candle is unclosed
- malformed candle objects
- wrong timestamp order
- non-consecutive timestamps
- `C2` does not sweep the relevant edge of `C1`
- `C2` closes on or outside the boundary of `C1`'s range
- `C3` touches or crosses `EQ(C2)` when strict support is required

## Non-goals

This spec does not yet define:

- `C3` closing above `high(C2)` for bullish continuation
- `C3` closing below `low(C2)` for bearish continuation
- `C4` continuation logic
- small-wick doctrine beyond the strict `C3` support rule
- full continuation / reversal / aligned sequence logic
- standalone trade-entry mechanics by itself
