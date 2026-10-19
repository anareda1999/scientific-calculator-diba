"""
core/equations.py
=================
Equation solving helpers: linear, quadratic and linear systems.
"""

import math

__all__ = [
    "EquationError", "solve_linear", "solve_quadratic",
    "solve_system", "solve_numerically",
]


class EquationError(Exception):
    """Raised for any invalid equation input."""


def solve_linear(a, b):
    """Solve ``a*x + b = 0``.

    Returns ``(x, kind)`` where kind is one of
    ``"unique"``, ``"none"``, ``"infinite"``.
    """
    a, b = complex(a), complex(b)
    if abs(a) < 1e-14:
        if abs(b) < 1e-14:
            return None, "infinite"
        return None, "none"
    return -b / a, "unique"


def solve_quadratic(a, b, c):
    """Solve ``a*x^2 + b*x + c = 0``.

    Returns ``(roots, delta, kind)`` where kind is
    ``"two"``, ``"double"``, ``"none"`` or ``"linear"``.
    """
    a, b, c = complex(a), complex(b), complex(c)
    if abs(a) < 1e-14:
        root, kind = solve_linear(b, c)
        if kind == "unique":
            return [root], complex(0), "linear"
        return [], complex(0), kind
    delta = b * b - 4 * a * c
    if abs(delta.imag) < 1e-14 and delta.real < 0:
        # negative discriminant -> complex conjugate roots
        root_delta = complex(0, math.sqrt(-delta.real))
        x1 = (-b + root_delta) / (2 * a)
        x2 = (-b - root_delta) / (2 * a)
        return [x1, x2], delta, "two"
    if abs(delta) < 1e-14:
        return [-b / (2 * a)], delta, "double"
    sqrt_delta = complex(math.sqrt(delta.real), delta.imag and
                         math.sqrt(abs(delta.imag)) * (1 if delta.imag > 0 else -1)
                         or 0)
    x1 = (-b + sqrt_delta) / (2 * a)
    x2 = (-b - sqrt_delta) / (2 * a)
    return [x1, x2], delta, "two"


def solve_system(equations, variables):
    """Solve a linear system by Gauss-Jordan elimination.

    *equations* is a list of coefficient rows (each the same length as
    *variables* plus the right-hand side), e.g. ``[[2,1,5],[1,-1,1]]``.
    Returns ``(solution_list, kind)`` with kind ``"unique"``,
    ``"none"`` or ``"infinite"``.
    """
    if not equations:
        raise EquationError("Aucune équation")
    width = len(equations[0])
    if width < 2:
        raise EquationError("Équation invalide")
    n = width - 1
    for row in equations:
        if len(row) != width:
            raise EquationError("Toutes les équations doivent avoir le même nombre de coefficients")

    aug = [[complex(v) for v in row] for row in equations]
    pivot_row = 0
    pivots = []
    for col in range(n):
        if pivot_row >= len(aug):
            break
        best = max(range(pivot_row, len(aug)), key=lambda r: abs(aug[r][col]))
        if abs(aug[best][col]) < 1e-13:
            continue
        aug[pivot_row], aug[best] = aug[best], aug[pivot_row]
        div = aug[pivot_row][col]
        aug[pivot_row] = [v / div for v in aug[pivot_row]]
        for row in range(len(aug)):
            if row != pivot_row and aug[row][col] != 0:
                factor = aug[row][col]
                aug[row] = [aug[row][k] - factor * aug[pivot_row][k]
                            for k in range(width)]
        pivots.append(col)
        pivot_row += 1

    # detect contradictions:  0x + 0y = c  (c != 0)
    for row in aug:
        if all(abs(row[c]) < 1e-12 for c in range(n)) and abs(row[n]) > 1e-12:
            return None, "none"
    if len(pivots) < n:
        return None, "infinite"

    solution = [complex(0) for _ in range(n)]
    for i, col in enumerate(pivots):
        solution[col] = aug[i][n]
    return solution, "unique"


def solve_numerically(func, variable="x", start=0.0, end=10.0, samples=800):
    """Scan an interval for sign changes of ``func`` and refine each root.

    *func* is a callable taking a real value and returning a real value.
    Returns a list of roots.
    """
    if end <= start:
        raise EquationError("Intervalle invalide (borne droite <= borne gauche)")
    step = (end - start) / samples
    roots = []
    prev_x = start
    try:
        prev_y = func(prev_x)
    except Exception:
        prev_y = None
    for i in range(1, samples + 1):
        x = start + i * step
        try:
            y = func(x)
        except Exception:
            y = None
        if prev_y is not None and y is not None:
            if prev_y == 0:
                roots.append(prev_x)
            elif (prev_y < 0) != (y < 0):
                roots.append(_bisect(func, prev_x, x))
        prev_x, prev_y = x, y
    if prev_y == 0:
        roots.append(prev_x)
    # de-duplicate
    unique = []
    for r in roots:
        if not any(abs(r - u) < 1e-6 for u in unique):
            unique.append(r)
    return unique


def _bisect(func, lo, hi, iterations=100):
    f_lo = func(lo)
    for _ in range(iterations):
        mid = (lo + hi) / 2
        f_mid = func(mid)
        if abs(f_mid) < 1e-14:
            return mid
        if (f_lo < 0) != (f_mid < 0):
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2
