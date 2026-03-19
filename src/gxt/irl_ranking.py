from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from statistics import median
from types import MappingProxyType
from typing import Any, Iterable, Literal, Mapping, Sequence

from .candles import Candle, require_closed
from .fvg import FVGCandidate, detect_fvg_candidates

IRLDirectionBias = Literal["bullish", "bearish", "neutral"]


@dataclass(frozen=True)
class IRLRankingWeights:
    state: float = 0.35
    direction: float = 0.25
    proximity: float = 0.25
    recency: float = 0.15

    def __post_init__(self) -> None:
        for field_name in ("state", "direction", "proximity", "recency"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{field_name} weight must be numeric")
            numeric = float(value)
            if not isfinite(numeric):
                raise ValueError(f"{field_name} weight must be finite")
            if numeric < 0:
                raise ValueError(f"{field_name} weight must be >= 0")
            object.__setattr__(self, field_name, numeric)

        if self.total <= 0:
            raise ValueError("at least one IRL ranking weight must be > 0")

    @property
    def total(self) -> float:
        return self.state + self.direction + self.proximity + self.recency


@dataclass(frozen=True)
class IRLRankedCandidate:
    candidate: FVGCandidate
    score: float
    rank: int
    reasons: tuple[str, ...]
    feature_values: Mapping[str, float | int | str | None]


def _validate_current_price(current_price: Any) -> float:
    if isinstance(current_price, bool) or not isinstance(current_price, (int, float)):
        raise TypeError("current_price must be numeric")
    price = float(current_price)
    if not isfinite(price) or price <= 0:
        raise ValueError("current_price must be a finite positive number")
    return price


def _validate_as_of_timestamp(as_of_timestamp: Any) -> datetime:
    if not isinstance(as_of_timestamp, datetime):
        raise TypeError("as_of_timestamp must be a datetime")
    if as_of_timestamp.tzinfo is None or as_of_timestamp.utcoffset() is None:
        raise ValueError("as_of_timestamp must be timezone-aware")
    return as_of_timestamp


def _validate_direction_bias(direction_bias: Any) -> IRLDirectionBias:
    if direction_bias not in {"bullish", "bearish", "neutral"}:
        raise ValueError("direction_bias must be 'bullish', 'bearish', or 'neutral'")
    return direction_bias


def _validate_candle_series(candles: Iterable[Any]) -> list[Candle]:
    items = list(candles)
    validated: list[Candle] = []
    for idx, item in enumerate(items):
        if not isinstance(item, Candle):
            raise TypeError(f"candles[{idx}] must be a Candle, got {type(item).__name__}")
        require_closed(item)
        validated.append(item)

    for previous, current in zip(validated, validated[1:]):
        if not previous.timestamp < current.timestamp:
            raise ValueError("candles must be in strict timestamp order")

    return validated


def _median_price_scale(candles: Sequence[Candle]) -> float:
    positive_ranges = [candle.range_size for candle in candles if candle.range_size > 0]
    if not positive_ranges:
        return 1.0
    scale = float(median(positive_ranges))
    return scale if scale > 0 else 1.0


def _distance_to_zone(candidate: FVGCandidate, current_price: float) -> float:
    if candidate.lower_bound <= current_price <= candidate.upper_bound:
        return 0.0
    if current_price < candidate.lower_bound:
        return candidate.lower_bound - current_price
    return current_price - candidate.upper_bound


def _state_score(candidate: FVGCandidate) -> float:
    if candidate.is_resting:
        return 1.0
    if candidate.is_invalidated:
        return 0.0
    return 0.35


def _direction_score(candidate: FVGCandidate, direction_bias: IRLDirectionBias) -> float:
    if direction_bias == "neutral":
        return 0.5
    if candidate.direction == direction_bias:
        return 1.0
    return 0.0


def _proximity_score(distance_to_zone: float, *, price_scale: float) -> float:
    if price_scale <= 0:
        raise ValueError("price_scale must be > 0")
    return 1.0 / (1.0 + (distance_to_zone / price_scale))


def _recency_score(age_candles: int) -> float:
    if age_candles < 0:
        raise ValueError("age_candles must be >= 0")
    return 1.0 / (1.0 + age_candles)


def _validate_rankable_candidates(
    candidates: Sequence[FVGCandidate],
    *,
    age_candles_by_confirmed_at: Mapping[datetime, int],
) -> None:
    if not candidates:
        return

    symbols = {candidate.symbol for candidate in candidates}
    timeframes = {candidate.timeframe for candidate in candidates}
    if len(symbols) != 1:
        raise ValueError("IRL ranked candidates must all have the same symbol")
    if len(timeframes) != 1:
        raise ValueError("IRL ranked candidates must all have the same timeframe")

    for candidate in candidates:
        if candidate.width <= 0:
            raise ValueError("IRL candidates must have positive width")
        if candidate.confirmed_at not in age_candles_by_confirmed_at:
            raise ValueError("missing age_candles entry for candidate confirmed_at")
        if age_candles_by_confirmed_at[candidate.confirmed_at] < 0:
            raise ValueError("candidate age_candles must be >= 0")


def _build_reasons(
    candidate: FVGCandidate,
    *,
    direction_bias: IRLDirectionBias,
    distance_to_zone: float,
    age_candles: int,
    nearest_distance: float,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if candidate.is_resting:
        reasons.append("candidate is resting, receiving full state score")
    elif candidate.is_invalidated:
        reasons.append("candidate has been directionally invalidated, receiving zero state score")
    else:
        reasons.append("candidate has already been reached, receiving discounted state score")

    if direction_bias == "neutral":
        reasons.append("neutral bias gives all candidates midpoint direction score")
    elif candidate.direction == direction_bias:
        reasons.append(f"candidate direction aligns with {direction_bias} bias")
    else:
        reasons.append(f"candidate direction opposes {direction_bias} bias")

    if distance_to_zone == 0:
        reasons.append("current price is inside the gap zone")
    elif distance_to_zone == nearest_distance:
        reasons.append("candidate is nearest to current price among ranked IRL candidates")
    else:
        reasons.append(f"candidate is {distance_to_zone:.2f} away from current price")

    if age_candles == 0:
        reasons.append("candidate was confirmed on the as-of candle")
    elif age_candles == 1:
        reasons.append("candidate is 1 candle old")
    else:
        reasons.append(f"candidate is {age_candles} candles old")

    return tuple(reasons)


def _rank_detected_irl_candidates(
    candidates: Sequence[FVGCandidate],
    *,
    current_price: float,
    direction_bias: IRLDirectionBias,
    weights: IRLRankingWeights,
    age_candles_by_confirmed_at: Mapping[datetime, int],
    price_scale: float,
) -> list[IRLRankedCandidate]:
    _validate_rankable_candidates(
        candidates,
        age_candles_by_confirmed_at=age_candles_by_confirmed_at,
    )
    if not candidates:
        return []

    distance_by_confirmed_at = {
        candidate.confirmed_at: _distance_to_zone(candidate, current_price) for candidate in candidates
    }
    nearest_distance = min(distance_by_confirmed_at.values())

    scored_rows: list[tuple[FVGCandidate, float, float, float, int, Mapping[str, float | int | str | None], tuple[str, ...]]] = []
    for candidate in candidates:
        age_candles = age_candles_by_confirmed_at[candidate.confirmed_at]
        distance_to_zone = distance_by_confirmed_at[candidate.confirmed_at]

        state_score = _state_score(candidate)
        direction_score = _direction_score(candidate, direction_bias)
        proximity_score = _proximity_score(distance_to_zone, price_scale=price_scale)
        recency_score = _recency_score(age_candles)

        weighted_total = (
            weights.state * state_score
            + weights.direction * direction_score
            + weights.proximity * proximity_score
            + weights.recency * recency_score
        )
        total_score = weighted_total / weights.total

        feature_values = MappingProxyType(
            {
                "state": candidate.lifecycle_state,
                "candidate_direction": candidate.direction,
                "state_score": state_score,
                "direction_score": direction_score,
                "proximity_score": proximity_score,
                "recency_score": recency_score,
                "distance_to_zone": distance_to_zone,
                "age_candles": age_candles,
                "width": candidate.width,
                "price_scale": price_scale,
            }
        )
        reasons = _build_reasons(
            candidate,
            direction_bias=direction_bias,
            distance_to_zone=distance_to_zone,
            age_candles=age_candles,
            nearest_distance=nearest_distance,
        )
        scored_rows.append(
            (
                candidate,
                total_score,
                state_score,
                distance_to_zone,
                age_candles,
                feature_values,
                reasons,
            )
        )

    scored_rows.sort(
        key=lambda row: (
            -row[1],  # higher score first
            -row[2],  # higher state score first
            row[3],   # nearer candidate first
            row[4],   # newer candidate first
            row[0].confirmed_at,
            row[0].lower_bound,
            row[0].upper_bound,
            row[0].direction,
        )
    )

    ranked: list[IRLRankedCandidate] = []
    for idx, row in enumerate(scored_rows, start=1):
        ranked.append(
            IRLRankedCandidate(
                candidate=row[0],
                score=row[1],
                rank=idx,
                reasons=row[6],
                feature_values=row[5],
            )
        )
    return ranked


def rank_irl_candidates(
    candles: Iterable[Any],
    *,
    current_price: Any,
    as_of_timestamp: Any,
    direction_bias: Any,
    weights: IRLRankingWeights | None = None,
) -> list[IRLRankedCandidate]:
    current_price = _validate_current_price(current_price)
    as_of_timestamp = _validate_as_of_timestamp(as_of_timestamp)
    direction_bias = _validate_direction_bias(direction_bias)
    weights = weights or IRLRankingWeights()

    validated = _validate_candle_series(candles)
    sliced = [candle for candle in validated if candle.timestamp <= as_of_timestamp]
    if len(sliced) < 3:
        return []

    candidates = detect_fvg_candidates(sliced)
    if not candidates:
        return []

    timestamp_to_index = {candle.timestamp: idx for idx, candle in enumerate(sliced)}
    as_of_index = len(sliced) - 1
    age_candles_by_confirmed_at = {
        candidate.confirmed_at: as_of_index - timestamp_to_index[candidate.confirmed_at]
        for candidate in candidates
    }
    price_scale = _median_price_scale(sliced)

    return _rank_detected_irl_candidates(
        candidates,
        current_price=current_price,
        direction_bias=direction_bias,
        weights=weights,
        age_candles_by_confirmed_at=age_candles_by_confirmed_at,
        price_scale=price_scale,
    )
