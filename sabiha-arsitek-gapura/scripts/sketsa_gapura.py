#!/usr/bin/env python3
"""
SABIHA Arsitek - Generator sketsa gapura sekolah (baja ringan, atap perisai).

Menghasilkan 1 lembar sketsa (SVG + PNG): tampak depan, tampak samping, denah.
Semua ukuran dalam METER. Ubah lewat argumen CLI, contoh:

    python3 sketsa_gapura.py --bukaan 5 --tinggi-tiang 1.2 --out sketsa

Model acuan: gapura dua pedestal beton + rangka baja ringan + atap spandek
perisai (foto: references/foto-referensi-gapura.jpg).
"""
import argparse
import html

p = argparse.ArgumentParser()
p.add_argument("--bukaan", type=float, default=6.0, help="lebar bukaan bersih antar pedestal")
p.add_argument("--ped-lebar", type=float, default=1.5, help="lebar pedestal (arah jalan melintang)")
p.add_argument("--ped-dalam", type=float, default=1.2, help="kedalaman pedestal (arah jalan memanjang)")
p.add_argument("--ped-tinggi", type=float, default=2.0, help="tinggi pedestal beton")
p.add_argument("--tinggi-tiang", type=float, default=1.0, help="tinggi tiang baja di atas pedestal")
p.add_argument("--overhang", type=float, default=1.0, help="teritis atap di luar pedestal (kiri/kanan)")
p.add_argument("--dalam-atap", type=float, default=3.0, help="kedalaman atap (arah jalan)")
p.add_argument("--tinggi-atap", type=float, default=0.8, help="tinggi atap dari tepi ke bubungan")
p.add_argument("--nama", default="GAPURA SEKOLAH")
p.add_argument("--versi", default="v2", help="label versi di blok judul")
p.add_argument("--out", default="sketsa-gapura-v2", help="nama file tanpa ekstensi")
a = p.parse_args()

B, PW, PD, PH = a.bukaan, a.ped_lebar, a.ped_dalam, a.ped_tinggi
TH, OV, D, RISE = a.tinggi_tiang, a.overhang, a.dalam_atap, a.tinggi_atap
W = 2 * OV + 2 * PW + B                  # lebar total atap
Y_BEAM = PH + TH                         # bawah balok keliling
Y_EAVE = Y_BEAM + 0.25                   # garis tepi atap
Y_RIDGE = Y_EAVE + RISE
RIDGE_LEN = max(W - D, 0)
CAP = 0.15                               # tebal cap pedestal
COL = 0.06                               # lebar tiang hollow (gambar)

S = 72                                   # px per meter
CW, CH = 1400, 1120
INK, GRID = "#2b2b2b", "#8a8a8a"
o = []


def add(s):
    o.append(s)


def line(x1, y1, x2, y2, w=1.4, c=INK, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>')


def rect(x, y, w, h, fill="none", stroke=INK, sw=1.4, op=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')


def poly(pts, fill="none", stroke=INK, sw=1.4, op=1):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    add(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')


def text(x, y, t, size=13, anchor="middle", w="normal", c=INK, rot=0):
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" '
        f'text-anchor="{anchor}" font-weight="{w}" fill="{c}"{r}>{html.escape(t)}</text>')


def dim_h(x1, x2, y, label):
    line(x1, y, x2, y, 1, "#c0392b")
    for x in (x1, x2):
        line(x, y - 6, x, y + 6, 1, "#c0392b")
    text((x1 + x2) / 2, y - 6, label, 12, c="#c0392b")


def dim_v(x, y1, y2, label):
    line(x, y1, x, y2, 1, "#c0392b")
    for y in (y1, y2):
        line(x - 6, y, x + 6, y, 1, "#c0392b")
    text(x - 8, (y1 + y2) / 2, label, 12, c="#c0392b", rot=-90)


def title(x, y, t):
    text(x, y, t, 16, "start", "bold")
    line(x, y + 5, x + 250, y + 5, 1.6)


# ---------------------------------------------------------------- canvas
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">')
add(f'<rect width="{CW}" height="{CH}" fill="#fbfaf6"/>')
rect(20, 20, CW - 40, CH - 40, stroke=INK, sw=2)
text(CW / 2, 60, f"SKETSA KONSEP {a.nama}", 24, w="bold")
text(CW / 2, 84, "Rangka baja ringan  |  Pedestal beton  |  Atap perisai spandek", 14, c="#555")

# ================================================================ TAMPAK DEPAN
X0, GY = 100, 480


def fx(m):
    return X0 + m * S


def fy(m):
    return GY - m * S


title(X0, 130, "TAMPAK DEPAN")
line(X0 - 40, GY, fx(W) + 40, GY, 2)
for k in range(0, 30):                       # arsir tanah
    x = X0 - 40 + k * 26
    if x < fx(W) + 30:
        line(x, GY, x - 8, GY + 9, 0.8, GRID)

# jalan (bukaan)
poly([(fx(OV + PW), GY), (fx(OV + PW + B), GY), (fx(OV + PW + B), GY + 8), (fx(OV + PW), GY + 8)], "#d9d9d9", GRID, 0.8)

ped_x = [OV, OV + PW + B]
cols_x = []
for i, px in enumerate(ped_x):
    # badan pedestal + cap
    rect(fx(px), fy(PH), PW * S, PH * S, "#bdbdb6")
    rect(fx(px) - 5, fy(PH) - CAP * S, PW * S + 10, CAP * S, "#a9a9a2")
    line(fx(px) + 8, fy(PH - 0.35), fx(px) + PW * S - 8, fy(PH - 0.35), 2.2, "#8f8f88")  # list
    # kolom hollow (2 buah tampak depan)
    cx = [px + 0.22, px + PW - 0.22]
    cols_x += cx
    for c in cx:
        rect(fx(c) - COL * S / 2, fy(Y_BEAM), COL * S, TH * S, "#dfe6ea")
        line(fx(c), fy(Y_BEAM), fx(c), fy(PH + CAP), 0.7, GRID)
    # bracing diagonal
    if i == 0:
        line(fx(cx[0]), fy(PH + 0.12), fx(cx[1]), fy(Y_BEAM - 0.1), 1.6, "#556")
    else:
        line(fx(cx[1]), fy(PH + 0.12), fx(cx[0]), fy(Y_BEAM - 0.1), 1.6, "#556")

# balok keliling + rusuk teritis
BEAM_H = 0.14
rect(fx(OV - 0.15), fy(Y_BEAM + BEAM_H), (W - 2 * OV + 0.3) * S, BEAM_H * S, "#cfd6db")
for k in range(0, int(W) + 1):
    x = 0.12 + k * ((W - 0.24) / max(int(W), 1))
    line(fx(x), fy(Y_EAVE - 0.03), fx(min(max(x, OV), W - OV)), fy(Y_BEAM + BEAM_H), 0.9, "#667")
# gording bawah (garis di bawah atap)
line(fx(0), fy(Y_EAVE - 0.03), fx(W), fy(Y_EAVE - 0.03), 2.2, "#667")

# atap perisai (tampak depan = trapesium)
roof = [(fx(0), fy(Y_EAVE)), (fx(D / 2), fy(Y_RIDGE)), (fx(W - D / 2), fy(Y_RIDGE)), (fx(W), fy(Y_EAVE))]
poly(roof, "#b3453a", INK, 1.8)
# rusuk spandek
step = 0.22
x = 0.0
while x <= W:
    top = Y_EAVE + min(RISE, RISE * min(x, W - x) / (D / 2))
    line(fx(x), fy(Y_EAVE), fx(x), fy(top), 0.6, "#7f2d25", op=0.8)
    x += step
# 2 panel transparan biru di tengah
for cxm in (W / 2 - 1.0, W / 2 + 1.0):
    rect(fx(cxm - 0.42), fy(Y_RIDGE), 0.84 * S, RISE * S, "#4b86c9", INK, 1, 0.85)
    for k in range(4):
        line(fx(cxm - 0.42 + 0.21 * k + 0.1), fy(Y_RIDGE), fx(cxm - 0.42 + 0.21 * k + 0.1), fy(Y_EAVE), 0.6, "#fff", op=0.7)
# lis tepi atap
line(fx(0), fy(Y_EAVE), fx(W), fy(Y_EAVE), 3, INK)

# dimensi
dim_h(fx(0), fx(W), fy(Y_RIDGE) - 34, f"{W:.2f} m  (lebar atap)")
dim_h(fx(OV + PW), fx(OV + PW + B), GY + 34, f"{B:.2f} m  (bukaan bersih)")
dim_h(fx(OV), fx(OV + PW), GY + 62, f"{PW:.2f}")
dim_h(fx(OV + PW + B), fx(OV + 2 * PW + B), GY + 62, f"{PW:.2f}")
dim_v(fx(0) - 30, GY, fy(PH), f"{PH:.2f}")
dim_v(fx(0) - 30, fy(PH), fy(Y_BEAM), f"{TH:.2f}")
dim_v(fx(W) + 34, GY, fy(Y_RIDGE), f"tinggi total {Y_RIDGE:.2f} m")
text(fx(W / 2), GY + 92, f"Tinggi bebas bawah balok ± {Y_BEAM:.2f} m", 12, c="#555")

# label
text(fx(OV + PW / 2), fy(PH / 2), "Pedestal", 12, c="#444")
text(fx(OV + PW / 2), fy(PH / 2) + 15, "beton plester", 11, c="#444")
text(fx(W / 2), fy(Y_EAVE) - 6, "atap spandek", 11, c="#fff")

# ================================================================ TAMPAK SAMPING
SX0, SGY = 1040, 480


def sx(m):
    return SX0 + m * S


title(SX0 - 40, 130, "TAMPAK SAMPING")
line(SX0 - 80, SGY, sx(D) + 80, SGY, 2)
p0 = (D - PD) / 2
rect(sx(p0), SGY - PH * S, PD * S, PH * S, "#bdbdb6")
rect(sx(p0) - 5, SGY - (PH + CAP) * S, PD * S + 10, CAP * S, "#a9a9a2")
line(sx(p0) + 8, SGY - (PH - 0.35) * S, sx(p0) + PD * S - 8, SGY - (PH - 0.35) * S, 2.2, "#8f8f88")
for c in (p0 + 0.22, p0 + PD - 0.22):
    rect(sx(c) - COL * S / 2, SGY - Y_BEAM * S, COL * S, TH * S, "#dfe6ea")
line(sx(p0 + 0.22), SGY - (PH + 0.12) * S, sx(p0 + PD - 0.22), SGY - (Y_BEAM - 0.1) * S, 1.6, "#556")
rect(sx(p0 - 0.1), SGY - (Y_BEAM + BEAM_H) * S, (PD + 0.2) * S, BEAM_H * S, "#cfd6db")
poly([(sx(0), SGY - Y_EAVE * S), (sx(D / 2), SGY - Y_RIDGE * S), (sx(D), SGY - Y_EAVE * S)], "#b3453a", INK, 1.8)
line(sx(0), SGY - Y_EAVE * S, sx(D), SGY - Y_EAVE * S, 3, INK)
dim_h(sx(0), sx(D), SGY - Y_RIDGE * S - 34, f"{D:.2f} m  (dalam atap)")
dim_h(sx(p0), sx(p0 + PD), SGY + 34, f"{PD:.2f} m")
dim_v(sx(D) + 44, SGY - Y_EAVE * S, SGY - Y_RIDGE * S, f"{RISE:.2f}")

# ================================================================ DENAH
DX0, DY0 = 100, 690


def dx(m):
    return DX0 + m * S


def dy(m):
    return DY0 + m * S


title(DX0, DY0 - 30, "DENAH  (tampak atas)")
# jalan
rect(dx(OV + PW), dy(0), B * S, D * S, "#e4e4e4", GRID, 0.8)
text(dx(W / 2), dy(D * 0.82), "JALAN MASUK", 13, c="#777")
# batas atap
rect(dx(0), dy(0), W * S, D * S, "none", "#b3453a", 2, dash="9 5")
line(dx(0), dy(0), dx(D / 2), dy(D / 2), 1.2, "#b3453a", "5 4")
line(dx(0), dy(D), dx(D / 2), dy(D / 2), 1.2, "#b3453a", "5 4")
line(dx(W), dy(0), dx(W - D / 2), dy(D / 2), 1.2, "#b3453a", "5 4")
line(dx(W), dy(D), dx(W - D / 2), dy(D / 2), 1.2, "#b3453a", "5 4")
line(dx(D / 2), dy(D / 2), dx(W - D / 2), dy(D / 2), 2, "#b3453a", "5 4")
text(dx(W / 2), dy(D / 2) - 8, "bubungan", 11, c="#b3453a")
# pedestal + tiang
for px in ped_x:
    rect(dx(px), dy(p0), PW * S, PD * S, "#bdbdb6")
    for cx in (px + 0.22, px + PW - 0.22):
        for cy in (p0 + 0.22, p0 + PD - 0.22):
            rect(dx(cx) - 4, dy(cy) - 4, 8, 8, "#556", INK, 1)
line(dx(0) - 24, dy(D / 2), dx(W) + 24, dy(D / 2), 0.8, GRID, "14 4 3 4")
dim_h(dx(OV + PW), dx(OV + PW + B), dy(D) + 34, f"{B:.2f} m")
dim_h(dx(0), dx(W), dy(D) + 62, f"{W:.2f} m")
dim_v(dx(0) - 34, dy(0), dy(D), f"{D:.2f}")
text(dx(OV + PW / 2), dy(p0 + PD) + 20, "P1", 12, w="bold")
text(dx(OV + PW + B + PW / 2), dy(p0 + PD) + 20, "P2", 12, w="bold")

# ================================================================ KETERANGAN
KX, KY = 930, 690
title(KX, KY - 30, "KETERANGAN & ASUMSI")
rows = [
    ("Bukaan bersih", f"{B:.2f} m"),
    ("Pedestal (P1, P2)", f"{PW:.2f} x {PD:.2f} x {PH:.2f} m"),
    ("Tiang baja ringan", f"4 btg/pedestal, t {TH:.2f} m"),
    ("Balok keliling", "hollow ganda, sepanjang bukaan"),
    ("Atap perisai", f"lebar {W:.2f}, dalam {D:.2f}, tinggi {RISE:.2f} m"),
    ("Penutup", "spandek merah + 2 panel transparan"),
    ("Tinggi total", f"± {Y_RIDGE:.2f} m dari muka tanah"),
]
for i, (k, v) in enumerate(rows):
    y = KY + i * 24
    text(KX, y, k, 13, "start", "bold")
    text(KX + 170, y, v, 13, "start")
text(KX, KY + 7 * 24 + 14, "Catatan:", 12, "start", "bold")
notes = [
    "1. Dimensi ASUMSI dari foto referensi, wajib diukur",
    "    ulang di lokasi sebelum dikerjakan.",
    "2. Sketsa konsep, belum gambar kerja/struktur.",
    "3. Pondasi, dimensi profil, dan sambungan dihitung",
    "    pada tahap RAB dan gambar detail.",
]
for i, n in enumerate(notes):
    text(KX, KY + 7 * 24 + 36 + i * 18, n, 12, "start", c="#444")

# blok judul
rect(930, 1000, 450, 100, "none", INK, 1.6)
line(930, 1030, 1380, 1030, 1)
text(1155, 1022, "SABIHA ARSITEK", 15, w="bold")
text(940, 1052, f"Proyek : {a.nama}", 12, "start")
text(940, 1070, f"Tahap  : Sketsa konsep {a.versi} (sebelum RAB)", 12, "start")
text(940, 1088, "Satuan : meter   |   Tanpa skala baku", 12, "start")

add("</svg>")
svg = "\n".join(o)
with open(f"{a.out}.svg", "w", encoding="utf-8") as f:
    f.write(svg)
try:
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=f"{a.out}.png", output_width=CW * 2)
    print(f"OK: {a.out}.svg, {a.out}.png")
except ImportError:
    print(f"OK: {a.out}.svg (pasang cairosvg untuk PNG: pip install cairosvg)")
print(f"Lebar atap {W:.2f} m | Tinggi total {Y_RIDGE:.2f} m | Tinggi bebas {Y_BEAM:.2f} m")
