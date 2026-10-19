"""
core/engine.py
==============
Expression engine for the DIDA Scientific Calculator.

Pipeline:  text  ->  tokenize  ->  parse (AST)  ->  evaluate

Highlights
----------
* NO ``eval()`` / ``exec()`` anywhere - a hand written tokenizer and
  recursive-descent parser are used instead.
* Every value is a Python ``complex`` so imaginary numbers come for
  free (``sqrt(-1)`` -> ``1j``).
* Desmos-style syntax: implicit multiplication (``2x``, ``2sin(x)``,
  ``(x+1)(x-1)``), ``^`` and unicode ``x**2`` powers, ``sqrt`` sign.
* Meaningful, user facing error messages in French/English.
"""

import cmath
import math
import re

__all__ = [
    "ExprError", "Engine", "Context",
    "format_number", "format_real",
    "numeric_derivative", "numeric_integral",
]


class ExprError(Exception):
    """Any user facing expression problem (bad syntax, domain, ...)."""


# ══════════════════════════════════════════════════════════════
#  Tokenizer
# ══════════════════════════════════════════════════════════════

# Unicode characters users expect to type directly
_UNICODE = {
    "²": "**2", "³": "**3", "¹": "**1",
    "⁴": "**4", "⁵": "**5", "⁶": "**6",
    "⁷": "**7", "⁸": "**8", "⁹": "**9",
    "π": "pi", "×": "*", "÷": "/", "−": "-",
    "–": "-", "—": "-", "∞": "inf",
}

_NUM_RE = re.compile(r"(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")
_ID_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


def tokenize(text):
    """Split *text* into a list of ``(kind, value)`` tuples.

    Kinds: ``NUM``, ``ID``, ``OP``, ``LPAR``, ``RPAR``, ``COMMA``, ``END``.
    """
    tokens = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < n and text[i + 1].isdigit()):
            m = _NUM_RE.match(text, i)
            tokens.append(("NUM", m.group(0)))
            i = m.end()
            continue
        if ch.isalpha() or ch == "_":
            m = _ID_RE.match(text, i)
            tokens.append(("ID", m.group(0)))
            i = m.end()
            continue
        if text.startswith("**", i):
            tokens.append(("OP", "**"))
            i += 2
            continue
        if ch == "(":
            tokens.append(("LPAR", "("))
            i += 1
            continue
        if ch == ")":
            tokens.append(("RPAR", ")"))
            i += 1
            continue
        if ch == ",":
            tokens.append(("COMMA", ","))
            i += 1
            continue
        if ch in "*/%^+-":
            tokens.append(("OP", ch))
            i += 1
            continue
        if ch == "√":
            tokens.append(("OP", "√"))
            i += 1
            continue
        raise ExprError(f"Caractère inconnu : '{ch}'")
    tokens.append(("END", None))
    return tokens


# ══════════════════════════════════════════════════════════════
#  AST nodes
# ══════════════════════════════════════════════════════════════

class Node:
    __slots__ = ()


class Num(Node):
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value


class Var(Node):
    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name


class Unary(Node):
    __slots__ = ("op", "operand")

    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class Binary(Node):
    __slots__ = ("op", "left", "right")

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Call(Node):
    __slots__ = ("name", "args")

    def __init__(self, name, args):
        self.name = name
        self.args = args


# ══════════════════════════════════════════════════════════════
#  Parser  (recursive descent)
# ══════════════════════════════════════════════════════════════

class Parser:
    def __init__(self, tokens, function_names=()):
        self.tokens = tokens
        self.pos = 0
        self.function_names = set(function_names)

    # -- token helpers ------------------------------------------------
    def peek(self, offset=0):
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def advance(self):
        tok = self.peek()
        if tok[0] != "END":
            self.pos += 1
        return tok

    # -- grammar ------------------------------------------------------
    def parse(self):
        node = self.parse_expr()
        if self.peek()[0] != "END":
            raise ExprError(f"Token inattendu : '{self.peek()[1]}'")
        return node

    def parse_expr(self):                       # + -
        node = self.parse_term()
        while True:
            kind, val = self.peek()
            if kind == "OP" and val in ("+", "-"):
                self.advance()
                node = Binary(val, node, self.parse_term())
            else:
                return node

    def parse_term(self):                       # * / % and implicit *
        node = self.parse_unary()
        while True:
            kind, val = self.peek()
            if kind == "OP" and val in ("*", "/", "%"):
                self.advance()
                node = Binary(val, node, self.parse_unary())
            elif kind in ("NUM", "ID", "LPAR"):
                # implicit multiplication: 2x  3sin(x)  (x+1)(x-1)
                node = Binary("*", node, self.parse_unary())
            else:
                return node

    def parse_unary(self):                      # -x  +x  sqrt-sign
        kind, val = self.peek()
        if kind == "OP" and val in ("+", "-"):
            self.advance()
            return Unary(val, self.parse_unary())
        if kind == "OP" and val == "√":
            self.advance()
            return Call("sqrt", [self.parse_unary()])
        return self.parse_power()

    def parse_power(self):                      # right associative
        base = self.parse_primary()
        kind, val = self.peek()
        if kind == "OP" and val == "**":
            self.advance()
            return Binary("**", base, self.parse_unary())
        return base

    def parse_primary(self):
        kind, val = self.advance()
        if kind == "NUM":
            return Num(complex(float(val)))
        if kind == "ID":
            if self.peek()[0] == "LPAR" and val in self.function_names:
                self.advance()                       # consume '('
                args = []
                if self.peek()[0] != "RPAR":
                    while True:
                        args.append(self.parse_expr())
                        if self.peek()[0] == "COMMA":
                            self.advance()
                            continue
                        break
                if self.peek()[0] != "RPAR":
                    raise ExprError("Parenthèse fermante ')' manquante")
                self.advance()
                return Call(val, args)
            return Var(val)
        if kind == "LPAR":
            node = self.parse_expr()
            if self.peek()[0] != "RPAR":
                raise ExprError("Parenthèse fermante ')' manquante")
            self.advance()
            return node
        raise ExprError(f"Expression invalide près de '{val}'")


# ══════════════════════════════════════════════════════════════
#  Functions & constants
# ══════════════════════════════════════════════════════════════

def _needs_ctx(fn):
    fn.needs_ctx = True
    return fn


def _trig(cmath_fn, real_fn):
    @_needs_ctx
    def wrapper(value, ctx):
        if ctx.angle_mode == "deg" and value.imag == 0:
            return complex(real_fn(math.radians(value.real)), 0.0)
        return cmath_fn(value)
    return wrapper


def _inv_trig(cmath_fn):
    @_needs_ctx
    def wrapper(value, ctx):
        result = cmath_fn(value)
        if ctx.angle_mode == "deg":
            return complex(math.degrees(result.real), result.imag)
        return result
    return wrapper


def _real_only(fn):
    @_needs_ctx
    def wrapper(value, ctx):
        if value.imag != 0:
            raise ExprError("Cette fonction n'accepte que les nombres réels")
        return complex(fn(value.real))
    return wrapper


def _sign(value):
    if value.imag != 0:
        return complex(abs(value.real) / abs(value) if value else 0,
                       value.imag / abs(value) if value else 0)
    return complex((value.real > 0) - (value.real < 0))


def _norm(value):
    """Normalise a complex number so a zero imaginary part is always +0.0.

    Without this, ``-complex(1)`` yields ``(-1-0j)`` and ``cmath.sqrt``
    then takes the *negative* real axis and returns ``-1j`` instead of ``1j``.
    """
    if isinstance(value, complex):
        if value.imag == 0:
            return complex(value.real, 0.0)
        return value
    return complex(value, 0.0)


def _cmod(a, b):
    """Modulo for complex values (Python's % only works on reals)."""
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a - b * math.floor((a / b).real)


def _cmin(*args):
    """min() for complex values (ordered by real then imaginary part)."""
    if not args:
        raise ValueError("min() requires at least one argument")
    return min(args, key=lambda v: (v.real, v.imag))


def _cmax(*args):
    """max() for complex values (ordered by real then imaginary part)."""
    if not args:
        raise ValueError("max() requires at least one argument")
    return max(args, key=lambda v: (v.real, v.imag))


DEFAULT_FUNCTIONS = {
    # trigonometry
    "sin": _trig(cmath.sin, math.sin),
    "cos": _trig(cmath.cos, math.cos),
    "tan": _trig(cmath.tan, math.tan),
    "sec": _trig(lambda v: 1 / cmath.cos(v), lambda v: 1 / math.cos(v)),
    "csc": _trig(lambda v: 1 / cmath.sin(v), lambda v: 1 / math.sin(v)),
    "cot": _trig(lambda v: 1 / cmath.tan(v), lambda v: 1 / math.tan(v)),
    "asin": _inv_trig(cmath.asin),
    "acos": _inv_trig(cmath.acos),
    "atan": _inv_trig(cmath.atan),
    "arcsin": _inv_trig(cmath.asin),
    "arccos": _inv_trig(cmath.acos),
    "arctan": _inv_trig(cmath.atan),
    "sinh": cmath.sinh,
    "cosh": cmath.cosh,
    "tanh": cmath.tanh,
    # exponential / logarithmic
    "exp": cmath.exp,
    "log": cmath.log10,
    "log10": cmath.log10,
    "ln": cmath.log,
    "sqrt": cmath.sqrt,
    "cbrt": lambda v: (complex(math.copysign(abs(v.real) ** (1.0 / 3.0), v.real))
                        if v.imag == 0 else cmath.exp(cmath.log(v) / 3)),
    # misc
    "abs": abs,
    "floor": _real_only(math.floor),
    "ceil": _real_only(math.ceil),
    "round": _real_only(round),
    "sign": _sign,
    "min": _cmin,
    "max": _cmax,
    "mod": _cmod,
    "gcd": math.gcd,
    "lcm": math.lcm,
    "re": lambda v: complex(v.real),
    "im": lambda v: complex(v.imag),
    "conj": lambda v: complex(v.conjugate()),
    "arg": lambda v: complex(cmath.phase(v)),
}

# Physical / mathematical constants (SI)
DEFAULT_CONSTANTS = {
    "pi": complex(math.pi),
    "π": complex(math.pi),
    "e": complex(math.e),
    "phi": complex((1 + math.sqrt(5)) / 2),
    "tau": complex(2 * math.pi),
    "c": complex(299792458.0),          # speed of light  (m/s)
    "g": complex(9.80665),              # gravity         (m/s^2)
    "h": complex(6.62607015e-34),       # Planck          (J*s)
    "hbar": complex(1.054571817e-34),   # reduced Planck
    "k": complex(1.380649e-23),         # Boltzmann       (J/K)
    "na": complex(6.02214076e23),       # Avogadro        (1/mol)
    "r": complex(8.314462618),          # gas constant    (J/(mol*K))
    "sigma": complex(5.670374419e-8),   # Stefan-Boltzmann
    "eps0": complex(8.8541878128e-12),  # vacuum permittivity
    "mu0": complex(1.25663706212e-6),   # vacuum permeability
    "g0": complex(9.80665),
    "inf": complex(math.inf),
}


# ══════════════════════════════════════════════════════════════
#  Context & evaluation
# ══════════════════════════════════════════════════════════════

class Context:
    """Variables, constants, functions and angle mode used while evaluating."""

    def __init__(self, functions=None, constants=None, variables=None,
                 angle_mode="rad"):
        self.functions = dict(DEFAULT_FUNCTIONS)
        if functions:
            self.functions.update(functions)
        self.constants = dict(DEFAULT_CONSTANTS)
        if constants:
            self.constants.update(constants)
        self.variables = dict(variables or {})
        self.angle_mode = angle_mode

    def copy(self, **overrides):
        ctx = Context(self.functions, self.constants, self.variables,
                      self.angle_mode)
        for key, val in overrides.items():
            setattr(ctx, key, val)
        return ctx

    def with_variable(self, name, value):
        variables = dict(self.variables)
        variables[name] = value
        return Context(self.functions, self.constants, variables,
                       self.angle_mode)

    def set(self, name, value):
        self.variables[name] = value


def evaluate(node, ctx):
    """Evaluate an AST *node* against *ctx* and return a ``complex``."""
    return _norm(_evaluate(node, ctx))


def _evaluate(node, ctx):
    if isinstance(node, Num):
        return node.value

    if isinstance(node, Var):
        name = node.name
        if name in ctx.variables:
            return ctx.variables[name]
        if name in ctx.constants:
            return ctx.constants[name]
        low = name.lower()
        if low in ctx.variables:
            return ctx.variables[low]
        if low in ctx.constants:
            return ctx.constants[low]
        raise ExprError(f"Variable inconnue : '{name}'")

    if isinstance(node, Unary):
        value = evaluate(node.operand, ctx)
        return -value if node.op == "-" else +value

    if isinstance(node, Binary):
        a = evaluate(node.left, ctx)
        b = evaluate(node.right, ctx)
        op = node.op
        try:
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if op == "/":
                if b == 0:
                    raise ExprError("Division par zéro")
                return a / b
            if op == "%":
                if b == 0:
                    raise ExprError("Division par zéro")
                return _cmod(a, b)
            if op == "**":
                return a ** b
        except ExprError:
            raise
        except ZeroDivisionError:
            raise ExprError("Division par zéro")
        except Exception as exc:
            raise ExprError(f"Erreur de calcul : {exc}")
        raise ExprError(f"Opérateur inconnu : '{op}'")

    if isinstance(node, Call):
        fn = ctx.functions.get(node.name) or ctx.functions.get(node.name.lower())
        if fn is None:
            raise ExprError(f"Fonction inconnue : '{node.name}'")
        args = [evaluate(arg, ctx) for arg in node.args]
        try:
            if getattr(fn, "needs_ctx", False):
                return fn(*args, ctx)
            return fn(*args)
        except ExprError:
            raise
        except ZeroDivisionError:
            raise ExprError("Division par zéro")
        except ValueError as exc:
            raise ExprError(f"Erreur de domaine : {exc}")
        except OverflowError:
            raise ExprError("Dépassement de capacité")
        except Exception as exc:
            raise ExprError(f"Erreur : {exc}")

    raise ExprError("Expression illisible")


# ══════════════════════════════════════════════════════════════
#  Number formatting
# ══════════════════════════════════════════════════════════════

def format_real(value, precision=10):
    """Format a real number nicely for display."""
    if value != value:                       # NaN
        return "indéfini"
    if value in (math.inf, -math.inf):
        return "∞" if value > 0 else "-∞"
    if value == 0:
        return "0"
    magnitude = abs(value)
    if magnitude >= 1e12 or magnitude < 1e-9:
        return f"{value:.{max(precision - 5, 3)}e}"
    if abs(value - round(value)) < 1e-12 * max(1.0, magnitude):
        return str(int(round(value)))
    return f"{value:.{precision}g}"


def format_number(value, precision=10):
    """Format a complex number, hiding a zero imaginary part."""
    if isinstance(value, complex):
        if abs(value.imag) < 1e-12 * max(1.0, abs(value.real)):
            return format_real(value.real, precision)
        real = format_real(value.real, precision)
        imag = format_real(abs(value.imag), precision)
        sign = "+" if value.imag >= 0 else "-"
        return f"{real} {sign} {imag}i"
    return format_real(value, precision)


# ══════════════════════════════════════════════════════════════
#  Engine - the public façade
# ══════════════════════════════════════════════════════════════

class Engine:
    """Parse once, evaluate many times (fast graphing)."""

    def __init__(self, angle_mode="rad"):
        self.angle_mode = angle_mode
        self.context = Context(angle_mode=angle_mode)
        self._cache = {}

    # -- configuration -------------------------------------------------
    def set_angle_mode(self, mode):
        self.angle_mode = mode
        self.context.angle_mode = mode

    def set_variable(self, name, value):
        self.context.set(name, value)
        self._cache.clear()

    def get_variable(self, name):
        return self.context.variables.get(name)

    def add_constant(self, name, value):
        self.context.constants[name] = value
        self._cache.clear()

    # -- parsing -------------------------------------------------------
    def parse(self, text):
        """Parse *text* into an AST (raises :class:`ExprError`)."""
        if text is None:
            raise ExprError("Aucune expression")
        cleaned = text
        for uni, rep in _UNICODE.items():
            cleaned = cleaned.replace(uni, rep)
        cleaned = cleaned.replace("^", "**")
        if not cleaned.strip():
            raise ExprError("Aucune expression")
        tokens = tokenize(cleaned)
        parser = Parser(tokens, self.context.functions.keys())
        return parser.parse()

    def evaluate_text(self, text):
        """Parse and evaluate *text* in one go."""
        return evaluate(self.parse(text), self.context)

    def evaluate(self, ast):
        return evaluate(ast, self.context)

    # -- calculus ------------------------------------------------------
    def derivative(self, ast, variable="x", point=0.0, h=1e-5):
        """Central-difference derivative of *ast* at *point*."""
        def f(v):
            ctx = self.context.with_variable(variable, complex(v))
            return evaluate(ast, ctx)
        try:
            return (f(point + h) - f(point - h)) / (2 * h)
        except ExprError:
            raise
        except Exception as exc:
            raise ExprError(f"Dérivée impossible : {exc}")

    def integral(self, ast, variable="x", lower=0.0, upper=1.0, steps=2000):
        """Simpson's rule integral of *ast* between *lower* and *upper*."""
        if steps % 2:
            steps += 1
        if steps < 2:
            steps = 2
        h = (upper - lower) / steps

        def f(v):
            ctx = self.context.with_variable(variable, complex(v))
            return evaluate(ast, ctx)

        try:
            total = f(lower) + f(upper)
            for i in range(1, steps):
                weight = 4 if i % 2 else 2
                total += weight * f(lower + i * h)
            return total * h / 3
        except ExprError:
            raise
        except Exception as exc:
            raise ExprError(f"Intégrale impossible : {exc}")

    def solve_newton(self, ast, variable="x", start=0.0, iterations=80):
        """Find a root of ``ast = 0`` with Newton's method."""
        def f(v):
            ctx = self.context.with_variable(variable, complex(v))
            return evaluate(ast, ctx)
        x = complex(start)
        h = 1e-6
        for _ in range(iterations):
            fx = f(x)
            if abs(fx) < 1e-12:
                return x
            d = (f(x + h) - f(x - h)) / (2 * h)
            if d == 0:
                break
            x = x - fx / d
        if abs(f(x)) < 1e-6:
            return x
        raise ExprError("Aucune racine trouvée (essuyez une autre valeur de départ)")
