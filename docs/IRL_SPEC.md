# IRL Spec

## Purpose

This spec defines `IRL` (`Internal Range Liquidity`) in Garrett's universal
model at the current doctrine level.

It exists to make the internal-side key level explicit before any later
confluence, sequence, or targeting logic is applied.

## Current Doctrinal Status

`IRL` is now directly defined in the reviewed material.

At the current doctrine level, `IRL` is not merely associated with `FVG`.
It is directly defined as a fair value gap.

## Definition

From the reviewed defining video:

- internal range liquidity is a fair value gap

So the current repo-level doctrine is:

- `IRL = FVG`

This is the watch / reaction location in the universal model when price is
seeking internal liquidity.

## Directional Role In The Universal Model

### External To Internal

In the current `external -> internal` model:

- price reaches `ERL`
- price is expected to seek `IRL`

### Internal To External

In the current `internal -> external` model:

- price reaches `IRL`
- price is expected to seek `ERL`

So `IRL` is the internal-side rebalance / reaction object in the universal
model.

## What Is Locked

Locked in the current repo doctrine:

- `IRL` is a fair value gap
- `IRL` is the internal-side key level in the universal model
- after taking `ERL`, price may seek `IRL`
- after reaching `IRL`, price may seek `ERL`

## What Is Not Yet Locked

Not yet locked:

1. how multiple internal fair value gaps should be ranked when more than one
   exists
2. whether every visible fair value gap is equally relevant as `IRL`
3. how `IRL` qualification should be subordinated to broader confluence
4. whether additional internal key-level types exist elsewhere in Garrett's
   model

## Important Boundary

Even though `IRL` is directly defined as a fair value gap, this does not solve:

- which `IRL` is most relevant when several exist
- when a given `IRL` should be acted on
- what extra confluence is required at that key level

Those remain separate doctrine questions.

## Implementation Status

Implementation status: doctrine plus helper-layer lifecycle tracking.

The repo already contains:

- baseline `FVG` geometry detection
- helper-layer `IRL/FVG` lifecycle tracking:
  - `resting`
  - `reached`
  - `invalidated`

But no higher-order `IRL` selection or qualification engine is currently
implemented.

## Non-goals

This spec does not yet define:

- active `IRL` ranking
- confluence scoring at `IRL`
- entry logic by itself
- target logic by itself
