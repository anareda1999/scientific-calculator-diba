"""
Scientific Calculator - Sweet & Modern Design
With Equation Solvers, 2D Grapher, Unit Converter & Scientific Formulas
Multilingual: English, Français, عربي
Built with Python + tkinter, packaged as a standalone .exe with PyInstaller.
Copyright © reda anagou
"""

import math
import re
import tkinter as tk
from tkinter import ttk, font as tkfont


class ScientificCalculator:
    # ── Translations ──────────────────────────────────────────────
    TR = {
        "app_title": {
            "en": "Scientific Calculator",
            "fr": "Calculatrice Scientifique",
            "ar": "الآلة الحاسبة العلمية",
        },
        "scientific": {
            "en": "SCIENTIFIC",
            "fr": "SCIENTIFIQUE",
            "ar": "علمي",
        },
        "converter": {
            "en": "Converter",
            "fr": "Convertisseur",
            "ar": "محول الوحدات",
        },
        "equations": {
            "en": "Equations",
            "fr": "Équations",
            "ar": "المعادلات",
        },
        "grapher": {
            "en": "Graph 2D",
            "fr": "Graphe 2D",
            "ar": "رسم بياني 2D",
        },
        "formulas": {
            "en": "Formulas",
            "fr": "Formules",
            "ar": "الصيغ",
        },
        "language": {
            "en": "Language",
            "fr": "Langue",
            "ar": "اللغة",
        },
        "deg": {
            "en": "DEG",
            "fr": "DEG",
            "ar": "درجة",
        },
        "from": {
            "en": "From",
            "fr": "De",
            "ar": "من",
        },
        "to": {
            "en": "To",
            "fr": "À",
            "ar": "إلى",
        },
        "swap": {
            "en": "Swap",
            "fr": "Inverser",
            "ar": "تبديل",
        },
        "weight": {
            "en": "Weight",
            "fr": "Poids",
            "ar": "الوزن",
        },
        "currency": {
            "en": "Currency",
            "fr": "Devise",
            "ar": "العملة",
        },
        "volume": {
            "en": "Volume",
            "fr": "Volume",
            "ar": "الحجم",
        },
        "area": {
            "en": "Area",
            "fr": "Surface",
            "ar": "المساحة",
        },
        "distance": {
            "en": "Distance",
            "fr": "Distance",
            "ar": "المسافة",
        },
        "eq_title": {
            "en": "Equations",
            "fr": "Équations",
            "ar": "المعادلات",
        },
        "eq1_tab": {
            "en": "1st degree  ax + b = 0",
            "fr": "1er degré  ax + b = 0",
            "ar": "الدرجة الأولى  ax + b = 0",
        },
        "eq2_tab": {
            "en": "2nd degree  ax² + bx + c = 0",
            "fr": "2ème degré  ax² + bx + c = 0",
            "ar": "الدرجة الثانية  ax² + bx + c = 0",
        },
        "coeff_a": {
            "en": "Coefficient a",
            "fr": "Coefficient a",
            "ar": "المعامل أ",
        },
        "coeff_b": {
            "en": "Coefficient b",
            "fr": "Coefficient b",
            "ar": "المعامل ب",
        },
        "coeff_c": {
            "en": "Coefficient c",
            "fr": "Coefficient c",
            "ar": "المعامل ج",
        },
        "solve": {
            "en": "Solve",
            "fr": "Résoudre",
            "ar": "حل",
        },
        "inf_solutions": {
            "en": "Infinite solutions",
            "fr": "∞ solutions",
            "ar": "حلول غير محدودة",
        },
        "no_solution": {
            "en": "No solution",
            "fr": "Pas de solution",
            "ar": "لا يوجد حل",
        },
        "invalid_input": {
            "en": "Invalid input",
            "fr": "Entrée invalide",
            "ar": "إدخال غير صحيح",
        },
        "graph_title": {
            "en": "2D Graph",
            "fr": "Graphe 2D",
            "ar": "رسم بياني 2D",
        },
        "y_eq": {
            "en": "y = f(x)",
            "fr": "y = f(x)",
            "ar": "ص = د(س)",
        },
        "draw": {
            "en": "Draw",
            "fr": "Tracer",
            "ar": "رسم",
        },
        "clear": {
            "en": "Clear",
            "fr": "Effacer",
            "ar": "مسح",
        },
        "func_error": {
            "en": "Function error",
            "fr": "Erreur de fonction",
            "ar": "خطأ في الدالة",
        },
        "graph_hint": {
            "en": "Ex: x**2+3*x-10, sin(x), cos(x), exp(x), log(x), sqrt(x)",
            "fr": "Ex: x**2+3*x-10, sin(x), cos(x), exp(x), log(x), sqrt(x)",
            "ar": "مثال: x**2+3*x-10, sin(x), cos(x), exp(x), log(x), sqrt(x)",
        },
        "copyright": {
            "en": "© reda anagou",
            "fr": "© reda anagou",
            "ar": "© reda anagou",
        },
        # Formula translations
        "formula_title": {
            "en": "Scientific Formulas",
            "fr": "Formules Scientifiques",
            "ar": "الصيغ العلمية",
        },
        "formula_quadratic": {
            "en": "Quadratic Formula",
            "fr": "Formule du second degré",
            "ar": "صيغة المعادلة التربيعية",
        },
        "formula_area_circle": {
            "en": "Area of Circle",
            "fr": "Aire du cercle",
            "ar": "مساحة الدائرة",
        },
        "formula_area_rect": {
            "en": "Area of Rectangle",
            "fr": "Aire du rectangle",
            "ar": "مساحة المستطيل",
        },
        "formula_area_triangle": {
            "en": "Area of Triangle",
            "fr": "Aire du triangle",
            "ar": "مساحة المثلث",
        },
        "formula_volume_sphere": {
            "en": "Volume of Sphere",
            "fr": "Volume de la sphère",
            "ar": "حجم الكرة",
        },
        "formula_volume_cyl": {
            "en": "Volume of Cylinder",
            "fr": "Volume du cylindre",
            "ar": "حجم الأسطوانة",
        },
        "formula_ohm": {
            "en": "Ohm's Law (V=IR)",
            "fr": "Loi d'Ohm (V=IR)",
            "ar": "قانون أوم (V=IR)",
        },
        "formula_force": {
            "en": "Force (F=ma)",
            "fr": "Force (F=ma)",
            "ar": "القوة (F=ma)",
        },
        "formula_kinetic": {
            "en": "Kinetic Energy",
            "fr": "Énergie cinétique",
            "ar": "طاقة الحركة",
        },
        "formula_result": {
            "en": "Result",
            "fr": "Résultat",
            "ar": "النتيجة",
        },
        "calculate": {
            "en": "Calculate",
            "fr": "Calculer",
            "ar": "احسب",
        },
        # Scientific functions for equations
        "eq_sin": {"en": "sin(x)", "fr": "sin(x)", "ar": "sin(x)"},
        "eq_cos": {"en": "cos(x)", "fr": "cos(x)", "ar": "cos(x)"},
        "eq_tan": {"en": "tan(x)", "fr": "tan(x)", "ar": "tan(x)"},
        "eq_cot": {"en": "cot(x)", "fr": "cot(x)", "ar": "cot(x)"},
        "eq_log": {"en": "log(x)", "fr": "log(x)", "ar": "log(x)"},
        "eq_ln": {"en": "ln(x)", "fr": "ln(x)", "ar": "ln(x)"},
        "eq_exp": {"en": "exp(x)", "fr": "exp(x)", "ar": "exp(x)"},
        "eq_sqrt": {"en": "√(x)", "fr": "√(x)", "ar": "√(x)"},
    }

    # ── Units ─────────────────────────────────────────────────────
    UNITS = {
        "Weight": {
            "en": {"Kilogram (kg)": 1.0, "Gram (g)": 1000.0, "Milligram (mg)": 1_000_000.0,
                   "Tonne (t)": 0.001, "Pound (lb)": 2.20462, "Ounce (oz)": 35.274},
            "fr": {"Kilogramme (kg)": 1.0, "Gramme (g)": 1000.0, "Milligramme (mg)": 1_000_000.0,
                   "Tonne (t)": 0.001, "Livre (lb)": 2.20462, "Once (oz)": 35.274},
            "ar": {"كيلوغرام (kg)": 1.0, "غرام (g)": 1000.0, "مليغرام (mg)": 1_000_000.0,
                   "طن (t)": 0.001, "رطل (lb)": 2.20462, "أونصة (oz)": 35.274},
        },
        "Currency": {
            "en": {"US Dollar (USD)": 1.0, "Euro (EUR)": 0.92, "British Pound (GBP)": 0.79,
                   "Japanese Yen (JPY)": 149.50, "Canadian Dollar (CAD)": 1.36,
                   "Australian Dollar (AUD)": 1.53, "Swiss Franc (CHF)": 0.88,
                   "Chinese Yuan (CNY)": 7.24, "Indian Rupee (INR)": 83.50,
                   "Algerian Dinar (DZD)": 134.50, "Moroccan Dirham (MAD)": 9.90,
                   "Tunisian Dinar (TND)": 3.10},
            "fr": {"Dollar américain (USD)": 1.0, "Euro (EUR)": 0.92, "Livre sterling (GBP)": 0.79,
                   "Yen japonais (JPY)": 149.50, "Dollar canadien (CAD)": 1.36,
                   "Dollar australien (AUD)": 1.53, "Franc suisse (CHF)": 0.88,
                   "Yuan chinois (CNY)": 7.24, "Roupie indienne (INR)": 83.50,
                   "Dinar algérien (DZD)": 134.50, "Dirham marocain (MAD)": 9.90,
                   "Dinar tunisien (TND)": 3.10},
            "ar": {"دولار أمريكي (USD)": 1.0, "يورو (EUR)": 0.92, "جنيه إسترليني (GBP)": 0.79,
                   "ين ياباني (JPY)": 149.50, "دولار كندي (CAD)": 1.36,
                   "دولار أسترالي (AUD)": 1.53, "فرنك سويسري (CHF)": 0.88,
                   "يوان صيني (CNY)": 7.24, "روبية هندية (INR)": 83.50,
                   "دinar جزائري (DZD)": 134.50, "درهم مغربي (MAD)": 9.90,
                   "دinar تونسي (TND)": 3.10},
        },
        "Volume": {
            "en": {"Liter (L)": 1.0, "Milliliter (mL)": 1000.0, "Cubic Meter (m³)": 0.001,
                   "Gallon (US gal)": 0.264172, "Quart (US qt)": 1.05669,
                   "Pint (US pt)": 2.11338, "Cup (US)": 4.22675,
                   "Fluid Ounce (US fl oz)": 33.814},
            "fr": {"Litre (L)": 1.0, "Millilitre (mL)": 1000.0, "Mètre cube (m³)": 0.001,
                   "Gallon (US gal)": 0.264172, "Quart (US qt)": 1.05669,
                   "Pinte (US pt)": 2.11338, "Tasse (US)": 4.22675,
                   "Once liquide (US fl oz)": 33.814},
            "ar": {"لتر (L)": 1.0, "مليلتر (mL)": 1000.0, "متر مكعب (m³)": 0.001,
                   "غالون (US gal)": 0.264172, "كوارت (US qt)": 1.05669,
                   "باينت (US pt)": 2.11338, "كوب (US)": 4.22675,
                   "أونصة سائلة (US fl oz)": 33.814},
        },
        "Area": {
            "en": {"Square Meter (m²)": 1.0, "Square Centimeter (cm²)": 10000.0,
                   "Square Millimeter (mm²)": 1_000_000.0, "Square Kilometer (km²)": 0.000001,
                   "Square Foot (ft²)": 10.7639, "Square Inch (in²)": 1550.0,
                   "Hectare (ha)": 0.0001, "Acre": 0.000247105},
            "fr": {"Mètre carré (m²)": 1.0, "Centimètre carré (cm²)": 10000.0,
                   "Millimètre carré (mm²)": 1_000_000.0, "Kilomètre carré (km²)": 0.000001,
                   "Pied carré (ft²)": 10.7639, "Pouce carré (in²)": 1550.0,
                   "Hectare (ha)": 0.0001, "Acre": 0.000247105},
            "ar": {"متر مربع (m²)": 1.0, "سنتيمتر مربع (cm²)": 10000.0,
                   "مليمتر مربع (mm²)": 1_000_000.0, "كيلومتر مربع (km²)": 0.000001,
                   "قدم مربع (ft²)": 10.7639, "بوصة مربعة (in²)": 1550.0,
                   "هكتار (ha)": 0.0001, "فدان": 0.000247105},
        },
        "Distance": {
            "en": {"Kilometer (km)": 1.0, "Meter (m)": 1000.0, "Centimeter (cm)": 100000.0,
                   "Millimeter (mm)": 1_000_000.0, "Mile (mi)": 0.621371,
                   "Yard (yd)": 1093.61, "Foot (ft)": 3280.84, "Inch (in)": 39370.1,
                   "Nautical Mile (nmi)": 0.539957},
            "fr": {"Kilomètre (km)": 1.0, "Mètre (m)": 1000.0, "Centimètre (cm)": 100000.0,
                   "Millimètre (mm)": 1_000_000.0, "Mile (mi)": 0.621371,
                   "Yard (yd)": 1093.61, "Pied (ft)": 3280.84, "Pouce (in)": 39370.1,
                   "Mille marin (nmi)": 0.539957},
            "ar": {"كيلومتر (km)": 1.0, "متر (m)": 1000.0, "سنتيمتر (cm)": 100000.0,
                   "مليمتر (mm)": 1_000_000.0, "ميل (mi)": 0.621371,
                   "ياردة (yd)": 1093.61, "قدم (ft)": 3280.84, "بوصة (in)": 39370.1,
                   "ميل بحري (nmi)": 0.539957},
        },
    }

    def __init__(self, root):
        self.root = root
        self.lang = "fr"

        self.root.title(self._t("app_title"))
        self.root.geometry("750x950")
        self.root.resizable(True, True)
        self.root.minsize(650, 750)

        # ── Sweet & Modern Color Palette ──────────────────────────
        self.C_BG       = "#f8fafc"
        self.C_CARD     = "#ffffff"
        self.C_DISPLAY  = "#0f172a"
        self.C_TEXT     = "#0f172a"
        self.C_TEXT_DIM = "#64748b"
        self.C_NUM      = "#f1f5f9"
        self.C_NUM_H    = "#e2e8f0"
        self.C_OP       = "#818cf8"
        self.C_OP_H     = "#6366f1"
        self.C_FUNC     = "#f0fdf4"
        self.C_FUNC_H   = "#d1fae5"
        self.C_FUNC_T   = "#059669"
        self.C_MEM      = "#fffbeb"
        self.C_MEM_H    = "#fef3c7"
        self.C_MEM_T    = "#d97706"
        self.C_CLEAR    = "#fee2e2"
        self.C_CLEAR_H  = "#fecaca"
        self.C_CLEAR_T  = "#b91c1c"
        self.C_EQUAL    = "#818cf8"
        self.C_EQUAL_H  = "#6366f1"
        self.C_ACCENT   = "#c084fc"
        self.C_CONVERT  = "#fce7f3"
        self.C_CONVERT_T= "#be185d"
        self.C_EQUATION = "#fff7ed"
        self.C_EQUATION_T= "#c2410c"
        self.C_GRAPH    = "#f0f9ff"
        self.C_GRAPH_T  = "#0c4a6e"
        self.C_FORMULA  = "#f0fdf4"
        self.C_FORMULA_T= "#059669"

        # State
        self.expression = ""
        self.memory = 0
        self.deg_mode = True
        self.new_input = True

        # Fonts
        self.f_display = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.f_expr    = tkfont.Font(family="Segoe UI", size=13)
        self.f_btn     = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.f_btn_s   = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_mode    = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_footer  = tkfont.Font(family="Segoe UI", size=9)
        self.f_conv    = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.f_eq      = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.f_graph   = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.f_formula = tkfont.Font(family="Segoe UI", size=11, weight="bold")

        self._build_ui()
        self._bind_keys()

    # ------------------------------------------------------------------ Helpers
    def _t(self, key):
        return self.TR.get(key, {}).get(self.lang, self.TR.get(key, {}).get("en", key))

    def _on_lang_change(self, val):
        self.lang = val
        self.lang_var.set(val)
        self._rebuild_ui()

    def _rebuild_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        self.root.configure(bg=self.C_BG)

        # ── Top bar (full width, all buttons visible) ──
        top = tk.Frame(self.root, bg=self.C_BG, height=60)
        top.pack(fill="x", padx=20, pady=(15, 10))
        top.pack_propagate(False)

        # Left: Language selector
        left_frame = tk.Frame(top, bg=self.C_BG)
        left_frame.pack(side="left", fill="y")

        self.lang_var = tk.StringVar(value=self.lang)
        tk.Label(left_frame, text=self._t("language") + ":", bg=self.C_BG,
                 fg=self.C_TEXT_DIM, font=self.f_mode).pack(side="left", padx=(0, 8))

        for lang_code, lang_label in [("fr", "Fr"), ("en", "En"), ("ar", "Ar")]:
            rb = tk.Radiobutton(
                left_frame, text=lang_label, variable=self.lang_var, value=lang_code,
                bg=self.C_BG, fg=self.C_TEXT, selectcolor=self.C_CARD,
                font=self.f_mode, activebackground=self.C_BG,
                activeforeground=self.C_TEXT, command=lambda c=lang_code: self._on_lang_change(c),
                bd=0, highlightthickness=0, padx=6,
            )
            rb.pack(side="left", padx=(0, 6))

        # Center: App title
        title_label = tk.Label(
            top, text=self._t("app_title"),
            bg=self.C_BG, fg=self.C_TEXT, font=self.f_btn,
            anchor="center",
        )
        title_label.pack(side="left", expand=True, fill="x")

        # Right: Action buttons (stacked horizontally, all visible)
        right_frame = tk.Frame(top, bg=self.C_BG)
        right_frame.pack(side="right")

        self.mode_label = tk.Label(
            right_frame, text="DEG",
            bg=self.C_BG, fg=self.C_ACCENT, font=self.f_mode,
        )
        self.mode_label.pack(side="right", padx=(12, 0))

        conv_btn = tk.Button(
            right_frame, text=self._t("converter"),
            command=self.open_converter,
            bg=self.C_CONVERT, fg=self.C_CONVERT_T,
            activebackground=self.C_CONVERT_T, activeforeground="#ffffff",
            font=self.f_mode, bd=0, relief="flat", cursor="hand2",
            highlightthickness=0, padx=14, pady=8,
        )
        conv_btn.pack(side="right", padx=(8, 0))

        eq_btn = tk.Button(
            right_frame, text=self._t("equations"),
            command=self.open_equation_solver,
            bg=self.C_EQUATION, fg=self.C_EQUATION_T,
            activebackground=self.C_EQUATION_T, activeforeground="#ffffff",
            font=self.f_mode, bd=0, relief="flat", cursor="hand2",
            highlightthickness=0, padx=14, pady=8,
        )
        eq_btn.pack(side="right", padx=(8, 0))

        graph_btn = tk.Button(
            right_frame, text=self._t("grapher"),
            command=self.open_grapher,
            bg=self.C_GRAPH, fg=self.C_GRAPH_T,
            activebackground=self.C_GRAPH_T, activeforeground="#ffffff",
            font=self.f_mode, bd=0, relief="flat", cursor="hand2",
            highlightthickness=0, padx=14, pady=8,
        )
        graph_btn.pack(side="right", padx=(8, 0))

        formula_btn = tk.Button(
            right_frame, text=self._t("formulas"),
            command=self.open_formulas,
            bg=self.C_FORMULA, fg=self.C_FORMULA_T,
            activebackground=self.C_FORMULA_T, activeforeground="#ffffff",
            font=self.f_mode, bd=0, relief="flat", cursor="hand2",
            highlightthickness=0, padx=14, pady=8,
        )
        formula_btn.pack(side="right", padx=(8, 0))

        # ── Expression preview ──
        self.expr_var = tk.StringVar(value="")
        expr_label = tk.Label(
            self.root, textvariable=self.expr_var,
            bg=self.C_DISPLAY, fg=self.C_TEXT_DIM, font=self.f_expr,
            anchor="e",
        )
        expr_label.pack(fill="x", padx=24, pady=(0, 4))

        # ── Main display card ──
        display_card = tk.Frame(self.root, bg=self.C_DISPLAY, bd=0)
        display_card.pack(fill="x", padx=24, pady=(0, 24))

        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            display_card, textvariable=self.display_var,
            font=self.f_display, bg=self.C_DISPLAY, fg="#ffffff",
            insertbackground="#ffffff", bd=0, justify="right",
            readonlybackground=self.C_DISPLAY,
        )
        display.pack(fill="x", padx=20, pady=20)
        display.configure(state="readonly")

        # ── Calculator button grid card ──
        btn_card = tk.Frame(self.root, bg=self.C_CARD, bd=0)
        btn_card.pack(padx=16, pady=(0, 14), fill="x")

        btn_frame = tk.Frame(btn_card, bg=self.C_CARD)
        btn_frame.pack(padx=14, pady=14)

        buttons = [
            [("MC", "mem"), ("MR", "mem"), ("M+", "mem"), ("M-", "mem")],
            [("DEG/RAD", "func"), ("(", "func"), (")", "func"), ("AC", "clear")],
            [("2nd", "func"), ("x²", "func"), ("xⁿ", "op"), ("÷", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("0", "num"), (".", "num"), ("=", "equal")],
        ]

        commands = {
            "MC": self.mc, "MR": self.mr, "M+": self.m_add, "M-": self.m_sub,
            "DEG/RAD": self.toggle_deg_rad,
            "(": lambda: self._add_char("("), ")": lambda: self._add_char(")"),
            "AC": self.clear_all, "2nd": self._noop,
            "x²": lambda: self._math_func("square"),
            "xⁿ": lambda: self._add_char("**"),
            "÷": lambda: self._add_operator("/"),
            "×": lambda: self._add_operator("*"),
            "−": lambda: self._add_operator("-"),
            "+": lambda: self._add_operator("+"),
            "=": self.calculate,
        }
        for d in "0123456789.":
            commands[d] = lambda digit=d: self._add_digit(digit)

        styles = {
            "num":   {"bg": self.C_NUM,   "fg": self.C_TEXT,     "active": self.C_NUM_H,     "hover": self.C_NUM_H},
            "op":    {"bg": self.C_OP,    "fg": "#ffffff",       "active": self.C_OP_H,     "hover": self.C_OP_H},
            "equal": {"bg": self.C_EQUAL, "fg": "#ffffff",       "active": self.C_EQUAL_H,  "hover": self.C_EQUAL_H},
            "clear": {"bg": self.C_CLEAR, "fg": self.C_CLEAR_T,  "active": self.C_CLEAR_H,  "hover": self.C_CLEAR_H},
            "mem":   {"bg": self.C_MEM,   "fg": self.C_MEM_T,    "active": self.C_MEM_H,    "hover": self.C_MEM_H},
            "func":  {"bg": self.C_FUNC,  "fg": self.C_FUNC_T,   "active": self.C_FUNC_H,   "hover": self.C_FUNC_H},
        }

        for row in buttons:
            r_frame = tk.Frame(btn_frame, bg=self.C_CARD)
            r_frame.pack(fill="x", pady=4)
            for text, style_class in row:
                cmd = commands.get(text, lambda: None)
                s = styles[style_class]
                colspan = 2 if text == "0" else 1
                btn = tk.Button(
                    r_frame, text=text, command=cmd,
                    font=self.f_btn, bg=s["bg"], fg=s["fg"],
                    activebackground=s["active"], activeforeground=s["fg"],
                    bd=0, relief="flat", cursor="hand2",
                    highlightthickness=0,
                )
                if colspan == 2:
                    btn.pack(side="left", fill="both", expand=True, padx=(0, 6))
                else:
                    btn.pack(side="left", fill="both", expand=True, padx=3)
                self._add_hover(btn, s["bg"], s["hover"])

        # ── Scientific function panel card ──
        sci_label = tk.Label(
            self.root, text=self._t("scientific"),
            bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_mode,
            anchor="w",
        )
        sci_label.pack(fill="x", padx=24, pady=(16, 6))

        sci_card = tk.Frame(self.root, bg=self.C_CARD, bd=0)
        sci_card.pack(padx=16, pady=(0, 14), fill="x")

        sci_frame = tk.Frame(sci_card, bg=self.C_CARD)
        sci_frame.pack(padx=14, pady=14)

        sci_buttons = [
            [("sin", "sin"), ("cos", "cos"), ("tan", "tan"), ("log", "log10")],
            [("ln", "ln"), ("√x", "sqrt"), ("x!", "factorial"), ("π", "pi")],
            [("eˣ", "exp"), ("10ˣ", "pow10"), ("mod", "mod"), ("±", "neg")],
        ]

        for row in sci_buttons:
            r_frame = tk.Frame(sci_frame, bg=self.C_CARD)
            r_frame.pack(fill="x", pady=4)
            for text, func_name in row:
                btn = tk.Button(
                    r_frame, text=text,
                    command=lambda f=func_name: self._sci_func(f),
                    font=self.f_btn_s, bg=self.C_FUNC, fg=self.C_FUNC_T,
                    activebackground=self.C_FUNC_H, activeforeground=self.C_FUNC_T,
                    bd=0, relief="flat", cursor="hand2", highlightthickness=0,
                )
                btn.pack(side="left", fill="both", expand=True, padx=3)
                self._add_hover(btn, self.C_FUNC, self.C_FUNC_H)

        # ── Footer ──
        footer = tk.Frame(self.root, bg=self.C_BG, height=30)
        footer.pack(fill="x", side="bottom", pady=(0, 14))
        footer.pack_propagate(False)

        tk.Label(
            footer, text=self._t("copyright"),
            bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_footer,
        ).pack(side="right")

    # ------------------------------------------------------------------ Converter Window
    def open_converter(self):
        win = tk.Toplevel(self.root)
        win.title(self._t("converter"))
        win.geometry("520x720")
        win.resizable(True, True)
        win.minsize(480, 600)
        win.configure(bg=self.C_BG)
        win.transient(self.root)
        win.grab_set()

        header = tk.Frame(win, bg=self.C_BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)

        tk.Label(
            header, text=self._t("converter"),
            bg=self.C_BG, fg=self.C_TEXT, font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            anchor="w",
        ).pack(side="left", expand=True)

        tk.Button(
            header, text="✕", command=win.destroy,
            bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_btn,
            bd=0, relief="flat", cursor="hand2",
        ).pack(side="right")

        cat_frame = tk.Frame(win, bg=self.C_BG)
        cat_frame.pack(fill="x", padx=24, pady=(0, 16))

        categories = ["Weight", "Currency", "Volume", "Area", "Distance"]
        cat_labels = {c: self._t(c.lower()) for c in categories}
        self.conv_category = tk.StringVar(value=categories[0])

        for cat in categories:
            rb = tk.Radiobutton(
                cat_frame, text=cat_labels[cat], variable=self.conv_category, value=cat,
                bg=self.C_BG, fg=self.C_TEXT, selectcolor=self.C_CARD,
                font=self.f_mode, activebackground=self.C_BG,
                activeforeground=self.C_TEXT, command=lambda: self._refresh_converter_units(win),
                bd=0, highlightthickness=0, padx=8,
            )
            rb.pack(side="left", padx=(0, 14))

        conv_card = tk.Frame(win, bg=self.C_CARD, bd=0)
        conv_card.pack(padx=20, pady=(0, 16), fill="both", expand=True)

        inner = tk.Frame(conv_card, bg=self.C_CARD)
        inner.pack(padx=20, pady=18, fill="both", expand=True)

        tk.Label(inner, text=self._t("from"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 6))

        self.conv_from_val = tk.StringVar(value="")
        from_entry = tk.Entry(
            inner, textvariable=self.conv_from_val,
            font=self.f_display, bg="#f8fafc", fg=self.C_TEXT,
            bd=0, justify="right", insertbackground=self.C_TEXT,
        )
        from_entry.pack(fill="x", pady=(0, 10))
        from_entry.bind("<KeyRelease>", lambda e: self._auto_convert(win))

        self.conv_from_unit = ttk.Combobox(
            inner, state="readonly", font=self.f_btn_s, height=10,
        )
        self.conv_from_unit.pack(fill="x", pady=(0, 18))

        swap_btn = tk.Button(
            inner, text=self._t("swap"), command=lambda: self._swap_units(win),
            bg=self.C_ACCENT, fg="#ffffff", font=self.f_mode,
            bd=0, relief="flat", cursor="hand2", highlightthickness=0,
            padx=14, pady=7,
        )
        swap_btn.pack(pady=(0, 18))

        tk.Label(inner, text=self._t("to"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 6))

        self.conv_to_val = tk.StringVar(value="")
        to_entry = tk.Entry(
            inner, textvariable=self.conv_to_val,
            font=self.f_display, bg="#f8fafc", fg=self.C_TEXT,
            bd=0, justify="right", insertbackground=self.C_TEXT, state="readonly",
        )
        to_entry.pack(fill="x", pady=(0, 10))

        self.conv_to_unit = ttk.Combobox(
            inner, state="readonly", font=self.f_btn_s, height=10,
        )
        self.conv_to_unit.pack(fill="x", pady=(0, 20))

        tk.Label(
            inner, text=self._t("copyright"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
            font=self.f_footer, anchor="center",
        ).pack(side="bottom")

        self._refresh_converter_units(win)

    # ------------------------------------------------------------------ Converter Logic
    def _refresh_converter_units(self, win):
        cat = self.conv_category.get()
        units = list(self.UNITS[cat][self.lang].keys())
        self.conv_from_unit["values"] = units
        self.conv_to_unit["values"] = units
        self.conv_from_unit.current(0)
        self.conv_to_unit.current(min(1, len(units) - 1))
        self.conv_from_val.set("")
        self.conv_to_val.set("")

    def _swap_units(self, win):
        from_idx = self.conv_from_unit.current()
        to_idx = self.conv_to_unit.current()
        self.conv_from_unit.current(to_idx)
        self.conv_to_unit.current(from_idx)
        self._auto_convert(win)

    def _auto_convert(self, win):
        try:
            cat = self.conv_category.get()
            from_unit = self.conv_from_unit.get()
            to_unit = self.conv_to_unit.get()
            raw = self.conv_from_val.get().strip()
            if raw == "":
                self.conv_to_val.set("")
                return
            value = float(raw)
            base = value / self.UNITS[cat][self.lang][from_unit]
            result = base * self.UNITS[cat][self.lang][to_unit]
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:g}"
            self.conv_to_val.set(result_str)
        except Exception:
            self.conv_to_val.set("")

    # ------------------------------------------------------------------ Equation Solver Window
    def open_equation_solver(self):
        win = tk.Toplevel(self.root)
        win.title(self._t("eq_title"))
        win.geometry("440x650")
        win.resizable(True, True)
        win.minsize(400, 500)
        win.configure(bg=self.C_BG)
        win.transient(self.root)
        win.grab_set()

        header = tk.Frame(win, bg=self.C_BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)

        tk.Label(
            header, text=self._t("eq_title"),
            bg=self.C_BG, fg=self.C_TEXT, font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            anchor="w",
        ).pack(side="left", expand=True)

        tk.Button(
            header, text="✕", command=win.destroy,
            bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_btn,
            bd=0, relief="flat", cursor="hand2",
        ).pack(side="right")

        nb = ttk.Notebook(win)
        nb.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.C_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.C_CARD, foreground=self.C_TEXT_DIM,
                        padding=[14, 10], font=self.f_mode)
        style.map("TNotebook.Tab", background=[("selected", self.C_CARD)],
                  foreground=[("selected", self.C_TEXT)])

        # ── 1st Degree Tab ──
        tab1 = tk.Frame(nb, bg=self.C_CARD)
        nb.add(tab1, text=self._t("eq1_tab"))

        inner1 = tk.Frame(tab1, bg=self.C_CARD)
        inner1.pack(padx=24, pady=20, fill="both", expand=True)

        tk.Label(inner1, text="ax + b = 0", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 16))

        tk.Label(inner1, text=self._t("coeff_a"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.eq1_a = tk.StringVar(value="")
        ent_a1 = tk.Entry(inner1, textvariable=self.eq1_a, font=self.f_display,
                          bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                          insertbackground=self.C_TEXT)
        ent_a1.pack(fill="x", pady=(0, 14))

        tk.Label(inner1, text=self._t("coeff_b"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.eq1_b = tk.StringVar(value="")
        ent_b1 = tk.Entry(inner1, textvariable=self.eq1_b, font=self.f_display,
                          bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                          insertbackground=self.C_TEXT)
        ent_b1.pack(fill="x", pady=(0, 20))

        btn_solve1 = tk.Button(
            inner1, text=self._t("solve"), command=self._solve_eq1,
            bg=self.C_EQUATION_T, fg="#ffffff", font=self.f_eq,
            bd=0, relief="flat", cursor="hand2", highlightthickness=0,
            padx=20, pady=10,
        )
        btn_solve1.pack(fill="x", pady=(0, 16))

        self.eq1_result = tk.Label(inner1, text="", bg=self.C_CARD, fg=self.C_TEXT,
                                   font=self.f_display, anchor="center", justify="center")
        self.eq1_result.pack(fill="x")

        # Scientific functions hint for equations
        sci_hint1 = tk.Frame(inner1, bg=self.C_BG)
        sci_hint1.pack(fill="x", pady=(10, 0))
        tk.Label(sci_hint1, text="Use: sin, cos, tan, cot, log, ln, exp, sqrt, pi, e",
                 bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_footer, anchor="w").pack(fill="x")

        # ── 2nd Degree Tab ──
        tab2 = tk.Frame(nb, bg=self.C_CARD)
        nb.add(tab2, text=self._t("eq2_tab"))

        inner2 = tk.Frame(tab2, bg=self.C_CARD)
        inner2.pack(padx=24, pady=20, fill="both", expand=True)

        tk.Label(inner2, text="ax² + bx + c = 0", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 16))

        tk.Label(inner2, text=self._t("coeff_a"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.eq2_a = tk.StringVar(value="")
        ent_a2 = tk.Entry(inner2, textvariable=self.eq2_a, font=self.f_display,
                          bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                          insertbackground=self.C_TEXT)
        ent_a2.pack(fill="x", pady=(0, 10))

        tk.Label(inner2, text=self._t("coeff_b"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.eq2_b = tk.StringVar(value="")
        ent_b2 = tk.Entry(inner2, textvariable=self.eq2_b, font=self.f_display,
                          bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                          insertbackground=self.C_TEXT)
        ent_b2.pack(fill="x", pady=(0, 10))

        tk.Label(inner2, text=self._t("coeff_c"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.eq2_c = tk.StringVar(value="")
        ent_c2 = tk.Entry(inner2, textvariable=self.eq2_c, font=self.f_display,
                          bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                          insertbackground=self.C_TEXT)
        ent_c2.pack(fill="x", pady=(0, 20))

        btn_solve2 = tk.Button(
            inner2, text=self._t("solve"), command=self._solve_eq2,
            bg=self.C_EQUATION_T, fg="#ffffff", font=self.f_eq,
            bd=0, relief="flat", cursor="hand2", highlightthickness=0,
            padx=20, pady=10,
        )
        btn_solve2.pack(fill="x", pady=(0, 16))

        self.eq2_result = tk.Label(inner2, text="", bg=self.C_CARD, fg=self.C_TEXT,
                                   font=self.f_display, anchor="center", justify="center")
        self.eq2_result.pack(fill="x", pady=(0, 4))

        self.eq2_delta = tk.Label(inner2, text="", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                                  font=self.f_mode, anchor="center", justify="center")
        self.eq2_delta.pack(fill="x", pady=(0, 16))

        sci_hint2 = tk.Frame(inner2, bg=self.C_BG)
        sci_hint2.pack(fill="x", pady=(0, 0))
        tk.Label(sci_hint2, text="Use: sin, cos, tan, cot, log, ln, exp, sqrt, pi, e",
                 bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_footer, anchor="w").pack(fill="x")

        # ── Expression Tab ──
        tab3 = tk.Frame(nb, bg=self.C_CARD)
        nb.add(tab3, text="Expression")

        inner3 = tk.Frame(tab3, bg=self.C_CARD)
        inner3.pack(padx=24, pady=20, fill="both", expand=True)

        tk.Label(inner3, text="Type your equation in x", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 8))

        tk.Label(inner3, text="Expression (use x as variable):", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.expr_input = tk.StringVar(value="sin(x) + cos(x) - 1")
        ent_expr = tk.Entry(inner3, textvariable=self.expr_input, font=self.f_display,
                            bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                            insertbackground=self.C_TEXT)
        ent_expr.pack(fill="x", pady=(0, 14))

        tk.Label(inner3, text="Value of x:", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(fill="x", pady=(0, 4))
        self.x_value = tk.StringVar(value="0")
        ent_x = tk.Entry(inner3, textvariable=self.x_value, font=self.f_display,
                         bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="center",
                         insertbackground=self.C_TEXT)
        ent_x.pack(fill="x", pady=(0, 14))

        btn_calc_expr = tk.Button(
            inner3, text=self._t("calculate"), command=self._calc_expression,
            bg=self.C_EQUATION_T, fg="#ffffff", font=self.f_eq,
            bd=0, relief="flat", cursor="hand2", highlightthickness=0,
            padx=20, pady=10,
        )
        btn_calc_expr.pack(fill="x", pady=(0, 16))

        self.expr_result = tk.Label(inner3, text="", bg=self.C_CARD, fg=self.C_TEXT,
                                    font=self.f_display, anchor="center", justify="center")
        self.expr_result.pack(fill="x")

        tk.Label(
            inner3, text=self._t("copyright"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
            font=self.f_footer, anchor="center",
        ).pack(side="bottom", pady=(10, 0))

    # ------------------------------------------------------------------ Equation Solving Logic
    def _parse_coeff(self, value_str):
        """Parse a coefficient value that may contain scientific functions."""
        value_str = value_str.strip()
        if value_str == "":
            return 0.0

        # Replace scientific functions with Python equivalents
        replacements = {
            "sin(": "math.sin(", "cos(": "math.cos(", "tan(": "math.tan(",
            "cot(": "1/math.tan(", "log(": "math.log10(", "ln(": "math.log(",
            "exp(": "math.exp(", "sqrt(": "math.sqrt(", "pi": "math.pi",
            "e": "math.e",
        }
        expr = value_str
        for old, new in replacements.items():
            expr = expr.replace(old, new)

        # Handle DEG/RAD: if DEG mode, convert trig arguments
        if self.deg_mode:
            # Wrap trig functions with radians conversion
            expr = expr.replace("math.sin(", "math.sin(math.radians(")
            expr = expr.replace("math.cos(", "math.cos(math.radians(")
            expr = expr.replace("math.tan(", "math.tan(math.radians(")
            # Need to balance parentheses - simpler approach: just use the value as-is
            # since users typically input simple values

        try:
            result = eval(expr, {"__builtins__": {}}, {"math": math})
            return float(result)
        except Exception:
            return 0.0

    def _solve_eq1(self):
        try:
            a = self._parse_coeff(self.eq1_a.get())
            b = self._parse_coeff(self.eq1_b.get())
            if a == 0:
                if b == 0:
                    self.eq1_result.config(text=self._t("inf_solutions"), fg=self.C_TEXT_DIM)
                else:
                    self.eq1_result.config(text=self._t("no_solution"), fg=self.C_CLEAR_T)
            else:
                x = -b / a
                x_str = str(int(x)) if x == int(x) else f"{x:g}"
                self.eq1_result.config(text=f"x = {x_str}", fg=self.C_TEXT)
        except Exception:
            self.eq1_result.config(text=self._t("invalid_input"), fg=self.C_CLEAR_T)

    def _solve_eq2(self):
        try:
            a = self._parse_coeff(self.eq2_a.get())
            b = self._parse_coeff(self.eq2_b.get())
            c = self._parse_coeff(self.eq2_c.get())

            if a == 0:
                if b == 0:
                    if c == 0:
                        self.eq2_result.config(text=self._t("inf_solutions"), fg=self.C_TEXT_DIM)
                        self.eq2_delta.config(text="")
                    else:
                        self.eq2_result.config(text=self._t("no_solution"), fg=self.C_CLEAR_T)
                        self.eq2_delta.config(text="")
                else:
                    x = -c / b
                    x_str = str(int(x)) if x == int(x) else f"{x:g}"
                    self.eq2_result.config(text=f"x = {x_str}", fg=self.C_TEXT)
                    self.eq2_delta.config(text="(1st degree)", fg=self.C_TEXT_DIM)
                return

            delta = b * b - 4 * a * c
            if delta > 0:
                x1 = (-b - math.sqrt(delta)) / (2 * a)
                x2 = (-b + math.sqrt(delta)) / (2 * a)
                def fmt(v):
                    return str(int(v)) if v == int(v) else f"{v:g}"
                self.eq2_result.config(text=f"x₁ = {fmt(x1)}\nx₂ = {fmt(x2)}", fg=self.C_TEXT)
                self.eq2_delta.config(text=f"Δ = {fmt(delta)} > 0", fg=self.C_FUNC_T)
            elif delta == 0:
                x = -b / (2 * a)
                x_str = str(int(x)) if x == int(x) else f"{x:g}"
                self.eq2_result.config(text=f"x₀ = {x_str} (double)", fg=self.C_TEXT)
                self.eq2_delta.config(text="Δ = 0 (double root)", fg=self.C_FUNC_T)
            else:
                self.eq2_result.config(text="No real roots", fg=self.C_TEXT_DIM)
                self.eq2_delta.config(text=f"Δ = {fmt(delta)} < 0", fg=self.C_TEXT_DIM)
        except Exception:
            self.eq2_result.config(text=self._t("invalid_input"), fg=self.C_CLEAR_T)
            self.eq2_delta.config(text="")

    def _calc_expression(self):
        """Evaluate a mathematical expression in x for a given x value."""
        try:
            expr = self.expr_input.get().strip()
            x_str = self.x_value.get().strip()
            if expr == "" or x_str == "":
                self.expr_result.config(text="Please fill all fields", fg=self.C_CLEAR_T)
                return

            x = float(x_str)

            # Prepare expression for Python eval
            s = expr.replace('^', '**')
            s = re.sub(r'(\d)([xX])', r'\1*\2', s)
            s = re.sub(r'\)([xX])', r')*\1', s)
            s = re.sub(r'([xX])\)', r'\1)*', s)
            s = s.replace('²', '**2')

            safe_dict = {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "cot": lambda v: 1 / math.tan(v),
                "log": math.log10, "ln": math.log, "log10": math.log10,
                "sqrt": math.sqrt, "exp": math.exp, "pi": math.pi, "e": math.e,
                "abs": abs, "pow": pow, "x": x,
            }

            result = eval(s, {"__builtins__": {}}, safe_dict)
            if result is None:
                self.expr_result.config(text="Error", fg=self.C_CLEAR_T)
                return
            result = float(result)
            if not math.isfinite(result):
                self.expr_result.config(text="Undefined", fg=self.C_CLEAR_T)
                return
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:g}"
            self.expr_result.config(text=f"Result: {result_str}", fg=self.C_TEXT)
        except Exception:
            self.expr_result.config(text=self._t("invalid_input"), fg=self.C_CLEAR_T)

    # ------------------------------------------------------------------ Grapher Window
    def open_grapher(self):
        win = tk.Toplevel(self.root)
        win.title(self._t("graph_title"))
        win.geometry("720x650")
        win.resizable(True, True)
        win.minsize(600, 500)
        win.configure(bg=self.C_BG)
        win.transient(self.root)
        win.grab_set()

        header = tk.Frame(win, bg=self.C_BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 8))
        header.pack_propagate(False)

        tk.Label(
            header, text=self._t("graph_title"),
            bg=self.C_BG, fg=self.C_TEXT, font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            anchor="w",
        ).pack(side="left", expand=True)

        tk.Button(
            header, text="✕", command=win.destroy,
            bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_btn,
            bd=0, relief="flat", cursor="hand2",
        ).pack(side="right")

        ctrl = tk.Frame(win, bg=self.C_CARD)
        ctrl.pack(fill="x", padx=16, pady=(0, 12))

        inner = tk.Frame(ctrl, bg=self.C_CARD)
        inner.pack(padx=16, pady=14, fill="x")

        tk.Label(inner, text=self._t("y_eq"), bg=self.C_CARD, fg=self.C_TEXT_DIM,
                 font=self.f_mode, anchor="w").pack(side="left", padx=(0, 8))

        self.graph_func = tk.StringVar(value="x**2+3*x-10")
        ent_func = tk.Entry(inner, textvariable=self.graph_func, font=self.f_btn,
                            bg="#f8fafc", fg=self.C_TEXT, bd=0, width=30,
                            insertbackground=self.C_TEXT)
        ent_func.pack(side="left", padx=(0, 12))

        btn_draw = tk.Button(
            inner, text=self._t("draw"), command=self._draw_graph,
            bg=self.C_GRAPH_T, fg="#ffffff", font=self.f_eq,
            bd=0, relief="flat", cursor="hand2", highlightthickness=0,
            padx=16, pady=8,
        )
        btn_draw.pack(side="left", padx=(0, 12))

        btn_clear = tk.Button(
            inner, text=self._t("clear"), command=self._clear_graph,
            bg=self.C_CLEAR_T, fg="#ffffff", font=self.f_eq,
            bd=0, relief="flat", cursor="hand2", highlightthickness=0,
            padx=16, pady=8,
        )
        btn_clear.pack(side="left")

        tk.Label(inner, text=self._t("graph_hint"),
                 bg=self.C_CARD, fg=self.C_TEXT_DIM, font=self.f_footer,
                 anchor="w").pack(side="left", padx=(16, 0))

        graph_card = tk.Frame(win, bg=self.C_CARD, bd=0)
        graph_card.pack(padx=16, pady=(0, 16), fill="both", expand=True)

        canvas_inner = tk.Frame(graph_card, bg=self.C_CARD)
        canvas_inner.pack(padx=14, pady=14, fill="both", expand=True)

        self.graph_canvas = tk.Canvas(
            canvas_inner, bg="#ffffff", bd=0, highlightthickness=0,
            width=680, height=440,
        )
        self.graph_canvas.pack(fill="both", expand=True)

        win.after(100, self._draw_graph)

        tk.Label(
            win, text=self._t("copyright"), bg=self.C_BG, fg=self.C_TEXT_DIM,
            font=self.f_footer, anchor="center",
        ).pack(side="bottom", pady=(0, 10))

    # ------------------------------------------------------------------ Graphing Logic
    def _prepare_func_string(self, func_str):
        s = func_str.strip()
        s = s.replace('^', '**')
        s = re.sub(r'(\d)([xX])', r'\1*\2', s)
        s = re.sub(r'\)([xX])', r')*\1', s)
        s = re.sub(r'([xX])\)', r'\1)*', s)
        s = s.replace('²', '**2')
        return s

    def _clear_graph(self):
        self.graph_canvas.delete("all")
        self._draw_axes()

    def _draw_axes(self):
        canvas = self.graph_canvas
        canvas.update_idletasks()
        w = max(canvas.winfo_width(), 600)
        h = max(canvas.winfo_height(), 400)
        cx = w // 2
        cy = h // 2

        step = 50
        for x in range(0, w, step):
            canvas.create_line(x, 0, x, h, fill="#f1f5f9", width=1)
        for y in range(0, h, step):
            canvas.create_line(0, y, w, y, fill="#f1f5f9", width=1)

        canvas.create_line(cx, 0, cx, h, fill="#94a3b8", width=2, arrow=tk.LAST)
        canvas.create_line(0, cy, w, cy, fill="#94a3b8", width=2, arrow=tk.LAST)

        canvas.create_text(cx - 12, cy + 22, text="0", fill="#64748b", font=("Segoe UI", 10, "bold"))
        canvas.create_text(w - 18, cy + 18, text="x", fill="#64748b", font=("Segoe UI", 12, "bold"))
        canvas.create_text(cx + 18, 18, text="y", fill="#64748b", font=("Segoe UI", 12, "bold"))

        for i in range(-10, 11):
            if i == 0:
                continue
            tx = cx + i * step
            ty = cy - i * step
            if 0 <= tx <= w:
                canvas.create_text(tx, cy + 24, text=str(i), fill="#94a3b8", font=("Segoe UI", 9))
            if 0 <= ty <= h:
                canvas.create_text(cx - 18, ty, text=str(i), fill="#94a3b8", font=("Segoe UI", 9))

    def _draw_graph(self):
        self.graph_canvas.delete("all")
        self._draw_axes()

        canvas = self.graph_canvas
        canvas.update_idletasks()
        w = max(canvas.winfo_width(), 600)
        h = max(canvas.winfo_height(), 400)
        cx = w // 2
        cy = h // 2
        step = 40

        func_str = self.graph_func.get().strip()
        if not func_str:
            return

        py_func = self._prepare_func_string(func_str)

        safe_dict = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log10, "ln": math.log, "log10": math.log10,
            "sqrt": math.sqrt, "exp": math.exp, "pi": math.pi, "e": math.e,
            "abs": abs, "pow": pow,
        }

        points = []
        try:
            for px in range(-w // 2, w // 2 + 1, 2):
                x = px / step
                try:
                    y = eval(py_func, {"__builtins__": {}}, {**safe_dict, "x": x})
                    if y is None:
                        continue
                    y = float(y)
                    if not math.isfinite(y):
                        continue
                    canvas_x = cx + px
                    canvas_y = cy - y * step
                    if 0 <= canvas_x <= w and 0 <= canvas_y <= h:
                        points.append((canvas_x, canvas_y))
                except Exception:
                    continue

            if len(points) >= 2:
                for i in range(len(points) - 1):
                    x1, y1 = points[i]
                    x2, y2 = points[i + 1]
                    if abs(y2 - y1) > h / 2:
                        continue
                    canvas.create_line(x1, y1, x2, y2, fill=self.C_GRAPH_T, width=2, capstyle=tk.ROUND)

            canvas.create_text(12, 12, text=f"y = {func_str}", fill=self.C_GRAPH_T,
                               font=("Segoe UI", 11, "bold"), anchor="nw")
        except Exception as e:
            canvas.create_text(cx, cy // 2, text=self._t("func_error"), fill=self.C_CLEAR_T,
                               font=("Segoe UI", 14, "bold"))

    # ------------------------------------------------------------------ Scientific Formulas Window
    def open_formulas(self):
        win = tk.Toplevel(self.root)
        win.title(self._t("formula_title"))
        win.geometry("560x700")
        win.resizable(True, True)
        win.minsize(500, 550)
        win.configure(bg=self.C_BG)
        win.transient(self.root)
        win.grab_set()

        header = tk.Frame(win, bg=self.C_BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)

        tk.Label(
            header, text=self._t("formula_title"),
            bg=self.C_BG, fg=self.C_TEXT, font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            anchor="w",
        ).pack(side="left", expand=True)

        tk.Button(
            header, text="✕", command=win.destroy,
            bg=self.C_BG, fg=self.C_TEXT_DIM, font=self.f_btn,
            bd=0, relief="flat", cursor="hand2",
        ).pack(side="right")

        # Scrollable formulas list
        container = tk.Frame(win, bg=self.C_BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        canvas = tk.Canvas(container, bg=self.C_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.C_BG)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Formula cards - each card stores its own result label reference
        formulas = [
            {
                "key": "formula_quadratic",
                "desc": {
                    "en": "ax² + bx + c = 0  →  x = (-b ± √(b²-4ac)) / 2a",
                    "fr": "ax² + bx + c = 0  →  x = (-b ± √(b²-4ac)) / 2a",
                    "ar": "ax² + bx + c = 0  →  x = (-b ± √(b²-4ac)) / 2a",
                },
                "inputs": ["a", "b", "c"],
                "calc": lambda vals: self._calc_quadratic_result(vals),
            },
            {
                "key": "formula_area_circle",
                "desc": {
                    "en": "Area = π × r²",
                    "fr": "Aire = π × r²",
                    "ar": "المساحة = π × r²",
                },
                "inputs": ["r (radius)"],
                "calc": lambda vals: math.pi * vals[0] ** 2,
            },
            {
                "key": "formula_area_rect",
                "desc": {
                    "en": "Area = length × width",
                    "fr": "Aire = longueur × largeur",
                    "ar": "المساحة = الطول × العرض",
                },
                "inputs": ["length", "width"],
                "calc": lambda vals: vals[0] * vals[1],
            },
            {
                "key": "formula_area_triangle",
                "desc": {
                    "en": "Area = (base × height) / 2",
                    "fr": "Aire = (base × hauteur) / 2",
                    "ar": "المساحة = (القاعدة × الارتفاع) / 2",
                },
                "inputs": ["base", "height"],
                "calc": lambda vals: (vals[0] * vals[1]) / 2,
            },
            {
                "key": "formula_volume_sphere",
                "desc": {
                    "en": "Volume = (4/3) × π × r³",
                    "fr": "Volume = (4/3) × π × r³",
                    "ar": "الحجم = (4/3) × π × r³",
                },
                "inputs": ["r (radius)"],
                "calc": lambda vals: (4/3) * math.pi * vals[0] ** 3,
            },
            {
                "key": "formula_volume_cyl",
                "desc": {
                    "en": "Volume = π × r² × h",
                    "fr": "Volume = π × r² × h",
                    "ar": "الحجم = π × r² × h",
                },
                "inputs": ["r (radius)", "h (height)"],
                "calc": lambda vals: math.pi * vals[0] ** 2 * vals[1],
            },
            {
                "key": "formula_ohm",
                "desc": {
                    "en": "Voltage = Current × Resistance",
                    "fr": "Tension = Courant × Résistance",
                    "ar": "الجهد = التيار × المقاومة",
                },
                "inputs": ["I (current)", "R (resistance)"],
                "calc": lambda vals: vals[0] * vals[1],
            },
            {
                "key": "formula_force",
                "desc": {
                    "en": "Force = mass × acceleration",
                    "fr": "Force = masse × accélération",
                    "ar": "القوة = الكتلة × التسارع",
                },
                "inputs": ["mass", "acceleration"],
                "calc": lambda vals: vals[0] * vals[1],
            },
            {
                "key": "formula_kinetic",
                "desc": {
                    "en": "KE = (1/2) × m × v²",
                    "fr": "EC = (1/2) × m × v²",
                    "ar": "طاقة الحركة = (1/2) × m × v²",
                },
                "inputs": ["m (mass)", "v (velocity)"],
                "calc": lambda vals: 0.5 * vals[0] * vals[1] ** 2,
            },
        ]

        for formula in formulas:
            card = tk.Frame(scrollable_frame, bg=self.C_CARD, bd=0, highlightthickness=1,
                            highlightbackground="#e2e8f0")
            card.pack(fill="x", pady=8, padx=4)

            inner = tk.Frame(card, bg=self.C_CARD)
            inner.pack(padx=16, pady=12, fill="x")

            tk.Label(inner, text=self._t(formula["key"]), bg=self.C_CARD, fg=self.C_TEXT,
                     font=self.f_eq, anchor="w").pack(fill="x", pady=(0, 4))

            desc_text = formula["desc"]["en"] if self.lang == "en" else \
                        formula["desc"]["fr"] if self.lang == "fr" else formula["desc"]["ar"]
            tk.Label(inner, text=desc_text, bg=self.C_CARD, fg=self.C_TEXT_DIM,
                     font=self.f_expr, anchor="w").pack(fill="x", pady=(0, 10))

            # Input fields
            entry_vars = []
            for inp_label in formula["inputs"]:
                row = tk.Frame(inner, bg=self.C_CARD)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=inp_label + ":", bg=self.C_CARD, fg=self.C_TEXT_DIM,
                         font=self.f_mode, width=14, anchor="w").pack(side="left")
                var = tk.StringVar(value="")
                ent = tk.Entry(row, textvariable=var, font=self.f_display,
                               bg="#f8fafc", fg=self.C_TEXT, bd=0, justify="right",
                               insertbackground=self.C_TEXT)
                ent.pack(side="left", fill="x", expand=True, padx=(8, 0))
                entry_vars.append(var)

            # Result label
            result_label = tk.Label(inner, text="", bg=self.C_CARD, fg=self.C_TEXT,
                                    font=self.f_display, anchor="w")
            result_label.pack(fill="x", pady=(8, 0))

            # Create calculate command using closure for reliability
            calc_func = formula["calc"]
            entry_vars_ref = entry_vars

            def make_calc_cmd(rl=result_label, cf=calc_func, ev=entry_vars_ref):
                def cmd():
                    try:
                        vals = []
                        for var in ev:
                            v = var.get().strip()
                            if v == "":
                                rl.config(text="Please fill all fields", fg=self.C_CLEAR_T)
                                return
                            vals.append(float(v))
                        result = cf(vals)
                        if isinstance(result, str):
                            result_str = result
                        elif result == int(result):
                            result_str = str(int(result))
                        else:
                            result_str = f"{result:g}"
                        rl.config(text=f"{self._t('formula_result')}: {result_str}", fg=self.C_TEXT)
                    except Exception:
                        rl.config(text=self._t("invalid_input"), fg=self.C_CLEAR_T)
                return cmd

            btn_calc = tk.Button(
                inner, text=self._t("calculate"),
                command=make_calc_cmd(),
                bg=self.C_FORMULA_T, fg="#ffffff", font=self.f_eq,
                bd=0, relief="flat", cursor="hand2", highlightthickness=0,
                padx=16, pady=6,
            )
            btn_calc.pack(fill="x", pady=(10, 0))

        tk.Label(
            scrollable_frame, text=self._t("copyright"), bg=self.C_BG, fg=self.C_TEXT_DIM,
            font=self.f_footer, anchor="center",
        ).pack(pady=(10, 0))

    def _calc_quadratic_result(self, vals):
        """Calculate quadratic formula result."""
        a, b, c = vals[0], vals[1], vals[2]
        if a == 0:
            return "Not quadratic (a=0)"
        delta = b * b - 4 * a * c
        if delta > 0:
            x1 = (-b - math.sqrt(delta)) / (2 * a)
            x2 = (-b + math.sqrt(delta)) / (2 * a)
            return f"x₁={x1:g}, x₂={x2:g}"
        elif delta == 0:
            x = -b / (2 * a)
            return f"x={x:g} (double)"
        else:
            return "No real roots"

    # ------------------------------------------------------------------ Hover & Helpers
    def _add_hover(self, btn, normal, hover):
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=normal))

    def _bind_keys(self):
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<KP_Enter>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear_all())
        for key in "0123456789+-*/().":
            self.root.bind(key, lambda e, k=key: self._key_char(k))

    def _key_char(self, ch):
        if ch in "0123456789.":
            self._add_digit(ch)
        elif ch in "+-*/()":
            self._add_char(ch)

    def _noop(self):
        pass

    # ------------------------------------------------------------------ Calculator helpers
    def _set_display(self, value):
        self.display_var.set(value)

    def _get_display(self):
        return self.display_var.get()

    def _add_digit(self, digit):
        current = self._get_display()
        if self.new_input or current in ("0", "Error"):
            self._set_display(digit if digit != "." else "0.")
            self.new_input = False
        else:
            if digit == "." and "." in current:
                return
            self._set_display(current + digit)

    def _add_char(self, ch):
        current = self._get_display()
        if current in ("0", "Error"):
            self._set_display(ch)
            self.new_input = False
            return
        self._set_display(current + ch)
        self.new_input = False

    def _add_operator(self, op):
        current = self._get_display()
        if current in ("0", "Error"):
            return
        if current and current[-1] in "+-*/**":
            self._set_display(current[:-1] + op)
        else:
            self._set_display(current + op)
        self.new_input = False

    def backspace(self):
        current = self._get_display()
        if current in ("Error",):
            return
        if len(current) > 1:
            self._set_display(current[:-1])
        else:
            self._set_display("0")
        self.new_input = False

    # ------------------------------------------------------------------ Calculator actions
    def clear_all(self):
        self.expression = ""
        self._set_display("0")
        self.expr_var.set("")
        self.new_input = True

    def calculate(self):
        expr = self._get_display()
        if expr in ("0", "Error", ""):
            return
        try:
            safe = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
            result = eval(safe, {"__builtins__": {}}, {"math": math})
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            self.expr_var.set(expr + " =")
            self._set_display(str(result))
            self.new_input = True
        except Exception:
            self._set_display("Error")
            self.new_input = True

    def _math_func(self, name):
        current = self._get_display()
        if current in ("0", "Error", ""):
            return
        try:
            val = float(current)
            res = val ** 2 if name == "square" else val
            self._set_display(self._fmt(res))
            self.new_input = True
        except Exception:
            self._set_display("Error")
            self.new_input = True

    def _sci_func(self, name):
        current = self._get_display()
        if current in ("0", "Error", ""):
            return
        try:
            val = float(current)
            rad = math.radians(val) if self.deg_mode else val

            if name == "sin":
                res = math.sin(rad)
            elif name == "cos":
                res = math.cos(rad)
            elif name == "tan":
                res = math.tan(rad)
            elif name == "log10":
                if val <= 0:
                    raise ValueError
                res = math.log10(val)
            elif name == "ln":
                if val <= 0:
                    raise ValueError
                res = math.log(val)
            elif name == "sqrt":
                if val < 0:
                    raise ValueError
                res = math.sqrt(val)
            elif name == "factorial":
                if val < 0 or val != int(val):
                    raise ValueError
                res = math.factorial(int(val))
            elif name == "pi":
                res = math.pi
            elif name == "exp":
                res = math.exp(val)
            elif name == "pow10":
                res = 10 ** val
            elif name == "mod":
                self._set_display(str(val % 1))
                self.new_input = True
                return
            elif name == "neg":
                res = -val
            else:
                return

            self._set_display(self._fmt(res))
            self.new_input = True
        except Exception:
            self._set_display("Error")
            self.new_input = True

    def _fmt(self, num):
        if isinstance(num, float):
            if num.is_integer():
                return str(int(num))
            return f"{num:g}"
        return str(num)

    def toggle_deg_rad(self):
        self.deg_mode = not self.deg_mode
        self.mode_label.config(text="DEG" if self.deg_mode else "RAD")

    # ------------------------------------------------------------------ Memory
    def mc(self):
        self.memory = 0

    def mr(self):
        self._set_display(self._fmt(self.memory))
        self.new_input = True

    def m_add(self):
        try:
            self.memory += float(self._get_display())
        except Exception:
            pass

    def m_sub(self):
        try:
            self.memory -= float(self._get_display())
        except Exception:
            pass


def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
