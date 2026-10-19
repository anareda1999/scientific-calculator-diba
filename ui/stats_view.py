"""
ui/stats_view.py
================
Descriptive statistics and linear regression.
"""

import tkinter as tk

from core import statistics as stats
from core.engine import format_number


class StatsView:
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
        win.title(self.t("statistics"))
        win.geometry("560x660")
        win.resizable(True, True)
        win.minsize(500, 560)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("statistics"), bg=th.BG, fg=th.TEXT,
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

        tk.Label(inner, text=self.t("data_input"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 6))
        self.data_var = tk.StringVar(value="12 15 18 22 25 30 34 40")
        tk.Entry(inner, textvariable=self.data_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                 insertbackground=th.TEXT).pack(fill="x", pady=(0, 14))

        # Buttons
        grid = tk.Frame(inner, bg=th.CARD)
        grid.pack(fill="x", pady=(0, 12))
        buttons = [
            ("stat_mean", stats.mean), ("stat_median", stats.median),
            ("stat_mode", stats.mode), ("stat_stdev", stats.stdev),
            ("stat_variance", stats.variance), ("stat_min", stats.minimum),
            ("stat_max", stats.maximum), ("stat_sum", stats.total),
            ("stat_range", stats.range_of), ("stat_count", len),
        ]
        for i, (key, fn) in enumerate(buttons):
            b = tk.Button(grid, text=self.t(key), bg=th.STATS, fg=th.STATS_T,
                          activebackground=th.STATS_T, activeforeground="#ffffff",
                          font=self.f["mode"], bd=0, relief="flat", cursor="hand2",
                          highlightthickness=0, padx=8, pady=8,
                          command=lambda f=fn, k=key: self._apply(f, k))
            b.grid(row=i // 3, column=i % 3, padx=4, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)

        self.result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                               font=self.f["display"], anchor="w")
        self.result.pack(fill="x", pady=(0, 18))

        # Percentile
        tk.Label(inner, text=self.t("stat_percentile"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 6))
        frame = tk.Frame(inner, bg=th.CARD)
        frame.pack(fill="x", pady=(0, 16))
        self.percent_var = tk.StringVar(value="90")
        tk.Entry(frame, textvariable=self.percent_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                 insertbackground=th.TEXT).pack(side="left", fill="x", expand=True,
                                               padx=(0, 8))
        tk.Button(frame, text=self.t("calculate"), command=self._percentile,
                  bg=th.STATS_T, fg="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=14, pady=6).pack(side="left")

        # Regression
        tk.Label(inner, text=self.t("stat_regression"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 6))
        self.reg_var = tk.StringVar(value="1,2  2,4  3,6  4,8  5,11")
        tk.Entry(inner, textvariable=self.reg_var, font=self.f["display"],
                 bg="#f8fafc", fg=th.TEXT, bd=0, justify="right",
                 insertbackground=th.TEXT).pack(fill="x", pady=(0, 10))
        tk.Button(inner, text=self.t("calculate"), command=self._regression,
                  bg=th.STATS_T, fg="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=14, pady=6).pack(fill="x", pady=(0, 16))

        self.reg_result = tk.Label(inner, text="", bg=th.CARD, fg=th.TEXT,
                                   font=self.f["mono"], anchor="w", justify="left")
        self.reg_result.pack(fill="x")

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    def _values(self):
        text = self.data_var.get().replace(",", " ")
        return [v for v in text.split() if v]

    def _apply(self, fn, key):
        try:
            values = self._values()
            value = fn(values)
            self.result.config(text=f"{self.t(key)} = {format_number(complex(value))}",
                               fg=self.theme.TEXT)
        except Exception as exc:
            self.result.config(text=str(exc), fg=self.theme.CLEAR_T)

    def _percentile(self):
        try:
            values = self._values()
            p = float(self.percent_var.get())
            value = stats.percentile(values, p)
            self.result.config(text=f"P{p:g} = {format_number(complex(value))}",
                               fg=self.theme.TEXT)
        except Exception as exc:
            self.result.config(text=str(exc), fg=self.theme.CLEAR_T)

    def _regression(self):
        try:
            pairs = []
            for chunk in self.reg_var.get().replace(";", " ").split():
                if "," in chunk:
                    xs, ys = chunk.split(",", 1)
                    pairs.append((float(xs), float(ys)))
            if len(pairs) < 2:
                raise ValueError("Entrez au moins 2 paires x,y")
            xs = [p[0] for p in pairs]
            ys = [p[1] for p in pairs]
            slope, intercept, r2 = stats.linear_regression(xs, ys)
            corr = stats.correlation(xs, ys)
            self.reg_result.config(
                text=f"y = {slope:.10g}·x + {intercept:.10g}\n"
                     f"{self.t('stat_r2')} = {r2:.10g}    "
                     f"{self.t('stat_corr')} = {corr:.10g}",
                fg=self.theme.TEXT)
        except Exception as exc:
            self.reg_result.config(text=str(exc), fg=self.theme.CLEAR_T)
