# FVG Spec

## Purpose

This spec isolates `FVG` as its own doctrine object so it does not get mixed
up with:

- the universal model framework
- `IRL / ERL` range-liquidity structure
- candle execution primitives

At this stage, `FVG` is being defined as a key-level object, not as a full
trade system by itself.

## Evidence Posture

There is no single cross-industry official standard for `FVG`.

However, current official vendor documentation from platforms and tool vendors
does converge on a common core definition:

- `FVG` is a three-candle imbalance / inefficiency
- bullish and bearish forms both exist
- the imbalance is defined between the first and third candles

This common vendor definition is useful as a baseline reference, but it is not
automatically identical to Garrett-specific doctrine unless Garrett's own
material confirms it directly.

The current baseline in this spec was verified against:

- LuxAlgo official indicator documentation
- TrendSpider official blog / scanner documentation

## Common Vendor Baseline Definition

The current common baseline definition is:

- `FVG` is a three-candle imbalance where price moves aggressively enough that
  the first and third candles do not overlap properly

### Bullish FVG

Common vendor baseline:

- `low(c3) > high(c1)`

The imbalance zone is the price interval between:

- lower boundary: `high(c1)`
- upper boundary: `low(c3)`

### Bearish FVG

Common vendor baseline:

- `high(c3) < low(c1)`

The imbalance zone is the price interval between:

- lower boundary: `high(c3)`
- upper boundary: `low(c1)`

## Optional Vendor Filters

Some official vendor implementations add extra filters, for example:

- the middle candle must be directionally aligned with the gap
- the gap must exceed a threshold
- mitigation / fill tracking
- volatility or volume filters

These are not universally standard and are not yet locked for this project.

Current vendor examples:

- LuxAlgo's published indicator rules add:
  - middle-candle close confirmation relative to `c1`
  - a threshold filter on gap size
- TrendSpider's official scanner example adds:
  - directional pressure from the middle candle
  - a configurable size / pressure condition

So the shared baseline is the three-candle imbalance itself, while directional
and threshold filters should be treated as implementation variants unless
Garrett explicitly locks them.

## Current Garrett-Specific Role

Within the currently extracted universal-model layer:

- `FVG` is the current key-level subtype being discussed inside `IRL`

So the current contextual hierarchy is:

1. `Universal Model`
2. `Key Levels`
3. `IRL / ERL`
4. `FVG` as the currently discussed `IRL` key-level object

This means `FVG` is currently important because it is the key level price is
expected to retrace into before the candle-sequence execution logic becomes
relevant.

## What Is Locked

Locked in the current repo doctrine:

- `FVG` is the currently discussed `IRL` key-level subtype in the universal
  model context
- `FVG` should be treated as a separate doctrine object from:
  - `IRL`
  - `ERL`
  - candle execution primitives

## What Is Not Yet Locked

Not yet locked:

1. whether Garrett uses the common three-candle vendor definition exactly
2. whether Garrett requires wick-based boundaries, body-based boundaries, or
   another refinement
3. whether Garrett applies a directional filter to the middle candle
4. whether Garrett defines mitigation / fill in a specific way
5. whether Garrett uses additional filters such as minimum size or context
6. exact machine-ready Garrett-specific `FVG` detection logic

## Implementation Status

Implementation status: not started.

No code should assume a final Garrett-specific `FVG` detector until more
direct doctrinal evidence is extracted.

## Non-goals

This spec does not yet define:

- final Garrett-specific `FVG` code
- mitigation logic
- fill logic
- entry logic by itself
- target logic by itself
