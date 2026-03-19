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

For this project, Garrett-specific use is now locked to this same baseline by:

- source-consistent reviewed diagrams
- user confirmation from prior Garrett study

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

- `IRL` is now directly defined as a fair value gap
- so `FVG` is not merely associated with `IRL`
- it is the current direct `IRL` object

So the current contextual hierarchy is:

1. `Universal Model`
2. `Key Levels`
3. `IRL / ERL`
4. `FVG` as the current direct `IRL` object

This means `FVG` is currently important because it is the key level price is
expected to retrace into before the candle-sequence execution logic becomes
relevant.

## What Is Locked

Locked in the current repo doctrine:

- `FVG` is the currently discussed `IRL` key-level subtype in the universal
  model context
- in the currently reviewed defining material, `IRL` is directly defined as a
  fair value gap
- `FVG` should be treated as a separate doctrine object from:
  - `IRL`
  - `ERL`
  - candle execution primitives
- Garrett's current `FVG` usage for this project follows the standard
  three-candle baseline definition
- current boundaries are wick-based:
  - bullish zone = `high(c1)` to `low(c3)`
  - bearish zone = `high(c3)` to `low(c1)`
- equality does not count as a valid gap:
  - bullish requires `low(c3) > high(c1)`
  - bearish requires `high(c3) < low(c1)`

## What Is Not Yet Locked

Not yet locked:

1. whether Garrett applies a directional filter to the middle candle
2. whether Garrett defines mitigation / fill in a specific way
3. whether Garrett uses additional filters such as minimum size or context
4. how `FVG` should later be ranked or filtered inside the broader universal
   model context

## Implementation Status

Implementation status: locked and ready for baseline detection code.

Code may implement the locked baseline `FVG` detector now, but must not add
extra filters unless they are explicitly labeled as research hypotheses.

Helper-layer candidate/state tracking beyond baseline geometry should remain
separate. The current repo uses:

- `IRL_MECHANICAL_PROXY_SPEC.md`

for research/helper classification such as:

- whether a detected `FVG` is still resting
- whether price has already reached that gap

## Repo Lifecycle Policy

The repo now separates:

1. baseline `FVG` geometry
2. helper-layer lifecycle state
3. directional eligibility for same-bias use

Current helper/research lifecycle states are:

- `resting`
- `reached`
- `invalidated`

Current repo lifecycle policy for directional invalidation is:

- bullish `FVG` becomes invalid for bullish use if a later candle closes below
  the lower boundary
- bearish `FVG` becomes invalid for bearish use if a later candle closes above
  the upper boundary

This is a repo lifecycle / eligibility policy used by integration and
research-layer code. It should not be overstated as a universal industry law or
as fully locked Garrett doctrine unless later source material explicitly does
so.

## Non-goals

This spec does not yet define:

- mitigation logic
- fill logic
- entry logic by itself
- target logic by itself
