from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Literal

from .candles import Candle, require_closed
from .sequence_primitives import validate_sequence_inputs

FVGDirection = Literal["bullish", "bearish"]


@dataclass(frozen=True)
class FairValueGap:
    symbol: str
    timeframe: str
    direction: FVGDirection
    lower_bound: float
    upper_bound: float
    c1_timestamp: datetime
    c2_timestamp: datetime
    c3_timestamp: datetime

    @property
    def width(self) -> float:
        return self.upper_bound - self.lower_bound


@dataclass(frozen=True)
class FVGCandidate:
    symbol: str
    timeframe: str
    direction: FVGDirection
    lower_bound: float
    upper_bound: float
    c1_timestamp: datetime
    c2_timestamp: datetime
    c3_timestamp: datetime
    confirmed_at: datetime
    is_reached: bool
    reached_at: datetime | None
    decision_time_safe: bool
    reason: str
    invalidated_at: datetime | None = None

    @property
    def width(self) -> float:
        return self.upper_bound - self.lower_bound

    @property
    def is_resting(self) -> bool:
        return not self.is_reached and not self.is_invalidated

    @property
    def is_invalidated(self) -> bool:
        return self.invalidated_at is not None

    @property
    def lifecycle_state(self) -> str:
        if self.is_invalidated:
            return "invalidated"
        if self.is_reached:
            return "reached"
        return "resting"


def validate_fvg_inputs(c1: Any, c2: Any, c3: Any) -> tuple[Candle, Candle, Candle]:
    return validate_sequence_inputs(c1, c2, c3)


def is_bullish_fvg(c1: Any, c2: Any, c3: Any) -> bool:
    c1, _, c3 = validate_fvg_inputs(c1, c2, c3)
    return c3.low > c1.high


def is_bearish_fvg(c1: Any, c2: Any, c3: Any) -> bool:
    c1, _, c3 = validate_fvg_inputs(c1, c2, c3)
    return c3.high < c1.low


def build_bullish_fvg(c1: Any, c2: Any, c3: Any) -> FairValueGap | None:
    c1, c2, c3 = validate_fvg_inputs(c1, c2, c3)
    if not is_bullish_fvg(c1, c2, c3):
        return None

    return FairValueGap(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction="bullish",
        lower_bound=c1.high,
        upper_bound=c3.low,
        c1_timestamp=c1.timestamp,
        c2_timestamp=c2.timestamp,
        c3_timestamp=c3.timestamp,
    )


def build_bearish_fvg(c1: Any, c2: Any, c3: Any) -> FairValueGap | None:
    c1, c2, c3 = validate_fvg_inputs(c1, c2, c3)
    if not is_bearish_fvg(c1, c2, c3):
        return None

    return FairValueGap(
        symbol=c1.symbol,
        timeframe=c1.timeframe,
        direction="bearish",
        lower_bound=c3.high,
        upper_bound=c1.low,
        c1_timestamp=c1.timestamp,
        c2_timestamp=c2.timestamp,
        c3_timestamp=c3.timestamp,
    )


def detect_fvg(c1: Any, c2: Any, c3: Any) -> FairValueGap | None:
    bullish_gap = build_bullish_fvg(c1, c2, c3)
    if bullish_gap is not None:
        return bullish_gap

    return build_bearish_fvg(c1, c2, c3)


def _validate_fvg_candidate_series(candles: Iterable[Any]) -> list[Candle]:
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
        raise ValueError("FVG candidate series must have the same symbol")
    if len(timeframes) != 1:
        raise ValueError("FVG candidate series must have the same timeframe")

    for previous, current in zip(validated, validated[1:]):
        if not previous.timestamp < current.timestamp:
            raise ValueError("FVG candidate series must be in strict timestamp order")

    return validated


def _ranges_overlap(
    *,
    candle_low: float,
    candle_high: float,
    zone_low: float,
    zone_high: float,
) -> bool:
    return candle_high >= zone_low and candle_low <= zone_high


def _find_first_reach_timestamp(
    candles: list[Candle],
    gap: FairValueGap,
) -> datetime | None:
    for candle in candles:
        if candle.timestamp <= gap.c3_timestamp:
            continue
        if _ranges_overlap(
            candle_low=candle.low,
            candle_high=candle.high,
            zone_low=gap.lower_bound,
            zone_high=gap.upper_bound,
        ):
            return candle.timestamp
    return None


def _is_directionally_invalidated_by_close(
    gap: FairValueGap,
    candle: Candle,
) -> bool:
    if candle.timestamp <= gap.c3_timestamp:
        return False
    if gap.direction == "bullish":
        return candle.close < gap.lower_bound
    return candle.close > gap.upper_bound


def _find_first_invalidation_timestamp(
    candles: list[Candle],
    gap: FairValueGap,
) -> datetime | None:
    for candle in candles:
        if _is_directionally_invalidated_by_close(gap, candle):
            return candle.timestamp
    return None


def _build_fvg_candidate(
    gap: FairValueGap,
    reached_at: datetime | None,
    invalidated_at: datetime | None,
) -> FVGCandidate:
    return FVGCandidate(
        symbol=gap.symbol,
        timeframe=gap.timeframe,
        direction=gap.direction,
        lower_bound=gap.lower_bound,
        upper_bound=gap.upper_bound,
        c1_timestamp=gap.c1_timestamp,
        c2_timestamp=gap.c2_timestamp,
        c3_timestamp=gap.c3_timestamp,
        confirmed_at=gap.c3_timestamp,
        is_reached=reached_at is not None,
        reached_at=reached_at,
        invalidated_at=invalidated_at,
        decision_time_safe=True,
        reason=(
            "Baseline three-candle FVG candidate with later state tracking for whether "
            "price has reached the gap zone or directionally invalidated it by "
            "closing through the opposite side."
        ),
    )


def detect_fvg_candidates(candles: Iterable[Any]) -> list[FVGCandidate]:
    validated = _validate_fvg_candidate_series(candles)
    if not validated:
        return []

    candidates: list[FVGCandidate] = []
    for idx in range(len(validated) - 2):
        c1, c2, c3 = validated[idx], validated[idx + 1], validated[idx + 2]
        try:
            gap = detect_fvg(c1, c2, c3)
        except ValueError:
            continue
        if gap is None:
            continue
        candidates.append(
            _build_fvg_candidate(
                gap,
                _find_first_reach_timestamp(validated, gap),
                _find_first_invalidation_timestamp(validated, gap),
            )
        )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.confirmed_at,
            candidate.direction,
            candidate.lower_bound,
            candidate.upper_bound,
        ),
    )
