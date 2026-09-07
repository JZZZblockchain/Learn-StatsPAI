from dataclasses import dataclass, replace
from typing import Any, Mapping, Optional, Sequence, Tuple

import numpy as np

from ..exceptions import DataInsufficient
from . import _oof_validation as _v
from ._irm_score import IRMScore
from ._oof_bundle_validation import AGGREGATION_RULE
from .oof import OOFBundle, OOFPredictions


@dataclass(frozen=True)
class AnalysisIdentity:
    ids: Tuple[str, ...]
    input_positions: Tuple[int, ...]
    dropped_positions: Tuple[int, ...]
    observation_ids_source: str


def internal_analysis_identity(
    *,
    n_input: int,
    complete_mask: np.ndarray,
    observation_ids: Optional[Sequence[str]],
) -> AnalysisIdentity:
    mask = np.asarray(complete_mask)
    if mask.shape != (n_input,) or mask.dtype.kind != "b":
        raise ValueError("complete_mask must be a one-dimensional bool array")
    if observation_ids is None:
        full_ids = tuple(f"row:{index}" for index in range(n_input))
        source = "generated_ordinal"
    else:
        full_ids = _v.validated_names(observation_ids, "observation_ids", n_input)
        source = "caller_provided"
    kept = tuple(np.flatnonzero(mask).tolist())
    ids = tuple(full_ids[index] for index in kept)
    return AnalysisIdentity(ids, kept, tuple(np.flatnonzero(~mask).tolist()), source)


def external_analysis_identity(
    *, predictions: "OOFPredictions", n_input: int, observation_ids_source: str
) -> AnalysisIdentity:
    if predictions.n_obs != n_input:
        raise ValueError("external prediction rows do not match input rows")
    ids = tuple(predictions.ids)
    return AnalysisIdentity(ids, tuple(range(n_input)), (), observation_ids_source)


def _internal_software_versions() -> Mapping[str, str]:
    import sklearn
    import statspai

    return {
        "statspai": str(statspai.__version__),
        "numpy": str(np.__version__),
        "scikit-learn": str(sklearn.__version__),
    }


def validate_oof_request_scope(
    *,
    model_tag: str,
    score: Optional[str],
    normalize_ipw: bool,
    has_sample_weight: bool,
    external_predictions: Optional["OOFPredictions"],
    store_oof: bool,
    observation_ids: Optional[Sequence[str]],
) -> bool:
    if type(store_oof) is not bool:
        raise TypeError("store_oof must be a bool")
    if external_predictions is None and not store_oof and observation_ids is None:
        return False
    if model_tag != "IRM" or score != "ATE":
        supported = "model='irm'" if model_tag != "IRM" else "score='ATE'"
        message = f"OOF scoring is currently implemented only for {supported}"
        raise NotImplementedError(message)
    if normalize_ipw:
        raise NotImplementedError("OOF scoring does not yet support normalize_ipw=True")
    if has_sample_weight:
        raise NotImplementedError("OOF scoring does not yet support sample_weight")
    if external_predictions is None and not store_oof:
        message = "observation_ids require external_predictions or store_oof=True"
        raise ValueError(message)
    return True


def _clone_external(predictions: "OOFPredictions") -> "OOFPredictions":
    from .oof import _clone_oof_predictions

    return _clone_oof_predictions(predictions)


def _validated_indices(value: Any, n_obs: int, name: str) -> np.ndarray:
    raw = np.asarray(value)
    if raw.ndim != 1 or raw.dtype.kind not in "iu" or raw.dtype.kind == "b":
        raise ValueError(f"{name} must be one-dimensional integer indices")
    result = np.array(raw, dtype=np.int64, copy=True)
    if np.any(result < 0) or np.any(result >= n_obs):
        raise ValueError(f"{name} contains an out-of-range index")
    if np.any(np.diff(result) <= 0):
        raise ValueError(f"{name} must be unique and strictly increasing")
    return result


def _validated_splits(capture: "OOFRepCapture", splits, minimum: int):
    try:
        rows = list(splits)
    except TypeError as exc:
        raise ValueError("splits must be a sequence") from exc
    owner, n_obs = capture._owner, len(capture._owner._y)
    if len(rows) != owner._n_folds:
        raise ValueError("splits must contain exactly n_folds entries")
    coverage, fold_ids = np.zeros(n_obs, dtype=int), np.full(n_obs, -1, dtype=int)
    records = []
    for fold, pair in enumerate(rows):
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError("each split must contain train and test indices")
        train = _validated_indices(pair[0], n_obs, "train indices")
        test = _validated_indices(pair[1], n_obs, "test indices")
        if np.intersect1d(train, test).size or len(train) + len(test) != n_obs:
            raise ValueError("each train/test split must be a disjoint full partition")
        for arm in (0, 1):
            count = int(np.sum(owner._d[train] == arm))
            if count < minimum:
                raise DataInsufficient(
                    "IRM retained OOF subgroup-mean fallback rejected: "
                    f"fold {fold}, D={arm}, count={count}, minimum={minimum}"
                )
        coverage[test] += 1
        fold_ids[test] = fold
        ids = owner._identity.ids
        train_ids, test_ids = ([ids[index] for index in part] for part in (train, test))
        treatment = owner._d[train]
        nuisance = {
            "g0": [row for row, arm in zip(train_ids, treatment) if arm == 0],
            "g1": [row for row, arm in zip(train_ids, treatment) if arm == 1],
            "ps": list(train_ids),
        }
        record = {"rep": capture._rep, "fold_id": fold, "origin": "statspai_internal"}
        record["train_ids"], record["test_ids"] = train_ids, test_ids
        record["nuisance_train_ids"] = nuisance
        record["preprocessing_train_ids"] = {k: list(v) for k, v in nuisance.items()}
        records.append(record)
    if not np.all(coverage == 1):
        raise ValueError("test folds must cover each analysis row exactly once")
    return fold_ids, records


class OOFRepCapture:
    def __init__(self, owner: Any, mode: str, rep: int, rng_seed: int) -> None:
        self._owner, self._mode, self._rep = owner, mode, rep
        self._rng_seed, self._stage = rng_seed, "new"
        self._arrays, self._records, self._score = {}, None, None

    def _require(self, mode: str, stage: str, message: str) -> None:
        if (self._mode, self._stage) != (mode, stage):
            raise RuntimeError(message)

    def record_internal_splits(self, splits, *, min_subgroup_fit: int) -> None:
        self._require("internal", "new", "internal split capture is invalid")
        fold_ids, records = _validated_splits(self, splits, min_subgroup_fit)
        self._arrays["fold_ids"], self._records = fold_ids, records
        self._stage = "split"

    def record_internal_score(
        self, *, g0, g1, ps_raw, score, fallback_g0: int, fallback_g1: int
    ) -> None:
        self._require("internal", "split", "internal score capture is invalid")
        if (fallback_g0, fallback_g1) != (0, 0) or not isinstance(score, IRMScore):
            raise RuntimeError("retained internal score cannot use subgroup fallback")
        values = {
            name: _v.immutable_array(value, name, 1)
            for name, value in {"g0": g0, "g1": g1, "ps_raw": ps_raw}.items()
        }
        if any(len(value) != len(self._owner._y) for value in values.values()):
            raise RuntimeError("internal prediction lengths do not match analysis rows")
        self._arrays.update(values)
        self._score, self._stage = score, "scored"

    def record_external_score(self, score: "IRMScore") -> None:
        self._require("external", "new", "external score capture is invalid")
        if not isinstance(score, IRMScore):
            raise RuntimeError("external score capture requires IRMScore")
        self._score, self._stage = score, "scored"


class OOFRetention:
    _predictions: Optional["OOFPredictions"]

    @classmethod
    def _new(cls, mode, identity, n_rep, n_folds, threshold):
        instance = object.__new__(cls)
        instance._mode, instance._n_rep, instance._n_folds = mode, n_rep, n_folds
        instance._trimming_threshold = threshold
        instance._identity = replace(identity)
        instance._captures, instance._active, instance._built = [], None, False
        return instance

    @classmethod
    def internal(
        cls,
        *,
        y,
        d,
        x,
        covariate_names,
        identity,
        n_rep,
        n_folds,
        random_state,
        trimming_threshold,
    ) -> "OOFRetention":
        instance = cls._new("internal", identity, n_rep, n_folds, trimming_threshold)
        y = _v.immutable_array(y, "y", 1)
        d = _v.immutable_array(d, "d", 1)
        x = _v.immutable_array(x, "x", 2)
        if d.shape != y.shape or x.shape[0] != len(y):
            raise ValueError("internal y, d, and x observation counts must match")
        if len(instance._identity.ids) != len(y):
            raise ValueError("internal identity rows must match analysis rows")
        covariates = _v.validated_names(covariate_names, "covariate_names", x.shape[1])
        recipe = (
            "StatsPAI-observed outer-fold scopes; observation_ids_source="
            f"{identity.observation_ids_source}; fit_seed is random_state + rep "
            "for split/call provenance and does not override learner randomness"
        )
        source = {"engine": "statspai_irm_internal", "recipe": recipe}
        source["seed"] = int(random_state)
        source["software_versions"] = dict(_internal_software_versions())
        base = {"ids": instance._identity.ids, "y": y, "d": d, "x": x}
        base["covariate_names"], base["source"] = covariates, source
        instance._prediction_base = base
        instance._y, instance._d, instance._predictions = y, d, None
        return instance

    @classmethod
    def external(
        cls, *, predictions, identity, n_rep, n_folds, trimming_threshold
    ) -> "OOFRetention":
        instance = cls._new("external", identity, n_rep, n_folds, trimming_threshold)
        instance._predictions = _clone_external(predictions)
        return instance

    def start_rep(self, rep: int, rng_seed: int) -> OOFRepCapture:
        if self._active is not None or rep != len(self._captures) or rep >= self._n_rep:
            raise RuntimeError("OOF repeats must start once in order")
        self._active = OOFRepCapture(self, self._mode, rep, rng_seed)
        return self._active

    def finish_rep(self, capture: OOFRepCapture, theta: float, se: float) -> None:
        valid = capture is self._active and capture._owner is self
        if not valid or capture._stage != "scored":
            raise RuntimeError("OOF repeat capture is incomplete or foreign")
        if theta != capture._score.theta or se != capture._score.se:
            raise RuntimeError("fit result disagrees with captured IRMScore")
        self._captures.append(capture)
        self._active = None

    def build(self, aggregate_theta: float, aggregate_se: float) -> "OOFBundle":
        complete = self._active is None and len(self._captures) == self._n_rep
        if not complete or self._built:
            raise RuntimeError("OOF retention is incomplete or already built")
        self._built = True
        threshold = self._trimming_threshold
        external = self._mode == "external"
        captures = self._captures
        if external:
            predictions = self._predictions
        else:
            arrays = {
                name: np.stack([capture._arrays[name] for capture in captures])
                for name in ("g0", "g1", "ps_raw", "fold_ids")
            }
            records = [item for capture in captures for item in capture._records]
            predictions = OOFPredictions.from_arrays(
                training_records=records, **self._prediction_base, **arrays
            )
        scores = [capture._score for capture in captures]
        fallback = None if external else {"g0": 0, "g1": 0}
        fit_records = []
        for row in predictions.training_records:
            record = {key: row[key] for key in ("rep", "fold_id")}
            record["fit_seed"] = None if external else captures[row["rep"]]._rng_seed
            record["subgroup_fallback_counts"] = fallback
            fit_records.append(record)
        clipping_counts = []
        for rep, raw in enumerate(predictions.ps_raw):
            record = {"rep": rep}
            record["n_clipped_low"] = int(np.sum(raw < threshold))
            record["n_clipped_high"] = int(np.sum(raw > 1.0 - threshold))
            clipping_counts.append(record)
        engine = "external_predictions" if external else "internal"
        metadata = {
            "scoring_engine": f"statspai_irm_{engine}",
            "score": "ATE",
            "psi_a": -1.0,
            "variance_policy": "ddof0",
            "trimming_threshold": threshold,
            "normalize_ipw": False,
            "clipping_counts": clipping_counts,
            "fit_records": fit_records,
        }
        score_arrays = {
            name: np.stack([getattr(score, name) for score in scores])
            for name in ("ps_used", "psi_b", "psi", "theta", "se")
        }
        return OOFBundle.from_arrays(
            predictions=predictions,
            input_positions=self._identity.input_positions,
            dropped_positions=self._identity.dropped_positions,
            aggregation={
                "rule": AGGREGATION_RULE,
                "theta": aggregate_theta,
                "se": aggregate_se,
            },
            metadata=metadata,
            **score_arrays,
        )
