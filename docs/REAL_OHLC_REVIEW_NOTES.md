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

## Confirmed FVG Matches

### Bullish FVG Match 1

- `C1 = 2026-02-27 08:00`
- `C2 = 2026-02-27 12:00`
- `C3 = 2026-02-27 16:00`
- result: `match`

Why it matches:

- `low(C3) > high(C1)`
- the zone is the wick-to-wick interval between:
  - `high(C1)`
  - `low(C3)`

Interpretation:

- the baseline bullish `FVG` detector matches the reviewed MT5 chart example
- no contradiction is currently observed between the locked baseline `FVG`
  geometry and Garrett's reviewed usage

### Bearish FVG Match 1

- `C1 = 2026-02-23 20:00`
- `C2 = 2026-02-24 00:00`
- `C3 = 2026-02-24 04:00`
- result: `match`

Why it matches:

- `high(C3) < low(C1)`
- the zone is the wick-to-wick interval between:
  - `high(C3)`
  - `low(C1)`

Interpretation:

- the baseline bearish `FVG` detector also matches the reviewed MT5 chart
  example
- current real-data review supports using the standard bullish/bearish
  three-candle imbalance geometry as the working Garrett-compatible baseline

## Confirmed IRL / FVG State Matches

### Reached Bearish FVG Match 1

- `C1 = 2026-02-23 20:00`
- `C2 = 2026-02-24 00:00`
- `C3 = 2026-02-24 04:00`
- candidate state = `reached`
- result: `match`

Why it matches:

- `high(C3) < low(C1)`
- zone = `5191.92` to `5201.13`
- later reviewed candle:
  - `2026-02-25 04:00`
  - `high = 5210.76`
  - `low = 5166.64`
- this later candle range overlaps the gap zone

Interpretation:

- the bearish `FVG` geometry is valid
- price later reached the gap
- so this `IRL` candidate is historical / reached, not still resting

### Reached Bullish FVG Match 1

- `C1 = 2026-02-27 08:00`
- `C2 = 2026-02-27 12:00`
- `C3 = 2026-02-27 16:00`
- candidate state = `reached`
- result: `match`

Why it matches:

- `low(C3) > high(C1)`
- zone = `5199.15` to `5213.95`
- later reviewed candle:
  - `2026-03-03 12:00`
  - `high = 5288.13`
  - `low = 5075.28`
- this later candle range overlaps the gap zone

Interpretation:

- the bullish `FVG` geometry is valid
- price later reached the gap
- so this `IRL` candidate is historical / reached, not still resting

### Resting Bearish FVG Match 1

- `C1 = 2026-03-03 04:00`
- `C2 = 2026-03-03 08:00`
- `C3 = 2026-03-03 12:00`
- candidate state = `resting`
- result: `match`

Why it matches:

- `high(C3) < low(C1)`
- zone = `5288.13` to `5305.41`
- no later reviewed candle overlaps that zone

Interpretation:

- this bearish `FVG` is still resting in the current reviewed sample
- so it remains a live `IRL` candidate in the helper/research layer

### Resting Bearish FVG Match 2

- `C1 = 2026-03-13 12:00`
- `C2 = 2026-03-13 16:00`
- `C3 = 2026-03-13 20:00`
- candidate state = `resting`
- result: `match`

Why it matches:

- `high(C3) < low(C1)`
- zone = `5051.82` to `5079.88`
- no later reviewed candle overlaps that zone

Interpretation:

- this bearish `FVG` is also still resting in the current reviewed sample
- current IRL reporting correctly preserves it as an unreached candidate

## Confirmed ERL Liquidity-State Matches

### Resting Old High Match 1

- `A = 2026-03-10 12:00`
- `B = 2026-03-10 16:00`
- `C = 2026-03-10 20:00`
- candidate = `old_high`
- result: `match`

Why it matches:

- `high(B) > high(A)`
- `high(B) > high(C)`
- so `B` is a confirmed swing high
- no later candle in the reviewed sample traded above `high(B) = 5238.55`

Interpretation:

- this is a valid `old_high` candidate
- the buy-side liquidity above that swing high is still resting in the current
  reviewed sample

### Taken Old High Match 1

- `A = 2026-02-25 00:00`
- `B = 2026-02-25 04:00`
- `C = 2026-02-25 08:00`
- candidate = `old_high`
- result: `match`

Why it matches:

- `high(B) > high(A)`
- `high(B) > high(C)`
- so `B` is a confirmed swing high
- later price traded above `high(B) = 5210.76`
- reviewed take candle:
  - `2026-02-25 16:00 high = 5217.80`

Interpretation:

- this is a valid historical `old_high` candidate
- but that buy-side liquidity has already been taken
- it should not be treated as still-resting liquidity

### Equal Lows Rejection Match 1

- first swing low:
  - `A = 2026-03-06 08:00`
  - `B = 2026-03-06 12:00`
  - `C = 2026-03-06 16:00`
- second swing low:
  - `A = 2026-03-09 12:00`
  - `B = 2026-03-09 16:00`
  - `C = 2026-03-09 20:00`
- result: `rejected as active equal_lows`

Why it was rejected:

- both middle candles are valid swing lows
- their lows are close in price:
  - `5062.82`
  - `5061.04`
- but the earlier low was already taken before the later low formed
- reviewed sweep candle:
  - `2026-03-09 00:00 low = 5014.71`
- and `5014.71 < 5062.82`

Interpretation:

- geometry alone made this look like `equal_lows`
- liquidity-state review shows it is not still-resting equal-lows liquidity
- this confirms the corrected rule:
  - equal highs / lows must also respect taken / untaken state

### Resting Old Low Match 1

- `A = 2026-03-16 08:00`
- `B = 2026-03-16 12:00`
- `C = 2026-03-16 16:00`
- candidate = `old_low`
- result: `match`

Why it matches:

- `low(B) < low(A)`
- `low(B) < low(C)`
- so `B` is a confirmed swing low
- no later candle in the reviewed sample traded below `low(B) = 4970.11`

Interpretation:

- this is a valid `old_low` candidate
- the sell-side liquidity below that swing low is still resting in the current
  reviewed sample

## Confirmed IRL Ranking V1 Matches

### IRL Ranking Match 1

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bearish`
- ranked candidate:
  - bearish `FVG`
  - `C1 = 2026-03-13 12:00`
  - `C2 = 2026-03-13 16:00`
  - `C3 = 2026-03-13 20:00`
  - zone = `5051.82` to `5079.88`
  - rank = `1`
- result: `match`

Why it matches:

- candidate is `resting`
- candidate direction aligns with bearish bias
- it is the nearest `IRL` candidate to current price in the reviewed snapshot
- its score advantage over the next candidates is explained by:
  - full state score
  - full direction-alignment score
  - best proximity score among ranked candidates

Interpretation:

- this is a strong sanity check that the v1 ranker prefers a nearby, resting,
  direction-aligned `IRL`

### IRL Ranking Match 2

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bearish`
- ranked candidate:
  - bearish `FVG`
  - `C1 = 2026-03-03 04:00`
  - `C2 = 2026-03-03 08:00`
  - `C3 = 2026-03-03 12:00`
  - zone = `5288.13` to `5305.41`
  - rank = `2`
- result: `match`

Why it matches:

- candidate is also `resting`
- candidate is also direction-aligned
- but it is much farther from current price and much older than rank `1`

Interpretation:

- the v1 ranking order correctly places this behind the closer and newer
  bearish resting gap

### IRL Ranking Match 3

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bullish`
- ranked candidate:
  - bullish `FVG`
  - `C1 = 2026-03-05 20:00`
  - `C2 = 2026-03-06 00:00`
  - `C3 = 2026-03-06 04:00`
  - zone = `5094.80` to `5114.39`
  - state = `reached`
  - rank = `2`
- result: `match`

Why it matches:

- candidate direction aligns with bullish bias
- but it is already `reached`
- the current v1 score still keeps it above many other bullish candidates
  because it is relatively closer and less stale than those alternatives

Interpretation:

- this confirms the intended v1 tradeoff:
  - reached candidates are discounted
  - but not hard-excluded

### IRL Ranking Match 4

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bullish`
- ranked candidate:
  - bearish `FVG`
  - `C1 = 2026-03-13 12:00`
  - `C2 = 2026-03-13 16:00`
  - `C3 = 2026-03-13 20:00`
  - zone = `5051.82` to `5079.88`
  - state = `resting`
  - rank = `1`
- result: `match`

Why it matches:

- candidate opposes bullish bias
- but it is still `resting`
- and it is the nearest `IRL` candidate to current price
- under the current v1 weights, those advantages are enough to outrank the
  aligned but already-reached bullish alternatives

Interpretation:

- this is not a bug
- it is a reviewed and understood property of v1 weighting
- future versions may change this only by explicit research refinement

### IRL Ranking Match 5

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bullish`
- ranked candidate:
  - bullish `FVG`
  - `C1 = 2026-03-09 16:00`
  - `C2 = 2026-03-09 20:00`
  - `C3 = 2026-03-10 00:00`
  - zone = `5116.12` to `5124.65`
  - state = `reached`
  - rank = `3`
- result: `match`

Why it matches:

- candidate is bullish and therefore bias-aligned
- candidate is reached, so it is discounted on state
- it ranks below the bullish reached candidate at rank `2` because its feature
  mix is slightly weaker in the reviewed snapshot

Interpretation:

- the relative order among reached bullish candidates matched the reviewed chart
  state and current v1 scoring explanation

## Confirmed ERL Ranking V1 Matches

### ERL Ranking Match 1

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bullish`
- ranked candidate:
  - `old_low`
  - side = `sell_side`
  - anchors:
    - `2026-03-17 12:00 +05:00`
    - `2026-03-17 16:00 +05:00`
    - `2026-03-17 20:00 +05:00`
  - level = `4973.51`
  - state = `resting`
  - rank = `1`
- result: `match`

Why it matches:

- `low(B) < low(A)`
- `low(B) < low(C)`
- so the middle candle is a confirmed swing low
- no later candle in the reviewed snapshot traded below `4973.51`
- under corrected `ERL -> IRL` reaction semantics:
  - bullish bias watches `old_low` / `sell_side` liquidity

Interpretation:

- this confirms the corrected `ERL` ranking direction model:
  - bullish bias aligns with reaction from `old_lows`
- the top-ranked bullish `ERL` is a nearby, resting swing low

### ERL Ranking Match 2

- snapshot:
  - `as_of = 2026-03-18 04:00 +05:00`
  - `current_price = 4989.97`
  - `direction_bias = bearish`
- ranked candidate:
  - `old_high`
  - side = `buy_side`
  - anchors:
    - `2026-03-17 20:00 +05:00`
    - `2026-03-18 00:00 +05:00`
    - `2026-03-18 04:00 +05:00`
  - level = `5015.99`
  - state = `resting`
  - rank = `1`
- result: `match`

Why it matches:

- `high(B) > high(A)`
- `high(B) > high(C)`
- so the middle candle is a confirmed swing high
- no later candle exists after `confirmed_at` inside the reviewed snapshot, so
  the liquidity is still resting
- under corrected `ERL -> IRL` reaction semantics:
  - bearish bias watches `old_high` / `buy_side` liquidity

Interpretation:

- this confirms the corrected `ERL` ranking direction model:
  - bearish bias aligns with reaction from `old_highs`
- the top-ranked bearish `ERL` is a nearby, fresh, resting swing high

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
- bullish `FVG` matches: `1`
- bearish `FVG` matches: `1`
- reached bearish `FVG` matches: `1`
- reached bullish `FVG` matches: `1`
- resting bearish `FVG` matches: `2`
- resting `old_high` ERL matches: `1`
- taken `old_high` ERL matches: `1`
- rejected `equal_lows` grouping matches: `1`
- resting `old_low` ERL matches: `1`
- reviewed `IRL` ranking v1 matches: `5`

This is sufficient evidence to:

- keep the current `C1 -> C2 -> C3` primitive
- keep the narrow bullish `C4` candidate primitive
- keep the narrow bearish `C4` candidate primitive
- keep the baseline bullish/bearish `FVG` primitive
- keep the helper-layer `IRL` candidate-state boundary between:
  - resting gaps
  - and already-reached gaps
- keep the current `IRL` ranking v1 behavior as a valid research baseline:
  - explicit
  - leakage-safe
  - manually reviewed on MT5
- keep the corrected ERL liquidity-state boundary between:
  - historical swing-derived liquidity
  - and still-resting liquidity
- proceed to the next doctrine clarification or review step without widening
  scope prematurely
