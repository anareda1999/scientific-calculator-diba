"""
tests/test_engine.py
====================
Unit tests for the expression engine and the supporting modules.

Run with:  python -m tests.test_engine      (from the project folder)
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import Engine, ExprError, format_number
from core import matrices, equations, statistics, units

PASSED = 0
FAILED = 0


def check(label, got, expected, tol=1e-9):
    global PASSED, FAILED
    # unwrap complex numbers whose imaginary part is zero
    if isinstance(got, complex) and abs(got.imag) < 1e-12:
        got = got.real
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

    section("Basic arithmetic")
    check("2+3", eng.evaluate_text("2+3"), 5)
    check("2+3*4", eng.evaluate_text("2+3*4"), 14)
    check("(2+3)*4", eng.evaluate_text("(2+3)*4"), 20)
    check("2^10", eng.evaluate_text("2^10"), 1024)
    check("2**10", eng.evaluate_text("2**10"), 1024)
    check("x²  (unicode)", eng.evaluate_text("3\u00b2"), 9)
    check("7/2", eng.evaluate_text("7/2"), 3.5)
    check("-5+3", eng.evaluate_text("-5+3"), -2)
    check("2**3**2 (right assoc)", eng.evaluate_text("2**3**2"), 512)

    section("Implicit multiplication (Desmos style)")
    eng.set_variable("x", complex(4))
    check("2x at x=4", eng.evaluate_text("2x"), 8)
    check("3x+2 at x=4", eng.evaluate_text("3x+2"), 14)
    check("(x+1)(x-1) at x=4", eng.evaluate_text("(x+1)(x-1)"), 15)
    check("x^2 at x=4", eng.evaluate_text("x^2"), 16)
    check("x³ at x=2", eng.evaluate_text("2**3"), 8)
    eng.set_variable("x", complex(0))
    check("2sin(x) at x=0", eng.evaluate_text("2sin(x)"), 0)
    eng.set_variable("x", complex(math.pi / 2))
    check("2sin(x) at x=pi/2", eng.evaluate_text("2sin(x)"), 2)

    section("Functions")
    check("sqrt(16)", eng.evaluate_text("sqrt(16)"), 4)
    check("ln(e)", eng.evaluate_text("ln(e)"), 1)
    check("log(1000)", eng.evaluate_text("log(1000)"), 3)
    check("abs(-7)", eng.evaluate_text("abs(-7)"), 7)
    check("round(3.7)", eng.evaluate_text("round(3.7)"), 4)
    check("floor(3.9)", eng.evaluate_text("floor(3.9)"), 3)
    check("ceil(3.1)", eng.evaluate_text("ceil(3.1)"), 4)
    check("min(3,1,2)", eng.evaluate_text("min(3,1,2)"), 1)
    check("max(3,1,2)", eng.evaluate_text("max(3,1,2)"), 3)
    check("mod(10,3)", eng.evaluate_text("mod(10,3)"), 1)

    section("Angle modes")
    rad = Engine(angle_mode="rad")
    deg = Engine(angle_mode="deg")
    check("sin(0) rad", rad.evaluate_text("sin(0)"), 0)
    check("sin(30) deg", deg.evaluate_text("sin(30)"), 0.5)
    check("cos(60) deg", deg.evaluate_text("cos(60)"), 0.5)
    check("tan(45) deg", deg.evaluate_text("tan(45)"), 1)
    check("cot(45) deg", deg.evaluate_text("cot(45)"), 1)
    check("asin(0.5) deg", deg.evaluate_text("asin(0.5)"), 30)
    check("atan(1) deg", deg.evaluate_text("atan(1)"), 45)
    check("atan(1) rad", rad.evaluate_text("atan(1)"), math.pi / 4)

    section("Complex numbers")
    check("sqrt(-1) -> i", eng.evaluate_text("sqrt(-1)").imag, 1)
    check("sqrt(-4) -> 2i", eng.evaluate_text("sqrt(-4)").imag, 2)
    check("i*i = -1", (eng.evaluate_text("sqrt(-1)") ** 2).real, -1)
    check("cbrt(-8) = -2", eng.evaluate_text("cbrt(-8)").real, -2)
    check("(-8)^(1/3) principal branch", eng.evaluate_text("(-8)**(1/3)").real, 1)
    check("format 1+2i", format_number(complex(1, 2)), "1 + 2i")
    check("format 3+0j", format_number(complex(3, 0)), "3")

    section("Constants")
    check("pi", eng.evaluate_text("pi"), math.pi)
    check("e", eng.evaluate_text("e"), math.e)
    check("c (light speed)", eng.evaluate_text("c"), 299792458.0)
    check("g (gravity)", eng.evaluate_text("g"), 9.80665)
    check("NA (Avogadro)", eng.evaluate_text("na"), 6.02214076e23)

    section("Variables and Ans")
    eng.set_variable("a", complex(4))
    check("a*2", eng.evaluate_text("a*2"), 8)
    eng.set_variable("a", complex(5))
    check("a re-set", eng.evaluate_text("a"), 5)

    section("Error handling")
    for bad, label in [("2+", "incomplete expression"),
                       ("(1+2", "unclosed parenthesis"),
                       ("1/0", "division by zero"),
                       ("unknownvar", "unknown variable"),
                       ("nosuchfunc(2)", "unknown function"),
                       ("2 $ 3", "illegal character")]:
        try:
            eng.evaluate_text(bad)
            check(label, "no error raised", "ExprError")
        except ExprError:
            check(label, "ExprError", "ExprError")

    section("Derivative & integral")
    ast = eng.parse("x^2")
    check("d/dx x^2 at 3", eng.derivative(ast, "x", 3), 6, tol=1e-5)
    ast = eng.parse("x^3")
    check("d/dx x^3 at 2", eng.derivative(ast, "x", 2), 12, tol=1e-4)
    ast = eng.parse("x^2")
    check("integral x^2 0..3", eng.integral(ast, "x", 0, 3), 9, tol=1e-6)
    ast = eng.parse("sin(x)")
    check("integral sin 0..pi", eng.integral(ast, "x", 0, math.pi), 2, tol=1e-6)

    section("Newton root finder")
    ast = eng.parse("x^2 - 4")
    root = eng.solve_newton(ast, "x", 1)
    check("root of x^2-4", root.real, 2, tol=1e-6)
    ast = eng.parse("x^2 - 2")
    root = eng.solve_newton(ast, "x", 1)
    check("root of x^2-2", root.real, math.sqrt(2), tol=1e-6)

    section("Equations")
    x, kind = equations.solve_linear(2, -4)
    check("2x-4=0", x.real, 2)
    check("linear kind", kind, "unique")
    x, kind = equations.solve_linear(0, 5)
    check("0x+5=0 none", kind, "none")
    x, kind = equations.solve_linear(0, 0)
    check("0x+0=0 infinite", kind, "infinite")
    roots, delta, kind = equations.solve_quadratic(1, -3, 2)
    check("x^2-3x+2 roots", sorted(r.real for r in roots), [1, 2])
    roots, delta, kind = equations.solve_quadratic(1, 2, 1)
    check("x^2+2x+1 double", kind, "double")
    roots, delta, kind = equations.solve_quadratic(1, 0, 1)
    check("x^2+1 gives complex roots", kind, "two")
    check("x^2+1 roots are imaginary", abs(roots[0].imag), 1)

    section("Linear systems")
    sol, kind = equations.solve_system([[2, 1, 5], [1, -1, 1]], 2)
    check("system 2x2 kind", kind, "unique")
    check("system 2x2 x", sol[0].real, 2)
    check("system 2x2 y", sol[1].real, 1)
    sol, kind = equations.solve_system([[1, 1, 2], [2, 2, 4]], 2)
    check("dependent system infinite", kind, "infinite")
    sol, kind = equations.solve_system([[1, 1, 2], [1, 1, 3]], 2)
    check("contradictory system none", kind, "none")

    section("Matrices")
    m2 = [[1, 2], [3, 4]]
    check("det 2x2", matrices.det(m2).real, -2)
    check("det 3x3", matrices.det([[6, 1, 1], [4, -2, 5], [2, 8, 7]]).real, -306)
    inv = matrices.inverse(m2)
    check("inverse check", matrices.matmul(m2, inv)[0][0].real, 1)
    check("transpose", matrices.transpose(m2)[0][1], 3)
    check("trace", matrices.trace(m2), 5)
    check("rank singular", matrices.rank([[1, 2], [2, 4]]), 1)
    check("matmul", matrices.matmul(m2, m2)[0][0], 7)
    check("matpow", matrices.matpow(m2, 2)[0][0], 7)

    section("Statistics")
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    check("mean", statistics.mean(data), 5)
    check("median", statistics.median(data), 4.5)
    check("mode", statistics.mode(data), 4)
    check("stdev", statistics.stdev(data), 2, tol=1e-9)
    check("min", statistics.minimum(data), 2)
    check("max", statistics.maximum(data), 9)
    check("sum", statistics.total(data), 40)
    check("range", statistics.range_of(data), 7)
    slope, intercept, r2 = statistics.linear_regression([1, 2, 3], [2, 4, 6])
    check("regression slope", slope, 2)
    check("regression intercept", intercept, 0)
    check("regression r2", r2, 1)

    section("Units")
    check("1 km -> m", units.convert("Distance", "en", 1, "Kilometer (km)", "Meter (m)"), 1000)
    check("1 kg -> g", units.convert("Weight", "en", 1, "Kilogram (kg)", "Gram (g)"), 1000)
    check("1 m -> cm", units.convert("Distance", "fr", 1, "M\u00e8tre (m)", "Centim\u00e8tre (cm)"), 100)

    print("\n" + "=" * 46)
    print(f"  PASSED: {PASSED}    FAILED: {FAILED}")
    print("=" * 46)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
