# ERL Spec

## Purpose

This spec defines `ERL` (`External Range Liquidity`) in Garrett's universal
model at the current doctrine level.

It exists to make the target-side / reaction-side external object explicit
without pretending that full `ERL` selection is already solved.

## Current Doctrinal Status

`ERL` is defined at the framework level.

It is not yet mechanically selectable when multiple candidate external levels
or structures exist.

## Definition

`ERL` is the external-side chart object in Garrett's universal model.

It represents the external range objective / external range side that price may
either:

- target
- react from

depending on which side of the universal-model relationship is active.

## Chart Objects That Can Count As ERL

From the currently reviewed doctrine, `ERL` may be represented by:

- range high / range low
- swing high / swing low
- manipulation range

This defines the current `ERL` object family.

It does not yet define how one candidate becomes the active external target
when several candidates exist.

## Directional Role In The Universal Model

### Internal To External

In the current `internal -> external` model:

- price reacts from `IRL`
- price targets `ERL`

### External To Internal

In the current `external -> internal` model:

- price reacts from `ERL`
- price targets `IRL`

So `ERL` is not only a target-side object.
It can also be the reaction location in the mirrored universal-model path.

## What Is Locked

Locked in the current repo doctrine:

- `ERL` is the external-side chart object in the universal model
- current chart objects that can count as `ERL` include:
  - range high / range low
  - swing high / swing low
  - manipulation range
- in `IRL -> ERL`, `ERL` is the target side
- in `ERL -> IRL`, `ERL` is the reaction side

## What Is Not Yet Locked

Not yet locked:

1. an explicit mechanical rule for selecting the relevant `ERL` when multiple
   candidates exist
2. a ranking method among multiple external highs / lows / ranges
3. a fully machine-ready `ERL` detector
4. the exact operational definition of `manipulation range`

## Important Boundary

Do not invent a deterministic `ERL` selector.

Current doctrine defines the `ERL` object family and directional role, but not
a full selection algorithm.

## Implementation Status

Implementation status: doctrine only.

No `ERL` detector is currently implemented.

## Non-goals

This spec does not yet define:

- final `ERL` code
- `ERL` ranking logic
- manipulation-range detection
- target confirmation logic by itself
