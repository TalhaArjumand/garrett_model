# Local Swing Point Helper Spec

## Purpose

This spec defines neutral local swing-point geometry.

It exists as a helper-layer object for:

- structural annotation
- liquidity mapping
- later research proxies

It is **not** equivalent to Garrett's swing formation doctrine.

## Source Scope

Source scope: single reviewed liquidity / swing-point teaching video.

Status: generic swing/liquidity layer.

Boundary: not equivalent to Garrett swing formation doctrine.

## Definition

For three consecutive candles `A, B, C` on the same timeframe:

### Local Swing High

`B` is a local swing high if:

- `high(B) > high(A)`
- `high(B) > high(C)`

### Local Swing Low

`B` is a local swing low if:

- `low(B) < low(A)`
- `low(B) < low(C)`

These are generic local extremum rules.

## Confirmation

A local swing point is only confirmed after the right-neighbor candle closes.

That means:

- local swing high `B` is only confirmed after `C` closes
- local swing low `B` is only confirmed after `C` closes

## Interpretation Boundary

These local swing points are:

- generic chart geometry
- useful for helper-layer analysis

They are not, by themselves:

- Garrett swing formation
- Garrett confluence
- entry logic

## What Is Locked

Locked in the current repo helper layer:

- local swing high geometry
- local swing low geometry
- confirmation only after the right-neighbor candle closes

## What Is Not Yet Locked

Not yet locked:

1. whether wider lookback swing logic is needed
2. whether equal highs/lows should invalidate or merge with local swings
3. whether local swing points are always relevant for ERL in Garrett doctrine
4. how multiple nearby swing points should be ranked

## Implementation Status

Implementation status: not started.

If implemented later, this should remain a helper-layer primitive rather than a
Garrett-specific execution doctrine object.

## Non-goals

This spec does not yet define:

- Garrett swing formation
- liquidity rules by itself
- ERL doctrine by itself
- range selection by itself
