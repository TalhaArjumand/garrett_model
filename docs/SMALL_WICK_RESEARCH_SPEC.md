# Small Wick Research Spec

## Purpose

This note defines a shared research-layer meaning for `small wick`.

It exists to keep the current expansion-quality checks consistent across:

- `Case B`
- base `Type C` strict `C4`
- rare `Type C` strict `C4`

This is a research helper, not locked Garrett doctrine.

## Base Mechanical Definition

`small wick` is direction-aware and range-normalized.

### Bullish candle

- same-side wick = `lower_wick`
- same-side wick fraction = `lower_wick / range`

### Bearish candle

- same-side wick = `upper_wick`
- same-side wick fraction = `upper_wick / range`

This is the current shared mechanical base.

## Hard-Cap Rule

The current strict pattern checks use a hard-cap rule:

- pass if `same_side_wick_fraction <= threshold`

Current research default:

- `threshold = 0.25`

This default is:

- explicit
- configurable
- not locked Garrett doctrine

## Statistical Layer

For stronger research, the repo also defines a contextual percentile view.

For a target candle, compare its same-side wick fraction against a prior
same-direction reference population on the same symbol and timeframe.

Current percentile definition:

- percentile = fraction of prior comparable candles whose same-side wick
  fraction is less than or equal to the target candle's fraction

Interpretation:

- lower percentile = smaller wick relative to the recent comparable population

## Combined Research Rule

A stricter contextual research rule can require both:

- `same_side_wick_fraction <= hard_cap`
- `same_side_wick_percentile <= percentile_cap`

Current research defaults:

- `hard_cap = 0.25`
- `percentile_cap = 0.25`

This combined rule is implemented as a reusable helper, but it is not yet wired
into the strict pattern detectors by default.

## Body Fraction

The repo also exposes:

- `body_fraction = body_size / range`

This is currently descriptive only.

It is available for later expansion-quality research, but it is not yet a hard
filter in the strict path detectors.

## Edge Cases

- zero-range candle: reject
- doji candle: reject for same-side wick logic
- future reference candles: reject in percentile logic
- mixed symbol/timeframe reference sets: reject
- equality boundary: `<=` passes

## Current Use

The current production research path is:

- strict pattern detectors use the shared hard-cap helper

The current optional research path is:

- use the contextual percentile helper for deeper analysis and later threshold
  tuning
