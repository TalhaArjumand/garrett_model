from __future__ import annotations

import unittest
from datetime import timedelta

from gxt.candles import Candle, utc_datetime
from gxt.key_level_integration import (
    count_external_to_internal_type_a_expansion_quality_sequences,
    count_external_to_internal_type_a_sequences,
    detect_external_to_internal_type_a_candidates,
    detect_external_to_internal_type_a_expansion_quality_candidates,
    count_internal_to_external_type_a_expansion_quality_sequences,
    count_internal_to_external_type_a_sequences,
    count_internal_to_external_type_b_sequences,
    count_internal_to_external_type_c_sequences,
    count_internal_to_external_type_c_rare_case_sequences,
    count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences,
    detect_internal_to_external_type_a_candidates,
    detect_internal_to_external_type_a_expansion_quality_candidates,
    detect_internal_to_external_type_b_candidates,
    detect_internal_to_external_type_c_candidates,
    detect_internal_to_external_type_c_rare_case_candidates,
    detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates,
)
from gxt.sequence_primitives import is_bullish_c3_closure
from gxt.swing_research import (
    has_bullish_rare_c3_closure_expansion_quality_candidate,
    is_bearish_rare_c3_closure_subtype,
    is_bullish_rare_c3_closure_subtype,
)


class KeyLevelIntegrationTests(unittest.TestCase):
    def make_candle(
        self,
        *,
        timestamp_hour: int,
        open: float,
        high: float,
        low: float,
        close: float,
        symbol: str = "XAUUSD",
        timeframe: str = "4H",
        is_closed: bool = True,
    ) -> Candle:
        return Candle(
            symbol=symbol,
            timestamp=utc_datetime(2026, 3, 14) + timedelta(hours=timestamp_hour),
            timeframe=timeframe,
            open=open,
            high=high,
            low=low,
            close=close,
            is_closed=is_closed,
        )

    def test_detect_internal_to_external_type_a_candidates_returns_bullish_pairings_and_dedupes_counts(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=110, high=112, low=107, close=108),
            self.make_candle(timestamp_hour=16, open=108, high=116, low=107, close=115),
            self.make_candle(timestamp_hour=20, open=115, high=122, low=114, close=121),
            self.make_candle(timestamp_hour=24, open=115, high=116, low=103, close=104),
            self.make_candle(timestamp_hour=28, open=104, high=115, low=101, close=110),
            self.make_candle(timestamp_hour=32, open=111, high=118, low=110.5, close=117),
        ]

        candidates = detect_internal_to_external_type_a_candidates(candles)

        self.assertEqual(len(candidates), 1)
        self.assertEqual({candidate.direction for candidate in candidates}, {"bullish"})
        self.assertEqual({candidate.key_level_touch for candidate in candidates}, {"c2"})
        self.assertEqual(
            count_internal_to_external_type_a_sequences(candles),
            (1, 0),
        )

    def test_detect_internal_to_external_type_a_expansion_quality_counts_unique_bullish_sequence(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=110, high=112, low=107, close=108),
            self.make_candle(timestamp_hour=16, open=108, high=116, low=107, close=115),
            self.make_candle(timestamp_hour=20, open=115, high=122, low=114, close=121),
            self.make_candle(timestamp_hour=24, open=115, high=116, low=103, close=104),
            self.make_candle(timestamp_hour=28, open=104, high=115, low=101, close=110),
            self.make_candle(timestamp_hour=32, open=111, high=118, low=110.5, close=117),
        ]

        strict_candidates = detect_internal_to_external_type_a_expansion_quality_candidates(candles)

        self.assertEqual(len(strict_candidates), 1)
        self.assertEqual(
            count_internal_to_external_type_a_expansion_quality_sequences(candles),
            (1, 0),
        )

    def test_detect_internal_to_external_type_a_candidates_supports_bearish_touch_through_c2_only(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=202, high=205, low=195, close=198),
            self.make_candle(timestamp_hour=4, open=198, high=200, low=190, close=192),
            self.make_candle(timestamp_hour=8, open=188, high=188, low=180, close=182),
            self.make_candle(timestamp_hour=12, open=186, high=187, low=180, close=182),
            self.make_candle(timestamp_hour=16, open=181, high=189, low=176, close=183),
            self.make_candle(timestamp_hour=20, open=182, high=182, low=170, close=172),
        ]

        candidates = detect_internal_to_external_type_a_candidates(candles)

        self.assertEqual(len(candidates), 2)
        self.assertEqual({candidate.direction for candidate in candidates}, {"bearish"})
        self.assertEqual({candidate.key_level_touch for candidate in candidates}, {"c2"})
        self.assertEqual(count_internal_to_external_type_a_sequences(candles), (0, 1))
        self.assertEqual(
            count_internal_to_external_type_a_expansion_quality_sequences(candles),
            (0, 1),
        )

    def test_detect_internal_to_external_type_a_candidates_allows_gap_confirmed_on_c1_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=120, high=125, low=115, close=118),
            self.make_candle(timestamp_hour=4, open=118, high=119, low=100, close=102),
            self.make_candle(timestamp_hour=8, open=103, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=12, open=108, high=112, low=94, close=104),
            self.make_candle(timestamp_hour=16, open=102, high=102, low=85, close=90),
        ]

        candidates = detect_internal_to_external_type_a_candidates(candles)
        strict_candidates = detect_internal_to_external_type_a_expansion_quality_candidates(
            candles
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bearish")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(candidates[0].irl_confirmed_at, candles[2].timestamp)
        self.assertEqual(len(strict_candidates), 1)
        self.assertEqual(count_internal_to_external_type_a_sequences(candles), (0, 1))
        self.assertEqual(
            count_internal_to_external_type_a_expansion_quality_sequences(candles),
            (0, 1),
        )

    def test_detect_internal_to_external_type_a_candidates_ignores_future_gap_confirmation(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=125, high=130, low=115, close=118),
            self.make_candle(timestamp_hour=4, open=116, high=124, low=112, close=117),
            self.make_candle(timestamp_hour=8, open=121, high=128, low=119, close=126),
            self.make_candle(timestamp_hour=12, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=16, open=108, high=115, low=107, close=114),
            self.make_candle(timestamp_hour=20, open=114, high=122, low=112, close=121),
        ]

        self.assertEqual(detect_internal_to_external_type_a_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_a_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_a_candidates_requires_gap_to_be_resting_before_sequence(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=4, open=108, high=115, low=107, close=114),
            self.make_candle(timestamp_hour=8, open=114, high=122, low=112, close=121),
            self.make_candle(timestamp_hour=12, open=121, high=123, low=111, close=120),
            self.make_candle(timestamp_hour=16, open=113, high=114, low=109, close=110),
            self.make_candle(timestamp_hour=20, open=110, high=113, low=108, close=111.5),
            self.make_candle(timestamp_hour=24, open=111.5, high=118, low=111, close=117),
        ]

        self.assertEqual(detect_internal_to_external_type_a_candidates(candles), [])
        self.assertEqual(
            count_internal_to_external_type_a_expansion_quality_sequences(candles),
            (0, 0),
        )

    def test_detect_internal_to_external_type_a_expansion_quality_rejects_large_c3_same_side_wick(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=4, open=108, high=115, low=107, close=114),
            self.make_candle(timestamp_hour=8, open=114, high=122, low=112, close=121),
            self.make_candle(timestamp_hour=12, open=125, high=130, low=115, close=118),
            self.make_candle(timestamp_hour=16, open=116, high=124, low=112, close=117),
            self.make_candle(timestamp_hour=20, open=127, high=129, low=118.5, close=128),
        ]

        base_candidates = detect_internal_to_external_type_a_candidates(candles)
        strict_candidates = detect_internal_to_external_type_a_expansion_quality_candidates(candles)

        self.assertEqual(len(base_candidates), 1)
        self.assertEqual(strict_candidates, [])
        self.assertEqual(count_internal_to_external_type_a_sequences(candles), (1, 0))
        self.assertEqual(
            count_internal_to_external_type_a_expansion_quality_sequences(candles),
            (0, 0),
        )

    def test_detect_internal_to_external_type_a_candidates_rejects_close_through_invalidation(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=108, high=112, low=97, close=99),
            self.make_candle(timestamp_hour=16, open=99, high=113, low=96, close=104),
            self.make_candle(timestamp_hour=20, open=104, high=118, low=103.5, close=117),
        ]

        self.assertEqual(detect_internal_to_external_type_a_candidates(candles), [])
        self.assertEqual(
            count_internal_to_external_type_a_expansion_quality_sequences(candles),
            (0, 0),
        )

    def test_detect_internal_to_external_type_a_candidates_rejects_mixed_symbol_series(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=110, low=95, close=108),
            self.make_candle(
                timestamp_hour=4,
                open=108,
                high=115,
                low=107,
                close=114,
                symbol="BTCUSD",
            ),
            self.make_candle(timestamp_hour=8, open=114, high=122, low=112, close=121),
        ]

        with self.assertRaises(ValueError):
            detect_internal_to_external_type_a_candidates(candles)

    def test_detect_external_to_internal_type_a_candidates_supports_preexisting_bullish_erl(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=110, high=112, low=105, close=108),
            self.make_candle(timestamp_hour=4, open=108, high=109, low=100, close=101),
            self.make_candle(timestamp_hour=8, open=101, high=115, low=101, close=114),
            self.make_candle(timestamp_hour=12, open=114, high=118, low=101, close=105),
            self.make_candle(timestamp_hour=16, open=105, high=116, low=99, close=108),
            self.make_candle(timestamp_hour=20, open=109, high=120, low=108.5, close=119),
        ]

        candidates = detect_external_to_internal_type_a_candidates(candles)
        strict_candidates = detect_external_to_internal_type_a_expansion_quality_candidates(
            candles
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].erl_kind, "old_low")
        self.assertEqual(candidates[0].erl_side, "sell_side")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertLess(candidates[0].erl_confirmed_at, candidates[0].sequence_c1_timestamp)
        self.assertEqual(len(strict_candidates), 1)
        self.assertEqual(count_external_to_internal_type_a_sequences(candles), (1, 0))
        self.assertEqual(
            count_external_to_internal_type_a_expansion_quality_sequences(candles),
            (1, 0),
        )

    def test_detect_external_to_internal_type_a_candidates_allows_erl_confirmed_on_c1_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=110, high=112, low=105, close=108),
            self.make_candle(timestamp_hour=4, open=108, high=109, low=100, close=101),
            self.make_candle(timestamp_hour=8, open=101, high=115, low=101, close=114),
            self.make_candle(timestamp_hour=12, open=114, high=116, low=99, close=108),
            self.make_candle(timestamp_hour=16, open=109, high=120, low=108.5, close=119),
        ]

        candidates = detect_external_to_internal_type_a_candidates(candles)
        strict_candidates = detect_external_to_internal_type_a_expansion_quality_candidates(
            candles
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(candidates[0].erl_confirmed_at, candles[2].timestamp)
        self.assertLess(candidates[0].erl_confirmed_at, candidates[0].sequence_c2_timestamp)
        self.assertEqual(len(strict_candidates), 1)
        self.assertEqual(count_external_to_internal_type_a_sequences(candles), (1, 0))
        self.assertEqual(
            count_external_to_internal_type_a_expansion_quality_sequences(candles),
            (1, 0),
        )

    def test_detect_external_to_internal_type_a_candidates_supports_preexisting_bearish_erl(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=105, low=95, close=100),
            self.make_candle(timestamp_hour=4, open=100, high=120, low=98, close=119),
            self.make_candle(timestamp_hour=8, open=113, high=115, low=100, close=102),
            self.make_candle(timestamp_hour=12, open=102, high=119, low=101, close=118),
            self.make_candle(timestamp_hour=16, open=118, high=121, low=105, close=110),
            self.make_candle(timestamp_hour=20, open=109, high=109.5, low=96, close=99),
        ]

        candidates = detect_external_to_internal_type_a_candidates(candles)
        strict_candidates = detect_external_to_internal_type_a_expansion_quality_candidates(
            candles
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bearish")
        self.assertEqual(candidates[0].erl_kind, "old_high")
        self.assertEqual(candidates[0].erl_side, "buy_side")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(len(strict_candidates), 1)
        self.assertEqual(count_external_to_internal_type_a_sequences(candles), (0, 1))
        self.assertEqual(
            count_external_to_internal_type_a_expansion_quality_sequences(candles),
            (0, 1),
        )

    def test_detect_external_to_internal_type_a_candidates_rejects_taken_erl_before_sequence(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=110, high=112, low=105, close=108),
            self.make_candle(timestamp_hour=4, open=108, high=109, low=100, close=101),
            self.make_candle(timestamp_hour=8, open=101, high=115, low=101, close=114),
            self.make_candle(timestamp_hour=12, open=114, high=116, low=99, close=104),
            self.make_candle(timestamp_hour=16, open=104, high=120, low=98, close=118),
            self.make_candle(timestamp_hour=20, open=118, high=122, low=97, close=105),
            self.make_candle(timestamp_hour=24, open=105, high=116, low=96, close=108),
            self.make_candle(timestamp_hour=28, open=109, high=120, low=108.5, close=119),
        ]

        self.assertEqual(detect_external_to_internal_type_a_candidates(candles), [])
        self.assertEqual(
            detect_external_to_internal_type_a_expansion_quality_candidates(candles),
            [],
        )
        self.assertEqual(count_external_to_internal_type_a_sequences(candles), (0, 0))
        self.assertEqual(
            count_external_to_internal_type_a_expansion_quality_sequences(candles),
            (0, 0),
        )

    def test_detect_internal_to_external_type_b_candidates_returns_bullish_pairings_and_dedupes_counts(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=107, low=103, close=104),
            self.make_candle(timestamp_hour=16, open=104, high=112, low=103, close=111),
            self.make_candle(timestamp_hour=20, open=111, high=118, low=108, close=117),
            self.make_candle(timestamp_hour=24, open=108, high=109, low=101, close=103),
            self.make_candle(timestamp_hour=28, open=103, high=113, low=100, close=112),
        ]

        candidates = detect_internal_to_external_type_b_candidates(candles)

        self.assertEqual(len(candidates), 1)
        self.assertEqual({candidate.direction for candidate in candidates}, {"bullish"})
        self.assertEqual({candidate.key_level_touch for candidate in candidates}, {"both"})
        self.assertEqual(count_internal_to_external_type_b_sequences(candles), (1, 0))

    def test_detect_internal_to_external_type_b_candidates_supports_bearish_touch_through_c2_only(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=202, high=205, low=195, close=198),
            self.make_candle(timestamp_hour=4, open=198, high=200, low=190, close=192),
            self.make_candle(timestamp_hour=8, open=188, high=188, low=180, close=182),
            self.make_candle(timestamp_hour=12, open=181, high=187, low=176, close=183),
            self.make_candle(timestamp_hour=16, open=189, high=190, low=175, close=178),
        ]

        candidates = detect_internal_to_external_type_b_candidates(candles)

        self.assertEqual(len(candidates), 2)
        self.assertEqual({candidate.direction for candidate in candidates}, {"bearish"})
        self.assertEqual({candidate.key_level_touch for candidate in candidates}, {"c2"})
        self.assertEqual(count_internal_to_external_type_b_sequences(candles), (0, 1))

    def test_detect_internal_to_external_type_b_candidates_requires_gap_to_be_resting_before_pair(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=109, high=111, low=101, close=110),
            self.make_candle(timestamp_hour=16, open=108, high=109, low=101, close=103),
            self.make_candle(timestamp_hour=20, open=103, high=113, low=100, close=112),
        ]

        self.assertEqual(detect_internal_to_external_type_b_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_b_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_b_candidates_rejects_close_through_invalidation(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=205, high=208, low=200, close=202),
            self.make_candle(timestamp_hour=4, open=202, high=204, low=194, close=196),
            self.make_candle(timestamp_hour=8, open=196, high=198, low=190, close=191),
            self.make_candle(timestamp_hour=12, open=191, high=206, low=189, close=205),
            self.make_candle(timestamp_hour=16, open=205, high=207, low=180, close=182),
        ]

        self.assertEqual(detect_internal_to_external_type_b_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_b_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_b_candidates_allows_gap_confirmed_on_c1_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=120, high=122, low=110, close=111),
            self.make_candle(timestamp_hour=4, open=111, high=112, low=100, close=101),
            self.make_candle(timestamp_hour=8, open=108, high=109, low=95, close=96),
            self.make_candle(timestamp_hour=12, open=109, high=109.5, low=90, close=91),
        ]

        candidates = detect_internal_to_external_type_b_candidates(candles)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bearish")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(candidates[0].irl_confirmed_at, candles[2].timestamp)
        self.assertEqual(count_internal_to_external_type_b_sequences(candles), (0, 1))

    def test_detect_internal_to_external_type_c_candidates_returns_bullish_pairings_and_dedupes_counts(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=107, low=101, close=103),
            self.make_candle(timestamp_hour=16, open=103, high=110, low=99, close=108),
            self.make_candle(timestamp_hour=20, open=108, high=115, low=102, close=114),
        ]

        candidates = detect_internal_to_external_type_c_candidates(candles)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].key_level_touch, "both")
        self.assertEqual(count_internal_to_external_type_c_sequences(candles), (1, 0))

    def test_detect_internal_to_external_type_c_candidates_allows_gap_confirmed_on_c1_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=120, high=125, low=115, close=118),
            self.make_candle(timestamp_hour=4, open=118, high=119, low=100, close=102),
            self.make_candle(timestamp_hour=8, open=103, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=12, open=108, high=112, low=94, close=111),
            self.make_candle(timestamp_hour=16, open=109, high=110, low=85, close=90),
        ]

        candidates = detect_internal_to_external_type_c_candidates(candles)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bearish")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(candidates[0].irl_confirmed_at, candles[2].timestamp)
        self.assertEqual(count_internal_to_external_type_c_sequences(candles), (0, 1))

    def test_detect_internal_to_external_type_c_candidates_ignores_fresh_gap_confirmed_on_c2_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=105, low=95, close=98),
            self.make_candle(timestamp_hour=4, open=78, high=90, low=75, close=88),
            self.make_candle(timestamp_hour=8, open=108, high=112, low=100, close=102),
            self.make_candle(timestamp_hour=12, open=102, high=115, low=95, close=113),
            self.make_candle(timestamp_hour=16, open=113, high=120, low=96, close=119),
        ]

        self.assertTrue(is_bullish_c3_closure(candles[2], candles[3], candles[4]))
        self.assertEqual(detect_internal_to_external_type_c_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_c_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_c_candidates_rejects_close_through_invalidation(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=107, low=101, close=103),
            self.make_candle(timestamp_hour=16, open=103, high=104, low=99, close=99.5),
            self.make_candle(timestamp_hour=20, open=100.5, high=110, low=100, close=104),
        ]

        self.assertTrue(is_bullish_c3_closure(candles[3], candles[4], candles[5]))
        self.assertEqual(detect_internal_to_external_type_c_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_c_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_c_rare_case_candidates_returns_bullish_pairings_and_dedupes_counts(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=107, low=101, close=103),
            self.make_candle(timestamp_hour=16, open=103, high=112, low=99, close=111),
            self.make_candle(timestamp_hour=20, open=111, high=118, low=106, close=117),
        ]

        candidates = detect_internal_to_external_type_c_rare_case_candidates(candles)

        self.assertTrue(is_bullish_rare_c3_closure_subtype(candles[3], candles[4], candles[5]))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].key_level_touch, "both")
        self.assertEqual(count_internal_to_external_type_c_sequences(candles), (1, 0))
        self.assertEqual(count_internal_to_external_type_c_rare_case_sequences(candles), (1, 0))

    def test_detect_internal_to_external_type_c_rare_case_candidates_allows_gap_confirmed_on_c1_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=112, low=99, close=111),
            self.make_candle(timestamp_hour=16, open=111, high=118, low=106, close=117),
        ]

        candidates = detect_internal_to_external_type_c_rare_case_candidates(candles)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(candidates[0].irl_confirmed_at, candles[2].timestamp)
        self.assertEqual(count_internal_to_external_type_c_rare_case_sequences(candles), (1, 0))

    def test_detect_internal_to_external_type_c_rare_case_candidates_ignores_fresh_gap_confirmed_on_c2_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=105, low=95, close=98),
            self.make_candle(timestamp_hour=4, open=78, high=90, low=75, close=88),
            self.make_candle(timestamp_hour=8, open=108, high=112, low=100, close=102),
            self.make_candle(timestamp_hour=12, open=102, high=114, low=95, close=113),
            self.make_candle(timestamp_hour=16, open=114, high=120, low=114, close=119),
        ]

        self.assertTrue(is_bullish_rare_c3_closure_subtype(candles[2], candles[3], candles[4]))
        self.assertEqual(detect_internal_to_external_type_c_rare_case_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_c_rare_case_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_c_rare_case_candidates_rejects_close_through_invalidation(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=4, open=108, high=115, low=107, close=114),
            self.make_candle(timestamp_hour=8, open=114, high=122, low=112, close=121),
            self.make_candle(timestamp_hour=12, open=106, high=112, low=104, close=111),
            self.make_candle(timestamp_hour=16, open=111, high=113, low=100, close=103),
            self.make_candle(timestamp_hour=20, open=103, high=105, low=90, close=92),
        ]

        self.assertTrue(is_bearish_rare_c3_closure_subtype(candles[3], candles[4], candles[5]))
        self.assertEqual(detect_internal_to_external_type_c_rare_case_candidates(candles), [])
        self.assertEqual(count_internal_to_external_type_c_rare_case_sequences(candles), (0, 0))

    def test_detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates_returns_bullish_pairings_and_dedupes_counts(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=107, low=101, close=103),
            self.make_candle(timestamp_hour=16, open=103, high=112, low=99, close=111),
            self.make_candle(timestamp_hour=20, open=111.5, high=118, low=110.5, close=117),
        ]

        candidates = detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates(
            candles
        )

        self.assertTrue(
            has_bullish_rare_c3_closure_expansion_quality_candidate(
                candles[3],
                candles[4],
                candles[5],
            )
        )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].key_level_touch, "both")
        self.assertEqual(count_internal_to_external_type_c_rare_case_sequences(candles), (1, 0))
        self.assertEqual(
            count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences(candles),
            (1, 0),
        )

    def test_detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates_allows_gap_confirmed_on_c1_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=112, low=99, close=111),
            self.make_candle(timestamp_hour=16, open=111.5, high=118, low=110.5, close=117),
        ]

        candidates = detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates(
            candles
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].direction, "bullish")
        self.assertEqual(candidates[0].key_level_touch, "c2")
        self.assertEqual(candidates[0].irl_confirmed_at, candles[2].timestamp)
        self.assertEqual(
            count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences(candles),
            (1, 0),
        )

    def test_detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates_ignores_fresh_gap_confirmed_on_c2_close(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=100, high=105, low=95, close=98),
            self.make_candle(timestamp_hour=4, open=78, high=90, low=75, close=88),
            self.make_candle(timestamp_hour=8, open=108, high=112, low=100, close=102),
            self.make_candle(timestamp_hour=12, open=102, high=114, low=95, close=113),
            self.make_candle(timestamp_hour=16, open=114, high=120, low=114, close=119),
        ]

        self.assertTrue(
            has_bullish_rare_c3_closure_expansion_quality_candidate(
                candles[2],
                candles[3],
                candles[4],
            )
        )
        self.assertEqual(
            detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates(candles),
            [],
        )
        self.assertEqual(
            count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences(candles),
            (0, 0),
        )

    def test_detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates_rejects_large_c3_same_side_wick(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=96, high=100, low=95, close=99),
            self.make_candle(timestamp_hour=4, open=99, high=105, low=98, close=104),
            self.make_candle(timestamp_hour=8, open=104, high=110, low=102, close=109),
            self.make_candle(timestamp_hour=12, open=106, high=107, low=101, close=103),
            self.make_candle(timestamp_hour=16, open=103, high=112, low=99, close=111),
            self.make_candle(timestamp_hour=20, open=111, high=118, low=106, close=117),
        ]

        base_candidates = detect_internal_to_external_type_c_rare_case_candidates(candles)
        strict_candidates = (
            detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates(candles)
        )

        self.assertEqual(len(base_candidates), 1)
        self.assertEqual(strict_candidates, [])
        self.assertEqual(count_internal_to_external_type_c_rare_case_sequences(candles), (1, 0))
        self.assertEqual(
            count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences(candles),
            (0, 0),
        )

    def test_detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates_rejects_close_through_invalidation(
        self,
    ) -> None:
        candles = [
            self.make_candle(timestamp_hour=0, open=120, high=122, low=110, close=111),
            self.make_candle(timestamp_hour=4, open=111, high=112, low=100, close=101),
            self.make_candle(timestamp_hour=8, open=108, high=109, low=95, close=96),
            self.make_candle(timestamp_hour=12, open=106, high=112, low=104, close=111),
            self.make_candle(timestamp_hour=16, open=111, high=113, low=100, close=103),
            self.make_candle(timestamp_hour=20, open=104, high=105, low=90, close=92),
        ]

        self.assertEqual(
            detect_internal_to_external_type_c_rare_case_c3_expansion_quality_candidates(candles),
            [],
        )
        self.assertEqual(
            count_internal_to_external_type_c_rare_case_c3_expansion_quality_sequences(candles),
            (0, 0),
        )


if __name__ == "__main__":
    unittest.main()
