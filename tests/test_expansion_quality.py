from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.expansion_quality import (
    body_fraction,
    has_small_same_side_wick,
    has_small_same_side_wick_with_context,
    same_side_wick_fraction,
    same_side_wick_percentile,
    same_side_wick_size,
)


class ExpansionQualityTests(unittest.TestCase):
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

    def test_same_side_wick_size_uses_lower_wick_for_bullish_candle(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        self.assertEqual(same_side_wick_size(candle), 5)

    def test_same_side_wick_size_uses_upper_wick_for_bearish_candle(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=108, high=112, low=95, close=100)
        self.assertEqual(same_side_wick_size(candle), 4)

    def test_same_side_wick_fraction_rejects_doji(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=100)
        with self.assertRaises(ValueError):
            same_side_wick_fraction(candle)

    def test_same_side_wick_fraction_rejects_zero_range(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=100, low=100, close=100)
        with self.assertRaises(ValueError):
            same_side_wick_fraction(candle)

    def test_body_fraction_is_scale_free(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=107)
        self.assertAlmostEqual(body_fraction(candle), 7 / 15)

    def test_has_small_same_side_wick_passes_on_boundary(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=108, low=98, close=106)
        self.assertTrue(has_small_same_side_wick(candle, threshold=0.2))

    def test_has_small_same_side_wick_rejects_larger_fraction(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        self.assertFalse(has_small_same_side_wick(candle, threshold=0.25))

    def test_same_side_wick_percentile_uses_prior_same_direction_reference_set(self) -> None:
        references = [
            self.make_candle(timestamp_hour=7, open=100, high=110, low=95, close=108),   # 5/15
            self.make_candle(timestamp_hour=8, open=105, high=112, low=103, close=110),  # 2/9
            self.make_candle(timestamp_hour=9, open=110, high=118, low=109, close=116),  # 1/9
            self.make_candle(timestamp_hour=9, timeframe="4H", open=110, high=118, low=109, close=116),
        ]
        candle = self.make_candle(timestamp_hour=10, open=116, high=124, low=114, close=122)  # 2/10

        with self.assertRaises(ValueError):
            same_side_wick_percentile(references, candle)

        percentile = same_side_wick_percentile(references[:3], candle)
        self.assertAlmostEqual(percentile, 1 / 3)

    def test_same_side_wick_percentile_rejects_future_reference(self) -> None:
        candle = self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108)
        future_reference = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)

        with self.assertRaises(ValueError):
            same_side_wick_percentile([future_reference], candle)

    def test_has_small_same_side_wick_with_context_requires_hard_cap_and_percentile_cap(
        self,
    ) -> None:
        references = [
            self.make_candle(timestamp_hour=6, open=100, high=110, low=95, close=108),   # 5/15
            self.make_candle(timestamp_hour=7, open=108, high=116, low=106, close=114),  # 2/10
            self.make_candle(timestamp_hour=8, open=114, high=122, low=113, close=120),  # 1/9
            self.make_candle(timestamp_hour=9, open=120, high=128, low=119, close=126),  # 1/9
        ]
        passing = self.make_candle(timestamp_hour=10, open=126, high=134, low=125, close=132)  # 1/9
        failing_percentile = self.make_candle(
            timestamp_hour=10,
            open=126,
            high=135,
            low=123,
            close=132,
        )  # 3/12

        self.assertTrue(
            has_small_same_side_wick_with_context(
                references,
                passing,
                hard_cap=0.25,
                percentile_cap=0.5,
            )
        )
        self.assertFalse(
            has_small_same_side_wick_with_context(
                references,
                failing_percentile,
                hard_cap=0.25,
                percentile_cap=0.25,
            )
        )


if __name__ == "__main__":
    unittest.main()
