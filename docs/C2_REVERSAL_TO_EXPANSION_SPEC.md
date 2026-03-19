# C2 Reversal To Expansion Spec

## Purpose

This spec defines the second currently reviewed candle-formation case in
Garrett's framework: `C2 reversal to expansion`.

It exists because the currently reviewed material no longer supports only one
expansion-entry path.

Current reviewed cases are now:

1. `C2 closure -> C3 expansion`
2. `C2 reversal to expansion`

## Direct Source-Derived Doctrine

From the reviewed transcript and diagram:

- `candle 2 reversal to expansion` is the same core thing as a reversal candle
- the difference is wick size
- a small wick allows price to reverse and expand in the same candle
- when candle `1` hits a key level and does not already reverse, reversal must
  occur from its high or low
- if the next candle forms a small wick and supports expansion away from that
  reversal, participation can occur in that same candle

## Current Reviewed Reading

At the current repo doctrine level, this is the compressed swing-formation
variant.

In this case:

- `C1` reaches the key level
- `C1` itself is not the trade candle
- `C2` sweeps the relevant edge of `C1`
- `C2` reverses from that sweep
- `C2` also expands away from that reversal
- the key discriminator is small wick structure

So unlike the standard `C2 closure -> C3 expansion` case, reversal and
expansion are compressed into `C2` itself.

## Current Reviewed Contrast With C2 Closure

Current reviewed difference between the two cases:

### Standard Case

- `C2` is a larger-wick reversal / closure-side event
- `C3` is the later small-wick expansion candle

### Compressed Case

- `C2` reverses and expands in the same candle
- `C2` has the smaller wick structure that supports expansion away from the
  reversal

So the difference is not a different species of logic.
It is the same reversal-to-expansion logic compressed into one candle because
wick structure allows it.

## What Is Locked

Locked at the current reviewed doctrine level:

- `C1` is not the primary trade candle
- `C2 reversal to expansion` is a second currently reviewed candle-formation
  case
- `C2` must sweep the relevant edge of `C1`
- in this case, `C2` can be the tradeable expansion candle
- the discriminator between standard reversal and reversal-to-expansion is wick
  size
- a smaller wick supports participation in `C2` because it supports expansion
  away from the reversal

## What Is Not Yet Locked

Not yet locked:

1. an exact mechanical threshold for what counts as a sufficiently small wick
2. whether `C1` may only come close to key level rather than touching it
3. a final machine-ready detector for this compressed case
4. whether Garrett gives additional filters before participating in `C2`
5. the exact bullish / bearish mirror wording beyond the current reviewed
   symmetry assumptions

## Implementation Status

Implementation status: partially implemented.

Current implementation includes:

- isolated bullish and bearish Case B primitives
- explicit research wick-threshold parameter
- real-data candidate counting

The implementation boundary is documented separately in:

- `C2_REVERSAL_TO_EXPANSION_IMPLEMENTATION_NOTES.md`

What remains open:

- final machine-ready Garrett threshold for wick size
- merged swing-formation selection across multiple cases
- trade-selection logic on top of this primitive
