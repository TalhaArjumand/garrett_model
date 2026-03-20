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
- it remains a live `IRL` candidate in the helper/research layer

## Confirmed Case B Matches

### Bullish Case B Match 1

- `C1 = 2026-02-27 08:00`
- `C2 = 2026-02-27 12:00`
- result: `match`

Why it matches:

- `low(C2) < low(C1)`
- `close(C2) > open(C2)`
- `close(C2) > low(C1)`
- `lower_wick(C2) / range(C2) = 0.101391`
- current default research threshold = `0.25`

Interpretation:

- this is a clean bullish `C2 reversal to expansion` candidate
- the reversal and expansion are compressed into `C2`
- the lower wick remains small enough to support expansion away from reversal

### Bullish Case B Match 2

- `C1 = 2026-03-16 08:00`
- `C2 = 2026-03-16 12:00`
- result: `match`

Why it matches:

- `low(C2) < low(C1)`
- `close(C2) > open(C2)`
- `close(C2) > low(C1)`
- `lower_wick(C2) / range(C2) = 0.081623`
- current default research threshold = `0.25`

Interpretation:

- this is another strong bullish compressed reversal-to-expansion case
- the wick is small relative to the full candle range
- the runtime-safe two-candle primitive matches the reviewed MT5 chart

### Bullish Case B Match 3

- `C1 = 2026-03-09 12:00`
- `C2 = 2026-03-09 16:00`
- result: `match`

Why it matches:

- `low(C2) < low(C1)`
- `close(C2) > open(C2)`
- `close(C2) > low(C1)`
- `lower_wick(C2) / range(C2) = 0.237836`
- current default research threshold = `0.25`

Interpretation:

- this bullish Case B candidate still passes, but it is near the current wick
  threshold
- it is therefore a useful stress-test example for the research parameter
  boundary

### Bearish Case B Match 1

- `C1 = 2026-03-10 00:00`
- `C2 = 2026-03-10 04:00`
- result: `match`

Why it matches:

- `high(C2) > high(C1)`
- `close(C2) < open(C2)`
- `close(C2) < high(C1)`
- `upper_wick(C2) / range(C2) = 0.083766`
- current default research threshold = `0.25`

Interpretation:

- this is a clean bearish `C2 reversal to expansion` candidate
- expansion away from the reversal occurs inside `C2` itself

### Bearish Case B Match 2

- `C1 = 2026-03-13 00:00`
- `C2 = 2026-03-13 04:00`
- result: `match`

Why it matches:

- `high(C2) > high(C1)`
- `close(C2) < open(C2)`
- `close(C2) < high(C1)`
- `upper_wick(C2) / range(C2) = 0.143758`
- current default research threshold = `0.25`

Interpretation:

- this is another reviewed bearish compressed reversal-to-expansion case
- the current Case B primitive matches the same-source MT5 chart here as well
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

## Confirmed Rare Type C Research Matches

### Rare Type C Match 1

- classification:
  - research-only rare bullish `Type C` subtype
- `C1 = 2026-02-24 20:00 +05:00`
- `C2 = 2026-02-25 00:00 +05:00`
- `C3 = 2026-02-25 04:00 +05:00`
- result: `match`

Why it matches:

- `C2` swept below `low(C1)`
  - `5120.04 < 5140.49`
- `C2` did not produce a Type A close back inside full `C1` range
  - `close(C2) = 5176.99`
  - `high(C1) = 5173.30`
- `C2` closed strongly beyond the opposite boundary of `C1`
  - `5176.99 > 5173.30`
- `EQ(C2) = 5155.03`
- `low(C3) > EQ(C2)`
  - `5166.64 > 5155.03`
- `close(C3) > body_top(C2)`
  - `5201.88 > 5176.99`

Interpretation:

- this is a strong bullish `Type C` subtype on real MT5 data
- it is stronger than base `Type C`, but still belongs in the research layer
- current status is:
  - rare
  - real
  - testable
  - not yet doctrine

### Rare Type C Match 2

- classification:
  - research-only rare bullish `Type C` subtype
- `C1 = 2026-02-27 08:00 +05:00`
- `C2 = 2026-02-27 12:00 +05:00`
- `C3 = 2026-02-27 16:00 +05:00`
- result: `match`

Why it matches:

- `C2` swept below `low(C1)`
  - `5168.70 < 5172.24`
- `C2` did not produce a Type A close back inside full `C1` range
  - `close(C2) = 5223.13`
  - `high(C1) = 5199.15`
- `C2` closed strongly beyond the opposite boundary of `C1`
  - `5223.13 > 5199.15`
- `EQ(C2) = 5204.65`
- `low(C3) > EQ(C2)`
  - `5213.95 > 5204.65`
- `close(C3) > body_top(C2)`
  - `5234.71 > 5223.13`

Interpretation:

- this is a second manually confirmed bullish rare-case `Type C` subtype
- the subtype is not a synthetic artifact because it survives:
  - real MT5 export
  - code detection
  - manual chart review
- but it is still not broad enough yet to become a new doctrine category

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
- bullish Case B matches: `3`
- bearish Case B matches: `2`
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
- reviewed `ERL` ranking v1 matches: `2`
- reviewed rare bullish `Type C` subtype matches: `2`
- reviewed rare bullish `Type C` `C3` expansion-quality matches: `2`

This is sufficient evidence to:

- keep the current `C1 -> C2 -> C3` primitive
- keep the narrow bullish `C4` candidate primitive
- keep the narrow bearish `C4` candidate primitive
- keep the narrow bullish `C2 reversal to expansion` primitive
- keep the narrow bearish `C2 reversal to expansion` primitive
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

## Rare Type C C4 Status

The rare `Type C` subtype is now implemented through the same downstream `C4`
checks as base `Type C`:

- base `C4` continuation
- stricter `C4` expansion-quality filter

Current reviewed status on the same MT5 `XAUUSD 4H` sample:

- bullish rare `Type C` `C4` continuation matches: `0`
- bearish rare `Type C` `C4` continuation matches: `0`
- bullish rare `Type C` `C4` expansion-quality matches: `0`
- bearish rare `Type C` `C4` expansion-quality matches: `0`

So the current repo-safe statement is:

- the downstream rare-subtype path is implemented
- unit-tested
- real-data counted
- but there are no current same-sample MT5 manual examples yet for this path

## Confirmed 2026-03-19 Window Refresh Matches

### Bearish Type A Strict C3 Match 3

- `C1 = 2026-03-18 04:00 +05:00`
- `C2 = 2026-03-18 08:00 +05:00`
- `C3 = 2026-03-18 12:00 +05:00`
- result: `match`

Why it matches:

- `C2` swept above `high(C1)`
  - `5016.30 > 5007.00`
- `C2` closed back inside full `C1` range
  - `close(C2) = 4992.12`
- `EQ(C2) = 4996.735`
- `high(C3) < EQ(C2)`
  - `4992.14 < 4996.735`
- `close(C3) < low(C2)`
  - `4878.20 < 4977.17`
- same-side wick on `C3` is small enough for the strict expansion-quality path

Interpretation:

- this new rolling-window bearish `Type A` sequence is valid on the refreshed
  same-source MT5 sample
- it also survives the shared expansion-quality filter

### Bearish C4 Match 2

- `C1 = 2026-03-18 04:00 +05:00`
- `C2 = 2026-03-18 08:00 +05:00`
- `C3 = 2026-03-18 12:00 +05:00`
- `C4 = 2026-03-18 16:00 +05:00`
- result: `match`

Why it matches:

- predecessor `C1 -> C2 -> C3` is already a valid bearish sequence
- `EQ(C3) = 4913.155`
- `high(C4) < EQ(C3)`
  - `4898.97 < 4913.155`

Interpretation:

- the refreshed sample adds one more valid bearish continuation case
- this supports the recursive continuation logic on the newly expanded window

### Resting Bearish FVG Match 3

- `C1 = 2026-03-19 04:00 +05:00`
- `C2 = 2026-03-19 08:00 +05:00`
- `C3 = 2026-03-19 12:00 +05:00`
- candidate state = `resting`
- result: `match`

Why it matches:

- `high(C3) < low(C1)`
  - `4719.84 < 4826.82`
- zone = `4719.84` to `4826.82`
- no later reviewed candle in the refreshed sample overlaps that zone

Interpretation:

- this is a new resting bearish `IRL/FVG` candidate on the refreshed MT5
  window

### Resting Bearish FVG Match 4

- `C1 = 2026-03-19 08:00 +05:00`
- `C2 = 2026-03-19 12:00 +05:00`
- `C3 = 2026-03-19 16:00 +05:00`
- candidate state = `resting`
- result: `match`

Why it matches:

- `high(C3) < low(C1)`
  - `4643.14 < 4686.85`
- zone = `4643.14` to `4686.85`
- no later reviewed candle in the refreshed sample overlaps that zone

Interpretation:

- this is a second new resting bearish `IRL/FVG` candidate on the refreshed
  window

## Confirmed ERL Delta Audit Matches

### New Resting Old High Match 1

- anchors:
  - `2026-03-18 04:00 +05:00`
  - `2026-03-18 08:00 +05:00`
  - `2026-03-18 12:00 +05:00`
- level: `5016.30`
- result: `match`

Why it matches:

- middle candle is a confirmed swing high
  - `5016.30 > 5007.00`
  - `5016.30 > 4992.14`
- no later candle in the refreshed 100-bar window trades above `5016.30`

Interpretation:

- this is a valid newly entered resting `old_high`
- the refreshed ERL inventory is correctly picking up new external highs on the
  right edge of the window

### New Resting Old High Match 2

- anchors:
  - `2026-03-18 16:00 +05:00`
  - `2026-03-18 20:00 +05:00`
  - `2026-03-19 00:00 +05:00`
- level: `4899.12`
- result: `match`

Why it matches:

- middle candle is a confirmed swing high
- no later candle in the refreshed window trades above `4899.12`

Interpretation:

- this is the second newly entered resting `old_high`
- the ERL helper layer remains consistent after the rolling-window refresh

### New Resting Old Low Match 1

- anchors:
  - `2026-03-19 08:00 +05:00`
  - `2026-03-19 12:00 +05:00`
  - `2026-03-19 16:00 +05:00`
- level: `4502.57`
- result: `match`

Why it matches:

- middle candle is a confirmed swing low
- no later candle exists yet below `4502.57` in the refreshed window

Interpretation:

- this is a valid newly entered resting `old_low`
- the new right-edge swing-low inventory is being counted correctly

### State-Change Old High Match 1

- anchors:
  - `2026-03-17 20:00 +05:00`
  - `2026-03-18 00:00 +05:00`
  - `2026-03-18 04:00 +05:00`
- level: `5015.99`
- prior state: `resting`
- new state: `taken`
- taken at: `2026-03-18 08:00 +05:00`
- result: `match`

Why it matches:

- take candle high:
  - `5016.30 > 5015.99`

Interpretation:

- the refreshed window correctly flips this `old_high` from resting to taken
- this confirms the ERL state-transition logic on newly arrived candles

### State-Change Old Low Match 1

- anchors:
  - `2026-03-16 08:00 +05:00`
  - `2026-03-16 12:00 +05:00`
  - `2026-03-16 16:00 +05:00`
- level: `4970.11`
- prior state: `resting`
- new state: `taken`
- taken at: `2026-03-18 12:00 +05:00`
- result: `match`

Why it matches:

- take candle low:
  - `4834.17 < 4970.11`

Interpretation:

- this confirms a valid low-side sweep in the refreshed window

### State-Change Old Low Match 2

- anchors:
  - `2026-03-17 12:00 +05:00`
  - `2026-03-17 16:00 +05:00`
  - `2026-03-17 20:00 +05:00`
- level: `4973.51`
- prior state: `resting`
- new state: `taken`
- taken at: `2026-03-18 12:00 +05:00`
- result: `match`

Why it matches:

- take candle low:
  - `4834.17 < 4973.51`

Interpretation:

- this confirms the second low-side state transition caused by the same sharp
  downside move
- the ERL state model remains faithful on the refreshed MT5 data

## Confirmed Rare Type C C3 Expansion-Quality Matches

### Rare Type C C3 Expansion-Quality Match 1

- classification:
  - research-only bullish rare `Type C` `C3` expansion-quality subtype
- `C1 = 2026-02-24 20:00 +05:00`
- `C2 = 2026-02-25 00:00 +05:00`
- `C3 = 2026-02-25 04:00 +05:00`
- result: `match`

Why it matches:

- valid bullish rare `Type C` subtype already exists
- `C2` swept below `low(C1)`
  - `5120.04 < 5140.49`
- `C2` closed beyond `high(C1)`
  - `5176.99 > 5173.30`
- `EQ(C2) = 5155.03`
- `low(C3) > EQ(C2)`
  - `5166.64 > 5155.03`
- `close(C3) > body_top(C2)`
  - `5201.88 > 5176.99`
- `C3` same-side wick fraction:
  - `0.234587`

Interpretation:

- this confirms that, in this rare bullish `Type C` subtype, `C3` itself can
  already satisfy the research expansion-quality condition
- this remains:
  - research only
  - real-data confirmed
  - not yet doctrine

### Rare Type C C3 Expansion-Quality Match 2

- classification:
  - research-only bullish rare `Type C` `C3` expansion-quality subtype
- `C1 = 2026-02-27 08:00 +05:00`
- `C2 = 2026-02-27 12:00 +05:00`
- `C3 = 2026-02-27 16:00 +05:00`
- result: `match`

Why it matches:

- valid bullish rare `Type C` subtype already exists
- `C2` swept below `low(C1)`
  - `5168.70 < 5172.24`
- `C2` closed beyond `high(C1)`
  - `5223.13 > 5199.15`
- `EQ(C2) = 5204.65`
- `low(C3) > EQ(C2)`
  - `5213.95 > 5204.65`
- `close(C3) > body_top(C2)`
  - `5234.71 > 5223.13`
- `C3` same-side wick fraction:
  - `0.208494`

Interpretation:

- this second manual confirmation shows the new `C3` quality path is
  repeatable on the same-source MT5 export
- current repo-safe status remains:
  - rare
  - real
  - testable
  - not yet doctrine

## Confirmed Integrated Internal-to-External Type A Review

### Corrected Bridge Boundary

- review scope:
  - integrated `IRL -> Type A -> strict C3` bridge
- correction applied:
  - the first bridge version was too permissive because it paired Type A
    sequences with prior `FVG` geometry even if that gap had already been
    reached earlier
- corrected rule:
  - build the `IRL` inventory from candles strictly before sequence `C1`
  - use existing `FVGCandidate` state logic
  - only same-direction `is_resting` `IRL`s are eligible
  - then check whether sequence `C1` or `C2` touches that still-active `IRL`

Interpretation:

- this now follows left-to-right market state instead of retrospective pairing
- already-reached `IRL/FVG`s cannot be reused later as active key levels

### Corrected March 19 Window Counts

- `bullish_internal_to_external_type_a_count = 0`
- `bearish_internal_to_external_type_a_count = 1`
- `bullish_internal_to_external_type_a_expansion_quality_count = 0`
- `bearish_internal_to_external_type_a_expansion_quality_count = 1`

Interpretation:

- the earlier bullish and one earlier bearish pairing disappeared for the
  correct reason: their `IRL/FVG`s had already been reached before the later
  Type A sequence began
- the corrected integrated bridge now leaves only one valid same-window
  real-data match

### Dropped Historical IRL Pairing 1

- dropped prior `IRL`:
  - bullish `FVG` `5094.80 -> 5114.39`
  - confirmed at `2026-03-06 04:00 +05:00`
  - reached at `2026-03-06 08:00 +05:00`
- later sequence that must no longer pair:
  - `2026-03-09 12:00 / 16:00 / 20:00 +05:00`
- result after correction:
  - rejected as active integrated `IRL -> Type A`

Interpretation:

- this confirms the bridge no longer reuses an already-reached bullish `IRL`
  for a later bullish Type A sequence

### Dropped Historical IRL Pairing 2

- dropped prior `IRL`:
  - bearish `FVG` `5175.60 -> 5226.29`
  - confirmed at `2026-03-03 16:00 +05:00`
  - reached at `2026-03-04 00:00 +05:00`
- later sequence that must no longer pair:
  - `2026-03-12 08:00 / 12:00 / 16:00 +05:00`
- result after correction:
  - rejected as active integrated `IRL -> Type A`

Interpretation:

- this confirms the bridge no longer reuses an already-reached bearish `IRL`
  for a much later bearish Type A sequence

### Surviving Integrated Type A Match 1

- classification:
  - bearish integrated `IRL -> Type A -> strict C3`
- active `IRL`:
  - bearish `FVG` from:
    - `2026-03-12 12:00 +05:00`
    - `2026-03-12 16:00 +05:00`
    - `2026-03-12 20:00 +05:00`
  - zone:
    - `5112.61 -> 5146.09`
  - state immediately before sequence `C1`:
    - `resting`
- sequence:
  - `C1 = 2026-03-13 00:00 +05:00`
  - `C2 = 2026-03-13 04:00 +05:00`
  - `C3 = 2026-03-13 08:00 +05:00`
- result:
  - `match`

Why it matches:

- before `C1`, this bearish `IRL` still exists as a resting candidate
- both `C1` and `C2` overlap the active `IRL` zone
- `C2` swept above `high(C1)`
  - `5128.53 > 5124.29`
- `C2` closed back inside the full range of `C1`
  - `5073.02 < 5103.21 < 5124.29`
- `EQ(C2) = 5113.47`
- `high(C3) < EQ(C2)`
  - `5107.91 < 5113.47`
- `close(C3) < low(C2)`
  - `5089.61 < 5098.41`
- strict expansion-quality check also passes
  - same-side wick fraction on `C3`:
    - `0.101337`

Interpretation:

- this is the surviving same-source MT5 example after enforcing real
  left-to-right `IRL` state
- the corrected integrated Type A bridge now behaves consistently with the
  existing `IRL/FVG` state model and runtime market ordering

## Confirmed FVG Invalidation Lifecycle Review

### Lifecycle Boundary

- review scope:
  - helper-layer `FVG / IRL` lifecycle
  - integrated `Type A` and integrated `Type B` after central lifecycle update
- lifecycle states now tracked explicitly:
  - `resting`
  - `reached`
  - `invalidated`
- current repo lifecycle policy:
  - bullish `FVG` becomes invalid for bullish use if a later candle closes
    below the lower bound
  - bearish `FVG` becomes invalid for bearish use if a later candle closes
    above the upper bound

Interpretation:

- `FVG` geometry remains separate from lifecycle
- same-bias integration logic now uses:
  - prior confirmed `IRL / FVG`
  - still `resting` before the sequence
  - no close-through invalidation during the sequence

### Confirmed March 20 Window Counts

- `bullish_internal_to_external_type_a_count = 0`
- `bearish_internal_to_external_type_a_count = 1`
- `bullish_internal_to_external_type_a_expansion_quality_count = 0`
- `bearish_internal_to_external_type_a_expansion_quality_count = 1`
- `bullish_internal_to_external_type_b_count = 0`
- `bearish_internal_to_external_type_b_count = 2`
- `fvg_candidate_count = 16`
- `fvg_resting_candidate_count = 4`
- `fvg_reached_candidate_count = 12`
- `fvg_invalidated_candidate_count = 9`

Interpretation:

- current same-window integrated `Type A` still has one surviving bearish match
- current same-window integrated `Type B` now has two surviving bearish matches
- invalidated `FVG`s are now counted explicitly instead of being hidden inside a
  generic non-resting bucket

### Integrated Type B Match 1

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG` from:
    - `2026-03-12 12:00 +05:00`
    - `2026-03-12 16:00 +05:00`
    - `2026-03-12 20:00 +05:00`
  - zone:
    - `5112.61 -> 5146.09`
  - state before sequence:
    - `resting`
- sequence:
  - `C1 = 2026-03-13 00:00 +05:00`
  - `C2 = 2026-03-13 04:00 +05:00`
- result:
  - `match`

Why it matches:

- the bearish `IRL` is still resting before `C1`
- both `C1` and `C2` overlap the active `IRL`
- `C2` sweeps above `high(C1)`
  - `5128.53 > 5124.29`
- `C2` then closes back down with a bearish body
  - `5103.21 < 5124.20`
- the same-side wick remains controlled
  - upper-wick fraction on `C2`:
    - `0.143758`
- neither `C1` nor `C2` closes above the upper boundary of the bearish `IRL`

Interpretation:

- this is a valid same-window bearish integrated `Type B`
- it also shares the same location as the surviving bearish integrated `Type A`
  path, but remains a separate faster branch

### Integrated Type B Match 2

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG` from:
    - `2026-03-18 08:00 +05:00`
    - `2026-03-18 12:00 +05:00`
    - `2026-03-18 16:00 +05:00`
  - zone:
    - `4898.97 -> 4977.17`
  - state before `C2`:
    - confirmed on `C1` close, then eligible from `C2`
- sequence:
  - `C1 = 2026-03-18 16:00 +05:00`
  - `C2 = 2026-03-18 20:00 +05:00`
- result:
  - `match`

Why it matches:

- the bearish `IRL` becomes defined on `C1` close
- `C2` is then the first eligible candle for the integrated `Type B` test
- `C2` touches the fresh bearish `IRL`
- `C2` sweeps above `high(C1)`
  - `4899.12 > 4898.97`
- `C2` then closes down strongly
  - `4817.91 < 4890.36`
- the same-side wick remains controlled
  - upper-wick fraction on `C2`:
    - `0.094723`

Interpretation:

- this confirms the fresh-on-`C1` bearish `IRL` path is real on same-source MT5
- the bridge no longer misses this valid runtime case

### Invalidated Bullish FVG Match 1

- candidate:
  - bullish `FVG`
  - zone:
    - `5199.15 -> 5213.95`
- confirmed at:
  - `2026-02-27 16:00 +05:00`
- later invalidated at:
  - `2026-03-03 12:00 +05:00`
- result:
  - `invalidated`

Why it invalidates:

- the invalidation candle closes below the lower boundary of the bullish `FVG`
  - lower boundary:
    - `5199.15`
  - invalidation candle close:
    - `5156.73`

Interpretation:

- this is a valid bullish close-through invalidation under the repo lifecycle
  policy
- it should no longer be treated as an active bullish `IRL`

### Invalidated Bearish FVG Match 1

- candidate:
  - bearish `FVG`
  - zone:
    - `5175.60 -> 5226.29`
- confirmed at:
  - `2026-03-03 16:00 +05:00`
- later invalidated at:
  - `2026-03-10 16:00 +05:00`
- result:
  - `invalidated`

Why it invalidates:

- the invalidation candle closes above the upper boundary of the bearish `FVG`
  - upper boundary:
    - `5226.29`
  - invalidation candle close:
    - `5227.60`

Interpretation:

- this is a valid bearish close-through invalidation under the repo lifecycle
  policy
- it should no longer be reused as an active bearish `IRL`

## Confirmed Full 500-Bar Integrated Type B Review

### Review Boundary

- source:
  - preserved MT5 raw snapshot
  - `xauusd_4h_mt5_raw_2026_03_19.csv`
- review scope:
  - integrated `IRL -> Type B`
  - full `500`-bar same-source extraction
- required boundary:
  - `IRL / FVG` must already exist in left-to-right time
  - it must still be directionally valid for same-bias use
  - the integrated pair must respect the current close-through invalidation
    policy

### Confirmed Full-Sample Counts

- total integrated `Type B` matches:
  - `8`
- bullish integrated `Type B` matches:
  - `3`
- bearish integrated `Type B` matches:
  - `5`

Interpretation:

- integrated `Type B` is real on the broader same-source sample
- it remains sparse enough to be selective
- the current left-to-right lifecycle filter is not overcounting aggressively

### Integrated Type B 500-Bar Match 1

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG`
  - zone:
    - `4226.13 -> 4229.37`
  - confirmed at:
    - `2025-12-02 04:00 +05:00`
- sequence:
  - `C1 = 2025-12-02 04:00 +05:00`
  - `C2 = 2025-12-02 08:00 +05:00`
- result:
  - `match`

Interpretation:

- this is a valid bearish `Type B` where the active bearish `IRL` is touched on
  `C2`
- `C2` sweeps above `high(C1)` and then rejects sharply lower with a very small
  same-side wick

### Integrated Type B 500-Bar Match 2

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG`
  - zone:
    - `4195.66 -> 4197.85`
  - confirmed at:
    - `2025-12-08 20:00 +05:00`
- sequence:
  - `C1 = 2025-12-09 00:00 +05:00`
  - `C2 = 2025-12-09 04:00 +05:00`
- result:
  - `match`

Interpretation:

- both `C1` and `C2` overlap the active bearish `IRL`
- `C2` then completes the bearish reversal-to-expansion behavior cleanly

### Integrated Type B 500-Bar Match 3

- classification:
  - bullish integrated `IRL -> Type B`
- active `IRL`:
  - bullish `FVG`
  - zone:
    - `4207.01 -> 4223.97`
  - confirmed at:
    - `2025-12-11 00:00 +05:00`
- sequence:
  - `C1 = 2025-12-11 04:00 +05:00`
  - `C2 = 2025-12-11 08:00 +05:00`
- result:
  - `match`

Interpretation:

- this is the first confirmed bullish full-sample integrated `Type B`
- both candles overlap the active bullish `IRL`
- `C2` sweeps below `low(C1)` and then reclaims upward with a controlled lower
  wick

### Integrated Type B 500-Bar Match 4

- classification:
  - bullish integrated `IRL -> Type B`
- active `IRL`:
  - bullish `FVG`
  - zone:
    - `4449.04 -> 4474.93`
  - confirmed at:
    - `2025-12-23 04:00 +05:00`
- sequence:
  - `C1 = 2025-12-23 04:00 +05:00`
  - `C2 = 2025-12-23 08:00 +05:00`
- result:
  - `match`

Interpretation:

- the relevant touch occurs on `C2`
- `C2` sweeps below `low(C1)` and recovers bullishly
- the lower wick remains just inside the current threshold, so this is a valid
  but less comfortable bullish `Type B`

### Integrated Type B 500-Bar Match 5

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG`
  - zone:
    - `4421.49 -> 4445.40`
  - confirmed at:
    - `2025-12-29 16:00 +05:00`
- sequence:
  - `C1 = 2026-01-05 08:00 +05:00`
  - `C2 = 2026-01-05 12:00 +05:00`
- result:
  - `match`

Interpretation:

- both sequence candles overlap the active bearish `IRL`
- `C2` sweeps above `high(C1)` and then closes back down cleanly

### Integrated Type B 500-Bar Match 6

- classification:
  - bullish integrated `IRL -> Type B`
- active `IRL`:
  - bullish `FVG`
  - zone:
    - `4892.76 -> 4912.94`
  - confirmed at:
    - `2026-02-18 08:00 +05:00`
- sequence:
  - `C1 = 2026-02-18 08:00 +05:00`
  - `C2 = 2026-02-18 12:00 +05:00`
- result:
  - `match`

Interpretation:

- this is another valid bullish integrated `Type B`
- the key interaction occurs on `C2`
- `C2` sweeps below `low(C1)` and then expands upward strongly

### Integrated Type B 500-Bar Match 7

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG`
  - zone:
    - `5112.61 -> 5146.09`
  - confirmed at:
    - `2026-03-12 20:00 +05:00`
- sequence:
  - `C1 = 2026-03-13 00:00 +05:00`
  - `C2 = 2026-03-13 04:00 +05:00`
- result:
  - `match`

Interpretation:

- both candles overlap the active bearish `IRL`
- this is the same region that also supports the slower bearish integrated
  `Type A`
- as a faster branch, it remains a valid bearish integrated `Type B`

### Integrated Type B 500-Bar Match 8

- classification:
  - bearish integrated `IRL -> Type B`
- active `IRL`:
  - bearish `FVG`
  - zone:
    - `4898.97 -> 4977.17`
  - confirmed at:
    - `2026-03-18 16:00 +05:00`
- sequence:
  - `C1 = 2026-03-18 16:00 +05:00`
  - `C2 = 2026-03-18 20:00 +05:00`
- result:
  - `match`

Interpretation:

- the bearish `IRL` is freshly confirmed on `C1` close
- `C2` then becomes the first eligible candle and forms a valid bearish
  reversal-to-expansion move
- this confirms the fresh-on-`C1` eligibility path is working on real MT5 data
