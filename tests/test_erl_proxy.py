from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.erl_proxy import (
    ERLProxy,
    build_bearish_swing_low_erl_proxy,
    build_bullish_swing_high_erl_proxy,
    validate_erl_proxy_inputs,
)


class ErlProxyTests(unittest.TestCase):
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

    def test_valid_bullish_swing_high_erl_proxy(self) -> None:
        b = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c = self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113)
        d = self.make_candle(timestamp_hour=12, open=113, high=114, low=102, close=104)

        proxy = build_bullish_swing_high_erl_proxy(b, c, d)

        self.assertIsInstance(proxy, ERLProxy)
        assert proxy is not None
        self.assertEqual(proxy.direction, "bullish")
        self.assertEqual(proxy.proxy_type, "confirmed_swing_high")
        self.assertEqual(proxy.price_level, 118)
        self.assertEqual(proxy.confirmed_at, d.timestamp)
        self.assertTrue(proxy.decision_time_safe)

    def test_valid_bearish_swing_low_erl_proxy(self) -> None:
        b = self.make_candle(timestamp_hour=10, open=120, high=125, low=111, close=114)
        c = self.make_candle(timestamp_hour=11, open=114, high=116, low=102, close=105)
        d = self.make_candle(timestamp_hour=12, open=109, high=118, low=104, close=112)

        proxy = build_bearish_swing_low_erl_proxy(b, c, d)

        self.assertIsInstance(proxy, ERLProxy)
        assert proxy is not None
        self.assertEqual(proxy.direction, "bearish")
        self.assertEqual(proxy.proxy_type, "confirmed_swing_low")
        self.assertEqual(proxy.price_level, 102)
        self.assertEqual(proxy.confirmed_at, d.timestamp)
        self.assertTrue(proxy.decision_time_safe)

    def test_bullish_proxy_returns_none_when_no_confirmed_swing_high(self) -> None:
        b = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        c = self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113)
        d = self.make_candle(timestamp_hour=12, open=113, high=118, low=102, close=104)

        self.assertIsNone(build_bullish_swing_high_erl_proxy(b, c, d))

    def test_bearish_proxy_returns_none_when_no_confirmed_swing_low(self) -> None:
        b = self.make_candle(timestamp_hour=10, open=120, high=125, low=111, close=114)
        c = self.make_candle(timestamp_hour=11, open=114, high=116, low=102, close=105)
        d = self.make_candle(timestamp_hour=12, open=105, high=118, low=102, close=112)

        self.assertIsNone(build_bearish_swing_low_erl_proxy(b, c, d))

    def test_mixed_symbol_rejection(self) -> None:
        b = self.make_candle(symbol="XAUUSD", timestamp_hour=10, open=100, high=110, low=95, close=108)
        c = self.make_candle(symbol="XAUUSD", timestamp_hour=11, open=108, high=118, low=101, close=113)
        d = self.make_candle(symbol="NQ", timestamp_hour=12, open=113, high=114, low=102, close=104)

        with self.assertRaisesRegex(ValueError, "same symbol"):
            validate_erl_proxy_inputs(b, c, d)


if __name__ == "__main__":
    unittest.main()
