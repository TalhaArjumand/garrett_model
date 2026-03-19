from __future__ import annotations

from typing import Any

from .candles import Candle, require_closed
from .expansion_quality import has_small_same_side_wick


def _require_candle(name: str, value: Any) -> Candle:
    if not isinstance(value, Candle):
        raise TypeError(f"{name} must be a Candle, got {type(value).__name__}")
    return value


def _is_next_candle(previous: Candle, current: Candle) -> bool:
    return current.timestamp - previous.timestamp == previous.duration


def _validate_pair_inputs(left_name: str, left: Any, right_name: str, right: Any) -> tuple[Candle, Candle]:
    left = _require_candle(left_name, left)
    right = _require_candle(right_name, right)

    require_closed(left)
    require_closed(right)

    if left.symbol != right.symbol:
        raise ValueError("paired sequence candles must have the same symbol")

    if left.timeframe != right.timeframe:
        raise ValueError("paired sequence candles must have the same timeframe")

    if not left.timestamp < right.timestamp:
        raise ValueError("paired sequence candles must be in strict timestamp order")

    if not _is_next_candle(left, right):
        raise ValueError("paired sequence candles must be consecutive for their timeframe")

    return left, right


def validate_sequence_inputs(c1: Any, c2: Any, c3: Any) -> tuple[Candle, Candle, Candle]:
    c1, c2 = _validate_pair_inputs("c1", c1, "c2", c2)
    _, c3 = _validate_pair_inputs("c2", c2, "c3", c3)
    return c1, c2, c3


def validate_case_b_inputs(c1: Any, c2: Any) -> tuple[Candle, Candle]:
    return _validate_pair_inputs("c1", c1, "c2", c2)


def validate_continuation_inputs(c1: Any, c2: Any, c3: Any, c4: Any) -> tuple[Candle, Candle, Candle, Candle]:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    _, c4 = _validate_pair_inputs("c3", c3, "c4", c4)
    return c1, c2, c3, c4


def equilibrium(candle: Candle) -> float:
    return candle.low + candle.range_size / 2


def closes_inside_range(reference: Candle, candidate: Candle) -> bool:
    _validate_pair_inputs("reference", reference, "candidate", candidate)
    return reference.low < candidate.close < reference.high


def _require_positive_range(candle: Candle) -> None:
    if candle.range_size <= 0:
        raise ValueError("case B requires a positive-range candle")


def _require_positive_range_for(label: str, candle: Candle) -> None:
    if candle.range_size <= 0:
        raise ValueError(f"{label} requires a positive-range candle")


def is_bullish_c2_closure(c1: Any, c2: Any) -> bool:
    c1, c2 = _validate_pair_inputs("c1", c1, "c2", c2)
    return c2.low < c1.low and closes_inside_range(c1, c2)


def is_bearish_c2_closure(c1: Any, c2: Any) -> bool:
    c1, c2 = _validate_pair_inputs("c1", c1, "c2", c2)
    return c2.high > c1.high and closes_inside_range(c1, c2)


def has_bullish_c3_support(c2: Any, c3: Any) -> bool:
    c2, c3 = _validate_pair_inputs("c2", c2, "c3", c3)
    return c3.low > equilibrium(c2)


def has_bearish_c3_support(c2: Any, c3: Any) -> bool:
    c2, c3 = _validate_pair_inputs("c2", c2, "c3", c3)
    return c3.high < equilibrium(c2)


def is_bullish_c3_expansion_confirmation(c2: Any, c3: Any) -> bool:
    c2, c3 = _validate_pair_inputs("c2", c2, "c3", c3)
    return c3.close > c2.high


def is_bearish_c3_expansion_confirmation(c2: Any, c3: Any) -> bool:
    c2, c3 = _validate_pair_inputs("c2", c2, "c3", c3)
    return c3.close < c2.low


def is_bullish_c3_closure(c1: Any, c2: Any, c3: Any) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    _require_positive_range_for("c2", c2)
    return (
        c2.low < c1.low
        and not is_bullish_c2_closure(c1, c2)
        and c3.is_bullish
        and c3.low > c2.low
        and c3.close > c2.body_top
    )


def is_bearish_c3_closure(c1: Any, c2: Any, c3: Any) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    _require_positive_range_for("c2", c2)
    return (
        c2.high > c1.high
        and not is_bearish_c2_closure(c1, c2)
        and c3.is_bearish
        and c3.high < c2.high
        and c3.close < c2.body_bottom
    )


def is_bullish_c2_reversal_to_expansion(
    c1: Any,
    c2: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2 = validate_case_b_inputs(c1, c2)
    _require_positive_range(c2)
    return (
        c2.low < c1.low
        and c2.close > c2.open
        and c2.close > c1.low
        and has_small_same_side_wick(c2, threshold=max_lower_wick_fraction)
    )


def is_bearish_c2_reversal_to_expansion(
    c1: Any,
    c2: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2 = validate_case_b_inputs(c1, c2)
    _require_positive_range(c2)
    return (
        c2.high > c1.high
        and c2.close < c2.open
        and c2.close < c1.high
        and has_small_same_side_wick(c2, threshold=max_upper_wick_fraction)
    )


def is_valid_bullish_c2_sequence(c1: Any, c2: Any, c3: Any) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return (
        is_bullish_c2_closure(c1, c2)
        and has_bullish_c3_support(c2, c3)
        and is_bullish_c3_expansion_confirmation(c2, c3)
    )


def is_valid_bearish_c2_sequence(c1: Any, c2: Any, c3: Any) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return (
        is_bearish_c2_closure(c1, c2)
        and has_bearish_c3_support(c2, c3)
        and is_bearish_c3_expansion_confirmation(c2, c3)
    )


def has_bullish_c4_after_c3_closure_candidate(c1: Any, c2: Any, c3: Any, c4: Any) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return is_bullish_c3_closure(c1, c2, c3) and c4.low > equilibrium(c3)


def has_bearish_c4_after_c3_closure_candidate(c1: Any, c2: Any, c3: Any, c4: Any) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return is_bearish_c3_closure(c1, c2, c3) and c4.high < equilibrium(c3)


def has_bullish_c4_after_c3_closure_expansion_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    _require_positive_range_for("c4", c4)
    return (
        has_bullish_c4_after_c3_closure_candidate(c1, c2, c3, c4)
        and c4.is_bullish
        and has_small_same_side_wick(c4, threshold=max_lower_wick_fraction)
    )


def has_bearish_c4_after_c3_closure_expansion_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    _require_positive_range_for("c4", c4)
    return (
        has_bearish_c4_after_c3_closure_candidate(c1, c2, c3, c4)
        and c4.is_bearish
        and has_small_same_side_wick(c4, threshold=max_upper_wick_fraction)
    )


def has_bullish_c4_continuation_candidate(c1: Any, c2: Any, c3: Any, c4: Any) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return is_valid_bullish_c2_sequence(c1, c2, c3) and c4.low > equilibrium(c3)


def has_bearish_c4_continuation_candidate(c1: Any, c2: Any, c3: Any, c4: Any) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return is_valid_bearish_c2_sequence(c1, c2, c3) and c4.high < equilibrium(c3)
