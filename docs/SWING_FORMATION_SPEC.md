# Swing Formation Spec

## Purpose

This spec defines `swing formation` in Garrett's currently reviewed framework.

It exists because swing formation is not the same thing as:

- a generic local swing point
- a key level
- the trade candle itself

Swing formation is the confirmation object that sits between:

- key level / context
and
- expansion-candle execution

## Direct Source-Derived Doctrine

From the reviewed transcript:

- the market cannot reverse without a swing formation
- a `candle 2 closure` is when candle `2` closes back inside candle `1`'s
  range
- once that closure exists, mark equilibrium of the previous candle's range
- the acceptable half of that range is used to judge the low of candle `3`
- this is a mechanical way to measure wick size
- expansion candles have small wicks
- reversal candles have large wicks
- the current reviewed `candle 2` reversal-to-expansion structure is the same
  core reversal logic, with wick size being the discriminator
- in the `candle 3 closure` case, we do not get a `C2` closure
  - meaning we do not get the Type A `C2` closure back inside `C1` range
- prior to `C3` open, reversal cannot be anticipated in that case
- the `C3 closure` forms only after candle `3` closes strongly over the body of
  candle `2`
- once that `C3` closure exists, mark `EQ(C3)` and seek continuation in `C4`

## Current Reviewed Reading

At the current repo doctrine level, Garrett swing formation is the reversal /
confirmation structure that appears at a valid key level before the tradeable
expansion or continuation candle.

Current organizing abstraction:

- swing formation is organized around `C2` and `C3`
- `C2` currently has two reviewed types
- `C3` currently has one reviewed closure type
- all three currently reviewed types require `C2` to sweep the relevant edge of
  `C1`
- the exact path determines which later candle becomes actionable

At least three currently reviewed swing-formation types now exist:

### Type A - C2 Closure -> C3 Expansion

In the standard currently reviewed candle grammar:

1. price reaches a key level
2. `C2` sweeps beyond the relevant edge of `C1`
3. `C2` closes back inside `C1` range
4. `EQ(C2)` measures wick quality mechanically
5. `C3` must preserve the correct half of `C2`
6. `C3` must then expand beyond `C2`

So the standard swing-formation flow is:

- key level reached
- `C2` closure
- wick-quality check through `EQ(C2)`
- `C3` support
- `C3` expansion

### Type B - C2 Reversal To Expansion

In the second currently reviewed case:

1. `C1` reaches the key level
2. `C1` is not the trade candle
3. `C2` sweeps the relevant edge of `C1`
4. `C2` reverses from that sweep
5. `C2` also expands away from that reversal
6. the key discriminator is smaller wick structure

So in this compressed case, reversal and expansion occur in `C2` itself.

### Type C - C3 Closure

In the third currently reviewed case:

1. `C1` or `C2` reaches the key level
2. `C2` sweeps the relevant edge of `C1`
3. no Type A `C2` closure forms back inside `C1` range
4. prior to `C3` open, reversal cannot be anticipated
5. swing formation only exists after `C3` closes strongly
6. that strong `C3` closure is mechanically defined as closing over the body of
   `C2`
7. after that closure, `EQ(C3)` becomes the active continuation boundary for
   `C4`

So in this delayed-confirmation case, the formation completes only at `C3`
close and continuation is then sought in `C4`.

For the current reviewed Type C reading, what matters is:

- `C2` sweeps the relevant edge of `C1`
- `C2` does not produce a Type A close back inside `C1` range
- `C3` closes strongly over the body of `C2`

`C2` itself does not currently require a locked bullish or bearish body color
for Type C.

## Relationship To Key Level

Swing formation is not the key level itself.

Current boundary:

- key level = location / context
- swing formation = confirmation at that location
- expansion or continuation candle = tradeable event after confirmation

## Relationship To Generic Swing Points

Swing formation is also not the same thing as a generic local swing point.

Current boundary:

- local swing point = neutral chart geometry
- Garrett swing formation = doctrinal reversal / confirmation object

This distinction is important for code architecture and doctrine hygiene.

## Relationship To Wick Size

The current reviewed doctrine explicitly ties swing formation to wick quality.

Why `EQ` is marked:

- it is a mechanical way to measure wick size

Current reviewed interpretation:

- expansion-like behavior has controlled / smaller wick structure
- reversal-style behavior with larger wick structure is weaker for the
  expansion trade Garrett wants

This is the doctrinal reason the repo already uses:

- `EQ(C2)` to qualify `C3` in Type A
- wick size to qualify `C2` itself in Type B
- `EQ(C3)` to qualify `C4` in Type C

So the currently reviewed chain is:

- `C2` can be:
  - closure-side event in Type A
  - reversal-to-expansion candle in Type B
- `C3` can be:
  - expansion-qualified event in Type A
  - closure-side event in Type C
- `C4` = continuation-qualified event after the appropriate predecessor state

In Type C specifically:

- the decisive object is the strong `C3` body close over `C2`
- `C2` color is not the current locked discriminator

## Relationship To Entry

Current reviewed execution reading:

- Garrett does not blindly trade the key level
- Garrett waits for swing formation there
- Garrett then trades the reviewed expansion / continuation candle of that
  formation type

In the current reviewed grammar:

- `C1` is not the trade candle
- Type A:
  - `C2` belongs to swing formation
  - `C3` is the tradeable expansion candle
- Type B:
  - `C2` belongs to swing formation
  - `C2` can itself be the tradeable expansion candle
- Type C:
  - `C3` is the closure / formation candle
  - `C4` becomes the next reviewed continuation / expansion candidate after the
    formation exists

## What Is Locked

Locked at the current doctrine level:

- the market cannot reverse without a swing formation
- swing formation is organized around `C2` and `C3`
- all three currently reviewed types require `C2` to sweep the relevant edge of
  `C1`
- `EQ` is used mechanically to measure wick size
- swing formation is the confirmation object between key level and expansion /
  continuation
- swing formation is not equivalent to a generic local swing point
- the currently reviewed swing-formation logic is a reversal-to-expansion
  structure whose key discriminator is wick quality
- at least three currently reviewed swing-formation types exist:
  - Type A: `C2 closure -> C3 expansion`
  - Type B: `C2 reversal to expansion`
  - Type C: `C3 closure -> C4 continuation candidate`

## What Is Not Yet Locked

Not yet locked:

1. a final exhaustive taxonomy of all Garrett swing formations
2. whether later material adds other swing-formation variants beyond the
   three currently reviewed types
3. whether SMT must be present for a swing formation to become tradeable in all
   later cases
4. exact execution details inside the actionable candle
5. exact machine-ready bullish and bearish formulas for `C3` closing over the
   body of `C2`

## Implementation Status

Implementation status: partially implemented.

Current code already implements:

- Type A components:
  - `C2` closure
  - `C3` support
  - `C3` expansion
  - `C4` continuation candidate
- Type B components:
  - isolated bullish and bearish `C2 reversal to expansion` primitives
- Type C components:
  - isolated bullish and bearish `C3 closure` primitives
  - separate bullish and bearish `C4` continuation candidates after `C3`
    closure

What is not implemented yet:

- a merged top-level swing-formation detector across Type A, Type B, and Type C
- later SMT-integrated confirmation logic
