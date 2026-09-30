#!/usr/bin/env python3
"""
SABIHA Arsitek - Mural Sapta Pesona dengan tema/referensi lain.

Tema:
  kebunteh : kebun teh & gunung khas Cianjur, 7 nilai di layang-layang
  pantai   : pantai & laut, 7 nilai di layar perahu, mercusuar
  kereta   : kereta Sapta Pesona melintasi sawah terasering, 1 gerbong = 1 nilai

Contoh:
  python3 mural_tema.py --tema kebunteh,pantai,kereta --lebar 6 --tinggi 4 --sekolah "SDN 1 CIANJUR"
Hasil per tema: <tema>-<tingkat>.png/.svg, <tema>-<tingkat>-grid.png, ringkasan-<tema>.png
"""
import argparse
import math
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mural_sapta_pesona as M  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--tema", default="kebunteh,pantai,kereta")
ap.add_argument("--lebar", type=float, default=6.0)
ap.add_argument("--tinggi", type=float, default=4.0)
ap.add_argument("--judul", default="SAPTA PESONA")
ap.add_argument("--sekolah", default="")
ap.add_argument("--tingkat", default="mudah,sedang,sulit")
args = ap.parse_args()

M.setup(args.lebar, args.tinggi)
M.a.judul, M.a.sekolah = args.judul, args.sekolah
W, H = M.W, M.H
rect, circ, ell, poly, path, line, text = M.rect, M.circ, M.ell, M.poly, M.path, M.line, M.text
person, icon, NILAI, INK = M.person, M.icon, M.NILAI, M.INK
WOOD, WOOD_D = "#a86b3c", "#7a4a26"
COLS = ["#e84a5f", "#f7a531", "#2f7fc1", "#3f9a52", "#b25fd1", "#e0473c", "#1f9aa8"]


def start():
    M.o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']


def end():
    M.add("</svg>")
    return "\n".join(M.o)


def sky(lvl, top="#8fd3f0", bottom="#e6f7fc", flat="#bfe6f5", y2=None):
    y2 = y2 or H
    if lvl == 3:
        M.add(f'<defs><linearGradient id="langit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
              f'<stop offset="1" stop-color="{bottom}"/></linearGradient></defs>')
        rect(0, 0, W, y2, "url(#langit)")
    else:
        rect(0, 0, W, y2, flat)


def hand_up(x, yf, h):
    u = h / 10
    sy = yf - h + 1.9 * u + 0.35 * u
    return x + 1.9 * u, sy - 1.7 * u


def tint(c, k=0.45):
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * k) for v in (r, g, b))


def fit(word, base):
    return base if len(word) < 7 else base * 0.8


def school_line(y, color="#ffffff"):
    if args.sekolah:
        text(W / 2, y, args.sekolah, 34, color)


def ribbon_title(lvl, y0=40, color="#d23a3a", dark="#9e2626"):
    wd, ht = 820, 120
    x0 = W / 2 - wd / 2
    for sgn in (-1, 1):   # ekor pita
        ex = W / 2 + sgn * (wd / 2 + 70)
        cx = W / 2 + sgn * (wd / 2 - 30)
        poly([(cx, y0 + 30), (ex, y0 + 30), (ex - sgn * 40, y0 + 30 + ht / 2), (ex, y0 + 30 + ht), (cx, y0 + 30 + ht)], dark)
        if lvl >= 2:
            poly([(W / 2 + sgn * wd / 2, y0 + ht), (W / 2 + sgn * (wd / 2 - 30), y0 + 30 + ht), (W / 2 + sgn * (wd / 2 - 30), y0 + ht)], "#6e1a1a")
    rect(x0, y0, wd, ht, color, rx=10, stroke=INK if lvl == 3 else None, sw=4)
    text(W / 2, y0 + 86, args.judul, 76, "#ffffff")
    school_line(y0 + ht + 72, INK)


def cloud_title(lvl, cx, cy):
    for dx, dy, r in ((-330, 25, 85), (-200, -30, 110), (-40, -55, 125), (120, -45, 115), (270, -10, 100), (360, 30, 75),
                      (0, 40, 120), (-180, 50, 95), (190, 50, 95)):
        circ(cx + dx, cy + dy, r, "#ffffff")
    if lvl == 3:
        ell(cx, cy + 118, 380, 20, "#dbeef6")
    text(cx, cy + 30, args.judul, 80, "#2f7fc1", stroke="#ffffff" if lvl < 3 else "#ffffff", sw=2)
    if args.sekolah:
        text(cx, cy + 82, args.sekolah, 30, "#2f7fc1")


def mountains(lvl, base, peaks, col="#8fb5c9", col2="#7aa3b8", snow=False):
    for px, ph, pw in peaks:
        poly([(px - pw, base), (px, base - ph), (px + pw, base)], col)
        if lvl >= 2:
            poly([(px, base - ph), (px + pw, base), (px + pw * 0.15, base)], col2)
        if lvl == 3 and snow:
            poly([(px - pw * 0.18, base - ph * 0.82), (px, base - ph), (px + pw * 0.18, base - ph * 0.82),
                  (px + pw * 0.06, base - ph * 0.86), (px - pw * 0.05, base - ph * 0.8)], "#eef4f7")


def flowers_strip(lvl, rnd, y_min, y_max, avoid=()):
    cols = ["#e84a5f", "#f7a531", "#b25fd1", "#ffffff"] if lvl == 3 else ["#e84a5f", "#f7a531"]
    n = 5 if lvl == 1 else (9 if lvl == 2 else 16)
    for i in range(n):
        x = rnd.uniform(30, W - 30)
        if any(lo < x < hi for lo, hi in avoid):
            continue
        M.flower(x, rnd.uniform(y_min, y_max), 15 if lvl == 1 else 12, cols[i % len(cols)], lvl)


def grass_tufts(lvl, rnd, y_min, y_max, n):
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(y_min, y_max)
        path(f"M{x - 8:.1f},{y:.1f} L{x - 4:.1f},{y - 18:.1f} M{x:.1f},{y:.1f} L{x:.1f},{y - 24:.1f} M{x + 8:.1f},{y:.1f} L{x + 4:.1f},{y - 18:.1f}",
             stroke="#4f9a44", sw=3)


# ====================================================================== 1. KEBUN TEH
def kite(cx, cy, word, color, lvl, target=None):
    w2, h2 = 100, 125
    top, bot = (cx, cy - h2), (cx, cy + h2)
    # tali
    tx, ty = target if target else (cx - 70, cy + h2 + 220)
    path(f"M{cx:.1f},{cy + h2:.1f} Q{cx + 40:.1f},{(cy + h2 + ty) / 2:.1f} {tx:.1f},{ty:.1f}", stroke="#555555", sw=2.5)
    # ekor
    tail = [(cx, cy + h2)]
    for k in range(1, 5):
        tail.append((cx + 25 * math.sin(k * 1.3), cy + h2 + k * 38))
    path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in tail), stroke=WOOD_D, sw=3)
    for x, y in tail[1:]:
        poly([(x - 14, y - 9), (x + 14, y + 9), (x + 14, y - 9), (x - 14, y + 9)], "#ffd34d" if lvl > 1 else color)
    poly([top, (cx + w2, cy - 20), bot, (cx - w2, cy - 20)], color, stroke=INK if lvl == 3 else None, sw=4)
    if lvl >= 2:
        poly([top, (cx + w2, cy - 20), (cx, cy - 20)], tint(color))
        poly([(cx - w2, cy - 20), bot, (cx, cy - 20)], tint(color, 0.25))
        line(cx, cy - h2, cx, cy + h2, "#ffffff", 3)
        line(cx - w2, cy - 20, cx + w2, cy - 20, "#ffffff", 3)
    if lvl == 1:
        text(cx, cy + 2, word, fit(word, 32), "#ffffff", stroke=INK, sw=4)
    else:
        icon(word, cx, cy - 62, 20, INK)
        text(cx, cy + 26, word, fit(word, 30), "#ffffff", stroke=INK, sw=4)


def tea_hill(fn, color, row_c, lvl, gap=30, bump=None):
    M.hill(fn, color)
    if lvl == 1:
        gap *= 2
    for k in range(1, 14):
        pts = [(x, fn(x) + k * gap) for x in range(0, W + 30, 30)]
        path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), stroke=row_c, sw=7 if lvl == 1 else 5)
        if lvl == 3 and bump:
            for x in range(10 + (k % 2) * 15, W, 30):
                circ(x, fn(x) + k * gap - 5, 7, bump)


def shade_tree(x, yb, h, lvl):
    line(x, yb, x, yb - h, WOOD_D, 10)
    line(x, yb - h * 0.6, x - h * 0.25, yb - h * 0.95, WOOD_D, 6)
    line(x, yb - h * 0.6, x + h * 0.25, yb - h * 0.95, WOOD_D, 6)
    ell(x, yb - h, h * 0.55, h * 0.16, "#2f7d43")
    if lvl == 3:
        ell(x - h * 0.1, yb - h * 1.05, h * 0.35, h * 0.08, "#4c9f45")


def basket(x, y, s):
    poly([(x - 0.5 * s, y - 0.6 * s), (x + 0.5 * s, y - 0.6 * s), (x + 0.38 * s, y + 0.3 * s), (x - 0.38 * s, y + 0.3 * s)], "#c08a4a")
    for k in range(3):
        line(x - 0.45 * s, y - 0.4 * s + k * 0.25 * s, x + 0.45 * s, y - 0.4 * s + k * 0.25 * s, "#8f5a30", 2)
    for dx in (-0.25, 0, 0.25):
        ell(x + dx * s, y - 0.65 * s, 0.16 * s, 0.1 * s, "#3f9a52")


def kebunteh(lvl):
    rnd = random.Random(20 + lvl)
    start()
    sky(lvl, "#7fcbee", "#e6f7fc")
    for cx, cy, s in ((W * 0.1, H * 0.1, 60), (W * 0.52, H * 0.53, 50)):
        M.cloud(cx, cy, s, lvl)
    # Gunung Gede-Pangrango (dua puncak)
    mountains(lvl, 700, [(620, 400, 520), (1050, 330, 480)], snow=False)
    if lvl >= 2:
        for bx, by, s in ((820, 470, 20), (870, 445, 15)):
            M.bird(bx, by, s, lvl)
    # kebun teh berlapis
    hills = [(M.wave(640, 30, 1 / 260, 0.5), "#8cc63f", "#76ad33", "#9ed24f"),
             (M.wave(760, 35, 1 / 220, 2.0), "#6fb83a", "#5b9f2d", "#86c94b"),
             (M.wave(900, 30, 1 / 200, 3.3), "#5aa832", "#488f26", "#72bf45")]
    for i, (fn, c, rc, bc) in enumerate(hills):
        if lvl == 1 and i == 0:
            M.hill(fn, c)
            continue
        tea_hill(fn, c, rc, lvl, bump=bc)
        if lvl >= 2 and i == 0:
            for sx in (300, 1350, 1600):
                shade_tree(sx, fn(sx) + 20, 130, lvl)
        if lvl == 3 and i == 1:
            for sx in (180, 1480):
                shade_tree(sx, fn(sx) + 25, 170, lvl)
            # saung
            sx, sy = 1200, hills[1][0](1200) + 20
            rect(sx - 60, sy - 70, 120, 70, "#c08a4a")
            poly([(sx - 85, sy - 65), (sx, sy - 125), (sx + 85, sy - 65)], "#8f5a30")
            rect(sx - 20, sy - 50, 40, 50, WOOD_D)
    # jalan setapak
    pts = []
    for y in range(880, H + 1, 20):
        t = (y - 880) / (H - 880)
        c = W / 2 + 70 * math.sin(t * 2.2 + 0.4)
        pts.append((c, y, 25 + t * 170))
    poly([(c - hw, y) for c, y, hw in pts] + [(c + hw, y) for c, y, hw in pts[::-1]], "#e2c79a")
    # rumput depan
    rect(0, 1000, W, H - 1000, "#7cc36a")
    poly([(c - hw, y) for c, y, hw in pts if y >= 1000] + [(c + hw, y) for c, y, hw in pts[::-1] if y >= 1000], "#e2c79a")
    if lvl >= 2:
        grass_tufts(lvl, rnd, 1010, H - 10, 30 if lvl == 2 else 60)
    # tokoh & layang-layang
    yf = H - 35
    if lvl == 1:
        chars = [(300, 400, "guru_p", "wave", None), (470, 300, "murid_l", "wave", None), (W - 460, 300, "murid_ph", "wave", None)]
        M.bin_(W - 290, yf, 80, lvl)
        strings = {}
    elif lvl == 2:
        chars = [(200, 290, "murid_l", "wave", None), (360, 370, "guru_p", "stand", None), (520, 285, "murid_ph", "hold", "bibit"),
                 (W - 560, 285, "murid_l", "throw", "sampah"), (W - 260, 290, "murid_p", "wave", None)]
        M.bin_(W - 440, yf, 75, lvl)
        strings = {0: 0, 4: 6}
    else:
        chars = [(170, 335, "guru_l", "wave", None), (310, 255, "murid_l", "wave", None), (440, 250, "murid_ph", "hold", "bibit"),
                 (575, 255, "murid_p", "wave", None), (W - 640, 255, "murid_l", "throw", "sampah"), (W - 400, 250, "murid_p", "hold", "kamera"),
                 (W - 260, 330, "guru_p", "stand", None), (W - 120, 255, "murid_ph", "wave", None)]
        M.bin_(W - 525, yf, 70, lvl)
        basket(700, yf - 20, 70)
        strings = {1: 0, 3: 2, 7: 6}
    kx = [150, 400, 650, 900, 1150, 1400, 1650]
    ky = [320, 255, 330, 420, 330, 255, 320]
    targets = {}
    for ci, kidx in strings.items():
        x, h = chars[ci][0], chars[ci][1]
        targets[kidx] = hand_up(x, yf, h)
    M.title(lvl)
    for i, word in enumerate(NILAI):
        kite(kx[i], ky[i], word, COLS[i], lvl, targets.get(i))
    if lvl == 3:
        M.butterfly(760, 1080, 20, "#f7a531", "#e84a5f")
        M.butterfly(1150, 1050, 18, "#b25fd1", "#5bb7e0")
    flowers_strip(lvl, rnd, 1030, H - 15, avoid=((720, 1100),))
    for i, (x, h, kind, pose, item) in enumerate(chars):
        skin = "#d9a57b" if i % 3 == 1 else "#f1c9a5"
        person(x, yf, h, kind, pose, lvl, item=item, skin=skin)
    return end()


# ====================================================================== 2. PANTAI
def boat(mx, wy, word, color, lvl, s=1.0):
    sw_, sh_ = 190 * s, 125 * s
    top = wy - 40 * s - sh_ - 25 * s
    line(mx, wy - 30 * s, mx, top - 30 * s, WOOD_D, 6 * s)
    poly([(mx, top - 30 * s), (mx + 36 * s, top - 20 * s), (mx, top - 10 * s)], "#ffd34d")
    poly([(mx - sw_ / 2, top), (mx + sw_ / 2, top + 8 * s), (mx + sw_ / 2 - 6 * s, top + sh_), (mx - sw_ / 2 + 6 * s, top + sh_)],
         color, stroke=INK if lvl == 3 else None, sw=3)
    if lvl >= 2:
        line(mx - sw_ / 2 + 8, top + sh_ - 14 * s, mx + sw_ / 2 - 8, top + sh_ - 14 * s, "#ffffff", 4)
    hull_c = "#ffffff" if lvl > 1 else WOOD
    poly([(mx - 120 * s, wy - 40 * s), (mx + 120 * s, wy - 40 * s), (mx + 85 * s, wy), (mx - 85 * s, wy)], hull_c,
         stroke=WOOD_D if lvl > 1 else None, sw=3)
    if lvl >= 2:
        rect(mx - 110 * s, wy - 40 * s, 220 * s, 10 * s, "#d23a3a")
    if lvl == 1:
        text(mx, top + sh_ / 2 + 12 * s, word, fit(word, 34) * s, "#ffffff")
    else:
        long_ = len(word) >= 7
        icon(word, mx - (72 if long_ else 62) * s, top + sh_ / 2 - 6 * s, (15 if long_ else 18) * s, "#ffffff")
        text(mx + (24 if long_ else 20) * s, top + sh_ / 2 + 4 * s, word, (20 if long_ else 28) * s, "#ffffff")
    if lvl == 3:
        for k in range(3):
            line(mx - 70 + k * 20, wy + 10 + k * 8, mx + 50 - k * 15, wy + 10 + k * 8, "#8fd3f0", 3)


def palm(x, yb, h, lean, lvl):
    tx, ty = x + lean, yb - h
    path(f"M{x:.1f},{yb:.1f} Q{x + lean * 0.2:.1f},{yb - h * 0.5:.1f} {tx:.1f},{ty:.1f}", stroke="#9c6a3c", sw=34)
    if lvl >= 2:
        for k in range(1, 9):
            t = k / 9
            px = (1 - t) ** 2 * x + 2 * (1 - t) * t * (x + lean * 0.2) + t * t * tx
            py = (1 - t) ** 2 * yb + 2 * (1 - t) * t * (yb - h * 0.5) + t * t * ty
            line(px - 16, py, px + 16, py - 4, "#7a4a26", 3)
    for ang in (-170, -140, -105, -70, -35, -5, 20):
        a_ = math.radians(ang)
        ex, ey = tx + 190 * math.cos(a_), ty + 190 * math.sin(a_) + 60
        path(f"M{tx:.1f},{ty:.1f} Q{(tx + ex) / 2:.1f},{min(ty, ey) - 50:.1f} {ex:.1f},{ey:.1f}", stroke="#2f8a3f", sw=26)
        if lvl == 3:
            path(f"M{tx:.1f},{ty:.1f} Q{(tx + ex) / 2:.1f},{min(ty, ey) - 50:.1f} {ex:.1f},{ey:.1f}", stroke="#4fae55", sw=8)
    for dx, dy in ((-14, 12), (14, 14), (0, 26)):
        circ(tx + dx, ty + dy, 15, "#7a4a26")


def lighthouse(x, yb, h, lvl):
    poly([(x - 170, yb + 40), (x - 120, yb - 20), (x - 30, yb - 35), (x + 70, yb - 15), (x + 140, yb + 40)], "#8a8f96")
    if lvl >= 2:
        poly([(x + 70, yb - 15), (x + 140, yb + 40), (x + 30, yb + 40)], "#6f747a")
    bw, tw = 60, 38
    n = 5
    for k in range(n):
        y1, y2 = yb - 30 - h * k / n, yb - 30 - h * (k + 1) / n
        w1 = bw - (bw - tw) * k / n
        w2 = bw - (bw - tw) * (k + 1) / n
        poly([(x - w1, y1), (x + w1, y1), (x + w2, y2), (x - w2, y2)], "#d23a3a" if k % 2 == 0 else "#ffffff")
    top = yb - 30 - h
    rect(x - 48, top - 8, 96, 14, INK)
    rect(x - 30, top - 60, 60, 52, "#ffe48a")
    poly([(x - 42, top - 60), (x, top - 100), (x + 42, top - 60)], "#d23a3a")
    if lvl == 3:
        poly([(x + 30, top - 45), (x + 260, top - 110), (x + 260, top + 10)], "#fff3b0")


def crab(x, y, s):
    for sgn in (-1, 1):
        for k in range(3):
            line(x + sgn * 0.4 * s, y + 0.1 * s + k * 0.12 * s, x + sgn * 0.85 * s, y + 0.3 * s + k * 0.15 * s, "#c9372c", 0.08 * s)
        circ(x + sgn * 0.75 * s, y - 0.4 * s, 0.2 * s, "#e0473c")
    ell(x, y, 0.55 * s, 0.35 * s, "#e0473c")
    for sgn in (-1, 1):
        line(x + sgn * 0.15 * s, y - 0.3 * s, x + sgn * 0.2 * s, y - 0.55 * s, "#c9372c", 0.06 * s)
        circ(x + sgn * 0.2 * s, y - 0.58 * s, 0.07 * s, INK)


def starfish(x, y, s, c="#f7a531"):
    pts = []
    for k in range(10):
        r = s if k % 2 == 0 else s * 0.42
        t = -math.pi / 2 + k * math.pi / 5
        pts.append((x + r * math.cos(t), y + r * math.sin(t)))
    poly(pts, c)


def sandcastle(x, yb, s, lvl):
    rect(x - 0.9 * s, yb - 0.6 * s, 1.8 * s, 0.6 * s, "#e3be78")
    rect(x - 0.45 * s, yb - 1.2 * s, 0.9 * s, 0.6 * s, "#e3be78")
    for dx in (-0.9, -0.45, 0, 0.45):
        rect(x + dx * s, yb - 0.72 * s, 0.22 * s, 0.14 * s, "#e3be78")
    line(x, yb - 1.2 * s, x, yb - 1.7 * s, WOOD_D, 3)
    poly([(x, yb - 1.7 * s), (x + 0.35 * s, yb - 1.58 * s), (x, yb - 1.46 * s)], "#d23a3a")
    if lvl == 3:
        rect(x - 0.12 * s, yb - 0.35 * s, 0.24 * s, 0.35 * s, "#c9a15f")


def umbrella(x, yb, s):
    line(x, yb, x + 0.1 * s, yb - 1.6 * s, "#666666", 6)
    cx, cy = x + 0.1 * s, yb - 1.6 * s
    for k in range(4):
        a1, a2 = math.pi + k * math.pi / 4, math.pi + (k + 1) * math.pi / 4
        poly([(cx, cy), (cx + s * math.cos(a1), cy + 0.55 * s * math.sin(a1)), (cx + s * math.cos(a2), cy + 0.55 * s * math.sin(a2))],
             "#e84a5f" if k % 2 == 0 else "#ffffff")


def pantai(lvl):
    rnd = random.Random(40 + lvl)
    HOR, SHORE = 520, 850
    start()
    sky(lvl, "#6ec6ef", "#fdf1d6", y2=HOR + 5)
    M.sun(lvl)
    for cx, cy, s in ((W * 0.14, H * 0.2, 60), (W * 0.62, H * 0.25, 50)):
        M.cloud(cx, cy, s, lvl)
    rect(0, HOR, W, SHORE - HOR + 40, "#2f9fd0")
    if lvl >= 2:
        rect(0, HOR, W, 70, "#5bb7e0")
        for k in range(12):
            x = rnd.uniform(0, W)
            y = rnd.uniform(HOR + 90, SHORE - 30)
            path(f"M{x:.1f},{y:.1f} q18,-10 36,0 t36,0", stroke="#9fdcf3", sw=4)
    if lvl >= 2:
        lighthouse(170, HOR + 110, 300, lvl)
    if lvl == 3:
        for bx, by, s in ((700, 330, 22), (760, 300, 17), (1180, 360, 20)):
            M.bird(bx, by, s, lvl)
    ribbon_title(lvl)
    back = [(420, HOR + 105), (760, HOR + 115), (1100, HOR + 105), (1440, HOR + 115)]
    front = [(590, HOR + 255), (930, HOR + 265), (1270, HOR + 255)]
    for i, (mx, wy) in enumerate(back + front):
        boat(mx, wy, NILAI[i], COLS[i], lvl, 0.92 if i < 4 else 1.0)
    # pasir
    shore = [(x, SHORE + 18 * math.sin(x / 170) + 8 * math.sin(x / 60)) for x in range(0, W + 20, 20)]
    poly(shore + [(W, H), (0, H)], "#f2d9a0")
    if lvl >= 2:
        path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in shore), stroke="#ffffff", sw=10)
    if lvl == 3:
        for _ in range(25):
            circ(rnd.uniform(0, W), rnd.uniform(SHORE + 60, H - 10), 3, "#dcc088")
    palm(W - 60, H - 80, 520, 20, lvl)
    if lvl == 3:
        palm(40, H - 60, 380, 10, lvl)
    yf = H - 35
    if lvl == 1:
        chars = [(280, 400, "guru_p", "wave", None), (450, 300, "murid_l", "wave", None), (W - 520, 300, "murid_ph", "wave", None)]
        M.bin_(W - 370, yf, 80, lvl)
        starfish(700, H - 70, 30)
    elif lvl == 2:
        chars = [(200, 290, "murid_l", "throw", "sampah"), (440, 370, "guru_p", "wave", None), (590, 285, "murid_ph", "hold", "kamera"),
                 (W - 640, 285, "murid_l", "wave", None), (W - 380, 285, "murid_p", "wave", None)]
        M.bin_(W - 1780 + 90, yf, 72, lvl) if False else M.bin_(330, yf, 72, lvl)
        sandcastle(W - 510, yf, 70, lvl)
        starfish(760, H - 60, 26)
        crab(1120, H - 70, 45)
    else:
        chars = [(150, 330, "guru_l", "wave", None), (410, 255, "murid_l", "throw", "sampah"), (640, 250, "murid_ph", "hold", "kamera"),
                 (W - 760, 255, "murid_p", "wave", None), (W - 610, 250, "murid_l", "hold", "bibit"), (W - 470, 330, "guru_p", "wave", None),
                 (W - 330, 255, "murid_ph", "hold", "buku"), (W - 190, 250, "murid_l", "wave", None)]
        M.bin_(540, yf, 66, lvl)
        umbrella(270, yf - 30, 150)
        sandcastle(820, yf, 70, lvl)
        starfish(1000, H - 55, 24)
        starfish(80, H - 40, 20, "#e84a5f")
        crab(1060, H - 120, 42)
        crab(260, H - 40, 34)
        for x, y in ((720, 1170), (940, 1110)):
            path(f"M{x - 16},{y} Q{x},{y - 30} {x + 16},{y} Z", "#f6c9c0")
    for i, (x, h, kind, pose, item) in enumerate(chars):
        person(x, yf, h, kind, pose, lvl, item=item, skin="#d9a57b" if i % 3 == 1 else "#f1c9a5")
    return end()


# ====================================================================== 3. KERETA & SAWAH
def carriage(x0, yb, w, word, color, lvl, idx):
    h = 150
    top = yb - h
    rect(x0, top - 16, w, 20, "#555b66", rx=6)
    rect(x0, top, w, h, color, rx=10, stroke=INK if lvl == 3 else None, sw=3)
    # jendela & penumpang
    nwin = 2
    ww = (w - 30) / nwin - 10
    for k in range(nwin):
        wx = x0 + 15 + k * (ww + 20)
        rect(wx, top + 14, ww, 58, "#dff3fb", rx=6)
        if lvl >= 2:
            hx = wx + ww / 2
            skin = "#d9a57b" if (idx + k) % 2 else "#f1c9a5"
            rect(hx - 20, top + 56, 40, 16, "#ffffff")
            circ(hx, top + 44, 16, skin)
            if (idx + k) % 3 == 0:
                path(f"M{hx - 20:.1f},{top + 46:.1f} A20,20 0 0 1 {hx + 20:.1f},{top + 46:.1f} L{hx + 20:.1f},{top + 62:.1f} "
                     f"L{hx - 20:.1f},{top + 62:.1f} Z", "#ffffff", stroke="#b9b9b9", sw=1.5)
                circ(hx, top + 46, 12, skin)
            else:
                path(f"M{hx - 17:.1f},{top + 42:.1f} A17,17 0 0 1 {hx + 17:.1f},{top + 42:.1f} Z", "#2a2a2a")
            circ(hx - 5, top + 45, 2, INK)
            circ(hx + 5, top + 45, 2, INK)
        if lvl == 3:
            rect(wx, top + 14, ww, 8, "#c3e6f2")
    rect(x0 + 8, top + 82, w - 16, 58, "#ffffff" if lvl > 1 else color, rx=6)
    tc = color if lvl > 1 else "#ffffff"
    if lvl == 1:
        text(x0 + w / 2, top + 124, word, fit(word, 34), tc)
    else:
        long_ = len(word) >= 7
        icon(word, x0 + (24 if long_ else 32), top + 111, 13 if long_ else 16, color)
        text(x0 + w / 2 + (22 if long_ else 18), top + 120, word, 29 if not long_ else 19, tc)
    for wx in (x0 + 40, x0 + w - 40):
        circ(wx, yb + 8, 22, "#333333")
        circ(wx, yb + 8, 8, "#aaaaaa" if lvl > 1 else "#333333")
    rect(x0 + w - 2, yb - 30, 14, 10, "#333333")


def locomotive(x0, yb, lvl):
    rect(x0 + 150, yb - 200, 120, 200, "#d23a3a", rx=10, stroke=INK if lvl == 3 else None, sw=3)
    rect(x0 + 140, yb - 216, 140, 20, "#333333", rx=6)
    rect(x0 + 172, yb - 180, 76, 60, "#dff3fb", rx=6)
    if lvl >= 2:   # masinis = guru
        circ(x0 + 210, yb - 138, 18, "#f1c9a5")
        rect(x0 + 188, yb - 168, 44, 12, "#2f4f7f", rx=5)
        circ(x0 + 204, yb - 140, 2.2, INK)
        circ(x0 + 216, yb - 140, 2.2, INK)
    rect(x0 + 20, yb - 130, 140, 110, "#2f7fc1", rx=40, stroke=INK if lvl == 3 else None, sw=3)
    rect(x0 + 50, yb - 190, 34, 64, "#333333")
    rect(x0 + 42, yb - 200, 50, 16, "#333333", rx=4)
    circ(x0 + 26, yb - 90, 14, "#ffd34d")
    poly([(x0 + 20, yb - 30), (x0 - 20, yb + 10), (x0 + 40, yb + 10)], "#555555")
    if lvl >= 2:
        rect(x0 + 20, yb - 60, 250, 12, "#ffd34d")
    for wx, r in ((x0 + 60, 26), (x0 + 125, 26), (x0 + 215, 32)):
        circ(wx, yb + 8 - (r - 22), r, "#333333")
        circ(wx, yb + 8 - (r - 22), r * 0.35, "#d23a3a" if lvl > 1 else "#333333")
    return x0 + 67, yb - 200   # cerobong


def terrace(lvl, top_y, bot_y):
    n = 7
    cols = ["#9ccc3d", "#86bb34"] if lvl == 1 else ["#a8d84a", "#8cc63f", "#7ab83a"]
    for k in range(n):
        y = top_y + (bot_y - top_y) * k / n
        fn = (lambda y0, kk: (lambda x: y0 + 18 * math.sin(x / 260 + kk * 0.8)))(y, k)
        pts = [(0, H)] + [(x, fn(x)) for x in range(0, W + 30, 30)] + [(W, H)]
        poly(pts, cols[k % len(cols)])
        path("M" + " L".join(f"{x:.1f},{fn(x):.1f}" for x in range(0, W + 30, 30)), stroke="#5a8f2e", sw=6)
        if lvl >= 2:
            for x in range(15 + (k % 2) * 20, W, 40):
                yy = fn(x) + 22
                line(x, yy, x - 4, yy - 12, "#4f8a28", 3)
                line(x, yy, x + 4, yy - 12, "#4f8a28", 3)
        if lvl == 3 and k in (1, 4):
            for x0 in (250, 900, 1500):
                ell(x0, fn(x0) + 30, 110, 12, "#bfe3e8")


def egret(x, yf, s):
    line(x - 0.05 * s, yf, x - 0.1 * s, yf - 0.5 * s, "#e0a43a", 0.05 * s)
    line(x + 0.1 * s, yf, x + 0.08 * s, yf - 0.5 * s, "#e0a43a", 0.05 * s)
    ell(x, yf - 0.65 * s, 0.35 * s, 0.2 * s, "#ffffff", -15)
    path(f"M{x + 0.25 * s:.1f},{yf - 0.75 * s:.1f} Q{x + 0.45 * s:.1f},{yf - 1.0 * s:.1f} {x + 0.35 * s:.1f},{yf - 1.2 * s:.1f}", stroke="#ffffff", sw=0.1 * s)
    circ(x + 0.38 * s, yf - 1.22 * s, 0.1 * s, "#ffffff")
    line(x + 0.45 * s, yf - 1.22 * s, x + 0.7 * s, yf - 1.18 * s, "#e0a43a", 0.05 * s)


def kereta(lvl):
    rnd = random.Random(60 + lvl)
    TRACK = 815
    start()
    sky(lvl, "#7fcbee", "#eaf7fb")
    for cx, cy, s in ((W * 0.9, H * 0.3, 55),):
        M.cloud(cx, cy, s, lvl)
    mountains(lvl, 560, [(300, 250, 380), (1300, 300, 480), (1700, 220, 300)], "#9bbfcf", "#85abbd", snow=True)
    if lvl >= 2:
        M.hill(M.wave(520, 30, 1 / 240, 1.1), "#7cc07f")
    terrace(lvl, 500, TRACK - 30)
    if lvl >= 2:
        M.tree_round(1760, 560, 190, lvl)
        M.tree_round(60, 590, 170, lvl)
    if lvl == 3:
        for x in (520, 1180):
            egret(x, 600, 50)
        # orang-orangan sawah
        sx, sy = 980, 600
        line(sx, sy, sx, sy - 110, WOOD_D, 6)
        line(sx - 45, sy - 80, sx + 45, sy - 80, WOOD_D, 6)
        rect(sx - 26, sy - 90, 52, 50, "#e0473c")
        circ(sx, sy - 105, 16, "#f3e3c8")
        poly([(sx - 32, sy - 115), (sx, sy - 145), (sx + 32, sy - 115)], "#d9b35a")
    # rel
    rect(0, TRACK + 22, W, 26, "#9a8f84")
    for x in range(0, W, 40):
        rect(x + 6, TRACK + 26, 26, 12, WOOD_D)
    rect(0, TRACK + 28, W, 7, "#6b6b6b")
    # kereta
    cx_, cy_ = locomotive(40, TRACK, lvl)
    x = 330
    for i, word in enumerate(NILAI):
        carriage(x, TRACK, 190, word, COLS[i], lvl, i)
        x += 205
    # asap menuju judul awan
    TX, TY = W / 2, 150
    for k in range(7):
        t = (k + 0.3) / 7.3
        px = cx_ + (TX - 420 - cx_) * t
        py = cy_ - 40 + (TY + 40 - cy_) * t - 60 * math.sin(t * math.pi)
        circ(px, py, 22 + 16 * t, "#f4f4f4" if lvl > 1 else "#ffffff")
    cloud_title(lvl, TX, TY)
    if lvl >= 2:
        M.sun(lvl) if False else None
        for bx, by, s in ((1320, 330, 20), (1370, 305, 15)):
            M.bird(bx, by, s, lvl)
    # rumput depan
    rect(0, TRACK + 48, W, H - TRACK - 48, "#7cc36a")
    if lvl >= 2:
        grass_tufts(lvl, rnd, TRACK + 70, H - 10, 30 if lvl == 2 else 60)
    yf = H - 35
    if lvl == 1:
        chars = [(300, 330, "guru_p", "wave", None), (470, 270, "murid_l", "wave", None), (W - 460, 270, "murid_ph", "wave", None)]
        M.bin_(W - 300, yf, 75, lvl)
    elif lvl == 2:
        chars = [(200, 270, "murid_l", "hold", "bibit"), (360, 320, "guru_p", "wave", None), (510, 265, "murid_ph", "wave", None),
                 (W - 560, 270, "murid_l", "throw", "sampah"), (W - 270, 265, "murid_p", "hold", "kamera")]
        M.bin_(W - 440, yf, 70, lvl)
    else:
        chars = [(160, 320, "guru_l", "wave", None), (300, 250, "murid_l", "hold", "bibit"), (430, 245, "murid_ph", "wave", None),
                 (560, 250, "murid_p", "hold", "buku"), (W - 640, 250, "murid_l", "throw", "sampah"), (W - 410, 245, "murid_p", "hold", "kamera"),
                 (W - 270, 320, "guru_p", "wave", None), (W - 130, 250, "murid_ph", "wave", None)]
        M.bin_(W - 525, yf, 66, lvl)
        M.rabbit(760, H - 50, 45)
        M.butterfly(900, 1000, 20, "#f7a531", "#e84a5f")
        M.butterfly(1100, 1060, 18, "#b25fd1", "#5bb7e0")
    flowers_strip(lvl, rnd, TRACK + 90, H - 15, avoid=())
    for i, (x, h, kind, pose, item) in enumerate(chars):
        person(x, yf, h, kind, pose, lvl, item=item, skin="#d9a57b" if i % 3 == 1 else "#f1c9a5")
    return end()


# ====================================================================== jalankan
TEMA = {
    "kebunteh": (kebunteh, "Kebun Teh & Layang-layang", {
        1: ("MUDAH", ["Warna rata, baris teh sederhana", "7 layang-layang berisi nilai", "1 guru + 2 murid"]),
        2: ("SEDANG", ["Ikon di layang-layang, pohon pelindung", "Murid menerbangkan layang-layang", "1 guru + 4 murid beraktivitas"]),
        3: ("SULIT", ["Gradasi, tekstur pucuk teh, saung", "Kupu-kupu, keranjang petik teh", "2 guru + 6 murid"])}),
    "pantai": (pantai, "Pantai & Perahu Layar", {
        1: ("MUDAH", ["Laut & pasir warna rata", "7 perahu layar berisi nilai", "1 guru + 2 murid"]),
        2: ("SEDANG", ["Mercusuar, ombak, ikon di layar", "Istana pasir, kepiting, bintang laut", "1 guru + 4 murid beraktivitas"]),
        3: ("SULIT", ["Gradasi senja, 2 pohon kelapa", "Payung pantai, burung camar, kerang", "2 guru + 6 murid"])}),
    "kereta": (kereta, "Kereta Sapta Pesona & Sawah", {
        1: ("MUDAH", ["Sawah terasering warna rata", "Lokomotif + 7 gerbong nilai", "1 guru + 2 murid"]),
        2: ("SEDANG", ["Murid di jendela, guru jadi masinis", "Ikon di gerbong, padi, burung", "1 guru + 4 murid beraktivitas"]),
        3: ("SULIT", ["Gradasi, gunung bersalju, air sawah", "Burung kuntul, orang-orangan sawah", "2 guru + 6 murid"])}),
}

for tema in [t.strip() for t in args.tema.split(",") if t.strip()]:
    fn, nama, desk = TEMA[tema]
    results = {}
    for nm in [t.strip() for t in args.tingkat.split(",") if t.strip()]:
        lvl = M.LV[nm]
        svg = fn(lvl)
        M.save(svg, f"{tema}-{nm}")
        M.save(M.with_grid(svg), f"{tema}-{nm}-grid")
        results[lvl] = svg
        print(f"OK {tema}-{nm}: {len(M.palette(svg))} warna")
    M.ringkasan(results, desk, f"Mural {args.judul.title()} - {nama}", f"ringkasan-{tema}", args.lebar, args.tinggi)
    print(f"OK ringkasan-{tema}")
