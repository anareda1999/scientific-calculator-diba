"""
ui/grapher_view.py
==================
Desmos-style graphing calculator.

Performance notes (Phase A)
---------------------------
* Expressions are parsed **once** into an AST and re-used for every
  sampled point, instead of re-parsing a string thousands of times.
* Mouse motion only updates the coordinate readout - the graph is NOT
  redrawn on every pixel of movement (that was the source of the lag).
* Implicit curves use an adaptive grid so they stay responsive.
"""

import math
import re
import tkinter as tk
from tkinter import ttk

from core.engine import ExprError
from ui.theme import Theme


class GrapherView:
    """A Desmos-like graphing window."""

    def __init__(self, app):
        self.app = app
        self.theme = app.theme
        self.f = app.fonts
        self.t = app.t

        self.exprs = []          # [{id, var, color, ast, kind, payload}]
        self.sliders = {}        # name -> {value, min, max, scale, label, expr}
        self.next_id = 1
        self.updating = False

        self.x0 = 0.0            # world coordinate at the centre
        self.y0 = 0.0
        self.scale = 50.0        # pixels per world unit
        self.drag = None
        self.win = None

    # ── Window construction ────────────────────────────────────────
    def open(self):
        if self.win is not None and self.win.winfo_exists():
            self.win.lift()
            self.win.focus_force()
            return

        th = self.theme
        win = tk.Toplevel(self.app.root)
        self.win = win
        win.title(self.t("graph_title"))
        win.geometry("1180x760")
        win.resizable(True, True)
        win.minsize(900, 600)
        win.configure(bg=th.BG)
        win.transient(self.app.root)
        win.grab_set()

        # Header
        header = tk.Frame(win, bg=th.BG, height=56)
        header.pack(fill="x", padx=16, pady=(14, 6))
        header.pack_propagate(False)

        tk.Label(header, text=self.t("graph_title"), bg=th.BG, fg=th.TEXT,
                 font=self.f["title_s"]).pack(side="left")

        tk.Button(header, text="✕", command=self.close, bg=th.BG, fg=th.TEXT_MUTE,
                  font=self.f["btn"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        tk.Button(header, text=self.t("clear_all"), command=self.clear_all,
                  bg=th.CLEAR, fg=th.CLEAR_T, activebackground=th.CLEAR_T,
                  activeforeground="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=14, pady=7).pack(side="right", padx=(8, 0))

        tk.Button(header, text=self.t("reset_view"), command=self.reset_view,
                  bg=th.GRAPH, fg=th.GRAPH_T, activebackground=th.GRAPH_T,
                  activeforeground="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=14, pady=7).pack(side="right", padx=(8, 0))

        # Body
        body = tk.Frame(win, bg=th.BG)
        body.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Left panel
        panel = tk.Frame(body, bg=th.CARD, width=320, highlightthickness=1,
                         highlightbackground=th.BORDER)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        expr_holder = tk.Frame(panel, bg=th.CARD)
        expr_holder.pack(fill="both", expand=True, padx=12, pady=(12, 4))

        tk.Label(expr_holder, text=self.t("expressions"), bg=th.CARD,
                 fg=th.TEXT_DIM, font=self.f["mode"], anchor="w").pack(fill="x", pady=(0, 8))

        self.expr_box = tk.Frame(expr_holder, bg=th.CARD)
        self.expr_box.pack(fill="x")

        tk.Button(expr_holder, text=self.t("add_expression"),
                  command=lambda: self.add_expression(),
                  bg=th.GRAPH, fg=th.GRAPH_T, activebackground=th.GRAPH_T,
                  activeforeground="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=12, pady=7).pack(fill="x", pady=(10, 0))

        tk.Label(expr_holder, text=self.t("graph_examples"), bg=th.CARD,
                 fg=th.TEXT_MUTE, font=self.f["footer"], anchor="w",
                 wraplength=280, justify="left").pack(fill="x", pady=(12, 0))

        # Sliders
        tk.Label(panel, text=self.t("sliders"), bg=th.CARD, fg=th.TEXT_DIM,
                 font=self.f["mode"], anchor="w").pack(fill="x", padx=12, pady=(8, 4))
        self.slider_box = tk.Frame(panel, bg=th.CARD)
        self.slider_box.pack(fill="x", padx=12, pady=(0, 12))

        # Canvas
        right = tk.Frame(body, bg=th.BG)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        card = tk.Frame(right, bg=th.CARD, highlightthickness=1,
                        highlightbackground=th.BORDER)
        card.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(card, bg="#ffffff", highlightthickness=0,
                                width=820, height=600, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<MouseWheel>", self.on_wheel)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", self.on_leave)

        # Bottom toolbar
        bottom = tk.Frame(right, bg=th.BG, height=38)
        bottom.pack(fill="x", pady=(8, 0))

        self.coord_label = tk.Label(bottom, text="", bg=th.BG, fg=th.TEXT_DIM,
                                    font=self.f["footer"], anchor="w")
        self.coord_label.pack(side="left")

        tk.Button(bottom, text=self.t("zoom_in"), command=lambda: self.zoom(1.25),
                  bg=th.GRAPH, fg=th.GRAPH_T, activebackground=th.GRAPH_T,
                  activeforeground="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=12, pady=5).pack(side="right")
        tk.Button(bottom, text=self.t("zoom_out"), command=lambda: self.zoom(0.8),
                  bg=th.GRAPH, fg=th.GRAPH_T, activebackground=th.GRAPH_T,
                  activeforeground="#ffffff", font=self.f["mode"], bd=0,
                  relief="flat", cursor="hand2", highlightthickness=0,
                  padx=12, pady=5).pack(side="right", padx=(8, 0))

        # Seed examples
        self.add_expression("y = x^2", self.theme.SERIES[0])
        self.add_expression("a = 3", self.theme.SERIES[1])
        self.add_expression("y = a*sin(x)", self.theme.SERIES[2])

        win.after(150, self.draw)

    def close(self):
        if self.win is not None:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

    # ── Expressions ────────────────────────────────────────────────
    def add_expression(self, text="", color=None):
        eid = self.next_id
        self.next_id += 1
        if color is None:
            color = self.theme.SERIES[(eid - 1) % len(self.theme.SERIES)]

        var = tk.StringVar(value=text)
        row = tk.Frame(self.expr_box, bg=self.theme.CARD)
        row.pack(fill="x", pady=3)

        dot = tk.Canvas(row, width=20, height=20, bg=self.theme.CARD,
                        highlightthickness=0)
        dot.create_oval(3, 3, 17, 17, fill=color, outline="")
        dot.pack(side="left")

        ent = tk.Entry(row, textvariable=var, font=self.f["btn"], bg="#f8fafc",
                       fg=self.theme.TEXT, bd=0, insertbackground=self.theme.TEXT)
        ent.pack(side="left", fill="x", expand=True, padx=8)

        tk.Button(row, text="✕", command=lambda: self.remove_expression(eid),
                  bg=self.theme.CARD, fg=self.theme.TEXT_MUTE,
                  activebackground=self.theme.CARD, activeforeground=self.theme.CLEAR_T,
                  font=self.f["mode"], bd=0, relief="flat", cursor="hand2").pack(side="right")

        entry = {"id": eid, "var": var, "color": color, "row": row,
                 "ast": None, "kind": None, "payload": None}
        self.exprs.append(entry)

        def on_change(*_args):
            self.reparse(entry)
            self.sync_sliders()
            self.draw()

        var.trace_add("write", on_change)
        self.reparse(entry)
        self.sync_sliders()
        return entry

    def remove_expression(self, eid):
        for i, e in enumerate(self.exprs):
            if e["id"] == eid:
                e["row"].destroy()
                self.exprs.pop(i)
                break
        self.sync_sliders()
        self.draw()

    def clear_all(self):
        for e in list(self.exprs):
            e["row"].destroy()
        self.exprs = []
        for s in list(self.sliders.values()):
            try:
                s["frame"].destroy()
            except Exception:
                pass
        self.sliders = {}
        self.draw()

    def reset_view(self):
        self.x0 = 0.0
        self.y0 = 0.0
        self.scale = 50.0
        self.draw()

    # ── Parsing / classification ───────────────────────────────────
    def reparse(self, entry):
        """Classify and compile the expression of *entry*."""
        text = entry["var"].get().strip()
        entry["ast"] = None
        entry["kind"] = None
        entry["payload"] = None
        if not text:
            return
        engine = self.app.engine

        # point  (x, y)
        pm = re.match(r"^\s*\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)\s*$", text)
        if pm:
            entry["kind"] = "point"
            entry["payload"] = (float(pm.group(1)), float(pm.group(2)))
            return

        m = re.match(r"^\s*([^=<>!]+?)\s*=\s*(.+?)\s*$", text)
        if m:
            lhs, rhs = m.group(1).strip(), m.group(2).strip()
            # slider:  name = number
            if re.match(r"^[A-Za-z_]\w*$", lhs) and re.match(r"^-?[\d.]+$", rhs):
                entry["kind"] = "slider"
                entry["payload"] = lhs
                return
            # vertical line:  x = 5
            if lhs == "x":
                try:
                    entry["kind"] = "vertical"
                    entry["payload"] = float(engine.evaluate_text(rhs).real)
                except ExprError:
                    pass
                return
            # function:  y = f(x)
            if lhs == "y":
                try:
                    entry["kind"] = "function"
                    entry["ast"] = engine.parse(rhs)
                except ExprError:
                    pass
                return
            # implicit curve:  f(x, y) = g(x, y)
            try:
                entry["kind"] = "implicit"
                entry["ast"] = engine.parse(f"({lhs})-({rhs})")
            except ExprError:
                pass
            return

        # plain expression -> y = f(x)
        try:
            entry["kind"] = "function"
            entry["ast"] = engine.parse(text)
        except ExprError:
            pass

    # ── Sliders ────────────────────────────────────────────────────
    def sync_sliders(self):
        found = {}
        for e in self.exprs:
            if e["kind"] == "slider":
                try:
                    found[e["payload"]] = float(e["var"].get().split("=")[1].strip())
                except Exception:
                    pass

        for name in list(self.sliders.keys()):
            if name not in found:
                s = self.sliders.pop(name)
                try:
                    s["frame"].destroy()
                except Exception:
                    pass

        for name, value in found.items():
            if name not in self.sliders:
                self.make_slider(name, value)
            else:
                s = self.sliders[name]
                if not self.updating and abs(s["value"] - value) > 1e-9:
                    self.updating = True
                    s["scale"].set(value)
                    s["value"] = value
                    s["label"].config(text=f"{value:.4g}")
                    self.updating = False
                    self.app.engine.set_variable(name, complex(value))

    def make_slider(self, name, value):
        th = self.theme
        frame = tk.Frame(self.slider_box, bg=th.CARD)
        frame.pack(fill="x", pady=4)

        lo = min(0.0, value - 5.0)
        hi = max(10.0, value + 5.0)

        tk.Label(frame, text=name, bg=th.CARD, fg=th.TEXT,
                 font=self.f["mode"], width=6, anchor="w").pack(side="left")
        val_lbl = tk.Label(frame, text=f"{value:g}", bg=th.CARD, fg=th.TEXT_DIM,
                           font=self.f["footer"], width=8, anchor="e")
        val_lbl.pack(side="left", padx=(4, 6))

        scale = ttk.Scale(frame, from_=lo, to=hi, orient="horizontal", length=170)
        scale.set(value)
        scale.pack(side="left", fill="x", expand=True)

        state = {"name": name, "value": value, "min": lo, "max": hi,
                 "scale": scale, "label": val_lbl, "frame": frame}

        def on_slider(raw):
            if self.updating:
                return
            try:
                fv = float(raw)
            except Exception:
                return
            state["value"] = fv
            val_lbl.config(text=f"{fv:.4g}")
            self.updating = True
            for e in self.exprs:
                if e["kind"] == "slider" and e["payload"] == name:
                    e["var"].set(f"{name} = {fv:.6g}")
            self.updating = False
            self.app.engine.set_variable(name, complex(fv))
            self.draw()

        scale.configure(command=on_slider)
        self.sliders[name] = state
        self.app.engine.set_variable(name, complex(value))

    # ── Drawing ────────────────────────────────────────────────────
    def _nice_step(self, scale):
        target = 70.0 / scale
        if target <= 0:
            target = 1.0
        exp = math.floor(math.log10(target))
        base = 10.0 ** exp
        for m in (1, 2, 5, 10):
            if base * m >= target:
                return base * m
        return base * 10

    def _fmt(self, v):
        if v == 0:
            return "0"
        if abs(v) < 1e-10 or abs(v) >= 1e6:
            return f"{v:.3g}"
        if abs(v - round(v)) < 1e-10:
            return str(int(round(v)))
        return f"{v:.3g}".rstrip("0").rstrip(".")

    def draw(self):
        canvas = getattr(self, "canvas", None)
        if canvas is None or self.win is None:
            return
        try:
            if not self.win.winfo_exists():
                return
            canvas.delete("all")
            canvas.update_idletasks()
            W = canvas.winfo_width()
            H = canvas.winfo_height()
        except Exception:
            return
        if W < 20 or H < 20:
            return

        sc = self.scale
        cx, cy = W / 2.0, H / 2.0

        def sx(wx):
            return cx + (wx - self.x0) * sc

        def sy(wy):
            return cy - (wy - self.y0) * sc

        def wx_of(px):
            return self.x0 + (px - cx) / sc

        def wy_of(py):
            return self.y0 + (cy - py) / sc

        # Grid
        step = self._nice_step(sc)
        x_min, x_max = wx_of(0), wx_of(W)
        y_min, y_max = wy_of(H), wy_of(0)
        gx = math.floor(x_min / step) * step
        while gx <= x_max:
            px = sx(gx)
            canvas.create_line(px, 0, px, H, fill="#f1f5f9")
            gx += step
        gy = math.floor(y_min / step) * step
        while gy <= y_max:
            py = sy(gy)
            canvas.create_line(0, py, W, py, fill="#f1f5f9")
            gy += step

        # Axes
        ax_x, ax_y = sx(0.0), sy(0.0)
        if 0 <= ax_x <= W:
            canvas.create_line(ax_x, 0, ax_x, H, fill="#94a3b8", width=2)
        if 0 <= ax_y <= H:
            canvas.create_line(0, ax_y, W, ax_y, fill="#94a3b8", width=2)

        # Tick labels
        gx = math.floor(x_min / step) * step
        while gx <= x_max:
            px = sx(gx)
            if abs(px - ax_x) > 1 and 0 <= px <= W:
                canvas.create_text(px, ax_y + 14, text=self._fmt(gx),
                                   fill="#94a3b8", font=("Segoe UI", 9))
            gx += step
        gy = math.floor(y_min / step) * step
        while gy <= y_max:
            py = sy(gy)
            if abs(py - ax_y) > 1 and 0 <= py <= H:
                canvas.create_text(ax_x - 14, py, text=self._fmt(gy),
                                   fill="#94a3b8", font=("Segoe UI", 9))
            gy += step
        if 0 <= ax_x <= W and 0 <= ax_y <= H:
            canvas.create_text(ax_x + 12, ax_y + 16, text="0",
                               fill="#64748b", font=("Segoe UI", 9, "bold"))

        # Curves
        engine = self.app.engine
        for e in self.exprs:
            kind = e["kind"]
            color = e["color"]
            try:
                if kind == "function" and e["ast"] is not None:
                    self._plot_function(canvas, e["ast"], color, engine, W, H, sx, sy, wx_of)
                elif kind == "implicit" and e["ast"] is not None:
                    self._plot_implicit(canvas, e["ast"], color, engine, W, H, sx, sy, wx_of, wy_of)
                elif kind == "vertical":
                    px = sx(e["payload"])
                    if 0 <= px <= W:
                        canvas.create_line(px, 0, px, H, fill=color, width=2)
                elif kind == "point":
                    px = sx(e["payload"][0])
                    py = sy(e["payload"][1])
                    canvas.create_oval(px - 5, py - 5, px + 5, py + 5,
                                       fill=color, outline="#ffffff", width=2)
            except Exception:
                pass

        # Slider handles
        for name, s in self.sliders.items():
            hx = sx(s["value"])
            hy = sy(0.0)
            if -20 <= hx <= W + 20 and -20 <= hy <= H + 20:
                canvas.create_rectangle(hx - 6, hy - 6, hx + 6, hy + 6,
                                        fill=self._slider_color(name),
                                        outline="#ffffff", width=2)
                canvas.create_text(hx, hy - 16, text=name,
                                   fill=self._slider_color(name),
                                   font=("Segoe UI", 10, "bold"))

    def _slider_color(self, name):
        for e in self.exprs:
            if e["kind"] == "slider" and e["payload"] == name:
                return e["color"]
        return self.theme.ACCENT

    def _plot_function(self, canvas, ast, color, engine, W, H, sx, sy, wx_of):
        """Sample the AST once per pixel and draw contiguous segments."""
        from core.engine import evaluate
        ctx = engine.context
        points = []
        for px in range(0, int(W) + 1):
            wx = wx_of(px)
            try:
                wy = evaluate(ast, ctx.with_variable("x", complex(wx)))
            except ExprError:
                points.append(None)
                continue
            except Exception:
                points.append(None)
                continue
            if wy is None:
                points.append(None)
                continue
            if abs(wy.imag) > 1e-12:
                points.append(None)
                continue
            py = sy(wy.real)
            if -5000 < py < H + 5000:
                points.append((px, py))
            else:
                points.append(None)
        self._draw_segments(canvas, points, color)

    def _draw_segments(self, canvas, points, color):
        seg = []
        for p in points:
            if p is None:
                if len(seg) > 1:
                    canvas.create_line(*[c for pt in seg for c in pt], fill=color,
                                       width=2, capstyle=tk.ROUND)
                seg = []
            else:
                seg.append(p)
        if len(seg) > 1:
            canvas.create_line(*[c for pt in seg for c in pt], fill=color,
                               width=2, capstyle=tk.ROUND)

    def _plot_implicit(self, canvas, ast, color, engine, W, H, sx, sy, wx_of, wy_of):
        """Contour tracing for f(x, y) = 0."""
        from core.engine import evaluate
        ctx = engine.context
        res = 18
        for gy in range(0, int(H) + 1, res):
            for gx in range(0, int(W) + 1, res):
                wx = wx_of(gx)
                wy = wy_of(gy)
                try:
                    v = evaluate(ast, ctx.with_variable("x", complex(wx))
                                 .with_variable("y", complex(wy)))
                    v2 = evaluate(ast, ctx.with_variable("x", complex(wx_of(gx + res)))
                                 .with_variable("y", complex(wy_of(gy + res))))
                except Exception:
                    continue
                if abs(v.imag) > 1e-12 or abs(v2.imag) > 1e-12:
                    continue
                if v.real == 0 or v2.real == 0:
                    continue
                if (v.real < 0) != (v2.real < 0):
                    t = v.real / (v.real - v2.real)
                    canvas.create_line(gx, gy, gx + res * t, gy + res * t,
                                       fill=color, width=2)

    # ── Mouse ──────────────────────────────────────────────────────
    def _world(self, px, py):
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        cx, cy = W / 2.0, H / 2.0
        return (self.x0 + (px - cx) / self.scale,
                self.y0 + (cy - py) / self.scale)

    def on_press(self, event):
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        cx, cy = W / 2.0, H / 2.0
        for name, s in self.sliders.items():
            hx = cx + (s["value"] - self.x0) * self.scale
            hy = cy - (0.0 - self.y0) * self.scale
            if abs(hx - event.x) < 12 and abs(hy - event.y) < 12:
                self.drag = ("slider", name, s)
                return
        self.drag = ("pan", event.x, event.y, self.x0, self.y0)

    def on_drag(self, event):
        if not self.drag:
            return
        if self.drag[0] == "pan":
            _, sx0, sy0, wx0, wy0 = self.drag
            self.x0 = wx0 - (event.x - sx0) / self.scale
            self.y0 = wy0 + (event.y - sy0) / self.scale
            self.draw()
        else:
            _, name, s = self.drag
            wx, _ = self._world(event.x, event.y)
            v = max(s["min"], min(s["max"], wx))
            s["value"] = v
            s["label"].config(text=f"{v:.4g}")
            s["scale"].set(v)
            self.updating = True
            for e in self.exprs:
                if e["kind"] == "slider" and e["payload"] == name:
                    e["var"].set(f"{name} = {v:.6g}")
            self.updating = False
            self.app.engine.set_variable(name, complex(v))
            self.draw()

    def on_release(self, event):
        self.drag = None

    def on_wheel(self, event):
        self.zoom_at(1.15 if event.delta > 0 else 1 / 1.15, event.x, event.y)

    def zoom(self, factor):
        self.zoom_at(factor, self.canvas.winfo_width() / 2.0,
                     self.canvas.winfo_height() / 2.0)

    def zoom_at(self, factor, px, py):
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        cx, cy = W / 2.0, H / 2.0
        wx = self.x0 + (px - cx) / self.scale
        wy = self.y0 + (cy - py) / self.scale
        new_scale = max(1.0, min(5000.0, self.scale * factor))
        self.x0 = wx - (px - cx) / new_scale
        self.y0 = wy + (py - cy) / new_scale
        self.scale = new_scale
        self.draw()

    def on_motion(self, event):
        """Only the coordinate readout is refreshed - no graph redraw."""
        wx, wy = self._world(event.x, event.y)
        self.coord_label.config(
            text=f"x = {self._fmt(wx)}    y = {self._fmt(wy)}")

    def on_leave(self, event):
        self.coord_label.config(text="")
