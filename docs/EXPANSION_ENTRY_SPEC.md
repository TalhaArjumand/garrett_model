# Expansion Entry Spec

## Purpose

This spec records the current Garrett execution doctrine for what actually gets
traded after price reaches a key level.

The important distinction is:

- key level is the watch location
- swing formation is the qualification event
- the expansion candle is the trade candle

This prevents the repo from collapsing:

- key level
- setup formation
- trade execution

into the same object.

## Locked Predecessor Context

Already locked elsewhere in the repo:

- `IRL` / `ERL` are the current key-level objects
- candle formation is watched once price reaches a key level
- `C2` closure is part of Garrett swing formation
- `C3` support and expansion confirmation qualify the move away from key level

## Current Doctrine Statement

At the current doctrinal level:

1. price reaches a key level
2. Garrett swing formation appears there
3. the trade is taken on the expansion candle

In the currently locked candle grammar, this means:

- `C1` is not the trade candle
- in the standard delayed-expansion case:
  - `C2` belongs to the swing-formation / qualification side
  - `C3` is the expansion candle
- in the compressed `C2 reversal to expansion` case:
  - `C2` itself can be the tradeable expansion candle
- Garrett trades the expansion candle of the reviewed case, not the raw
  key-level touch candle

## Execution Flow

The current execution reading is:

1. identify the relevant key level
2. wait for price to reach that level
3. require Garrett swing formation there
   - currently represented by either:
     - `C2` closure and downstream qualification
     - or `C2` reversal to expansion
4. trade the expansion candle
   - currently:
     - `C3` in the standard delayed-expansion case
     - `C2` in the compressed case

So the current doctrinal flow is:

- key level -> swing formation -> expansion candle trade

## What This Clarifies

This doctrine clarification means:

- `C1` is not the primary trade candle
- `C3` is not just confirmation in the abstract in the standard case
- the actual trade candle is the candle that performs the reviewed expansion
- `C4` is not the primary entry candle in this flow

## Relationship to C4

`C4` remains a later continuation layer.

That means:

- `C4` is downstream continuation behavior after the trade candle already
  exists
- the trade candle can currently be:
  - `C3` in the standard delayed-expansion case
  - `C2` in the compressed reversal-to-expansion case

## What Is Locked

Locked at the current doctrine level:

- Garrett wants swing formation at key level
- Garrett trades the expansion candle
- `C1` is not the trade candle
- in the standard delayed-expansion case, the expansion candle is `C3`
- in the compressed reviewed case, `C2` can itself be the expansion candle

## What Is Not Yet Locked

Not yet locked:

1. exact execution mechanics inside the trade candle
2. stop placement doctrine
3. target-taking doctrine
4. whether later material adds more entry variants beyond the two currently
   reviewed cases

## Implementation Status

Implementation status: doctrine only.

The repo currently detects and validates this structure, but does not yet
implement trade execution or order-management logic.
