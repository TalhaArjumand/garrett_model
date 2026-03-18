from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Iterator, Literal

from .candles import Candle
from .sequence_primitives import validate_sequence_inputs

LocalSwingKind = Literal["swing_high", "swing_low"]


@dataclass(frozen=True)
class LocalSwingPoint:
    symbol: str
    timeframe: str
    kind: LocalSwingKind
    price_level: float
    left_timestamp: datetime
    pivot_timestamp: datetime
    right_timestamp: datetime
    confirmed_at: datetime


def validate_local_swing_inputs(a: Any, b: Any, c: Any) -> tuple[Candle, Candle, Candle]:
    return validate_sequence_inputs(a, b, c)


def is_local_swing_high(a: Any, b: Any, c: Any) -> bool:
    a, b, c = validate_local_swing_inputs(a, b, c)
    return b.high > a.high and b.high > c.high


def is_local_swing_low(a: Any, b: Any, c: Any) -> bool:
    a, b, c = validate_local_swing_inputs(a, b, c)
    return b.low < a.low and b.low < c.low


def build_local_swing_high(a: Any, b: Any, c: Any) -> LocalSwingPoint | None:
    a, b, c = validate_local_swing_inputs(a, b, c)
    if not is_local_swing_high(a, b, c):
        return None

    return LocalSwingPoint(
        symbol=b.symbol,
        timeframe=b.timeframe,
        kind="swing_high",
        price_level=b.high,
        left_timestamp=a.timestamp,
        pivot_timestamp=b.timestamp,
        right_timestamp=c.timestamp,
        confirmed_at=c.timestamp,
    )


def build_local_swing_low(a: Any, b: Any, c: Any) -> LocalSwingPoint | None:
    a, b, c = validate_local_swing_inputs(a, b, c)
    if not is_local_swing_low(a, b, c):
        return None

    return LocalSwingPoint(
        symbol=b.symbol,
        timeframe=b.timeframe,
        kind="swing_low",
        price_level=b.low,
        left_timestamp=a.timestamp,
        pivot_timestamp=b.timestamp,
        right_timestamp=c.timestamp,
        confirmed_at=c.timestamp,
    )


def iter_local_swing_highs(candles: Iterable[Candle]) -> Iterator[LocalSwingPoint]:
    candles = list(candles)
    for idx in range(len(candles) - 2):
        try:
            swing = build_local_swing_high(candles[idx], candles[idx + 1], candles[idx + 2])
        except ValueError:
            continue
        if swing is not None:
            yield swing


def iter_local_swing_lows(candles: Iterable[Candle]) -> Iterator[LocalSwingPoint]:
    candles = list(candles)
    for idx in range(len(candles) - 2):
        try:
            swing = build_local_swing_low(candles[idx], candles[idx + 1], candles[idx + 2])
        except ValueError:
            continue
        if swing is not None:
            yield swing


def iter_local_swing_points(candles: Iterable[Candle]) -> Iterator[LocalSwingPoint]:
    candles = list(candles)
    for idx in range(len(candles) - 2):
        try:
            high = build_local_swing_high(candles[idx], candles[idx + 1], candles[idx + 2])
            low = build_local_swing_low(candles[idx], candles[idx + 1], candles[idx + 2])
        except ValueError:
            continue
        if high is not None:
            yield high
        if low is not None:
            yield low
