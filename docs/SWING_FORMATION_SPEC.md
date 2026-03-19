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
- after candle `3` expands, continuation in candle `4` depends on candle `3`
  closing beyond candle `2`'s extreme and preserving the correct half of candle
  `3`

## Current Reviewed Reading

At the current repo doctrine level, Garrett swing formation is the reversal /
confirmation structure that appears at a valid key level before the tradeable
expansion candle.

At least two currently reviewed cases now exist:

### Case 1 - Standard Delayed Expansion

In the standard currently reviewed candle grammar:

1. price reaches a key level
2. `C2` closes back inside `C1` range
3. `EQ(C2)` measures wick quality mechanically
4. `C3` must preserve the correct half of `C2`
5. `C3` must then expand beyond `C2`

So the standard swing-formation flow is:

- key level reached
- `C2` closure
- wick-quality check through `EQ(C2)`
- `C3` support
- `C3` expansion

### Case 2 - Compressed C2 Reversal To Expansion

In the second currently reviewed case:

1. `C1` reaches the key level
2. `C1` is not the trade candle
3. `C2` reverses from the relevant edge of `C1`
4. `C2` also expands away from that reversal
5. the key discriminator is smaller wick structure

So in this compressed case, reversal and expansion occur in `C2` itself.

## Relationship To Key Level

Swing formation is not the key level itself.

Current boundary:

- key level = location / context
- swing formation = confirmation at that location
- expansion candle = tradeable event after confirmation

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

- `EQ(C2)` to qualify `C3`
- `EQ(C3)` to qualify `C4`

So the currently reviewed chain is:

- `C2` can be:
  - reversal-side closure event in the standard case
  - reversal-to-expansion candle in the compressed case
- `C3` = expansion-qualified event in the standard delayed-expansion case
- `C4` = continuation-qualified event

## Relationship To Entry

Current reviewed execution reading:

- Garrett does not blindly trade the key level
- Garrett waits for swing formation there
- Garrett then trades the expansion candle

In the current reviewed grammar:

- `C1` is not the trade candle
- `C2` belongs to swing formation in both reviewed cases
- `C3` is the tradeable expansion candle in the standard delayed-expansion case
- `C2` can itself be the tradeable expansion candle in the compressed case
- `C4` is later continuation context

## What Is Locked

Locked at the current doctrine level:

- the market cannot reverse without a swing formation
- `C2` closure is part of swing formation
- `EQ` is used mechanically to measure wick size
- swing formation is the confirmation object between key level and expansion
  candle
- swing formation is not equivalent to a generic local swing point
- the currently reviewed swing-formation logic is a reversal-to-expansion
  structure whose key discriminator is wick quality
- at least two currently reviewed swing-formation cases exist:
  - standard `C2 closure -> C3 expansion`
  - compressed `C2 reversal to expansion`

## What Is Not Yet Locked

Not yet locked:

1. a final exhaustive taxonomy of all Garrett swing formations
2. whether later material adds other swing-formation variants beyond the
   two currently reviewed cases
3. whether SMT must be present for a swing formation to become tradeable in all
   later cases
4. exact execution details inside the expansion candle

## Implementation Status

Implementation status: doctrine only.

Current code already implements parts of this formation through:

- `C2` closure
- `C3` support
- `C3` expansion
- `C4` continuation candidate

But the repo does not yet contain a separate top-level swing-formation engine
or later SMT-integrated confirmation logic.
