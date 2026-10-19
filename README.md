# 🔢 Scientific Calculator — Sweet & Modern Desktop App

A professional, multilingual scientific calculator built with **Python + tkinter**, packaged as a standalone Windows `.exe` with **PyInstaller**.

**Copyright © reda anagou**

---

## ✨ Features

### 🧮 Scientific Calculator
- Basic arithmetic with a large, clean keypad
- Scientific functions: `sin`, `cos`, `tan`, `log`, `ln`, `√x`, `x!`, `π`, `eˣ`, `10ˣ`, `mod`, `±`
- Memory functions: `MC`, `MR`, `M+`, `M-`
- `DEG` / `RAD` angle mode toggle
- `x²` and `xⁿ` power operations
- Live expression preview line
- Keyboard support (numbers, operators, Enter, Backspace, Escape)

### ⚗️ Scientific Formulas
A built-in library of 9 ready-to-use formulas, each with its own inputs and instant calculation:

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

### 📐 Equation Solvers
Three tabs in the Equations window:

1. **1st degree** — solves `ax + b = 0`
2. **2nd degree** — solves `ax² + bx + c = 0` with discriminant `Δ`
3. **Expression** — type any expression in `x` and evaluate it

Coefficients accept scientific functions: `sin`, `cos`, `tan`, `cot`, `log`, `ln`, `exp`, `sqrt`, `pi`, `e`.

### 📈 2D Grapher
- Draws any function `y = f(x)` on a Cartesian coordinate system
- Friendly equation parsing: `3x` → `3*x`, `x²` → `x**2`, `^` → `**`
- Supports `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`, `log(x)`, `sqrt(x)`, `abs(x)`
- Grid, labelled axes, and tick marks

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
Switch instantly from the top bar: **Français · English · العربية** — the entire interface, all unit names, and all messages are translated.

### 🎨 Design
- Soft light theme with white cards on a slate background
- Color-coded buttons (indigo operators, mint scientific, amber memory, rose clear)
- Hover effects, resizable windows, no cut-off text

---

## 🚀 Run from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python scientific_calculator.py
```

## 📦 Build Standalone Executable

```bash
pyinstaller ScientificCalculator.spec --noconfirm
```

The executable will be created in the `dist/` folder as `ScientificCalculator.exe` — no Python installation required on the target machine.

---

## 📁 Project Structure

```
test001/
├── scientific_calculator.py      # Main application source
├── ScientificCalculator.spec     # PyInstaller build configuration
├── version.txt                   # Windows version info resource
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Files excluded from version control
├── build/                        # PyInstaller temp (git-ignored)
└── dist/                         # Compiled .exe output (git-ignored)
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
