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

This spec now covers the directly defined framework relationship between:

- `internal to external`
- `external to internal`

The following term is still present but not yet fully defined here:

- `manipulation range`

## Core Source-Derived Doctrine

From the reviewed defining material, the universal model is presented as a
generalized framework.

The framework says, in effect:

- the market either reaches for old highs / old lows
  or
- seeks to rebalance a fair value gap

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
4. `IRL`
   - fair value gap (`FVG`)
5. `ERL`
   - swing high / swing low in the form of buy-side / sell-side liquidity

This hierarchy is important because it prevents collapsing:

- framework
- range relationship
- key level object

into one concept.

## Internal to External Model

### Current Context Reading

For the `internal to external` model:

- watch location / key level is `IRL`
- expected target is `ERL`

For the `external to internal` model:

- watch location / key level is `ERL`
- expected target is `IRL`

## IRL as Key Level

From the reviewed defining material, `IRL` is directly defined as a fair value
gap.

Current source-derived doctrine statement:

- `IRL = FVG`
- after taking `ERL`, price can seek `IRL`
- after reaching `IRL`, price can seek `ERL`

## ERL as Target

The external range liquidity is the external-side swing-liquidity object in the
model.

Current source-derived doctrine statement:

- `ERL` is a swing high or swing low in the form of buy-side or sell-side
  liquidity
- in `IRL -> ERL`, it is the target side
- in `ERL -> IRL`, it is the reaction side

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
3. specific internal / external objects under the current chunk:
   - `IRL = FVG`
   - `ERL = swing high / swing low liquidity`
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
- the market either reaches for old highs / old lows or seeks to rebalance a
  fair value gap
- `IRL = FVG`
- `ERL` is a swing high or swing low in the form of buy-side / sell-side
  liquidity
- in `internal -> external`:
  - watch location = `IRL`
  - target = `ERL`
- in `external -> internal`:
  - watch location = `ERL`
  - target = `IRL`

## What Is Not Yet Locked

Not yet locked:

1. how the active `ERL` is selected unambiguously when multiple candidates
   exist
2. how the active `IRL` is selected unambiguously when multiple fair value gaps
   exist
3. the exact operational definition of `manipulation range`
4. whether later doctrine adds further qualification rules beyond the current
   framework mapping

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
