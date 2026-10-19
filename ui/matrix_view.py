"""
ui/matrix_view.py
=================
Matrix calculator: determinant, inverse, transpose, product, power,
trace and rank for 2x2, 3x3 and 4x4 matrices.
"""

import tkinter as tk
from tkinter import ttk

from core import matrices
from core.engine import ExprError


class MatrixView:
    def __init__(self, app):
        self.app = app
        self.theme = app.theme
        self.f = app.fonts
        self.t = app.t
        self.win = None
        self.size = 3
        self._size_ref = tk.IntVar(value=3)

    def open(self):
        if self.win is not None and self.win.winfo_exists():
            self.win.lift()
            return
        th = self.theme
        win = tk.Toplevel(self.app.root)
        self.win = win
        win.title(self.t("matrices"))
        win.geometry("620x720")
        win.resizable(True, True)
        win.minsize(560, 600)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("matrices"), bg=th.BG, fg=th.TEXT,
                 font=self.f["title"]).pack(side="left", expand=True)
        tk.Button(header, text="✕", command=self.close, bg=th.BG, fg=th.TEXT_MUTE,
                  font=self.f["btn"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        body = tk.Frame(win, bg=th.BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        # Size selector
        top = tk.Frame(body, bg=th.BG)
        top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text=self.t("matrix_size"), bg=th.BG, fg=th.TEXT_DIM,
                 font=self.f["mode"]).pack(side="left", padx=(0, 10))
        for n in (2, 3, 4):
            tk.Radiobutton(top, text=f"{n}×{n}", variable=self._size_var(), value=n,
                           bg=th.BG, fg=th.TEXT, selectcolor=th.CARD,
                           font=self.f["mode"], activebackground=th.BG,
                           activeforeground=th.TEXT, command=self._rebuild,
                           bd=0, highlightthickness=0, padx=8).pack(side="left")

        # Two matrices side by side
        grids = tk.Frame(body, bg=th.BG)
        grids.pack(fill="both", expand=True)

        self.mat_a = tk.Frame(grids, bg=th.CARD, highlightthickness=1,
                              highlightbackground=th.BORDER)
        self.mat_a.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.mat_b = tk.Frame(grids, bg=th.CARD, highlightthickness=1,
                              highlightbackground=th.BORDER)
        self.mat_b.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # Operations
        ops = tk.Frame(body, bg=th.BG)
        ops.pack(fill="x", pady=(12, 0))

        row1 = tk.Frame(ops, bg=th.BG)
        row1.pack(fill="x", pady=3)
        for label, key, fn in [("det", "matrix_det", self.op_det),
                               ("inv", "matrix_inv", self.op_inv),
                               ("T", "matrix_trans", self.op_trans),
                               ("tr", "matrix_trace", self.op_trace)]:
            self._op_button(row1, self.t(key), fn)

        row2 = tk.Frame(ops, bg=th.BG)
        row2.pack(fill="x", pady=3)
        self._op_button(row2, "A × B", self.op_mul)
        self._op_button(row2, "A + B", self.op_add)
        self._op_button(row2, "rank", self.op_rank)

        row3 = tk.Frame(ops, bg=th.BG)
        row3.pack(fill="x", pady=3)
        tk.Label(row3, text="Aⁿ", bg=th.BG, fg=th.TEXT_DIM,
                 font=self.f["mode"]).pack(side="left", padx=(0, 6))
        self.pow_var = tk.StringVar(value="2")
        tk.Entry(row3, textvariable=self.pow_var, font=self.f["display"],
                 bg="#ffffff", fg=th.TEXT, bd=0, justify="center", width=6,
                 insertbackground=th.TEXT).pack(side="left", padx=(0, 8))
        tk.Button(row3, text="Aⁿ", command=self.op_pow, bg=self.theme.MATRIX_T,
                  fg="#ffffff", font=self.f["section"], bd=0, relief="flat",
                  cursor="hand2", highlightthickness=0, padx=14,
                  pady=5).pack(side="left")

        # Result
        result_card = tk.Frame(body, bg=th.CARD, highlightthickness=1,
                               highlightbackground=th.BORDER)
        result_card.pack(fill="x", pady=(12, 0))
        self.result_label = tk.Label(result_card, text="", bg=th.CARD, fg=th.TEXT,
                                     font=self.f["mono"], anchor="w", justify="left")
        self.result_label.pack(fill="x", padx=16, pady=14)

        self._rebuild()

    def _size_var(self):
        return self._size_ref

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    def _op_button(self, parent, label, command):
        tk.Button(parent, text=label, command=command, bg=self.theme.MATRIX,
                  fg=self.theme.MATRIX_T, activebackground=self.theme.MATRIX_T,
                  activeforeground="#ffffff", font=self.f["section"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=14, pady=7).pack(side="left", padx=(0, 8), fill="x", expand=True)

    def _rebuild(self):
        self.size = self._size_var().get()
        self.a_vars = []
        self.b_vars = []
        for frame, store, title in ((self.mat_a, self.a_vars, "A"),
                                    (self.mat_b, self.b_vars, "B")):
            for child in frame.winfo_children():
                child.destroy()
            tk.Label(frame, text=title, bg=self.theme.CARD, fg=self.theme.TEXT_DIM,
                     font=self.f["mode"]).pack(anchor="w", padx=12, pady=(10, 4))
            for r in range(self.size):
                row = tk.Frame(frame, bg=self.theme.CARD)
                row.pack(fill="x", pady=2, padx=12)
                for c in range(self.size):
                    var = tk.StringVar(value="0")
                    tk.Entry(row, textvariable=var, font=self.f["display"],
                             bg="#f8fafc", fg=self.theme.TEXT, bd=0, justify="right",
                             insertbackground=self.theme.TEXT).pack(side="left",
                                                                   fill="x",
                                                                   expand=True,
                                                                   padx=3)
                    store.append(var)

    def _read(self, store):
        matrix = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                text = store[r * self.size + c].get().strip() or "0"
                row.append(self.app.engine.evaluate_text(text))
            matrix.append(row)
        return matrix

    def _show(self, text):
        self.result_label.config(text=text)

    def _guard(self, fn):
        try:
            fn()
        except (matrices.MatrixError, ExprError) as exc:
            self._show(str(exc))
        except Exception as exc:
            self._show(str(exc))

    def op_det(self):
        from core.engine import format_number
        self._guard(lambda: self._show(
            f"det(A) = {format_number(matrices.det(self._read(self.a_vars)))}"))

    def op_inv(self):
        def run():
            inv = matrices.inverse(self._read(self.a_vars))
            self._show("A⁻¹ =\n" + matrices.format_matrix(inv))
        self._guard(run)

    def op_trans(self):
        def run():
            self._show("Aᵀ =\n" + matrices.format_matrix(
                matrices.transpose(self._read(self.a_vars))))
        self._guard(run)

    def op_trace(self):
        from core.engine import format_number
        self._guard(lambda: self._show(
            f"tr(A) = {format_number(matrices.trace(self._read(self.a_vars)))}"))

    def op_rank(self):
        self._guard(lambda: self._show(
            f"rank(A) = {matrices.rank(self._read(self.a_vars))}"))

    def op_mul(self):
        def run():
            product = matrices.matmul(self._read(self.a_vars), self._read(self.b_vars))
            self._show("A × B =\n" + matrices.format_matrix(product))
        self._guard(run)

    def op_add(self):
        def run():
            total = matrices.matadd(self._read(self.a_vars), self._read(self.b_vars))
            self._show("A + B =\n" + matrices.format_matrix(total))
        self._guard(run)

    def op_pow(self):
        def run():
            n = int(float(self.pow_var.get()))
            self._show(f"A^{n} =\n" + matrices.format_matrix(
                matrices.matpow(self._read(self.a_vars), n)))
        self._guard(run)
