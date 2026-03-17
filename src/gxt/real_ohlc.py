from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .candles import Candle
from .sequence_primitives import (
    is_valid_bearish_c2_sequence,
    is_valid_bullish_c2_sequence,
)


@dataclass(frozen=True)
class RealSampleReport:
    symbol: str
    timeframe: str
    candle_count: int
    gap_count: int
    bullish_sequence_count: int
    bearish_sequence_count: int


def load_candles_from_csv(csv_path: Path) -> list[Candle]:
    rows: list[Candle] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        expected = ["symbol", "timestamp", "timeframe", "open", "high", "low", "close"]
        if reader.fieldnames != expected:
            raise ValueError(
                f"CSV columns must be exactly {expected}, got {reader.fieldnames}"
            )

        for row in reader:
            rows.append(
                Candle.from_dict(
                    {
                        "symbol": row["symbol"],
                        "timestamp": row["timestamp"],
                        "timeframe": row["timeframe"],
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "is_closed": True,
                    }
                )
            )

    return rows


def find_timestamp_gaps(candles: list[Candle]) -> list[tuple[Candle, Candle]]:
    gaps: list[tuple[Candle, Candle]] = []
    for previous, current in zip(candles, candles[1:]):
        if current.timestamp - previous.timestamp != previous.duration:
            gaps.append((previous, current))
    return gaps


def iter_triples(candles: Iterable[Candle]) -> Iterable[tuple[Candle, Candle, Candle]]:
    candles = list(candles)
    for idx in range(len(candles) - 2):
        yield candles[idx], candles[idx + 1], candles[idx + 2]


def count_valid_sequences(candles: list[Candle]) -> tuple[int, int]:
    bullish = 0
    bearish = 0
    for c1, c2, c3 in iter_triples(candles):
        if is_valid_bullish_c2_sequence(c1, c2, c3):
            bullish += 1
        if is_valid_bearish_c2_sequence(c1, c2, c3):
            bearish += 1
    return bullish, bearish


def build_real_sample_report(candles: list[Candle]) -> RealSampleReport:
    if not candles:
        raise ValueError("real sample cannot be empty")

    symbols = {candle.symbol for candle in candles}
    timeframes = {candle.timeframe for candle in candles}
    if len(symbols) != 1:
        raise ValueError(f"real sample must contain exactly one symbol, got {sorted(symbols)}")
    if len(timeframes) != 1:
        raise ValueError(
            f"real sample must contain exactly one timeframe, got {sorted(timeframes)}"
        )

    gaps = find_timestamp_gaps(candles)
    bullish, bearish = count_valid_sequences(candles)
    first = candles[0]
    return RealSampleReport(
        symbol=first.symbol,
        timeframe=first.timeframe,
        candle_count=len(candles),
        gap_count=len(gaps),
        bullish_sequence_count=bullish,
        bearish_sequence_count=bearish,
    )
