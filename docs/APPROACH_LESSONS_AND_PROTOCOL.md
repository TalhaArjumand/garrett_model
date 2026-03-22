# Approach Lessons And Protocol

## Purpose

This document records the mistakes made in earlier approach decisions, the
lessons learned from them, and the protocol that should govern future work.

It exists to keep process discipline explicit for:

- structural integrations
- stage-aware family interpretation
- left-to-right real-market review
- taxonomy stability
- future ML / DL label quality

This is a process and architecture document. It is not doctrine.

## Core Rule

Never let analogy replace structure, and never let structure replace stage.

## Runtime Realism Rule

All research, review, and implementation must simulate real-life market
behavior.

That means:

- read price left to right
- use only candles that would already be visible at that moment
- extract key levels only from prior confirmed structure
- update key-level state only when a later candle actually reaches, takes, or
  invalidates it
- open family windows only after a live key level is touched
- do not use refresh deltas, later candles, or retrospective knowledge as a
  substitute for live-sequence interpretation

## Approach Mistakes

### 1. Integration Boundary Was Assumed From Analogy

What went wrong:

- timing rules were transferred from one branch to another
- branch-specific lifecycle constraints were not always derived from the actual
  structure

Lesson:

- never transfer timing rules by analogy
- derive timing from the exact combination of:
  - key level type
  - family type
  - stage model

### 2. Primitive Truth And Integration Truth Were Mixed

What went wrong:

- a family primitive could be correct
- but the key-level integration around it could still be incomplete or wrong

Lesson:

- always separate:
  - primitive truth
  - key-level lifecycle truth
  - integration truth
  - stage truth

### 3. Structural Coverage Was Mistaken For Execution Meaning

What went wrong:

- integrated detections were sometimes discussed too loosely as if they were
  already execution-stage objects

Lesson:

- always separate:
  - structural family coverage
  - domain confirmation
  - first tradable candle
  - continuation stage

### 4. Taxonomy Drift Was Allowed

What went wrong:

- the old rare-`Type C` branch remained inside `Type C` too long
- that polluted strict `Type C` staging

Lesson:

- if staging changes, family identity must be questioned immediately
- strict family taxonomy must remain stage-clean

### 5. Refresh-Delta Scan Was Treated Like A Full Left-To-Right Audit

What went wrong:

- newly changed candles were summarized as if they represented a full-day
  left-to-right read

Lesson:

- refresh-delta is not a full-day liquidity audit
- live review must follow this order:
  1. liquidity inventory
  2. touch event
  3. family classification
  4. stage assignment

### 6. First-Touch Anchoring Was Described Too Casually

What went wrong:

- one candidate window was described as if it were the only valid alignment
- for preexisting key levels, both practical alignments can be valid

Lesson:

- for preexisting key levels, test both valid consecutive windows:
  - touch as `C1`
  - touch as `C2`
- let family rules decide afterward

### 7. Overlap Was Not Classified Early Enough

What went wrong:

- overlap cases were allowed to feel like contradictions

Lesson:

- explicitly classify overlap as one of:
  - valid overlap
  - invalid by stage
  - invalid by primitive
  - invalid by lifecycle
- do not force a winner unless source requires it

### 8. Evidence Status Was Not Always Labeled

What went wrong:

- some branches were discussed before stating whether they were:
  - chart-anchored
  - implementation-only
  - zero-match

Lesson:

- every branch must carry an evidence label:
  - `chart_anchored`
  - `implementation_verified_only`
  - `zero_match_current_window`

## Learned Lessons

### A. Key Level Comes Before Family

Always use this order:

1. key level first
2. touch second
3. family third
4. stage fourth

### B. Stage Is Part Of The Object

A family label alone is incomplete. The object must also carry:

- `family`
- `domain_confirmed_at`
- `first_tradable_candle`
- `continuation_from`
- `stage_status`
- `extension_kind`

### C. Families Must Remain Stage-Clean

Locked meaning:

- `Type A` -> first tradable candle = `C3`
- `Type B` -> first tradable candle = `C2`
- `Type C` -> first tradable candle = `C4`

And:

- `Type B additive extension` stays under `Type B`
- it is not a new family
- it must not contaminate strict `Type C`

### D. Timing Matrix Must Be Explicit Before Coding

For every new integration tranche, lock:

- `preexisting_before_c1`
- `fresh_on_c1_close`
- `fresh_on_c2_close`

And classify each as:

- `allowed`
- `excluded`
- `structurally_impossible`

### E. Evidence Must Be Layered

For any new branch or claim:

1. docs first if taxonomy changes
2. code second
3. tests third
4. stress test fourth
5. manual anchor fifth

### F. Real-Market Simulation Must Be Explicit

If the repo process does not resemble how the market would be seen in live
time, the process is wrong even if the later chart looks coherent.

Always ask:

- what key level was already live at this moment
- what state was it in
- what was the first actual interaction
- what family windows were truly eligible from that interaction
- what would have been knowable before the next candle printed

## Future-Proof Protocol

### Protocol 1: Before Any New Integration

Answer these before code:

1. What is the exact scope?
2. What is excluded?
3. What is the timing matrix?
4. What is the strict stage mapping?
5. What overlap is allowed?
6. What evidence status is expected?

If these are not written, do not code.

### Protocol 2: Keep Layers Separate

For every object, keep these layers separate:

Layer 1: primitive

- family conditions only

Layer 2: key-level lifecycle

- `IRL` / `ERL` extraction
- `resting` / `reached` / `taken` / `invalidated`

Layer 3: integration

- live key level + family

Layer 4: stage

- domain confirmed where
- first tradable candle where
- continuation from where

Layer 5: evidence

- chart-anchored
- implementation-only
- zero-match

### Protocol 3: Left-To-Right Live Review

Always use this order:

1. liquidity inventory
2. touch event
3. candidate windows
4. family classification
5. stage assignment

Never:

- classify family first
- then search backward for liquidity

And never:

- use later candles to justify an earlier key-level or family conclusion
- compress a multi-step live read into a single hindsight summary

### Protocol 4: Window Testing Rule

For preexisting key levels:

- test both valid consecutive alignments when applicable:
  - touch on `C1`
  - touch on `C2`

For fresh-on-`C1` levels:

- first eligible interaction starts at `C2`

For fresh-on-`C2`:

- do not allow unless structurally proven

### Protocol 5: Taxonomy Correction Rule

If a branch changes first tradable candle, ask immediately:

- does it still belong in the same family?

If not:

- reclassify before counting more examples

Do not allow stage drift to accumulate.

### Protocol 6: Branch Status Labels

Every branch or result must be labeled as one of:

- `strict_family`
- `family_extension`
- `research_only`
- `implementation_verified_only`
- `chart_anchored`
- `zero_match_current_window`

This prevents false certainty.

### Protocol 7: Anti-Drift Checklist Before Publish

Before commit/push, confirm:

- taxonomy is frozen
- timing matrix is explicit
- stage mapping is explicit
- overlap policy is explicit
- evidence status is explicit
- no old labels remain active in code
- docs and code match
- tests cover the new boundary

## Short Operating Rule

For every new unit:

`spec -> timing matrix -> code -> tests -> stress test -> manual anchor -> publish`

Not:

`idea -> code -> explanation later`

## Current Taxonomy Reference

Family:

- `type_a`
- `type_b`
- `type_c`

Extension kind:

- `none`
- `type_b_additive`
- `type_b_additive_c3_quality`

Strict `Type C` excludes both extension kinds.

## Related Documents

- [MANUAL_VALIDATION_PROTOCOL.md](/Users/njap/Downloads/garrett-trading-research/docs/MANUAL_VALIDATION_PROTOCOL.md)
- [REAL_DATA_REFRESH_PROTOCOL.md](/Users/njap/Downloads/garrett-trading-research/docs/REAL_DATA_REFRESH_PROTOCOL.md)
- [DOMAIN_STAGE_MODEL_SPEC.md](/Users/njap/Downloads/garrett-trading-research/docs/DOMAIN_STAGE_MODEL_SPEC.md)
- [REAL_OHLC_REVIEW_NOTES.md](/Users/njap/Downloads/garrett-trading-research/docs/REAL_OHLC_REVIEW_NOTES.md)
