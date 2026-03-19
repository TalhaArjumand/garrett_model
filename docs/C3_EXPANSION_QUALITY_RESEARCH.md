# C3 Expansion Quality Research

## Purpose

This note records a stricter research-only quality filter for `Type A`, where
`C3` is the reviewed expansion candle.

It does not replace the base `Type A` doctrine-safe sequence.

## Boundary

Base reviewed doctrine for `Type A` remains:

- valid `C2` closure
- valid `C3` support
- valid `C3` expansion confirmation

This note adds a stricter research filter on top of that base sequence:

- expansion-like `C3` should also have a small same-side wick
- and a directional body consistent with the move

## Shared Small-Wick Definition

The strict `Type A` path uses the shared helper defined in
[SMALL_WICK_RESEARCH_SPEC.md](/Users/njap/Downloads/garrett-trading-research/docs/SMALL_WICK_RESEARCH_SPEC.md).

Current hard-cap rule:

- bullish `C3`: `lower_wick / range <= threshold`
- bearish `C3`: `upper_wick / range <= threshold`

Current research default:

- `threshold = 0.25`

## Current Machine Form

### Bullish strict `Type A` expansion quality

- valid bullish `Type A`
- `C3` is bullish
- `lower_wick(C3) / range(C3) <= threshold`

### Bearish strict `Type A` expansion quality

- valid bearish `Type A`
- `C3` is bearish
- `upper_wick(C3) / range(C3) <= threshold`

## Intended Use

Use this stricter path for:

- real-data rarity counting
- manual review
- comparing base `Type A` sequences against stronger-quality expansion candles

Do not use it yet as:

- doctrine
- a hidden filter inside the base `Type A` detector
- a final execution law
