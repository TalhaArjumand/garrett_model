# Type B Additive Extension Research

## Provenance

Historical references to:

- `rare Type C`
- `rare Type C C3 quality`

are retained only as provenance notes.

Active taxonomy now classifies those structures as:

- `Type B additive extension`
- `Type B additive extension C3 quality`

## Purpose

This note records the research layer for a stronger `Type B` branch where:

- `C2` is still the base `Type B` trade candle
- `C2` also closes through the body boundary of `C1`
- that stronger `C2` regime can make `C3` tradable as an additive extension

It is intentionally research-only, not doctrine.

## Boundary

This file does **not** create a new family.

Live family taxonomy remains:

- `Type A`
- `Type B`
- `Type C`

Strict `Type C` keeps:

- `domain_confirmed_at = c3_close`
- `first_tradable_candle = c4`

So any branch whose first tradable candle is `C3` must not remain inside live
`Type C` taxonomy.

## Structural Definition

### Base prerequisite

`Type B additive extension` must first satisfy valid base `Type B`.

### Decisive `C2` boundary

Use the body boundary of `C1`, not the full `high(C1)` / `low(C1)`.

- bullish:
  - `close(C2) > body_top(C1)`
- bearish:
  - `close(C2) < body_bottom(C1)`

### Additive extension trigger

Once base `Type B` is valid and the body-close condition holds:

- mark `EQ(C2)`
- if `C3` respects `EQ(C2)`, then `C3` becomes the additive tradable candle

## Current Machine Form

### Bullish Type B additive extension

- valid bullish `Type B`
- `close(C2) > body_top(C1)`
- `low(C3) > EQ(C2)`

### Bearish Type B additive extension

- valid bearish `Type B`
- `close(C2) < body_bottom(C1)`
- `high(C3) < EQ(C2)`

## `C3` Quality Subtype

This is a stricter research refinement inside the additive extension itself.

### Bullish Type B additive extension `C3` quality

- valid bullish `Type B additive extension`
- `low(C3) > EQ(C2)`
- small same-side wick on `C3`

### Bearish Type B additive extension `C3` quality

- valid bearish `Type B additive extension`
- `high(C3) < EQ(C2)`
- small same-side wick on `C3`

## IRL Integration Contract

This extension may be integrated with `IRL / FVG` context, but only as a
research extension inside integrated `Type B`.

### Base prerequisite

An integrated `Type B additive extension` must first satisfy canonical
integrated `Type B`.

### Integration upgrade

Once integrated base `Type B` is valid, the additive upgrade is exact:

- bullish:
  - `close(C2) > body_top(C1)`
  - `low(C3) > EQ(C2)`
- bearish:
  - `close(C2) < body_bottom(C1)`
  - `high(C3) < EQ(C2)`

### Timing

Use the same timing matrix as integrated base `Type B`.

### Validity horizon

The active `IRL` must remain directionally valid through `C3` close.

### Overlap policy

- overlap with integrated `Type B`:
  - yes by definition
- overlap with strict integrated `Type C`:
  - no under active taxonomy
- overlap with additive `C3` quality:
  - yes by definition when the stricter subtype passes

## Historical Migration Note

The previously named:

- `rare Type C`
- `rare Type C C3 quality`

research branches are now historical labels only.

Current live taxonomy should not count them as active `Type C` trade-family
objects.

## Current Reviewed Status

Current reviewed status on the preserved `XAUUSD 4H` MT5 sample:

- integrated `Type B additive extension` matches:
  - `1`
- integrated `Type B additive extension C3 quality` matches:
  - `1`

The reviewed integrated example is:

- bullish
- `IRL = 4892.76 -> 4912.94`
- `C1 = 2026-02-18 08:00 +05:00`
- `C2 = 2026-02-18 12:00 +05:00`
- `C3 = 2026-02-18 16:00 +05:00`

This region remains useful because it preserves:

- base `Type B`
- `Type B additive extension`
- `Type B additive extension C3 quality`

without polluting strict `Type C`.
