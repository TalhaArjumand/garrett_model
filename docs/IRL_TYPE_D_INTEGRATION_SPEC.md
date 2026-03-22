# IRL Type D Integration Spec

## Scope

This tranche is:

- `IRL -> Type D`
- key level + family only
- target excluded
- selector excluded

This tranche is not:

- `ERL -> Type D`
- target logic
- selector logic
- execution modeling beyond the locked stage contract

## Locked Family Dependency

Integrated `IRL -> Type D` is allowed only if the family primitive is already
true:

- bullish `Type D`
- bearish `Type D`

That family primitive already excludes:

- `Type A`
- `Type B`
- `Type B additive extension`
- strict `Type C`

So the integration layer must not re-broaden those boundaries.

## Locked Stage Mapping

Integrated `IRL -> Type D` inherits the family-general `Type D` stage contract:

- `family = type_d`
- `domain_confirmed_at = c3_close`
- `first_tradable_candle = c4`

If a candidate would make `C3` tradable, it is not `Type D`.

## Timing Matrix

The timing matrix is locked as:

- `preexisting_before_c1`: allowed
- `fresh_on_c1_close`: allowed
- `fresh_on_c2_close`: excluded

Rationale:

- a preexisting resting `IRL` may be touched by `C1`, `C2`, or both
- a fresh `IRL` confirmed on `C1` close becomes first eligible from `C2`
- a fresh-on-`C2` confirmation would require future-derived key-level knowledge
  for the same sequence window, so it is excluded

## Touch Rule

For a preexisting resting `IRL`:

- touch on `C1`: allowed
- touch on `C2`: allowed
- touch on both: allowed

For a fresh-on-`C1` `IRL`:

- first eligible touch begins at `C2`
- touch label is therefore `c2`

## Eligibility Ladder

A candidate is valid `IRL -> Type D` only if all of the following are true:

1. a live directional `IRL` exists
2. the sequence window touches that `IRL` in an allowed way
3. the `IRL` remains eligible through `C3` close
4. the family primitive is valid `Type D`

## Evidence Boundary

The integration was published only after:

1. unit tests pass
2. real-sample counts are inspectable
3. at least one manual anchor is confirmed on chart

This keeps the branch:

- implementation-verified
- stage-clean
- left-to-right safe

## First Manual Integrated Anchor

The first confirmed manual integrated anchor on preserved raw `MT5 XAUUSD 4H`
data is:

- direction: bullish
- `IRL = 4100.39 -> 4122.46`
- `confirmed_at = 2025-11-25 00:00 +05:00`
- `key_level_touch = c2`
- `C1 = 2025-11-25 04:00 +05:00`
  - `4134.59 / 4155.61 / 4132.89 / 4150.95`
- `C2 = 2025-11-25 08:00 +05:00`
  - `4150.93 / 4151.96 / 4109.01 / 4128.46`
- `C3 = 2025-11-25 12:00 +05:00`
  - `4128.41 / 4150.88 / 4115.99 / 4147.87`

This anchor is:

- valid `IRL -> Type D`
- chart-confirmed
- preserved as the first integrated manual reference for this branch
