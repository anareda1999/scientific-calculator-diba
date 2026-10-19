"""
ui/advanced_view.py
===================
Advanced analysis window with four tabs:

* Limits          lim f(x) as x -> a / a- / a+ / +-oo
* Taylor          expansion of f around a point
* Inequalities    solving f(x) > 0 and f(x) < 0
* Differential equations  y' = f(x,y)  and  y'' = f(x,y,y')
"""

import math
import tkinter as tk
from tkinter import ttk

from core import calculus
from core.engine import ExprError, format_number


class AdvancedView:
    def __init__(self, app):
        self.app = app
        self.theme = app.theme
        self.f = app.fonts
        self.t = app.t
        self.win = None

    # ── window ────────────────────────────────────────────────────
    def open(self):
        if self.win is not None and self.win.winfo_exists():
            self.win.lift()
            return
        th = self.theme
        win = tk.Toplevel(self.app.root)
        self.win = win
        win.title(self.t("advanced_title"))
        win.geometry("600x700")
        win.resizable(True, True)
        win.minsize(520, 600)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("advanced_title"), bg=th.BG, fg=th.TEXT,
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

        self._tab_limits(nb)
        self._tab_taylor(nb)
        self._tab_inequality(nb)
        self._tab_ode(nb)

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    # ── generic builders ──────────────────────────────────────────
    def _card(self, nb):
        tab = tk.Frame(nb, bg=self.theme.CARD)
        nb.add(tab)
        inner = tk.Frame(tab, bg=self.theme.CARD)
        inner.pack(padx=24, pady=20, fill="both", expand=True)
        inner.columnconfigure(0, weight=1)
        return inner

    def _label(self, parent, text, pady=(0, 5), color=None):
        lbl = tk.Label(parent, text=text, bg=self.theme.CARD,
                       fg=color or self.theme.TEXT_DIM, font=self.f["mode"],
                       anchor="w")
        lbl.grid(row=self._row(parent), column=0, sticky="ew", pady=pady)
        return lbl

    def _entry(self, parent, var, width=12, font=None):
        ent = tk.Entry(parent, textvariable=var, font=font or self.f["input"],
                       bg="#f8fafc", fg=self.theme.TEXT, bd=0, justify="right",
                       width=width, insertbackground=self.theme.TEXT)
        ent.grid(row=self._row(parent), column=0, sticky="ew", pady=(0, 12))
        return ent

    def _row(self, parent):
        row = getattr(parent, "_next_row", 0)
        parent._next_row = row + 1
        return row

    def _button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command,
                        bg=self.theme.CALCULUS_T, fg="#ffffff",
                        font=self.f["section"], bd=0, relief="flat",
                        cursor="hand2", highlightthickness=0, padx=16, pady=8)
        btn.grid(row=self._row(parent), column=0, sticky="ew", pady=(0, 12))
        return btn

    def _result(self, parent):
        lbl = tk.Label(parent, text="", bg=self.theme.CARD, fg=self.theme.TEXT,
                       font=self.f["input"], anchor="w", justify="left",
                       wraplength=520)
        lbl.grid(row=self._row(parent), column=0, sticky="ew", pady=(0, 8))
        return lbl

    def _parse(self, text):
        return self.app.engine.parse(text)

    # ══════════════════════════════════════════════════════════
    #  Tab 1 : Limits
    # ══════════════════════════════════════════════════════════
    def _tab_limits(self, nb):
        inner = self._card(nb)
        inner._next_row = 0
        th = self.theme

        self._label(inner, self.t("expression"))
        self.lim_expr = tk.StringVar(value="(x^2-1)/(x-1)")
        self._entry(inner, self.lim_expr, width=16, font=self.f["display"])

        self._label(inner, self.t("limit_point"))
        self.lim_point = tk.StringVar(value="1")
        self._entry(inner, self.lim_point, width=16, font=self.f["display"])

        # direction
        self._label(inner, self.t("limit_direction"))
        row = tk.Frame(inner, bg=th.CARD)
        row.grid(row=self._row(inner), column=0, sticky="ew", pady=(0, 12))
        self.lim_dir = tk.StringVar(value="both")
        for value, label in (("both", self.t("lim_both")),
                             ("right", self.t("lim_right")),
                             ("left", self.t("lim_left"))):
            tk.Radiobutton(row, text=label, variable=self.lim_dir, value=value,
                           bg=th.CARD, fg=th.TEXT, selectcolor=th.CARD,
                           font=self.f["mode"], activebackground=th.CARD,
                           activeforeground=th.TEXT, bd=0,
                           highlightthickness=0, padx=8).pack(side="left")

        self._button(inner, self.t("calculate"), self._do_limit)
        self.lim_result = self._result(inner)
        self.lim_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                 font=self.f["footer"], anchor="w",
                                 wraplength=520)
        self.lim_note.grid(row=self._row(inner), column=0, sticky="ew")

    def _do_limit(self):
        try:
            ast = self._parse(self.lim_expr.get())
            point = self.lim_point.get().strip()
            direction = {"both": 0, "right": 1, "left": -1}[self.lim_dir.get()]
            value, kind, note = calculus.limit(ast, self.app.engine, "x",
                                               point, direction)
            if value.imag == 0:
                if math.isinf(value.real):
                    shown = "+∞" if value.real > 0 else "-∞"
                else:
                    shown = f"{value.real:g}"
            else:
                shown = format_number(value)
            self.lim_result.config(text=f"{self.t('lim_result')} : {shown}",
                                   fg=self.theme.TEXT)
            self.lim_note.config(text=note)
        except ExprError as exc:
            self.lim_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.lim_note.config(text=str(exc))
        except Exception as exc:
            self.lim_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.lim_note.config(text=str(exc))

    # ══════════════════════════════════════════════════════════
    #  Tab 2 : Taylor
    # ══════════════════════════════════════════════════════════
    def _tab_taylor(self, nb):
        inner = self._card(nb)
        inner._next_row = 0

        self._label(inner, self.t("expression"))
        self.tay_expr = tk.StringVar(value="sin(x)")
        self._entry(inner, self.tay_expr, width=16, font=self.f["display"])

        self._label(inner, self.t("taylor_point"))
        self.tay_point = tk.StringVar(value="0")
        self._entry(inner, self.tay_point, width=16, font=self.f["display"])

        self._label(inner, self.t("taylor_order"))
        self.tay_order = tk.StringVar(value="4")
        self._entry(inner, self.tay_order, width=16)

        self._button(inner, self.t("calculate"), self._do_taylor)
        self.tay_result = self._result(inner)
        self.tay_note = tk.Label(inner, text="", bg=self.theme.CARD,
                                 fg=self.theme.TEXT_DIM, font=self.f["footer"],
                                 anchor="w", justify="left", wraplength=520)
        self.tay_note.grid(row=self._row(inner), column=0, sticky="ew")

    def _do_taylor(self):
        try:
            ast = self._parse(self.tay_expr.get())
            point = float(self.tay_point.get())
            order = int(float(self.tay_order.get()))
            terms = calculus.taylor_series(ast, self.app.engine, "x", point, order)
            poly = calculus.format_taylor(terms, "x", point)
            self.tay_result.config(text=f"f(x) ≈ {poly}", fg=self.theme.TEXT)
            lines = []
            for k, deriv, coeff in terms:
                lines.append(f"f^({k})({point:g}) = {deriv:.10g}   "
                             f"terme : {coeff:.10g}/n! · (x-{point:g})^{k}")
            self.tay_note.config(text="\n".join(lines))
        except ExprError as exc:
            self.tay_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.tay_note.config(text=str(exc))
        except Exception as exc:
            self.tay_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.tay_note.config(text=str(exc))

    # ══════════════════════════════════════════════════════════
    #  Tab 3 : Inequalities
    # ══════════════════════════════════════════════════════════
    def _tab_inequality(self, nb):
        inner = self._card(nb)
        inner._next_row = 0
        th = self.theme

        self._label(inner, self.t("ineq_expression"))
        self.ineq_expr = tk.StringVar(value="x^2 - 4")
        self._entry(inner, self.ineq_expr, width=16, font=self.f["display"])

        self._label(inner, self.t("ineq_sign"))
        row = tk.Frame(inner, bg=th.CARD)
        row.grid(row=self._row(inner), column=0, sticky="ew", pady=(0, 12))
        self.ineq_sign = tk.StringVar(value="gt")
        for value, label in (("gt", "f(x) > 0"), ("ge", "f(x) ≥ 0"),
                             ("lt", "f(x) < 0"), ("le", "f(x) ≤ 0")):
            tk.Radiobutton(row, text=label, variable=self.ineq_sign, value=value,
                           bg=th.CARD, fg=th.TEXT, selectcolor=th.CARD,
                           font=self.f["mode"], activebackground=th.CARD,
                           activeforeground=th.TEXT, bd=0,
                           highlightthickness=0, padx=8).pack(side="left")

        self._label(inner, self.t("interval"))
        frame = tk.Frame(inner, bg=th.CARD)
        frame.grid(row=self._row(inner), column=0, sticky="ew", pady=(0, 12))
        frame.columnconfigure(0, weight=1, uniform="iv")
        frame.columnconfigure(2, weight=1, uniform="iv")
        self.ineq_lo = tk.StringVar(value="-10")
        self.ineq_hi = tk.StringVar(value="10")
        tk.Entry(frame, textvariable=self.ineq_lo, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=0, sticky="ew",
                                               padx=(0, 6))
        tk.Label(frame, text="→", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"]).grid(row=0, column=1, padx=4)
        tk.Entry(frame, textvariable=self.ineq_hi, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=2, sticky="ew")

        self._button(inner, self.t("calculate"), self._do_inequality)
        self.ineq_result = self._result(inner)
        self.ineq_note = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT_DIM,
                                  font=self.f["footer"], anchor="w",
                                  wraplength=520)
        self.ineq_note.grid(row=self._row(inner), column=0, sticky="ew")

    def _do_inequality(self):
        try:
            ast = self._parse(self.ineq_expr.get())
            sign_map = {"gt": (1, True), "ge": (1, False),
                        "lt": (-1, True), "le": (-1, False)}
            sign, strict = sign_map[self.ineq_sign.get()]
            lo = float(self.ineq_lo.get())
            hi = float(self.ineq_hi.get())
            intervals = calculus.solve_inequality(ast, self.app.engine, "x",
                                                  lo, hi, sign, strict=strict)
            self.ineq_result.config(text=calculus.format_solution(intervals),
                                    fg=self.theme.TEXT)
            self.ineq_note.config(text=self.t("ineq_note"))
        except ExprError as exc:
            self.ineq_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.ineq_note.config(text=str(exc))
        except Exception as exc:
            self.ineq_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
            self.ineq_note.config(text=str(exc))

    # ══════════════════════════════════════════════════════════
    #  Tab 4 : Differential equations
    # ══════════════════════════════════════════════════════════
    def _tab_ode(self, nb):
        inner = self._card(nb)
        inner._next_row = 0
        th = self.theme

        self._label(inner, self.t("ode_expression"))
        self.ode_expr = tk.StringVar(value="y")
        self._entry(inner, self.ode_expr, width=16, font=self.f["display"])

        self._label(inner, self.t("ode_order"))
        row = tk.Frame(inner, bg=th.CARD)
        row.grid(row=self._row(inner), column=0, sticky="ew", pady=(0, 12))
        self.ode_order = tk.StringVar(value="1")
        for value, label in (("1", "y' = f(x, y)"), ("2", "y'' = f(x, y, y')")):
            tk.Radiobutton(row, text=label, variable=self.ode_order, value=value,
                           bg=th.CARD, fg=th.TEXT, selectcolor=th.CARD,
                           font=self.f["mode"], activebackground=th.CARD,
                           activeforeground=th.TEXT, bd=0,
                           highlightthickness=0, padx=8).pack(side="left")

        self._label(inner, self.t("ode_initial"))
        frame = tk.Frame(inner, bg=th.CARD)
        frame.grid(row=self._row(inner), column=0, sticky="ew", pady=(0, 12))
        frame.columnconfigure(0, weight=1, uniform="ode")
        frame.columnconfigure(2, weight=1, uniform="ode")
        frame.columnconfigure(4, weight=1, uniform="ode")
        self.ode_x0 = tk.StringVar(value="0")
        self.ode_y0 = tk.StringVar(value="1")
        self.ode_dy0 = tk.StringVar(value="0")
        for col, var, title in ((0, self.ode_x0, "x0"),
                                 (2, self.ode_y0, "y(x0)"),
                                 (4, self.ode_dy0, "y'(x0)")):
            tk.Label(frame, text=title, bg=th.CARD, fg=th.TEXT_DIM,
                     font=self.f["mode"], anchor="w").grid(row=0, column=col,
                                                           sticky="w")
            tk.Entry(frame, textvariable=var, font=self.f["input"], bg="#f8fafc",
                     fg=th.TEXT, bd=0, justify="right", width=6,
                     insertbackground=th.TEXT).grid(row=1, column=col, sticky="ew",
                                                   padx=(0, 8))
        frame.rowconfigure(1, weight=1)

        self._label(inner, self.t("ode_range"))
        frame2 = tk.Frame(inner, bg=th.CARD)
        frame2.grid(row=self._row(inner), column=0, sticky="ew", pady=(0, 12))
        frame2.columnconfigure(0, weight=1, uniform="ode2")
        frame2.columnconfigure(2, weight=1, uniform="ode2")
        frame2.columnconfigure(4, weight=1, uniform="ode2")
        self.ode_xend = tk.StringVar(value="10")
        self.ode_steps = tk.StringVar(value="100")
        for col, var, title in ((0, self.ode_xend, "x final"),
                                 (2, self.ode_steps, "pas"),
                                 (4, tk.StringVar(value=""), "")):
            if title:
                tk.Label(frame2, text=title, bg=th.CARD, fg=th.TEXT_DIM,
                         font=self.f["mode"], anchor="w").grid(row=0, column=col,
                                                               sticky="w")
                tk.Entry(frame2, textvariable=var, font=self.f["input"],
                         bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=6,
                         insertbackground=th.TEXT).grid(row=1, column=col, sticky="ew",
                                                       padx=(0, 8))

        self._button(inner, self.t("calculate"), self._do_ode)
        self.ode_result = self._result(inner)
        self.ode_table = tk.Text(inner, height=9, font=self.f["mono"],
                                 bg="#f8fafc", fg=th.TEXT, bd=0, wrap="none",
                                 insertbackground=th.TEXT)
        self.ode_table.grid(row=self._row(inner), column=0, sticky="nsew",
                             pady=(0, 8))
        inner.rowconfigure(self._row(inner) - 1, weight=1)

    def _do_ode(self):
        try:
            ast = self._parse(self.ode_expr.get())
            order = int(self.ode_order.get())
            points = calculus.solve_ode(
                ast, self.app.engine, "x",
                x0=float(self.ode_x0.get()),
                y0=float(self.ode_y0.get()),
                x_end=float(self.ode_xend.get()),
                steps=int(float(self.ode_steps.get())),
                order=order,
                dy0=float(self.ode_dy0.get()))

            self.ode_table.delete("1.0", "end")
            self.ode_table.insert("end", f"{'x':>12}   {'y(x)':>16}\n")
            self.ode_table.insert("end", "-" * 32 + "\n")
            step = max(1, len(points) // 12)
            for i, (x, y) in enumerate(points):
                if i % step == 0 or i == len(points) - 1:
                    self.ode_table.insert("end", f"{x:>12.6g}   {y:>16.10g}\n")

            last = points[-1]
            self.ode_result.config(
                text=f"{self.t('ode_result')} : y({last[0]:.6g}) = {last[1]:.10g}",
                fg=self.theme.TEXT)
        except ExprError as exc:
            self.ode_result.config(text=self.t("invalid_input"), fg=self.theme.CLEAR_T)
        except Exception as exc:
            self.ode_result.config(text=str(exc), fg=self.theme.CLEAR_T)
