# Garrett Model Research

This repository contains the first doctrine-driven implementation units for the
Garrett trading research system.

## Current scope

The first completed unit includes:

- candle schema and validation
- derived candle geometry
- Garrett-specific `C2 closure` doctrine
- `C3 support`
- `C3 expansion confirmation`
- composed bullish and bearish `C1 -> C2 -> C3` sequence validators

## Project structure

- `docs/`
  - doctrine specs
- `src/gxt/`
  - implementation primitives
- `tests/`
  - unit tests
- `data/golden/`
  - controlled golden examples

## Verification

Run the test suite with:

```bash
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
```

## Current doctrine units

- `CANDLE_SPEC.md`
- `C2_CLOSURE_SPEC.md`
- `C3_EXPANSION_CONFIRMATION_SPEC.md`

## Next likely unit

- `C4` continuation logic
