#!/usr/bin/env python3
"""
SABIHA Arsitek - Sketsa perspektif 3D gapura (tanpa biaya).
Ukuran sama dengan sketsa_gapura.py. Contoh:
    python3 perspektif_gapura.py --lebar-total 6 --dalam-atap 1.5 --out perspektif-v4
"""
import argparse
import html
import math

p = argparse.ArgumentParser()
p.add_argument("--bukaan", type=float, default=3.0)
p.add_argument("--lebar-total", type=float, default=None)
p.add_argument("--ped-lebar", type=float, default=1.2)
p.add_argument("--ped-dalam", type=float, default=1.2)
p.add_argument("--ped-tinggi", type=float, default=2.0)
p.add_argument("--tinggi-tiang", type=float, default=1.0)
p.add_argument("--overhang", type=float, default=0.3)
p.add_argument("--dalam-atap", type=float, default=1.5)
p.add_argument("--tinggi-atap", type=float, default=0.4)
p.add_argument("--yaw", type=float, default=22, help="sudut putar pandangan (derajat)")
p.add_argument("--pitch", type=float, default=7, help="sudut pandang dari atas (derajat)")
p.add_argument("--nama", default="GAPURA SEKOLAH")
p.add_argument("--versi", default="v4")
p.add_argument("--out", default="perspektif-gapura-v4")
a = p.parse_args()

PW, PD, PH, TH = a.ped_lebar, a.ped_dalam, a.ped_tinggi, a.tinggi_tiang
OV, D, RISE = a.overhang, a.dalam_atap, a.tinggi_atap
B = a.bukaan if not a.lebar_total else a.lebar_total - 2 * OV - 2 * PW
if B <= 0:
    raise SystemExit("Bukaan <= 0, periksa ukuran.")
W = 2 * OV + 2 * PW + B
Y_BEAM, BEAM_H = PH + TH, 0.14
Y_EAVE = Y_BEAM + 0.25
Y_RIDGE = Y_EAVE + RISE
P0 = (D - PD) / 2
CAP, COL, INS = 0.15, 0.07, 0.22

ty, tp = math.radians(a.yaw), math.radians(a.pitch)
cy, sy_, cp, sp = math.cos(ty), math.sin(ty), math.cos(tp), math.sin(tp)


def view(pt):
    x, y, z = pt
    xr = x * cy + z * sy_
    zr = -x * sy_ + z * cy
    return xr, y * cp + zr * sp, zr * cp - y * sp   # screen x, screen y(up), depth


faces = []   # (depth, pts3d, fill, stroke, sw, opacity)


def face(pts, fill, stroke="#2b2b2b", sw=1.1, op=1.0, bias=0.0):
    d = sum(view(q)[2] for q in pts) / len(pts) + bias
    faces.append((d, pts, fill, stroke, sw, op))


def shade(base, k):
    r, g, b = (int(base[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * k))) for c in (r, g, b))


def box(x0, y0, z0, x1, y1, z1, col, bias=0.0):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    for idx, k in (((0, 1, 2, 3), 1.0), ((4, 5, 6, 7), 0.8), ((0, 3, 7, 4), 0.82),
                   ((1, 2, 6, 5), 0.9), ((3, 2, 6, 7), 1.12), ((0, 1, 5, 4), 0.6)):
        face([v[i] for i in idx], shade(col, k), bias=bias)


lines = []   # garis tambahan (bracing, rusuk spandek) digambar dengan depth


def seg(p1, p2, c="#4a4f5a", w=1.6, bias=0.0):
    d = (view(p1)[2] + view(p2)[2]) / 2 + bias
    lines.append((d, p1, p2, c, w))


# ---------------------------------------------------------------- model
ped_x = [OV, OV + PW + B]
for px in ped_x:
    box(px, 0, P0, px + PW, PH, P0 + PD, "#bdbdb6")
    box(px - 0.05, PH, P0 - 0.05, px + PW + 0.05, PH + CAP, P0 + PD + 0.05, "#a9a9a2")
    cx = [px + INS, px + PW - INS]
    cz = [P0 + INS, P0 + PD - INS]
    for x in cx:
        for z in cz:
            box(x - COL / 2, PH + CAP, z - COL / 2, x + COL / 2, Y_BEAM, z + COL / 2, "#dfe6ea", bias=-0.01)
    for z in cz:   # bracing sisi depan & belakang
        seg((cx[0], PH + CAP + 0.05, z), (cx[1], Y_BEAM - 0.05, z))
    for x in cx:   # bracing sisi samping
        seg((x, PH + CAP + 0.05, cz[0]), (x, Y_BEAM - 0.05, cz[1]))

# balok keliling (depan & belakang) + balok melintang
for z in (P0 + INS, P0 + PD - INS):
    box(OV - 0.1, Y_BEAM, z - 0.05, W - OV + 0.1, Y_BEAM + BEAM_H, z + 0.05, "#cfd6db")
for px in ped_x:
    box(px + INS - 0.05, Y_BEAM, P0 + INS, px + PW - INS + 0.05, Y_BEAM + BEAM_H, P0 + PD - INS, "#cfd6db")
# rusuk teritis ke tepi atap
for x in [0.1 + i * (W - 0.2) / 8 for i in range(9)]:
    xb = min(max(x, OV), W - OV)
    seg((x, Y_EAVE - 0.03, 0.02), (xb, Y_BEAM + BEAM_H, P0 + INS), "#6a707c", 1.0)
    seg((x, Y_EAVE - 0.03, D - 0.02), (xb, Y_BEAM + BEAM_H, P0 + PD - INS), "#6a707c", 1.0)

# atap perisai
e = [(0, Y_EAVE, 0), (W, Y_EAVE, 0), (W, Y_EAVE, D), (0, Y_EAVE, D)]
r1, r2 = (D / 2, Y_RIDGE, D / 2), (W - D / 2, Y_RIDGE, D / 2)
ROOF, BIAS = "#b3453a", -50   # atap selalu digambar paling akhir (di atas rangka)
face([e[0], e[1], r2, r1], ROOF, sw=1.6, bias=BIAS)             # depan
face([e[3], e[2], r2, r1], shade(ROOF, 0.75), sw=1.6, bias=BIAS - 0.5 + 0.49)  # belakang
face([e[0], e[3], r1], shade(ROOF, 0.85), sw=1.6, bias=BIAS)     # kiri
face([e[1], e[2], r2], shade(ROOF, 0.7), sw=1.6, bias=BIAS)      # kanan


def roof_front(x, t):   # titik di sisi depan atap; t=0 tepi, t=1 garis bubungan/jurai
    zt = min(x, W - x, D / 2)
    z = zt * t
    return (x, Y_EAVE + RISE * z / (D / 2), z)


# panel transparan biru
for c in (W / 2 - 0.8, W / 2 + 0.8):
    x0, x1 = c - 0.3, c + 0.3
    face([roof_front(x0, 0), roof_front(x1, 0), roof_front(x1, 1), roof_front(x0, 1)],
         "#4b86c9", sw=1.0, op=0.92, bias=BIAS - 1)
# rusuk spandek
x = 0.2
while x < W - 0.1:
    seg(roof_front(x, 0), roof_front(x, 1), "#7f2d25", 0.7, bias=BIAS - 2)
    x += 0.2
seg(e[0], e[1], "#2b2b2b", 3, bias=BIAS - 3)
seg(r1, r2, "#2b2b2b", 2.2, bias=BIAS - 3)

# ---------------------------------------------------------------- proyeksi & kanvas
CW, CH = 1400, 1000
allpts = [q for f in faces for q in f[1]] + [(-0.8, 0, -1.6), (W + 0.8, 0, -1.6), (-0.8, 0, D + 1.2), (W + 0.8, 0, D + 1.2)]
xs = [view(q)[0] for q in allpts]
ys = [view(q)[1] for q in allpts]
S = min((CW - 220) / (max(xs) - min(xs)), (CH - 330) / (max(ys) - min(ys)))
OX = (CW - (max(xs) - min(xs)) * S) / 2 - min(xs) * S
OY = 150 + max(ys) * S


def scr(q):
    vx, vy, _ = view(q)
    return OX + vx * S, OY - vy * S


o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">',
     f'<rect width="{CW}" height="{CH}" fill="#fbfaf6"/>',
     f'<rect x="20" y="20" width="{CW - 40}" height="{CH - 40}" fill="none" stroke="#2b2b2b" stroke-width="2"/>']


def text(x, y, t, size=13, anchor="middle", w="normal", c="#2b2b2b"):
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" '
             f'text-anchor="{anchor}" font-weight="{w}" fill="{c}">{html.escape(t)}</text>')


def poly(pts, fill, stroke="#2b2b2b", sw=1.1, op=1.0):
    s = " ".join("%.1f,%.1f" % scr(q) for q in pts)
    o.append(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
             f'stroke-linejoin="round" opacity="{op}"/>')


text(CW / 2, 62, f"SKETSA PERSPEKTIF {a.nama}", 24, w="bold")
text(CW / 2, 88, "Rangka baja ringan  |  Pedestal beton  |  Atap perisai spandek", 14, c="#555")

# tanah & jalan
poly([(-0.8, 0, -1.6), (W + 0.8, 0, -1.6), (W + 0.8, 0, D + 1.2), (-0.8, 0, D + 1.2)], "#e9eadf", "none")
poly([(OV + PW, 0, -1.6), (OV + PW + B, 0, -1.6), (OV + PW + B, 0, D + 1.2), (OV + PW, 0, D + 1.2)], "#cfcfcc", "#999", 0.8)

items = [(f[0], "f", f) for f in faces] + [(l[0], "l", l) for l in lines]
items.sort(key=lambda t: -t[0])   # jauh dulu, dekat terakhir
for _, kind, it in items:
    if kind == "f":
        _, pts, fill, stroke, sw, op = it
        poly(pts, fill, stroke, sw, op)
    else:
        _, p1, p2, c, w = it
        (x1, y1), (x2, y2) = scr(p1), scr(p2)
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
                 f'stroke-width="{w}" stroke-linecap="round"/>')

# figur manusia 1,6 m sebagai skala
hx, hz = OV + PW + B * 0.5, -0.6
hb, ht = scr((hx, 0, hz)), scr((hx, 1.6, hz))
hh = hb[1] - ht[1]
o.append(f'<circle cx="{ht[0]:.1f}" cy="{ht[1] + hh * 0.07:.1f}" r="{hh * 0.07:.1f}" fill="#555"/>')
o.append(f'<rect x="{ht[0] - hh * 0.09:.1f}" y="{ht[1] + hh * 0.15:.1f}" width="{hh * 0.18:.1f}" '
         f'height="{hh * 0.85:.1f}" rx="{hh * 0.05:.1f}" fill="#555"/>')


# keterangan & blok judul
ky = CH - 150
text(60, ky, "Ukuran utama", 15, "start", "bold")
info = [f"Lebar total atap  : {W:.2f} m", f"Bukaan bersih     : {B:.2f} m",
        f"Kedalaman atap    : {D:.2f} m", f"Pedestal          : {PW:.2f} x {PD:.2f} x {PH:.2f} m",
        f"Tinggi total      : ± {Y_RIDGE:.2f} m   (figur manusia 1,60 m sebagai skala)"]
for i, t in enumerate(info):
    text(60, ky + 24 + i * 20, t, 13, "start")
o.append(f'<rect x="930" y="{CH - 130}" width="430" height="92" fill="none" stroke="#2b2b2b" stroke-width="1.6"/>')
o.append(f'<line x1="930" y1="{CH - 100}" x2="1360" y2="{CH - 100}" stroke="#2b2b2b"/>')
text(1145, CH - 108, "SABIHA ARSITEK", 15, w="bold")
text(942, CH - 80, f"Proyek : {a.nama}", 12, "start")
text(942, CH - 62, f"Tahap  : Sketsa perspektif {a.versi}", 12, "start")
text(942, CH - 44, "Ukuran asumsi, wajib diukur ulang di lokasi", 12, "start")
o.append("</svg>")

svg = "\n".join(o)
with open(f"{a.out}.svg", "w", encoding="utf-8") as f:
    f.write(svg)
try:
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{a.out}.png", output_width=CW * 2)
    print(f"OK: {a.out}.svg, {a.out}.png")
except ImportError:
    print(f"OK: {a.out}.svg")
print(f"W {W:.2f} | bukaan {B:.2f} | tinggi {Y_RIDGE:.2f}")
