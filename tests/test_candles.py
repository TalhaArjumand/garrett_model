from __future__ import annotations

import json
import unittest
from math import isclose
from pathlib import Path

from gxt.candles import Candle, require_closed, utc_datetime


class CandleTests(unittest.TestCase):
    def test_valid_candle_is_accepted(self) -> None:
        candle = Candle(
            symbol="XAUUSD",
            timestamp=utc_datetime(2026, 3, 17, 10, 0),
            timeframe="5m",
            open=3000.0,
            high=3005.0,
            low=2998.0,
            close=3002.0,
            is_closed=True,
        )

        self.assertEqual(candle.symbol, "XAUUSD")
        self.assertEqual(candle.timeframe, "5m")
        self.assertTrue(candle.is_closed)

    def test_bullish_candle_geometry_is_correct(self) -> None:
        candle = Candle(
            symbol="XAUUSD",
            timestamp=utc_datetime(2026, 3, 17, 10, 0),
            timeframe="5m",
            open=100.0,
            high=110.0,
            low=95.0,
            close=107.0,
        )

        self.assertEqual(candle.direction, "bullish")
        self.assertTrue(candle.is_bullish)
        self.assertFalse(candle.is_bearish)
        self.assertFalse(candle.is_doji)
        self.assertEqual(candle.body_top, 107.0)
        self.assertEqual(candle.body_bottom, 100.0)
        self.assertEqual(candle.body_size, 7.0)
        self.assertEqual(candle.range_size, 15.0)
        self.assertEqual(candle.upper_wick, 3.0)
        self.assertEqual(candle.lower_wick, 5.0)
        self.assertTrue(candle.obeys_range_decomposition())

    def test_bearish_candle_geometry_is_correct(self) -> None:
        candle = Candle(
            symbol="NQ",
            timestamp=utc_datetime(2026, 3, 17, 14, 0),
            timeframe="1H",
            open=210.0,
            high=214.0,
            low=200.0,
            close=203.0,
        )

        self.assertEqual(candle.direction, "bearish")
        self.assertFalse(candle.is_bullish)
        self.assertTrue(candle.is_bearish)
        self.assertFalse(candle.is_doji)
        self.assertEqual(candle.body_top, 210.0)
        self.assertEqual(candle.body_bottom, 203.0)
        self.assertEqual(candle.body_size, 7.0)
        self.assertEqual(candle.range_size, 14.0)
        self.assertEqual(candle.upper_wick, 4.0)
        self.assertEqual(candle.lower_wick, 3.0)
        self.assertTrue(candle.obeys_range_decomposition())

    def test_doji_geometry_is_correct(self) -> None:
        candle = Candle(
            symbol="EURUSD",
            timestamp=utc_datetime(2026, 3, 17, 16, 0),
            timeframe="15m",
            open=1.1000,
            high=1.1015,
            low=1.0980,
            close=1.1000,
        )

        self.assertEqual(candle.direction, "doji")
        self.assertFalse(candle.is_bullish)
        self.assertFalse(candle.is_bearish)
        self.assertTrue(candle.is_doji)
        self.assertEqual(candle.body_top, 1.1000)
        self.assertEqual(candle.body_bottom, 1.1000)
        self.assertEqual(candle.body_size, 0.0)
        self.assertTrue(isclose(candle.upper_wick, 0.0015))
        self.assertTrue(isclose(candle.lower_wick, 0.0020))
        self.assertTrue(candle.obeys_range_decomposition())

    def test_invalid_timeframe_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "timeframe must be one of"):
            Candle(
                symbol="XAUUSD",
                timestamp=utc_datetime(2026, 3, 17, 10, 0),
                timeframe="7m",
                open=3000.0,
                high=3005.0,
                low=2998.0,
                close=3002.0,
            )

    def test_open_outside_range_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "low must be <= open, close, and high"):
            Candle(
                symbol="XAUUSD",
                timestamp=utc_datetime(2026, 3, 17, 10, 0),
                timeframe="5m",
                open=2997.0,
                high=3005.0,
                low=2998.0,
                close=3002.0,
            )

    def test_close_outside_range_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "high must be >= open, close, and low"):
            Candle(
                symbol="XAUUSD",
                timestamp=utc_datetime(2026, 3, 17, 10, 0),
                timeframe="5m",
                open=3000.0,
                high=3005.0,
                low=2998.0,
                close=3006.0,
            )

    def test_naive_timestamp_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            Candle.from_dict(
                {
                    "symbol": "XAUUSD",
                    "timestamp": "2026-03-17T10:00:00",
                    "timeframe": "5m",
                    "open": 3000.0,
                    "high": 3005.0,
                    "low": 2998.0,
                    "close": 3002.0,
                    "is_closed": True,
                }
            )

    def test_unclosed_candle_is_blocked_for_doctrine_logic(self) -> None:
        candle = Candle(
            symbol="XAUUSD",
            timestamp=utc_datetime(2026, 3, 17, 10, 0),
            timeframe="5m",
            open=3000.0,
            high=3005.0,
            low=2998.0,
            close=3002.0,
            is_closed=False,
        )

        with self.assertRaisesRegex(ValueError, "must be closed"):
            require_closed(candle)

    def test_golden_examples_parse_into_candles(self) -> None:
        golden_path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "golden"
            / "candle_examples.json"
        )
        payload = json.loads(golden_path.read_text())

        valid_examples = payload["valid_examples"]
        self.assertGreaterEqual(len(valid_examples), 2)

        first = Candle.from_dict(valid_examples[0]["candle"])
        self.assertEqual(first.symbol, valid_examples[0]["candle"]["symbol"])
        self.assertTrue(first.is_closed)
        self.assertTrue(first.obeys_range_decomposition())


if __name__ == "__main__":
    unittest.main()
