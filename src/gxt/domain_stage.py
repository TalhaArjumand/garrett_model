from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Family(str, Enum):
    TYPE_A = "type_a"
    TYPE_B = "type_b"
    TYPE_C = "type_c"
    TYPE_D = "type_d"


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


class ExtensionKind(str, Enum):
    NONE = "none"
    TYPE_B_ADDITIVE = "type_b_additive"
    TYPE_B_ADDITIVE_C3_QUALITY = "type_b_additive_c3_quality"


def _validate_extension_kind_for_family(
    family: Family,
    extension_kind: ExtensionKind,
) -> None:
    if extension_kind is ExtensionKind.NONE:
        return

    if family is not Family.TYPE_B:
        raise ValueError(
            "extension_kind is only supported for family 'type_b'; "
            f"got family={family.value!r}, extension_kind={extension_kind.value!r}"
        )


@dataclass(frozen=True)
class DomainStageModel:
    family: Family
    domain_candle: SequenceCandle
    domain_confirmed_at: DomainConfirmedAt
    first_tradable_candle: SequenceCandle
    continuation_from: ContinuationFrom
    stage_status: StageStatus
    extension_kind: ExtensionKind

    def __post_init__(self) -> None:
        _validate_extension_kind_for_family(self.family, self.extension_kind)

    def with_stage_status(
        self,
        stage_status: StageStatus | str,
        *,
        extension_kind: ExtensionKind | str | None = None,
    ) -> DomainStageModel:
        return DomainStageModel(
            family=self.family,
            domain_candle=self.domain_candle,
            domain_confirmed_at=self.domain_confirmed_at,
            first_tradable_candle=self.first_tradable_candle,
            continuation_from=self.continuation_from,
            stage_status=_coerce_stage_status(stage_status),
            extension_kind=(
                self.extension_kind
                if extension_kind is None
                else _coerce_extension_kind(extension_kind)
            ),
        )


_DOMAIN_STAGE_BLUEPRINTS: dict[Family, DomainStageModel] = {
    Family.TYPE_A: DomainStageModel(
        family=Family.TYPE_A,
        domain_candle=SequenceCandle.C2,
        domain_confirmed_at=DomainConfirmedAt.C2_CLOSE,
        first_tradable_candle=SequenceCandle.C3,
        continuation_from=ContinuationFrom.C3_CONFIRMED,
        stage_status=StageStatus.STRUCTURAL_ONLY,
        extension_kind=ExtensionKind.NONE,
    ),
    Family.TYPE_B: DomainStageModel(
        family=Family.TYPE_B,
        domain_candle=SequenceCandle.C2,
        domain_confirmed_at=DomainConfirmedAt.C2,
        first_tradable_candle=SequenceCandle.C2,
        continuation_from=ContinuationFrom.NONE_LOCKED_YET,
        stage_status=StageStatus.STRUCTURAL_ONLY,
        extension_kind=ExtensionKind.NONE,
    ),
    Family.TYPE_C: DomainStageModel(
        family=Family.TYPE_C,
        domain_candle=SequenceCandle.C3,
        domain_confirmed_at=DomainConfirmedAt.C3_CLOSE,
        first_tradable_candle=SequenceCandle.C4,
        continuation_from=ContinuationFrom.NONE_LOCKED_YET,
        stage_status=StageStatus.STRUCTURAL_ONLY,
        extension_kind=ExtensionKind.NONE,
    ),
    Family.TYPE_D: DomainStageModel(
        family=Family.TYPE_D,
        domain_candle=SequenceCandle.C3,
        domain_confirmed_at=DomainConfirmedAt.C3_CLOSE,
        first_tradable_candle=SequenceCandle.C4,
        continuation_from=ContinuationFrom.NONE_LOCKED_YET,
        stage_status=StageStatus.STRUCTURAL_ONLY,
        extension_kind=ExtensionKind.NONE,
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


def _coerce_extension_kind(extension_kind: ExtensionKind | str) -> ExtensionKind:
    if isinstance(extension_kind, ExtensionKind):
        return extension_kind

    try:
        return ExtensionKind(extension_kind)
    except ValueError as exc:
        raise ValueError(f"unsupported extension_kind: {extension_kind!r}") from exc


def build_domain_stage_model(
    family: Family | str,
    *,
    stage_status: StageStatus | str = StageStatus.STRUCTURAL_ONLY,
    extension_kind: ExtensionKind | str = ExtensionKind.NONE,
) -> DomainStageModel:
    resolved_family = _coerce_family(family)
    blueprint = _DOMAIN_STAGE_BLUEPRINTS[resolved_family]
    return blueprint.with_stage_status(
        stage_status,
        extension_kind=extension_kind,
    )
