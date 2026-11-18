"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """Return tp/fp/fn/tn with FAIL as the positive class."""
    if len(human) != len(judge):
        raise ValueError("human and judge must have the same length")

    tp = fp = fn = tn = 0

    for actual, predicted in zip(human, judge):
        if actual == POS and predicted == POS:
            tp += 1
        elif actual != POS and predicted == POS:
            fp += 1
        elif actual == POS and predicted != POS:
            fn += 1
        else:
            tn += 1

    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    """Return precision and recall; zero when a denominator is zero."""
    counts = confusion(human, judge)
    tp, fp, fn = counts["tp"], counts["fp"], counts["fn"]

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """Calculate Cohen's kappa. Raise ValueError when expected agreement is 1."""
    if len(human) != len(judge):
        raise ValueError("human and judge must have the same length")
    if not human:
        raise ValueError("kappa requires at least one observation")

    n = len(human)
    counts = confusion(human, judge)

    observed = (counts["tp"] + counts["tn"]) / n

    human_fail = sum(x == POS for x in human) / n
    judge_fail = sum(x == POS for x in judge) / n
    human_pass = 1.0 - human_fail
    judge_pass = 1.0 - judge_fail

    expected = human_fail * judge_fail + human_pass * judge_pass

    if expected == 1.0:
        raise ValueError("Cohen's kappa is undefined when expected agreement is 1")

    return (observed - expected) / (1.0 - expected)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denominator = sensitivity + specificity - 1.0
    if denominator == 0:
        raise ValueError("sensitivity + specificity - 1 must not be zero")

    corrected = (observed_rate + specificity - 1.0) / denominator
    return max(0.0, min(1.0, corrected))


def paired_bootstrap(
    a: Sequence[float],
    b: Sequence[float],
    *,
    n_resamples: int = 1000,
    rng: int = 2027,
    confidence: float = 0.95,
) -> tuple[float, float, float]:
    """Return mean(a)-mean(b) and a paired percentile bootstrap confidence interval."""
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b):
        raise ValueError("a and b must have the same length")
    if len(a) == 0:
        raise ValueError("paired bootstrap requires at least one observation")

    a_array = np.asarray(a, dtype=float)
    b_array = np.asarray(b, dtype=float)

    if np.array_equal(a_array, b_array):
        return (0.0, 0.0, 0.0)

    def mean_difference(x, y, axis=-1):
        return np.mean(x - y, axis=axis)

    result = bootstrap(
        (a_array, b_array),
        mean_difference,
        paired=True,
        vectorized=True,
        n_resamples=n_resamples,
        confidence_level=confidence,
        method="percentile",
        rng=np.random.default_rng(rng),
    )

    difference = float(np.mean(a_array - b_array))
    return (
        difference,
        float(result.confidence_interval.low),
        float(result.confidence_interval.high),
    )


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that at least one of k trials drawn from n passes."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """Probability that all k trials drawn from n pass."""
    # TODO M6
    raise NotImplementedError
