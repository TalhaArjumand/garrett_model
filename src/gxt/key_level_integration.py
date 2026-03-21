from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Literal

from .candles import Candle, require_closed
from .erl_proxy import ERLCandidate, detect_erl_candidates
from .fvg import FVGCandidate, detect_fvg_candidates
from .sequence_primitives import (
    is_bearish_c2_reversal_to_expansion,
    is_bearish_c3_closure,
    is_valid_bearish_c2_sequence,
    is_valid_bearish_c2_sequence_expansion_quality,
    is_bullish_c2_reversal_to_expansion,
    is_bullish_c3_closure,
    is_valid_bullish_c2_sequence,
    is_valid_bullish_c2_sequence_expansion_quality,
)
from .swing_research import (
    has_bearish_type_b_additive_extension_c3_quality_candidate,
    has_bullish_type_b_additive_extension_c3_quality_candidate,
    is_bearish_type_b_additive_extension,
    is_bullish_type_b_additive_extension,
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


@dataclass(frozen=True)
class InternalToExternalTypeBCandidate:
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
    key_level_touch: KeyLevelTouch
    decision_time_safe: bool
    reason: str


@dataclass(frozen=True)
class InternalToExternalTypeCCandidate:
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


@dataclass(frozen=True)
class InternalToExternalTypeBAdditiveExtensionCandidate:
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


@dataclass(frozen=True)
class InternalToExternalTypeBAdditiveExtensionC3QualityCandidate:
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


@dataclass(frozen=True)
class ExternalToInternalTypeACandidate:
    symbol: str
    timeframe: str
    direction: Direction
    erl_kind: str
    erl_side: str
    erl_lower_bound: float
    erl_upper_bound: float
    erl_anchor_timestamps: tuple[datetime, ...]
    erl_confirmed_at: datetime
    sequence_c1_timestamp: datetime
    sequence_c2_timestamp: datetime
    sequence_c3_timestamp: datetime
    key_level_touch: KeyLevelTouch
    decision_time_safe: bool
    reason: str


@dataclass(frozen=True)
class ExternalToInternalTypeBCandidate:
    symbol: str
    timeframe: str
    direction: Direction
    erl_kind: str
    erl_side: str
    erl_lower_bound: float
    erl_upper_bound: float
    erl_anchor_timestamps: tuple[datetime, ...]
    erl_confirmed_at: datetime
    sequence_c1_timestamp: datetime
    sequence_c2_timestamp: datetime
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


def _collect_active_directional_irls(
    candles: list[Candle],
    *,
    before_index: int,
    direction: Direction,
) -> list[FVGCandidate]:
    if before_index <= 0:
        return []

    prior_candidates = detect_fvg_candidates(candles[:before_index])
    return [
        candidate
        for candidate in prior_candidates
        if candidate.direction == direction and candidate.is_resting
    ]


def _collect_touching_active_directional_irls(
    candles: list[Candle],
    *,
    before_index: int,
    direction: Direction,
    c1: Candle,
    c2: Candle,
) -> list[tuple[FVGCandidate, KeyLevelTouch]]:
    touching: list[tuple[FVGCandidate, KeyLevelTouch]] = []
    for irl in _collect_active_directional_irls(
        candles,
        before_index=before_index,
        direction=direction,
    ):
        touch_c1 = _ranges_overlap(
            candle_low=c1.low,
            candle_high=c1.high,
            zone_low=irl.lower_bound,
            zone_high=irl.upper_bound,
        )
        touch_c2 = _ranges_overlap(
            candle_low=c2.low,
            candle_high=c2.high,
            zone_low=irl.lower_bound,
            zone_high=irl.upper_bound,
        )
        touch = _touch_label(touch_c1=touch_c1, touch_c2=touch_c2)
        if touch is not None:
            touching.append((irl, touch))
    return touching


def _is_irl_invalidated_by_close(irl: FVGCandidate, candle: Candle) -> bool:
    if irl.direction == "bullish":
        return candle.close < irl.lower_bound
    return candle.close > irl.upper_bound


def _sequence_preserves_irl_on_closes(irl: FVGCandidate, *candles: Candle) -> bool:
    return not any(_is_irl_invalidated_by_close(irl, candle) for candle in candles)


def _collect_fresh_directional_irls_confirmed_on_c1(
    candles: list[Candle],
    *,
    c1_index: int,
    direction: Direction,
    c2: Candle,
    preserve_candles: tuple[Candle, ...] = (),
) -> list[tuple[FVGCandidate, KeyLevelTouch]]:
    if c1_index < 2:
        return []

    touching: list[tuple[FVGCandidate, KeyLevelTouch]] = []
    c1 = candles[c1_index]
    for irl in detect_fvg_candidates(candles[: c1_index + 1]):
        if irl.direction != direction:
            continue
        if irl.confirmed_at != c1.timestamp:
            continue
        if not _ranges_overlap(
            candle_low=c2.low,
            candle_high=c2.high,
            zone_low=irl.lower_bound,
            zone_high=irl.upper_bound,
        ):
            continue
        if not _sequence_preserves_irl_on_closes(irl, c2, *preserve_candles):
            continue
        touching.append((irl, "c2"))
    return touching


def _erl_side_for_direction(direction: Direction) -> Literal["buy_side", "sell_side"]:
    if direction == "bullish":
        return "sell_side"
    return "buy_side"


def _collect_active_directional_erls(
    candles: list[Candle],
    *,
    before_index: int,
    direction: Direction,
) -> list[ERLCandidate]:
    if before_index <= 0:
        return []

    expected_side = _erl_side_for_direction(direction)
    prior_candidates = detect_erl_candidates(candles[:before_index])
    return [
        candidate
        for candidate in prior_candidates
        if candidate.side == expected_side and candidate.is_resting
    ]


def _collect_touching_active_directional_erls(
    candles: list[Candle],
    *,
    before_index: int,
    direction: Direction,
    c1: Candle,
    c2: Candle,
) -> list[tuple[ERLCandidate, KeyLevelTouch]]:
    touching: list[tuple[ERLCandidate, KeyLevelTouch]] = []
    for erl in _collect_active_directional_erls(
        candles,
        before_index=before_index,
        direction=direction,
    ):
        touch_c1 = _ranges_overlap(
            candle_low=c1.low,
            candle_high=c1.high,
            zone_low=erl.lower_bound,
            zone_high=erl.upper_bound,
        )
        touch_c2 = _ranges_overlap(
            candle_low=c2.low,
            candle_high=c2.high,
            zone_low=erl.lower_bound,
            zone_high=erl.upper_bound,
        )
        touch = _touch_label(touch_c1=touch_c1, touch_c2=touch_c2)
        if touch is not None:
            touching.append((erl, touch))
    return touching


def _collect_fresh_directional_erls_confirmed_on_c1(
    candles: list[Candle],
    *,
    c1_index: int,
    direction: Direction,
    c2: Candle,
) -> list[tuple[ERLCandidate, KeyLevelTouch]]:
    if c1_index < 2:
        return []

    expected_side = _erl_side_for_direction(direction)
    c1 = candles[c1_index]
    touching: list[tuple[ERLCandidate, KeyLevelTouch]] = []
    for erl in detect_erl_candidates(candles[: c1_index + 1]):
        if erl.side != expected_side:
            continue
        if erl.confirmed_at != c1.timestamp:
            continue
        if not _ranges_overlap(
            candle_low=c2.low,
            candle_high=c2.high,
            zone_low=erl.lower_bound,
            zone_high=erl.upper_bound,
        ):
            continue
        touching.append((erl, "c2"))
    return touching


def _build_type_a_candidate(
    *,
    irl: FVGCandidate,
    c1: Candle,
    c2: Candle,
    c3: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    strict_expansion_quality: bool,
) -> InternalToExternalTypeACandidate:
    quality_label = " strict-expansion" if strict_expansion_quality else ""
    return InternalToExternalTypeACandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        irl_lower_bound=irl.lower_bound,
        irl_upper_bound=irl.upper_bound,
        irl_c1_timestamp=irl.c1_timestamp,
        irl_c2_timestamp=irl.c2_timestamp,
        irl_c3_timestamp=irl.c3_timestamp,
        irl_confirmed_at=irl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        sequence_c3_timestamp=c3.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} Type A{quality_label} sequence formed after a prior "
            f"{direction} IRL/FVG was confirmed and still resting before sequence "
            "C1. The active IRL was then touched through C1 or C2."
        ),
    )


def _build_type_b_candidate(
    *,
    irl: FVGCandidate,
    c1: Candle,
    c2: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    fresh_on_c1_close: bool,
) -> InternalToExternalTypeBCandidate:
    timing_phrase = (
        "was confirmed on C1 close and became eligible from C2 onward"
        if fresh_on_c1_close
        else "was confirmed and still resting before sequence C1"
    )
    return InternalToExternalTypeBCandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        irl_lower_bound=irl.lower_bound,
        irl_upper_bound=irl.upper_bound,
        irl_c1_timestamp=irl.c1_timestamp,
        irl_c2_timestamp=irl.c2_timestamp,
        irl_c3_timestamp=irl.c3_timestamp,
        irl_confirmed_at=irl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} Type B reversal-to-expansion candle formed after a "
            f"{direction} IRL/FVG {timing_phrase}. The active IRL was then touched "
            "through the allowed sequence candles without a close-through "
            "invalidation."
        ),
    )


def _build_type_c_candidate(
    *,
    irl: FVGCandidate,
    c1: Candle,
    c2: Candle,
    c3: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    fresh_on_c1_close: bool,
) -> InternalToExternalTypeCCandidate:
    timing_phrase = (
        "was confirmed on C1 close and became eligible from C2 onward"
        if fresh_on_c1_close
        else "was confirmed and still resting before sequence C1"
    )
    return InternalToExternalTypeCCandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        irl_lower_bound=irl.lower_bound,
        irl_upper_bound=irl.upper_bound,
        irl_c1_timestamp=irl.c1_timestamp,
        irl_c2_timestamp=irl.c2_timestamp,
        irl_c3_timestamp=irl.c3_timestamp,
        irl_confirmed_at=irl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        sequence_c3_timestamp=c3.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} Type C c3-closure sequence formed after a "
            f"{direction} IRL/FVG {timing_phrase}. The active IRL was touched "
            "through C1 or C2, remained eligible through C3 close, and the first "
            "strong confirming closure arrived on C3."
        ),
    )


def _build_type_b_additive_extension_candidate(
    *,
    irl: FVGCandidate,
    c1: Candle,
    c2: Candle,
    c3: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    fresh_on_c1_close: bool,
) -> InternalToExternalTypeBAdditiveExtensionCandidate:
    timing_phrase = (
        "was confirmed on C1 close and became eligible from C2 onward"
        if fresh_on_c1_close
        else "was confirmed and still resting before sequence C1"
    )
    return InternalToExternalTypeBAdditiveExtensionCandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        irl_lower_bound=irl.lower_bound,
        irl_upper_bound=irl.upper_bound,
        irl_c1_timestamp=irl.c1_timestamp,
        irl_c2_timestamp=irl.c2_timestamp,
        irl_c3_timestamp=irl.c3_timestamp,
        irl_confirmed_at=irl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        sequence_c3_timestamp=c3.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} Type B additive extension formed after a "
            f"{direction} IRL/FVG {timing_phrase}. Base integrated Type B held, "
            "the active IRL remained eligible through C3 close, and the additive "
            "C3 trade trigger also passed."
        ),
    )


def _build_type_b_additive_extension_c3_quality_candidate(
    *,
    irl: FVGCandidate,
    c1: Candle,
    c2: Candle,
    c3: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    fresh_on_c1_close: bool,
) -> InternalToExternalTypeBAdditiveExtensionC3QualityCandidate:
    timing_phrase = (
        "was confirmed on C1 close and became eligible from C2 onward"
        if fresh_on_c1_close
        else "was confirmed and still resting before sequence C1"
    )
    return InternalToExternalTypeBAdditiveExtensionC3QualityCandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        irl_lower_bound=irl.lower_bound,
        irl_upper_bound=irl.upper_bound,
        irl_c1_timestamp=irl.c1_timestamp,
        irl_c2_timestamp=irl.c2_timestamp,
        irl_c3_timestamp=irl.c3_timestamp,
        irl_confirmed_at=irl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        sequence_c3_timestamp=c3.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} Type B additive extension C3-quality subtype "
            f"formed after a {direction} IRL/FVG {timing_phrase}. Integrated base "
            "Type B held, integrated Type B additive extension held, the active "
            "IRL remained eligible through C3 close, and the stricter C3 quality "
            "upgrade also passed."
        ),
    )


def detect_internal_to_external_type_a_candidates(
    candles: Iterable[Any],
) -> list[InternalToExternalTypeACandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    candidates: list[InternalToExternalTypeACandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = is_valid_bullish_c2_sequence(c1, c2, c3)
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=False,
                    )
                )

        try:
            bearish_sequence = is_valid_bearish_c2_sequence(c1, c2, c3)
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=False,
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
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=True,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=True,
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
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=True,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_a_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=True,
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


def detect_internal_to_external_type_b_candidates(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> list[InternalToExternalTypeBCandidate]:
    validated = _validate_series(candles)
    if len(validated) < 2:
        return []

    candidates: list[InternalToExternalTypeBCandidate] = []
    for idx in range(len(validated) - 1):
        c1, c2 = validated[idx], validated[idx + 1]

        try:
            bullish_sequence = is_bullish_c2_reversal_to_expansion(
                c1,
                c2,
                max_lower_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2):
                    continue
                candidates.append(
                    _build_type_b_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
            ):
                candidates.append(
                    _build_type_b_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=True,
                    )
                )

        try:
            bearish_sequence = is_bearish_c2_reversal_to_expansion(
                c1,
                c2,
                max_upper_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2):
                    continue
                candidates.append(
                    _build_type_b_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
            ):
                candidates.append(
                    _build_type_b_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=True,
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


def count_internal_to_external_type_b_sequences(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    candidates = detect_internal_to_external_type_b_candidates(
        candles,
        max_wick_fraction=max_wick_fraction,
    )
    bullish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bullish"
    }
    bearish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bearish"
    }
    return len(bullish), len(bearish)


def detect_internal_to_external_type_c_candidates(
    candles: Iterable[Any],
) -> list[InternalToExternalTypeCCandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    candidates: list[InternalToExternalTypeCCandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = is_bullish_c3_closure(c1, c2, c3)
        except ValueError:
            bullish_sequence = False
        if bullish_sequence and not is_bullish_type_b_additive_extension(c1, c2, c3):
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_c_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_c_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=True,
                    )
                )

        try:
            bearish_sequence = is_bearish_c3_closure(c1, c2, c3)
        except ValueError:
            bearish_sequence = False
        if bearish_sequence and not is_bearish_type_b_additive_extension(c1, c2, c3):
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_c_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_c_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=True,
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


def count_internal_to_external_type_c_sequences(
    candles: Iterable[Any],
) -> tuple[int, int]:
    candidates = detect_internal_to_external_type_c_candidates(candles)
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


def detect_internal_to_external_type_b_additive_extension_candidates(
    candles: Iterable[Any],
) -> list[InternalToExternalTypeBAdditiveExtensionCandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    candidates: list[InternalToExternalTypeBAdditiveExtensionCandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = is_bullish_type_b_additive_extension(c1, c2, c3)
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_b_additive_extension_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_b_additive_extension_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=True,
                    )
                )

        try:
            bearish_sequence = is_bearish_type_b_additive_extension(c1, c2, c3)
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_b_additive_extension_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_b_additive_extension_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=True,
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


def count_internal_to_external_type_b_additive_extension_sequences(
    candles: Iterable[Any],
) -> tuple[int, int]:
    candidates = detect_internal_to_external_type_b_additive_extension_candidates(candles)
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


def detect_internal_to_external_type_b_additive_extension_c3_quality_candidates(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> list[InternalToExternalTypeBAdditiveExtensionC3QualityCandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    candidates: list[InternalToExternalTypeBAdditiveExtensionC3QualityCandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = has_bullish_type_b_additive_extension_c3_quality_candidate(
                c1,
                c2,
                c3,
                max_lower_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_b_additive_extension_c3_quality_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_b_additive_extension_c3_quality_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=True,
                    )
                )

        try:
            bearish_sequence = has_bearish_type_b_additive_extension_c3_quality_candidate(
                c1,
                c2,
                c3,
                max_upper_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for irl, touch in _collect_touching_active_directional_irls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                if not _sequence_preserves_irl_on_closes(irl, c1, c2, c3):
                    continue
                candidates.append(
                    _build_type_b_additive_extension_c3_quality_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for irl, touch in _collect_fresh_directional_irls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
                preserve_candles=(c3,),
            ):
                candidates.append(
                    _build_type_b_additive_extension_c3_quality_candidate(
                        irl=irl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=True,
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


def count_internal_to_external_type_b_additive_extension_c3_quality_sequences(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    candidates = detect_internal_to_external_type_b_additive_extension_c3_quality_candidates(
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


def _build_external_type_a_candidate(
    *,
    erl: ERLCandidate,
    c1: Candle,
    c2: Candle,
    c3: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    strict_expansion_quality: bool,
    fresh_on_c1_close: bool,
) -> ExternalToInternalTypeACandidate:
    quality_label = " strict-expansion" if strict_expansion_quality else ""
    timing_phrase = (
        "was confirmed on C1 close and became eligible from C2 onward"
        if fresh_on_c1_close
        else "was confirmed and still resting before sequence C1"
    )
    return ExternalToInternalTypeACandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        erl_kind=erl.kind,
        erl_side=erl.side,
        erl_lower_bound=erl.lower_bound,
        erl_upper_bound=erl.upper_bound,
        erl_anchor_timestamps=erl.anchor_timestamps,
        erl_confirmed_at=erl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        sequence_c3_timestamp=c3.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} external-to-internal Type A{quality_label} sequence "
            f"formed after a same-bias ERL that {timing_phrase}. The live ERL was "
            "then touched through C1 or C2, and target-side logic remains "
            "intentionally excluded from this bridge."
        ),
    )


def detect_external_to_internal_type_a_candidates(
    candles: Iterable[Any],
) -> list[ExternalToInternalTypeACandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    candidates: list[ExternalToInternalTypeACandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]

        try:
            bullish_sequence = is_valid_bullish_c2_sequence(c1, c2, c3)
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for erl, touch in _collect_touching_active_directional_erls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=False,
                        fresh_on_c1_close=False,
                    )
                )
            for erl, touch in _collect_fresh_directional_erls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=False,
                        fresh_on_c1_close=True,
                    )
                )

        try:
            bearish_sequence = is_valid_bearish_c2_sequence(c1, c2, c3)
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for erl, touch in _collect_touching_active_directional_erls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=False,
                        fresh_on_c1_close=False,
                    )
                )
            for erl, touch in _collect_fresh_directional_erls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=False,
                        fresh_on_c1_close=True,
                    )
                )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.sequence_c1_timestamp,
            candidate.direction,
            candidate.erl_confirmed_at,
            candidate.erl_lower_bound,
            candidate.erl_upper_bound,
        ),
    )


def detect_external_to_internal_type_a_expansion_quality_candidates(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> list[ExternalToInternalTypeACandidate]:
    validated = _validate_series(candles)
    if len(validated) < 3:
        return []

    candidates: list[ExternalToInternalTypeACandidate] = []
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
            for erl, touch in _collect_touching_active_directional_erls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=True,
                        fresh_on_c1_close=False,
                    )
                )
            for erl, touch in _collect_fresh_directional_erls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bullish",
                        touch=touch,
                        strict_expansion_quality=True,
                        fresh_on_c1_close=True,
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
            for erl, touch in _collect_touching_active_directional_erls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=True,
                        fresh_on_c1_close=False,
                    )
                )
            for erl, touch in _collect_fresh_directional_erls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_a_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        c3=c3,
                        direction="bearish",
                        touch=touch,
                        strict_expansion_quality=True,
                        fresh_on_c1_close=True,
                    )
                )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.sequence_c1_timestamp,
            candidate.direction,
            candidate.erl_confirmed_at,
            candidate.erl_lower_bound,
            candidate.erl_upper_bound,
        ),
    )


def count_external_to_internal_type_a_sequences(
    candles: Iterable[Any],
) -> tuple[int, int]:
    candidates = detect_external_to_internal_type_a_candidates(candles)
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


def count_external_to_internal_type_a_expansion_quality_sequences(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    candidates = detect_external_to_internal_type_a_expansion_quality_candidates(
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


def _build_external_type_b_candidate(
    *,
    erl: ERLCandidate,
    c1: Candle,
    c2: Candle,
    direction: Direction,
    touch: KeyLevelTouch,
    fresh_on_c1_close: bool,
) -> ExternalToInternalTypeBCandidate:
    timing_phrase = (
        "was confirmed on C1 close and became eligible from C2 onward"
        if fresh_on_c1_close
        else "was confirmed and still resting before sequence C1"
    )
    return ExternalToInternalTypeBCandidate(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction=direction,
        erl_kind=erl.kind,
        erl_side=erl.side,
        erl_lower_bound=erl.lower_bound,
        erl_upper_bound=erl.upper_bound,
        erl_anchor_timestamps=erl.anchor_timestamps,
        erl_confirmed_at=erl.confirmed_at,
        sequence_c1_timestamp=c1.timestamp,
        sequence_c2_timestamp=c2.timestamp,
        key_level_touch=touch,
        decision_time_safe=True,
        reason=(
            f"Valid {direction} external-to-internal Type B reversal-to-expansion "
            f"candle formed after a same-bias ERL that {timing_phrase}. The live "
            "ERL was then touched through the allowed sequence candles, and "
            "target-side logic remains intentionally excluded from this bridge."
        ),
    )


def detect_external_to_internal_type_b_candidates(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> list[ExternalToInternalTypeBCandidate]:
    validated = _validate_series(candles)
    if len(validated) < 2:
        return []

    candidates: list[ExternalToInternalTypeBCandidate] = []
    for idx in range(len(validated) - 1):
        c1, c2 = validated[idx], validated[idx + 1]

        try:
            bullish_sequence = is_bullish_c2_reversal_to_expansion(
                c1,
                c2,
                max_lower_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bullish_sequence = False
        if bullish_sequence:
            for erl, touch in _collect_touching_active_directional_erls(
                validated,
                before_index=idx,
                direction="bullish",
                c1=c1,
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_b_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for erl, touch in _collect_fresh_directional_erls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bullish",
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_b_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        direction="bullish",
                        touch=touch,
                        fresh_on_c1_close=True,
                    )
                )

        try:
            bearish_sequence = is_bearish_c2_reversal_to_expansion(
                c1,
                c2,
                max_upper_wick_fraction=max_wick_fraction,
            )
        except ValueError:
            bearish_sequence = False
        if bearish_sequence:
            for erl, touch in _collect_touching_active_directional_erls(
                validated,
                before_index=idx,
                direction="bearish",
                c1=c1,
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_b_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=False,
                    )
                )
            for erl, touch in _collect_fresh_directional_erls_confirmed_on_c1(
                validated,
                c1_index=idx,
                direction="bearish",
                c2=c2,
            ):
                candidates.append(
                    _build_external_type_b_candidate(
                        erl=erl,
                        c1=c1,
                        c2=c2,
                        direction="bearish",
                        touch=touch,
                        fresh_on_c1_close=True,
                    )
                )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.sequence_c1_timestamp,
            candidate.direction,
            candidate.erl_confirmed_at,
            candidate.erl_lower_bound,
            candidate.erl_upper_bound,
        ),
    )


def count_external_to_internal_type_b_sequences(
    candles: Iterable[Any],
    *,
    max_wick_fraction: float = 0.25,
) -> tuple[int, int]:
    candidates = detect_external_to_internal_type_b_candidates(
        candles,
        max_wick_fraction=max_wick_fraction,
    )
    bullish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bullish"
    }
    bearish = {
        (
            candidate.sequence_c1_timestamp,
            candidate.sequence_c2_timestamp,
        )
        for candidate in candidates
        if candidate.direction == "bearish"
    }
    return len(bullish), len(bearish)
