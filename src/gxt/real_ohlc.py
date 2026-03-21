from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .candles import Candle
from .erl_proxy import detect_erl_candidates
from .fvg import detect_fvg_candidates, is_bearish_fvg, is_bullish_fvg
from .key_level_integration import (
    count_external_to_internal_type_a_expansion_quality_sequences,
    count_external_to_internal_type_a_sequences,
    count_external_to_internal_type_b_sequences,
    count_internal_to_external_type_a_expansion_quality_sequences,
    count_internal_to_external_type_a_sequences,
    count_internal_to_external_type_b_sequences,
    count_internal_to_external_type_c_sequences,
    count_internal_to_external_type_c_rare_case_sequences,
    count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences,
)
from .sequence_primitives import (
    has_bearish_c4_after_c3_closure_candidate,
    has_bearish_c4_after_c3_closure_expansion_quality_candidate,
    has_bearish_c4_continuation_candidate,
    has_bullish_c4_continuation_candidate,
    has_bullish_c4_after_c3_closure_candidate,
    has_bullish_c4_after_c3_closure_expansion_quality_candidate,
    is_bearish_c2_reversal_to_expansion,
    is_valid_bearish_c2_sequence_expansion_quality,
    is_bearish_c3_closure,
    is_valid_bearish_c2_sequence,
    is_bullish_c2_reversal_to_expansion,
    is_valid_bullish_c2_sequence_expansion_quality,
    is_bullish_c3_closure,
    is_valid_bullish_c2_sequence,
)
from .swing_research import (
    has_bearish_rare_c3_closure_expansion_quality_candidate,
    has_bearish_c4_after_rare_c3_closure_candidate,
    has_bearish_c4_after_rare_c3_closure_expansion_quality_candidate,
    has_bullish_rare_c3_closure_expansion_quality_candidate,
    has_bullish_c4_after_rare_c3_closure_candidate,
    has_bullish_c4_after_rare_c3_closure_expansion_quality_candidate,
    is_bearish_rare_c3_closure_subtype,
    is_bullish_rare_c3_closure_subtype,
)


@dataclass(frozen=True)
class RealSampleReport:
    symbol: str
    timeframe: str
    candle_count: int
    gap_count: int
    bullish_sequence_count: int
    bearish_sequence_count: int
    bullish_sequence_expansion_quality_count: int
    bearish_sequence_expansion_quality_count: int
    bullish_internal_to_external_type_a_count: int
    bearish_internal_to_external_type_a_count: int
    bullish_internal_to_external_type_a_expansion_quality_count: int
    bearish_internal_to_external_type_a_expansion_quality_count: int
    bullish_external_to_internal_type_a_count: int
    bearish_external_to_internal_type_a_count: int
    bullish_external_to_internal_type_a_expansion_quality_count: int
    bearish_external_to_internal_type_a_expansion_quality_count: int
    bullish_external_to_internal_type_b_count: int
    bearish_external_to_internal_type_b_count: int
    bullish_internal_to_external_type_b_count: int
    bearish_internal_to_external_type_b_count: int
    bullish_internal_to_external_type_c_count: int
    bearish_internal_to_external_type_c_count: int
    bullish_internal_to_external_type_c_rare_case_count: int
    bearish_internal_to_external_type_c_rare_case_count: int
    bullish_internal_to_external_type_c_rare_case_c3_expansion_quality_count: int
    bearish_internal_to_external_type_c_rare_case_c3_expansion_quality_count: int
    bullish_c4_candidate_count: int
    bearish_c4_candidate_count: int
    bullish_case_b_candidate_count: int
    bearish_case_b_candidate_count: int
    bullish_c3_closure_count: int
    bearish_c3_closure_count: int
    bullish_c3_closure_rare_case_count: int
    bearish_c3_closure_rare_case_count: int
    bullish_c3_closure_rare_case_c3_expansion_quality_count: int
    bearish_c3_closure_rare_case_c3_expansion_quality_count: int
    bullish_c3_closure_c4_candidate_count: int
    bearish_c3_closure_c4_candidate_count: int
    bullish_c3_closure_c4_expansion_quality_count: int
    bearish_c3_closure_c4_expansion_quality_count: int
    bullish_c3_closure_rare_case_c4_candidate_count: int
    bearish_c3_closure_rare_case_c4_candidate_count: int
    bullish_c3_closure_rare_case_c4_expansion_quality_count: int
    bearish_c3_closure_rare_case_c4_expansion_quality_count: int
    bullish_fvg_count: int
    bearish_fvg_count: int
    fvg_candidate_count: int
    fvg_resting_candidate_count: int
    fvg_reached_candidate_count: int
    fvg_invalidated_candidate_count: int
    bullish_resting_fvg_count: int
    bearish_resting_fvg_count: int
    bullish_reached_fvg_count: int
    bearish_reached_fvg_count: int
    bullish_invalidated_fvg_count: int
    bearish_invalidated_fvg_count: int
    erl_candidate_count: int
    erl_resting_candidate_count: int
    erl_old_high_count: int
    erl_old_low_count: int
    erl_equal_highs_count: int
    erl_equal_lows_count: int
    erl_resting_old_high_count: int
    erl_resting_old_low_count: int
    erl_resting_equal_highs_count: int
    erl_resting_equal_lows_count: int


def load_candles_from_csv(csv_path: Path) -> list[Candle]:
    rows: list[Candle] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        expected = ["symbol", "timestamp", "timeframe", "open", "high", "low", "close"]
        if reader.fieldnames != expected:
            raise ValueError(
                f"CSV columns must be exactly {expected}, got {reader.fieldnames}"
            )

        for row in reader:
            rows.append(
                Candle.from_dict(
                    {
                        "symbol": row["symbol"],
                        "timestamp": row["timestamp"],
                        "timeframe": row["timeframe"],
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "is_closed": True,
                    }
                )
            )

    return rows


def find_timestamp_gaps(candles: list[Candle]) -> list[tuple[Candle, Candle]]:
    gaps: list[tuple[Candle, Candle]] = []
    for previous, current in zip(candles, candles[1:]):
        if current.timestamp - previous.timestamp != previous.duration:
            gaps.append((previous, current))
    return gaps


def iter_triples(candles: Iterable[Candle]) -> Iterable[tuple[Candle, Candle, Candle]]:
    candles = list(candles)
    for idx in range(len(candles) - 2):
        yield candles[idx], candles[idx + 1], candles[idx + 2]


def iter_pairs(candles: Iterable[Candle]) -> Iterable[tuple[Candle, Candle]]:
    candles = list(candles)
    for idx in range(len(candles) - 1):
        yield candles[idx], candles[idx + 1]


def iter_quads(candles: Iterable[Candle]) -> Iterable[tuple[Candle, Candle, Candle, Candle]]:
    candles = list(candles)
    for idx in range(len(candles) - 3):
        yield candles[idx], candles[idx + 1], candles[idx + 2], candles[idx + 3]


def count_valid_sequences(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        try:
            if is_valid_bullish_c2_sequence(c1, c2, c3):
                bullish += 1
            if is_valid_bearish_c2_sequence(c1, c2, c3):
                bearish += 1
        except ValueError:
            # Real OHLC samples can contain weekend gaps or vendor-specific
            # timestamp shifts; those windows are not valid sequence candidates.
            continue
    return bullish, bearish


def count_valid_sequences_expansion_quality(
    candles: list[Candle],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        try:
            if is_valid_bullish_c2_sequence_expansion_quality(
                c1,
                c2,
                c3,
                max_lower_wick_fraction=max_wick_fraction,
            ):
                bullish += 1
            if is_valid_bearish_c2_sequence_expansion_quality(
                c1,
                c2,
                c3,
                max_upper_wick_fraction=max_wick_fraction,
            ):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c4_candidates(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3, c4 in iter_quads(candles):
        try:
            if has_bullish_c4_continuation_candidate(c1, c2, c3, c4):
                bullish += 1
            if has_bearish_c4_continuation_candidate(c1, c2, c3, c4):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_case_b_candidates(
    candles: list[Candle],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2 in iter_pairs(candles):
        try:
            if is_bullish_c2_reversal_to_expansion(
                c1,
                c2,
                max_lower_wick_fraction=max_wick_fraction,
            ):
                bullish += 1
            if is_bearish_c2_reversal_to_expansion(
                c1,
                c2,
                max_upper_wick_fraction=max_wick_fraction,
            ):
                bearish += 1
        except ValueError:
            # Weekend gaps and invalid runtime windows are not candidate pairs.
            continue
    return bullish, bearish


def count_c3_closures(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        try:
            if is_bullish_c3_closure(c1, c2, c3):
                bullish += 1
            if is_bearish_c3_closure(c1, c2, c3):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c3_closure_rare_cases(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        try:
            if is_bullish_rare_c3_closure_subtype(c1, c2, c3):
                bullish += 1
            if is_bearish_rare_c3_closure_subtype(c1, c2, c3):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c3_closure_rare_case_c3_expansion_quality_candidates(
    candles: list[Candle],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        try:
            if has_bullish_rare_c3_closure_expansion_quality_candidate(
                c1,
                c2,
                c3,
                max_lower_wick_fraction=max_wick_fraction,
            ):
                bullish += 1
            if has_bearish_rare_c3_closure_expansion_quality_candidate(
                c1,
                c2,
                c3,
                max_upper_wick_fraction=max_wick_fraction,
            ):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c3_closure_c4_candidates(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3, c4 in iter_quads(candles):
        try:
            if has_bullish_c4_after_c3_closure_candidate(c1, c2, c3, c4):
                bullish += 1
            if has_bearish_c4_after_c3_closure_candidate(c1, c2, c3, c4):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c3_closure_c4_expansion_quality_candidates(
    candles: list[Candle],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3, c4 in iter_quads(candles):
        try:
            if has_bullish_c4_after_c3_closure_expansion_quality_candidate(
                c1,
                c2,
                c3,
                c4,
                max_lower_wick_fraction=max_wick_fraction,
            ):
                bullish += 1
            if has_bearish_c4_after_c3_closure_expansion_quality_candidate(
                c1,
                c2,
                c3,
                c4,
                max_upper_wick_fraction=max_wick_fraction,
            ):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c3_closure_rare_case_c4_candidates(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3, c4 in iter_quads(candles):
        try:
            if has_bullish_c4_after_rare_c3_closure_candidate(c1, c2, c3, c4):
                bullish += 1
            if has_bearish_c4_after_rare_c3_closure_candidate(c1, c2, c3, c4):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_c3_closure_rare_case_c4_expansion_quality_candidates(
    candles: list[Candle],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3, c4 in iter_quads(candles):
        try:
            if has_bullish_c4_after_rare_c3_closure_expansion_quality_candidate(
                c1,
                c2,
                c3,
                c4,
                max_lower_wick_fraction=max_wick_fraction,
            ):
                bullish += 1
            if has_bearish_c4_after_rare_c3_closure_expansion_quality_candidate(
                c1,
                c2,
                c3,
                c4,
                max_upper_wick_fraction=max_wick_fraction,
            ):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_fvgs(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        try:
            if is_bullish_fvg(c1, c2, c3):
                bullish += 1
            if is_bearish_fvg(c1, c2, c3):
                bearish += 1
        except ValueError:
            continue
    return bullish, bearish


def count_fvg_candidates(candles: list[Candle]) -> dict[str, int]:
    candidates = detect_fvg_candidates(candles)
    counts = {
        "fvg_candidate_count": len(candidates),
        "fvg_resting_candidate_count": 0,
        "fvg_reached_candidate_count": 0,
        "fvg_invalidated_candidate_count": 0,
        "bullish_resting_fvg_count": 0,
        "bearish_resting_fvg_count": 0,
        "bullish_reached_fvg_count": 0,
        "bearish_reached_fvg_count": 0,
        "bullish_invalidated_fvg_count": 0,
        "bearish_invalidated_fvg_count": 0,
    }

    for candidate in candidates:
        if candidate.is_resting:
            counts["fvg_resting_candidate_count"] += 1
            if candidate.direction == "bullish":
                counts["bullish_resting_fvg_count"] += 1
            elif candidate.direction == "bearish":
                counts["bearish_resting_fvg_count"] += 1
        if candidate.is_reached:
            counts["fvg_reached_candidate_count"] += 1
            if candidate.direction == "bullish":
                counts["bullish_reached_fvg_count"] += 1
            elif candidate.direction == "bearish":
                counts["bearish_reached_fvg_count"] += 1
        if candidate.is_invalidated:
            counts["fvg_invalidated_candidate_count"] += 1
            if candidate.direction == "bullish":
                counts["bullish_invalidated_fvg_count"] += 1
            elif candidate.direction == "bearish":
                counts["bearish_invalidated_fvg_count"] += 1

    return counts


def count_erl_candidates(
    candles: list[Candle],
    *,
    equal_tolerance: float | None = None,
) -> dict[str, int]:
    candidates = detect_erl_candidates(candles, equal_tolerance=equal_tolerance)
    counts = {
        "erl_candidate_count": len(candidates),
        "erl_resting_candidate_count": 0,
        "erl_old_high_count": 0,
        "erl_old_low_count": 0,
        "erl_equal_highs_count": 0,
        "erl_equal_lows_count": 0,
        "erl_resting_old_high_count": 0,
        "erl_resting_old_low_count": 0,
        "erl_resting_equal_highs_count": 0,
        "erl_resting_equal_lows_count": 0,
    }

    for candidate in candidates:
        if candidate.kind == "old_high":
            counts["erl_old_high_count"] += 1
            if candidate.is_resting:
                counts["erl_resting_old_high_count"] += 1
        elif candidate.kind == "old_low":
            counts["erl_old_low_count"] += 1
            if candidate.is_resting:
                counts["erl_resting_old_low_count"] += 1
        elif candidate.kind == "equal_highs":
            counts["erl_equal_highs_count"] += 1
            if candidate.is_resting:
                counts["erl_resting_equal_highs_count"] += 1
        elif candidate.kind == "equal_lows":
            counts["erl_equal_lows_count"] += 1
            if candidate.is_resting:
                counts["erl_resting_equal_lows_count"] += 1
        if candidate.is_resting:
            counts["erl_resting_candidate_count"] += 1

    return counts


def build_real_sample_report(
    candles: list[Candle],
    *,
    erl_equal_tolerance: float | None = None,
    c3_expansion_max_wick_fraction: float = 0.25,
    case_b_max_wick_fraction: float = 0.25,
    c4_expansion_max_wick_fraction: float = 0.25,
) -> RealSampleReport:
    if not candles:
        raise ValueError("real sample cannot be empty")

    symbols = {candle.symbol for candle in candles}
    timeframes = {candle.timeframe for candle in candles}
    if len(symbols) != 1:
        raise ValueError(f"real sample must contain exactly one symbol, got {sorted(symbols)}")
    if len(timeframes) != 1:
        raise ValueError(
            f"real sample must contain exactly one timeframe, got {sorted(timeframes)}"
        )

    gaps = find_timestamp_gaps(candles)
    bullish, bearish = count_valid_sequences(candles)
    (
        bullish_sequence_expansion_quality,
        bearish_sequence_expansion_quality,
    ) = count_valid_sequences_expansion_quality(
        candles,
        max_wick_fraction=c3_expansion_max_wick_fraction,
    )
    (
        bullish_internal_to_external_type_a,
        bearish_internal_to_external_type_a,
    ) = count_internal_to_external_type_a_sequences(candles)
    (
        bullish_external_to_internal_type_a,
        bearish_external_to_internal_type_a,
    ) = count_external_to_internal_type_a_sequences(candles)
    (
        bullish_internal_to_external_type_a_expansion_quality,
        bearish_internal_to_external_type_a_expansion_quality,
    ) = count_internal_to_external_type_a_expansion_quality_sequences(
        candles,
        max_wick_fraction=c3_expansion_max_wick_fraction,
    )
    (
        bullish_external_to_internal_type_a_expansion_quality,
        bearish_external_to_internal_type_a_expansion_quality,
    ) = count_external_to_internal_type_a_expansion_quality_sequences(
        candles,
        max_wick_fraction=c3_expansion_max_wick_fraction,
    )
    (
        bullish_external_to_internal_type_b,
        bearish_external_to_internal_type_b,
    ) = count_external_to_internal_type_b_sequences(
        candles,
        max_wick_fraction=case_b_max_wick_fraction,
    )
    (
        bullish_internal_to_external_type_b,
        bearish_internal_to_external_type_b,
    ) = count_internal_to_external_type_b_sequences(
        candles,
        max_wick_fraction=case_b_max_wick_fraction,
    )
    (
        bullish_internal_to_external_type_c,
        bearish_internal_to_external_type_c,
    ) = count_internal_to_external_type_c_sequences(candles)
    (
        bullish_internal_to_external_type_c_rare_case,
        bearish_internal_to_external_type_c_rare_case,
    ) = count_internal_to_external_type_c_rare_case_sequences(candles)
    (
        bullish_internal_to_external_type_c_rare_case_c3_expansion_quality,
        bearish_internal_to_external_type_c_rare_case_c3_expansion_quality,
    ) = count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences(
        candles,
        max_wick_fraction=c3_expansion_max_wick_fraction,
    )
    bullish_c4, bearish_c4 = count_c4_candidates(candles)
    bullish_case_b, bearish_case_b = count_case_b_candidates(
        candles,
        max_wick_fraction=case_b_max_wick_fraction,
    )
    bullish_c3_closure, bearish_c3_closure = count_c3_closures(candles)
    bullish_c3_closure_rare, bearish_c3_closure_rare = count_c3_closure_rare_cases(candles)
    (
        bullish_c3_closure_rare_c3_expansion_quality,
        bearish_c3_closure_rare_c3_expansion_quality,
    ) = count_c3_closure_rare_case_c3_expansion_quality_candidates(
        candles,
        max_wick_fraction=c3_expansion_max_wick_fraction,
    )
    bullish_c3_closure_c4, bearish_c3_closure_c4 = count_c3_closure_c4_candidates(candles)
    (
        bullish_c3_c4_expansion_quality,
        bearish_c3_c4_expansion_quality,
    ) = count_c3_closure_c4_expansion_quality_candidates(
        candles,
        max_wick_fraction=c4_expansion_max_wick_fraction,
    )
    (
        bullish_c3_rare_c4,
        bearish_c3_rare_c4,
    ) = count_c3_closure_rare_case_c4_candidates(candles)
    (
        bullish_c3_rare_c4_expansion_quality,
        bearish_c3_rare_c4_expansion_quality,
    ) = count_c3_closure_rare_case_c4_expansion_quality_candidates(
        candles,
        max_wick_fraction=c4_expansion_max_wick_fraction,
    )
    bullish_fvg, bearish_fvg = count_fvgs(candles)
    fvg_candidate_counts = count_fvg_candidates(candles)
    erl_counts = count_erl_candidates(candles, equal_tolerance=erl_equal_tolerance)
    first = candles[0]
    return RealSampleReport(
        symbol=first.symbol,
        timeframe=first.timeframe,
        candle_count=len(candles),
        gap_count=len(gaps),
        bullish_sequence_count=bullish,
        bearish_sequence_count=bearish,
        bullish_sequence_expansion_quality_count=bullish_sequence_expansion_quality,
        bearish_sequence_expansion_quality_count=bearish_sequence_expansion_quality,
        bullish_internal_to_external_type_a_count=bullish_internal_to_external_type_a,
        bearish_internal_to_external_type_a_count=bearish_internal_to_external_type_a,
        bullish_internal_to_external_type_a_expansion_quality_count=(
            bullish_internal_to_external_type_a_expansion_quality
        ),
        bearish_internal_to_external_type_a_expansion_quality_count=(
            bearish_internal_to_external_type_a_expansion_quality
        ),
        bullish_external_to_internal_type_a_count=bullish_external_to_internal_type_a,
        bearish_external_to_internal_type_a_count=bearish_external_to_internal_type_a,
        bullish_external_to_internal_type_a_expansion_quality_count=(
            bullish_external_to_internal_type_a_expansion_quality
        ),
        bearish_external_to_internal_type_a_expansion_quality_count=(
            bearish_external_to_internal_type_a_expansion_quality
        ),
        bullish_external_to_internal_type_b_count=bullish_external_to_internal_type_b,
        bearish_external_to_internal_type_b_count=bearish_external_to_internal_type_b,
        bullish_internal_to_external_type_b_count=bullish_internal_to_external_type_b,
        bearish_internal_to_external_type_b_count=bearish_internal_to_external_type_b,
        bullish_internal_to_external_type_c_count=bullish_internal_to_external_type_c,
        bearish_internal_to_external_type_c_count=bearish_internal_to_external_type_c,
        bullish_internal_to_external_type_c_rare_case_count=(
            bullish_internal_to_external_type_c_rare_case
        ),
        bearish_internal_to_external_type_c_rare_case_count=(
            bearish_internal_to_external_type_c_rare_case
        ),
        bullish_internal_to_external_type_c_rare_case_c3_expansion_quality_count=(
            bullish_internal_to_external_type_c_rare_case_c3_expansion_quality
        ),
        bearish_internal_to_external_type_c_rare_case_c3_expansion_quality_count=(
            bearish_internal_to_external_type_c_rare_case_c3_expansion_quality
        ),
        bullish_c4_candidate_count=bullish_c4,
        bearish_c4_candidate_count=bearish_c4,
        bullish_case_b_candidate_count=bullish_case_b,
        bearish_case_b_candidate_count=bearish_case_b,
        bullish_c3_closure_count=bullish_c3_closure,
        bearish_c3_closure_count=bearish_c3_closure,
        bullish_c3_closure_rare_case_count=bullish_c3_closure_rare,
        bearish_c3_closure_rare_case_count=bearish_c3_closure_rare,
        bullish_c3_closure_rare_case_c3_expansion_quality_count=(
            bullish_c3_closure_rare_c3_expansion_quality
        ),
        bearish_c3_closure_rare_case_c3_expansion_quality_count=(
            bearish_c3_closure_rare_c3_expansion_quality
        ),
        bullish_c3_closure_c4_candidate_count=bullish_c3_closure_c4,
        bearish_c3_closure_c4_candidate_count=bearish_c3_closure_c4,
        bullish_c3_closure_c4_expansion_quality_count=bullish_c3_c4_expansion_quality,
        bearish_c3_closure_c4_expansion_quality_count=bearish_c3_c4_expansion_quality,
        bullish_c3_closure_rare_case_c4_candidate_count=bullish_c3_rare_c4,
        bearish_c3_closure_rare_case_c4_candidate_count=bearish_c3_rare_c4,
        bullish_c3_closure_rare_case_c4_expansion_quality_count=(
            bullish_c3_rare_c4_expansion_quality
        ),
        bearish_c3_closure_rare_case_c4_expansion_quality_count=(
            bearish_c3_rare_c4_expansion_quality
        ),
        bullish_fvg_count=bullish_fvg,
        bearish_fvg_count=bearish_fvg,
        fvg_candidate_count=fvg_candidate_counts["fvg_candidate_count"],
        fvg_resting_candidate_count=fvg_candidate_counts["fvg_resting_candidate_count"],
        fvg_reached_candidate_count=fvg_candidate_counts["fvg_reached_candidate_count"],
        fvg_invalidated_candidate_count=fvg_candidate_counts["fvg_invalidated_candidate_count"],
        bullish_resting_fvg_count=fvg_candidate_counts["bullish_resting_fvg_count"],
        bearish_resting_fvg_count=fvg_candidate_counts["bearish_resting_fvg_count"],
        bullish_reached_fvg_count=fvg_candidate_counts["bullish_reached_fvg_count"],
        bearish_reached_fvg_count=fvg_candidate_counts["bearish_reached_fvg_count"],
        bullish_invalidated_fvg_count=fvg_candidate_counts["bullish_invalidated_fvg_count"],
        bearish_invalidated_fvg_count=fvg_candidate_counts["bearish_invalidated_fvg_count"],
        erl_candidate_count=erl_counts["erl_candidate_count"],
        erl_resting_candidate_count=erl_counts["erl_resting_candidate_count"],
        erl_old_high_count=erl_counts["erl_old_high_count"],
        erl_old_low_count=erl_counts["erl_old_low_count"],
        erl_equal_highs_count=erl_counts["erl_equal_highs_count"],
        erl_equal_lows_count=erl_counts["erl_equal_lows_count"],
        erl_resting_old_high_count=erl_counts["erl_resting_old_high_count"],
        erl_resting_old_low_count=erl_counts["erl_resting_old_low_count"],
        erl_resting_equal_highs_count=erl_counts["erl_resting_equal_highs_count"],
        erl_resting_equal_lows_count=erl_counts["erl_resting_equal_lows_count"],
    )
