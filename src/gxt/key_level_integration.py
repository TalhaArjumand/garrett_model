from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Literal

from .candles import Candle, require_closed
from .fvg import FairValueGap, build_bearish_fvg, build_bullish_fvg
from .sequence_primitives import (
    is_valid_bearish_c2_sequence,
    is_valid_bearish_c2_sequence_expansion_quality,
    is_valid_bullish_c2_sequence,
    is_valid_bullish_c2_sequence_expansion_quality,
)

Direction = Literal["bullish", "bearish"]
KeyLevelTouch = Literal["c1", "c2", "both"]


@dataclass(frozen=True)
class InternalToExternalTypeACandidate:
    symbol: str
    timeframe: str
    direction: Direction
    irl_lower_bound: float
    irl_upper_bound: float
    irl_c1_timestamp: datetime
    irl_c2_timestamp: datetime
    irl_c3_timestamp: datetime
    irl_confirmed_at: datetime
    sequence_c1_timestamp: datetime
    sequence_c2_timestamp: datetime
    sequence_c3_timestamp: datetime
    key_level_touch: KeyLevelTouch
    decision_time_safe: bool
    reason: str


def _validate_series(candles: Iterable[Any]) -> list[Candle]:
    items = list(candles)
    if not items:
        return []

    validated: list[Candle] = []
    for idx, item in enumerate(items):
        if not isinstance(item, Candle):
            raise TypeError(f"candles[{idx}] must be a Candle, got {type(item).__name__}")
        require_closed(item)
        validated.append(item)

    symbols = {candle.symbol for candle in validated}
    timeframes = {candle.timeframe for candle in validated}
    if len(symbols) != 1:
        raise ValueError("integration series must contain exactly one symbol")
    if len(timeframes) != 1:
        raise ValueError("integration series must contain exactly one timeframe")

    for previous, current in zip(validated, validated[1:]):
        if not previous.timestamp < current.timestamp:
            raise ValueError("integration series must be in strict timestamp order")

    return validated


def _ranges_overlap(
    *,
    candle_low: float,
    candle_high: float,
    zone_low: float,
    zone_high: float,
) -> bool:
    return candle_high >= zone_low and candle_low <= zone_high


def _touch_label(*, touch_c1: bool, touch_c2: bool) -> KeyLevelTouch | None:
    if touch_c1 and touch_c2:
        return "both"
    if touch_c1:
        return "c1"
    if touch_c2:
        return "c2"
    return None


def _collect_directional_gaps(candles: list[Candle], direction: Direction) -> list[FairValueGap]:
    gaps: list[FairValueGap] = []
    for idx in range(len(candles) - 2):
        c1, c2, c3 = candles[idx], candles[idx + 1], candles[idx + 2]
        try:
            gap = (
                build_bullish_fvg(c1, c2, c3)
                if direction == "bullish"
                else build_bearish_fvg(c1, c2, c3)
            )
        except ValueError:
            continue
        if gap is not None:
            gaps.append(gap)
    return gaps


def detect_internal_to_external_type_a_candidates(
    candles: Iterable[Any],
) -> list[InternalToExternalTypeACandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    bullish_gaps = _collect_directional_gaps(validated, "bullish")
    bearish_gaps = _collect_directional_gaps(validated, "bearish")

    candidates: list[InternalToExternalTypeACandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = is_valid_bullish_c2_sequence(c1, c2, c3)
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for gap in bullish_gaps:
                if gap.c3_timestamp >= c1.timestamp:
                    continue
                touch_c1 = _ranges_overlap(
                    candle_low=c1.low,
                    candle_high=c1.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch_c2 = _ranges_overlap(
                    candle_low=c2.low,
                    candle_high=c2.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch = _touch_label(touch_c1=touch_c1, touch_c2=touch_c2)
                if touch is None:
                    continue
                candidates.append(
                    InternalToExternalTypeACandidate(
                        symbol=c1.symbol,
                        timeframe=c1.timeframe,
                        direction="bullish",
                        irl_lower_bound=gap.lower_bound,
                        irl_upper_bound=gap.upper_bound,
                        irl_c1_timestamp=gap.c1_timestamp,
                        irl_c2_timestamp=gap.c2_timestamp,
                        irl_c3_timestamp=gap.c3_timestamp,
                        irl_confirmed_at=gap.c3_timestamp,
                        sequence_c1_timestamp=c1.timestamp,
                        sequence_c2_timestamp=c2.timestamp,
                        sequence_c3_timestamp=c3.timestamp,
                        key_level_touch=touch,
                        decision_time_safe=True,
                        reason=(
                            "Valid bullish Type A sequence formed after a prior bullish IRL/FVG "
                            "was confirmed and the sequence touched that gap through C1 or C2."
                        ),
                    )
                )

        try:
            bearish_sequence = is_valid_bearish_c2_sequence(c1, c2, c3)
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for gap in bearish_gaps:
                if gap.c3_timestamp >= c1.timestamp:
                    continue
                touch_c1 = _ranges_overlap(
                    candle_low=c1.low,
                    candle_high=c1.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch_c2 = _ranges_overlap(
                    candle_low=c2.low,
                    candle_high=c2.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch = _touch_label(touch_c1=touch_c1, touch_c2=touch_c2)
                if touch is None:
                    continue
                candidates.append(
                    InternalToExternalTypeACandidate(
                        symbol=c1.symbol,
                        timeframe=c1.timeframe,
                        direction="bearish",
                        irl_lower_bound=gap.lower_bound,
                        irl_upper_bound=gap.upper_bound,
                        irl_c1_timestamp=gap.c1_timestamp,
                        irl_c2_timestamp=gap.c2_timestamp,
                        irl_c3_timestamp=gap.c3_timestamp,
                        irl_confirmed_at=gap.c3_timestamp,
                        sequence_c1_timestamp=c1.timestamp,
                        sequence_c2_timestamp=c2.timestamp,
                        sequence_c3_timestamp=c3.timestamp,
                        key_level_touch=touch,
                        decision_time_safe=True,
                        reason=(
                            "Valid bearish Type A sequence formed after a prior bearish IRL/FVG "
                            "was confirmed and the sequence touched that gap through C1 or C2."
                        ),
                    )
                )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.sequence_c1_timestamp,
            candidate.direction,
            candidate.irl_confirmed_at,
            candidate.irl_lower_bound,
            candidate.irl_upper_bound,
        ),
    )


def detect_internal_to_external_type_a_expansion_quality_candidates(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> list[InternalToExternalTypeACandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    bullish_gaps = _collect_directional_gaps(validated, "bullish")
    bearish_gaps = _collect_directional_gaps(validated, "bearish")

    candidates: list[InternalToExternalTypeACandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = is_valid_bullish_c2_sequence_expansion_quality(
                c1,
                c2,
                c3,
                max_lower_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for gap in bullish_gaps:
                if gap.c3_timestamp >= c1.timestamp:
                    continue
                touch_c1 = _ranges_overlap(
                    candle_low=c1.low,
                    candle_high=c1.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch_c2 = _ranges_overlap(
                    candle_low=c2.low,
                    candle_high=c2.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch = _touch_label(touch_c1=touch_c1, touch_c2=touch_c2)
                if touch is None:
                    continue
                candidates.append(
                    InternalToExternalTypeACandidate(
                        symbol=c1.symbol,
                        timeframe=c1.timeframe,
                        direction="bullish",
                        irl_lower_bound=gap.lower_bound,
                        irl_upper_bound=gap.upper_bound,
                        irl_c1_timestamp=gap.c1_timestamp,
                        irl_c2_timestamp=gap.c2_timestamp,
                        irl_c3_timestamp=gap.c3_timestamp,
                        irl_confirmed_at=gap.c3_timestamp,
                        sequence_c1_timestamp=c1.timestamp,
                        sequence_c2_timestamp=c2.timestamp,
                        sequence_c3_timestamp=c3.timestamp,
                        key_level_touch=touch,
                        decision_time_safe=True,
                        reason=(
                            "Valid bullish Type A strict-expansion sequence formed after a prior "
                            "bullish IRL/FVG was confirmed and the sequence touched that gap "
                            "through C1 or C2."
                        ),
                    )
                )

        try:
            bearish_sequence = is_valid_bearish_c2_sequence_expansion_quality(
                c1,
                c2,
                c3,
                max_upper_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for gap in bearish_gaps:
                if gap.c3_timestamp >= c1.timestamp:
                    continue
                touch_c1 = _ranges_overlap(
                    candle_low=c1.low,
                    candle_high=c1.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch_c2 = _ranges_overlap(
                    candle_low=c2.low,
                    candle_high=c2.high,
                    zone_low=gap.lower_bound,
                    zone_high=gap.upper_bound,
                )
                touch = _touch_label(touch_c1=touch_c1, touch_c2=touch_c2)
                if touch is None:
                    continue
                candidates.append(
                    InternalToExternalTypeACandidate(
                        symbol=c1.symbol,
                        timeframe=c1.timeframe,
                        direction="bearish",
                        irl_lower_bound=gap.lower_bound,
                        irl_upper_bound=gap.upper_bound,
                        irl_c1_timestamp=gap.c1_timestamp,
                        irl_c2_timestamp=gap.c2_timestamp,
                        irl_c3_timestamp=gap.c3_timestamp,
                        irl_confirmed_at=gap.c3_timestamp,
                        sequence_c1_timestamp=c1.timestamp,
                        sequence_c2_timestamp=c2.timestamp,
                        sequence_c3_timestamp=c3.timestamp,
                        key_level_touch=touch,
                        decision_time_safe=True,
                        reason=(
                            "Valid bearish Type A strict-expansion sequence formed after a prior "
                            "bearish IRL/FVG was confirmed and the sequence touched that gap "
                            "through C1 or C2."
                        ),
                    )
                )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.sequence_c1_timestamp,
            candidate.direction,
            candidate.irl_confirmed_at,
            candidate.irl_lower_bound,
            candidate.irl_upper_bound,
        ),
    )


def count_internal_to_external_type_a_sequences(
    candles: Iterable[Any],
) -> tuple[int, int]:
    candidates = detect_internal_to_external_type_a_candidates(candles)
    bullish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
            candidate.sequence_c3_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bullish"
    }
    bearish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
            candidate.sequence_c3_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bearish"
    }
    return len(bullish), len(bearish)


def count_internal_to_external_type_a_expansion_quality_sequences(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    candidates = detect_internal_to_external_type_a_expansion_quality_candidates(
        candles,
        max_wick_fraction=max_wick_fraction,
    )
    bullish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
            candidate.sequence_c3_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bullish"
    }
    bearish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
            candidate.sequence_c3_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bearish"
    }
    return len(bullish), len(bearish)
