# Real OHLC Review Notes

## Purpose

This file records manual review of detected `C1 -> C2 -> C3` sequence
candidates against the same-source MT5 `XAUUSD 4H` chart/feed.

It is not a profitability log.
It is a doctrine-faithfulness review log.

## Source

- chart/feed: MT5 `XAUUSD 4H`
- raw data file: `data/real_samples/xauusd_4h_mt5_raw.csv`
- normalized verifier file: `data/real_samples/xauusd_4h.csv`

## Confirmed Matches

### Bullish Match 1

- `C1 = 2026-03-04 16:00`
- `C2 = 2026-03-04 20:00`
- `C3 = 2026-03-05 00:00`
- result: `match`

Why it matches:

- `C2` swept below `low(C1)`
- `C2` closed back inside `C1` range
- `low(C3) > EQ(C2)`
- `close(C3) > high(C2)`

### Bullish Match 2

- `C1 = 2026-03-09 12:00`
- `C2 = 2026-03-09 16:00`
- `C3 = 2026-03-09 20:00`
- result: `match`

Why it matches:

- `C2` swept below `low(C1)`
- `C2` closed back inside `C1` range
- `low(C3) > EQ(C2)`
- `close(C3) > high(C2)`

### Bearish Match 1

- `C1 = 2026-03-12 08:00`
- `C2 = 2026-03-12 12:00`
- `C3 = 2026-03-12 16:00`
- result: `match`

Why it matches:

- `C2` swept above `high(C1)`
- `C2` closed back inside `C1` range
- `high(C3) < EQ(C2)`
- `close(C3) < low(C2)`

### Bearish Match 2

- `C1 = 2026-03-13 00:00`
- `C2 = 2026-03-13 04:00`
- `C3 = 2026-03-13 08:00`
- result: `match`

Why it matches:

- `C2` swept above `high(C1)`
- `C2` closed back inside `C1` range
- `high(C3) < EQ(C2)`
- `close(C3) < low(C2)`

## Reviewed Near-Miss

### Bearish Candidate Rejected

- `C1 = 2026-03-13 08:00`
- `C2 = 2026-03-13 12:00`
- `C3 = 2026-03-13 16:00`
- result: `rejected`

Why it was rejected:

- `C2` did sweep above `high(C1)`
- `C2` did close back inside `C1` range
- `C3` did close below `low(C2)`
- but `high(C3)` was **not** below `EQ(C2)`

Interpretation:

- bearish intent was present
- expansion did occur lower
- but the structure did not satisfy the current strict Garrett
  `C1 -> C2 -> C3` bearish rule

## Confirmed C4 Candidate

### Bullish C4 Candidate Match 1

- `C1 = 2026-03-09 12:00`
- `C2 = 2026-03-09 16:00`
- `C3 = 2026-03-09 20:00`
- `C4 = 2026-03-10 00:00`
- result: `match`

Why it matches:

- predecessor `C1 -> C2 -> C3` was already a valid bullish sequence
- `EQ(C3)` was the active continuation boundary
- `low(C4) > EQ(C3)`

Interpretation:

- the current narrow bullish `C4` candidate primitive survived same-source
  MT5 chart review
- this confirms the recursive EQ logic one step higher:
  - `EQ(C2)` qualifies `C3`
  - `EQ(C3)` qualifies `C4`

### Bearish C4 Candidate Match 1

- `C1 = 2026-03-12 08:00`
- `C2 = 2026-03-12 12:00`
- `C3 = 2026-03-12 16:00`
- `C4 = 2026-03-12 20:00`
- result: `match`

Why it matches:

- predecessor `C1 -> C2 -> C3` was already a valid bearish sequence
- `EQ(C3)` was the active continuation boundary
- `high(C4) < EQ(C3)`

Interpretation:

- the narrow bearish `C4` candidate primitive also survived same-source MT5
  chart review
- the generalized bullish/bearish symmetry rule is now supported by reviewed
  real-data behavior at the `C4` candidate layer too

## Current Assessment

The current doctrine implementation state is:

- unit-tested
- real-data tested
- manually confirmed on same-source MT5 chart examples
- extended through the first reviewed bullish `C4` candidate
- extended through the first reviewed bearish `C4` candidate

Current reviewed result set:

- bullish matches: `2`
- bearish matches: `2`
- reviewed near-miss rejection: `1`
- bullish `C4` candidate matches: `1`
- bearish `C4` candidate matches: `1`

This is sufficient evidence to:

- keep the current `C1 -> C2 -> C3` primitive
- keep the narrow bullish `C4` candidate primitive
- keep the narrow bearish `C4` candidate primitive
- proceed to the next doctrine clarification or review step without widening
  scope prematurely
