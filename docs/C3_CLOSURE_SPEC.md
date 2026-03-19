# C3 Closure Spec

## Purpose

This spec defines the third currently reviewed swing-formation type in
Garrett's framework: `C3 closure`.

It exists because the reviewed doctrine now supports a delayed-confirmation
case that is not reducible to either:

- `C2 closure -> C3 expansion`
- or `C2 reversal to expansion`

## Direct Source-Derived Doctrine

From the reviewed transcript:

- `C1` can hit a key level, or `C2` can hit a key level
- in this case, we do not get a `C2` closure
  - meaning we do not get the Type A `C2` closure condition where `C2` closes
    back inside the full range of `C1`
- `C3` expands away from `C2`'s low without taking that low out in the bullish
  example
- prior to `C3` open, the reversal cannot be anticipated because there is no
  closure yet
- the reversal can only be anticipated after the swing formation actually forms
- a strong `C3` closure is mechanically defined as closing over the body of
  candle `2`
- once that closure exists, mark `EQ(C3)` and seek continuation in `C4` with
  the low in the upper half of `C3` range in the bullish example

## Current Reviewed Reading

At the current repo doctrine level, this is the delayed-confirmation
swing-formation type.

In this case:

- the key level has already been reached by `C1` or `C2`
- `C2` does not produce a valid Type A `C2` closure back inside `C1` range
- the formation is not knowable before `C3` closes
- `C3` becomes the candle that completes the swing formation
- `EQ(C3)` then becomes the active continuation boundary for `C4`

So unlike the standard delayed-expansion case, `C3` is not merely the already
anticipated expansion candle. In this case, `C3` is the candle that finally
creates the actionable confirmation.

## What Is Locked

Locked at the current reviewed doctrine level:

- `C3 closure` is a third reviewed swing-formation type
- this type can arise when `C1` or `C2` reaches the key level
- a valid Type A `C2` closure is absent in this case
- that means `C2` does not close back inside the full range of `C1`
- reversal cannot be anticipated before `C3` closes
- the reviewed mechanical definition is:
  - strong `C3` closure over the body of `C2`
- after that closure, `EQ(C3)` is marked for `C4` continuation / expansion
  seeking

## What Is Not Yet Locked

Not yet locked:

1. exact machine-ready bullish and bearish body-closure rules
2. whether `C1` and `C2` key-level contact are equally valid in all cases
3. whether `C4` in this branch should already be treated as the trade candle or
   only as the next continuation candidate
4. whether additional confluences must sit on top of this branch before it is
   tradeable

## Implementation Status

Implementation status: doctrine only.

Current code does not yet implement a separate `C3 closure` primitive.
