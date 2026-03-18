from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.erl_proxy import (
    ERLCandidate,
    ERLProxy,
    build_bearish_swing_low_erl_proxy,
    build_bullish_swing_high_erl_proxy,
    detect_erl_candidates,
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

    def test_detect_erl_candidates_returns_old_high_and_old_low(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=116, low=99, close=101),
            self.make_candle(timestamp_hour=14, open=101, high=117, low=100, close=112),
        ]

        candidates = detect_erl_candidates(candles)

        self.assertEqual([candidate.kind for candidate in candidates], ["old_high", "old_low"])
        self.assertTrue(all(isinstance(candidate, ERLCandidate) for candidate in candidates))
        self.assertEqual(candidates[0].side, "buy_side")
        self.assertEqual(candidates[0].lower_bound, 118)
        self.assertTrue(candidates[0].is_resting)
        self.assertFalse(candidates[0].is_taken)
        self.assertEqual(candidates[1].side, "sell_side")
        self.assertEqual(candidates[1].lower_bound, 99)
        self.assertTrue(candidates[1].is_resting)
        self.assertFalse(candidates[1].is_taken)

    def test_detect_erl_candidates_marks_old_high_taken_when_later_high_sweeps_it(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=117, low=99, close=101),
            self.make_candle(timestamp_hour=14, open=101, high=121, low=100, close=112),
        ]

        candidates = detect_erl_candidates(candles)
        old_high = next(candidate for candidate in candidates if candidate.kind == "old_high")

        self.assertTrue(old_high.is_taken)
        self.assertFalse(old_high.is_resting)
        self.assertEqual(old_high.taken_at, candles[4].timestamp)

    def test_detect_erl_candidates_groups_equal_highs_with_explicit_tolerance(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120.0, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=119.6, low=105, close=111),
            self.make_candle(timestamp_hour=14, open=111, high=113, low=103, close=104),
        ]

        candidates = detect_erl_candidates(candles, equal_tolerance=0.5)

        equal_highs = [candidate for candidate in candidates if candidate.kind == "equal_highs"]
        self.assertEqual(len(equal_highs), 1)
        self.assertEqual(equal_highs[0].side, "buy_side")
        self.assertEqual(equal_highs[0].lower_bound, 119.6)
        self.assertEqual(equal_highs[0].upper_bound, 120.0)
        self.assertEqual(len(equal_highs[0].anchor_timestamps), 2)
        self.assertTrue(equal_highs[0].is_resting)

    def test_detect_erl_candidates_groups_equal_lows_with_explicit_tolerance(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=120, high=125, low=111, close=114),
            self.make_candle(timestamp_hour=11, open=114, high=116, low=100.0, close=105),
            self.make_candle(timestamp_hour=12, open=109, high=118, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=119, low=100.3, close=111),
            self.make_candle(timestamp_hour=14, open=111, high=120, low=104, close=115),
        ]

        candidates = detect_erl_candidates(candles, equal_tolerance=0.5)

        equal_lows = [candidate for candidate in candidates if candidate.kind == "equal_lows"]
        self.assertEqual(len(equal_lows), 1)
        self.assertEqual(equal_lows[0].side, "sell_side")
        self.assertEqual(equal_lows[0].lower_bound, 100.0)
        self.assertEqual(equal_lows[0].upper_bound, 100.3)
        self.assertEqual(len(equal_lows[0].anchor_timestamps), 2)
        self.assertTrue(equal_lows[0].is_resting)

    def test_detect_erl_candidates_does_not_group_equal_lows_when_later_low_takes_earlier_low(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=120, high=125, low=111, close=114),
            self.make_candle(timestamp_hour=11, open=114, high=116, low=100.3, close=105),
            self.make_candle(timestamp_hour=12, open=109, high=118, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=119, low=100.0, close=111),
            self.make_candle(timestamp_hour=14, open=111, high=120, low=104, close=115),
        ]

        candidates = detect_erl_candidates(candles, equal_tolerance=0.5)

        self.assertEqual(
            [candidate for candidate in candidates if candidate.kind == "equal_lows"],
            [],
        )

    def test_detect_erl_candidates_requires_non_negative_equal_tolerance(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
        ]

        with self.assertRaisesRegex(ValueError, "equal_tolerance must be >= 0"):
            detect_erl_candidates(candles, equal_tolerance=-0.1)


if __name__ == "__main__":
    unittest.main()
