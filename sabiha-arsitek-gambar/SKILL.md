---
name: sabiha-arsitek-gambar
description: Membuat desain gambar/mural dinding sekolah untuk SABIHA Arsitek, dimulai dari mural Sapta Pesona tema hutan alam dalam 3 tingkat (mudah, sedang, sulit) lengkap dengan tokoh guru dan murid, grid 1 m, dan palet cat. Gunakan saat pengguna menyebut mural, gambar dinding, lukisan dinding sekolah, Sapta Pesona, atau sabiha arsitek gambar.
---

# SABIHA Arsitek - Gambar & Mural Sekolah

Skill desain mural dinding sekolah milik SABIHA (Cianjur, Jawa Barat).
Bahasa kerja: **Bahasa Indonesia**. Satuan: **meter**.

## Alur kerja

1. **Fokus ke gambar.** Jangan membahas biaya kecuali pengguna memintanya.
2. Tanyakan hal yang belum jelas: ukuran dinding (lebar x tinggi), nama sekolah (opsional), dan tema. Sapta Pesona tema hutan alam sudah tersedia.
3. Jalankan generator, lalu **periksa setiap gambar** (teks papan terbaca, tidak ada yang tumpang tindih, tokoh tidak tertutup) sebelum diberikan ke pengguna.
4. Berikan lembar ringkasan dulu (3 tingkat berdampingan), lalu gambar yang dipilih pengguna dan versi grid-nya.

## Mural Sapta Pesona - hutan alam

Generator: `scripts/mural_sapta_pesona.py` (Python 3, butuh `cairosvg` untuk PNG: `pip install cairosvg`).

```bash
python3 scripts/mural_sapta_pesona.py --lebar 6 --tinggi 4 --sekolah "SDN 1 CIANJUR"
```

Opsi: `--lebar`, `--tinggi` (m), `--judul` (default "SAPTA PESONA"), `--sekolah`, `--tingkat mudah,sedang,sulit`, `--prefix`.

Hasil untuk tiap tingkat:
- `mural-<tingkat>.png/.svg`: desain bersih.
- `mural-<tingkat>-grid.png/.svg`: grid 1 m (garis putus-putus tiap 50 cm) dengan label kotak A1, B1, ... untuk memindahkan gambar ke dinding.
- `ringkasan-mural.png`: ketiga tingkat berdampingan, dengan keterangan dan palet cat.

Isi mural: papan judul, 7 papan nilai Sapta Pesona (AMAN, TERTIB, BERSIH, SEJUK, INDAH, RAMAH, KENANGAN), hutan, bukit, jalan setapak, serta tokoh guru dan murid berseragam SD (merah-putih, ada yang berhijab).

| Tingkat | Ciri | Tokoh |
|---|---|---|
| Mudah | Bidang warna rata, tanpa gradasi, papan hanya teks | 1 guru + 2 murid |
| Sedang | Warna dua tone, ikon di papan, sungai, jembatan, burung, semak | 1 guru + 4 murid (menanam, membuang sampah, memotret, melambai) |
| Sulit | Gradasi langit, gunung, garis tepi tokoh, rusa, kelinci, kupu-kupu, jamur | 2 guru + 6 murid beraktivitas |

Aktivitas murid dipilih agar sesuai nilai Sapta Pesona: membuang sampah (Bersih), menanam bibit (Sejuk), memotret (Kenangan), melambai (Ramah).

## Tema lain

Generator: `scripts/mural_tema.py` (memakai fungsi gambar dari `mural_sapta_pesona.py`).

```bash
python3 scripts/mural_tema.py --tema kebunteh,pantai,kereta --lebar 6 --tinggi 4 --sekolah "SDN 1 CIANJUR"
```

| Tema | Referensi | Tempat 7 nilai |
|---|---|---|
| `kebunteh` | Kebun teh & Gunung Gede-Pangrango khas Cianjur, pohon pelindung, saung | 7 layang-layang, sebagian talinya dipegang murid |
| `pantai` | Laut, pasir, mercusuar, pohon kelapa, istana pasir | Layar 7 perahu |
| `kereta` | Sawah terasering, gunung, burung kuntul, orang-orangan sawah | 7 gerbong kereta, murid di jendela, guru jadi masinis |
| `alam` | Alam murni: gunung, tebing, air terjun, danau, sungai, hutan, hewan (pelangi di tingkat sulit) | **Tanpa** tulisan Sapta Pesona dan tanpa tokoh, hanya pemandangan |

Hasil: `<tema>-<tingkat>.png/.svg`, `<tema>-<tingkat>-grid.png`, dan `ringkasan-<tema>.png`.
Setiap tema tetap punya 3 tingkat (mudah, sedang, sulit) dengan pola tokoh yang sama: 1+2, 1+4, 2+6.

## Aturan menggambar

- Tokoh dibuat orisinal dan sederhana. Jangan meniru karakter kartun terkenal atau logo resmi.
- Perbandingan gambar harus sama dengan ukuran dinding (1 m = 300 px).
- Jumlah warna di palet adalah jumlah warna cat yang perlu disiapkan. Tingkat mudah dibuat seminim mungkin.
- Setiap revisi disimpan dengan prefix/versi baru agar riwayat terlihat.

## Rencana berikutnya

- Mural literasi, mural profil pelajar Pancasila, dan tema lain sesuai permintaan sekolah.

## Struktur folder

```
sabiha-arsitek-gambar/
  SKILL.md
  scripts/mural_sapta_pesona.py   (tema hutan alam + fungsi gambar bersama)
  scripts/mural_tema.py           (tema kebun teh, pantai, kereta)
  examples/  (mural-*, kebunteh-*, pantai-*, kereta-*, versi -grid, ringkasan-*)
```
