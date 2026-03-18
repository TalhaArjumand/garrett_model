from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

from .candles import Candle
from .local_swing import (
    build_local_swing_high,
    build_local_swing_low,
    validate_local_swing_inputs,
)

ERLProxyDirection = Literal["bullish", "bearish"]


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
