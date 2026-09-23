"""Averages of a causal forest fitted on a continuous treatment.

The binary AIPW score divides by ``e(1 - e)`` for a propensity ``e`` and is
undefined when ``T`` is continuous: on the Card returns-to-schooling design the
clipped "propensity" ``E[educ | X]`` turned it into a ~1,200x multiplier and an
"ATE" of -1266.6.  These tests pin how each engine handles that design.

* GRF engine (default): ``target_sample="all"`` uses the continuous-treatment
  doubly-robust score, whose debiasing weight is ``(W - W_hat) / Var(W | X)``
  with ``Var(W | X)`` estimated by an out-of-bag regression forest (the Riesz
  representer of the average effect in the partially linear model); ``overlap``
  is the partially linear coefficient.
* ``treated`` and ``control`` raise on both engines, as in grf: a continuous
  treatment defines no treated group, and ``T == 1`` would select the rows
  with one year of schooling.
* Legacy engine: ``all`` falls back to the plug-in average with a warning.
"""

from __future__ import annotations

import numpy as np
import pytest

import statspai as sp
from statspai.exceptions import AssumptionWarning


@pytest.fixture(scope="module")
def card():
    return sp.datasets.card_1995()


def _forest(data, treatment, *, discrete, split_rule="grf"):
    kwargs = {} if split_rule == "grf" else {"split_rule": "legacy"}
    return sp.causal_forest(
        f"lwage ~ {treatment} | exper + black + south + smsa",
        data=data,
        n_estimators=200,
        discrete_treatment=discrete,
        random_state=42,
        **kwargs,
    )


@pytest.fixture(scope="module")
def educ_forest(card):
    return _forest(card, "educ", discrete=False)


class TestContinuousTreatmentAggregation:
    def test_all_uses_the_continuous_doubly_robust_score(self, educ_forest):
        payload = educ_forest.average_treatment_effect()
        assert payload["method"] == "aipw_continuous"
        assert payload["se"] > 0

    def test_continuous_estimate_is_on_the_effect_scale(self, educ_forest):
        # The regression the guard exists for returned -1266. The
        # doubly-robust average must stay near the mean out-of-bag CATE
        # (about 0.075 log points per year of schooling here).
        payload = educ_forest.average_treatment_effect()
        mean_cate = float(np.mean(educ_forest.predict()))
        assert abs(payload["estimate"] - mean_cate) < 0.02
        assert 0.0 < payload["estimate"] < 0.2

    def test_overlap_is_the_partially_linear_coefficient(self, educ_forest):
        payload = educ_forest.average_treatment_effect(target_sample="overlap")
        assert payload["method"] == "partially_linear"
        W_res = educ_forest._T_original - educ_forest._e_insample
        Y_res = educ_forest._Y_original - educ_forest._m_insample
        design = np.column_stack([np.ones_like(W_res), W_res])
        beta = np.linalg.lstsq(design, Y_res, rcond=None)[0]
        assert payload["estimate"] == pytest.approx(beta[1], rel=1e-10)

    def test_treated_target_raises(self, educ_forest):
        with pytest.raises(sp.MethodIncompatibility, match="needs a binary treatment"):
            educ_forest.average_treatment_effect(target_sample="treated")

    def test_att_raises_instead_of_averaging_the_dose_one_rows(self, educ_forest):
        # Before 1.30 this returned the mean CATE over rows with educ == 1,
        # printed as "ATT" with a zero-width interval.
        with pytest.raises(sp.MethodIncompatibility, match="needs a binary treatment"):
            educ_forest.att()

    def test_binary_treatment_still_uses_the_aipw_score(self, card):
        forest = _forest(card, "nearc4", discrete=True)
        payload = forest.average_treatment_effect()
        assert payload["method"] == "aipw"
        assert "plug_in_reason" not in payload
        mean_cate = float(np.mean(forest.predict()))
        assert abs(payload["estimate"] - mean_cate) < 0.5

    def test_binary_treatment_effect_prints_the_aipw_label(self, card):
        forest = _forest(card, "nearc4", discrete=True)
        assert "descriptive SE" not in str(forest.ate())

    def test_atc_on_a_continuous_treatment_raises(self, educ_forest):
        with pytest.raises(sp.MethodIncompatibility, match="needs a binary treatment"):
            educ_forest.average_treatment_effect(target_sample="control")


class TestLegacyEngineContinuousTreatment:
    @pytest.fixture(scope="class")
    def legacy(self, card):
        with pytest.warns(DeprecationWarning):
            return _forest(card, "educ", discrete=False, split_rule="legacy")

    def test_legacy_warns_and_falls_back_to_plug_in(self, legacy):
        with pytest.warns(AssumptionWarning, match="requires a binary treatment"):
            payload = legacy.average_treatment_effect()
        assert payload["method"] == "plug_in"
        assert payload["plug_in_reason"] == "non_binary_treatment"

    def test_legacy_estimate_tracks_the_mean_cate(self, legacy, card):
        mean_cate = float(np.mean(legacy.effect(card)))
        with pytest.warns(AssumptionWarning):
            payload = legacy.average_treatment_effect()
        assert payload["estimate"] == pytest.approx(mean_cate, rel=1e-10)
        assert abs(payload["estimate"]) < 1.0

    def test_legacy_printed_effect_labels_the_descriptive_standard_error(self, legacy):
        with pytest.warns(AssumptionWarning):
            effect = legacy.ate()
        assert "descriptive SE" in str(effect)

    def test_legacy_treated_target_raises(self, legacy):
        with pytest.raises(sp.MethodIncompatibility, match="needs a binary treatment"):
            legacy.average_treatment_effect(target_sample="treated")
