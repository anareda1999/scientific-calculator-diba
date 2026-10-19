"""
ui/calculator_view.py
=====================
Main calculator screen: keypad, display, answer key, history tape and
a constants library.  (Phase A features.)
"""

import tkinter as tk
from tkinter import ttk

from core.engine import ExprError, format_number
from ui.theme import Theme


class CalculatorView:
    """The main calculator screen (built directly into the root window)."""

    def __init__(self, app):
        self.app = app
        self.theme = app.theme
        self.f = app.fonts
        self.t = app.t

        self.expression = ""
        self.new_input = True

        self.display_var = tk.StringVar(value="0")
        self.expr_var = tk.StringVar(value="")

    def build(self):
        """Create the widgets (called by the application shell)."""
        self._build()
        self._bind_keys()

    # ── Layout ─────────────────────────────────────────────────────
    def _build(self):
        th = self.theme
        root = self.app.root
        root.configure(bg=th.BG)

        body = tk.Frame(root, bg=th.BG)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        # ── Left column: display + keypad ──
        left = tk.Frame(body, bg=th.BG)
        left.pack(side="left", fill="both", expand=True)

        # Display card
        display_card = tk.Frame(left, bg=th.DISPLAY)
        display_card.pack(fill="x", pady=(0, 14))

        tk.Label(display_card, textvariable=self.expr_var, bg=th.DISPLAY,
                 fg=th.TEXT_MUTE, font=self.f["expr"], anchor="e").pack(
            fill="x", padx=22, pady=(14, 0))

        self.display_entry = tk.Entry(
            display_card, textvariable=self.display_var,
            font=self.f["display"], bg=th.DISPLAY, fg=th.ON_DARK,
            insertbackground=th.ON_DARK, bd=0, justify="right",
            readonlybackground=th.DISPLAY)
        self.display_entry.pack(fill="x", padx=22, pady=(0, 18))
        self.display_entry.configure(state="readonly")

        # Ans banner (last result)
        self.ans_var = tk.StringVar(value="")
        ans_bar = tk.Frame(left, bg=th.MEM, highlightthickness=1,
                           highlightbackground=th.MEM_H)
        ans_bar.pack(fill="x", pady=(0, 12))
        tk.Label(ans_bar, text=self.t("answer_label"), bg=th.MEM, fg=th.MEM_T,
                 font=self.f["mode"]).pack(side="left", padx=12, pady=7)
        tk.Label(ans_bar, textvariable=self.ans_var, bg=th.MEM, fg=th.MEM_T,
                 font=self.f["mono"]).pack(side="left", padx=(0, 12))

        # Keypad card
        keypad = tk.Frame(left, bg=th.CARD, highlightthickness=1,
                          highlightbackground=th.BORDER)
        keypad.pack(fill="both", expand=True)

        grid = tk.Frame(keypad, bg=th.CARD)
        grid.pack(padx=12, pady=12, fill="both", expand=True)

        # Row 0: memory + answer + clear
        row0 = [
            ("MC", "mem", self.mc), ("MR", "mem", self.mr),
            ("M+", "mem", self.m_add), ("M-", "mem", self.m_sub),
            ("Ans", "mem", self.use_ans), ("AC", "clear", self.clear_all),
        ]
        self._button_row(grid, row0)

        # Row 1: functions
        row1 = [
            ("DEG/RAD", "func", self.toggle_deg_rad), ("(", "func", self._lpar),
            (")", "func", self._rpar), ("x²", "func", self._square),
            ("xⁿ", "op", self._power), ("÷", "op", self._op_div),
        ]
        self._button_row(grid, row1)

        # Row 2: digits
        row2 = [
            ("7", "num", self._digit), ("8", "num", self._digit),
            ("9", "num", self._digit), ("×", "op", self._op_mul),
            ("π", "const", self._insert_pi), ("⌫", "clear", self.backspace),
        ]
        self._button_row(grid, row2)

        row3 = [
            ("4", "num", self._digit), ("5", "num", self._digit),
            ("6", "num", self._digit), ("−", "op", self._op_sub),
            ("e", "const", self._insert_e), ("÷", "op", self._op_div),
        ]
        self._button_row(grid, row3)

        row4 = [
            ("1", "num", self._digit), ("2", "num", self._digit),
            ("3", "num", self._digit), ("+", "op", self._op_add),
            ("c", "const", self._insert_c), ("g", "const", self._insert_g),
        ]
        self._button_row(grid, row4)

        row5 = [
            ("0", "num", self._digit), (".", "num", self._digit),
            ("=", "equal", self.calculate), ("√", "func", self._sqrt),
            ("ln", "func", self._ln), ("log", "func", self._log),
        ]
        self._button_row(grid, row5)

        # ── Right column: history + constants ──
        right = tk.Frame(body, bg=th.BG, width=280)
        right.pack(side="right", fill="both", padx=(14, 0))
        right.pack_propagate(False)

        # History card
        hist_card = tk.Frame(right, bg=th.CARD, highlightthickness=1,
                              highlightbackground=th.BORDER)
        hist_card.pack(fill="both", expand=True)

        head = tk.Frame(hist_card, bg=th.CARD)
        head.pack(fill="x", padx=12, pady=(12, 6))
        tk.Label(head, text=self.t("history"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(side="left")
        tk.Button(head, text="✕", command=self.clear_history, bg=th.CARD,
                  fg=th.TEXT_MUTE, activebackground=th.CARD, activeforeground=th.CLEAR_T,
                  font=self.f["mode"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        list_wrap = tk.Frame(hist_card, bg=th.CARD)
        list_wrap.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.history_list = tk.Listbox(
            list_wrap, bg=th.CARD, fg=th.TEXT, bd=0, highlightthickness=0,
            font=self.f["mono"], activestyle="none", selectbackground=th.OP,
            selectforeground="#ffffff")
        hscroll = ttk.Scrollbar(list_wrap, orient="vertical",
                                 command=self.history_list.yview)
        self.history_list.configure(yscrollcommand=hscroll.set)
        self.history_list.pack(side="left", fill="both", expand=True)
        hscroll.pack(side="right", fill="y")
        self.history_list.bind("<ButtonRelease-1>", self._history_click)

        # Constants card
        const_card = tk.Frame(right, bg=th.CARD, highlightthickness=1,
                              highlightbackground=th.BORDER)
        const_card.pack(fill="x", pady=(12, 0))
        tk.Label(const_card, text="CONSTANTS", bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", padx=12, pady=(12, 4))

        consts = [("π", "pi"), ("e", "e"), ("c", "c"), ("g", "g"),
                  ("h", "h"), ("k", "k"), ("NA", "na"), ("R", "r")]
        grid_c = tk.Frame(const_card, bg=th.CARD)
        grid_c.pack(padx=12, pady=(0, 12))
        for i, (label, name) in enumerate(consts):
            b = tk.Button(grid_c, text=label, bg=th.FUNC, fg=th.FUNC_T,
                          activebackground=th.FUNC_H, activeforeground=th.FUNC_T,
                          font=self.f["btn_s"], bd=0, relief="flat", cursor="hand2",
                          highlightthickness=0, padx=8, pady=5,
                          command=lambda n=name: self._insert_constant(n))
            b.grid(row=i // 4, column=i % 4, padx=3, pady=3, sticky="ew")
        for c in range(4):
            grid_c.columnconfigure(c, weight=1)

        self._refresh_history()

    def _button_row(self, parent, spec):
        frame = tk.Frame(parent, bg=self.theme.CARD)
        frame.pack(fill="x", pady=3)
        for text, style, cmd in spec:
            bg, fg, active = self._style(style)
            btn = tk.Button(frame, text=text, command=cmd, font=self.f["btn"],
                            bg=bg, fg=fg, activebackground=active,
                            activeforeground=fg, bd=0, relief="flat",
                            cursor="hand2", highlightthickness=0)
            btn.pack(side="left", fill="both", expand=True, padx=3)
            self.app.add_hover(btn, bg, active)

    def _style(self, style):
        th = self.theme
        table = {
            "num":   (th.NUM, th.TEXT, th.NUM_H),
            "op":    (th.OP, "#ffffff", th.OP_H),
            "equal": (th.EQUAL, "#ffffff", th.EQUAL_H),
            "clear": (th.CLEAR, th.CLEAR_T, th.CLEAR_H),
            "mem":   (th.MEM, th.MEM_T, th.MEM_H),
            "func":  (th.FUNC, th.FUNC_T, th.FUNC_H),
            "const": (th.MATRIX, th.MATRIX_T, "#c7d2fe"),
        }
        return table[style]

    # ── Keyboard ───────────────────────────────────────────────────
    def _bind_keys(self):
        root = self.app.root
        root.bind("<Return>", lambda e: self.calculate())
        root.bind("<KP_Enter>", lambda e: self.calculate())
        root.bind("<BackSpace>", lambda e: self.backspace())
        root.bind("<Escape>", lambda e: self.clear_all())
        for key in "0123456789+-*/().":
            root.bind(key, lambda e, k=key: self._key_char(k))

    def _key_char(self, ch):
        if ch in "0123456789.":
            self._digit(ch)
        elif ch in "+-*/()":
            self._append(ch)

    # ── Display helpers ────────────────────────────────────────────
    def _get(self):
        return self.display_var.get()

    def _set(self, value):
        self.display_var.set(value)

    def _append(self, ch):
        current = self._get()
        if current in ("0", "Error"):
            self._set(ch)
        else:
            self._set(current + ch)
        self.new_input = False

    def _digit(self, digit):
        current = self._get()
        if self.new_input or current in ("0", "Error"):
            self._set("0." if digit == "." else digit)
            self.new_input = False
        else:
            if digit == "." and "." in current:
                return
            self._set(current + digit)

    def _lpar(self):
        self._append("(")

    def _rpar(self):
        self._append(")")

    def _op_add(self):
        self._operator("+")

    def _op_sub(self):
        self._operator("-")

    def _op_mul(self):
        self._operator("*")

    def _op_div(self):
        self._operator("/")

    def _operator(self, op):
        current = self._get()
        if current in ("0", "Error"):
            return
        if current and current[-1] in "+-*/(":
            self._set(current[:-1] + op)
        else:
            self._set(current + op)
        self.new_input = False

    def _power(self):
        self._append("**")

    def _square(self):
        self._append("**2")

    def _sqrt(self):
        self._append("sqrt(")

    def _ln(self):
        self._append("ln(")

    def _log(self):
        self._append("log(")

    def _insert_pi(self):
        self._append("pi")

    def _insert_e(self):
        self._append("e")

    def _insert_c(self):
        self._append("c")

    def _insert_g(self):
        self._append("g")

    def _insert_constant(self, name):
        self._append(name)

    def backspace(self):
        current = self._get()
        if current == "Error":
            return
        self._set(current[:-1] if len(current) > 1 else "0")
        self.new_input = False

    def clear_all(self):
        self._set("0")
        self.expr_var.set("")
        self.new_input = True

    # ── Memory ─────────────────────────────────────────────────────
    def mc(self):
        self.app.memory = 0

    def mr(self):
        self._set(format_number(complex(self.app.memory)))
        self.new_input = True

    def m_add(self):
        try:
            self.app.memory += float(self._get())
        except ValueError:
            pass

    def m_sub(self):
        try:
            self.app.memory -= float(self._get())
        except ValueError:
            pass

    def use_ans(self):
        """Insert the last computed answer."""
        if self.app.last_answer is not None:
            self._set(format_number(self.app.last_answer))
            self.new_input = True

    # ── Angle mode ─────────────────────────────────────────────────
    def toggle_deg_rad(self):
        self.app.toggle_angle_mode()

    # ── Calculation (uses the new engine) ─────────────────────────
    def calculate(self):
        text = self._get()
        if text in ("0", "Error", ""):
            return
        try:
            result = self.app.engine.evaluate_text(text)
        except ExprError as exc:
            self._set("Error")
            self.new_input = True
            self.app.show_error(str(exc))
            return
        self.expr_var.set(text + " =")
        self._set(format_number(result))
        self.new_input = True
        self.app.set_answer(result)
        self.app.add_history(text, result)

    # ── History ────────────────────────────────────────────────────
    def _refresh_history(self):
        self.history_list.delete(0, "end")
        if not self.app.history:
            self.history_list.insert("end", self.t("history_empty"))
            return
        for expr, result in reversed(self.app.history):
            self.history_list.insert("end", f"{expr} = {result}")

    def _history_click(self, event):
        selection = self.history_list.curselection()
        if not selection:
            return
        index = len(self.app.history) - 1 - selection[0]
        if 0 <= index < len(self.app.history):
            expr, _ = self.app.history[index]
            self._set(expr)
            self.new_input = True

    def clear_history(self):
        self.app.history.clear()
        self._refresh_history()
