"""
scientific_calculator.py
=========================
DIDA Scientific Calculator - entry point.

A multilingual (FR / EN / AR) scientific calculator with:
  * scientific keypad with memory, answer key and history tape
  * scientific constants library (c, g, h, k, NA, R, ...)
  * unit converter (weight, currency, volume, area, distance)
  * equation solver (1st degree, 2nd degree, expression, roots, systems)
  * Desmos-style graphing calculator with draggable sliders
  * scientific formulas library
  * matrix calculator
  * derivative / integral / root finder
  * descriptive statistics and linear regression

The expression engine (core/engine.py) uses a hand written tokenizer and
recursive-descent parser - no eval() / exec() anywhere.

Copyright © reda anagou
"""

import os
import sys
import tkinter as tk

# make the packages importable when the script is run directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine import Engine, ExprError, format_number
from ui.theme import Theme
from ui.i18n import STRINGS, LANGUAGES, translate
from ui.calculator_view import CalculatorView
from ui.grapher_view import GrapherView
from ui.converter_view import ConverterView
from ui.equations_view import EquationsView
from ui.formulas_view import FormulasView
from ui.matrix_view import MatrixView
from ui.calculus_view import CalculusView
from ui.stats_view import StatsView
from ui.advanced_view import AdvancedView

APP_NAME = "Scientific Calculator"
VERSION = "2.0.0"


class ScientificCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.theme = Theme()
        self.fonts = self.theme.fonts()
        self.lang = "fr"
        self.engine = Engine(angle_mode="rad")
        self.memory = 0.0
        self.last_answer = None
        self.history = []
        self.angle_mode = "rad"
        self.mode_var = tk.StringVar(value="RAD")

        self._create_views()
        self._build_header()
        self.calculator.build()

    # ── Translation helper ──────────────────────────────────────────
    def t(self, key):
        return translate(key, self.lang)

    # ── Shared helpers used by the views ───────────────────────────
    def add_hover(self, widget, normal, hover):
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal))

    def set_answer(self, value):
        self.last_answer = value
        self.calculator.ans_var.set(format_number(value))

    def add_history(self, expression, result):
        self.history.append((expression, format_number(result)))
        if len(self.history) > 200:
            self.history.pop(0)
        self.calculator._refresh_history()

    def show_error(self, message):
        """Show a transient error banner under the display."""
        if hasattr(self, "_error_label"):
            try:
                self._error_label.destroy()
            except Exception:
                pass
        self._error_label = tk.Label(
            self.root, text=message, bg=self.theme.CLEAR, fg=self.theme.CLEAR_T,
            font=self.fonts["footer"], anchor="w", padx=10, pady=4)
        self._error_label.pack(fill="x", padx=24, pady=(0, 8))
        self.root.after(4000, self._hide_error)

    def _hide_error(self):
        if hasattr(self, "_error_label"):
            try:
                self._error_label.destroy()
            except Exception:
                pass
            del self._error_label

    def toggle_angle_mode(self):
        self.angle_mode = "rad" if self.angle_mode == "deg" else "deg"
        self.engine.set_angle_mode(self.angle_mode)
        self.mode_var.set(self.angle_mode.upper())

    # ── Header / toolbar ───────────────────────────────────────────
    def _build_header(self):
        th = self.theme
        self.root.title(f"{self.t('app_title')} {VERSION}")
        self.root.geometry("1080x760")
        self.root.resizable(True, True)
        self.root.minsize(880, 640)
        self.root.configure(bg=th.BG)

        # Row 1 : language | title | angle mode
        top = tk.Frame(self.root, bg=th.BG, height=56)
        top.pack(fill="x", padx=20, pady=(16, 6))
        top.pack_propagate(False)

        self.lang_var = tk.StringVar(value=self.lang)
        for code, label in LANGUAGES:
            tk.Radiobutton(
                top, text=label, variable=self.lang_var, value=code,
                bg=th.BG, fg=th.TEXT, selectcolor=th.CARD, font=self.fonts["mode"],
                activebackground=th.BG, activeforeground=th.TEXT,
                command=lambda c=code: self.set_language(c),
                bd=0, highlightthickness=0, padx=6).pack(side="left", padx=(0, 4))

        tk.Label(top, text=self.t("app_title"), bg=th.BG, fg=th.TEXT,
                 font=self.fonts["btn"], anchor="center").pack(side="left",
                                                                expand=True, fill="x")

        self.mode_var = tk.StringVar(value=self.angle_mode.upper())
        tk.Label(top, textvariable=self.mode_var, bg=th.BG, fg=th.ACCENT,
                 font=self.fonts["mode"]).pack(side="right")

        # Row 2 : module buttons
        bar = tk.Frame(self.root, bg=th.BG, height=44)
        bar.pack(fill="x", padx=20, pady=(0, 10))
        bar.pack_propagate(False)

        modules = [
            ("converter", self.converter.open, th.CONVERT, th.CONVERT_T),
            ("equations", self.equations.open, th.EQUATION, th.EQUATION_T),
            ("grapher", self.grapher.open, th.GRAPH, th.GRAPH_T),
            ("formulas", self.formulas.open, th.FORMULA, th.FORMULA_T),
            ("matrices", self.matrices.open, th.MATRIX, th.MATRIX_T),
            ("calculus", self.calculus.open, th.CALCULUS, th.CALCULUS_T),
            ("advanced", self.advanced.open, th.ACCENT, "#ffffff"),
            ("statistics", self.statistics.open, th.STATS, th.STATS_T),
        ]
        for key, command, bg, fg in modules:
            tk.Button(bar, text=self.t(key), command=command, bg=bg, fg=fg,
                      activebackground=fg, activeforeground="#ffffff",
                      font=self.fonts["mode"], bd=0, relief="flat", cursor="hand2",
                      highlightthickness=0, padx=14, pady=7).pack(side="left",
                                                                  padx=(0, 8))

        # Footer
        footer = tk.Frame(self.root, bg=th.BG, height=26)
        footer.pack(fill="x", side="bottom", pady=(0, 8))
        footer.pack_propagate(False)
        tk.Label(footer, text=self.t("copyright"), bg=th.BG, fg=th.TEXT_DIM,
                 font=self.fonts["footer"]).pack(side="right")

    # ── Language switching ──────────────────────────────────────────
    def set_language(self, code):
        if code == self.lang:
            return
        self.lang = code
        # close every open window
        for view in (self.grapher, self.converter, self.equations, self.formulas,
                     self.matrices, self.calculus, self.statistics,
                     self.advanced):
            try:
                view.close()
            except Exception:
                pass
        # destroy the whole UI (including the toolbars) and rebuild it
        for child in self.root.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass
        self._create_views()
        self._build_header()
        self.calculator.build()

    def _create_views(self):
        """Instantiate every view (fresh widget references)."""
        self.calculator = CalculatorView(self)
        self.grapher = GrapherView(self)
        self.converter = ConverterView(self)
        self.equations = EquationsView(self)
        self.formulas = FormulasView(self)
        self.matrices = MatrixView(self)
        self.calculus = CalculusView(self)
        self.statistics = StatsView(self)
        self.advanced = AdvancedView(self)


def main():
    root = tk.Tk()
    app = ScientificCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
