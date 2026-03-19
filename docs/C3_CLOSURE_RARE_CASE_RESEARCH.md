# C3 Closure Rare-Case Research

## Purpose

This note records a rare real-data subtype hypothesis inside `Type C` swing
formation.

It is intentionally a research artifact, not doctrine.

## Boundary

This file does **not** create a new Garrett doctrine category.

It isolates a stronger-quality `Type C` subtype candidate that appeared on
same-source MT5 `XAUUSD 4H` data and should be counted and reviewed
separately.

## Hypothesis

Inside valid `Type C` closure cases, there may be a rare stronger subtype
where:

- `C2` sweeps the relevant edge of `C1`
- `C2` does not produce a Type A close back inside `C1` range
- `C2` closes strongly beyond the opposite boundary of `C1`
- `C3` still holds the correct half of `C2` through `EQ(C2)`
- `C3` closes strongly over the body of `C2`

## Current Machine Form

### Bullish rare-case subtype

- valid bullish `Type C`
- `close(C2) > high(C1)`
- `low(C3) > EQ(C2)`

### Bearish rare-case subtype

- valid bearish `Type C`
- `close(C2) < low(C1)`
- `high(C3) < EQ(C2)`

## Why This Is Research Only

Current evidence:

- comes from real MT5 examples
- is structurally interesting
- suggests stronger-quality `Type C`
- has now been manually confirmed on reviewed same-source MT5 examples

But it is still not enough to lock:

- a new doctrine category
- a final subtype taxonomy
- a mandatory rule inside all `Type C` cases

## Current Use

Use this subtype only for:

- counting rarity on real data
- checking whether downstream `C4` continuation also appears
- checking whether downstream `C4` also keeps expansion-quality wick behavior
- gathering more bullish and bearish examples
- comparing strong `Type C` against base `Type C`

Do not use it yet as:

- doctrine
- a standalone entry family
- a ranking rule

## Downstream Continuation Research

The rare subtype can also be checked through the same downstream `C4` logic
used by base `Type C`.

## Rare-Subtype `C3` Expansion-Quality Research

This is a stricter research refinement inside the rare subtype itself.

It does **not** change base `Type C` doctrine.

### Bullish rare-subtype `C3` expansion quality

- valid bullish rare-case `Type C`
- `low(C3) > EQ(C2)`
- small same-side wick on `C3`

### Bearish rare-subtype `C3` expansion quality

- valid bearish rare-case `Type C`
- `high(C3) < EQ(C2)`
- small same-side wick on `C3`

Interpretation:

- `C2` already sweeps and closes strongly beyond `C1`
- `C3` then accepts the correct half of `C2`
- controlled wick behavior on `C3` suggests that `C3` itself may already
  behave like an expansion-quality candle, rather than waiting for `C4`

This is still research only.

### Base rare-subtype `C4` continuation

- valid rare-case `Type C`
- bullish: `low(C4) > EQ(C3)`
- bearish: `high(C4) < EQ(C3)`

### Stricter rare-subtype `C4` expansion quality

This is a research-quality layer only.

- valid rare-case `Type C` `C4` continuation
- directional `C4` body
- small same-side wick on `C4`
- default wick threshold `0.25`

## Current Reviewed MT5 Status

Current reviewed status on the normalized `XAUUSD 4H` MT5 sample:

- base bullish `Type C` count = `4`
- base bearish `Type C` count = `3`
- bullish rare-case subtype count = `2`
- bearish rare-case subtype count = `0`
- bullish rare-case `C3` expansion-quality count = `2`
- bearish rare-case `C3` expansion-quality count = `0`
- bullish rare-case `C4` continuation count = `0`
- bearish rare-case `C4` continuation count = `0`
- bullish rare-case `C4` expansion-quality count = `0`
- bearish rare-case `C4` expansion-quality count = `0`

Two bullish rare-case subtype examples have now been manually confirmed against
the same-source MT5 chart.

So the current repo-safe status is:

- rare
- real
- testable
- not yet doctrine
