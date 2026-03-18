from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.fvg import (
    FairValueGap,
    build_bearish_fvg,
    build_bullish_fvg,
    detect_fvg,
    is_bearish_fvg,
    is_bullish_fvg,
    validate_fvg_inputs,
)


class FairValueGapTests(unittest.TestCase):
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

    def test_valid_bullish_fvg(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119)
        c3 = self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123)

        gap = build_bullish_fvg(c1, c2, c3)

        self.assertTrue(is_bullish_fvg(c1, c2, c3))
        self.assertIsInstance(gap, FairValueGap)
        assert gap is not None
        self.assertEqual(gap.direction, "bullish")
        self.assertEqual(gap.lower_bound, 110)
        self.assertEqual(gap.upper_bound, 112)
        self.assertEqual(gap.width, 2)

    def test_valid_bearish_fvg(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=120, high=125, low=110, close=112)
        c2 = self.make_candle(timestamp_hour=11, open=111, high=113, low=100, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=102, high=108, low=95, close=97)

        gap = build_bearish_fvg(c1, c2, c3)

        self.assertTrue(is_bearish_fvg(c1, c2, c3))
        self.assertIsInstance(gap, FairValueGap)
        assert gap is not None
        self.assertEqual(gap.direction, "bearish")
        self.assertEqual(gap.lower_bound, 108)
        self.assertEqual(gap.upper_bound, 110)
        self.assertEqual(gap.width, 2)

    def test_bullish_fvg_requires_strict_gap(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119)
        c3 = self.make_candle(timestamp_hour=12, open=118, high=125, low=110, close=123)

        self.assertFalse(is_bullish_fvg(c1, c2, c3))
        self.assertIsNone(build_bullish_fvg(c1, c2, c3))

    def test_bearish_fvg_requires_strict_gap(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=120, high=125, low=110, close=112)
        c2 = self.make_candle(timestamp_hour=11, open=111, high=113, low=100, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=102, high=110, low=95, close=97)

        self.assertFalse(is_bearish_fvg(c1, c2, c3))
        self.assertIsNone(build_bearish_fvg(c1, c2, c3))

    def test_detect_fvg_returns_none_when_no_gap_exists(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=112, low=101, close=104)
        c3 = self.make_candle(timestamp_hour=12, open=104, high=111, low=99, close=110)

        self.assertIsNone(detect_fvg(c1, c2, c3))

    def test_detect_fvg_returns_bullish_gap(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119)
        c3 = self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123)

        gap = detect_fvg(c1, c2, c3)

        self.assertIsNotNone(gap)
        assert gap is not None
        self.assertEqual(gap.direction, "bullish")

    def test_mixed_timeframe_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, timeframe="1H", open=100, high=110, low=95, close=108)
        c2 = self.make_candle(timestamp_hour=11, timeframe="1H", open=108, high=120, low=107, close=119)
        c3 = Candle(
            symbol="XAUUSD",
            timestamp=utc_datetime(2026, 3, 17, 12, 0),
            timeframe="30m",
            open=118,
            high=125,
            low=112,
            close=123,
        )

        with self.assertRaisesRegex(ValueError, "same timeframe"):
            validate_fvg_inputs(c1, c2, c3)

    def test_non_consecutive_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119)
        c3 = self.make_candle(timestamp_hour=13, open=118, high=125, low=112, close=123)

        with self.assertRaisesRegex(ValueError, "must be consecutive"):
            validate_fvg_inputs(c1, c2, c3)

    def test_unclosed_candle_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c2 = self.make_candle(
            timestamp_hour=11,
            open=108,
            high=120,
            low=107,
            close=119,
            is_closed=False,
        )
        c3 = self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123)

        with self.assertRaisesRegex(ValueError, "must be closed"):
            validate_fvg_inputs(c1, c2, c3)


if __name__ == "__main__":
    unittest.main()
