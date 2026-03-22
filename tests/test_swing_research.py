from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.swing_research import (
    has_bearish_c4_after_type_d_candidate,
    has_bearish_type_b_additive_extension_c3_quality_candidate,
    has_bearish_c4_after_type_b_additive_extension_candidate,
    has_bearish_c4_after_type_b_additive_extension_expansion_quality_candidate,
    has_bullish_c4_after_type_d_candidate,
    has_bullish_type_b_additive_extension_c3_quality_candidate,
    has_bullish_c4_after_type_b_additive_extension_candidate,
    has_bullish_c4_after_type_b_additive_extension_expansion_quality_candidate,
    is_bearish_type_d,
    is_bearish_type_b_additive_extension,
    is_bullish_type_d,
    is_bullish_type_b_additive_extension,
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

    def test_valid_bullish_type_b_additive_extension(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=113, close=118)

        self.assertTrue(is_bullish_type_b_additive_extension(c1, c2, c3))

    def test_bullish_type_b_additive_extension_requires_c2_close_above_c1_body_top(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=109)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=113, close=118)

        self.assertFalse(is_bullish_type_b_additive_extension(c1, c2, c3))

    def test_bullish_type_b_additive_extension_requires_c3_support_above_eq_of_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=107, close=118)

        self.assertFalse(is_bullish_type_b_additive_extension(c1, c2, c3))

    def test_valid_bullish_type_b_additive_extension_c3_quality_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=113, close=118)

        self.assertTrue(has_bullish_type_b_additive_extension_c3_quality_candidate(c1, c2, c3))

    def test_bullish_type_b_additive_extension_c3_quality_rejects_large_lower_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=108, close=118)

        self.assertFalse(
            has_bullish_type_b_additive_extension_c3_quality_candidate(c1, c2, c3)
        )

    def test_valid_bearish_type_b_additive_extension(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=97, low=90, close=92)

        self.assertTrue(is_bearish_type_b_additive_extension(c1, c2, c3))

    def test_bearish_type_b_additive_extension_requires_c2_close_below_c1_body_bottom(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=99, high=100, low=90, close=92)

        self.assertFalse(is_bearish_type_b_additive_extension(c1, c2, c3))

    def test_bearish_type_b_additive_extension_requires_c3_resistance_below_eq_of_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=103, low=90, close=92)

        self.assertFalse(is_bearish_type_b_additive_extension(c1, c2, c3))

    def test_valid_bearish_type_b_additive_extension_c3_quality_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=97, low=90, close=92)

        self.assertTrue(has_bearish_type_b_additive_extension_c3_quality_candidate(c1, c2, c3))

    def test_bearish_type_b_additive_extension_c3_quality_rejects_large_upper_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=101, low=90, close=92)

        self.assertFalse(
            has_bearish_type_b_additive_extension_c3_quality_candidate(c1, c2, c3)
        )

    def test_valid_bullish_c4_after_type_b_additive_extension_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=113, close=118)
        c4 = self.make_candle(timestamp_hour=13, open=118, high=125, low=117, close=124)

        self.assertTrue(has_bullish_c4_after_type_b_additive_extension_candidate(c1, c2, c3, c4))

    def test_bullish_c4_after_type_b_additive_extension_candidate_requires_extension(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=109)
        c3 = self.make_candle(timestamp_hour=12, open=111, high=120, low=105, close=118)
        c4 = self.make_candle(timestamp_hour=13, open=118, high=125, low=117, close=124)

        self.assertFalse(has_bullish_c4_after_type_b_additive_extension_candidate(c1, c2, c3, c4))

    def test_valid_bullish_c4_after_type_b_additive_extension_expansion_quality_candidate(
        self,
    ) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=113, close=118)
        c4 = self.make_candle(timestamp_hour=13, open=118, high=125, low=117, close=124)

        self.assertTrue(
            has_bullish_c4_after_type_b_additive_extension_expansion_quality_candidate(
                c1, c2, c3, c4
            )
        )

    def test_bullish_c4_after_type_b_additive_extension_expansion_quality_rejects_large_lower_wick(
        self,
    ) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=120, low=113, close=118)
        c4 = self.make_candle(timestamp_hour=13, open=123, high=125, low=117, close=124)

        self.assertFalse(
            has_bullish_c4_after_type_b_additive_extension_expansion_quality_candidate(
                c1, c2, c3, c4
            )
        )

    def test_valid_bearish_c4_after_type_b_additive_extension_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=101, low=90, close=92)
        c4 = self.make_candle(timestamp_hour=13, open=92, high=94, low=85, close=86)

        self.assertTrue(has_bearish_c4_after_type_b_additive_extension_candidate(c1, c2, c3, c4))

    def test_bearish_c4_after_type_b_additive_extension_candidate_requires_extension(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=99, high=101, low=90, close=92)
        c4 = self.make_candle(timestamp_hour=13, open=92, high=94, low=85, close=86)

        self.assertFalse(has_bearish_c4_after_type_b_additive_extension_candidate(c1, c2, c3, c4))

    def test_valid_bearish_c4_after_type_b_additive_extension_expansion_quality_candidate(
        self,
    ) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=101, low=90, close=92)
        c4 = self.make_candle(timestamp_hour=13, open=92, high=93, low=85, close=86)

        self.assertTrue(
            has_bearish_c4_after_type_b_additive_extension_expansion_quality_candidate(
                c1, c2, c3, c4
            )
        )

    def test_bearish_c4_after_type_b_additive_extension_expansion_quality_rejects_large_upper_wick(
        self,
    ) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=110, high=110.5, low=94, close=96)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=101, low=90, close=92)
        c4 = self.make_candle(timestamp_hour=13, open=92, high=95, low=85, close=86)

        self.assertFalse(
            has_bearish_c4_after_type_b_additive_extension_expansion_quality_candidate(
                c1, c2, c3, c4
            )
        )

    def test_valid_bullish_type_d(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=103, high=104, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=103, low=93, close=97)

        self.assertTrue(is_bullish_type_d(c1, c2, c3))

    def test_bullish_type_d_requires_strict_inside_c3_high(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=103, high=104, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=104, low=93, close=97)

        self.assertFalse(is_bullish_type_d(c1, c2, c3))

    def test_bullish_type_d_rejects_type_a_case(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=95, high=104, low=92, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=100, high=103, low=93, close=96)

        self.assertFalse(is_bullish_type_d(c1, c2, c3))

    def test_bullish_type_d_rejects_type_b_additive_extension_case(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=99.5, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=114, high=115, low=113, close=114.5)

        self.assertFalse(is_bullish_type_d(c1, c2, c3))

    def test_valid_bullish_c4_after_type_d_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=103, high=104, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=103, low=93, close=97)
        c4 = self.make_candle(timestamp_hour=13, open=100, high=109, low=99, close=108)

        self.assertTrue(has_bullish_c4_after_type_d_candidate(c1, c2, c3, c4))

    def test_bullish_c4_after_type_d_candidate_requires_eq_of_c3_respect(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=103, high=104, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=96, high=103, low=93, close=97)
        c4 = self.make_candle(timestamp_hour=13, open=98, high=109, low=98, close=108)

        self.assertFalse(has_bullish_c4_after_type_d_candidate(c1, c2, c3, c4))

    def test_valid_bearish_type_d(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=107, high=120, low=106, close=118)
        c3 = self.make_candle(timestamp_hour=12, open=117, high=119, low=110, close=112)

        self.assertTrue(is_bearish_type_d(c1, c2, c3))

    def test_bearish_type_d_requires_strict_inside_c3_low(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=107, high=120, low=106, close=118)
        c3 = self.make_candle(timestamp_hour=12, open=117, high=119, low=106, close=112)

        self.assertFalse(is_bearish_type_d(c1, c2, c3))

    def test_bearish_type_d_rejects_strict_type_c_case(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=107, high=120, low=106, close=118)
        c3 = self.make_candle(timestamp_hour=12, open=117, high=119, low=100, close=105)

        self.assertFalse(is_bearish_type_d(c1, c2, c3))

    def test_valid_bearish_c4_after_type_d_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=107, high=120, low=106, close=118)
        c3 = self.make_candle(timestamp_hour=12, open=117, high=119, low=110, close=112)
        c4 = self.make_candle(timestamp_hour=13, open=112, high=114, low=100, close=101)

        self.assertTrue(has_bearish_c4_after_type_d_candidate(c1, c2, c3, c4))


if __name__ == "__main__":
    unittest.main()
