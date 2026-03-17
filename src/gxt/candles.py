from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from math import isclose
from typing import Any


ALLOWED_TIMEFRAMES = frozenset({"5m", "15m", "30m", "1H", "4H", "1D"})

TIMEFRAME_TO_DELTA = {
    "5m": timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "30m": timedelta(minutes=30),
    "1H": timedelta(hours=1),
    "4H": timedelta(hours=4),
    "1D": timedelta(days=1),
}


def _validate_price(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric, got {type(value).__name__}")

    price = float(value)
    if price <= 0:
        raise ValueError(f"{name} must be positive, got {price}")

    return price


@dataclass(frozen=True)
class Candle:
    symbol: str
    timestamp: datetime
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    is_closed: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.symbol, str) or not self.symbol.strip():
            raise ValueError("symbol must be a non-empty string")

        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime")

        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be timezone-aware")

        if self.timeframe not in ALLOWED_TIMEFRAMES:
            raise ValueError(
                f"timeframe must be one of {sorted(ALLOWED_TIMEFRAMES)}, got {self.timeframe!r}"
            )

        open_price = _validate_price("open", self.open)
        high_price = _validate_price("high", self.high)
        low_price = _validate_price("low", self.low)
        close_price = _validate_price("close", self.close)

        if high_price < max(open_price, close_price, low_price):
            raise ValueError("high must be >= open, close, and low")

        if low_price > min(open_price, close_price, high_price):
            raise ValueError("low must be <= open, close, and high")

        object.__setattr__(self, "open", open_price)
        object.__setattr__(self, "high", high_price)
        object.__setattr__(self, "low", low_price)
        object.__setattr__(self, "close", close_price)

    @property
    def duration(self) -> timedelta:
        return TIMEFRAME_TO_DELTA[self.timeframe]

    @property
    def body_size(self) -> float:
        return abs(self.close - self.open)

    @property
    def range_size(self) -> float:
        return self.high - self.low

    @property
    def body_top(self) -> float:
        return max(self.open, self.close)

    @property
    def body_bottom(self) -> float:
        return min(self.open, self.close)

    @property
    def upper_wick(self) -> float:
        return self.high - self.body_top

    @property
    def lower_wick(self) -> float:
        return self.body_bottom - self.low

    @property
    def direction(self) -> str:
        if self.close > self.open:
            return "bullish"
        if self.close < self.open:
            return "bearish"
        return "doji"

    @property
    def is_bullish(self) -> bool:
        return self.direction == "bullish"

    @property
    def is_bearish(self) -> bool:
        return self.direction == "bearish"

    @property
    def is_doji(self) -> bool:
        return self.direction == "doji"

    def obeys_range_decomposition(self, rel_tol: float = 1e-12, abs_tol: float = 1e-12) -> bool:
        return isclose(
            self.body_size + self.upper_wick + self.lower_wick,
            self.range_size,
            rel_tol=rel_tol,
            abs_tol=abs_tol,
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Candle":
        timestamp_raw = payload["timestamp"]
        if isinstance(timestamp_raw, str):
            normalized = timestamp_raw.replace("Z", "+00:00")
            timestamp = datetime.fromisoformat(normalized)
        elif isinstance(timestamp_raw, datetime):
            timestamp = timestamp_raw
        else:
            raise TypeError("timestamp must be an ISO 8601 string or datetime")

        return cls(
            symbol=payload["symbol"],
            timestamp=timestamp,
            timeframe=payload["timeframe"],
            open=payload["open"],
            high=payload["high"],
            low=payload["low"],
            close=payload["close"],
            is_closed=payload.get("is_closed", True),
        )


def require_closed(candle: Candle) -> None:
    if not candle.is_closed:
        raise ValueError("candle must be closed before doctrine logic can use it")


def utc_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
) -> datetime:
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
