from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Family(str, Enum):
    TYPE_A = "type_a"
    TYPE_B = "type_b"
    TYPE_C = "type_c"


class SequenceCandle(str, Enum):
    C1 = "c1"
    C2 = "c2"
    C3 = "c3"
    C4 = "c4"


class DomainConfirmedAt(str, Enum):
    C2 = "c2"
    C2_CLOSE = "c2_close"
    C3_CLOSE = "c3_close"


class ContinuationFrom(str, Enum):
    C3_CONFIRMED = "c3_confirmed"
    NONE_LOCKED_YET = "none_locked_yet"


class StageStatus(str, Enum):
    STRUCTURAL_ONLY = "structural_only"
    DOMAIN_CONFIRMED = "domain_confirmed"
    FIRST_TRADABLE = "first_tradable"
    CONTINUATION_ELIGIBLE = "continuation_eligible"
    INVALIDATED = "invalidated"


@dataclass(frozen=True)
class DomainStageModel:
    family: Family
    domain_candle: SequenceCandle
    domain_confirmed_at: DomainConfirmedAt
    first_tradable_candle: SequenceCandle
    continuation_from: ContinuationFrom
    stage_status: StageStatus

    def with_stage_status(self, stage_status: StageStatus | str) -> DomainStageModel:
        return DomainStageModel(
            family=self.family,
            domain_candle=self.domain_candle,
            domain_confirmed_at=self.domain_confirmed_at,
            first_tradable_candle=self.first_tradable_candle,
            continuation_from=self.continuation_from,
            stage_status=_coerce_stage_status(stage_status),
        )


_DOMAIN_STAGE_BLUEPRINTS: dict[Family, DomainStageModel] = {
    Family.TYPE_A: DomainStageModel(
        family=Family.TYPE_A,
        domain_candle=SequenceCandle.C2,
        domain_confirmed_at=DomainConfirmedAt.C2_CLOSE,
        first_tradable_candle=SequenceCandle.C3,
        continuation_from=ContinuationFrom.C3_CONFIRMED,
        stage_status=StageStatus.STRUCTURAL_ONLY,
    ),
    Family.TYPE_B: DomainStageModel(
        family=Family.TYPE_B,
        domain_candle=SequenceCandle.C2,
        domain_confirmed_at=DomainConfirmedAt.C2,
        first_tradable_candle=SequenceCandle.C2,
        continuation_from=ContinuationFrom.NONE_LOCKED_YET,
        stage_status=StageStatus.STRUCTURAL_ONLY,
    ),
    Family.TYPE_C: DomainStageModel(
        family=Family.TYPE_C,
        domain_candle=SequenceCandle.C3,
        domain_confirmed_at=DomainConfirmedAt.C3_CLOSE,
        first_tradable_candle=SequenceCandle.C4,
        continuation_from=ContinuationFrom.NONE_LOCKED_YET,
        stage_status=StageStatus.STRUCTURAL_ONLY,
    ),
}


def _coerce_family(family: Family | str) -> Family:
    if isinstance(family, Family):
        return family

    try:
        return Family(family)
    except ValueError as exc:
        raise ValueError(f"unsupported family: {family!r}") from exc


def _coerce_stage_status(stage_status: StageStatus | str) -> StageStatus:
    if isinstance(stage_status, StageStatus):
        return stage_status

    try:
        return StageStatus(stage_status)
    except ValueError as exc:
        raise ValueError(f"unsupported stage_status: {stage_status!r}") from exc


def build_domain_stage_model(
    family: Family | str,
    *,
    stage_status: StageStatus | str = StageStatus.STRUCTURAL_ONLY,
) -> DomainStageModel:
    resolved_family = _coerce_family(family)
    blueprint = _DOMAIN_STAGE_BLUEPRINTS[resolved_family]
    return blueprint.with_stage_status(stage_status)
