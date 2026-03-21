# Domain Stage Model Spec

## Purpose

This spec freezes the family-general stage model that sits between:

- structural swing-family detection
- actual tradable-candle timing
- later continuation timing

It exists to prevent the repo from collapsing:

- family structure
- family confirmation
- first trade timing
- continuation timing

into one flat object.

That separation is required for:

- runtime realism
- later state-machine design
- clean research labels
- future ML / deep-learning datasets

## Scope

This spec is family-general only.

It does **not** yet attach:

- `IRL`
- `ERL`
- selector logic
- target logic
- stop logic
- entry mechanics inside the tradable candle

Those belong in later key-level-context and execution-model layers.

## Hard Distinction

Structural integration match is **not** the same object as a tradable-stage
object.

Current repo integrations such as:

- `IRL -> Type A`
- `ERL -> Type B`

should therefore be treated as:

- structural/key-level coverage

not as the final execution-stage model.

## Required Fields

The family-general contract should carry explicit fields for:

- `family`
- `domain_candle`
- `domain_confirmed_at`
- `first_tradable_candle`
- `continuation_from`
- `stage_status`

These fields should not be left implicit.

## Field Definitions

### `family`

Allowed values:

- `type_a`
- `type_b`
- `type_c`

### `domain_candle`

The candle on which the family domain becomes structurally meaningful.

Allowed values:

- `c2`
- `c3`

### `domain_confirmed_at`

The event at which the family domain becomes confirmed enough to activate the
next stage.

Current reviewed values:

- `c2`
- `c2_close`
- `c3_close`

### `first_tradable_candle`

The first candle that belongs to the actual trade domain of the reviewed
family.

Current reviewed values:

- `c2`
- `c3`
- `c4`

### `continuation_from`

The predecessor event that must complete before the continuation stage can
become eligible.

Current reviewed values:

- `c3_confirmed`
- `none_locked_yet`

### `stage_status`

This should be explicit, not inferred.

Recommended controlled enum:

- `structural_only`
- `domain_confirmed`
- `first_tradable`
- `continuation_eligible`
- `invalidated`

This field is a normalized stage summary, not a replacement for the structural
fields above.

## Family Mapping

### Type A

Structural reading:

- `C2` closes back inside the full range of `C1`

Stage mapping:

- `family = type_a`
- `domain_candle = c2`
- `domain_confirmed_at = c2_close`
- `first_tradable_candle = c3`
- `continuation_from = c3_confirmed`

Operational meaning:

- once `C2` closes inside `C1`, the `Type A` domain is alive
- `C3` is the first tradable candle
- if `C3` fully confirms, then `C4` becomes the continuation trade domain

### Type B

Structural reading:

- `C2` performs the reversal-to-expansion behavior itself

Stage mapping:

- `family = type_b`
- `domain_candle = c2`
- `domain_confirmed_at = c2`
- `first_tradable_candle = c2`
- `continuation_from = none_locked_yet`

Operational meaning:

- the first trade domain and the family domain collapse into `C2`

### Type C

Structural reading:

- no valid `Type A` `C2` closure forms
- the decisive confirming event is the `C3` closure

Stage mapping:

- `family = type_c`
- `domain_candle = c3`
- `domain_confirmed_at = c3_close`
- `first_tradable_candle = c4`
- `continuation_from = none_locked_yet`

Operational meaning:

- `C3` is the closure / formation candle
- `C4` is the first tradable candle
- `Type C` should not be flattened into “trade `C3`”

## Stage Progression

Current reviewed stage progression by family:

- `Type A`
  - `structural_only -> domain_confirmed -> first_tradable -> continuation_eligible`
- `Type B`
  - `structural_only -> domain_confirmed -> first_tradable`
- `Type C`
  - `structural_only -> domain_confirmed -> first_tradable`

This is a family-general state model, not a full execution engine.

## Why `stage_status` Must Be Explicit

If stage is left implicit, future labels will mix:

- pattern detection
- trade readiness
- continuation readiness

That creates:

- ambiguous research labels
- brittle feature engineering
- hidden coupling
- poor ML / DL targets

So the repo should carry:

- explicit structural fields
- plus an explicit stage summary

## Non-Goals

This spec does not yet define:

- `IRL` / `ERL` timing
- target selection
- stop placement
- lower-timeframe trigger logic
- order execution mechanics
- later continuation beyond the currently reviewed family mapping

## Current Repo Implication

Current integrated detectors remain useful.

But they should now be interpreted as:

- structural coverage objects

and not as the final tradable-stage schema.

The next architecture layer should attach:

- key-level context
- timing eligibility
- overlap state

on top of this family-general contract.
