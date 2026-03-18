from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.local_swing import (
    LocalSwingPoint,
    build_local_swing_high,
    build_local_swing_low,
    is_local_swing_high,
    is_local_swing_low,
    validate_local_swing_inputs,
)


class LocalSwingPointTests(unittest.TestCase):
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

    def test_local_swing_high(self) -> None:
        a = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        b = self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113)
        c = self.make_candle(timestamp_hour=12, open=113, high=114, low=102, close=104)

        swing = build_local_swing_high(a, b, c)

        self.assertTrue(is_local_swing_high(a, b, c))
        self.assertIsInstance(swing, LocalSwingPoint)
        assert swing is not None
        self.assertEqual(swing.kind, "swing_high")
        self.assertEqual(swing.price_level, 118)
        self.assertEqual(swing.confirmed_at, c.timestamp)

    def test_local_swing_low(self) -> None:
        a = self.make_candle(timestamp_hour=10, open=120, high=125, low=111, close=114)
        b = self.make_candle(timestamp_hour=11, open=114, high=116, low=102, close=105)
        c = self.make_candle(timestamp_hour=12, open=109, high=118, low=104, close=112)

        swing = build_local_swing_low(a, b, c)

        self.assertTrue(is_local_swing_low(a, b, c))
        self.assertIsInstance(swing, LocalSwingPoint)
        assert swing is not None
        self.assertEqual(swing.kind, "swing_low")
        self.assertEqual(swing.price_level, 102)
        self.assertEqual(swing.confirmed_at, c.timestamp)

    def test_local_swing_high_requires_strict_inequality(self) -> None:
        a = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        b = self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113)
        c = self.make_candle(timestamp_hour=12, open=113, high=118, low=102, close=104)

        self.assertFalse(is_local_swing_high(a, b, c))
        self.assertIsNone(build_local_swing_high(a, b, c))

    def test_local_swing_low_requires_strict_inequality(self) -> None:
        a = self.make_candle(timestamp_hour=10, open=120, high=125, low=111, close=114)
        b = self.make_candle(timestamp_hour=11, open=114, high=116, low=102, close=105)
        c = self.make_candle(timestamp_hour=12, open=105, high=118, low=102, close=112)

        self.assertFalse(is_local_swing_low(a, b, c))
        self.assertIsNone(build_local_swing_low(a, b, c))

    def test_non_consecutive_rejection(self) -> None:
        a = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        b = self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113)
        c = self.make_candle(timestamp_hour=13, open=113, high=114, low=102, close=104)

        with self.assertRaisesRegex(ValueError, "must be consecutive"):
            validate_local_swing_inputs(a, b, c)

    def test_unclosed_rejection(self) -> None:
        a = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        b = self.make_candle(
            timestamp_hour=11,
            open=108,
            high=118,
            low=101,
            close=113,
            is_closed=False,
        )
        c = self.make_candle(timestamp_hour=12, open=113, high=114, low=102, close=104)

        with self.assertRaisesRegex(ValueError, "must be closed"):
            validate_local_swing_inputs(a, b, c)


if __name__ == "__main__":
    unittest.main()
