# 🔢 Scientific Calculator v2.0 — Sweet & Modern Desktop App

A professional, multilingual scientific calculator built with **Python + tkinter**, packaged as a standalone Windows `.exe` with **PyInstaller**.

**Copyright © reda anagou**

---

## ✨ What's new in v2.0

### 🧠 Real expression engine (no more `eval()`)
A hand-written **tokenizer + recursive-descent parser** replaces the old `eval()` calls:

- **No arbitrary code execution** — the parser only understands maths
- **Real error messages** — *"Division par zéro"*, *"Variable inconnue : 'x'"*, *"Parenthèse fermante manquante"*
- **Complex numbers** — `sqrt(-16)` → `0 + 4i`, `cbrt(-8)` → `-2`
- **Desmos-style syntax** — implicit multiplication: `2x`, `3x+2`, `2sin(x)`, `(x+1)(x-1)`
- **Unicode input** — `x²`, `x³`, `√`, `π`, `×`, `÷`, `−` all work
- **Right-associative powers** — `2**3**2` = 512

### ⚡ Performance fix
The graphing canvas no longer redraws on every mouse-move — only the coordinate readout updates. Curves are parsed **once** into an AST and re-used for every sampled point.

---

## 📦 Features

### 🧮 Scientific Calculator
- Full keypad with memory keys (`MC`, `MR`, `M+`, `M-`)
- **Ans key** — reuse the last result
- **History tape** — click any past calculation to reuse it
- **Constants library** — `π` `e` `c` (light speed) `g` (gravity) `h` (Planck) `k` (Boltzmann) `NA` (Avogadro) `R` (gas constant)
- `DEG` / `RAD` angle mode (affects trig **and** inverse trig)
- Keyboard support: numbers, operators, `Enter`, `Backspace`, `Escape`

### ⚗️ Scientific Formulas
9 ready-to-use formulas, each with inputs and instant calculation:

| Formula | Equation |
|---------|----------|
| Quadratic Formula | `x = (-b ± √(b²-4ac)) / 2a` |
| Area of Circle | `π × r²` |
| Area of Rectangle | `length × width` |
| Area of Triangle | `(base × height) / 2` |
| Volume of Sphere | `(4/3) × π × r³` |
| Volume of Cylinder | `π × r² × h` |
| Ohm's Law | `V = I × R` |
| Force | `F = m × a` |
| Kinetic Energy | `KE = (1/2) × m × v²` |

### 📐 Equation Solver — 5 tabs
1. **1st degree** — `ax + b = 0`
2. **2nd degree** — `ax² + bx + c = 0` with discriminant `Δ`
3. **Expression** — evaluate any expression in `x`
4. **Find roots** — numerical root finder over an interval
5. **System** — solve 2×2 and 3×3 linear systems (Gauss-Jordan)

Coefficients accept scientific functions: `sin`, `cos`, `tan`, `cot`, `log`, `ln`, `exp`, `sqrt`, `pi`, `e`.

### 📈 Graphing Calculator (Desmos-style)
- **Live plotting** — curves update instantly as you type
- **Multiple expressions**, each with its own colour and a ✕ delete button
- **Draggable sliders** — write `a = 3`, then drag it on the graph or in the panel
- **Pan & zoom** — drag to pan, scroll wheel to zoom, plus zoom buttons
- **Coordinate readout** under the mouse cursor
- **Every expression type:**

| Type | Example | Result |
|------|---------|--------|
| Function | `y = x^2` | parabola |
| Function | `y = sin(x)` | sine wave |
| Implicit curve | `x^2 + y^2 = 25` | circle |
| Vertical line | `x = 5` | straight line |
| Point | `(3, 4)` | single point |
| Slider | `a = 3` | draggable parameter |

- **30+ functions:** `sin cos tan sec csc cot asin acos atan sinh cosh tanh log ln exp sqrt cbrt abs floor ceil sign round min max mod gcd lcm`
- **Constants:** `pi` `e` `phi` `tau` `c` `g` `h` `hbar` `k` `na` `r` `sigma` `eps0` `mu0`

### 🔢 Matrix Calculator
2×2, 3×3 and 4×4 matrices with: **determinant**, **inverse**, **transpose**, **trace**, **rank**, **A × B**, **A + B**, **Aⁿ**

### ∫ Calculus
- **Derivative** — numeric (central difference) at any point
- **Integral** — Simpson's rule between two bounds
- **Root finder** — Newton + bisection

### 🔬 Advanced Analysis (new module)
A dedicated window with four tabs:

| Tab | What it does |
|-----|--------------|
| **Limits** | `lim f(x)` as `x → a`, `a-`, `a+`, `+∞`, `-∞` — direct substitution, numeric approach with uncertainty, and divergence detection (±∞) |
| **Taylor** | Series expansion of `f` around any point, up to order 12 — shows every derivative and the resulting polynomial |
| **Inequalities** | Solves `f(x) > 0`, `≥ 0`, `< 0`, `≤ 0` — returns the solution as a union of intervals |
| **Differential equations** | `y' = f(x,y)` and `y'' = f(x,y,y')` solved with Runge-Kutta 4 — initial conditions, variable range, result table |

**Examples:**
```
Limit     : (x^2-1)/(x-1)  as x→1        =  2
Limit     : 1/x            as x→0+        =  +∞
Taylor    : exp(x)  at 0, order 4        =  1 + x + 0.5x² + 0.1667x³ + 0.0376x⁴
Inequality: x^2-4 > 0                    =  [ -∞ ; -2 ] ∪ [ 2 ; +∞ ]
ODE       : y' = y,  y(0)=1,  x∈[0,1]   →  y(1) = 2.718281828
```

### 📊 Statistics
`mean` `median` `mode` `stdev` `variance` `min` `max` `sum` `range` `count` `percentile` + **linear regression** (slope, intercept, R², correlation)

### 🔄 Unit Converter
Five categories, auto-converting as you type:

| Category | Units |
|----------|-------|
| **Weight** | kg, g, mg, tonne, lb, oz |
| **Currency** | USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, DZD, MAD, TND |
| **Volume** | L, mL, m³, US gal, qt, pt, cup, fl oz |
| **Area** | m², cm², mm², km², ft², in², hectare, acre |
| **Distance** | km, m, cm, mm, mile, yard, foot, inch, nautical mile |

### 🌍 Three Languages
Switch instantly from the top bar: **Français · English · العربية** — the whole interface, all unit names and all messages are translated.

---

## 🚀 Run from Source

```bash
pip install -r requirements.txt
python scientific_calculator.py
```

## 📦 Build the Standalone Executable

```bash
pyinstaller ScientificCalculator.spec --noconfirm
```

Output: `dist/ScientificCalculator.exe` — no Python needed on the target machine.

## ✅ Run the Test Suite

```bash
python tests/test_engine.py      # 95 tests - parser, evaluator, matrices, stats
python tests/test_calculus.py    # 33 tests - limits, Taylor, inequalities, ODEs
```

---

## 📁 Project Structure

```
test001/
├── scientific_calculator.py      # Entry point / application shell
├── core/                         # ── Pure logic (no UI) ──
│   ├── engine.py                 #   Tokenizer, parser, evaluator, calculus
│   ├── calculus.py               #   Limits, Taylor, inequalities, ODEs
│   ├── matrices.py               #   Matrix operations
│   ├── equations.py              #   Linear/quadratic/system solvers
│   ├── statistics.py             #   Descriptive statistics & regression
│   └── units.py                  #   Unit conversion tables
├── ui/                           # ── Presentation layer ──
│   ├── theme.py                  #   Colours, fonts, spacing
│   ├── i18n.py                   #   FR / EN / AR translations
│   ├── calculator_view.py        #   Keypad, Ans key, history, constants
│   ├── grapher_view.py           #   Desmos-style canvas
│   ├── converter_view.py         #   Unit converter
│   ├── equations_view.py         #   Equation solver
│   ├── formulas_view.py          #   Formula library
│   ├── matrix_view.py            #   Matrix calculator
│   ├── calculus_view.py          #   Derivative / integral / roots
│   ├── advanced_view.py          #   Limits / Taylor / inequalities / ODEs
│   └── stats_view.py             #   Statistics
├── tests/
│   ├── test_engine.py            #   95 unit tests
│   └── test_calculus.py          #   33 unit tests
├── ScientificCalculator.spec     # PyInstaller config
├── version.txt                   # Windows version resource
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0-9`, `.` | Digits |
| `+ - * /` | Operators |
| `Enter` | Calculate |
| `Backspace` | Delete last character |
| `Escape` | Clear all |

---

**Made with ❤️ by reda anagou**
