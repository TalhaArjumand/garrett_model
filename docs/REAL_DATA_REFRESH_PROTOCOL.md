# Real Data Refresh Protocol

## Purpose

This protocol standardizes how same-source MT5 data refreshes are handled in
this repo.

It exists to preserve:

- raw evidence
- canonical window discipline
- count-delta traceability
- manual chart verification
- clean separation between doctrine, helper geometry, and research

This is a process artifact, not doctrine.

## Scope

Current default scope:

- source: MT5 desktop export
- symbol: `XAUUSD`
- timeframe: `4H`
- canonical verifier window: latest `100` closed candles

If a future refresh uses a different symbol, timeframe, or window size, record
 that explicitly before comparing results.

## Required Artifacts

Each refresh must preserve all of the following:

1. prior raw snapshot
2. new raw snapshot
3. canonical raw source file
4. canonical normalized verifier file
5. count-delta summary
6. manual review notes for changed branches
7. final verdict by layer

## Directory Rules

Canonical files:

- `data/real_samples/xauusd_4h_mt5_raw.csv`
- `data/real_samples/xauusd_4h.csv`

Historical snapshots:

- `data/real_samples/raw_snapshots/`

Review log:

- `docs/REAL_OHLC_REVIEW_NOTES.md`

## Refresh Procedure

### 1. Preserve the previous raw source

Before replacing the canonical raw file:

- copy the current `xauusd_4h_mt5_raw.csv` into `raw_snapshots/`
- use a timestamped filename that reflects the last candle in that raw file

Example:

- `xauusd_4h_mt5_raw_until_2026_03_18_04_00.csv`

### 2. Preserve the new raw export

Copy the new MT5 export into `raw_snapshots/` under its original refresh name.

Example:

- `xauusd_4h_mt5_raw_2026_03_19.csv`

### 3. Promote the new raw export to canonical raw

Replace:

- `data/real_samples/xauusd_4h_mt5_raw.csv`

with the latest MT5 raw source.

### 4. Rebuild the canonical verifier input

Rebuild:

- `data/real_samples/xauusd_4h.csv`

using the latest `100` closed candles from the new raw source.

Normalization requirements:

- exact schema:
  - `symbol,timestamp,timeframe,open,high,low,close`
- timestamps sorted ascending
- closed candles only
- explicit timezone offset preserved in normalized output
- one symbol only
- one timeframe only

## Comparison Checklist

For every refresh, record:

### Window Bounds

- previous canonical first timestamp
- previous canonical last timestamp
- new canonical first timestamp
- new canonical last timestamp

### Count Deltas

At minimum, compare:

- doctrine-sequence counts
- strict expansion-quality counts
- continuation counts
- FVG counts and resting/reached state counts
- ERL counts and resting/taken state counts
- rare-subtype counts where applicable

### Newly Nonzero Branches

Explicitly identify any branch that moved:

- `0 -> positive`

These require highest-priority manual review.

### Rollover Removals

When a count drops, classify the drop as one of:

- left-edge rollover
- true state transition
- logic regression
- unresolved

Do not call a drop invalidation until rollover is ruled out.

### True State Transitions

For stateful objects, isolate exact candidates that changed state:

- `resting -> taken`
- `resting -> reached`

Record:

- candidate identity
- transition candle
- transition timestamp

## Manual Review Rules

Changed branches must be manually checked on the same-source MT5 chart before
they are treated as trustworthy.

Priority order:

1. newly nonzero doctrine branches
2. newly nonzero research branches
3. true state transitions
4. new resting inventory
5. window-rolloff explanations

For each manual check, record:

- timestamps
- candidate type
- result:
  - `match`
  - `rejected`
  - `rollover only`
- concise reason

## Final Verdict Template

Every refresh should end with a short verdict by layer:

### Doctrine Layer

- valid match / drift / unresolved

### Helper Geometry Layer

- valid match / state issue / unresolved

### Research Layer

- valid candidate movement / threshold issue / unresolved

## Failure Handling

If a refresh surfaces a problem:

### If tests fail

- stop
- do not trust the new counts
- fix or explain before review

### If count deltas are unexplained

- isolate candidate identities
- compare old vs new window membership
- determine whether the issue is rollover, transition, or regression

### If chart review disagrees with code

- record the mismatch
- do not silently adjust doctrine
- determine whether the bug is:
  - normalization
  - candidate logic
  - state logic
  - review interpretation

## Current Repo Policy

Current working policy for this repo:

- preserve raw MT5 evidence
- keep canonical verification window reviewable
- explain count movement before drawing conclusions
- require manual chart confirmation on materially changed branches
- keep doctrine, helper geometry, and research conclusions separate
