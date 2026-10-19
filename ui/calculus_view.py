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

        tk.Label(inner, text=self.t("expression"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 8))
        self.func_var = tk.StringVar(value="x^3 - 3*x")
        tk.Entry(inner, textvariable=self.func_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="center",
                 insertbackground=th.TEXT).pack(fill="x", pady=(0, 16))

        # Derivative
        tk.Label(inner, text=self.t("derivative"), bg=th.CARD, fg=th.TEXT,
                 font=self.f["section"], anchor="w").pack(fill="x", pady=(0, 6))
        frame = tk.Frame(inner, bg=th.CARD)
        frame.pack(fill="x", pady=(0, 12))
        tk.Label(frame, text=self.t("point"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], width=8, anchor="w").pack(side="left")
        self.point_var = tk.StringVar(value="1")
        tk.Entry(frame, textvariable=self.point_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                 insertbackground=th.TEXT).pack(side="left", fill="x", expand=True)

        tk.Button(inner, text=self.t("calculate"), command=self.compute_derivative,
                  bg=th.CALCULUS_T, fg="#ffffff", font=self.f["section"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=16, pady=8).pack(fill="x", pady=(0, 10))
        self.deriv_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["display"], anchor="center")
        self.deriv_result.pack(fill="x", pady=(0, 20))

        # Integral
        tk.Label(inner, text=self.t("integral"), bg=th.CARD, fg=th.TEXT,
                 font=self.f["section"], anchor="w").pack(fill="x", pady=(0, 6))
        frame2 = tk.Frame(inner, bg=th.CARD)
        frame2.pack(fill="x", pady=(0, 12))
        tk.Label(frame2, text=self.t("lower_bound"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], width=14, anchor="w").pack(side="left")
        self.lower_var = tk.StringVar(value="0")
        tk.Entry(frame2, textvariable=self.lower_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                 insertbackground=th.TEXT).pack(side="left", fill="x", expand=True)
        tk.Label(frame2, text=self.t("upper_bound"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], width=14, anchor="w").pack(side="left")
        self.upper_var = tk.StringVar(value="2")
        tk.Entry(frame2, textvariable=self.upper_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                 insertbackground=th.TEXT).pack(side="left", fill="x", expand=True)

        tk.Button(inner, text=self.t("calculate"), command=self.compute_integral,
                  bg=th.CALCULUS_T, fg="#ffffff", font=self.f["section"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=16, pady=8).pack(fill="x", pady=(0, 10))
        self.integ_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["display"], anchor="center")
        self.integ_result.pack(fill="x", pady=(0, 20))

        # Root finder
        tk.Label(inner, text=self.t("find_roots"), bg=th.CARD, fg=th.TEXT,
                 font=self.f["section"], anchor="w").pack(fill="x", pady=(0, 6))
        frame3 = tk.Frame(inner, bg=th.CARD)
        frame3.pack(fill="x", pady=(0, 12))
        tk.Label(frame3, text=self.t("interval"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], width=8, anchor="w").pack(side="left")
        self.root_from = tk.StringVar(value="-10")
        self.root_to = tk.StringVar(value="10")
        for var in (self.root_from, self.root_to):
            tk.Entry(frame3, textvariable=var, font=self.f["display"], bg="#f8fafc",
                     fg=th.TEXT, bd=0, justify="right",
                     insertbackground=th.TEXT).pack(side="left", fill="x", expand=True,
                                                   padx=(0, 6))
        tk.Label(frame3, text="→", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"]).pack(side="left")

        tk.Button(inner, text=self.t("find_roots"), command=self.compute_roots,
                  bg=th.CALCULUS_T, fg="#ffffff", font=self.f["section"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=16, pady=8).pack(fill="x", pady=(0, 10))
        self.roots_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["display"], anchor="center",
                                     justify="center")
        self.roots_result.pack(fill="x")

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
