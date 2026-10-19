"""
tests/test_calculus.py
=====================
Unit tests for the advanced calculus tools: limits, Taylor expansion,
inequality solving and differential equations.

Run with:  python tests/test_calculus.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import Engine
from core import calculus

PASSED = 0
FAILED = 0


def check(label, got, expected, tol=1e-6):
    global PASSED, FAILED
    if isinstance(got, complex):
        got = got.real if abs(got.imag) < 1e-9 else got
    if isinstance(got, (int, float)) and isinstance(expected, (int, float)):
        ok = abs(got - expected) <= tol * max(1.0, abs(expected))
    else:
        ok = got == expected
    if ok:
        PASSED += 1
        print(f"  PASS  {label}")
    else:
        FAILED += 1
        print(f"  FAIL  {label}: got {got!r}, expected {expected!r}")


def section(title):
    print(f"\n{title}")
    print("-" * len(title))


def main():
    eng = Engine(angle_mode="rad")

    section("Limits")
    ast = eng.parse("x^2+1")
    value, kind, _ = calculus.limit(ast, eng, "x", 3)
    check("lim(x^2+1) as x->3", value.real, 10)

    ast = eng.parse("x")
    value, kind, _ = calculus.limit(ast, eng, "x", 0)
    check("lim(x) as x->0", value.real, 0)
    check("lim(x) direct substitution", kind, "direct")

    ast = eng.parse("(x^2-1)/(x-1)")
    value, kind, _ = calculus.limit(ast, eng, "x", 1)
    check("lim (x^2-1)/(x-1) as x->1", value.real, 2)

    ast = eng.parse("sin(x)/x")
    value, kind, _ = calculus.limit(ast, eng, "x", 0)
    check("lim sin(x)/x as x->0", value.real, 1, tol=1e-4)

    ast = eng.parse("1/x")
    value, kind, _ = calculus.limit(ast, eng, "x", 0, direction=1)
    check("lim 1/x as x->0+", value.real > 1e6, True)

    ast = eng.parse("1/x")
    value, kind, _ = calculus.limit(ast, eng, "x", 0, direction=-1)
    check("lim 1/x as x->0-", value.real < -1e6, True)

    ast = eng.parse("x^2")
    value, kind, _ = calculus.limit(ast, eng, "x", "inf")
    check("lim x^2 as x->+inf is +inf", value.real > 1e6, True)

    ast = eng.parse("1/x")
    value, kind, _ = calculus.limit(ast, eng, "x", "inf")
    check("lim 1/x as x->+inf = 0", value.real, 0, tol=1e-6)

    ast = eng.parse("exp(x)")
    value, kind, _ = calculus.limit(ast, eng, "x", "-inf")
    check("lim exp(x) as x->-inf = 0", value.real, 0, tol=1e-6)

    section("Taylor series")
    ast = eng.parse("x^2")
    terms = calculus.taylor_series(ast, eng, "x", 0, 4)
    check("f(0) for x^2", terms[0][1], 0)
    check("f'(0) for x^2", terms[1][1], 0, tol=1e-4)
    check("f''(0) for x^2", terms[2][1], 2, tol=1e-3)
    check("f'''(0) for x^2", terms[3][1], 0, tol=1e-3)

    ast = eng.parse("exp(x)")
    terms = calculus.taylor_series(ast, eng, "x", 0, 3)
    check("exp: f(0)=1", terms[0][1], 1)
    check("exp: f'(0)=1", terms[1][1], 1, tol=1e-4)
    check("exp: f''(0)=1", terms[2][1], 1, tol=1e-3)
    check("exp: f'''(0)=1", terms[3][1], 1, tol=1e-3)

    poly = calculus.format_taylor(terms, "x", 0)
    check("exp polynomial has 1 + x", "1" in poly and "x" in poly, True)

    section("Inequalities")
    ast = eng.parse("x^2 - 4")
    intervals = calculus.solve_inequality(ast, eng, "x", -10, 10, sign=1, strict=True)
    check("x^2-4 > 0 has 2 intervals", len(intervals), 2)
    check("x^2-4 > 0 first upper bound", intervals[0][1], -2, tol=1e-4)
    check("x^2-4 > 0 second lower bound", intervals[1][0], 2, tol=1e-4)

    ast = eng.parse("x^2 - 4")
    intervals = calculus.solve_inequality(ast, eng, "x", -10, 10, sign=-1, strict=True)
    check("x^2-4 < 0 has 1 interval", len(intervals), 1)
    check("x^2-4 < 0 lower bound", intervals[0][0], -2, tol=1e-4)
    check("x^2-4 < 0 upper bound", intervals[0][1], 2, tol=1e-4)

    ast = eng.parse("x + 1")
    intervals = calculus.solve_inequality(ast, eng, "x", -10, 10, sign=1, strict=True)
    check("x+1 > 0 starts at -1", intervals[0][0], -1, tol=1e-4)

    ast = eng.parse("x^2 + 1")
    intervals = calculus.solve_inequality(ast, eng, "x", -10, 10, sign=-1, strict=True)
    check("x^2+1 < 0 has no solution", len(intervals), 0)

    ast = eng.parse("x^2")
    intervals = calculus.solve_inequality(ast, eng, "x", -10, 10, sign=1, strict=False)
    check("x^2 >= 0 covers everything", len(intervals), 1)

    section("Differential equations")
    # y' = y  ->  y = e^x,  y(0)=1
    ast = eng.parse("y")
    points = calculus.solve_ode(ast, eng, "x", x0=0, y0=1, x_end=1, steps=200)
    check("y'=y  number of points", len(points), 201)
    check("y'=y  y(1) = e", points[-1][1], math.e, tol=1e-5)

    # y' = 2x  ->  y = x^2,  y(0)=0
    ast = eng.parse("2*x")
    points = calculus.solve_ode(ast, eng, "x", x0=0, y0=0, x_end=3, steps=200)
    check("y'=2x  y(3) = 9", points[-1][1], 9, tol=1e-5)

    # y'' = -y  ->  y = cos(x),  y(0)=1, y'(0)=0
    ast = eng.parse("-y")
    points = calculus.solve_ode(ast, eng, "x", x0=0, y0=1, x_end=math.pi,
                                steps=400, order=2, dy0=0)
    check("y''=-y  y(pi) = -1", points[-1][1], -1, tol=1e-4)

    # y'' = 0  ->  y constant
    ast = eng.parse("0")
    points = calculus.solve_ode(ast, eng, "x", x0=0, y0=5, x_end=2, steps=50,
                                order=2, dy0=0)
    check("y''=0 keeps y constant", points[-1][1], 5, tol=1e-9)

    print("\n" + "=" * 46)
    print(f"  PASSED: {PASSED}    FAILED: {FAILED}")
    print("=" * 46)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
