# C4 Expansion Quality Research

## Purpose

This note records a stricter research-only quality filter for `C4` after a
valid predecessor has already activated `EQ(C3)`.

It does not replace the base `C4` doctrine candidate.

## Boundary

Base reviewed doctrine currently supports:

- after the relevant predecessor state
- mark `EQ(C3)`
- seek `C4` with its low/high formed in the correct half of `C3` range

This note adds a stricter research filter on top of that base candidate:

- expansion-like `C4` should also have a small same-side wick

## Shared Small-Wick Definition

The strict `C4` path now uses the shared small-wick helper defined in
[SMALL_WICK_RESEARCH_SPEC.md](/Users/njap/Downloads/garrett-trading-research/docs/SMALL_WICK_RESEARCH_SPEC.md).

Current hard-cap rule:

- bullish `C4`: `lower_wick / range <= threshold`
- bearish `C4`: `upper_wick / range <= threshold`

Current research default:

- `threshold = 0.25`

## Why This Exists

Earlier reviewed doctrine already tied expansion candles to smaller wick
structure.

So for `Type C`:

- base rule:
  - `low(C4) > EQ(C3)` for bullish
  - `high(C4) < EQ(C3)` for bearish
- stricter research rule:
  - `C4` also has directional body consistency
  - `C4` also has a small same-side wick

## Current Machine Form

### Bullish strict `C4` quality candidate

- valid bullish `Type C` `C4` candidate
- `C4` is bullish
- `lower_wick(C4) / range(C4) <= threshold`

### Bearish strict `C4` quality candidate

- valid bearish `Type C` `C4` candidate
- `C4` is bearish
- `upper_wick(C4) / range(C4) <= threshold`

## Threshold Status

The wick threshold is currently a research parameter, not locked doctrine.

Current default in code:

- `0.25`

## Intended Use

Use this stricter path for:

- real-data rarity counting
- manual review
- comparing base `C4` candidates against stronger-quality `C4` candidates

Do not use it yet as:

- doctrine
- final trade-entry law
- a hidden filter inside the base `C4` detector
