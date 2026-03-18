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
is presented as a framework.

The framework says, in effect:

- when price retraces into the correct internal key level
- reversal is expected from that level
- the expected objective is the relevant external range

This gives the model three context objects:

1. a watch location / key level
2. an expected reaction
3. a target level

## Internal to External Model

### Current Context Reading

For the `internal to external` model:

- `IRL` is the internal range liquidity
- `ERL` is the external range liquidity

The current evidence strongly supports the interpretation that:

- `IRL` is the internal fair value gap / internal imbalance zone
- `ERL` is the external target liquidity

So, in the current doctrinal reading:

- watch location / key level = `IRL`
- expected behavior = reversal from `IRL`
- target = `ERL`

## IRL as Key Level

From the current transcript and image pair, the internal key level is being
presented as the fair value gap / imbalance zone inside the model structure.

Current source-derived doctrine statement:

- in this universal-model explanation, `IRL` is being represented as the fair
  value gap / internal imbalance zone that price retraces into before
  reversing

This is important because it ties the higher-level model directly to a
specific key level concept.

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
2. key level (`IRL`)
3. target (`ERL`)
4. candle reaction / execution grammar:
   - `C2` closure
   - `C3` support / expansion
   - `C4` continuation candidate

This means a valid candle sequence matters only if it occurs at the right
contextual location.

## What Is Locked

Locked as source-derived doctrine context:

- the universal model is a framework for where to watch and where to target
- in the current `internal to external` explanation:
  - `IRL` is the key level
  - `ERL` is the target
- the current evidence strongly supports `IRL` being represented as the fair
  value gap / internal imbalance zone

## What Is Not Yet Locked

Not yet locked:

1. the exact mechanical boundaries of `IRL`
2. the exact mechanical boundaries of `ERL`
3. whether every `IRL` in Garrett's framework is always exactly a codable
   three-candle fair value gap object
4. how the active `ERL` is selected unambiguously when multiple candidates
   exist
5. the exact doctrine for:
   - `external to internal`
   - `manipulation range`

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
