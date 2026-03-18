# ERL Mechanical Proxy Spec

## Purpose

This spec defines a **research-layer mechanical proxy** for `ERL`
(`External Range Liquidity`).

It does **not** upgrade `ERL` selection into locked Garrett doctrine.

Its purpose is to let the project test a deterministic `ERL` approximation
without pretending Garrett has already provided a final mechanical selector.

## Evidence Posture

Current Garrett-reviewed doctrine locks:

- `ERL` is the external-side chart object in the universal model
- `ERL` can be represented by:
  - range high / range low
  - swing high / swing low
  - manipulation range
- in `IRL -> ERL`, `ERL` is the target side
- in `ERL -> IRL`, `ERL` is the reaction side

Current Garrett-reviewed doctrine does **not** lock:

- a deterministic `ERL` selection algorithm when multiple candidates exist

So this document is explicitly a **research hypothesis**, not doctrine.

## Supporting External References

These references support the hypothesis shape below, but are not the locking
criterion for this repo:

- ICT-oriented documentation consistently defines external liquidity as highs
  and lows outside a dealing range
- common ICT-style references also pair internal fair value gaps with external
  range highs / lows as target-side objects

These references are useful because they are directionally consistent with the
current Garrett-reviewed framework, but they do not replace direct Garrett
evidence.

## Research Hypothesis

For a selected dealing range, the active `ERL` proxy can be modeled as the
nearest relevant external boundary on the target side of that range.

At the current project stage, that means:

- first define the active dealing range
- then define its external boundaries
- then choose the side implied by the active universal-model direction

### H2 — Local swing-point ERL proxy

In bullish universal-model examples, a candidate mechanical `ERL` proxy may be
the high of a confirmed local swing-high candle `C`, where for consecutive
candles `B, C, D`:

- `high(C) > high(B)`
- `high(C) > high(D)`

In bearish universal-model examples, a candidate mechanical `ERL` proxy may be
the low of a confirmed local swing-low candle `C`, where for consecutive
candles `B, C, D`:

- `low(C) < low(B)`
- `low(C) < low(D)`

Status:

- research hypothesis only
- not locked Garrett doctrine

Important timing note:

- this proxy is only confirmed after the right-neighbor candle `D` closes
- so it is suitable for structural annotation, proxy targeting, and later
  testing
- it is not yet suitable as a locked real-time doctrinal selector

## Mechanical Proxy

### Step 1: Define the dealing range

The research proxy assumes a dealing range already exists.

At minimum, that range must provide:

- `range_high`
- `range_low`

How the dealing range itself is chosen is still outside this spec.

### Step 2: Define ERL candidates

For the current range, `ERL` candidates are:

- `range_high`
- `range_low`
- nearest swing high above `range_high`
- nearest swing low below `range_low`
- manipulation-range boundary, if the current chart model explicitly marks that
  boundary as external to the range

### Step 3: Choose direction side

For `IRL -> ERL`:

- bullish target side uses the upper external candidate set
- bearish target side uses the lower external candidate set

For `ERL -> IRL`:

- the reaction location is the external candidate already being reached or
  touched

### Step 4: Rank candidates

The current research ranking is:

1. the active dealing-range boundary itself
2. the nearest untouched external swing point beyond that boundary
3. a manipulation-range boundary, if the model is explicitly using a
   manipulation range

### Step 5: Proxy output

The proxy should return:

- `direction`
- `erl_type`
- `erl_price`
- `source_range_high`
- `source_range_low`
- `selection_reason`

## Why This Is Only A Proxy

This proxy is intentionally weaker than doctrine because Garrett has not yet
provided a final explicit rule for:

- how the active dealing range is selected
- how multiple external candidates are ranked in every case
- when a manipulation range overrides a simple range high / low

So this spec should be treated as:

- deterministic enough to test
- not strong enough to call doctrine

## What Is Locked

Locked in this spec:

- any ERL mechanic beyond current Garrett doctrine is a research hypothesis
- the safest first proxy treats ERL as an external boundary / external swing
  object outside a selected range
- the proxy must keep the distinction between:
  - doctrine
  - research approximation

## What Is Not Yet Locked

Not yet locked:

1. final dealing-range selection
2. final swing-point definition for ERL ranking
3. manipulation-range override logic
4. whether the nearest external candidate is always the correct target
5. whether higher-timeframe bias or time windows should change ranking

## Implementation Status

Implementation status: not started.

If implemented later, it must live in the repo as:

- research layer
- clearly separate from locked doctrine detectors

## Non-goals

This spec does not yet define:

- final Garrett `ERL` doctrine
- production `ERL` code
- target-confidence scoring
- full universal-model range selection
