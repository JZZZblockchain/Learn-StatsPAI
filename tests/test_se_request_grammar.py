"""Shared Stata-style SE grammar: ``parse_se_request`` and ``ml_vcov``.

``parse_se_request`` is the one place every estimator's ``robust=`` / ``vce=``
value is interpreted.  The contract these tests pin:

* every Stata spelling that means the same thing maps to the same kind
  (``True`` / ``"robust"`` / ``"vce(robust)"`` / ``"r"``);
* a cluster variable may be written inline (``"cluster firm"``) exactly as in
  Stata's ``vce(cluster firm)``;
* anything unknown, unsupported, or self-contradictory raises -- never a
  quiet fallback to some other standard error.

``ml_vcov`` pins the finite-sample factors of Stata's ML sandwich; the
factors are exact algebraic identities, so the tolerances are 1e-12.
"""

from __future__ import annotations

import numpy as np
import pytest

from statspai.core._vcov import ml_vcov, sandwich_vcov
from statspai.core._vcov_spec import parse_se_request
from statspai.exceptions import MethodIncompatibility

ALL = ("nonrobust", "robust", "hc0", "hc1", "hc2", "hc3", "cluster", "cr2", "wild")


def _parse(robust, cluster=None, supported=ALL, multiway=False):
    return parse_se_request(
        robust, cluster, function="f", supported=supported, multiway=multiway
    )


class TestSpellings:
    @pytest.mark.parametrize("value", [None, False, "nonrobust", "OIM", "ols", "iid"])
    def test_model_based(self, value):
        assert _parse(value).kind == "nonrobust"

    @pytest.mark.parametrize(
        "value", [True, "robust", "Robust", "r", "vce(robust)", " VCE( robust ) "]
    )
    def test_robust(self, value):
        assert _parse(value).kind == "robust"

    @pytest.mark.parametrize(
        "value,kind", [("HC1", "hc1"), ("hc3", "hc3"), ("white", "hc0")]
    )
    def test_hc_family(self, value, kind):
        assert _parse(value).kind == kind

    def test_spelling_is_kept(self):
        assert _parse("vce(robust)").spelling == "vce(robust)"


class TestCluster:
    @pytest.mark.parametrize(
        "value", ["cluster firm", "cl firm", "vce(cluster firm)", "CLUSTER firm"]
    )
    def test_inline_cluster_variable(self, value):
        req = _parse(value)
        assert (req.kind, req.cluster) == ("cluster", "firm")

    def test_variable_name_case_is_preserved(self):
        assert _parse("cluster FirmID").cluster == "FirmID"

    def test_cluster_keyword_with_cluster_argument(self):
        req = _parse("cluster", cluster="firm")
        assert (req.kind, req.cluster) == ("cluster", "firm")

    def test_inline_and_argument_agree(self):
        assert _parse("cluster firm", cluster="firm").cluster == "firm"

    def test_inline_and_argument_conflict_raises(self):
        with pytest.raises(
            MethodIncompatibility, match="Pass the cluster variable once"
        ):
            _parse("cluster firm", cluster="state")

    @pytest.mark.parametrize("value", ["cluster", "cr2", "wild"])
    def test_cluster_kind_without_variable_raises(self, value):
        with pytest.raises(MethodIncompatibility, match="requires cluster"):
            _parse(value)

    @pytest.mark.parametrize("value", [None, "nonrobust", "robust", "hc0", "hc1", True])
    def test_cluster_argument_upgrades_heteroskedastic_kinds(self, value):
        # The documented ``robust='hc1', cluster='firm'`` idiom keeps working.
        req = _parse(value, cluster="firm")
        assert (req.kind, req.cluster) == ("cluster", "firm")

    def test_small_sample_cluster_kind_is_kept(self):
        assert _parse("cr2", cluster="firm").kind == "cr2"

    @pytest.mark.parametrize("value", ["hc3", "hc2"])
    def test_incompatible_kind_with_cluster_raises(self, value):
        with pytest.raises(MethodIncompatibility, match="cannot be combined"):
            _parse(value, cluster="firm")

    def test_multiway_inline_requires_permission(self):
        with pytest.raises(MethodIncompatibility, match="multiway"):
            _parse("cluster firm year")
        req = _parse("cluster firm year", multiway=True)
        assert req.cluster == ["firm", "year"]

    def test_single_element_list_collapses(self):
        assert _parse(None, cluster=["firm"]).cluster == "firm"

    def test_array_cluster_passes_through(self):
        labels = np.array([1, 1, 2, 2])
        req = _parse("robust", cluster=labels)
        assert req.kind == "cluster" and req.cluster is labels


class TestFailures:
    def test_unknown_spelling_raises_with_supported_list(self):
        with pytest.raises(MethodIncompatibility, match="Unknown robust option") as exc:
            _parse("hc9")
        assert "'robust'" in str(exc.value)

    def test_unknown_is_a_value_error(self):
        # Historical callers catch ValueError.
        with pytest.raises(ValueError):
            _parse("bogus")

    def test_recognised_but_unsupported_raises(self):
        with pytest.raises(MethodIncompatibility, match="not available"):
            _parse("hc3", supported=("nonrobust", "robust", "cluster"))

    def test_cluster_unsupported_raises(self):
        with pytest.raises(MethodIncompatibility, match="not available"):
            _parse("robust", cluster="firm", supported=("nonrobust", "robust"))

    def test_variable_after_non_cluster_kind_raises(self):
        with pytest.raises(MethodIncompatibility, match="only cluster-type"):
            _parse("robust firm")

    @pytest.mark.parametrize("value", [1, 0.5, {"CRV1": "firm"}])
    def test_wrong_type_raises(self, value):
        with pytest.raises(MethodIncompatibility, match="must be a string or a bool"):
            _parse(value)

    def test_empty_string_raises(self):
        with pytest.raises(MethodIncompatibility, match="Unknown robust option"):
            _parse("   ")


class TestMLVcov:
    @pytest.fixture()
    def parts(self):
        rng = np.random.default_rng(3)
        n, k = 60, 3
        scores = rng.normal(size=(n, k))
        a = rng.normal(size=(k, k))
        bread = np.linalg.inv(a @ a.T + k * np.eye(k))
        clusters = np.repeat(np.arange(12), 5)
        return bread, scores, clusters, n, k

    def test_nonrobust_is_the_bread(self, parts):
        bread, scores, _, _, _ = parts
        v = ml_vcov(bread, scores, kind="nonrobust")
        np.testing.assert_array_equal(v, bread)
        assert v is not bread

    def test_robust_is_hc0_times_n_over_n_minus_1(self, parts):
        bread, scores, _, n, _ = parts
        hc0 = bread @ scores.T @ scores @ bread
        np.testing.assert_allclose(
            ml_vcov(bread, scores, kind="robust"), hc0 * n / (n - 1), rtol=1e-12
        )
        np.testing.assert_allclose(ml_vcov(bread, scores, kind="hc0"), hc0, rtol=1e-12)

    def test_hc1_is_hc0_times_n_over_n_minus_k(self, parts):
        bread, scores, _, n, k = parts
        np.testing.assert_allclose(
            ml_vcov(bread, scores, kind="hc1"),
            ml_vcov(bread, scores, kind="hc0") * n / (n - k),
            rtol=1e-12,
        )

    def test_cluster_is_g_over_g_minus_1_only(self, parts):
        bread, scores, clusters, _, _ = parts
        g = len(np.unique(clusters))
        summed = np.vstack(
            [scores[clusters == c].sum(axis=0) for c in np.unique(clusters)]
        )
        expected = g / (g - 1) * bread @ summed.T @ summed @ bread
        np.testing.assert_allclose(
            ml_vcov(bread, scores, kind="cluster", clusters=clusters),
            expected,
            rtol=1e-12,
        )
        # ... and it is not the regress-family factor.
        stata_ols = sandwich_vcov(bread, scores, clusters=clusters, correction="stata")
        assert not np.allclose(stata_ols, expected, rtol=1e-6)

    def test_kind_is_case_insensitive(self, parts):
        bread, scores, _, _, _ = parts
        np.testing.assert_array_equal(
            ml_vcov(bread, scores, kind="ROBUST"), ml_vcov(bread, scores, kind="robust")
        )

    def test_missing_scores_or_clusters_raise(self, parts):
        bread, scores, _, _, _ = parts
        with pytest.raises(MethodIncompatibility, match="scores"):
            ml_vcov(bread, None, kind="robust")
        with pytest.raises(MethodIncompatibility, match="cluster labels"):
            ml_vcov(bread, scores, kind="cluster")

    @pytest.mark.parametrize("kind", ["hc3", "wild", "bogus"])
    def test_undefined_kind_raises(self, parts, kind):
        bread, scores, _, _, _ = parts
        with pytest.raises(MethodIncompatibility, match="not defined"):
            ml_vcov(bread, scores, kind=kind)
