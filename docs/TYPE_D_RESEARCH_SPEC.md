# Type D Research Spec

## Status

This is a research candidate family.

It is:

- implemented as a family primitive
- implemented in the family-general domain/stage contract
- not integrated under `IRL` / `ERL`
- not counted in active reports
- not part of strict `Type A`, `Type B`, or `Type C`

It exists to preserve and test a fourth swing-family structure without yet
promoting it into integrated key-level taxonomy.

## Motivation

The candidate was proposed because there appears to be a real swing-formation
path that is not captured by:

- `Type A`
- `Type B`
- `Type B additive extension`
- strict `Type C`

The proposed difference is the role of `C3`:

- strict `Type C` uses `C3` as the confirming closure candle
- proposed `Type D` uses `C3` as a fully contained setup candle inside `C2`
- `C4` becomes the first tradable candle from `EQ(C3)`

## Research Boundary

This document freezes only the candidate structure.

It does not:

- change active integrated family counts
- change the locked stage model for existing active families
- change any `IRL` / `ERL` integration behavior

## Candidate Identity

Proposed `Type D` is a delayed swing-family candidate where:

- `C2` sweeps the relevant edge of `C1`
- `C2` does not resolve into `Type A`
- `C2` does not resolve into `Type B`
- `C2` does not resolve into `Type B additive extension`
- `C3` is a strict inside candle relative to `C2`
- `EQ(C3)` becomes the operative level
- first tradable candle = `C4`

## Strict Inside-Candle Rule

The inside condition is strict.

Allowed:

- `high(C3) < high(C2)`
- `low(C3) > low(C2)`

Therefore:

- `open(C3)` is inside the range of `C2`
- `close(C3)` is inside the range of `C2`

Equality is not allowed at either boundary.

## Bullish Candidate Rule

Proposed bullish `Type D` requires:

1. a relevant bullish key-level interaction already exists
2. `C2` sweeps below `low(C1)`
3. `C2` is not valid bullish `Type A`
4. `C2` is not valid bullish `Type B`
5. `C2` is not valid bullish `Type B additive extension`
6. `C3` is a strict inside candle within `C2`
7. `EQ(C3)` becomes the operative level
8. `C4` is the first tradable candle if it respects the bullish setup logic

## Bearish Mirror Rule

Proposed bearish `Type D` requires:

1. a relevant bearish key-level interaction already exists
2. `C2` sweeps above `high(C1)`
3. `C2` is not valid bearish `Type A`
4. `C2` is not valid bearish `Type B`
5. `C2` is not valid bearish `Type B additive extension`
6. `C3` is a strict inside candle within `C2`
7. `EQ(C3)` becomes the operative level
8. `C4` is the first tradable candle if it respects the bearish setup logic

## Exclusions From Existing Families

### Not Type A

`Type D` excludes any case where:

- `C2` closes back inside full `C1` range in the valid `Type A` manner

### Not Type B

`Type D` excludes any case where:

- `C2` itself is the valid reversal-to-expansion trade candle

### Not Type B Additive Extension

`Type D` excludes any case where:

- base `Type B` is already valid
- and the stronger `C2` regime extends tradability to `C3`

### Not Strict Type C

`Type D` excludes any case where:

- `C3` is the strict confirming closure candle of `Type C`

The defining difference is:

- strict `Type C`: `C3` confirms
- proposed `Type D`: `C3` contains and prepares

## Stage Mapping

This candidate currently implies:

- `family = type_d`
- `domain_confirmed_at = c3_close`
- `first_tradable_candle = c4`

This stage mapping is now implemented at the family-general contract level.

## Evidence Status

Current evidence status:

- `research_only`
- `source_tethered_research_anchor`
- `family_primitive_implemented`

Current evidence basis:

- observed chart behavior
- source claim that Garrett traded the pattern on `6H`
- normalized `6H` exported data now exists for direct research inspection

## First 6H Source Anchor

This anchor is confirmed on normalized `6H` exported data and is preserved as
source-tethered research evidence, not live family implementation.

### Context

- key-level context:
  - bearish `IRL`
- IRL zone:
  - `4663.38 -> 4686.85`
- IRL confirmation:
  - `2026-03-19 18:00 +05:00`
- timing class:
  - `fresh_on_c1`

### Sequence

- `C1 = 2026-03-19 18:00 +05:00`
  - `4596.52 / 4663.38 / 4574.04 / 4648.73`
- `C2 = 2026-03-20 00:00 +05:00`
  - `4654.32 / 4735.84 / 4634.19 / 4725.64`
- `C3 = 2026-03-20 06:00 +05:00`
  - `4725.65 / 4734.87 / 4659.88 / 4667.59`
- `C4 = 2026-03-20 12:00 +05:00`
  - `4667.60 / 4695.44 / 4540.53 / 4553.31`

### Why It Is Not Type A

- bearish `Type A` would require `C2` to close back inside full `C1` range
- `high(C1) = 4663.38`
- `close(C2) = 4725.64`
- so `C2` does not close back inside `C1` range

### Why It Is Not Type B

- bearish `Type B` would require `C2` itself to be the bearish
  reversal-to-expansion candle
- `C2` is bullish, not bearish

### Why It Is Not Type B Additive Extension

- `Type B additive extension` requires base `Type B` to already be true
- base `Type B` is false here

### Why It Is Not Strict Type C

- strict bearish `Type C` would require `C3` to be the confirming bearish
  closure candle
- instead, `C3` is a strict inside candle within `C2`

### Inside-Candle Confirmation

- `high(C3) = 4734.87 < 4735.84 = high(C2)`
- `low(C3) = 4659.88 > 4634.19 = low(C2)`

So `C3` satisfies the strict inside-candle rule.

### Operative Level And Tradable Candle

- `EQ(C3) = (4734.87 + 4659.88) / 2 = 4697.375`
- `C4.high = 4695.44 < EQ(C3)`

Research interpretation:

- `C3` is the contained setup candle
- `EQ(C3)` becomes the operative level
- `C4` is the first tradable candle

### Current Research Conclusion

This is a strong bearish `6H` source anchor for proposed `Type D`.

It supports:

- distinct structure from `Type A`
- distinct structure from `Type B`
- distinct structure from `Type B additive extension`
- distinct structure from strict `Type C`

It does not yet justify live `IRL` / `ERL` integration by itself.

## Promotion Conditions

Do not promote this candidate into live integrated taxonomy until all of the
following are done:

1. capture the actual source example on `6H`
2. verify the exact candle structure on exported data
3. confirm the bullish and bearish rules are exact
4. confirm separation from:
   - `Type A`
   - `Type B`
   - `Type B additive extension`
   - strict `Type C`
5. test it on preserved real exports
6. confirm that the candidate is stable enough to deserve live taxonomy

## Safe Current Statement

The safe current statement is:

- `Type D` is a plausible fourth swing-family candidate in the framework

Do not currently state:

- that it is already integrated under `IRL` / `ERL`
- that it is proven exhaustive with `A / B / C`
