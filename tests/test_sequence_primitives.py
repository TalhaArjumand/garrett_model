from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.sequence_primitives import (
    has_bearish_c4_after_c3_closure_candidate,
    has_bearish_c4_after_c3_closure_expansion_quality_candidate,
    has_bearish_c4_continuation_candidate,
    closes_inside_range,
    equilibrium,
    is_bearish_c2_reversal_to_expansion,
    is_bearish_c3_closure,
    has_bearish_c3_support,
    has_bullish_c4_after_c3_closure_candidate,
    has_bullish_c4_after_c3_closure_expansion_quality_candidate,
    is_bullish_c2_reversal_to_expansion,
    is_bullish_c3_closure,
    has_bullish_c4_continuation_candidate,
    has_bullish_c3_support,
    is_bearish_c2_closure,
    is_bearish_c3_expansion_confirmation,
    is_bullish_c2_closure,
    is_bullish_c3_expansion_confirmation,
    is_valid_bearish_c2_sequence,
    is_valid_bearish_c2_sequence_expansion_quality,
    is_valid_bullish_c2_sequence,
    is_valid_bullish_c2_sequence_expansion_quality,
    validate_case_b_inputs,
    validate_continuation_inputs,
    validate_sequence_inputs,
)


class SequencePrimitiveTests(unittest.TestCase):
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

    def test_equilibrium_of_c2_range(self) -> None:
        c2 = self.make_candle(timestamp_hour=11, open=103, high=107, low=95, close=101)
        self.assertEqual(equilibrium(c2), 101.0)

    def test_close_inside_range_uses_strict_boundaries(self) -> None:
        reference = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        inside = self.make_candle(timestamp_hour=11, open=96, high=106, low=94, close=105)
        on_low = self.make_candle(timestamp_hour=11, open=96, high=104, low=94, close=98)
        on_high = self.make_candle(timestamp_hour=11, open=96, high=111, low=94, close=110)

        self.assertTrue(closes_inside_range(reference, inside))
        self.assertFalse(closes_inside_range(reference, on_low))
        self.assertFalse(closes_inside_range(reference, on_high))

    def test_valid_bullish_c2_sequence(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)

        self.assertTrue(is_bullish_c2_closure(c1, c2))
        self.assertTrue(has_bullish_c3_support(c2, c3))
        self.assertTrue(is_bullish_c3_expansion_confirmation(c2, c3))
        self.assertTrue(is_valid_bullish_c2_sequence(c1, c2, c3))

    def test_valid_bullish_c2_sequence_expansion_quality(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=104, close=111)

        self.assertTrue(is_valid_bullish_c2_sequence_expansion_quality(c1, c2, c3))

    def test_bullish_c2_sequence_expansion_quality_requires_bullish_body(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=113, low=104, close=111)

        self.assertFalse(is_valid_bullish_c2_sequence_expansion_quality(c1, c2, c3))

    def test_bullish_c2_sequence_expansion_quality_rejects_large_lower_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)

        self.assertFalse(is_valid_bullish_c2_sequence_expansion_quality(c1, c2, c3))

    def test_valid_bullish_c4_continuation_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)
        c4 = self.make_candle(timestamp_hour=13, open=111, high=117, low=107, close=115)

        self.assertTrue(has_bullish_c4_continuation_candidate(c1, c2, c3, c4))

    def test_bullish_c4_candidate_requires_valid_bullish_predecessor(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=100.0, close=111)
        c4 = self.make_candle(timestamp_hour=13, open=111, high=117, low=107, close=115)

        self.assertFalse(has_bullish_c4_continuation_candidate(c1, c2, c3, c4))

    def test_bullish_c4_candidate_requires_low_above_eq_of_c3(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)
        c4 = self.make_candle(timestamp_hour=13, open=111, high=117, low=106.75, close=115)

        self.assertFalse(has_bullish_c4_continuation_candidate(c1, c2, c3, c4))

    def test_valid_bearish_c4_continuation_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=114.5, low=99, close=101)
        c4 = self.make_candle(timestamp_hour=13, open=101, high=105, low=96, close=97)

        self.assertTrue(has_bearish_c4_continuation_candidate(c1, c2, c3, c4))

    def test_valid_bearish_c2_sequence_expansion_quality(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=113, low=99, close=101)

        self.assertTrue(is_valid_bearish_c2_sequence_expansion_quality(c1, c2, c3))

    def test_bearish_c2_sequence_expansion_quality_requires_bearish_body(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=100, high=101, low=99, close=101)

        self.assertFalse(is_valid_bearish_c2_sequence_expansion_quality(c1, c2, c3))

    def test_bearish_c2_sequence_expansion_quality_rejects_large_upper_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=103, high=114.5, low=99, close=101)

        self.assertFalse(is_valid_bearish_c2_sequence_expansion_quality(c1, c2, c3))

    def test_bearish_c4_candidate_requires_valid_bearish_predecessor(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=115, low=99, close=101)
        c4 = self.make_candle(timestamp_hour=13, open=101, high=105, low=96, close=97)

        self.assertFalse(has_bearish_c4_continuation_candidate(c1, c2, c3, c4))

    def test_bearish_c4_candidate_requires_high_below_eq_of_c3(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=114.5, low=99, close=101)
        c4 = self.make_candle(timestamp_hour=13, open=101, high=106.75, low=96, close=97)

        self.assertFalse(has_bearish_c4_continuation_candidate(c1, c2, c3, c4))

    def test_bullish_c2_closure_requires_sweep_below_c1_low(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=99, high=106, low=98, close=105)

        self.assertFalse(is_bullish_c2_closure(c1, c2))

    def test_bullish_c2_closure_rejects_close_on_boundary(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=104, low=94, close=98)

        self.assertFalse(is_bullish_c2_closure(c1, c2))

    def test_bullish_c3_support_requires_low_above_eq_of_c2(self) -> None:
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=100.0, close=111)

        self.assertFalse(has_bullish_c3_support(c2, c3))

    def test_bullish_c3_expansion_requires_close_above_high_of_c2(self) -> None:
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=106.0)

        self.assertFalse(is_bullish_c3_expansion_confirmation(c2, c3))

    def test_valid_bullish_c3_closure(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=101.5)

        self.assertTrue(is_bullish_c3_closure(c1, c2, c3))

    def test_bullish_c3_closure_requires_no_type_a_c2_closure(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=104, high=105, low=98, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=102, high=108, low=100.5, close=106)

        self.assertFalse(is_bullish_c3_closure(c1, c2, c3))

    def test_bullish_c3_closure_requires_c2_to_sweep_below_c1_low(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=105, high=106, low=100, close=101)
        c3 = self.make_candle(timestamp_hour=12, open=102, high=108, low=101, close=106)

        self.assertFalse(is_bullish_c3_closure(c1, c2, c3))

    def test_bullish_c3_closure_requires_c3_to_hold_above_c2_low(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=92, close=101.5)

        self.assertFalse(is_bullish_c3_closure(c1, c2, c3))

    def test_bullish_c3_closure_requires_strict_close_over_c2_body(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=100)

        self.assertFalse(is_bullish_c3_closure(c1, c2, c3))

    def test_bullish_c3_closure_allows_bullish_c2_when_sweep_and_no_type_a_close_hold(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=93, high=96, low=92, close=95)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=97)

        self.assertTrue(is_bullish_c3_closure(c1, c2, c3))

    def test_valid_bullish_c4_after_c3_closure_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=101.5)
        c4 = self.make_candle(timestamp_hour=13, open=102, high=112, low=101, close=110)

        self.assertTrue(has_bullish_c4_after_c3_closure_candidate(c1, c2, c3, c4))

    def test_valid_bullish_c4_after_c3_closure_expansion_quality_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=101.5)
        c4 = self.make_candle(timestamp_hour=13, open=102, high=112, low=101, close=110)

        self.assertTrue(
            has_bullish_c4_after_c3_closure_expansion_quality_candidate(c1, c2, c3, c4)
        )

    def test_bullish_c4_after_c3_closure_candidate_requires_low_above_eq_of_c3(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=101.5)
        c4 = self.make_candle(timestamp_hour=13, open=102, high=112, low=100.5, close=110)

        self.assertFalse(has_bullish_c4_after_c3_closure_candidate(c1, c2, c3, c4))

    def test_bullish_c4_after_c3_closure_expansion_quality_requires_bullish_body(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=101.5)
        c4 = self.make_candle(timestamp_hour=13, open=110, high=112, low=101, close=102)

        self.assertFalse(
            has_bullish_c4_after_c3_closure_expansion_quality_candidate(c1, c2, c3, c4)
        )

    def test_bullish_c4_after_c3_closure_expansion_quality_rejects_large_lower_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=101, low=92, close=94)
        c3 = self.make_candle(timestamp_hour=12, open=95, high=108, low=93, close=101.5)
        c4 = self.make_candle(timestamp_hour=13, open=110, high=112, low=95, close=111)

        self.assertFalse(
            has_bullish_c4_after_c3_closure_expansion_quality_candidate(c1, c2, c3, c4)
        )

    def test_valid_bullish_c2_reversal_to_expansion(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=98, close=114)

        self.assertTrue(is_bullish_c2_reversal_to_expansion(c1, c2))

    def test_bullish_c2_reversal_to_expansion_requires_strict_sweep(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=100, close=114)

        self.assertFalse(is_bullish_c2_reversal_to_expansion(c1, c2))

    def test_bullish_c2_reversal_to_expansion_requires_reclaim_of_c1_low(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=95, high=103, low=94, close=99)

        self.assertFalse(is_bullish_c2_reversal_to_expansion(c1, c2))

    def test_bullish_c2_reversal_to_expansion_rejects_large_lower_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=90, close=114)

        self.assertFalse(is_bullish_c2_reversal_to_expansion(c1, c2))

    def test_bullish_c2_reversal_to_expansion_rejects_doji_like_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=104, high=110, low=98, close=104)

        self.assertFalse(is_bullish_c2_reversal_to_expansion(c1, c2))

    def test_valid_bearish_c2_sequence(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=114.5, low=99, close=101)

        self.assertTrue(is_bearish_c2_closure(c1, c2))
        self.assertTrue(has_bearish_c3_support(c2, c3))
        self.assertTrue(is_bearish_c3_expansion_confirmation(c2, c3))
        self.assertTrue(is_valid_bearish_c2_sequence(c1, c2, c3))

    def test_bearish_c2_closure_requires_sweep_above_c1_high(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=117, high=118, low=109, close=112)

        self.assertFalse(is_bearish_c2_closure(c1, c2))

    def test_bearish_c2_closure_rejects_close_on_boundary(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=118, low=100, close=103)
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=118)

        self.assertFalse(is_bearish_c2_closure(c1, c2))

    def test_bearish_c3_support_requires_high_below_eq_of_c2(self) -> None:
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=115, low=99, close=101)

        self.assertFalse(has_bearish_c3_support(c2, c3))

    def test_bearish_c3_expansion_requires_close_below_low_of_c2(self) -> None:
        c2 = self.make_candle(timestamp_hour=11, open=119, high=121, low=109, close=112)
        c3 = self.make_candle(timestamp_hour=12, open=112, high=114.5, low=99, close=109.0)

        self.assertFalse(is_bearish_c3_expansion_confirmation(c2, c3))

    def test_valid_bearish_c3_closure(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=107)

        self.assertTrue(is_bearish_c3_closure(c1, c2, c3))

    def test_bearish_c3_closure_requires_no_type_a_c2_closure(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=106, high=114, low=104, close=109)
        c3 = self.make_candle(timestamp_hour=12, open=108, high=109.5, low=100, close=105)

        self.assertFalse(is_bearish_c3_closure(c1, c2, c3))

    def test_bearish_c3_closure_requires_c2_to_sweep_above_c1_high(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=104, high=110, low=103, close=109)
        c3 = self.make_candle(timestamp_hour=12, open=108, high=109.5, low=100, close=103)

        self.assertFalse(is_bearish_c3_closure(c1, c2, c3))

    def test_bearish_c3_closure_requires_c3_to_hold_below_c2_high(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=116, low=104, close=107)

        self.assertFalse(is_bearish_c3_closure(c1, c2, c3))

    def test_bearish_c3_closure_requires_strict_close_below_c2_body(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=108)

        self.assertFalse(is_bearish_c3_closure(c1, c2, c3))

    def test_bearish_c3_closure_allows_bearish_c2_when_sweep_and_no_type_a_close_hold(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=115, high=116, low=112, close=113)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=111)

        self.assertTrue(is_bearish_c3_closure(c1, c2, c3))

    def test_valid_bearish_c4_after_c3_closure_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=107)
        c4 = self.make_candle(timestamp_hour=13, open=106, high=108.5, low=99, close=100)

        self.assertTrue(has_bearish_c4_after_c3_closure_candidate(c1, c2, c3, c4))

    def test_valid_bearish_c4_after_c3_closure_expansion_quality_candidate(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=107)
        c4 = self.make_candle(timestamp_hour=13, open=106, high=108.0, low=99, close=100)

        self.assertTrue(
            has_bearish_c4_after_c3_closure_expansion_quality_candidate(c1, c2, c3, c4)
        )

    def test_bearish_c4_after_c3_closure_candidate_requires_high_below_eq_of_c3(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=107)
        c4 = self.make_candle(timestamp_hour=13, open=106, high=109.5, low=99, close=100)

        self.assertFalse(has_bearish_c4_after_c3_closure_candidate(c1, c2, c3, c4))

    def test_bearish_c4_after_c3_closure_expansion_quality_requires_bearish_body(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=107)
        c4 = self.make_candle(timestamp_hour=13, open=100, high=108.5, low=99, close=106)

        self.assertFalse(
            has_bearish_c4_after_c3_closure_expansion_quality_candidate(c1, c2, c3, c4)
        )

    def test_bearish_c4_after_c3_closure_expansion_quality_rejects_large_upper_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=108, high=116, low=107, close=114)
        c3 = self.make_candle(timestamp_hour=12, open=113, high=115, low=104, close=107)
        c4 = self.make_candle(timestamp_hour=13, open=101, high=114, low=99, close=100)

        self.assertFalse(
            has_bearish_c4_after_c3_closure_expansion_quality_candidate(c1, c2, c3, c4)
        )

    def test_valid_bearish_c2_reversal_to_expansion(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=109, high=112, low=96, close=97)

        self.assertTrue(is_bearish_c2_reversal_to_expansion(c1, c2))

    def test_bearish_c2_reversal_to_expansion_requires_strict_sweep(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=109, high=110, low=96, close=97)

        self.assertFalse(is_bearish_c2_reversal_to_expansion(c1, c2))

    def test_bearish_c2_reversal_to_expansion_requires_reclaim_of_c1_high(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=112, high=113, low=104, close=111)

        self.assertFalse(is_bearish_c2_reversal_to_expansion(c1, c2))

    def test_bearish_c2_reversal_to_expansion_rejects_large_upper_wick(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=109, high=120, low=96, close=97)

        self.assertFalse(is_bearish_c2_reversal_to_expansion(c1, c2))

    def test_bearish_c2_reversal_to_expansion_rejects_doji_like_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=104, high=112, low=100, close=104)

        self.assertFalse(is_bearish_c2_reversal_to_expansion(c1, c2))

    def test_mixed_symbol_rejection(self) -> None:
        c1 = self.make_candle(symbol="XAUUSD", timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(symbol="XAUUSD", timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(symbol="NQ", timestamp_hour=12, open=105, high=112, low=101.5, close=111)

        with self.assertRaisesRegex(ValueError, "same symbol"):
            validate_sequence_inputs(c1, c2, c3)

    def test_mixed_timeframe_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, timeframe="1H", open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, timeframe="1H", open=97, high=106, low=94, close=105)
        c3 = Candle(
            symbol="XAUUSD",
            timestamp=utc_datetime(2026, 3, 17, 12, 0),
            timeframe="30m",
            open=105,
            high=112,
            low=101.5,
            close=111,
        )

        with self.assertRaisesRegex(ValueError, "same timeframe"):
            validate_sequence_inputs(c1, c2, c3)

    def test_non_consecutive_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=13, open=105, high=112, low=101.5, close=111)

        with self.assertRaisesRegex(ValueError, "must be consecutive"):
            validate_sequence_inputs(c1, c2, c3)

    def test_unclosed_c3_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(
            timestamp_hour=12,
            open=105,
            high=112,
            low=101.5,
            close=111,
            is_closed=False,
        )

        with self.assertRaisesRegex(ValueError, "must be closed"):
            validate_sequence_inputs(c1, c2, c3)

    def test_wrong_timestamp_order_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=12, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=10, open=105, high=112, low=101.5, close=111)

        with self.assertRaisesRegex(ValueError, "strict timestamp order"):
            validate_sequence_inputs(c1, c2, c3)

    def test_malformed_candle_object_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = {"not": "a candle"}
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)

        with self.assertRaisesRegex(TypeError, "must be a Candle"):
            validate_sequence_inputs(c1, c2, c3)

    def test_case_b_rejects_non_consecutive_inputs(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=12, open=100, high=116, low=98, close=114)

        with self.assertRaisesRegex(ValueError, "must be consecutive"):
            validate_case_b_inputs(c1, c2)

    def test_case_b_rejects_unclosed_inputs(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(
            timestamp_hour=11,
            open=100,
            high=116,
            low=98,
            close=114,
            is_closed=False,
        )

        with self.assertRaisesRegex(ValueError, "must be closed"):
            validate_case_b_inputs(c1, c2)

    def test_case_b_rejects_zero_range_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=100, low=100, close=100)

        with self.assertRaisesRegex(ValueError, "positive-range"):
            is_bullish_c2_reversal_to_expansion(c1, c2)

    def test_case_b_rejects_invalid_wick_fraction(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=116, low=98, close=114)

        with self.assertRaisesRegex(ValueError, "between 0 and 1 inclusive"):
            is_bullish_c2_reversal_to_expansion(c1, c2, max_lower_wick_fraction=1.1)

    def test_c3_closure_rejects_zero_range_c2(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=110, high=112, low=100, close=102)
        c2 = self.make_candle(timestamp_hour=11, open=100, high=100, low=100, close=100)
        c3 = self.make_candle(timestamp_hour=12, open=99, high=108, low=93, close=101.5)

        with self.assertRaisesRegex(ValueError, "c2 requires a positive-range candle"):
            is_bullish_c3_closure(c1, c2, c3)

    def test_c4_non_consecutive_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)
        c4 = self.make_candle(timestamp_hour=14, open=111, high=117, low=107, close=115)

        with self.assertRaisesRegex(ValueError, "must be consecutive"):
            validate_continuation_inputs(c1, c2, c3, c4)

    def test_unclosed_c4_rejection(self) -> None:
        c1 = self.make_candle(timestamp_hour=10, open=100, high=110, low=98, close=108)
        c2 = self.make_candle(timestamp_hour=11, open=97, high=106, low=94, close=105)
        c3 = self.make_candle(timestamp_hour=12, open=105, high=112, low=101.5, close=111)
        c4 = self.make_candle(
            timestamp_hour=13,
            open=111,
            high=117,
            low=107,
            close=115,
            is_closed=False,
        )

        with self.assertRaisesRegex(ValueError, "must be closed"):
            validate_continuation_inputs(c1, c2, c3, c4)


if __name__ == "__main__":
    unittest.main()
