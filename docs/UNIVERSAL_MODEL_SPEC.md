# Universal Model Spec

## Purpose

This spec captures the higher-level context layer that sits above the candle
and sequence primitives.

At this layer, the goal is not to define entry candles directly. The goal is
to define:

- where to watch
- what kind of reaction to expect
- where price is expected to trade next

This is the context layer that gives meaning to the lower candle-formation
logic.

## Scope

This spec is currently limited to the first universal-model explanation
processed from Garrett's material:

- `internal to external`

The following terms are present but not yet fully defined here:

- `external to internal`
- `manipulation range`

## Core Source-Derived Doctrine

From the current transcript chunk and accompanying diagram, the universal model
is presented as a generalized framework.

The framework says, in effect:

- when price retraces into the correct internal key level
- reversal is expected from that level
- the expected objective is the relevant external range

This gives the model three high-level context objects:

1. a watch location / key level
2. an expected reaction
3. a target level

## Current Hierarchy

The cleanest current doctrinal hierarchy is:

1. `Universal Model`
   - generalized framework
2. `Key Levels`
   - important locations inside the framework
3. `IRL / ERL`
   - internal / external range-liquidity structure used by the framework
4. `IRL Key Level`
   - in the current chunk, the fair value gap (`FVG`)

This hierarchy is important because it prevents collapsing:

- framework
- range relationship
- key level object

into one concept.

## Internal to External Model

### Current Context Reading

For the `internal to external` model:

- `IRL` is the internal range liquidity
- `ERL` is the external range liquidity

The current evidence strongly supports the interpretation that:

- `IRL` is the internal-side range-liquidity context
- `ERL` is the external-side target liquidity context

So, in the current doctrinal reading:

- watch location / key level is found on the `IRL` side
- expected behavior = reversal from the `IRL` key level
- target = `ERL`

## IRL as Key Level

From the current transcript and image pair, the internal key level is being
presented as the fair value gap / imbalance zone inside the `IRL` structure.

Current source-derived doctrine statement:

- in this universal-model explanation, the `IRL` key level is the fair value
  gap / internal imbalance zone that price retraces into before reversing

This is important because it ties the higher-level model directly to a
specific key-level subtype.

So the current refined reading is:

- `IRL` is not simply equal to `FVG`
- rather, `FVG` is the current key level being defined within the `IRL`
  structure

## ERL as Target

The external range liquidity is the target side of the model.

Current source-derived doctrine statement:

- after price retraces into the internal key level (`IRL`), the expected move
  is toward the external range liquidity (`ERL`)

This means the model is not only location-aware but also target-aware before
the candle-formation layer is applied.

## Relationship to Candle Sequences

The candle/sequence primitives already implemented in the repo are execution
grammar, not standalone trade context.

Current hierarchy:

1. universal-model context
2. range / key-level context:
   - `IRL`
   - `ERL`
3. specific key level under the current chunk:
   - `FVG` inside `IRL`
4. candle reaction / execution grammar:
   - `C2` closure
   - `C3` support / expansion
   - `C4` continuation candidate

This means a valid candle sequence matters only if it occurs at the right
contextual location.

## What Is Locked

Locked as source-derived doctrine context:

- the universal model is a generalized framework for where to watch and where
  to target
- the framework uses key levels
- in the current `internal to external` explanation:
  - `IRL` is the internal-side range-liquidity context
  - `ERL` is the external target-side liquidity context
- the current evidence strongly supports the `IRL` key level being represented
  by the fair value gap / internal imbalance zone

## What Is Not Yet Locked

Not yet locked:

1. the exact mechanical boundaries of `IRL`
2. the exact mechanical boundaries of `ERL`
3. whether every `IRL` in Garrett's framework always contains the same kind of
   codable `FVG` object
4. how the active `ERL` is selected unambiguously when multiple candidates
   exist
5. the exact doctrine for:
   - `external to internal`
   - `manipulation range`
6. whether there are additional key-level types under `IRL` besides `FVG`

## Implementation Status

Implementation status: not started.

This is currently a doctrine/context artifact only.

No code should assume a final machine-ready definition of `IRL` or `ERL`
until more direct definitional evidence is extracted.

## Non-goals

This spec does not yet define:

- code for `IRL` detection
- code for `ERL` detection
- entry rules by itself
- target-taking rules by itself
- session rules
- driver rules
