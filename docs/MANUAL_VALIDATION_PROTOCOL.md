# Manual Validation Protocol

## Purpose

This protocol defines how to manually validate the current repo state against
the MT5 chart without mixing:

- structural/key-level coverage
- family confirmation
- tradable-stage timing
- continuation-stage timing

It exists because the repo now has both:

- structural integrations
- family-general domain/stage contracts

and those must be reviewed separately.

## Scope

This protocol is for:

- manual chart review
- doctrine-faithfulness review
- stage-timing review

It is not for:

- profitability review
- backtesting
- lower-timeframe execution validation
- target/stop evaluation

## First Principle

Manual validation should begin from the real data already preserved in the
repo.

Do not begin with:

- abstract family discussion
- fresh chart hunting
- later roadmap objects

Begin with:

- the existing reviewed `XAUUSD 4H` real sample
- the already extracted structural matches
- the locked family/stage contract

## Real-Market Simulation Rule

Manual review must simulate live-market behavior.

That means:

- read candles left to right
- use only what was already confirmed by prior candles
- extract key levels before family
- wait for a real touch before opening family windows
- assign family before assigning stage
- never use hindsight to force an earlier family label

## Live Review Order

Use this exact left-to-right review order:

1. Key level first

- scan left to right
- extract `IRL` / `ERL` only from prior candles
- record:
  - level / zone
  - `confirmed_at`
  - state

2. Touch second

- do not ask family before a live key level is touched
- once touched, open the candidate sequence windows

3. Family third

- test only around that live touch:
  - `Type A`
  - `Type B`
  - `Type B additive extension`
  - strict `Type C`

4. Stage fourth

- after family is known, assign:
  - `domain_confirmed_at`
  - `first_tradable_candle`
  - continuation stage

## Refresh Boundary Warning

A refresh-delta scan must never be used as a full-day left-to-right
conclusion.

Keep these separate:

- refresh-delta scan:
  - what changed because of the newly added candles
- full-day audit:
  - what liquidity and family structure exists across the whole reviewed day

## First Manual Test

The first manual test is:

- `Type A`

Reason:

- it cleanly separates domain confirmation from trade timing
- `C2` confirms the domain
- `C3` is the first tradable candle
- `C4` is only continuation after full `C3` confirmation

That makes `Type A` the best family for learning the distinction between:

- structural match
- domain confirmation
- first tradable stage
- continuation stage

## Current Review Objects

Manual validation should currently cover two layers:

1. Structural integration layer

- `IRL -> Type A`
- `IRL -> Type B`
- `IRL -> base Type C`
- `IRL -> Type B additive extension`
- `IRL -> Type B additive extension C3 quality`
- `ERL -> Type A`
- `ERL -> Type B`

2. Domain/stage layer

- `Type A`
  - domain valid on `C2` close
  - first tradable candle = `C3`
  - continuation stage = `C4` only after full `C3` confirmation
- `Type B`
  - domain valid on `C2`
  - first tradable candle = `C2`
- `Type C`
  - domain confirmed on `C3` close
  - first tradable candle = `C4`

Strict `Type C` excludes:

- `type_b_additive`
- `type_b_additive_c3_quality`

## Source Files

Use these repo files while reviewing:

- [REAL_OHLC_REVIEW_NOTES.md](/Users/njap/Downloads/garrett-trading-research/docs/REAL_OHLC_REVIEW_NOTES.md)
- [DOMAIN_STAGE_MODEL_SPEC.md](/Users/njap/Downloads/garrett-trading-research/docs/DOMAIN_STAGE_MODEL_SPEC.md)
- [EXPANSION_ENTRY_SPEC.md](/Users/njap/Downloads/garrett-trading-research/docs/EXPANSION_ENTRY_SPEC.md)
- [SWING_FORMATION_SPEC.md](/Users/njap/Downloads/garrett-trading-research/docs/SWING_FORMATION_SPEC.md)

## Review Order

Always review in this order:

1. Known positive real-data `Type A` examples
2. Known overlap `Type A` examples
3. Known near-miss / exclusion `Type A` examples
4. Only then move to other families
5. New chart-discovered candidates last

This prevents reviewing ambiguous new cases before the locked baseline is
stable in your eye.

## Real-Data Starting Point

Use the real sample already in the repo first:

- raw snapshot:
  [xauusd_4h_mt5_raw_2026_03_19.csv](/Users/njap/Downloads/garrett-trading-research/data/real_samples/raw_snapshots/xauusd_4h_mt5_raw_2026_03_19.csv)
- canonical verifier window:
  [xauusd_4h.csv](/Users/njap/Downloads/garrett-trading-research/data/real_samples/xauusd_4h.csv)

## First Real-Data Test Set: Type A

Start with these exact reviewed examples.

### 1. IRL -> Type A Positive

- direction: `bullish`
- context: `IRL`
- timing: `preexisting_before_c1`
- IRL zone: `4712.85 -> 4745.49`
- IRL confirmed: `2026-02-03 04:00 +05:00`
- `C1 = 2026-02-05 20:00 +05:00`
- `C2 = 2026-02-06 00:00 +05:00`
- `C3 = 2026-02-06 04:00 +05:00`

What to verify:

- `C2` sweeps below `low(C1)`
- `C2` closes back inside full `C1` range
- mark `EQ(C2)`
- `low(C3) > EQ(C2)`
- `close(C3) > high(C2)`

Stage check:

- `Type A` domain becomes valid on `C2` close
- `C3` is the first tradable candle
- only after full `C3` confirmation does `C4` become continuation-eligible

### 2. IRL -> Type A Overlap Case

- direction: `bearish`
- context: `IRL`
- timing: `preexisting_before_c1`
- IRL zone: `5112.61 -> 5146.09`
- IRL confirmed: `2026-03-12 20:00 +05:00`
- `C1 = 2026-03-13 00:00 +05:00`
- `C2 = 2026-03-13 04:00 +05:00`
- `C3 = 2026-03-13 08:00 +05:00`

What to verify:

- `C2` sweeps above `high(C1)`
- `C2` closes back inside full `C1` range
- mark `EQ(C2)`
- `high(C3) < EQ(C2)`
- `close(C3) < low(C2)`

Stage check:

- this is still `Type A` domain on `C2` close
- `C3` is still the first tradable `Type A` candle
- this region also overlaps structural `Type B`
- overlap must be recorded, not erased

### 3. ERL -> Type A Positive

- direction: `bullish`
- context: `ERL`
- timing: `preexisting_before_c1`
- ERL kind: `old_low`
- ERL level: `5122.39`
- ERL confirmed: `2026-03-04 12:00 +05:00`
- `C1 = 2026-03-04 16:00 +05:00`
- `C2 = 2026-03-04 20:00 +05:00`
- `C3 = 2026-03-05 00:00 +05:00`

What to verify:

- ERL is still resting before `C1`
- `C2` sweeps below `low(C1)`
- `C2` closes back inside full `C1` range
- mark `EQ(C2)`
- `low(C3) > EQ(C2)`
- `close(C3) > high(C2)`

Stage check:

- exact same family-stage logic as `IRL -> Type A`
- only the key-level context changes

### 4. Type A Near-Miss

- use the already reviewed bearish near-miss in
  [REAL_OHLC_REVIEW_NOTES.md](/Users/njap/Downloads/garrett-trading-research/docs/REAL_OHLC_REVIEW_NOTES.md)

Why include it:

- to train the eye not to promote every good-looking `C2` close into full
  valid `Type A`
- to separate:
  - `Type A domain alive`
  - from
  - `full Type A confirmation completed`

## Manual Review Workflow

### Step 1. Pick One Example

Start from a reviewed example in:

- `docs/REAL_OHLC_REVIEW_NOTES.md`

For each candidate, note:

- context: `IRL` or `ERL`
- family: `Type A`, `Type B`, `Type C`
- subtype if any
- `C1`
- `C2`
- `C3`
- `C4` if relevant

### Step 2. Open the Exact Chart

On MT5:

- symbol: `XAUUSD`
- timeframe: `4H`

Then move to the exact timestamps listed in the review note.

### Step 3. Mark the Sequence

Mark on chart:

- `C1`
- `C2`
- `C3`
- `C4` if relevant

Do not start with “does it look good?”
Start with the exact candle identities.

### Step 4. Mark the Key Level

If context is `IRL`:

- mark the FVG zone
- verify when it was confirmed
- verify whether it was still resting before the allowed sequence timing
- verify that it was not already invalidated

If context is `ERL`:

- mark the old high / old low
- verify when the swing became confirmed
- verify whether it was still resting / untaken before the allowed sequence timing

### Step 5. Verify Timing Class

Classify the key-level timing explicitly as one of:

- `preexisting_before_c1`
- `fresh_on_c1_close`
- `fresh_on_c2_close`
- `not_eligible`

Do not leave timing implicit.

### Step 6. Verify Structural Family

#### Type A

Check:

- `C2` sweeps the relevant edge of `C1`
- `C2` closes back inside the full range of `C1`
- `C3` respects the correct side of `EQ(C2)`
- `C3` closes beyond the opposite edge of `C2` in the expected direction

Strict quality layer if relevant:

- `C3` has small same-side wick

#### Type B

Check:

- `C2` sweeps the relevant edge of `C1`
- `C2` has the correct body direction
- `C2` reclaims / rejects correctly relative to `C1`
- `C2` has small same-side wick

#### Type C

Check:

- `C2` sweeps the relevant edge of `C1`
- `C2` does not form valid `Type A`
- `C3` is the first confirming closure event

Rare subtype if relevant:

- `C2.close` exceeds the relevant `C1` body/range condition already locked
- `C3` respects the required side of `EQ(C2)`

Rare `C3` quality if relevant:

- `C3` has small same-side wick

### Step 7. Verify Domain/Stage Mapping

This is a separate review from structural pass/fail.

#### Type A stage review

Mark:

- `domain_confirmed_at = C2_close`
- `first_tradable_candle = C3`

Then ask:

- did `C2` closure already place the sequence in Type A domain?
- is `C3` the reviewed trade candle candidate?
- only after full `C3` confirmation, does `C4` become continuation-eligible?

#### Type B stage review

Mark:

- `domain_confirmed_at = C2`
- `first_tradable_candle = C2`

Then ask:

- does the same candle that confirms the Type B story also become the trade candle?

#### Type C stage review

Mark:

- `domain_confirmed_at = C3_close`
- `first_tradable_candle = C4`

Then ask:

- is `C3` the closure/formation candle rather than the trade candle?
- does the first actual trade domain begin only at `C4`?

### Step 8. Record Overlap Honestly

If the same region supports multiple predicates, record it.

Examples:

- `Type B` plus `Type A pending after C2`
- base `Type B` plus `Type B additive extension`
- `Type B additive extension` plus `Type B additive extension C3 quality`

Do not force a winner.

### Step 9. Record One Outcome

Use one of:

- `confirmed`
- `rejected`
- `unclear`
- `needs lower timeframe`

## Minimum Review Template

For each manually reviewed example, record:

- context
- family
- subtype
- direction
- timing class
- touch type
- structural result
- stage result
- overlap result
- notes

## What Counts as a Good Manual Test

A good manual test answers all of these:

1. Was the key level actually live and eligible?
2. Did the family predicate actually form?
3. Does the stage mapping match the reviewed doctrine?
4. Is this a clean pass, a near-miss, or an overlap case?

## What Not To Do

Do not:

- start from target logic
- start from lower-timeframe entry logic
- force one family winner when overlap is real
- confuse “looks tradeable” with “passes the current structural predicate”
- confuse structural pass with first tradable candle timing

## Recommended Practical Testing Sequence

Use this exact order:

1. Re-check a known `Type A` positive example
2. Re-check a known `Type B` positive example
3. Re-check a known `Type C` positive example
4. Re-check one overlap case
5. Re-check one near-miss or rejection case
6. Only then inspect fresh chart-discovered candidates

## Current Goal

The current goal of manual testing is:

- validate current integrations as structural coverage
- validate the family-general domain/stage contract against reviewed examples

The current goal is not:

- live execution validation
- target doctrine
- stop doctrine
- ML feature generation
