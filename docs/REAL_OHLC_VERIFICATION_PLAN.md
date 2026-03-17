# Real OHLC Verification Plan

## Purpose

This layer verifies that the current Garrett doctrine primitives behave
correctly on real market candles.

It is not a backtest, not a profitability study, and not an ML evaluation.

## Current Scope

The first real-data verification target is:

- `symbol`: `XAUUSD`
- `timeframe`: `4H`

## Goals

The real OHLC verification layer should prove:

1. real candle rows parse into strict `Candle` objects
2. timestamps are ordered correctly
3. candles are consecutive at the 4H level
4. data gaps are detected explicitly
5. current Garrett primitives run cleanly on real candles
6. a small set of detected sequences can be checked manually against charts

## Non-goals

This layer does not prove:

- profitability
- predictive value
- strategy robustness
- broker execution quality
- slippage realism

## Expected Input File

Place the real sample here:

- `data/real_samples/xauusd_4h.csv`

The file should contain only closed candles.

## Required CSV Columns

Use this exact schema:

- `symbol`
- `timestamp`
- `timeframe`
- `open`
- `high`
- `low`
- `close`

Timestamps should be exported in UTC when possible. If the source exports
another timezone, normalize it before relying on the results.

## Verification Steps

### 1. Parsing

Every row must load into a strict `Candle`.

### 2. Continuity

Rows must be:

- sorted by timestamp
- 4 hours apart
- same symbol
- same timeframe

Missing bars should be reported, not silently ignored.

### 3. Sequence Scan

Slide a 3-candle window across the sample and evaluate:

- bullish `C2` closure
- bearish `C2` closure
- bullish `C3` support
- bearish `C3` support
- bullish `C3` expansion confirmation
- bearish `C3` expansion confirmation
- full bullish `C1 -> C2 -> C3` sequence
- full bearish `C1 -> C2 -> C3` sequence

### 4. Manual Chart Alignment

For a small subset of detected sequences:

- record the `C1`, `C2`, `C3` timestamps
- compare them manually against the actual chart
- mark each one as:
  - `match`
  - `mismatch`
  - `unclear`

## Expected Output

The verification layer should be able to report:

- total candles loaded
- continuity status
- missing timestamp gaps
- bullish sequence count
- bearish sequence count
- manual review candidates

## Success Criteria

This layer is successful when:

- the real sample loads cleanly
- gaps are either absent or explicitly reported
- detected sequences are plausible on chart review
- any mismatches can be traced back to doctrine or data issues
