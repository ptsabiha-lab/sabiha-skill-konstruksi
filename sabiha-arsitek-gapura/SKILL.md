---
name: sabiha-arsitek-gapura
description: Membuat sketsa konsep dan (tahap berikutnya) RAB gapura sekolah rangka baja ringan dengan pedestal beton dan atap perisai spandek, untuk SABIHA Arsitek. Gunakan saat pengguna menyebut gapura, gerbang sekolah, sabiha arsitek gapura, sketsa gapura, atau RAB gapura.
---

# SABIHA Arsitek - Gapura

Skill untuk proyek gapura sekolah milik SABIHA (Cianjur, Jawa Barat).
Bahasa kerja: **Bahasa Indonesia**. Satuan: **meter**.

## Model acuan

Foto acuan: `references/foto-referensi-gapura.jpg`

- Dua pedestal beton/bata plester di kiri dan kanan jalan masuk.
- Di atas tiap pedestal berdiri 4 tiang baja ringan (hollow) dengan bracing diagonal.
- Balok keliling menghubungkan kedua sisi, di atasnya rangka atap baja ringan.
- Atap perisai (4 sisi) penutup spandek merah, dengan 2 panel transparan biru di tengah.

## Alur kerja (urutan wajib)

1. **Sketsa dulu, RAB belakangan.** Jangan menghitung RAB sebelum sketsa disetujui pengguna.
2. Tanyakan ukuran lokasi: lebar jalan/bukaan, tinggi bebas yang dibutuhkan (mobil, truk, ambulans), dan teks/logo sekolah yang akan dipasang.
3. Jalankan generator sketsa dengan ukuran tersebut, tampilkan hasilnya, lalu revisi sampai disetujui.
4. Setelah sketsa disetujui, baru masuk tahap RAB (lihat bagian RAB).

## Tahap 1 - Sketsa

Generator: `scripts/sketsa_gapura.py` (Python 3, butuh `cairosvg` untuk PNG: `pip install cairosvg`).
Hasil: satu lembar SVG + PNG berisi tampak depan, tampak samping, denah, dimensi, keterangan, dan blok judul.

```bash
python3 scripts/sketsa_gapura.py --bukaan 5 --tinggi-tiang 1.2 --nama "GAPURA SDN 1 CIANJUR" --out sketsa-v2
```

Parameter (meter): `--bukaan`, `--ped-lebar`, `--ped-dalam`, `--ped-tinggi`, `--tinggi-tiang`, `--overhang`, `--dalam-atap`, `--tinggi-atap`.

Dimensi asumsi awal (dari foto, **wajib diverifikasi di lokasi**):

| Bagian | Nilai |
|---|---|
| Bukaan bersih | 4,50 m |
| Pedestal | 1,20 x 1,20 x 2,00 m |
| Tiang baja di atas pedestal | 1,00 m |
| Tinggi bebas bawah balok | 3,00 m |
| Teritis atap di luar pedestal | 1,00 m |
| Atap | lebar 8,90 m, dalam 3,00 m, tinggi 0,80 m |
| Tinggi total | sekitar 4,05 m |

Aturan saat menggambar:
- Selalu beri catatan bahwa ukuran adalah asumsi sampai diukur di lokasi.
- Cek tinggi bebas terhadap kendaraan yang lewat. Untuk truk/ambulans, tinggi bebas minimal 4,0 m, sehingga `--tinggi-tiang` atau `--ped-tinggi` perlu dinaikkan.
- Setelah membuat sketsa, periksa gambarnya (label tidak tumpang tindih, dimensi terbaca) sebelum diberikan ke pengguna.

## Tahap 2 - RAB (belum dikerjakan)

Dikerjakan hanya setelah sketsa disetujui. Rencana isi:
- Excel dengan openpyxl, formula hidup, siap dipakai di lapangan (sesuai kebiasaan pengguna).
- Sheet: Input ukuran, Volume, Harga satuan, RAB per pekerjaan, Rekap, Daftar belanja per supplier.
- Pekerjaan: persiapan, galian dan pondasi, pedestal (bata/beton, plester, acian, cat), rangka baja ringan (tiang, balok, kuda-kuda, reng), penutup atap spandek dan panel transparan, nok dan talang, finishing, papan nama/logo.
- Harga satuan **jangan ditebak**: minta dari supplier atau cari harga terkini, dan tandai sumber serta tanggalnya.
- Struktur baja ringan dan pondasi harus dicek tenaga ahli sebelum dibangun. Sampaikan ini di keterangan RAB.

## Skill lain yang direncanakan

Satu folder per skill di repo yang sama: `sabiha-arsitek-gambar` (gambar kerja), dan proyek bangunan lainnya.

## Struktur folder

```
sabiha-arsitek-gapura/
  SKILL.md
  scripts/sketsa_gapura.py
  references/foto-referensi-gapura.jpg
  examples/sketsa-gapura-v1.png (+ .svg)
```
