#!/usr/bin/env python3
"""
SABIHA Arsitek - Generator desain mural "Sapta Pesona" tema hutan alam.

Tiga tingkat kerumitan untuk dilukis di dinding:
  mudah  : bidang warna rata, sedikit warna, 1 guru + 2 murid
  sedang : warna dua tone, ikon di papan, sungai & jembatan, 1 guru + 4 murid
  sulit  : gradasi, detail, hewan hutan, 2 guru + 6 murid beraktivitas

Contoh:
  python3 mural_sapta_pesona.py --lebar 6 --tinggi 4 --sekolah "SDN 1 CIANJUR"
Hasil (per tingkat): mural-<tingkat>.png/.svg dan mural-<tingkat>-grid.png
(grid 1 m untuk memindahkan gambar ke dinding), plus ringkasan-mural.png.
"""
import argparse
import html
import math
import random
import re

ap = argparse.ArgumentParser()
ap.add_argument("--lebar", type=float, default=6.0, help="lebar dinding (m)")
ap.add_argument("--tinggi", type=float, default=4.0, help="tinggi dinding (m)")
ap.add_argument("--judul", default="SAPTA PESONA")
ap.add_argument("--sekolah", default="", help="nama sekolah (opsional, di bawah judul)")
ap.add_argument("--tingkat", default="mudah,sedang,sulit")
ap.add_argument("--prefix", default="mural")
a = ap.parse_args([])          # nilai default saat diimpor sebagai modul

PXM = 300                      # piksel per meter
W, H = int(a.lebar * PXM), int(a.tinggi * PXM)
GROUND = int(H * 0.60)          # garis cakrawala / tanah
NILAI = ["AMAN", "TERTIB", "BERSIH", "SEJUK", "INDAH", "RAMAH", "KENANGAN"]
INK = "#3b2a1a"

o = []


def add(s):
    o.append(s)


def f(v):
    return f"{v:.1f}"


def rect(x, y, w, h, fill, rx=0, stroke=None, sw=0):
    st = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}"{st}/>')


def circ(x, y, r, fill, stroke=None, sw=0):
    st = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}"{st}/>')


def ell(x, y, rx, ry, fill, rot=0, stroke=None, sw=0):
    st = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    tr = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot else ""
    add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"{st}{tr}/>')


def poly(pts, fill, stroke=None, sw=0):
    st = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linejoin="round"' if stroke else ""
    add(f'<polygon points="{" ".join(f(x) + "," + f(y) for x, y in pts)}" fill="{fill}"{st}/>')


def path(d, fill="none", stroke=None, sw=0, cap="round"):
    st = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linecap="{cap}" stroke-linejoin="round"' if stroke else ""
    add(f'<path d="{d}" fill="{fill}"{st}/>')


def line(x1, y1, x2, y2, c, w):
    add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="round"/>')


def text(x, y, t, size, fill="#ffffff", w="bold", anchor="middle", stroke=None, sw=0):
    base = (f'x="{f(x)}" y="{f(y)}" font-family="Arial Rounded MT Bold, Helvetica, Arial, sans-serif" '
            f'font-size="{f(size)}" font-weight="{w}" text-anchor="{anchor}"')
    if stroke:   # garis tepi digambar lebih dulu agar isi huruf tetap utuh
        add(f'<text {base} fill="{stroke}" stroke="{stroke}" stroke-width="{f(sw * 2)}" stroke-linejoin="round">{html.escape(t)}</text>')
    add(f'<text {base} fill="{fill}">{html.escape(t)}</text>')


# ================================================================== alam
def sky(lvl):
    if lvl == 3:
        add('<defs><linearGradient id="sky3" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#8fd3f0"/><stop offset="1" stop-color="#e6f7fc"/></linearGradient></defs>')
        rect(0, 0, W, GROUND + 40, "url(#sky3)")
    else:
        rect(0, 0, W, GROUND + 40, "#bfe6f5")


def sun(lvl):
    x, y = W * 0.775, H * 0.21
    if lvl >= 2:
        for k in range(12):
            t = k * math.pi / 6
            line(x + 95 * math.cos(t), y + 95 * math.sin(t), x + 130 * math.cos(t), y + 130 * math.sin(t), "#ffd34d", 14)
    circ(x, y, 75, "#ffd34d")
    if lvl == 3:
        circ(x - 18, y - 18, 40, "#ffe48a")


def cloud(x, y, s, lvl):
    for dx, dy, r in ((-0.6, 0.1, 0.45), (0, -0.15, 0.6), (0.6, 0.1, 0.45), (0.2, 0.2, 0.5), (-0.2, 0.2, 0.5)):
        circ(x + dx * s, y + dy * s, r * s, "#ffffff")
    if lvl == 3:
        ell(x, y + 0.45 * s, 0.9 * s, 0.12 * s, "#dbeef6")


def wave(y0, amp, freq, phase):
    return lambda x: y0 + amp * math.sin(x * freq + phase) + amp * 0.5 * math.sin(x * freq * 2.3 + phase * 1.7)


def hill(fn, color):
    pts = [(0, H)] + [(x, fn(x)) for x in range(0, W + 30, 30)] + [(W, H)]
    poly(pts, color)


def tree_round(x, yb, s, lvl, dark=False):
    trunk = "#7a4a26"
    rect(x - 0.09 * s, yb - 0.55 * s, 0.18 * s, 0.55 * s, trunk)
    if lvl == 3:
        rect(x - 0.09 * s, yb - 0.55 * s, 0.06 * s, 0.55 * s, "#8f5a30")
    cy = yb - 0.55 * s - 0.3 * s
    base = "#2f7d43" if dark else "#3f9a52"
    shade = "#276b39" if dark else "#2f7d43"
    hi = "#56b066" if dark else "#6cc070"
    if lvl >= 2:
        for dx, dy, r in ((-0.28, 0.1, 0.3), (0.28, 0.1, 0.3), (0, 0.18, 0.32)):
            circ(x + dx * s, cy + dy * s, r * s, shade)
    for dx, dy, r in ((-0.25, 0, 0.28), (0.25, 0, 0.28), (0, -0.2, 0.36), (0, 0.05, 0.3)):
        circ(x + dx * s, cy + dy * s - (0.04 * s if lvl >= 2 else 0), r * s, base)
    if lvl == 3:
        for dx, dy, r in ((-0.12, -0.32, 0.12), (0.18, -0.15, 0.09), (-0.3, -0.05, 0.08)):
            circ(x + dx * s, cy + dy * s, r * s, hi)


def tree_pine(x, yb, s, lvl, dark=False):
    rect(x - 0.06 * s, yb - 0.2 * s, 0.12 * s, 0.2 * s, "#7a4a26")
    base = "#23603d" if dark else "#2e7a4f"
    shade = "#1b4d31" if dark else "#23603d"
    for i in range(3):
        top = yb - 0.2 * s - (0.28 + 0.26 * i) * s - 0.3 * s
        bot = yb - 0.2 * s - 0.24 * i * s
        wd = (0.42 - 0.1 * i) * s
        poly([(x - wd, bot), (x, top), (x + wd, bot)], base)
        if lvl >= 2:
            poly([(x, top), (x + wd, bot), (x + 0.1 * wd, bot)], shade)


def bush(x, y, s, lvl):
    for dx, r in ((-0.5, 0.35), (0.5, 0.35), (0, 0.5)):
        circ(x + dx * s, y - r * s * 0.6, r * s, "#4c9f45")
    if lvl == 3:
        circ(x - 0.15 * s, y - 0.55 * s, 0.14 * s, "#6fbf5a")
        for dx in (-0.35, 0.1, 0.45):
            circ(x + dx * s, y - 0.3 * s, 0.06 * s, "#e0473c")


def flower(x, y, s, color, lvl):
    line(x, y, x, y - 1.6 * s, "#3d8b3d", max(2, 0.2 * s))
    if lvl == 3:
        ell(x + 0.35 * s, y - 0.7 * s, 0.35 * s, 0.14 * s, "#3d8b3d", -30)
    for k in range(5):
        t = k * 2 * math.pi / 5
        circ(x + 0.42 * s * math.cos(t), y - 1.6 * s + 0.42 * s * math.sin(t), 0.33 * s, color)
    circ(x, y - 1.6 * s, 0.25 * s, "#ffd34d")


def bird(x, y, s, lvl):
    c = "#35506b" if lvl < 3 else "#2d3f55"
    path(f"M{f(x - s)},{f(y)} Q{f(x - s / 2)},{f(y - s / 1.6)} {f(x)},{f(y)} Q{f(x + s / 2)},{f(y - s / 1.6)} {f(x + s)},{f(y)}",
         stroke=c, sw=max(3, s / 6))


def butterfly(x, y, s, c1, c2):
    ell(x - 0.45 * s, y - 0.3 * s, 0.5 * s, 0.38 * s, c1, -25)
    ell(x + 0.45 * s, y - 0.3 * s, 0.5 * s, 0.38 * s, c1, 25)
    ell(x - 0.35 * s, y + 0.3 * s, 0.32 * s, 0.25 * s, c2, 25)
    ell(x + 0.35 * s, y + 0.3 * s, 0.32 * s, 0.25 * s, c2, -25)
    line(x, y - 0.5 * s, x, y + 0.5 * s, INK, 0.12 * s)


def deer(x, yf, s):
    c, dk = "#b9773f", "#8a5328"
    for dx in (-0.45, -0.3, 0.35, 0.5):
        line(x + dx * s, yf - 0.55 * s, x + dx * s, yf, dk, 0.1 * s)
    ell(x, yf - 0.7 * s, 0.65 * s, 0.28 * s, c)
    poly([(x + 0.4 * s, yf - 0.85 * s), (x + 0.62 * s, yf - 1.35 * s), (x + 0.8 * s, yf - 1.3 * s), (x + 0.62 * s, yf - 0.75 * s)], c)
    ell(x + 0.8 * s, yf - 1.38 * s, 0.22 * s, 0.14 * s, c, -15)
    ell(x + 0.62 * s, yf - 1.52 * s, 0.1 * s, 0.05 * s, dk, -40)
    circ(x + 0.86 * s, yf - 1.42 * s, 0.035 * s, INK)
    for sgn in (-1, 1):
        bx = x + 0.72 * s + sgn * 0.05 * s
        path(f"M{f(bx)},{f(yf - 1.5 * s)} L{f(bx - 0.1 * s)},{f(yf - 1.85 * s)} M{f(bx - 0.06 * s)},{f(yf - 1.72 * s)} L{f(bx - 0.22 * s)},{f(yf - 1.8 * s)}",
             stroke=dk, sw=0.05 * s)
    for dx, dy in ((-0.3, -0.75), (-0.05, -0.8), (0.2, -0.72), (-0.15, -0.62)):
        circ(x + dx * s, yf + dy * s, 0.05 * s, "#f3e3c8")
    ell(x - 0.66 * s, yf - 0.82 * s, 0.1 * s, 0.06 * s, "#f3e3c8", -30)


def rabbit(x, yf, s):
    c = "#e9e4dc"
    ell(x, yf - 0.35 * s, 0.45 * s, 0.35 * s, c, stroke="#b8b0a4", sw=2)
    circ(x + 0.4 * s, yf - 0.7 * s, 0.25 * s, c, stroke="#b8b0a4", sw=2)
    ell(x + 0.32 * s, yf - 1.1 * s, 0.08 * s, 0.25 * s, c, -10, stroke="#b8b0a4", sw=2)
    ell(x + 0.5 * s, yf - 1.1 * s, 0.08 * s, 0.25 * s, c, 10, stroke="#b8b0a4", sw=2)
    circ(x + 0.48 * s, yf - 0.74 * s, 0.04 * s, INK)
    circ(x - 0.45 * s, yf - 0.4 * s, 0.1 * s, "#ffffff")


def mushroom(x, yf, s):
    rect(x - 0.12 * s, yf - 0.45 * s, 0.24 * s, 0.45 * s, "#f3e3c8")
    path(f"M{f(x - 0.45 * s)},{f(yf - 0.4 * s)} Q{f(x)},{f(yf - 1.05 * s)} {f(x + 0.45 * s)},{f(yf - 0.4 * s)} Z", "#d9443a")
    for dx, dy in ((-0.2, -0.55), (0.15, -0.65), (0.25, -0.48)):
        circ(x + dx * s, yf + dy * s, 0.06 * s, "#ffffff")


# ================================================================== ikon Sapta Pesona
def icon(name, x, y, s, c="#ffffff"):
    if name == "AMAN":
        path(f"M{f(x)},{f(y - s)} L{f(x + 0.8 * s)},{f(y - 0.65 * s)} L{f(x + 0.7 * s)},{f(y + 0.2 * s)} "
             f"Q{f(x + 0.5 * s)},{f(y + 0.75 * s)} {f(x)},{f(y + s)} Q{f(x - 0.5 * s)},{f(y + 0.75 * s)} {f(x - 0.7 * s)},{f(y + 0.2 * s)} "
             f"L{f(x - 0.8 * s)},{f(y - 0.65 * s)} Z", c)
    elif name == "TERTIB":
        for i in range(3):
            circ(x - 0.6 * s + 0.6 * i * s, y - 0.35 * s, 0.22 * s, c)
            rect(x - 0.82 * s + 0.6 * i * s, y - 0.1 * s, 0.44 * s, 0.75 * s, c, rx=0.15 * s)
    elif name == "BERSIH":
        poly([(x - 0.6 * s, y - 0.5 * s), (x + 0.6 * s, y - 0.5 * s), (x + 0.45 * s, y + s), (x - 0.45 * s, y + s)], c)
        rect(x - 0.75 * s, y - 0.78 * s, 1.5 * s, 0.2 * s, c, rx=0.08 * s)
        rect(x - 0.2 * s, y - s, 0.4 * s, 0.2 * s, c, rx=0.08 * s)
    elif name == "SEJUK":
        ell(x, y - 0.1 * s, 0.5 * s, 0.9 * s, c, 35)
        line(x - 0.55 * s, y + 0.8 * s, x + 0.25 * s, y - 0.4 * s, "#7a4a26", 0.12 * s)
    elif name == "INDAH":
        for k in range(5):
            t = k * 2 * math.pi / 5 - math.pi / 2
            circ(x + 0.5 * s * math.cos(t), y + 0.5 * s * math.sin(t), 0.38 * s, c)
        circ(x, y, 0.3 * s, "#ffd34d")
    elif name == "RAMAH":
        circ(x, y, 0.9 * s, c)
        circ(x - 0.3 * s, y - 0.2 * s, 0.1 * s, "#7a4a26")
        circ(x + 0.3 * s, y - 0.2 * s, 0.1 * s, "#7a4a26")
        path(f"M{f(x - 0.45 * s)},{f(y + 0.2 * s)} Q{f(x)},{f(y + 0.65 * s)} {f(x + 0.45 * s)},{f(y + 0.2 * s)}", stroke="#7a4a26", sw=0.13 * s)
    elif name == "KENANGAN":
        rect(x - 0.9 * s, y - 0.5 * s, 1.8 * s, 1.2 * s, c, rx=0.2 * s)
        rect(x - 0.35 * s, y - 0.8 * s, 0.7 * s, 0.35 * s, c, rx=0.1 * s)
        circ(x, y + 0.1 * s, 0.38 * s, "#7a4a26")
        circ(x, y + 0.1 * s, 0.2 * s, c)


def sign(cx, top, word, lvl):
    wd, ht = (215, 72) if lvl == 1 else (250, 84)
    x0 = cx - wd / 2
    for px in (x0 + 30, x0 + wd - 30):
        rect(px - 9, top + ht - 5, 18, GROUND + 30 - top - ht, "#7a4a26")
    rect(x0, top, wd, ht, "#a86b3c", rx=14, stroke="#7a4a26", sw=6)
    if lvl == 3:
        for k in range(1, 3):
            line(x0 + 12, top + k * ht / 3, x0 + wd - 12, top + k * ht / 3, "#96602f", 3)
    if lvl == 1:
        text(cx, top + ht / 2 + 13, word, 36 if len(word) < 8 else 31)
    else:
        icon(word, x0 + 40, top + ht / 2, 22)
        text(cx + 24, top + ht / 2 + 11, word, 32 if len(word) < 8 else 25)


def title(lvl):
    wd, ht = 820, 130 if not a.sekolah else 165
    x0 = W / 2 - wd / 2
    y0 = 42
    for px in (x0 + 90, x0 + wd - 90):
        line(px, 0, px, y0 + 10, "#7a4a26", 10)
    rect(x0, y0, wd, ht, "#a86b3c", rx=24, stroke="#7a4a26", sw=9)
    if lvl >= 2:
        for k in (-1, 1):
            circ(W / 2 + k * (wd / 2 - 38), y0 + 36, 10, "#7a4a26")
    if lvl == 3:
        for dx in (-wd / 2 + 10, wd / 2 - 10):   # daun menjuntai di papan judul
            for k in range(4):
                ell(W / 2 + dx + (k - 1.5) * 16 * (1 if dx < 0 else -1), y0 + ht - 5 + k * 8, 20, 10, "#4c9f45", 30 * (1 if dx < 0 else -1))
    text(W / 2, y0 + 92, a.judul, 78, "#ffffff", stroke="#7a4a26" if lvl == 3 else None, sw=6)
    if a.sekolah:
        text(W / 2, y0 + 142, a.sekolah, 34, "#fff3d6")


# ================================================================== tokoh guru & murid
KIND = {
    "guru_p": dict(top="#c9a86a", bottom="#2f3a55", hijab="#2f4f7f", lower="longskirt", sleeve="long"),
    "guru_l": dict(top="#c9a86a", bottom="#3d3d4a", hair="#2a2a2a", lower="trousers", sleeve="long"),
    "murid_l": dict(top="#ffffff", bottom="#d23a3a", hair="#2a2a2a", lower="shorts", sleeve="short"),
    "murid_ph": dict(top="#ffffff", bottom="#d23a3a", hijab="#ffffff", lower="skirt", sleeve="long"),
    "murid_p": dict(top="#ffffff", bottom="#d23a3a", hair="#3a2618", lower="skirt", sleeve="short", ponytail=True),
}


def person(x, yf, h, kind, pose="stand", lvl=1, item=None, skin="#f1c9a5"):
    k = KIND[kind]
    u = h / 10
    ol = "#3b2a1a" if lvl == 3 else None
    ow = 0.1 * u
    wh_ol = "#b9b9b9"                          # garis untuk bidang putih
    hy, hr = yf - h + 0.95 * u, 0.95 * u
    neck = yf - h + 1.9 * u
    hip = yf - 4.5 * u
    sy = neck + 0.35 * u
    top_ol = ol or (wh_ol if k["top"] == "#ffffff" else None)
    # --- kaki & bawahan
    if k["lower"] == "longskirt":
        poly([(x - 1.0 * u, hip - 0.2 * u), (x + 1.0 * u, hip - 0.2 * u), (x + 1.35 * u, yf - 0.35 * u), (x - 1.35 * u, yf - 0.35 * u)],
             k["bottom"], ol, ow)
    else:
        for sgn in (-1, 1):
            leg_c = k["bottom"] if k["lower"] == "trousers" else skin
            line(x + sgn * 0.45 * u, hip, x + sgn * 0.55 * u, yf - 0.3 * u, leg_c, 0.7 * u)
            if k["lower"] != "trousers":
                line(x + sgn * 0.55 * u, yf - 0.95 * u, x + sgn * 0.55 * u, yf - 0.3 * u, "#ffffff", 0.72 * u)
        if k["lower"] == "shorts":
            rect(x - 1.05 * u, hip - 0.3 * u, 2.1 * u, 1.6 * u, k["bottom"], rx=0.25 * u, stroke=ol, sw=ow)
        elif k["lower"] == "skirt":
            poly([(x - 1.0 * u, hip - 0.3 * u), (x + 1.0 * u, hip - 0.3 * u), (x + 1.4 * u, hip + 2.1 * u), (x - 1.4 * u, hip + 2.1 * u)],
                 k["bottom"], ol, ow)
    for sgn in (-1, 1):
        ell(x + sgn * 0.6 * u, yf - 0.22 * u, 0.5 * u, 0.26 * u, "#222222")
    # --- badan
    rect(x - 1.05 * u, neck, 2.1 * u, hip - neck + 0.2 * u, k["top"], rx=0.45 * u, stroke=top_ol, sw=ow if ol else 2)
    if lvl >= 2:
        if kind.startswith("murid"):
            poly([(x - 0.18 * u, neck + 0.15 * u), (x + 0.18 * u, neck + 0.15 * u), (x + 0.12 * u, neck + 1.3 * u),
                  (x, neck + 1.5 * u), (x - 0.12 * u, neck + 1.3 * u)], "#d23a3a")
        else:
            rect(x + 0.3 * u, neck + 0.6 * u, 0.55 * u, 0.3 * u, "#ffffff", rx=0.05 * u)   # papan nama
            line(x - 0.75 * u, neck + 0.7 * u, x - 0.25 * u, neck + 0.7 * u, "#a88a52", 0.08 * u)
    # --- lengan
    arm_c = k["top"] if k["sleeve"] == "long" else skin

    def arm(pts):
        d = "M" + " L".join(f"{f(px)},{f(py)}" for px, py in pts)
        if arm_c == "#ffffff":
            path(d, stroke=wh_ol, sw=0.62 * u + 4)
        path(d, stroke=arm_c, sw=0.62 * u)
        if k["sleeve"] == "short":
            line(pts[0][0], pts[0][1], pts[0][0] + (pts[1][0] - pts[0][0]) * 0.35,
                 pts[0][1] + (pts[1][1] - pts[0][1]) * 0.35, k["top"], 0.8 * u)
        circ(pts[-1][0], pts[-1][1], 0.34 * u, skin)

    L = (x - 0.95 * u, sy)
    R = (x + 0.95 * u, sy)
    if pose == "wave":
        arm([L, (x - 1.3 * u, sy + 1.3 * u), (x - 1.2 * u, hip + 0.2 * u)])
        arm([R, (x + 1.8 * u, sy - 0.2 * u), (x + 1.9 * u, sy - 1.7 * u)])
    elif pose == "hold":
        arm([L, (x - 1.25 * u, sy + 1.2 * u), (x - 0.35 * u, hip - 0.6 * u)])
        arm([R, (x + 1.25 * u, sy + 1.2 * u), (x + 0.35 * u, hip - 0.6 * u)])
    elif pose == "throw":
        arm([L, (x - 1.3 * u, sy + 1.3 * u), (x - 1.2 * u, hip + 0.2 * u)])
        arm([R, (x + 1.7 * u, sy + 0.6 * u), (x + 2.4 * u, sy + 0.9 * u)])
    else:
        arm([L, (x - 1.3 * u, sy + 1.3 * u), (x - 1.2 * u, hip + 0.2 * u)])
        arm([R, (x + 1.3 * u, sy + 1.3 * u), (x + 1.2 * u, hip + 0.2 * u)])
    # --- kepala
    if "hijab" in k:
        hj_ol = ol or (wh_ol if k["hijab"] == "#ffffff" else None)
        path(f"M{f(x - 1.25 * u)},{f(hy)} A{f(1.25 * u)},{f(1.25 * u)} 0 0 1 {f(x + 1.25 * u)},{f(hy)} "
             f"L{f(x + 1.3 * u)},{f(neck + 1.0 * u)} Q{f(x)},{f(neck + 1.5 * u)} {f(x - 1.3 * u)},{f(neck + 1.0 * u)} Z",
             k["hijab"], stroke=hj_ol, sw=ow if ol else 2)
        circ(x, hy + 0.1 * u, hr * 0.82, skin)
    else:
        circ(x, hy, hr, skin, stroke=ol, sw=ow)
        if k.get("ponytail"):
            circ(x + 1.05 * u, hy - 0.2 * u, 0.45 * u, k["hair"])
        path(f"M{f(x - hr - 0.05 * u)},{f(hy + 0.05 * u)} A{f(hr + 0.05 * u)},{f(hr + 0.1 * u)} 0 0 1 {f(x + hr + 0.05 * u)},{f(hy + 0.05 * u)} "
             f"Q{f(x + 0.3 * u)},{f(hy - 0.55 * u)} {f(x - hr - 0.05 * u)},{f(hy + 0.05 * u)} Z", k["hair"])
    # --- wajah
    ey = hy + 0.05 * u
    for sgn in (-1, 1):
        circ(x + sgn * 0.32 * u, ey, 0.1 * u, INK)
        if lvl >= 2:
            circ(x + sgn * 0.5 * u, ey + 0.35 * u, 0.13 * u, "#f29a8e")
        if lvl == 3:
            line(x + sgn * 0.2 * u, ey - 0.25 * u, x + sgn * 0.45 * u, ey - 0.28 * u, INK, 0.06 * u)
    path(f"M{f(x - 0.28 * u)},{f(ey + 0.33 * u)} Q{f(x)},{f(ey + 0.62 * u)} {f(x + 0.28 * u)},{f(ey + 0.33 * u)}", stroke=INK, sw=0.09 * u)
    # --- barang yang dibawa
    hx, hy2 = x, hip - 0.6 * u
    if item == "bibit":
        poly([(hx - 0.55 * u, hy2 - 0.2 * u), (hx + 0.55 * u, hy2 - 0.2 * u), (hx + 0.4 * u, hy2 + 0.6 * u), (hx - 0.4 * u, hy2 + 0.6 * u)], "#b5562f")
        line(hx, hy2 - 0.2 * u, hx, hy2 - 1.0 * u, "#3d8b3d", 0.12 * u)
        ell(hx - 0.3 * u, hy2 - 0.95 * u, 0.32 * u, 0.15 * u, "#4caf50", -30)
        ell(hx + 0.3 * u, hy2 - 0.75 * u, 0.32 * u, 0.15 * u, "#4caf50", 30)
    elif item == "kamera":
        rect(hx - 0.7 * u, hy2 - 0.55 * u, 1.4 * u, 0.9 * u, "#333333", rx=0.15 * u)
        circ(hx, hy2 - 0.1 * u, 0.3 * u, "#9fb7c9")
    elif item == "buku":
        rect(hx - 0.7 * u, hy2 - 0.6 * u, 1.4 * u, 1.0 * u, "#2f7fc1", rx=0.08 * u)
        line(hx, hy2 - 0.6 * u, hx, hy2 + 0.4 * u, "#ffffff", 0.08 * u)
    elif item == "sampah":
        circ(x + 2.55 * u, sy + 0.8 * u, 0.3 * u, "#e8e8e8", stroke="#a0a0a0", sw=2)


def bin_(x, yf, s, lvl):
    poly([(x - 0.5 * s, yf - 1.2 * s), (x + 0.5 * s, yf - 1.2 * s), (x + 0.4 * s, yf), (x - 0.4 * s, yf)], "#2e8b57")
    rect(x - 0.6 * s, yf - 1.38 * s, 1.2 * s, 0.2 * s, "#236b43", rx=0.06 * s)
    if lvl >= 2:
        icon("SEJUK", x, yf - 0.6 * s, 0.25 * s, "#ffffff")


# ================================================================== susun mural
def river_fn(x):
    return GROUND + 105 + 22 * math.sin(x / 210) + 10 * math.sin(x / 90)


def path_edges(y):
    t = (y - GROUND) / (H - GROUND)
    c = W / 2 + 40 * math.sin(t * 3)
    half = 22 + t * 210
    return c - half, c + half


def mural(lvl):
    global o
    o = []
    rnd = random.Random(7 + lvl)
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    sky(lvl)
    sun(lvl)
    for cx, cy, s in ((W * 0.12, H * 0.13, 70), (W * 0.33, H * 0.2, 55), (W * 0.68, H * 0.11, 60))[: 2 if lvl == 1 else 3]:
        cloud(cx, cy, s, lvl)
    if lvl >= 2:
        for bx, by, s in ((W * 0.42, H * 0.3, 22), (W * 0.47, H * 0.27, 17), (W * 0.62, H * 0.32, 20))[: 2 if lvl == 2 else 3]:
            bird(bx, by, s, lvl)
    # bukit
    layers = [(wave(GROUND - 230, 50, 1 / 260, 0.3), "#a7d6a9"), (wave(GROUND - 120, 45, 1 / 200, 1.7), "#7cc07f"),
              (wave(GROUND - 30, 25, 1 / 170, 2.9), "#5fae6e")]
    if lvl == 3:
        poly([(W * 0.18, GROUND - 170), (W * 0.33, GROUND - 440), (W * 0.48, GROUND - 170)], "#9bb7c9")   # gunung jauh
        poly([(W * 0.29, GROUND - 380), (W * 0.33, GROUND - 440), (W * 0.37, GROUND - 380), (W * 0.35, GROUND - 370),
              (W * 0.33, GROUND - 390), (W * 0.31, GROUND - 368)], "#ffffff")
    for fn, c in (layers[1:] if lvl == 1 else layers):
        hill(fn, c)
    # barisan hutan belakang
    if lvl >= 2:
        xs = range(30, W, 70 if lvl == 3 else 110)
        for i, x in enumerate(xs):
            s = rnd.uniform(0.8, 1.15) * (150 if lvl == 3 else 130)
            (tree_pine if i % 2 else tree_round)(x + rnd.uniform(-15, 15), GROUND + 10, s, lvl, dark=True)
    else:
        for x in range(90, W, 180):
            tree_round(x, GROUND + 10, 130, lvl, dark=True)
    # tanah
    rect(0, GROUND, W, H - GROUND, "#7cc36a")
    if lvl == 3:
        rect(0, GROUND, W, 45, "#6db85c")
    # jalan setapak
    pts_l, pts_r = [], []
    for y in range(GROUND, H + 1, 20):
        l, r = path_edges(y)
        pts_l.append((l, y))
        pts_r.append((r, y))
    poly(pts_l + pts_r[::-1], "#e2c79a")
    if lvl == 3:
        for i in range(14):
            y = GROUND + 30 + i * (H - GROUND - 40) / 14
            l, r = path_edges(y)
            ell(rnd.uniform(l + 10, r - 10), y, 6 + i * 1.5, 3 + i * 0.7, "#cdb07e")
    # sungai & jembatan
    if lvl >= 2:
        top = [(x, river_fn(x)) for x in range(0, W + 20, 20)]
        bot = [(x, river_fn(x) + 62) for x in range(W, -20, -20)]
        poly(top + bot, "#5bb7e0")
        if lvl == 3:
            for x in range(40, W, 160):
                path(f"M{f(x)},{f(river_fn(x) + 25)} q20,-8 40,0 t40,0", stroke="#bfe8f7", sw=4)
            for x in (150, 520, 1350, 1640):
                ell(x, river_fn(x) + 62, 34, 16, "#9a9a92")
        yb = river_fn(W / 2)
        l, r = path_edges(yb + 30)
        rect(l - 35, yb - 14, r - l + 70, 92, "#a86b3c", rx=6)
        for px in range(int(l - 30), int(r + 35), 26):
            line(px, yb - 10, px, yb + 74, "#7a4a26", 3)
        for py in (yb - 14, yb + 76):
            rect(l - 45, py - 6, r - l + 90, 12, "#7a4a26", rx=4)
    # pohon besar di sudut (dibelakang papan)
    tree_round(80, GROUND + 60, 480, lvl)
    tree_round(W - 80, GROUND + 60, 470, lvl)
    if lvl >= 2:
        tree_pine(250, GROUND + 40, 330, lvl)
        tree_pine(W - 250, GROUND + 40, 320, lvl)
    # papan Sapta Pesona
    top_sign = GROUND - 150
    step = (W - 290) / 6
    for i, word in enumerate(NILAI):
        sign(145 + i * step, top_sign + (0 if i % 2 == 0 or lvl == 1 else 18), word, lvl)
    title(lvl)
    # rumput, bunga, semak
    if lvl >= 2:
        for _ in range(40 if lvl == 2 else 90):
            x, y = rnd.uniform(0, W), rnd.uniform(GROUND + 20, H - 10)
            l, r = path_edges(y)
            if l - 10 < x < r + 10:
                continue
            path(f"M{f(x - 8)},{f(y)} L{f(x - 4)},{f(y - 18)} M{f(x)},{f(y)} L{f(x)},{f(y - 24)} M{f(x + 8)},{f(y)} L{f(x + 4)},{f(y - 18)}",
                 stroke="#4f9a44", sw=3)
    fl_cols = ["#e84a5f", "#f7a531", "#b25fd1", "#ffffff"] if lvl == 3 else ["#e84a5f", "#f7a531"]
    fl_pos = [(60, H - 40), (640, H - 30), (1170, H - 25), (W - 60, H - 45)]
    if lvl >= 2:
        fl_pos += [(330, GROUND + 70), (1460, GROUND + 60), (760, H - 120), (1060, H - 110)]
    if lvl == 3:
        fl_pos += [(rnd.uniform(0, W), rnd.uniform(GROUND + 230, H - 20)) for _ in range(10)]
    for i, (x, y) in enumerate(fl_pos):
        l, r = path_edges(y)
        if not (l - 15 < x < r + 15):
            flower(x, y, 16 if lvl == 1 else 13, fl_cols[i % len(fl_cols)], lvl)
    if lvl >= 2:
        bush(420, GROUND + 55, 60, lvl)
        bush(W - 420, GROUND + 55, 60, lvl)
    if lvl == 3:
        mushroom(90, H - 15, 55)
        mushroom(140, H - 12, 38)
        deer(640, GROUND + 100, 78)
        rabbit(680, H - 45, 50)
        butterfly(560, GROUND + 160, 22, "#f7a531", "#e84a5f")
        butterfly(1240, GROUND + 140, 20, "#b25fd1", "#5bb7e0")
        butterfly(W - 160, H - 210, 18, "#ffd34d", "#f7a531")
    # guru & murid
    yf = H - 35
    if lvl == 1:
        person(300, yf, 410, "guru_p", "wave", lvl)
        person(480, yf, 310, "murid_l", "wave", lvl)
        person(W - 450, yf, 310, "murid_ph", "wave", lvl)
        bin_(W - 280, yf, 85, lvl)
    elif lvl == 2:
        person(220, yf, 285, "murid_l", "hold", lvl, item="bibit")
        person(380, yf, 370, "guru_p", "wave", lvl)
        person(540, yf, 285, "murid_ph", "wave", lvl)
        person(W - 580, yf, 285, "murid_l", "throw", lvl, item="sampah", skin="#d9a57b")
        bin_(W - 445, yf, 78, lvl)
        person(W - 270, yf, 285, "murid_p", "hold", lvl, item="kamera")
    else:
        person(200, yf, 335, "guru_l", "wave", lvl, skin="#d9a57b")
        person(335, yf, 250, "murid_l", "hold", lvl, item="bibit")
        person(460, yf, 245, "murid_ph", "wave", lvl)
        person(585, yf, 250, "murid_p", "hold", lvl, item="buku", skin="#d9a57b")
        person(W - 620, yf, 250, "murid_l", "throw", lvl, item="sampah", skin="#d9a57b")
        bin_(W - 505, yf, 70, lvl)
        person(W - 390, yf, 245, "murid_p", "hold", lvl, item="kamera")
        person(W - 245, yf, 330, "guru_p", "wave", lvl)
        person(W - 110, yf, 250, "murid_ph", "wave", lvl)
    add("</svg>")
    return "\n".join(o)


def with_grid(svg):
    DASH = ' stroke-dasharray="10 8"'
    g = []
    for i in range(1, int(a.lebar * 2)):
        x = i * PXM / 2
        major = i % 2 == 0
        g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#000" stroke-opacity="{0.55 if major else 0.25}" '
                 f'stroke-width="{3 if major else 1.5}"{"" if major else DASH}/>')
    for j in range(1, int(a.tinggi * 2)):
        y = j * PXM / 2
        major = j % 2 == 0
        g.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#000" stroke-opacity="{0.55 if major else 0.25}" '
                 f'stroke-width="{3 if major else 1.5}"{"" if major else DASH}/>')
    for i in range(int(math.ceil(a.lebar))):
        for j in range(int(math.ceil(a.tinggi))):
            lab = f"{chr(65 + i)}{j + 1}"
            g.append(f'<rect x="{i * PXM + 4}" y="{j * PXM + 4}" width="46" height="30" rx="5" fill="#ffffff" fill-opacity="0.9" stroke="#000" stroke-width="1.5"/>')
            g.append(f'<text x="{i * PXM + 27}" y="{j * PXM + 27}" font-family="Arial" font-size="22" font-weight="bold" '
                     f'text-anchor="middle" fill="#111">{lab}</text>')
    g.append(f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" fill="none" stroke="#000" stroke-width="3"/>')
    return svg.replace("</svg>", "\n".join(g) + "\n</svg>")


def palette(svg):
    cols = re.findall(r'(?:fill|stop-color)="(#[0-9a-fA-F]{6})"', svg)
    seen = []
    for c in cols:
        c = c.lower()
        if c not in seen:
            seen.append(c)
    return seen


def save(svg, name):
    with open(name + ".svg", "w", encoding="utf-8") as fh:
        fh.write(svg)
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=name + ".png")
    except ImportError:
        pass


DESK = {
    1: ("MUDAH", ["Bidang warna rata, tanpa gradasi", "1 guru + 2 murid", "Bisa dikerjakan guru & murid"]),
    2: ("SEDANG", ["Warna dua tone + ikon di papan", "Sungai, jembatan, burung", "1 guru + 4 murid beraktivitas"]),
    3: ("SULIT", ["Gradasi langit, detail & garis tepi", "Rusa, kelinci, kupu-kupu, jamur", "2 guru + 6 murid, butuh pelukis mural"]),
}
LV = {"mudah": 1, "sedang": 2, "sulit": 3}


def ringkasan(results, desk, judul, out, lebar=None, tinggi=None):
    """Lembar ringkasan: 3 tingkat berdampingan + keterangan + palet cat."""
    lebar = lebar or W / PXM
    tinggi = tinggi or H / PXM
    SW, TW = 1900, 580
    th = TW * H / W
    SH = int(200 + th + 460)
    r = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">',
         f'<rect width="{SW}" height="{SH}" fill="#fbfaf6"/>',
         f'<text x="{SW / 2}" y="70" font-family="Helvetica, Arial" font-size="44" font-weight="bold" text-anchor="middle" fill="#2b2b2b">'
         f'{html.escape(judul)}</text>',
         f'<text x="{SW / 2}" y="112" font-family="Helvetica, Arial" font-size="24" text-anchor="middle" fill="#555">'
         f'Ukuran dinding {lebar:g} x {tinggi:g} m  |  SABIHA Arsitek</text>']
    for idx, lvl in enumerate(sorted(results)):
        x0, y0 = 50 + idx * (TW + 45), 150
        inner = results[lvl].split(">", 1)[1].rsplit("</svg>", 1)[0]
        inner = re.sub(r'id="([\w-]+)"', lambda m: f'id="{m.group(1)}_r{idx}"', inner)
        inner = re.sub(r'url\(#([\w-]+)\)', lambda m: f'url(#{m.group(1)}_r{idx})', inner)
        r.append(f'<svg x="{x0}" y="{y0}" width="{TW}" height="{th:.0f}" viewBox="0 0 {W} {H}">{inner}</svg>')
        r.append(f'<rect x="{x0}" y="{y0}" width="{TW}" height="{th:.0f}" fill="none" stroke="#2b2b2b" stroke-width="2"/>')
        nm, pts = desk[lvl]
        ty = y0 + th + 50
        r.append(f'<text x="{x0}" y="{ty:.0f}" font-family="Helvetica, Arial" font-size="32" font-weight="bold" fill="#2b2b2b">{nm}</text>')
        for k, t in enumerate(pts):
            r.append(f'<text x="{x0}" y="{ty + 40 + k * 32:.0f}" font-family="Helvetica, Arial" font-size="22" fill="#444">- {html.escape(t)}</text>')
        pal = palette(results[lvl])
        py = ty + 150
        r.append(f'<text x="{x0}" y="{py:.0f}" font-family="Helvetica, Arial" font-size="22" font-weight="bold" fill="#2b2b2b">'
                 f'Palet cat: {len(pal)} warna</text>')
        for k, c in enumerate(pal):
            cx = x0 + (k % 14) * 41
            cy = py + 18 + (k // 14) * 41
            r.append(f'<rect x="{cx}" y="{cy:.0f}" width="34" height="34" rx="6" fill="{c}" stroke="#999" stroke-width="1.5"/>')
    r.append("</svg>")
    save("\n".join(r), out)


def setup(lebar, tinggi):
    """Atur ukuran kanvas (dipanggil juga oleh skrip tema lain)."""
    global W, H, GROUND
    W, H = int(lebar * PXM), int(tinggi * PXM)
    GROUND = int(H * 0.60)


if __name__ == "__main__":
    a = ap.parse_args()
    setup(a.lebar, a.tinggi)
    results = {}
    for nm in [t.strip() for t in a.tingkat.split(",") if t.strip()]:
        lvl = LV[nm]
        svg = mural(lvl)
        save(svg, f"{a.prefix}-{nm}")
        save(with_grid(svg), f"{a.prefix}-{nm}-grid")
        results[lvl] = svg
        print(f"OK {a.prefix}-{nm}: {len(palette(svg))} warna")
    ringkasan(results, DESK, f"Desain Mural {a.judul.title()} - Tema Hutan Alam", f"ringkasan-{a.prefix}", a.lebar, a.tinggi)
    print(f"OK ringkasan-{a.prefix}")
