from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

from .candles import Candle
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
