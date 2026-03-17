from __future__ import annotations

import unittest
from pathlib import Path

from gxt.real_ohlc import build_real_sample_report, load_candles_from_csv


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


if __name__ == "__main__":
    unittest.main()
