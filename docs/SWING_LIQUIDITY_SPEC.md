# Swing Liquidity Spec

## Purpose

This spec defines liquidity resting around local swing points.

It exists to capture the generic swing-derived liquidity layer described in the
reviewed teaching material, without confusing it with Garrett's separate swing
formation doctrine.

## Source Scope

Source scope: single reviewed liquidity / swing-point teaching video.

Status: generic swing/liquidity layer.

Boundary: not equivalent to Garrett swing formation doctrine.

## Locked Predecessor Context

This spec depends on the helper-layer geometry defined in:

- `LOCAL_SWING_POINT_HELPER_SPEC.md`

## Definition

### Sell-Side Liquidity

Sell-side liquidity rests below a confirmed swing low.

### Buy-Side Liquidity

Buy-side liquidity rests above a confirmed swing high.

## Dynamic Update Behavior

Once a swing high or swing low is taken, focus shifts to the next obvious
relevant level.

This means liquidity mapping is dynamic:

- once buy-side liquidity is taken, that specific buy-side pool is no longer
  the active focus
- once sell-side liquidity is taken, that specific sell-side pool is no longer
  the active focus

## Relative Equal Highs And Lows

The reviewed teaching material also states:

- relatively equal highs can be treated together as one buy-side liquidity area
- relatively equal lows can be treated together as one sell-side liquidity area

At the current doctrine state, this grouping concept is locked at a qualitative
level only.

## Obvious Outside-Of-Range Focus

The reviewed teaching material emphasizes focusing on:

- the obvious highs
- the obvious lows
- especially those on the outside of the range

This is currently a qualitative prioritization rule, not a final mechanical
ranking algorithm.

## What Is Locked

Locked in the current repo helper layer:

- buy-side liquidity rests above confirmed swing highs
- sell-side liquidity rests below confirmed swing lows
- relatively equal highs/lows can be grouped as one liquidity area
- once a level is taken, focus shifts to the next obvious level
- obvious outside-of-range highs/lows deserve priority attention

## What Is Not Yet Locked

Not yet locked:

1. the tolerance for `relatively equal`
2. timeframe priority rules
3. a fully mechanical ranking method for `obvious` highs/lows
4. how this swing-liquidity layer should be subordinated to the full universal
   model in final machine-ready form

## Implementation Status

Implementation status: not started.

If implemented later, this should remain a neutral swing-liquidity helper layer
unless Garrett directly promotes specific pieces into core doctrine.

## Non-goals

This spec does not yet define:

- final Garrett ERL selection
- final IRL selection
- swing formation doctrine
- target logic by itself
