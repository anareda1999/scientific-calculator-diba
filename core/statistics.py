"""
core/statistics.py
==================
Statistical functions for the DIDA Scientific Calculator.
"""

import math

__all__ = [
    "StatisticsError", "mean", "median", "mode", "variance", "stdev",
    "minimum", "maximum", "total", "range_of", "percentile",
    "linear_regression", "correlation", "summary",
]


class StatisticsError(Exception):
    """Raised for invalid statistical input."""


def _clean(values):
    nums = []
    for v in values:
        try:
            nums.append(float(v))
        except (TypeError, ValueError):
            raise StatisticsError(f"Valeur non numérique : '{v}'")
    if not nums:
        raise StatisticsError("Aucune donnée")
    return nums


def mean(values):
    nums = _clean(values)
    return sum(nums) / len(nums)


def median(values):
    nums = sorted(_clean(values))
    n = len(nums)
    mid = n // 2
    if n % 2:
        return nums[mid]
    return (nums[mid - 1] + nums[mid]) / 2


def mode(values):
    nums = _clean(values)
    counts = {}
    for v in nums:
        counts[v] = counts.get(v, 0) + 1
    best = max(counts.values())
    winners = sorted(v for v, c in counts.items() if c == best)
    if best == 1:
        raise StatisticsError("Aucune valeur ne se répète (pas de mode)")
    if len(winners) > 1:
        return winners
    return winners[0]


def variance(values, sample=False):
    nums = _clean(values)
    n = len(nums)
    if sample and n < 2:
        raise StatisticsError("Il faut au moins 2 valeurs pour un écart-type d'échantillon")
    if not sample and n < 1:
        raise StatisticsError("Aucune donnée")
    m = sum(nums) / n
    divisor = (n - 1) if sample else n
    return sum((v - m) ** 2 for v in nums) / divisor


def stdev(values, sample=False):
    return math.sqrt(variance(values, sample))


def minimum(values):
    return min(_clean(values))


def maximum(values):
    return max(_clean(values))


def total(values):
    return sum(_clean(values))


def range_of(values):
    nums = _clean(values)
    return max(nums) - min(nums)


def percentile(values, p):
    """Linear-interpolation percentile (0-100)."""
    nums = sorted(_clean(values))
    if not 0 <= p <= 100:
        raise StatisticsError("Le percentile doit être compris entre 0 et 100")
    if len(nums) == 1:
        return nums[0]
    rank = (len(nums) - 1) * p / 100.0
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return nums[int(rank)]
    return nums[low] + (nums[high] - nums[low]) * (rank - low)


def linear_regression(xs, ys):
    """Least-squares fit ``y = a*x + b``.

    Returns ``(slope, intercept, r_squared)``.
    """
    xv = _clean(xs)
    yv = _clean(ys)
    if len(xv) != len(yv):
        raise StatisticsError("Les deux séries doivent avoir la même longueur")
    if len(xv) < 2:
        raise StatisticsError("Il faut au moins 2 points")
    n = len(xv)
    mx = sum(xv) / n
    my = sum(yv) / n
    sxx = sum((x - mx) ** 2 for x in xv)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xv, yv))
    syy = sum((y - my) ** 2 for y in yv)
    if sxx == 0:
        raise StatisticsError("Toutes les valeurs x sont identiques")
    slope = sxy / sxx
    intercept = my - slope * mx
    r2 = 0.0 if syy == 0 else (sxy * sxy) / (sxx * syy)
    return slope, intercept, r2


def correlation(xs, ys):
    """Pearson correlation coefficient."""
    xv = _clean(xs)
    yv = _clean(ys)
    if len(xv) != len(yv) or len(xv) < 2:
        raise StatisticsError("Séries invalides")
    n = len(xv)
    mx = sum(xv) / n
    my = sum(yv) / n
    sxx = sum((x - mx) ** 2 for x in xv)
    syy = sum((y - my) ** 2 for y in yv)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xv, yv))
    if sxx == 0 or syy == 0:
        raise StatisticsError("Corrélation impossible (série constante)")
    return sxy / math.sqrt(sxx * syy)


def summary(values):
    """Return an ordered dict of the main descriptive statistics."""
    nums = _clean(values)
    return {
        "count": len(nums),
        "sum": sum(nums),
        "mean": mean(nums),
        "median": median(nums),
        "min": min(nums),
        "max": max(nums),
        "range": max(nums) - min(nums),
        "variance": variance(nums),
        "stdev": stdev(nums),
    }
