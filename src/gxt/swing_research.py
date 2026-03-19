from __future__ import annotations

from typing import Any

from .sequence_primitives import (
    equilibrium,
    is_bearish_c3_closure,
    is_bullish_c3_closure,
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
