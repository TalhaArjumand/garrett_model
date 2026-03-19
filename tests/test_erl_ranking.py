from __future__ import annotations

import unittest

from gxt.candles import Candle, utc_datetime
from gxt.erl_proxy import ERLCandidate
from gxt.erl_ranking import (
    ERLRankingWeights,
    _rank_detected_erl_candidates,
    rank_erl_candidates,
)


class ErlRankingTests(unittest.TestCase):
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
        kind: str = "old_high",
        side: str = "buy_side",
        symbol: str = "XAUUSD",
        timeframe: str = "1H",
        taken_at_hour: int | None = None,
    ) -> ERLCandidate:
        confirmed_at = utc_datetime(2026, 3, 17, confirmed_hour, 0)
        taken_at = (
            utc_datetime(2026, 3, 17, taken_at_hour, 0)
            if taken_at_hour is not None
            else None
        )
        return ERLCandidate(
            symbol=symbol,
            timeframe=timeframe,
            kind=kind,
            side=side,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            anchor_timestamps=(utc_datetime(2026, 3, 17, confirmed_hour - 2, 0),),
            confirmed_at=confirmed_at,
            is_taken=taken_at is not None,
            taken_at=taken_at,
            source_kind="test",
            decision_time_safe=True,
            reason="test candidate",
        )

    def test_rank_erl_candidates_returns_empty_when_no_candidates_exist(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=111, low=101, close=109),
            self.make_candle(timestamp_hour=12, open=109, high=112, low=102, close=110),
        ]

        ranked = rank_erl_candidates(
            candles,
            current_price=109,
            as_of_timestamp=utc_datetime(2026, 3, 17, 12, 0),
            direction_bias="bullish",
        )

        self.assertEqual(ranked, [])

    def test_rank_erl_candidates_prevents_future_leakage_for_taken_state(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=117, low=99, close=101),
            self.make_candle(timestamp_hour=14, open=101, high=121, low=100, close=112),
        ]

        ranked_before_take = rank_erl_candidates(
            candles,
            current_price=117,
            as_of_timestamp=utc_datetime(2026, 3, 17, 12, 0),
            direction_bias="bullish",
        )
        ranked_after_take = rank_erl_candidates(
            candles,
            current_price=117,
            as_of_timestamp=utc_datetime(2026, 3, 17, 14, 0),
            direction_bias="bullish",
        )

        old_high_before = next(item for item in ranked_before_take if item.candidate.kind == "old_high")
        old_high_after = next(item for item in ranked_after_take if item.candidate.kind == "old_high")

        self.assertEqual(old_high_before.feature_values["state"], "resting")
        self.assertEqual(old_high_before.feature_values["state_score"], 1.0)
        self.assertEqual(old_high_after.feature_values["state"], "taken")
        self.assertEqual(old_high_after.feature_values["state_score"], 0.35)

    def test_rank_erl_candidates_direction_alignment_scores(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=118, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=116, low=99, close=101),
            self.make_candle(timestamp_hour=14, open=101, high=117, low=100, close=112),
        ]

        ranked = rank_erl_candidates(
            candles,
            current_price=110,
            as_of_timestamp=utc_datetime(2026, 3, 17, 14, 0),
            direction_bias="bullish",
        )

        by_side = {item.candidate.side: item for item in ranked}
        self.assertEqual(by_side["buy_side"].feature_values["direction_score"], 1.0)
        self.assertEqual(by_side["sell_side"].feature_values["direction_score"], 0.0)

    def test_rank_erl_candidates_price_inside_zone_gets_max_proximity_score(self) -> None:
        candles = [
            self.make_candle(timestamp_hour=10, open=100, high=110, low=95, close=108),
            self.make_candle(timestamp_hour=11, open=108, high=120.0, low=101, close=113),
            self.make_candle(timestamp_hour=12, open=109, high=114, low=104, close=112),
            self.make_candle(timestamp_hour=13, open=112, high=119.6, low=105, close=111),
            self.make_candle(timestamp_hour=14, open=111, high=113, low=103, close=104),
        ]

        ranked = rank_erl_candidates(
            candles,
            current_price=119.8,
            as_of_timestamp=utc_datetime(2026, 3, 17, 14, 0),
            direction_bias="bullish",
            equal_tolerance=0.5,
        )

        equal_highs = next(item for item in ranked if item.candidate.kind == "equal_highs")
        self.assertEqual(equal_highs.feature_values["distance_to_candidate"], 0.0)
        self.assertEqual(equal_highs.feature_values["proximity_score"], 1.0)

    def test_rank_detected_erl_candidates_closer_candidate_ranks_higher(self) -> None:
        far_candidate = self.make_candidate(
            confirmed_hour=12,
            lower_bound=120.0,
            upper_bound=120.0,
            kind="old_high",
            side="buy_side",
        )
        near_candidate = self.make_candidate(
            confirmed_hour=13,
            lower_bound=130.0,
            upper_bound=130.0,
            kind="old_high",
            side="buy_side",
        )

        ranked = _rank_detected_erl_candidates(
            [far_candidate, near_candidate],
            current_price=129.0,
            direction_bias="bullish",
            weights=ERLRankingWeights(),
            age_candles_by_confirmed_at={
                far_candidate.confirmed_at: 2,
                near_candidate.confirmed_at: 2,
            },
            price_scale=10.0,
        )

        self.assertEqual(ranked[0].candidate.lower_bound, 130.0)

    def test_rank_detected_erl_candidates_newer_candidate_gets_higher_recency_score(self) -> None:
        older = self.make_candidate(
            confirmed_hour=12,
            lower_bound=120.0,
            upper_bound=120.0,
            kind="old_high",
            side="buy_side",
        )
        newer = self.make_candidate(
            confirmed_hour=13,
            lower_bound=120.0,
            upper_bound=120.0,
            kind="old_high",
            side="buy_side",
        )

        ranked = _rank_detected_erl_candidates(
            [older, newer],
            current_price=120.0,
            direction_bias="bullish",
            weights=ERLRankingWeights(),
            age_candles_by_confirmed_at={
                older.confirmed_at: 3,
                newer.confirmed_at: 1,
            },
            price_scale=10.0,
        )
        by_confirmed = {item.candidate.confirmed_at: item for item in ranked}

        self.assertGreater(
            by_confirmed[newer.confirmed_at].feature_values["recency_score"],
            by_confirmed[older.confirmed_at].feature_values["recency_score"],
        )

    def test_rank_detected_erl_candidates_tie_break_is_deterministic(self) -> None:
        candidate_a = self.make_candidate(
            confirmed_hour=12,
            lower_bound=120.0,
            upper_bound=120.0,
            kind="old_high",
            side="buy_side",
        )
        candidate_b = self.make_candidate(
            confirmed_hour=13,
            lower_bound=120.0,
            upper_bound=120.0,
            kind="old_high",
            side="buy_side",
        )

        ranked = _rank_detected_erl_candidates(
            [candidate_b, candidate_a],
            current_price=120.0,
            direction_bias="bullish",
            weights=ERLRankingWeights(),
            age_candles_by_confirmed_at={
                candidate_a.confirmed_at: 2,
                candidate_b.confirmed_at: 2,
            },
            price_scale=10.0,
        )

        self.assertEqual(ranked[0].candidate.confirmed_at, candidate_a.confirmed_at)
        self.assertEqual(ranked[1].candidate.confirmed_at, candidate_b.confirmed_at)

    def test_rank_detected_erl_candidates_allows_zero_width_point_candidate(self) -> None:
        point_candidate = self.make_candidate(
            confirmed_hour=12,
            lower_bound=120.0,
            upper_bound=120.0,
            kind="old_high",
            side="buy_side",
        )

        ranked = _rank_detected_erl_candidates(
            [point_candidate],
            current_price=119.0,
            direction_bias="bullish",
            weights=ERLRankingWeights(),
            age_candles_by_confirmed_at={point_candidate.confirmed_at: 1},
            price_scale=10.0,
        )

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0].feature_values["width"], 0.0)

    def test_rank_detected_erl_candidates_rejects_inverted_bounds(self) -> None:
        invalid = self.make_candidate(
            confirmed_hour=12,
            lower_bound=121.0,
            upper_bound=120.0,
            kind="equal_highs",
            side="buy_side",
        )

        with self.assertRaisesRegex(ValueError, "non-inverted bounds"):
            _rank_detected_erl_candidates(
                [invalid],
                current_price=120.0,
                direction_bias="bullish",
                weights=ERLRankingWeights(),
                age_candles_by_confirmed_at={invalid.confirmed_at: 1},
                price_scale=10.0,
            )

    def test_negative_weight_rejection(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be >= 0"):
            ERLRankingWeights(state=-0.1)


if __name__ == "__main__":
    unittest.main()
