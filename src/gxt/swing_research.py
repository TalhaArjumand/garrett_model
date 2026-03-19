from __future__ import annotations

from typing import Any

from .sequence_primitives import (
    equilibrium,
    has_bearish_c4_after_c3_closure_candidate,
    has_bearish_c4_after_c3_closure_expansion_quality_candidate,
    has_bullish_c4_after_c3_closure_candidate,
    has_bullish_c4_after_c3_closure_expansion_quality_candidate,
    is_bearish_c3_closure,
    is_bullish_c3_closure,
    validate_continuation_inputs,
    validate_sequence_inputs,
)


def is_bullish_rare_c3_closure_subtype(c1: Any, c2: Any, c3: Any) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return (
        is_bullish_c3_closure(c1, c2, c3)
        and c2.close > c1.high
        and c3.low > equilibrium(c2)
    )


def is_bearish_rare_c3_closure_subtype(c1: Any, c2: Any, c3: Any) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return (
        is_bearish_c3_closure(c1, c2, c3)
        and c2.close < c1.low
        and c3.high < equilibrium(c2)
    )


def has_bullish_c4_after_rare_c3_closure_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bullish_rare_c3_closure_subtype(c1, c2, c3)
        and has_bullish_c4_after_c3_closure_candidate(c1, c2, c3, c4)
    )


def has_bearish_c4_after_rare_c3_closure_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bearish_rare_c3_closure_subtype(c1, c2, c3)
        and has_bearish_c4_after_c3_closure_candidate(c1, c2, c3, c4)
    )


def has_bullish_c4_after_rare_c3_closure_expansion_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bullish_rare_c3_closure_subtype(c1, c2, c3)
        and has_bullish_c4_after_c3_closure_expansion_quality_candidate(
            c1,
            c2,
            c3,
            c4,
            max_lower_wick_fraction=max_lower_wick_fraction,
        )
    )


def has_bearish_c4_after_rare_c3_closure_expansion_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bearish_rare_c3_closure_subtype(c1, c2, c3)
        and has_bearish_c4_after_c3_closure_expansion_quality_candidate(
            c1,
            c2,
            c3,
            c4,
            max_upper_wick_fraction=max_upper_wick_fraction,
        )
    )
