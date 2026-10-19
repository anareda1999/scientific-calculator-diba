"""
core/calculus.py
================
Advanced calculus tools:

* limits          lim f(x) as x -> a, a-, a+, +oo, -oo
* Taylor series  expansion of f around a point
* inequalities    solving f(x) > 0 / f(x) < 0 numerically
* differential equations  y' = f(x,y) and y'' = f(x,y,y') by Runge-Kutta 4
"""

import math

from .engine import ExprError, evaluate

__all__ = [
    "limit", "taylor_series", "format_taylor", "solve_inequality",
    "format_interval", "solve_ode",
]


# ══════════════════════════════════════════════════════════════
#  helpers
# ══════════════════════════════════════════════════════════════

def _make_func(ast, engine, var="x", extra=None):
    """Return a callable f(v) evaluating *ast* with var = v."""
    ctx = engine.context

    def fn(v):
        c = ctx.with_variable(var, complex(v))
        if extra:
            for name, value in extra.items():
                c = c.with_variable(name, complex(value))
        return evaluate(ast, c)
    return fn


def _finite(value):
    return (math.isfinite(value.real) and math.isfinite(value.imag))


# ══════════════════════════════════════════════════════════════
#  Limits
# ══════════════════════════════════════════════════════════════

def limit(ast, engine, var="x", point=0.0, direction=0):
    """Compute ``lim_{var -> point} f(var)``.

    *direction* : ``1`` right, ``-1`` left, ``0`` two-sided.
    *point* may be a number or the strings ``"inf"`` / ``"-inf"``.

    Returns ``(value, kind, note)``.
    """
    f = _make_func(ast, engine, var)

    # ── infinite limit ──
    low = str(point).strip().lower()
    if low in ("inf", "+inf", "infinity", "+infinity", "oo", "+oo"):
        return _limit_infinity(f, +1)
    if low in ("-inf", "-infinity", "-oo"):
        return _limit_infinity(f, -1)

    point = float(point)

    # ── 1. direct substitution (continuous case) ──
    try:
        value = f(point)
        if _finite(value):
            if value.imag == 0:
                return value, "direct", f"f({point:g}) = {value.real:g}"
            return value, "direct", f"f({point:g}) = {value.real:g} + {value.imag:g}i"
    except Exception:
        pass

    # ── 2. numeric approach ──
    directions = [direction] if direction else [1, -1]
    results = []
    for d in directions:
        results.append(_numeric_limit(f, point, d))

    if len(results) == 1:
        value, err = results[0]
        side = "a+" if direction > 0 else "a-"
        return value, "numeric", f"approche numerique par {side} (incertitude {err:.1e})"

    v1, e1 = results[0]
    v2, e2 = results[1]
    if abs(v1.real - v2.real) <= 1e-6 * max(1.0, abs(v1.real)):
        return v1, "numeric", (f"approche numerique des deux cotes "
                               f"(incertitude {max(e1, e2):.1e})")
    return v1, "discontinuous", ("les deux limites differentes : la fonction "
                                 "n'est pas continue en ce point")


def _numeric_limit(f, point, direction, h0=1e-1, hmin=1e-13):
    """Approximate a limit by shrinking the distance to the point.

    Detects both convergence to a finite value and divergence to
    +/- infinity (which is what happens at a vertical asymptote).
    """
    samples = []
    h = h0
    while h > hmin:
        try:
            v = f(point + direction * h)
        except Exception:
            h /= 10.0
            continue
        if not (_finite(v)):
            h /= 10.0
            continue
        samples.append((h, v))
        h /= 10.0

    if not samples:
        raise ExprError("Limite non definie en ce point")

    # ── convergence to a finite value ──
    if len(samples) >= 2:
        (_, v1), (_, v2) = samples[-2], samples[-1]
        err = abs(v2.real - v1.real)
        if err <= 1e-7 * max(1.0, abs(v2.real)):
            return v2, err

    # ── divergence : the magnitude grows as we approach the point ──
    magnitudes = [abs(v.real) for _, v in samples]
    growing = all(magnitudes[i + 1] > magnitudes[i] * 1.2
                  for i in range(len(magnitudes) - 1))
    if growing:
        last = samples[-1][1].real
        return complex(math.copysign(math.inf, last)), math.inf

    last_value = samples[-1][1]
    return last_value, abs(last_value.real)


def _limit_infinity(f, sign):
    """Limit when x -> +oo (sign = 1) or x -> -oo (sign = -1)."""
    h = 1e3
    samples = []
    for _ in range(14):
        try:
            v = f(sign * h)
        except Exception:
            h *= 10.0
            continue
        if not _finite(v):
            h *= 10.0
            continue
        samples.append((h, v.real))
        h *= 10.0

    if not samples:
        raise ExprError("Limite non definie")

    # converging to a finite value?
    if len(samples) >= 2:
        (_, a), (_, b) = samples[-2], samples[-1]
        if abs(b - a) <= 1e-6 * max(1.0, abs(b)):
            return complex(b), "infinity", f"limite finie = {b:g}"

    # diverging ?
    magnitudes = [abs(v) for _, v in samples]
    growing = all(magnitudes[i + 1] >= magnitudes[i] * 1.5
                  for i in range(len(magnitudes) - 1))
    last = samples[-1][1]
    if magnitudes[-1] > 1e10 and growing:
        return complex(last), "infinity", ("+inf" if last > 0 else "-inf")

    return complex(last), "infinity", f"comportement a l'infini : {last:.6g}"


# ══════════════════════════════════════════════════════════════
#  Taylor series
# ══════════════════════════════════════════════════════════════

def taylor_series(ast, engine, var="x", point=0.0, order=4, h=1e-4):
    """Taylor expansion of *ast* around *point*.

    Returns a list of ``(n, derivative, coefficient)`` tuples where
    *derivative* is f^(n)(point) and *coefficient* is derivative / n!.
    """
    if order < 0:
        raise ExprError("L'ordre doit etre positif ou nul")
    order = min(int(order), 12)

    fn = _make_func(ast, engine, var)
    result = []
    for k in range(order + 1):
        try:
            value = fn(point)
            deriv = value.real if _finite(value) else float("nan")
        except Exception:
            deriv = float("nan")
        coeff = deriv / math.factorial(k) if deriv == deriv else float("nan")
        result.append((k, deriv, coeff))

        def nxt(x, _fn=fn, _h=h):
            return (_fn(x + _h) - _fn(x - _h)) / (2.0 * _h)
        fn = nxt
    return result


def format_taylor(terms, var="x", point=0.0):
    """Build a readable Taylor polynomial string."""
    pieces = []
    for k, deriv, coeff in terms:
        if coeff != coeff:            # NaN
            continue
        if abs(coeff) < 1e-12 and k > 0:
            continue
        sign = " - " if coeff < 0 else (" + " if pieces else "")
        magnitude = abs(coeff)
        if k == 0:
            pieces.append(f"{magnitude:g}")
        else:
            power = f"({var} - {point:g})" if point else var
            if k == 1:
                body = power
            else:
                body = f"{power}^{k}"
            pieces.append(f"{sign}{magnitude:g}·{body}")
    if not pieces:
        return "0"
    return "".join(pieces)


# ══════════════════════════════════════════════════════════════
#  Inequalities
# ══════════════════════════════════════════════════════════════

def solve_inequality(ast, engine, var="x", lower=-10.0, upper=10.0,
                     sign=1, samples=4000, strict=True):
    """Solve ``sign * f(var) > 0`` (or ``>= 0``) on ``[lower, upper]``.

    *sign* is ``+1`` for ``f > 0`` and ``-1`` for ``f < 0``.
    Returns a list of ``(lo, hi)`` intervals (endpoints may be infinite).
    """
    lower = float(lower)
    upper = float(upper)
    if upper <= lower:
        raise ExprError("Intervalle invalide (borne droite <= borne gauche)")

    f = _make_func(ast, engine, var)

    # ── find the sign changes (roots) inside the interval ──
    step = (upper - lower) / samples
    roots = []
    prev_x = lower
    prev_v = None
    try:
        prev_v = f(prev_x)
    except Exception:
        prev_v = None
    x = lower + step
    while x <= upper + step:
        try:
            v = f(x)
        except Exception:
            v = None
        if prev_v is not None and v is not None and _finite(prev_v) and _finite(v):
            if abs(prev_v.real) < 1e-14:
                roots.append(prev_x)
            elif (prev_v.real < 0) != (v.real < 0):
                roots.append(_bisect(f, prev_x, x))
        prev_x, prev_v = x, v
        x += step

    # ── build the candidate intervals ──
    cuts = sorted(set(roots))
    edges = [-math.inf] + cuts + [math.inf]
    solution = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        test_lo = max(lo, lower)
        test_hi = min(hi, upper)
        if test_lo > test_hi:
            continue
        if math.isinf(lo) and math.isinf(hi):
            continue
        if math.isinf(lo):
            probe = test_hi - step
        elif math.isinf(hi):
            probe = test_lo + step
        else:
            probe = (lo + hi) / 2.0
        if probe <= test_lo or probe >= test_hi:
            continue
        try:
            value = f(probe)
        except Exception:
            continue
        if not _finite(value):
            continue
        product = sign * value.real
        holds = product > 0 if strict else product >= 0
        if holds:
            if solution and solution[-1][1] == lo:
                solution[-1] = (solution[-1][0], hi)
            else:
                solution.append((lo, hi))
    return solution


def _bisect(f, lo, hi, iterations=80):
    try:
        f_lo = f(lo).real
    except Exception:
        return lo
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        try:
            f_mid = f(mid).real
        except Exception:
            return mid
        if abs(f_mid) < 1e-14:
            return mid
        if (f_lo < 0) != (f_mid < 0):
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def format_interval(interval):
    """Format a single interval tuple as text."""
    lo, hi = interval
    if math.isinf(lo) and math.isinf(hi):
        return "R"
    left = "-inf" if math.isinf(lo) else f"{lo:.6g}"
    right = "+inf" if math.isinf(hi) else f"{hi:.6g}"
    if math.isinf(lo) and math.isinf(hi):
        return "R"
    return f"[ {left} ; {right} ]"


def format_solution(intervals):
    """Format the whole solution set."""
    if not intervals:
        return "∅ (aucune solution)"
    return "  ∪  ".join(format_interval(i) for i in intervals)


# ══════════════════════════════════════════════════════════════
#  Differential equations
# ══════════════════════════════════════════════════════════════

def solve_ode(rhs_ast, engine, var="x", x0=0.0, y0=1.0, x_end=10.0,
              steps=200, order=1, dy0=0.0):
    """Solve a differential equation with Runge-Kutta 4.

    *order* 1 : ``y'  = f(x, y)``
    *order* 2 : ``y'' = f(x, y, y')``

    Returns a list of ``(x, y)`` pairs.
    """
    x0 = float(x0)
    x_end = float(x_end)
    y0 = float(y0)
    steps = max(1, int(steps))
    if x_end == x0:
        raise ExprError("L'intervalle de resolution est vide")
    h = (x_end - x0) / steps

    if order == 1:
        ctx = engine.context

        def f(x, y):
            c = ctx.with_variable(var, complex(x)).with_variable("y", complex(y))
            return evaluate(rhs_ast, c).real

        return _rk4_1(f, x0, y0, x_end, steps)
    if order == 2:
        ctx = engine.context

        def f(x, y, yp):
            c = (ctx.with_variable(var, complex(x))
                    .with_variable("y", complex(y))
                    .with_variable("yp", complex(yp)))
            return evaluate(rhs_ast, c).real

        return _rk4_2(f, x0, y0, float(dy0), x_end, steps)
    raise ExprError("L'ordre de l'equation doit etre 1 ou 2")


def _rk4_1(f, x0, y0, x_end, steps):
    h = (x_end - x0) / steps
    x, y = x0, y0
    points = [(x, y)]
    for _ in range(steps):
        k1 = f(x, y)
        k2 = f(x + h / 2.0, y + h * k1 / 2.0)
        k3 = f(x + h / 2.0, y + h * k2 / 2.0)
        k4 = f(x + h, y + h * k3)
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        x = x + h
        points.append((x, y))
    return points


def _rk4_2(f, x0, y0, v0, x_end, steps):
    h = (x_end - x0) / steps
    x, u, v = x0, y0, v0
    points = [(x, u)]
    for _ in range(steps):
        k1u, k1v = v, f(x, u, v)
        k2u, k2v = (v + h * k1v / 2.0,
                     f(x + h / 2.0, u + h * k1u / 2.0, v + h * k1v / 2.0))
        k3u, k3v = (v + h * k2v / 2.0,
                     f(x + h / 2.0, u + h * k2u / 2.0, v + h * k2v / 2.0))
        k4u, k4v = (v + h * k3v,
                     f(x + h, u + h * k3u, v + h * k3v))
        u = u + h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6.0
        v = v + h * (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0
        x = x + h
        points.append((x, u))
    return points
