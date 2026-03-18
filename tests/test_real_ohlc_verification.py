from __future__ import annotations

import unittest
from pathlib import Path

from gxt.candles import Candle, utc_datetime
from gxt.real_ohlc import (
    build_real_sample_report,
    count_c4_candidates,
    count_valid_sequences,
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

    def test_count_c4_candidates_skips_non_consecutive_windows(self) -> None:
        candles = [
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 0), "4H", 100, 105, 95, 102),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 4), "4H", 102, 106, 96, 103),
            Candle("XAUUSD", utc_datetime(2026, 3, 14, 8), "4H", 103, 107, 97, 104),
            Candle("XAUUSD", utc_datetime(2026, 3, 17, 0), "4H", 104, 108, 98, 105),
        ]

        bullish, bearish = count_c4_candidates(candles)
        self.assertEqual((bullish, bearish), (0, 0))


if __name__ == "__main__":
    unittest.main()
