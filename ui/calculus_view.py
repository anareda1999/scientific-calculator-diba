"""
ui/calculus_view.py
===================
Derivative, integral and root finder for arbitrary expressions.
"""

import tkinter as tk

from core.engine import ExprError, format_number


class CalculusView:
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
        win.title(self.t("calculus"))
        win.geometry("520x640")
        win.resizable(True, True)
        win.minsize(460, 540)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("calculus"), bg=th.BG, fg=th.TEXT,
                 font=self.f["title"]).pack(side="left", expand=True)
        tk.Button(header, text="✕", command=self.close, bg=th.BG, fg=th.TEXT_MUTE,
                  font=self.f["btn"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        body = tk.Frame(win, bg=th.BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        card = tk.Frame(body, bg=th.CARD, highlightthickness=1,
                        highlightbackground=th.BORDER)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=th.CARD)
        inner.pack(padx=20, pady=18, fill="both", expand=True)
        # grid layout: every row shares the same width, nothing gets squeezed
        inner.columnconfigure(0, weight=1)
        self._row = 0

        def add(widget, **kwargs):
            widget.grid(row=self._row, column=0, sticky="ew", **kwargs)
            self._row += 1
            return widget

        def add_label(text, font=None, color=None, pady=(0, 6)):
            lbl = tk.Label(inner, text=text, bg=th.CARD,
                           fg=color or th.TEXT_DIM, font=font or self.f["mode"],
                           anchor="w")
            add(lbl, pady=pady)
            return lbl

        add_label(self.t("expression"), pady=(0, 8))
        self.func_var = tk.StringVar(value="x^3 - 3*x")
        add(tk.Entry(inner, textvariable=self.func_var, font=self.f["display"],
                     bg="#f8fafc", fg=th.TEXT, bd=0, justify="center",
                     insertbackground=th.TEXT), pady=(0, 16))

        # ── Derivative ──
        add_label(self.t("derivative"), font=self.f["section"], color=th.TEXT)
        frame = tk.Frame(inner, bg=th.CARD)
        frame.columnconfigure(1, weight=1)
        tk.Label(frame, text=self.t("point"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], width=8, anchor="w").grid(row=0, column=0,
                                                                 sticky="w")
        self.point_var = tk.StringVar(value="1")
        tk.Entry(frame, textvariable=self.point_var, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=1, sticky="ew")
        add(frame, pady=(0, 12))

        add(tk.Button(inner, text=self.t("calculate"),
                      command=self.compute_derivative,
                      bg=th.CALCULUS_T, fg="#ffffff", font=self.f["section"], bd=0,
                      relief="flat", cursor="hand2", highlightthickness=0,
                      padx=16, pady=8), pady=(0, 10))
        self.deriv_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["display"], anchor="center")
        add(self.deriv_result, pady=(0, 20))

        # ── Integral ──
        add_label(self.t("integral"), font=self.f["section"], color=th.TEXT)
        frame2 = tk.Frame(inner, bg=th.CARD)
        frame2.columnconfigure(1, weight=1, uniform="bounds")
        frame2.columnconfigure(3, weight=1, uniform="bounds")
        tk.Label(frame2, text=self.t("lower_bound"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").grid(row=0, column=0, sticky="w")
        self.lower_var = tk.StringVar(value="0")
        tk.Entry(frame2, textvariable=self.lower_var, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=1, sticky="ew",
                                               padx=(0, 10))
        tk.Label(frame2, text=self.t("upper_bound"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").grid(row=0, column=2, sticky="w")
        self.upper_var = tk.StringVar(value="2")
        tk.Entry(frame2, textvariable=self.upper_var, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=3, sticky="ew")
        add(frame2, pady=(0, 12))

        add(tk.Button(inner, text=self.t("calculate"),
                      command=self.compute_integral,
                      bg=th.CALCULUS_T, fg="#ffffff", font=self.f["section"], bd=0,
                      relief="flat", cursor="hand2", highlightthickness=0,
                      padx=16, pady=8), pady=(0, 10))
        self.integ_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["display"], anchor="center")
        add(self.integ_result, pady=(0, 20))

        # ── Root finder ──
        add_label(self.t("find_roots"), font=self.f["section"], color=th.TEXT)
        frame3 = tk.Frame(inner, bg=th.CARD)
        frame3.columnconfigure(1, weight=1, uniform="roots")
        frame3.columnconfigure(3, weight=1, uniform="roots")
        tk.Label(frame3, text=self.t("interval"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").grid(row=0, column=0, sticky="w")
        self.root_from = tk.StringVar(value="-10")
        self.root_to = tk.StringVar(value="10")
        tk.Entry(frame3, textvariable=self.root_from, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=1, sticky="ew",
                                               padx=(0, 6))
        tk.Label(frame3, text="→", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"]).grid(row=0, column=2, padx=4)
        tk.Entry(frame3, textvariable=self.root_to, font=self.f["input"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right", width=8,
                 insertbackground=th.TEXT).grid(row=0, column=3, sticky="ew")
        add(frame3, pady=(0, 12))

        add(tk.Button(inner, text=self.t("find_roots"),
                      command=self.compute_roots,
                      bg=th.CALCULUS_T, fg="#ffffff", font=self.f["section"], bd=0,
                      relief="flat", cursor="hand2", highlightthickness=0,
                      padx=16, pady=8), pady=(0, 10))
        self.roots_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["display"], anchor="center",
                                     justify="center")
        add(self.roots_result)

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    def compute_derivative(self):
        try:
            ast = self.app.engine.parse(self.func_var.get())
            point = float(self.point_var.get())
            value = self.app.engine.derivative(ast, "x", point)
            self.deriv_result.config(
                text=f"f'({point:g}) = {format_number(value)}", fg=self.theme.TEXT)
        except ExprError as exc:
            self.deriv_result.config(text=self.t("invalid_input"),
                                     fg=self.theme.CLEAR_T)
        except ValueError:
            self.deriv_result.config(text=self.t("invalid_input"),
                                     fg=self.theme.CLEAR_T)

    def compute_integral(self):
        try:
            ast = self.app.engine.parse(self.func_var.get())
            low = float(self.lower_var.get())
            high = float(self.upper_var.get())
            value = self.app.engine.integral(ast, "x", low, high)
            self.integ_result.config(
                text=f"∫ = {format_number(value)}", fg=self.theme.TEXT)
        except ExprError as exc:
            self.integ_result.config(text=self.t("invalid_input"),
                                     fg=self.theme.CLEAR_T)
        except ValueError:
            self.integ_result.config(text=self.t("invalid_input"),
                                     fg=self.theme.CLEAR_T)

    def compute_roots(self):
        from core.equations import solve_numerically
        from core.engine import evaluate
        try:
            ast = self.app.engine.parse(self.func_var.get())

            def f(v):
                val = evaluate(ast, self.app.engine.context.with_variable("x", complex(v)))
                if abs(val.imag) > 1e-12:
                    raise ValueError
                return val.real

            roots = solve_numerically(f, "x", float(self.root_from.get()),
                                      float(self.root_to.get()))
            if roots:
                self.roots_result.config(
                    text="\n".join(f"x = {r:.10g}" for r in roots), fg=self.theme.TEXT)
            else:
                self.roots_result.config(text="No real root", fg=self.theme.TEXT_DIM)
        except Exception:
            self.roots_result.config(text=self.t("invalid_input"),
                                     fg=self.theme.CLEAR_T)
