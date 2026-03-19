from __future__ import annotations

from math import isfinite
from typing import Any, Iterable

from .candles import Candle, require_closed


def _require_candle(name: str, value: Any) -> Candle:
    if not isinstance(value, Candle):
        raise TypeError(f"{name} must be a Candle, got {type(value).__name__}")
    require_closed(value)
    return value


def _require_directional_candle(name: str, candle: Candle) -> None:
    if candle.is_doji:
        raise ValueError(f"{name} must be bullish or bearish")


def _require_positive_range(name: str, candle: Candle) -> None:
    if candle.range_size <= 0:
        raise ValueError(f"{name} must have positive range")


def _validate_fraction_threshold(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    if numeric < 0 or numeric > 1:
        raise ValueError(f"{name} must be between 0 and 1 inclusive")
    return numeric


def same_side_wick_size(candle: Any) -> float:
    candle = _require_candle("candle", candle)
    _require_directional_candle("candle", candle)
    return candle.lower_wick if candle.is_bullish else candle.upper_wick


def same_side_wick_fraction(candle: Any) -> float:
    candle = _require_candle("candle", candle)
    _require_directional_candle("candle", candle)
    _require_positive_range("candle", candle)
    return same_side_wick_size(candle) / candle.range_size


def body_fraction(candle: Any) -> float:
    candle = _require_candle("candle", candle)
    _require_positive_range("candle", candle)
    return candle.body_size / candle.range_size


def same_side_wick_percentile(reference_candles: Iterable[Candle], candle: Any) -> float:
    candle = _require_candle("candle", candle)
    _require_directional_candle("candle", candle)
    target_fraction = same_side_wick_fraction(candle)

    comparable_fractions: list[float] = []
    for index, reference in enumerate(reference_candles):
        reference = _require_candle(f"reference_candles[{index}]", reference)
        if reference.symbol != candle.symbol:
            raise ValueError("reference candles must have the same symbol as candle")
        if reference.timeframe != candle.timeframe:
            raise ValueError("reference candles must have the same timeframe as candle")
        if reference.timestamp >= candle.timestamp:
            raise ValueError("reference candles must be strictly earlier than candle")
        if reference.direction != candle.direction:
            continue
        if reference.range_size <= 0 or reference.is_doji:
            continue
        comparable_fractions.append(same_side_wick_fraction(reference))

    if not comparable_fractions:
        raise ValueError("at least one prior same-direction reference candle is required")

    return (
        sum(fraction <= target_fraction for fraction in comparable_fractions)
        / len(comparable_fractions)
    )


def has_small_same_side_wick(candle: Any, *, threshold: Any = 0.25) -> bool:
    threshold = _validate_fraction_threshold("threshold", threshold)
    return same_side_wick_fraction(candle) <= threshold


def has_small_same_side_wick_with_context(
    reference_candles: Iterable[Candle],
    candle: Any,
    *,
    hard_cap: Any = 0.25,
    percentile_cap: Any = 0.25,
) -> bool:
    hard_cap = _validate_fraction_threshold("hard_cap", hard_cap)
    percentile_cap = _validate_fraction_threshold("percentile_cap", percentile_cap)
    return (
        same_side_wick_fraction(candle) <= hard_cap
        and same_side_wick_percentile(reference_candles, candle) <= percentile_cap
    )
