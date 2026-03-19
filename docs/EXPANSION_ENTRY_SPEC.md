# Expansion Entry Spec

## Purpose

This spec records the current Garrett execution doctrine for what actually gets
traded after price reaches a key level.

The important distinction is:

- key level is the watch location
- swing formation is the qualification event
- the actionable candle depends on the reviewed swing-formation type

This prevents the repo from collapsing:

- key level
- setup formation
- trade execution

into the same object.

## Locked Predecessor Context

Already locked elsewhere in the repo:

- `IRL` / `ERL` are the current key-level objects
- candle formation is watched once price reaches a key level
- Garrett swing formation currently has three reviewed types:
  - Type A: `C2 closure -> C3 expansion`
  - Type B: `C2 reversal to expansion`
  - Type C: `C3 closure -> C4 continuation candidate`

## Current Doctrine Statement

At the current doctrinal level:

1. price reaches a key level
2. Garrett swing formation appears there
3. the reviewed actionable candle depends on which formation type completes

In the currently locked candle grammar, this means:

- `C1` is not the trade candle
- Type A:
  - `C2` belongs to the swing-formation / qualification side
  - `C3` is the expansion candle
- Type B:
  - `C2` itself can be the tradeable expansion candle
- Type C:
  - `C3` is the closure / formation candle
  - continuation or expansion is then sought in `C4`
- Garrett trades the reviewed post-formation expansion / continuation candle,
  not the raw key-level touch candle

## Execution Flow

The current execution reading is:

1. identify the relevant key level
2. wait for price to reach that level
3. require Garrett swing formation there
4. act on the reviewed post-formation expansion / continuation candle of that
   path

So the current doctrinal flow is:

- key level -> swing formation -> actionable expansion / continuation candle

## What This Clarifies

This doctrine clarification means:

- `C1` is not the primary trade candle
- no single candle number is universally the trade candle across all reviewed
  swing-formation types
- the actionable candle depends on which reviewed formation path completed
- `C4` is not universally only downstream context anymore, because the reviewed
  `C3 closure` branch explicitly seeks continuation in `C4`

## Relationship to C4

`C4` remains downstream of Type A and Type B primary expansion behavior.

But in the reviewed Type C branch:

- `C3` forms the closure
- `EQ(C3)` is marked only after that closure exists
- `C4` becomes the next reviewed continuation / expansion candidate

So current doctrine should not flatten all reviewed entry logic into:

- always trade `C3`

## What Is Locked

Locked at the current doctrine level:

- Garrett wants swing formation at key level
- Garrett does not blindly trade the key-level touch candle
- `C1` is not the trade candle
- the reviewed actionable candle depends on the reviewed formation type:
  - Type A -> `C3`
  - Type B -> `C2`
  - Type C -> `C4` candidate after `C3` closure

## What Is Not Yet Locked

Not yet locked:

1. exact execution mechanics inside the actionable candle
2. stop placement doctrine
3. target-taking doctrine
4. whether later material adds more entry variants beyond the three currently
   reviewed types
5. whether the `C3 closure` branch should be described finally as continuation
   only or as a full entry branch

## Implementation Status

Implementation status: doctrine only.

The repo currently detects and validates parts of this structure, but does not
yet implement trade execution or order-management logic.
