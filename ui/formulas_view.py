"""
ui/formulas_view.py
===================
Scrollable library of scientific formulas.
"""

import math
import tkinter as tk
from tkinter import ttk

from core.engine import format_number


class FormulasView:
    def __init__(self, app):
        self.app = app
        self.theme = app.theme
        self.f = app.fonts
        self.t = app.t
        self.win = None

    def open(self):
        if self.win is not None and self.win.winfo_exists():
            self.win.lift()
            return
        th = self.theme
        win = tk.Toplevel(self.app.root)
        self.win = win
        win.title(self.t("formula_title"))
        win.geometry("560x700")
        win.resizable(True, True)
        win.minsize(500, 550)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("formula_title"), bg=th.BG, fg=th.TEXT,
                 font=self.f["title"]).pack(side="left", expand=True)
        tk.Button(header, text="✕", command=self.close, bg=th.BG, fg=th.TEXT_MUTE,
                  font=self.f["btn"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        container = tk.Frame(win, bg=th.BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        canvas = tk.Canvas(container, bg=th.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable = tk.Frame(canvas, bg=th.BG)
        self.scrollable.bind("<Configure>",
                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for key, desc, inputs, calc in self._formulas():
            self._card(key, desc, inputs, calc)

        tk.Label(self.scrollable, text=self.t("copyright"), bg=th.BG,
                 fg=th.TEXT_DIM, font=self.f["footer"],
                 anchor="center").pack(pady=(10, 0))

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    def _formulas(self):
        return [
            ("formula_quadratic",
             "ax² + bx + c = 0  →  x = (-b ± √(b²-4ac)) / 2a",
             ["a", "b", "c"], self._quadratic),
            ("formula_area_circle", "Area = π × r²", ["r (radius)"],
             lambda v: math.pi * v[0] ** 2),
            ("formula_area_rect", "Area = length × width", ["length", "width"],
             lambda v: v[0] * v[1]),
            ("formula_area_triangle", "Area = (base × height) / 2", ["base", "height"],
             lambda v: (v[0] * v[1]) / 2),
            ("formula_volume_sphere", "Volume = (4/3) × π × r³", ["r (radius)"],
             lambda v: (4 / 3) * math.pi * v[0] ** 3),
            ("formula_volume_cyl", "Volume = π × r² × h", ["r (radius)", "h (height)"],
             lambda v: math.pi * v[0] ** 2 * v[1]),
            ("formula_ohm", "Voltage = Current × Resistance",
             ["I (current)", "R (resistance)"], lambda v: v[0] * v[1]),
            ("formula_force", "Force = mass × acceleration", ["mass", "acceleration"],
             lambda v: v[0] * v[1]),
            ("formula_kinetic", "KE = (1/2) × m × v²", ["m (mass)", "v (velocity)"],
             lambda v: 0.5 * v[0] * v[1] ** 2),
        ]

    def _quadratic(self, vals):
        a, b, c = vals
        if a == 0:
            return "Not quadratic (a=0)"
        delta = b * b - 4 * a * c
        if delta < 0:
            return "No real roots"
        if delta == 0:
            return f"x={-b / (2 * a):g} (double)"
        r1 = (-b + math.sqrt(delta)) / (2 * a)
        r2 = (-b - math.sqrt(delta)) / (2 * a)
        return f"x₁={r1:g}, x₂={r2:g}"

    def _card(self, key, desc, inputs, calc):
        th = self.theme
        card = tk.Frame(self.scrollable, bg=th.CARD, highlightthickness=1,
                        highlightbackground=th.BORDER)
        card.pack(fill="x", pady=8, padx=4)
        inner = tk.Frame(card, bg=th.CARD)
        inner.pack(padx=16, pady=12, fill="x")

        tk.Label(inner, text=self.t(key), bg=th.CARD, fg=th.TEXT,
                 font=self.f["section"], anchor="w").pack(fill="x", pady=(0, 4))
        tk.Label(inner, text=desc, bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["expr"], anchor="w").pack(fill="x", pady=(0, 10))

        entry_vars = []
        for label in inputs:
            row = tk.Frame(inner, bg=th.CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label + ":", bg=th.CARD, fg=th.TEXT_DIM,
                     font=self.f["mode"], width=14, anchor="w").pack(side="left")
            var = tk.StringVar(value="")
            tk.Entry(row, textvariable=var, font=self.f["display"], bg="#f8fafc",
                     fg=th.TEXT, bd=0, justify="right",
                     insertbackground=th.TEXT).pack(side="left", fill="x",
                                                   expand=True, padx=(8, 0))
            entry_vars.append(var)

        result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                           font=self.f["display"], anchor="w")
        result.pack(fill="x", pady=(8, 0))

        def command(r=result, c=calc, ev=list(entry_vars)):
            try:
                vals = []
                for var in ev:
                    text = var.get().strip()
                    if text == "":
                        r.config(text="Please fill all fields", fg=th.CLEAR_T)
                        return
                    vals.append(float(text))
                value = c(vals)
                if isinstance(value, str):
                    text = value
                else:
                    text = format_number(complex(value))
                r.config(text=f"{self.t('result')}: {text}", fg=th.TEXT)
            except Exception:
                r.config(text=self.t("invalid_input"), fg=th.CLEAR_T)

        tk.Button(inner, text=self.t("calculate"), command=command,
                  bg=th.FORMULA_T, fg="#ffffff", font=self.f["section"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=16, pady=6).pack(fill="x", pady=(10, 0))
