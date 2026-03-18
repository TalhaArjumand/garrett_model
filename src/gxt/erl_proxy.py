from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Literal

from .candles import Candle, require_closed
from .local_swing import (
    LocalSwingPoint,
    build_local_swing_high,
    build_local_swing_low,
    iter_local_swing_highs,
    iter_local_swing_lows,
    validate_local_swing_inputs,
)

ERLProxyDirection = Literal["bullish", "bearish"]
ERLCandidateKind = Literal["old_high", "old_low", "equal_highs", "equal_lows"]
ERLCandidateSide = Literal["buy_side", "sell_side"]


@dataclass(frozen=True)
class ERLProxy:
    symbol: str
    timeframe: str
    direction: ERLProxyDirection
    proxy_type: str
    price_level: float
    left_timestamp: datetime
    pivot_timestamp: datetime
    right_timestamp: datetime
    confirmed_at: datetime
    decision_time_safe: bool
    selection_reason: str


@dataclass(frozen=True)
class ERLCandidate:
    symbol: str
    timeframe: str
    kind: ERLCandidateKind
    side: ERLCandidateSide
    lower_bound: float
    upper_bound: float
    anchor_timestamps: tuple[datetime, ...]
    confirmed_at: datetime
    is_taken: bool
    taken_at: datetime | None
    source_kind: str
    decision_time_safe: bool
    reason: str

    @property
    def is_zone(self) -> bool:
        return self.lower_bound != self.upper_bound

    @property
    def is_resting(self) -> bool:
        return not self.is_taken


def _validate_erl_candidate_series(candles: Iterable[Any]) -> list[Candle]:
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
        raise ValueError("ERL candidate series must have the same symbol")
    if len(timeframes) != 1:
        raise ValueError("ERL candidate series must have the same timeframe")

    for previous, current in zip(validated, validated[1:]):
        if not previous.timestamp < current.timestamp:
            raise ValueError("ERL candidate series must be in strict timestamp order")

    return validated


def _validate_equal_tolerance(equal_tolerance: float | None) -> float | None:
    if equal_tolerance is None:
        return None
    if isinstance(equal_tolerance, bool) or not isinstance(equal_tolerance, (int, float)):
        raise TypeError("equal_tolerance must be numeric or None")
    tolerance = float(equal_tolerance)
    if tolerance < 0:
        raise ValueError("equal_tolerance must be >= 0")
    return tolerance


def _build_old_high_candidate(swing: LocalSwingPoint) -> ERLCandidate:
    return ERLCandidate(
        symbol=swing.symbol,
        timeframe=swing.timeframe,
        kind="old_high",
        side="buy_side",
        lower_bound=swing.price_level,
        upper_bound=swing.price_level,
        anchor_timestamps=(swing.left_timestamp, swing.pivot_timestamp, swing.right_timestamp),
        confirmed_at=swing.confirmed_at,
        is_taken=False,
        taken_at=None,
        source_kind="confirmed_swing_high",
        decision_time_safe=True,
        reason="Old high candidate derived from a confirmed local swing high.",
    )


def _build_old_low_candidate(swing: LocalSwingPoint) -> ERLCandidate:
    return ERLCandidate(
        symbol=swing.symbol,
        timeframe=swing.timeframe,
        kind="old_low",
        side="sell_side",
        lower_bound=swing.price_level,
        upper_bound=swing.price_level,
        anchor_timestamps=(swing.left_timestamp, swing.pivot_timestamp, swing.right_timestamp),
        confirmed_at=swing.confirmed_at,
        is_taken=False,
        taken_at=None,
        source_kind="confirmed_swing_low",
        decision_time_safe=True,
        reason="Old low candidate derived from a confirmed local swing low.",
    )


def _find_take_timestamp(
    candles: list[Candle],
    *,
    side: ERLCandidateSide,
    threshold: float,
    confirmed_at: datetime,
) -> datetime | None:
    for candle in candles:
        if candle.timestamp <= confirmed_at:
            continue
        if side == "buy_side" and candle.high > threshold:
            return candle.timestamp
        if side == "sell_side" and candle.low < threshold:
            return candle.timestamp
    return None


def _with_take_state(
    candidate: ERLCandidate,
    *,
    taken_at: datetime | None,
) -> ERLCandidate:
    return ERLCandidate(
        symbol=candidate.symbol,
        timeframe=candidate.timeframe,
        kind=candidate.kind,
        side=candidate.side,
        lower_bound=candidate.lower_bound,
        upper_bound=candidate.upper_bound,
        anchor_timestamps=candidate.anchor_timestamps,
        confirmed_at=candidate.confirmed_at,
        is_taken=taken_at is not None,
        taken_at=taken_at,
        source_kind=candidate.source_kind,
        decision_time_safe=candidate.decision_time_safe,
        reason=candidate.reason,
    )


def _group_equal_swings(
    swings: list[LocalSwingPoint],
    *,
    equal_tolerance: float,
    taken_at_by_pivot: dict[datetime, datetime | None],
) -> list[list[LocalSwingPoint]]:
    if len(swings) < 2:
        return []

    groups: list[list[LocalSwingPoint]] = []
    current_group = [swings[0]]

    for swing in swings[1:]:
        proposed_levels = [point.price_level for point in current_group] + [swing.price_level]
        if max(proposed_levels) - min(proposed_levels) <= equal_tolerance:
            if any(
                taken_at_by_pivot.get(point.pivot_timestamp) is not None
                and taken_at_by_pivot[point.pivot_timestamp] <= swing.pivot_timestamp
                for point in current_group
            ):
                if len(current_group) >= 2:
                    groups.append(current_group)
                current_group = [swing]
                continue
            current_group.append(swing)
            continue

        if len(current_group) >= 2:
            groups.append(current_group)
        current_group = [swing]

    if len(current_group) >= 2:
        groups.append(current_group)

    return groups


def _build_equal_highs_candidate(group: list[LocalSwingPoint]) -> ERLCandidate:
    return ERLCandidate(
        symbol=group[0].symbol,
        timeframe=group[0].timeframe,
        kind="equal_highs",
        side="buy_side",
        lower_bound=min(point.price_level for point in group),
        upper_bound=max(point.price_level for point in group),
        anchor_timestamps=tuple(point.pivot_timestamp for point in group),
        confirmed_at=max(point.confirmed_at for point in group),
        is_taken=False,
        taken_at=None,
        source_kind="grouped_swing_highs",
        decision_time_safe=True,
        reason="Equal-highs candidate grouped from confirmed local swing highs within explicit tolerance.",
    )


def _build_equal_lows_candidate(group: list[LocalSwingPoint]) -> ERLCandidate:
    return ERLCandidate(
        symbol=group[0].symbol,
        timeframe=group[0].timeframe,
        kind="equal_lows",
        side="sell_side",
        lower_bound=min(point.price_level for point in group),
        upper_bound=max(point.price_level for point in group),
        anchor_timestamps=tuple(point.pivot_timestamp for point in group),
        confirmed_at=max(point.confirmed_at for point in group),
        is_taken=False,
        taken_at=None,
        source_kind="grouped_swing_lows",
        decision_time_safe=True,
        reason="Equal-lows candidate grouped from confirmed local swing lows within explicit tolerance.",
    )


def validate_erl_proxy_inputs(b: Any, c: Any, d: Any) -> tuple[Candle, Candle, Candle]:
    return validate_local_swing_inputs(b, c, d)


def build_bullish_swing_high_erl_proxy(b: Any, c: Any, d: Any) -> ERLProxy | None:
    b, c, d = validate_erl_proxy_inputs(b, c, d)
    swing_high = build_local_swing_high(b, c, d)
    if swing_high is None:
        return None

    return ERLProxy(
        symbol=c.symbol,
        timeframe=c.timeframe,
        direction="bullish",
        proxy_type="confirmed_swing_high",
        price_level=swing_high.price_level,
        left_timestamp=b.timestamp,
        pivot_timestamp=c.timestamp,
        right_timestamp=d.timestamp,
        confirmed_at=d.timestamp,
        decision_time_safe=True,
        selection_reason=(
            "Bullish ERL research proxy uses the high of a confirmed local swing-high "
            "pivot after right-side confirmation."
        ),
    )


def build_bearish_swing_low_erl_proxy(b: Any, c: Any, d: Any) -> ERLProxy | None:
    b, c, d = validate_erl_proxy_inputs(b, c, d)
    swing_low = build_local_swing_low(b, c, d)
    if swing_low is None:
        return None

    return ERLProxy(
        symbol=c.symbol,
        timeframe=c.timeframe,
        direction="bearish",
        proxy_type="confirmed_swing_low",
        price_level=swing_low.price_level,
        left_timestamp=b.timestamp,
        pivot_timestamp=c.timestamp,
        right_timestamp=d.timestamp,
        confirmed_at=d.timestamp,
        decision_time_safe=True,
        selection_reason=(
            "Bearish ERL research proxy uses the low of a confirmed local swing-low "
            "pivot after right-side confirmation."
        ),
    )


def detect_erl_candidates(
    candles: Iterable[Any],
    *,
    equal_tolerance: float | None = None,
) -> list[ERLCandidate]:
    validated = _validate_erl_candidate_series(candles)
    tolerance = _validate_equal_tolerance(equal_tolerance)
    if not validated:
        return []

    swing_highs = list(iter_local_swing_highs(validated))
    swing_lows = list(iter_local_swing_lows(validated))
    swing_high_taken_at = {
        swing.pivot_timestamp: _find_take_timestamp(
            validated,
            side="buy_side",
            threshold=swing.price_level,
            confirmed_at=swing.confirmed_at,
        )
        for swing in swing_highs
    }
    swing_low_taken_at = {
        swing.pivot_timestamp: _find_take_timestamp(
            validated,
            side="sell_side",
            threshold=swing.price_level,
            confirmed_at=swing.confirmed_at,
        )
        for swing in swing_lows
    }

    candidates: list[ERLCandidate] = []
    candidates.extend(
        _with_take_state(
            _build_old_high_candidate(swing),
            taken_at=swing_high_taken_at[swing.pivot_timestamp],
        )
        for swing in swing_highs
    )
    candidates.extend(
        _with_take_state(
            _build_old_low_candidate(swing),
            taken_at=swing_low_taken_at[swing.pivot_timestamp],
        )
        for swing in swing_lows
    )

    if tolerance is not None:
        candidates.extend(
            _with_take_state(
                _build_equal_highs_candidate(group),
                taken_at=_find_take_timestamp(
                    validated,
                    side="buy_side",
                    threshold=max(point.price_level for point in group),
                    confirmed_at=max(point.confirmed_at for point in group),
                ),
            )
            for group in _group_equal_swings(
                swing_highs,
                equal_tolerance=tolerance,
                taken_at_by_pivot=swing_high_taken_at,
            )
        )
        candidates.extend(
            _with_take_state(
                _build_equal_lows_candidate(group),
                taken_at=_find_take_timestamp(
                    validated,
                    side="sell_side",
                    threshold=min(point.price_level for point in group),
                    confirmed_at=max(point.confirmed_at for point in group),
                ),
            )
            for group in _group_equal_swings(
                swing_lows,
                equal_tolerance=tolerance,
                taken_at_by_pivot=swing_low_taken_at,
            )
        )

    return sorted(candidates, key=lambda candidate: (candidate.confirmed_at, candidate.kind, candidate.lower_bound, candidate.upper_bound))
