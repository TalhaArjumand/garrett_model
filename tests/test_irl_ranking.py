from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.fvg import FVGCandidate
from gxt.irl_ranking import (
    IRLRankingWeights,
    _rank_detected_irl_candidates,
    rank_irl_candidates,
)


class IrlRankingTests(unittest.TestCase):
    def make_candle(
        self,
        *,
        timestamp_hour: int,
        symbol: str = "XAUUSD",
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

    def make_candidate(
        self,
        *,
        confirmed_hour: int,
        lower_bound: float,
        upper_bound: float,
        direction: str = "bullish",
        symbol: str = "XAUUSD",
        timeframe: str = "1H",
        reached_at_hour: int | None = None,
        invalidated_at_hour: int | None = None,
    ) -> FVGCandidate:
        confirmed_at = utc_datetime(2026, 3, 17, confirmed_hour, 0)
        reached_at = (
            utc_datetime(2026, 3, 17, reached_at_hour, 0)
            if reached_at_hour is not None
            else None
        )
        invalidated_at = (
            utc_datetime(2026, 3, 17, invalidated_at_hour, 0)
            if invalidated_at_hour is not None
            else None
        )
        return FVGCandidate(
            symbol=symbol,
            timeframe=timeframe,
            direction=direction,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            c1_timestamp=utc_datetime(2026, 3, 17, confirmed_hour - 2, 0),
            c2_timestamp=utc_datetime(2026, 3, 17, confirmed_hour - 1, 0),
            c3_timestamp=confirmed_at,
            confirmed_at=confirmed_at,
            is_reached=reached_at is not None,
            reached_at=reached_at,
            decision_time_safe=True,
            reason="test candidate",
            invalidated_at=invalidated_at,
        )

    def test_rank_irl_candidates_returns_empty_when_no_candidates_exist(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=112, low=101, close=104),
            self.make_candle(timestamp_hour=12, open=104, high=111, low=99, close=110),
        ]

        ranked = rank_irl_candidates(
            candles,
            current_price=109,
            as_of_timestamp=utc_datetime(2026, 3, 17, 12, 0),
            direction_bias="bullish",
        )

        self.assertEqual(ranked, [])

    def test_rank_irl_candidates_prevents_future_leakage_for_reached_state(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119),
            self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123),
            self.make_candle(timestamp_hour=13, open=123, high=124, low=111, close=112),
        ]

        ranked_before_reach = rank_irl_candidates(
            candles,
            current_price=118,
            as_of_timestamp=utc_datetime(2026, 3, 17, 12, 0),
            direction_bias="bullish",
        )
        ranked_after_reach = rank_irl_candidates(
            candles,
            current_price=118,
            as_of_timestamp=utc_datetime(2026, 3, 17, 13, 0),
            direction_bias="bullish",
        )

        self.assertEqual(len(ranked_before_reach), 1)
        self.assertEqual(len(ranked_after_reach), 1)
        self.assertEqual(ranked_before_reach[0].feature_values["state"], "resting")
        self.assertEqual(ranked_before_reach[0].feature_values["state_score"], 1.0)
        self.assertEqual(ranked_after_reach[0].feature_values["state"], "reached")
        self.assertEqual(ranked_after_reach[0].feature_values["state_score"], 0.35)

    def test_rank_irl_candidates_direction_alignment_scores(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119),
            self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123),
            self.make_candle(timestamp_hour=13, open=123, high=124, low=100, close=101),
            self.make_candle(timestamp_hour=14, open=101, high=103, low=90, close=92),
            self.make_candle(timestamp_hour=15, open=92, high=98, low=80, close=85),
        ]

        ranked = rank_irl_candidates(
            candles,
            current_price=90,
            as_of_timestamp=utc_datetime(2026, 3, 17, 15, 0),
            direction_bias="bullish",
        )

        by_direction = {item.candidate.direction: item for item in ranked}
        self.assertEqual(by_direction["bullish"].feature_values["direction_score"], 1.0)
        self.assertEqual(by_direction["bearish"].feature_values["direction_score"], 0.0)

    def test_rank_irl_candidates_price_inside_gap_gets_max_proximity_score(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119),
            self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123),
        ]

        ranked = rank_irl_candidates(
            candles,
            current_price=111,
            as_of_timestamp=utc_datetime(2026, 3, 17, 12, 0),
            direction_bias="bullish",
        )

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0].feature_values["distance_to_zone"], 0.0)
        self.assertEqual(ranked[0].feature_values["proximity_score"], 1.0)

    def test_rank_irl_candidates_closer_candidate_ranks_higher(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119),
            self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123),
            self.make_candle(timestamp_hour=13, open=123, high=130, low=119, close=129),
            self.make_candle(timestamp_hour=14, open=129, high=138, low=126, close=137),
            self.make_candle(timestamp_hour=15, open=137, high=145, low=132, close=144),
        ]

        ranked = rank_irl_candidates(
            candles,
            current_price=133,
            as_of_timestamp=utc_datetime(2026, 3, 17, 15, 0),
            direction_bias="bullish",
        )

        self.assertGreaterEqual(len(ranked), 2)
        self.assertEqual(ranked[0].candidate.c3_timestamp, utc_datetime(2026, 3, 17, 15, 0))

    def test_rank_irl_candidates_newer_candidate_gets_higher_recency_score(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120, low=107, close=119),
            self.make_candle(timestamp_hour=12, open=118, high=125, low=112, close=123),
            self.make_candle(timestamp_hour=13, open=123, high=130, low=119, close=129),
            self.make_candle(timestamp_hour=14, open=129, high=138, low=126, close=137),
            self.make_candle(timestamp_hour=15, open=137, high=145, low=132, close=144),
        ]

        ranked = rank_irl_candidates(
            candles,
            current_price=133,
            as_of_timestamp=utc_datetime(2026, 3, 17, 15, 0),
            direction_bias="bullish",
        )
        by_confirmed = {item.candidate.confirmed_at: item for item in ranked}
        older = by_confirmed[utc_datetime(2026, 3, 17, 12, 0)]
        newer = by_confirmed[utc_datetime(2026, 3, 17, 15, 0)]

        self.assertGreater(newer.feature_values["recency_score"], older.feature_values["recency_score"])

    def test_rank_detected_irl_candidates_tie_break_is_deterministic(self) -> None:
        candidate_a = self.make_candidate(confirmed_hour=12, lower_bound=100, upper_bound=110)
        candidate_b = self.make_candidate(confirmed_hour=13, lower_bound=100, upper_bound=110)

        ranked = _rank_detected_irl_candidates(
            [candidate_b, candidate_a],
            current_price=105,
            direction_bias="bullish",
            weights=IRLRankingWeights(),
            age_candles_by_confirmed_at={
                candidate_a.confirmed_at: 2,
                candidate_b.confirmed_at: 2,
            },
            price_scale=10.0,
        )

        self.assertEqual(ranked[0].candidate.confirmed_at, candidate_a.confirmed_at)
        self.assertEqual(ranked[1].candidate.confirmed_at, candidate_b.confirmed_at)

    def test_rank_detected_irl_candidates_rejects_invalid_width(self) -> None:
        invalid = FVGCandidate(
            symbol="XAUUSD",
            timeframe="1H",
            direction="bullish",
            lower_bound=100.0,
            upper_bound=100.0,
            c1_timestamp=utc_datetime(2026, 3, 17, 10, 0),
            c2_timestamp=utc_datetime(2026, 3, 17, 11, 0),
            c3_timestamp=utc_datetime(2026, 3, 17, 12, 0),
            confirmed_at=utc_datetime(2026, 3, 17, 12, 0),
            is_reached=False,
            reached_at=None,
            decision_time_safe=True,
            reason="invalid",
            invalidated_at=None,
        )

        with self.assertRaisesRegex(ValueError, "positive width"):
            _rank_detected_irl_candidates(
                [invalid],
                current_price=101,
                direction_bias="bullish",
                weights=IRLRankingWeights(),
                age_candles_by_confirmed_at={invalid.confirmed_at: 1},
                price_scale=10.0,
            )

    def test_negative_weight_rejection(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be >= 0"):
            IRLRankingWeights(state=-0.1)

    def test_rank_detected_irl_candidates_marks_invalidated_state_with_zero_score(self) -> None:
        candidate = self.make_candidate(
            confirmed_hour=12,
            lower_bound=100,
            upper_bound=110,
            invalidated_at_hour=14,
        )

        ranked = _rank_detected_irl_candidates(
            [candidate],
            current_price=105,
            direction_bias="bullish",
            weights=IRLRankingWeights(),
            age_candles_by_confirmed_at={candidate.confirmed_at: 2},
            price_scale=10.0,
        )

        self.assertEqual(ranked[0].feature_values["state"], "invalidated")
        self.assertEqual(ranked[0].feature_values["state_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
