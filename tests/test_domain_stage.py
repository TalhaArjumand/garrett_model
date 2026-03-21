from __future__ import annotations

import unittest

from gxt import (
    ContinuationFrom,
    DomainConfirmedAt,
    ExtensionKind,
    Family,
    SequenceCandle,
    StageStatus,
    build_domain_stage_model,
)


class DomainStageTests(unittest.TestCase):
    def test_type_a_stage_blueprint_matches_locked_contract(self) -> None:
        model = build_domain_stage_model(Family.TYPE_A)

        self.assertEqual(model.family, Family.TYPE_A)
        self.assertEqual(model.domain_candle, SequenceCandle.C2)
        self.assertEqual(model.domain_confirmed_at, DomainConfirmedAt.C2_CLOSE)
        self.assertEqual(model.first_tradable_candle, SequenceCandle.C3)
        self.assertEqual(model.continuation_from, ContinuationFrom.C3_CONFIRMED)
        self.assertEqual(model.stage_status, StageStatus.STRUCTURAL_ONLY)
        self.assertEqual(model.extension_kind, ExtensionKind.NONE)

    def test_type_b_stage_blueprint_matches_locked_contract(self) -> None:
        model = build_domain_stage_model("type_b", stage_status="domain_confirmed")

        self.assertEqual(model.family, Family.TYPE_B)
        self.assertEqual(model.domain_candle, SequenceCandle.C2)
        self.assertEqual(model.domain_confirmed_at, DomainConfirmedAt.C2)
        self.assertEqual(model.first_tradable_candle, SequenceCandle.C2)
        self.assertEqual(model.continuation_from, ContinuationFrom.NONE_LOCKED_YET)
        self.assertEqual(model.stage_status, StageStatus.DOMAIN_CONFIRMED)
        self.assertEqual(model.extension_kind, ExtensionKind.NONE)

    def test_type_c_stage_blueprint_matches_locked_contract(self) -> None:
        model = build_domain_stage_model(Family.TYPE_C)

        self.assertEqual(model.family, Family.TYPE_C)
        self.assertEqual(model.domain_candle, SequenceCandle.C3)
        self.assertEqual(model.domain_confirmed_at, DomainConfirmedAt.C3_CLOSE)
        self.assertEqual(model.first_tradable_candle, SequenceCandle.C4)
        self.assertEqual(model.continuation_from, ContinuationFrom.NONE_LOCKED_YET)
        self.assertEqual(model.stage_status, StageStatus.STRUCTURAL_ONLY)
        self.assertEqual(model.extension_kind, ExtensionKind.NONE)

    def test_with_stage_status_preserves_structure(self) -> None:
        model = build_domain_stage_model(Family.TYPE_A)
        updated = model.with_stage_status(StageStatus.FIRST_TRADABLE)

        self.assertEqual(updated.family, model.family)
        self.assertEqual(updated.domain_candle, model.domain_candle)
        self.assertEqual(updated.domain_confirmed_at, model.domain_confirmed_at)
        self.assertEqual(updated.first_tradable_candle, model.first_tradable_candle)
        self.assertEqual(updated.continuation_from, model.continuation_from)
        self.assertEqual(updated.stage_status, StageStatus.FIRST_TRADABLE)
        self.assertEqual(updated.extension_kind, ExtensionKind.NONE)

    def test_build_domain_stage_model_allows_locked_extension_kind(self) -> None:
        model = build_domain_stage_model(
            Family.TYPE_B,
            extension_kind=ExtensionKind.TYPE_B_ADDITIVE,
        )

        self.assertEqual(model.family, Family.TYPE_B)
        self.assertEqual(model.extension_kind, ExtensionKind.TYPE_B_ADDITIVE)

    def test_build_domain_stage_model_rejects_unknown_family(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported family"):
            build_domain_stage_model("type_d")

    def test_with_stage_status_rejects_unknown_stage_status(self) -> None:
        model = build_domain_stage_model(Family.TYPE_B)

        with self.assertRaisesRegex(ValueError, "unsupported stage_status"):
            model.with_stage_status("ready")

    def test_build_domain_stage_model_rejects_unknown_extension_kind(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported extension_kind"):
            build_domain_stage_model(Family.TYPE_B, extension_kind="type_d_additive")

    def test_build_domain_stage_model_rejects_type_b_extension_on_non_type_b_family(self) -> None:
        with self.assertRaisesRegex(ValueError, "only supported for family 'type_b'"):
            build_domain_stage_model(
                Family.TYPE_C,
                extension_kind=ExtensionKind.TYPE_B_ADDITIVE,
            )
