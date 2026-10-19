"""
ui/converter_view.py
====================
Unit converter window (weight, currency, volume, area, distance).
"""

import tkinter as tk
from tkinter import ttk

from core import units


class ConverterView:
    def __init__(self, app):
        self.app = app
        self.theme = app.theme
        self.f = app.fonts
        self.t = app.t
        self.win = None
        self.category = "Weight"

    def open(self):
        if self.win is not None and self.win.winfo_exists():
            self.win.lift()
            return
        th = self.theme
        win = tk.Toplevel(self.app.root)
        self.win = win
        win.title(self.t("converter"))
        win.geometry("520x720")
        win.resizable(True, True)
        win.minsize(480, 600)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=th.BG, height=60)
        header.pack(fill="x", padx=20, pady=(16, 10))
        header.pack_propagate(False)
        tk.Label(header, text=self.t("converter"), bg=th.BG, fg=th.TEXT,
                 font=self.f["title"]).pack(side="left", expand=True)
        tk.Button(header, text="✕", command=self.close, bg=th.BG, fg=th.TEXT_MUTE,
                  font=self.f["btn"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        cat_frame = tk.Frame(win, bg=th.BG)
        cat_frame.pack(fill="x", padx=24, pady=(0, 16))

        for cat in units.CATEGORY_KEYS:
            rb = tk.Radiobutton(cat_frame, text=self.t(cat.lower()),
                                variable=self._cat_var(), value=cat,
                                bg=th.BG, fg=th.TEXT, selectcolor=th.CARD,
                                font=self.f["mode"], activebackground=th.BG,
                                activeforeground=th.TEXT,
                                command=lambda c=cat: self.set_category(c),
                                bd=0, highlightthickness=0, padx=8)
            rb.pack(side="left", padx=(0, 12))

        card = tk.Frame(win, bg=th.CARD, highlightthickness=1,
                        highlightbackground=th.BORDER)
        card.pack(padx=20, pady=(0, 16), fill="both", expand=True)
        inner = tk.Frame(card, bg=th.CARD)
        inner.pack(padx=20, pady=18, fill="both", expand=True)

        tk.Label(inner, text=self.t("from"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 6))
        self.from_val = tk.StringVar(value="")
        from_entry = tk.Entry(inner, textvariable=self.from_val,
                              font=self.f["display"], bg="#f8fafc", fg=th.TEXT,
                              bd=0, justify="right", insertbackground=th.TEXT)
        from_entry.pack(fill="x", pady=(0, 10))
        from_entry.bind("<KeyRelease>", lambda e: self.convert())

        self.from_unit = ttk.Combobox(inner, state="readonly", font=self.f["btn_s"],
                                      height=10)
        self.from_unit.pack(fill="x", pady=(0, 18))

        tk.Button(inner, text=self.t("swap"), command=self.swap,
                  bg=self.theme.ACCENT, fg="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=14, pady=7).pack(pady=(0, 18))

        tk.Label(inner, text=self.t("to"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 6))
        self.to_val = tk.StringVar(value="")
        self.to_entry = tk.Entry(inner, textvariable=self.to_val,
                                 font=self.f["display"], bg="#f8fafc", fg=th.TEXT,
                                 bd=0, justify="right", insertbackground=th.TEXT,
                                 state="readonly")
        self.to_entry.pack(fill="x", pady=(0, 10))

        self.to_unit = ttk.Combobox(inner, state="readonly", font=self.f["btn_s"],
                                    height=10)
        self.to_unit.pack(fill="x", pady=(0, 20))

        tk.Label(inner, text=self.t("copyright"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["footer"], anchor="center").pack(side="bottom")

        self.refresh_units()

    def _cat_var(self):
        if not hasattr(self, "_cat_var_ref"):
            self._cat_var_ref = tk.StringVar(value=self.category)
        return self._cat_var_ref

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    def set_category(self, cat):
        self.category = cat
        self._cat_var_ref.set(cat)
        self.refresh_units()

    def refresh_units(self):
        names = units.unit_names(self.category, self.app.lang)
        self.from_unit["values"] = names
        self.to_unit["values"] = names
        self.from_unit.current(0)
        self.to_unit.current(min(1, len(names) - 1))
        self.from_val.set("")
        self.to_val.set("")

    def swap(self):
        fi = self.from_unit.current()
        ti = self.to_unit.current()
        self.from_unit.current(ti)
        self.to_unit.current(fi)
        self.convert()

    def convert(self):
        raw = self.from_val.get().strip()
        if raw == "":
            self.to_val.set("")
            return
        try:
            value = float(raw)
            result = units.convert(self.category, self.app.lang, value,
                                   self.from_unit.get(), self.to_unit.get())
            self.to_val.set(str(int(result)) if result == int(result) else f"{result:g}")
        except Exception:
            self.to_val.set("")
