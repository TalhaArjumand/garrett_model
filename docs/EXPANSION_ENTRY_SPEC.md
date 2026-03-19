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

- `C2` belongs to the swing-formation / qualification side
- `C3` is the expansion candle
- Garrett trades the expansion candle

## Execution Flow

The current execution reading is:

1. identify the relevant key level
2. wait for price to reach that level
3. require Garrett swing formation there
   - currently represented by `C2` closure and downstream qualification
4. trade the expansion candle
   - currently `C3`

So the current doctrinal flow is:

- key level -> swing formation -> expansion candle trade

## What This Clarifies

This doctrine clarification means:

- `C2` is not the primary trade candle
- `C3` is not just confirmation in the abstract
- `C3` is the actual expansion candle Garrett wants to trade
- `C4` is not the primary entry candle in this flow

## Relationship to C4

`C4` remains a later continuation layer.

That means:

- `C3` is the primary trade candle in the currently reviewed flow
- `C4` is downstream continuation behavior after that trade candle already
  exists

## What Is Locked

Locked at the current doctrine level:

- Garrett wants swing formation at key level
- Garrett trades the expansion candle
- in the current candle grammar, the expansion candle is `C3`

## What Is Not Yet Locked

Not yet locked:

1. exact execution mechanics inside the `C3` candle
2. stop placement doctrine
3. target-taking doctrine
4. whether later material adds exceptions where a non-`C3` candle is the
   primary trade candle

## Implementation Status

Implementation status: doctrine only.

The repo currently detects and validates this structure, but does not yet
implement trade execution or order-management logic.
