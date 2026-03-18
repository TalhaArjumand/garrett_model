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

So the helper layer must distinguish between:

- a historical swing-derived liquidity object that existed
- a liquidity pool that is still resting now

A later breach above a swing high takes that buy-side pool.

A later breach below a swing low takes that sell-side pool.

## Relative Equal Highs And Lows

The reviewed teaching material also states:

- relatively equal highs can be treated together as one buy-side liquidity area
- relatively equal lows can be treated together as one sell-side liquidity area

At the current doctrine state, this grouping concept is locked at a qualitative
level only.

The reviewed examples show two common forms:

### Form 1: Multiple Swing Points Very Close Together

Relatively equal highs or lows can appear as:

- two different swing points
- whose highs are very close together
  or
- whose lows are very close together

This still forms one grouped liquidity area.

Important boundary:

- if one of the earlier highs / lows is already taken before the later clustered
  level forms, that grouped liquidity area should not be treated as still
  resting equal-high / equal-low liquidity

### Form 2: Clustered Highs Or Lows

Relatively equal highs or lows can also appear as:

- multiple highs clustered together
  or
- multiple lows clustered together

This also forms one grouped liquidity area.

## Old Highs And Old Lows

Old highs and old lows refer to prior standout swing points.

At the current reviewed doctrine level:

- an old high refers to a previous high where a single swing high stands out
- an old low refers to a previous low where a single swing low stands out

So the current liquidity layer includes both:

- grouped liquidity from relatively equal highs / lows
- single standout old highs / old lows

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

Implementation status: partially implemented in helper / research code.

Current implementation includes:

- confirmed local swing-point detection
- swing-derived liquidity candidate extraction
- explicit taken / resting state tracking

This still remains a neutral swing-liquidity helper layer unless Garrett
directly promotes specific pieces into core doctrine.

## Non-goals

This spec does not yet define:

- final Garrett ERL selection
- final IRL selection
- swing formation doctrine
- target logic by itself
