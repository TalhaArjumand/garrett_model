from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.swing_research import (
    is_bearish_rare_c3_closure_subtype,
    is_bullish_rare_c3_closure_subtype,
)


class SwingResearchTests(unittest.TestCase):
    def make_candle(
        self,
        *,
        symbol: str = "XAUUSD",
        timestamp_hour: int,
        timeframe: str = "1H",
        open: float,
        high: float,
        low: float,
        close: float,
        is_closed: bool = True,
    ) -> Candle:
        return Candle(
            symbol=symbol,
            timestamp=utc_datetime(2026, 3, 17, timestamp_hour, 0),
            timeframe=timeframe,
            open=open,
            high=high,
            low=low,
            close=close,
            is_closed=is_closed,
        )

    def test_valid_bullish_rare_c3_closure_subtype(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=92, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=105, close=118)

        self.assertTrue(is_bullish_rare_c3_closure_subtype(c1, c2, c3))

    def test_bullish_rare_c3_closure_subtype_requires_c2_close_above_c1_high(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=92, close=111)
        c3 = self.make_candle(timestamp_hour=12, open=111, high=120, low=105, close=118)

        self.assertFalse(is_bullish_rare_c3_closure_subtype(c1, c2, c3))

    def test_bullish_rare_c3_closure_subtype_requires_c3_support_above_eq_of_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=92, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=104, close=118)

        self.assertFalse(is_bullish_rare_c3_closure_subtype(c1, c2, c3))

    def test_valid_bearish_rare_c3_closure_subtype(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=101, low=90, close=92)

        self.assertTrue(is_bearish_rare_c3_closure_subtype(c1, c2, c3))

    def test_bearish_rare_c3_closure_subtype_requires_c2_close_below_c1_low(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=94, close=99)
        c3 = self.make_candle(timestamp_hour=12, open=99, high=101, low=90, close=92)

        self.assertFalse(is_bearish_rare_c3_closure_subtype(c1, c2, c3))

    def test_bearish_rare_c3_closure_subtype_requires_c3_resistance_below_eq_of_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=106, low=90, close=92)

        self.assertFalse(is_bearish_rare_c3_closure_subtype(c1, c2, c3))


if __name__ == "__main__":
    unittest.main()
