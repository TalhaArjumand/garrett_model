from __future__ import annotations

import unittest
from pathlib import Path

from gxt.candles import Candle, utc_datetime
from gxt.real_ohlc import (
    build_real_sample_report,
    count_c3_closure_rare_cases,
    count_c3_closure_c4_candidates,
    count_c3_closure_c4_expansion_quality_candidates,
    count_c3_closures,
    count_case_b_candidates,
    count_c4_candidates,
    count_fvg_candidates,
    count_erl_candidates,
    count_fvgs,
    count_valid_sequences,
    iter_pairs,
    iter_quads,
    load_candles_from_csv,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = PROJECT_ROOT / "data" / "real_samples" / "xauusd_4h_template.csv"
REAL_SAMPLE_PATH = PROJECT_ROOT / "data" / "real_samples" / "xauusd_4h.csv"


class RealOhlcVerificationTests(unittest.TestCase):
    def test_template_csv_exists(self) -> None:
        self.assertTrue(TEMPLATE_PATH.exists())
        header = TEMPLATE_PATH.read_text(encoding="utf-8").strip()
        self.assertEqual(header, "symbol,timestamp,timeframe,open,high,low,close")

    @unittest.skipUnless(REAL_SAMPLE_PATH.exists(), "drop data/real_samples/xauusd_4h.csv to activate")
    def test_real_xauusd_4h_sample_loads_and_reports(self) -> None:
        candles = load_candles_from_csv(REAL_SAMPLE_PATH)
        self.assertGreaterEqual(len(candles), 20)
        self.assertLessEqual(len(candles), 100)

        report = build_real_sample_report(candles)
        self.assertEqual(report.symbol, "XAUUSD")
        self.assertEqual(report.timeframe, "4H")
        self.assertEqual(report.candle_count, len(candles))
        self.assertGreaterEqual(report.bullish_sequence_count, 0)
        self.assertGreaterEqual(report.bearish_sequence_count, 0)
        self.assertGreaterEqual(report.bullish_c4_candidate_count, 0)
        self.assertGreaterEqual(report.bearish_c4_candidate_count, 0)
        self.assertGreaterEqual(report.bullish_case_b_candidate_count, 0)
        self.assertGreaterEqual(report.bearish_case_b_candidate_count, 0)
        self.assertGreaterEqual(report.bullish_c3_closure_count, 0)
        self.assertGreaterEqual(report.bearish_c3_closure_count, 0)
        self.assertGreaterEqual(report.bullish_c3_closure_rare_case_count, 0)
        self.assertGreaterEqual(report.bearish_c3_closure_rare_case_count, 0)
        self.assertGreaterEqual(report.bullish_c3_closure_c4_candidate_count, 0)
        self.assertGreaterEqual(report.bearish_c3_closure_c4_candidate_count, 0)
        self.assertGreaterEqual(report.bullish_c3_closure_c4_expansion_quality_count, 0)
        self.assertGreaterEqual(report.bearish_c3_closure_c4_expansion_quality_count, 0)
        self.assertGreaterEqual(report.bullish_fvg_count, 0)
        self.assertGreaterEqual(report.bearish_fvg_count, 0)
        self.assertGreaterEqual(report.fvg_candidate_count, 0)
        self.assertGreaterEqual(report.fvg_resting_candidate_count, 0)
        self.assertGreaterEqual(report.fvg_reached_candidate_count, 0)
        self.assertGreaterEqual(report.bullish_resting_fvg_count, 0)
        self.assertGreaterEqual(report.bearish_resting_fvg_count, 0)
        self.assertGreaterEqual(report.bullish_reached_fvg_count, 0)
        self.assertGreaterEqual(report.bearish_reached_fvg_count, 0)
        self.assertGreaterEqual(report.erl_candidate_count, 0)
        self.assertGreaterEqual(report.erl_resting_candidate_count, 0)
        self.assertGreaterEqual(report.erl_old_high_count, 0)
        self.assertGreaterEqual(report.erl_old_low_count, 0)
        self.assertGreaterEqual(report.erl_equal_highs_count, 0)
        self.assertGreaterEqual(report.erl_equal_lows_count, 0)
        self.assertGreaterEqual(report.erl_resting_old_high_count, 0)
        self.assertGreaterEqual(report.erl_resting_old_low_count, 0)
        self.assertGreaterEqual(report.erl_resting_equal_highs_count, 0)
        self.assertGreaterEqual(report.erl_resting_equal_lows_count, 0)

    def test_count_valid_sequences_skips_non_consecutive_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 105, 95, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 102, 106, 96, 103),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 103, 107, 97, 104),
            Candle("XAUUSD", utc_datetime(2026, 3, 17, 0), "4H", 104, 108, 98, 105),
        ]

        bullish, bearish = count_valid_sequences(candles)
        self.assertEqual((bullish, bearish), (0, 0))

    def test_iter_quads_yields_overlapping_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 105, 95, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 102, 106, 96, 103),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 103, 107, 97, 104),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 104, 108, 98, 105),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 105, 109, 99, 106),
        ]

        quads = list(iter_quads(candles))
        self.assertEqual(len(quads), 2)
        self.assertEqual(quads[0][0].timestamp, candles[0].timestamp)
        self.assertEqual(quads[0][3].timestamp, candles[3].timestamp)
        self.assertEqual(quads[1][0].timestamp, candles[1].timestamp)
        self.assertEqual(quads[1][3].timestamp, candles[4].timestamp)

    def test_iter_pairs_yields_overlapping_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 105, 95, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 102, 106, 96, 103),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 103, 107, 97, 104),
        ]

        pairs = list(iter_pairs(candles))
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0][0].timestamp, candles[0].timestamp)
        self.assertEqual(pairs[0][1].timestamp, candles[1].timestamp)
        self.assertEqual(pairs[1][0].timestamp, candles[1].timestamp)
        self.assertEqual(pairs[1][1].timestamp, candles[2].timestamp)

    def test_count_c4_candidates_skips_non_consecutive_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 105, 95, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 102, 106, 96, 103),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 103, 107, 97, 104),
            Candle("XAUUSD", utc_datetime(2026, 3, 17, 0), "4H", 104, 108, 98, 105),
        ]

        bullish, bearish = count_c4_candidates(candles)
        self.assertEqual((bullish, bearish), (0, 0))

    def test_count_case_b_candidates_counts_bullish_and_bearish_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 110, 112, 100, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 100, 116, 98, 114),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 100, 110, 98, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 109, 112, 96, 97),
        ]

        bullish, bearish = count_case_b_candidates(candles)
        self.assertEqual((bullish, bearish), (1, 1))

    def test_count_case_b_candidates_skips_non_consecutive_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 110, 112, 100, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 100, 116, 98, 114),
            Candle("XAUUSD", utc_datetime(2026, 3, 17, 0), "4H", 100, 110, 98, 108),
        ]

        bullish, bearish = count_case_b_candidates(candles)
        self.assertEqual((bullish, bearish), (1, 0))

    def test_count_c3_closures_counts_bullish_and_bearish_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 110, 112, 100, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 100, 101, 92, 94),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 95, 108, 93, 101.5),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 100, 110, 98, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 108, 116, 107, 114),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 20), "4H", 113, 115, 104, 107),
        ]

        bullish, bearish = count_c3_closures(candles)
        self.assertEqual((bullish, bearish), (1, 1))

    def test_count_c3_closure_c4_candidates_counts_bullish_window(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 110, 112, 100, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 100, 101, 92, 94),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 95, 108, 93, 101.5),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 102, 112, 101, 110),
        ]

        bullish, bearish = count_c3_closure_c4_candidates(candles)
        self.assertEqual((bullish, bearish), (1, 0))

    def test_count_c3_closure_c4_candidates_counts_bearish_window(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 110, 98, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 108, 116, 107, 114),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 113, 115, 104, 107),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 106, 108.5, 99, 100),
        ]

        bullish, bearish = count_c3_closure_c4_candidates(candles)
        self.assertEqual((bullish, bearish), (0, 1))

    def test_count_c3_closure_c4_expansion_quality_candidates_counts_bullish_and_bearish_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 110, 112, 100, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 100, 116, 92, 114),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 114, 120, 105, 118),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 118, 125, 117, 124),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 100, 110, 98, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 20), "4H", 108, 116, 94, 96),
            Candle("XAUUSD", utc_datetime(2026, 3, 15, 0), "4H", 96, 101, 90, 92),
            Candle("XAUUSD", utc_datetime(2026, 3, 15, 4), "4H", 92, 94, 85, 86),
        ]

        bullish, bearish = count_c3_closure_c4_expansion_quality_candidates(candles)
        self.assertEqual((bullish, bearish), (1, 1))

    def test_count_c3_closure_rare_cases_counts_bullish_and_bearish_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 110, 112, 100, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 100, 116, 92, 114),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 114, 120, 105, 118),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 100, 110, 98, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 108, 116, 94, 96),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 20), "4H", 96, 101, 90, 92),
        ]

        bullish, bearish = count_c3_closure_rare_cases(candles)
        self.assertEqual((bullish, bearish), (1, 1))

    def test_count_fvgs_counts_bullish_and_bearish_baseline_gaps(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 110, 95, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 108, 120, 107, 119),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 118, 125, 112, 123),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 123, 124, 109, 111),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 111, 111.5, 95, 97),
        ]

        bullish, bearish = count_fvgs(candles)
        self.assertEqual((bullish, bearish), (1, 1))

    def test_count_fvgs_skips_non_consecutive_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 110, 95, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 108, 120, 107, 119),
            Candle("XAUUSD", utc_datetime(2026, 3, 17, 0), "4H", 118, 125, 112, 123),
        ]

        bullish, bearish = count_fvgs(candles)
        self.assertEqual((bullish, bearish), (0, 0))

    def test_count_fvg_candidates_tracks_resting_and_reached_states(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 110, 95, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 108, 120, 107, 119),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 118, 125, 112, 123),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 123, 124, 111, 112),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 112, 113, 100, 101),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 20), "4H", 101, 102, 94, 95),
            Candle("XAUUSD", utc_datetime(2026, 3, 15, 0), "4H", 95, 100, 90, 91),
        ]

        counts = count_fvg_candidates(candles)
        self.assertEqual(counts["fvg_candidate_count"], 2)
        self.assertEqual(counts["fvg_resting_candidate_count"], 1)
        self.assertEqual(counts["fvg_reached_candidate_count"], 1)
        self.assertEqual(counts["bullish_resting_fvg_count"], 0)
        self.assertEqual(counts["bearish_resting_fvg_count"], 1)
        self.assertEqual(counts["bullish_reached_fvg_count"], 1)
        self.assertEqual(counts["bearish_reached_fvg_count"], 0)

    def test_count_erl_candidates_counts_old_and_equal_structures(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 110, 95, 108),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 108, 120.0, 101, 113),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 109, 114, 104, 112),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 12), "4H", 112, 119.6, 105, 111),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 16), "4H", 111, 113, 103, 104),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 20), "4H", 104, 112, 100.0, 105),
            Candle("XAUUSD", utc_datetime(2026, 3, 15, 0), "4H", 105, 116, 104, 112),
            Candle("XAUUSD", utc_datetime(2026, 3, 15, 4), "4H", 112, 119, 100.3, 111),
            Candle("XAUUSD", utc_datetime(2026, 3, 15, 8), "4H", 111, 120, 104, 115),
        ]

        counts = count_erl_candidates(candles, equal_tolerance=0.5)
        self.assertEqual(counts["erl_candidate_count"], 6)
        self.assertEqual(counts["erl_resting_candidate_count"], 5)
        self.assertEqual(counts["erl_old_high_count"], 2)
        self.assertEqual(counts["erl_old_low_count"], 2)
        self.assertEqual(counts["erl_equal_highs_count"], 1)
        self.assertEqual(counts["erl_equal_lows_count"], 1)
        self.assertEqual(counts["erl_resting_old_high_count"], 1)
        self.assertEqual(counts["erl_resting_old_low_count"], 2)
        self.assertEqual(counts["erl_resting_equal_highs_count"], 1)
        self.assertEqual(counts["erl_resting_equal_lows_count"], 1)


if __name__ == "__main__":
    unittest.main()
