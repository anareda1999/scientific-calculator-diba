"""
ui/theme.py
===========
Central place for every colour, font and spacing constant so the
whole application shares one visual language.
"""

import tkinter.font as tkfont

__all__ = ["Theme"]


class Theme:
    # ── Surfaces ──────────────────────────────────────────────────
    BG         = "#f8fafc"
    CARD       = "#ffffff"
    DISPLAY    = "#0f172a"
    BORDER     = "#e2e8f0"
    BORDER_STR = "#cbd5e1"

    # ── Text ──────────────────────────────────────────────────────
    TEXT       = "#0f172a"
    TEXT_DIM   = "#64748b"
    TEXT_MUTE  = "#94a3b8"
    ON_DARK    = "#ffffff"

    # ── Accents ───────────────────────────────────────────────────
    NUM        = "#f1f5f9"
    NUM_H      = "#e2e8f0"
    OP         = "#818cf8"
    OP_H       = "#6366f1"
    FUNC       = "#f0fdf4"
    FUNC_H     = "#d1fae5"
    FUNC_T     = "#059669"
    MEM        = "#fffbeb"
    MEM_H      = "#fef3c7"
    MEM_T      = "#d97706"
    CLEAR      = "#fee2e2"
    CLEAR_H    = "#fecaca"
    CLEAR_T    = "#b91c1c"
    EQUAL      = "#818cf8"
    EQUAL_H    = "#6366f1"
    ACCENT     = "#c084fc"

    CONVERT    = "#fce7f3"
    CONVERT_T  = "#be185d"
    EQUATION   = "#fff7ed"
    EQUATION_T = "#c2410c"
    GRAPH      = "#f0f9ff"
    GRAPH_T    = "#0c4a6e"
    FORMULA    = "#f0fdf4"
    FORMULA_T  = "#059669"
    MATRIX     = "#eef2ff"
    MATRIX_T   = "#4338ca"
    CALCULUS   = "#fdf4ff"
    CALCULUS_T = "#a21caf"
    STATS      = "#ecfdf5"
    STATS_T    = "#047857"

    # ── Graphing series colours (Desmos-like) ─────────────────────
    SERIES = [
        "#2563eb", "#dc2626", "#16a34a", "#9333ea",
        "#ea580c", "#0891b2", "#db2777", "#65a30d",
    ]

    # ── Radii / spacing ──────────────────────────────────────────
    RADIUS_CARD = 20
    RADIUS_BTN  = 14
    RADIUS_INPUT = 14

    @staticmethod
    def fonts():
        """Return a dict of the fonts used across the application."""
        return {
            "display": tkfont.Font(family="Segoe UI", size=32, weight="bold"),
            "expr":    tkfont.Font(family="Segoe UI", size=13),
            "btn":     tkfont.Font(family="Segoe UI", size=12, weight="bold"),
            "btn_s":   tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            "mode":    tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            "footer":  tkfont.Font(family="Segoe UI", size=9),
            "title":   tkfont.Font(family="Segoe UI", size=18, weight="bold"),
            "title_s": tkfont.Font(family="Segoe UI", size=16, weight="bold"),
            "section": tkfont.Font(family="Segoe UI", size=11, weight="bold"),
            "mono":    tkfont.Font(family="JetBrains Mono", size=12),
        }
