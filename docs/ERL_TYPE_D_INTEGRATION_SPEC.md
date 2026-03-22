# ERL Type D Integration Spec

## Scope

This tranche is:

- `ERL -> Type D`
- key level + family only
- target excluded
- selector excluded

This tranche is not:

- `IRL -> Type D`
- target logic
- selector logic
- execution modeling beyond the locked stage contract

## Locked Family Dependency

Integrated `ERL -> Type D` is allowed only if the family primitive is already
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

Integrated `ERL -> Type D` inherits the family-general `Type D` stage contract:

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

- a preexisting resting `ERL` may be touched by `C1`, `C2`, or both
- a fresh `ERL` confirmed on `C1` close becomes first eligible from `C2`
- a fresh-on-`C2` confirmation would require future-derived key-level knowledge
  for the same sequence window, so it is excluded

## Touch Rule

For a preexisting resting `ERL`:

- touch on `C1`: allowed
- touch on `C2`: allowed
- touch on both: allowed

For a fresh-on-`C1` `ERL`:

- first eligible touch begins at `C2`
- touch label is therefore `c2`

## Eligibility Ladder

A candidate is valid `ERL -> Type D` only if all of the following are true:

1. a live same-bias `ERL` exists
2. the sequence window touches that `ERL` in an allowed way
3. the family primitive is valid `Type D`
4. the candidate remains excluded from:
   - `Type A`
   - `Type B`
   - `Type B additive extension`
   - strict `Type C`

## Evidence Boundary

The integration should be published only after:

1. unit tests pass
2. real-sample counts are inspectable
3. at least one manual anchor is confirmed on chart

This keeps the branch:

- implementation-verified
- stage-clean
- left-to-right safe
