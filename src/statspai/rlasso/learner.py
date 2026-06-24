"""scikit-learn-compatible wrappers around the rigorous Lasso.

These adapters let the rigorous Lasso (:func:`statspai.rlasso.rlasso`) be
used as a **nuisance learner** inside the Double/Debiased ML machinery
(``sp.dml``).  They are the principled replacement for an ad-hoc
``sklearn`` LassoCV: the penalty is data-driven (no cross-validation),
heteroskedasticity-robust, and theory-justified, exactly as in
``hdm``/``DoubleML``'s ``rlasso`` learner.

* :class:`RlassoRegressor` — for continuous nuisances ``E[Y|X]`` and
  ``E[D|X]`` (the natural choice for the partially-linear model ``sp.dml(
  model='plr')``).
* :class:`RlassoClassifier` — a **linear-probability** classifier for
  binary nuisances (e.g. IRM propensities).  It fits ``rlasso`` to the
  0/1 label and clips the linear prediction into ``(eps, 1-eps)``; it is
  a convenience, not a calibrated probability model — prefer a genuine
  classifier when propensity calibration matters.

Both follow the scikit-learn estimator contract (``get_params`` /
``set_params`` / clone-safe ``__init__``) so ``sklearn.base.clone`` —
which the DML cross-fitting calls on every fold — works unchanged.

References
----------
Chernozhukov, V., Hansen, C. and Spindler, M. (2016). "hdm:
    High-Dimensional Metrics." *The R Journal*, 8(2), 185-199.
    [@chernozhukov2016hdm]
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np

try:
    from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
except Exception:  # pragma: no cover - sklearn is a hard dep of dml anyway
    BaseEstimator = object  # type: ignore[assignment,misc]

    class RegressorMixin:  # type: ignore[no-redef]
        pass

    class ClassifierMixin:  # type: ignore[no-redef]
        pass


from ._core import rlasso


def _penalty_dict(self: Any) -> Dict[str, Any]:
    pen: Dict[str, Any] = {
        "c": self.c,
        "homoscedastic": self.homoscedastic,
        "X.dependent.lambda": self.x_dependent,
    }
    if self.gamma is not None:
        pen["gamma"] = self.gamma
    if self.lambda_start is not None:
        pen["lambda.start"] = self.lambda_start
    return pen


class RlassoRegressor(BaseEstimator, RegressorMixin):
    """Rigorous (post-)Lasso as a scikit-learn regressor.

    Parameters mirror :func:`statspai.rlasso.rlasso`.  Suitable as
    ``ml_g`` / ``ml_m`` in ``sp.dml(model='plr', ...)``.
    """

    def __init__(
        self,
        post: bool = True,
        intercept: bool = True,
        c: float = 1.1,
        gamma: Optional[float] = None,
        homoscedastic: bool = False,
        x_dependent: bool = False,
        num_iter: int = 15,
        tol: float = 1e-5,
        lambda_start: Optional[float] = None,
    ):
        self.post = post
        self.intercept = intercept
        self.c = c
        self.gamma = gamma
        self.homoscedastic = homoscedastic
        self.x_dependent = x_dependent
        self.num_iter = num_iter
        self.tol = tol
        self.lambda_start = lambda_start

    def fit(self, X, y, sample_weight=None):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        y = np.asarray(y, dtype=float).ravel()
        control = {"numIter": self.num_iter, "tol": self.tol}
        self.fit_ = rlasso(
            X, y, post=self.post, intercept=self.intercept,
            penalty=_penalty_dict(self), control=control,
        )
        self.coef_ = self.fit_.beta
        self.intercept_ = self.fit_.intercept
        self.n_features_in_ = X.shape[1]
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        return self.fit_.predict(X)


class RlassoClassifier(BaseEstimator, ClassifierMixin):
    """Linear-probability classifier backed by the rigorous Lasso.

    Fits ``rlasso`` to the 0/1 label and exposes clipped
    ``predict_proba``.  Use only when a linear-probability propensity is
    acceptable; for calibrated propensities use a genuine classifier.
    """

    def __init__(
        self,
        post: bool = True,
        intercept: bool = True,
        c: float = 1.1,
        gamma: Optional[float] = None,
        homoscedastic: bool = False,
        x_dependent: bool = False,
        num_iter: int = 15,
        tol: float = 1e-5,
        lambda_start: Optional[float] = None,
        clip: float = 1e-3,
    ):
        self.post = post
        self.intercept = intercept
        self.c = c
        self.gamma = gamma
        self.homoscedastic = homoscedastic
        self.x_dependent = x_dependent
        self.num_iter = num_iter
        self.tol = tol
        self.lambda_start = lambda_start
        self.clip = clip

    def fit(self, X, y, sample_weight=None):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        y = np.asarray(y, dtype=float).ravel()
        self.classes_ = np.unique(y)
        control = {"numIter": self.num_iter, "tol": self.tol}
        self.fit_ = rlasso(
            X, y, post=self.post, intercept=self.intercept,
            penalty=_penalty_dict(self), control=control,
        )
        self.coef_ = self.fit_.beta
        self.intercept_ = self.fit_.intercept
        self.n_features_in_ = X.shape[1]
        return self

    def predict_proba(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        p1 = np.clip(self.fit_.predict(X), self.clip, 1.0 - self.clip)
        return np.column_stack([1.0 - p1, p1])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)
