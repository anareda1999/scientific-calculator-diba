"""
ui/equations_view.py
====================
Equation solver window: 1st degree, 2nd degree, expression evaluator,
root finder and linear systems.
"""

import tkinter as tk
from tkinter import ttk

from core.engine import ExprError, format_number
from core.equations import EquationError, solve_linear, solve_quadratic, solve_system
from core import equations as eq_mod


class EquationsView:
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
        win.title(self.t("eq_title"))
        win.geometry("500x660")
        win.resizable(True, True)
        win.minsize(440, 520)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("eq_title"), bg=th.BG, fg=th.TEXT,
                 font=self.f["title"]).pack(side="left", expand=True)
        tk.Button(header, text="✕", command=self.close, bg=th.BG, fg=th.TEXT_MUTE,
                  font=self.f["btn"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        nb = ttk.Notebook(win)
        nb.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=th.BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=th.CARD, foreground=th.TEXT_DIM,
                        padding=[14, 10], font=self.f["mode"])
        style.map("TNotebook.Tab", background=[("selected", th.CARD)],
                  foreground=[("selected", th.TEXT)])

        self._tab_linear(nb)
        self._tab_quadratic(nb)
        self._tab_expression(nb)
        self._tab_roots(nb)
        self._tab_system(nb)

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    # ── helpers ────────────────────────────────────────────────────
    def _label(self, parent, text, pady=(0, 4)):
        tk.Label(parent, text=text, bg=self.theme.CARD, fg=self.theme.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=pady)

    def _entry(self, parent, var, mono=False):
        e = tk.Entry(parent, textvariable=var,
                     font=self.f["mono"] if mono else self.f["display"],
                     bg="#f8fafc", fg=self.theme.TEXT, bd=0, justify="right",
                     insertbackground=self.theme.TEXT)
        e.pack(fill="x", pady=(0, 12))
        return e

    def _solve_button(self, parent, command, text=None):
        tk.Button(parent, text=text or self.t("solve"), command=command,
                  bg=self.theme.EQUATION_T, fg="#ffffff", font=self.f["section"],
                  bd=0, relief="flat", cursor="hand2", highlightthickness=0,
                  padx=20, pady=10).pack(fill="x", pady=(0, 16))

    def _result_label(self, parent):
        lbl = tk.Label(parent, text="", bg=self.theme.CARD, fg=self.theme.TEXT,
                       font=self.f["display"], anchor="center", justify="center")
        lbl.pack(fill="x", pady=(4, 0))
        return lbl

    def _coeff(self, text):
        """Evaluate a coefficient with the engine (supports sin, cos, ...)."""
        try:
            return self.app.engine.evaluate_text(text)
        except ExprError:
            raise

    # ── Tab 1: 1st degree ──────────────────────────────────────────
    def _tab_linear(self, nb):
        th = self.theme
        tab = tk.Frame(nb, bg=th.CARD)
        nb.add(tab, text=self.t("eq1_tab"))
        inner = tk.Frame(tab, bg=th.CARD)
        inner.pack(padx=24, pady=20, fill="both", expand=True)

        tk.Label(inner, text="ax + b = 0", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 14))

        self._label(inner, self.t("coeff_a"))
        self.lin_a = tk.StringVar(value="")
        self._entry(inner, self.lin_a)

        self._label(inner, self.t("coeff_b"))
        self.lin_b = tk.StringVar(value="")
        self._entry(inner, self.lin_b)

        self._solve_button(inner, self.solve_linear)
        self.lin_result = self._result_label(inner)
        self.lin_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                 font=self.f["footer"], anchor="center")
        self.lin_note.pack(fill="x")

    def solve_linear(self):
        try:
            a = self._coeff(self.lin_a.get())
            b = self._coeff(self.lin_b.get())
        except ExprError as exc:
            self.lin_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.lin_note.config(text=str(exc))
            return
        root, kind = solve_linear(a, b)
        if kind == "unique":
            self.lin_result.config(text=f"x = {format_number(root)}", fg=self.theme.TEXT)
            self.lin_note.config(text="")
        elif kind == "infinite":
            self.lin_result.config(text=self.t("inf_solutions"), fg=self.theme.TEXT_DIM)
            self.lin_note.config(text="")
        else:
            self.lin_result.config(text=self.t("no_solution"), fg=self.theme.CLEAR_T)
            self.lin_note.config(text="")

    # ── Tab 2: 2nd degree ──────────────────────────────────────────
    def _tab_quadratic(self, nb):
        th = self.theme
        tab = tk.Frame(nb, bg=th.CARD)
        nb.add(tab, text=self.t("eq2_tab"))
        inner = tk.Frame(tab, bg=th.CARD)
        inner.pack(padx=24, pady=20, fill="both", expand=True)

        tk.Label(inner, text="ax² + bx + c = 0", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 14))

        self._label(inner, self.t("coeff_a"))
        self.quad_a = tk.StringVar(value="")
        self._entry(inner, self.quad_a)

        self._label(inner, self.t("coeff_b"))
        self.quad_b = tk.StringVar(value="")
        self._entry(inner, self.quad_b)

        self._label(inner, self.t("coeff_c"))
        self.quad_c = tk.StringVar(value="")
        self._entry(inner, self.quad_c)

        self._solve_button(inner, self.solve_quadratic)
        self.quad_result = self._result_label(inner)
        self.quad_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                  font=self.f["mode"], anchor="center", justify="center")
        self.quad_note.pack(fill="x")

    def solve_quadratic(self):
        try:
            a = self._coeff(self.quad_a.get())
            b = self._coeff(self.quad_b.get())
            c = self._coeff(self.quad_c.get())
        except ExprError as exc:
            self.quad_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.quad_note.config(text=str(exc))
            return
        roots, delta, kind = solve_quadratic(a, b, c)
        if kind == "two":
            self.quad_result.config(
                text=f"x₁ = {format_number(roots[0])}\nx₂ = {format_number(roots[1])}",
                fg=self.theme.TEXT)
            self.quad_note.config(text=f"Δ = {format_number(delta)}")
        elif kind == "double":
            self.quad_result.config(
                text=f"x₀ = {format_number(roots[0])}", fg=self.theme.TEXT)
            self.quad_note.config(text="Δ = 0 (double root)")
        elif kind == "linear":
            self.quad_result.config(
                text=f"x = {format_number(roots[0])}", fg=self.theme.TEXT)
            self.quad_note.config(text="a = 0 → 1st degree")
        elif kind == "infinite":
            self.quad_result.config(text=self.t("inf_solutions"), fg=self.theme.TEXT_DIM)
            self.quad_note.config(text="")
        else:
            self.quad_result.config(text=self.t("no_solution"), fg=self.theme.CLEAR_T)
            self.quad_note.config(text=f"Δ = {format_number(delta)}")

    # ── Tab 3: expression ──────────────────────────────────────────
    def _tab_expression(self, nb):
        th = self.theme
        tab = tk.Frame(nb, bg=th.CARD)
        nb.add(tab, text=self.t("eq_expr_tab"))
        inner = tk.Frame(tab, bg=th.CARD)
        inner.pack(padx=24, pady=20, fill="both", expand=True)

        self._label(inner, self.t("expression"), (0, 10))
        self.expr_text = tk.StringVar(value="sin(x) + cos(x) - 1")
        self._entry(inner, self.expr_text)

        self._label(inner, self.t("value_of_x"), (0, 10))
        self.expr_x = tk.StringVar(value="0")
        self._entry(inner, self.expr_x)

        self._solve_button(inner, self.eval_expression, self.t("calculate"))
        self.expr_result = self._result_label(inner)
        self.expr_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                  font=self.f["footer"], anchor="center")
        self.expr_note.pack(fill="x")

    def eval_expression(self):
        try:
            text = self.expr_text.get().strip()
            if not text:
                raise ExprError("Aucune expression")
            x_text = self.expr_x.get().strip()
            if x_text == "":
                raise ExprError("Valeur de x manquante")
            x = complex(float(x_text))
            ast = self.app.engine.parse(text)
            value = self.app.engine.evaluate(ast) if False else None
            from core.engine import evaluate
            value = evaluate(ast, self.app.engine.context.with_variable("x", x))
            self.expr_result.config(text=f"{self.t('result')}: {format_number(value)}",
                                    fg=self.theme.TEXT)
            self.expr_note.config(text="")
        except ExprError as exc:
            self.expr_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.expr_note.config(text=str(exc))
        except ValueError:
            self.expr_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.expr_note.config(text="Valeur de x invalide")

    # ── Tab 4: root finder ────────────────────────────────────────
    def _tab_roots(self, nb):
        th = self.theme
        tab = tk.Frame(nb, bg=th.CARD)
        nb.add(tab, text=self.t("find_roots"))
        inner = tk.Frame(tab, bg=th.CARD)
        inner.pack(padx=24, pady=20, fill="both", expand=True)

        self._label(inner, self.t("expression"), (0, 10))
        self.root_text = tk.StringVar(value="x^2 - 4")
        self._entry(inner, self.root_text)

        self._label(inner, self.t("interval"), (0, 10))
        frame = tk.Frame(inner, bg=th.CARD)
        frame.pack(fill="x", pady=(0, 12))
        self.root_from = tk.StringVar(value="-10")
        self.root_to = tk.StringVar(value="10")
        for var, label in ((self.root_from, "from"), (self.root_to, "to")):
            e = tk.Entry(frame, textvariable=var, font=self.f["display"],
                         bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                         insertbackground=th.TEXT)
            e.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(frame, text="→", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"]).pack(side="left", padx=(0, 8))

        self._solve_button(inner, self.find_roots, self.t("find_roots"))
        self.roots_result = self._result_label(inner)
        self.roots_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                   font=self.f["footer"], anchor="center")
        self.roots_note.pack(fill="x")

    def find_roots(self):
        try:
            text = self.root_text.get().strip()
            ast = self.app.engine.parse(text)
            from core.engine import evaluate

            def f(v):
                val = evaluate(ast, self.app.engine.context.with_variable("x", complex(v)))
                if abs(val.imag) > 1e-12:
                    raise ValueError("complex")
                return val.real

            lo = float(self.root_from.get())
            hi = float(self.root_to.get())
            roots = eq_mod.solve_numerically(f, "x", lo, hi)
            if roots:
                self.roots_result.config(
                    text="\n".join(f"x = {r:.10g}" for r in roots), fg=self.theme.TEXT)
                self.roots_note.config(text=f"{len(roots)} root(s) found")
            else:
                self.roots_result.config(text="No real root", fg=self.theme.TEXT_DIM)
                self.roots_note.config(text="")
        except ExprError as exc:
            self.roots_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.roots_note.config(text=str(exc))
        except Exception as exc:
            self.roots_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.roots_note.config(text=str(exc))

    # ── Tab 5: linear system ───────────────────────────────────────
    def _tab_system(self, nb):
        th = self.theme
        tab = tk.Frame(nb, bg=th.CARD)
        nb.add(tab, text=self.t("eq_system_tab"))
        inner = tk.Frame(tab, bg=th.CARD)
        inner.pack(padx=24, pady=18, fill="both", expand=True)

        tk.Label(inner, text=self.t("system_size"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 6))
        self.sys_size = tk.IntVar(value=2)
        size_frame = tk.Frame(inner, bg=th.CARD)
        size_frame.pack(fill="x", pady=(0, 12))
        for n in (2, 3):
            rb = tk.Radiobutton(size_frame, text=f"{n}×{n}", variable=self.sys_size,
                                value=n, bg=th.CARD, fg=th.TEXT, selectcolor=th.CARD,
                                font=self.f["mode"], activebackground=th.CARD,
                                activeforeground=th.TEXT, command=self._rebuild_system,
                                bd=0, highlightthickness=0, padx=8)
            rb.pack(side="left")

        self.sys_frame = tk.Frame(inner, bg=th.CARD)
        self.sys_frame.pack(fill="both", expand=True)

        self._solve_button(inner, self.solve_system)
        self.sys_result = self._result_label(inner)
        self.sys_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                 font=self.f["footer"], anchor="center", justify="center")
        self.sys_note.pack(fill="x")

        self.sys_vars = []
        self._rebuild_system()

    def _rebuild_system(self):
        for child in self.sys_frame.winfo_children():
            child.destroy()
        self.sys_vars = []
        n = self.sys_size.get()
        for row in range(n):
            frame = tk.Frame(self.sys_frame, bg=self.theme.CARD)
            frame.pack(fill="x", pady=4)
            for col in range(n + 1):
                var = tk.StringVar(value="")
                e = tk.Entry(frame, textvariable=var, font=self.f["display"],
                             bg="#f8fafc", fg=self.theme.TEXT, bd=0, justify="right",
                             insertbackground=self.theme.TEXT, width=6)
                e.pack(side="left", fill="x", expand=True, padx=3)
                self.sys_vars.append(var)
            tk.Label(frame, text="=", bg=self.theme.CARD, fg=self.theme.TEXT_DIM,
                     font=self.f["mode"]).pack(side="left", padx=4)

    def solve_system(self):
        try:
            n = self.sys_size.get()
            rows = []
            for r in range(n):
                row = []
                for c in range(n + 1):
                    var = self.sys_vars[r * (n + 1) + c]
                    text = var.get().strip()
                    if text == "":
                        text = "0"
                    row.append(self.app.engine.evaluate_text(text))
                rows.append(row)
            solution, kind = solve_system(rows, n)
            if kind == "unique":
                names = ["x", "y", "z"][:n]
                self.sys_result.config(
                    text="\n".join(f"{names[i]} = {format_number(v)}"
                                    for i, v in enumerate(solution)),
                    fg=self.theme.TEXT)
                self.sys_note.config(text="")
            elif kind == "infinite":
                self.sys_result.config(text=self.t("inf_solutions"), fg=self.theme.TEXT_DIM)
                self.sys_note.config(text="")
            else:
                self.sys_result.config(text=self.t("no_solution"), fg=self.theme.CLEAR_T)
                self.sys_note.config(text="")
        except (ExprError, EquationError) as exc:
            self.sys_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.sys_note.config(text=str(exc))
        except Exception as exc:
            self.sys_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.sys_note.config(text=str(exc))
