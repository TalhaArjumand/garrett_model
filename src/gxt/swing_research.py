from __future__ import annotations

from typing import Any

from .expansion_quality import has_small_same_side_wick
from .sequence_primitives import (
    equilibrium,
    is_bearish_c2_reversal_to_expansion,
    is_bullish_c2_reversal_to_expansion,
    validate_continuation_inputs,
    validate_sequence_inputs,
)


def is_bullish_type_b_additive_extension(
    c1: Any,
    c2: Any,
    c3: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return (
        is_bullish_c2_reversal_to_expansion(
            c1,
            c2,
            max_lower_wick_fraction=max_lower_wick_fraction,
        )
        and c2.close > c1.body_top
        and c3.low > equilibrium(c2)
    )


def is_bearish_type_b_additive_extension(
    c1: Any,
    c2: Any,
    c3: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return (
        is_bearish_c2_reversal_to_expansion(
            c1,
            c2,
            max_upper_wick_fraction=max_upper_wick_fraction,
        )
        and c2.close < c1.body_bottom
        and c3.high < equilibrium(c2)
    )


def has_bullish_type_b_additive_extension_c3_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return is_bullish_type_b_additive_extension(
        c1,
        c2,
        c3,
        max_lower_wick_fraction=max_lower_wick_fraction,
    ) and has_small_same_side_wick(
        c3,
        threshold=max_lower_wick_fraction,
    )


def has_bearish_type_b_additive_extension_c3_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3 = validate_sequence_inputs(c1, c2, c3)
    return is_bearish_type_b_additive_extension(
        c1,
        c2,
        c3,
        max_upper_wick_fraction=max_upper_wick_fraction,
    ) and has_small_same_side_wick(
        c3,
        threshold=max_upper_wick_fraction,
    )


def has_bullish_c4_after_type_b_additive_extension_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bullish_type_b_additive_extension(
            c1,
            c2,
            c3,
            max_lower_wick_fraction=max_lower_wick_fraction,
        )
        and c4.low > equilibrium(c3)
    )


def has_bearish_c4_after_type_b_additive_extension_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bearish_type_b_additive_extension(
            c1,
            c2,
            c3,
            max_upper_wick_fraction=max_upper_wick_fraction,
        )
        and c4.high < equilibrium(c3)
    )


def has_bullish_c4_after_type_b_additive_extension_expansion_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_lower_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bullish_type_b_additive_extension(
            c1,
            c2,
            c3,
            max_lower_wick_fraction=max_lower_wick_fraction,
        )
        and c4.low > equilibrium(c3)
        and c4.is_bullish
        and has_small_same_side_wick(c4, threshold=max_lower_wick_fraction)
    )


def has_bearish_c4_after_type_b_additive_extension_expansion_quality_candidate(
    c1: Any,
    c2: Any,
    c3: Any,
    c4: Any,
    *,
    max_upper_wick_fraction: Any = 0.25,
) -> bool:
    c1, c2, c3, c4 = validate_continuation_inputs(c1, c2, c3, c4)
    return (
        is_bearish_type_b_additive_extension(
            c1,
            c2,
            c3,
            max_upper_wick_fraction=max_upper_wick_fraction,
        )
        and c4.high < equilibrium(c3)
        and c4.is_bearish
        and has_small_same_side_wick(c4, threshold=max_upper_wick_fraction)
    )
