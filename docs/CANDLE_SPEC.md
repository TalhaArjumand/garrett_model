# Candle Spec

## Purpose

The `Candle` is the atomic price object for the Garrett trading research system.
All higher-order doctrine units such as swing formation, sequence detection, and
later labeling must operate on validated candles.

## Schema

Each candle must contain:

- `symbol`: market identifier such as `XAUUSD`, `NQ`, or `EURUSD`
- `timestamp`: start time of the candle as an ISO 8601 datetime
- `timeframe`: discrete timeframe string
- `open`: opening price for the candle window
- `high`: highest traded price in the candle window
- `low`: lowest traded price in the candle window
- `close`: closing price for the candle window
- `is_closed`: whether the candle is complete and safe for doctrine logic

## Derived Candle Primitives

These are derived from raw OHLC values and are still part of the candle layer,
not doctrine interpretation:

- `body_size = abs(close - open)`
- `range_size = high - low`
- `body_top = max(open, close)`
- `body_bottom = min(open, close)`
- `upper_wick = high - body_top`
- `lower_wick = body_bottom - low`

Direction is also derived:

- bullish if `close > open`
- bearish if `close < open`
- doji if `close == open`

## Geometric Invariant

For a valid candle, geometric decomposition should hold:

- `body_size + upper_wick + lower_wick == range_size`

In code this should be checked with float tolerance rather than exact equality.

## Allowed Timeframes

The initial supported timeframes are:

- `5m`
- `15m`
- `30m`
- `1H`
- `4H`
- `1D`

Timeframe support can be extended later, but doctrine logic must reject unknown
timeframes rather than guess.

## Invariants

A valid candle must satisfy all of the following:

1. `symbol` is a non-empty string.
2. `timestamp` is timezone-aware.
3. `timeframe` is one of the allowed values.
4. `open`, `high`, `low`, and `close` are numeric.
5. All price fields are strictly positive.
6. `high >= open`
7. `high >= close`
8. `high >= low`
9. `low <= open`
10. `low <= close`
11. `low <= high`

## Doctrine Safety Rule

Any doctrine primitive that depends on candle confirmation must require
`is_closed == True`.

This is non-negotiable because the first doctrine unit we locked, swing
formation, only becomes valid after the confirming candle has closed.

## Implementation Notes

- Validation should fail loudly and early.
- The model should not silently coerce invalid data.
- Future code may add helpers for parsing JSON/CSV rows into candles, but the
  core candle object should stay strict.

## Testing Strategy

The first test layer is not live market data. It is controlled examples:

- valid candles
- invalid OHLC combinations
- invalid timeframe
- naive timestamp mistakes
- open or close outside the `low` / `high` range
- unclosed candles for doctrine-sensitive workflows
- bullish candle geometry
- bearish candle geometry
- doji geometry
- wick calculations
- range decomposition invariant

After unit tests pass, the same schema can be exercised against real OHLC data.
