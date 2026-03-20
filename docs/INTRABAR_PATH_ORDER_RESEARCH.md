# Intrabar Path Order Research

## Purpose

This note preserves an emerging research observation about intrabar path order
inside Garrett-aligned swing setups.

It is intentionally a research artifact, not doctrine and not code logic.

## Boundary

This file does **not** claim:

- a locked Garrett rule
- a final entry model
- a machine-ready execution protocol
- that H4 OHLC bars alone prove true intrabar order

It records a path-order hypothesis that appears structurally coherent with:

- key-level anticipation
- swing-formation role separation
- the central role of wick quality in Garrett's framework

## Terminology

In this note:

- `OHLC` means a path label:
  - open -> high -> low -> close
- `OLHC` means a path label:
  - open -> low -> high -> close

These are idealized intrabar path labels, not a statement about how OHLC data
fields are stored.

## Why This Observation Emerged

The observation emerged because the current framework already implies that:

- price is anticipated in a direction once the right `IRL / FVG` is reached
- `C1` and `C2` have different functional roles
- wick quality often decides whether a setup is tradeable
- intrabar path order is what produces the wick

So if a setup is clean, it is reasonable to expect non-random candle-path
behavior rather than arbitrary motion.

## Current Structural Hypothesis

### Bullish path-order hypothesis

After a bullish `IRL / FVG` already exists:

- retracement `C1` often behaves like `OHLC`
  - price opens
  - trades higher first
  - then trades down into the bullish `IRL`
  - then closes
- reversal `C2` often behaves like `OLHC`
  - price opens
  - trades lower first
  - sweeps `C1` low / taps the bullish `IRL`
  - then reclaims higher and closes up

Implication:

- if `C2` closes back inside `C1` range, this supports `Type A`
- if `C2` keeps a controlled lower wick and expands strongly in the same
  candle, this supports `Type B`

### Bearish path-order hypothesis

After a bearish `IRL / FVG` already exists:

- retracement `C1` often behaves like `OLHC`
  - price opens
  - trades lower first
  - then trades up into the bearish `IRL`
  - then closes
- reversal `C2` often behaves like `OHLC`
  - price opens
  - trades higher first
  - sweeps `C1` high
  - then rejects lower and closes down

Implication:

- if `C2` only gives closure and the later expansion comes through `C3`, this
  supports `Type A`
- if `C2` itself expands away with a controlled upper wick, this supports
  `Type B`

## Why This Makes Sense

This hypothesis is coherent with the current doctrine already locked in the
repo:

- key level gives the directional expectation
- swing formation confirms the reversal structure
- wick quality distinguishes better expansion from lower-quality reversal
  behavior
- intrabar path is the hidden process that produces the wick

So path order, wick size, and expansion quality are logically connected.

## Evidence Buckets

### Bucket A: lower-timeframe-confirmed path observations

Use this bucket only when the path order is actually verified from lower
timeframe data, replay, or platform observation.

This is the stronger evidence class.

### Bucket B: H4 morphology-consistent observations

Use this bucket when the candle shape strongly suggests the path order, but H4
data alone does not prove the true intrabar sequence.

This is still useful research evidence, but weaker than lower-timeframe
confirmation.

## Current Observed Example Classes

### Reviewed integrated Type B examples

Current real-data review already confirmed:

- `8` integrated `Type B` examples on the preserved `500`-bar MT5 raw sample
- `3` bullish
- `5` bearish

Current repo-safe interpretation:

- these examples are structurally compatible with the path-order hypothesis
- but unless lower-timeframe confirmation is attached, they belong in Bucket B

### Reviewed Garrett illustration alignment

The current observation also appears consistent with Garrett's illustrated
logic:

- retracement-side candle into key level
- sweep/reversal-side candle
- later expansion / continuation candle where applicable

This is supportive context, not final proof.

## Support Classification

Use these status labels when collecting future examples:

- `supports_type_a`
  - path behavior appears to support the delayed-expansion `Type A` branch
- `supports_type_b`
  - path behavior appears to support the same-candle reversal-to-expansion
    `Type B` branch
- `supports_both`
  - the region appears compatible with both branches after the fact
- `failed_or_unclear`
  - path behavior is missing, contradictory, or cannot be classified with
    confidence

## Important Warning

H4 OHLC bars do **not** guarantee true intrabar order.

So:

- a candle may be morphology-consistent with `OHLC` or `OLHC`
- but the exact sequence still remains unproven without lower-timeframe
  confirmation

This note should therefore not be used to smuggle execution logic into the
closed-candle doctrine layer.

## Relation To Later Entry Logic

This observation may connect directly to Garrett's later entry model, but it is
not that model yet.

So the correct repo-safe posture is:

- preserve the observation
- do not promote it into doctrine
- do not hard-code it into detection logic yet
- revisit it once later source material defines the actual entry protocol

## Current Status

Current status:

- structurally coherent
- consistent with reviewed examples
- probably relevant to wick formation and execution quality
- not yet doctrine
- not yet code logic
