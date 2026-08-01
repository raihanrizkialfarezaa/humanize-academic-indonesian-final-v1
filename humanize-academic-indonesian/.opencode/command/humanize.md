---
description: Humanize end-to-end naskah akademik Indonesia untuk skripsi S1 Teknik Informatika dengan audit makna, teknis, retoris, dan sidang-ready.
---

Jalankan proses humanize akademik Indonesia end-to-end untuk input pengguna berikut.

Input pengguna:

$ARGUMENTS

## Tujuan

Hasil akhir harus menjadi naskah akademik Indonesia yang:

- formal;
- jelas;
- wajar untuk mahasiswa S1 Teknik Informatika;
- tidak terlalu formulaik;
- tidak terlalu profesional atau over-polished;
- teknisnya tetap terlacak;
- siap dipertanggungjawabkan saat sidang;
- tidak mengubah makna, angka, sitasi, istilah teknis, atau batas klaim.

## Deteksi Mode Otomatis

Tentukan mode dari input pengguna:

- Jika pengguna meminta `audit`, `review`, `cek`, `analisis`, `nilai`, `status`, atau `sudah natural belum`, lakukan audit lengkap.
- Jika pengguna meminta `revisi`, `rewrite`, `parafrase`, `humanize`, `rapikan`, `buat lebih natural`, atau memberi teks tanpa instruksi jelas, lakukan audit singkat lalu revisi.
- Jika pengguna meminta `checker`, `rule`, `metrik`, `PASS`, `REVIEW`, atau `FAIL`, gunakan mode checker.
- Jika pengguna meminta `sidang`, `dosen penguji`, `skripsi`, atau `S1 TI`, aktifkan mode sidang-ready.
- Jika input ambigu, lakukan mode default: audit singkat, revisi aman, dan catatan risiko.

## Pemakaian Seluruh Aset Project

Gunakan aset project secara adaptif, bukan membaca semua file secara membabi buta. Setiap aset memiliki fungsi berikut:

| Aset | Fungsi |
| :--- | :--- |
| `SKILL.md` | kontrak induk humanisasi akademik, alur wajib, integritas, validator, bentuk keluaran |
| `references/qa-dan-integritas.md` | gerbang kesetiaan makna, audit angka/sitasi, delta makna, detektor AI, sidang-ready |
| `references/ragam-akademik.md` | ragam akademik per bagian, klaim, aktif/pasif, posisi studi terdahulu, suara penulis |
| `references/keterbacaan-akademik.md` | kalibrasi pembaca, beban istilah, eksplisitasi aman, keterbacaan teknis |
| `references/informatika-akademik.md` | sistem, arsitektur, basis data, endpoint, event, metrik, performa, detail teknis Informatika |
| `references/pola-bahasa-ai-indonesia.md` | diagnosis pola formulaik, transisi mekanis, interferensi Inggris, positif palsu |
| `references/residu-retoris-akademik.md` | audit residu retoris, S1 TI naturalness, over-polish guard |
| `references/checker-metriks-retoris.md` | rule checker, status `PASS/INFO/REVIEW/FAIL`, S1TI rules, technical guard |
| `references/contoh-uji-retoris-s1-ti.md` | bank contoh terlalu formulaik, wajar S1 TI, terlalu profesional, rusak makna |
| `references/contoh-transformasi.md` | contoh transformasi berbasis ledger fakta lintasbidang |
| `references/pertahanan-parafrase-adversarial.md` | guard saat pengguna menyebut detektor AI, humanizer, skor, atau pengelabuan |
| `references/landasan.md` | landasan EYD/KBBI, riset deteksi AI, kebijakan integritas, keterbatasan vendor |
| `scripts/validate_rewrite.py` | validator deterministik jika tersedia pasangan naskah asli dan revisi |
| `scripts/test_validate_rewrite.py` | regression awareness saat mengembangkan atau mengecek validator |
| `agents/openai.yaml` | metadata packaging/agent, bukan sumber bahasa harian |
| `assets/icon.svg` | ikon packaging/UI, bukan sumber analisis naskah |

## Referensi Baseline

Untuk tugas humanize umum, gunakan baseline berikut:

- `SKILL.md`
- `references/qa-dan-integritas.md`
- `references/ragam-akademik.md`
- `references/keterbacaan-akademik.md`
- `references/pola-bahasa-ai-indonesia.md`
- `references/residu-retoris-akademik.md`
- `references/checker-metriks-retoris.md`
- `references/contoh-uji-retoris-s1-ti.md`

Gunakan referensi kondisional berikut sesuai pemicu:

- `references/informatika-akademik.md` jika ada sistem, aplikasi, arsitektur, basis data, kode, endpoint, event, algoritma, pengujian, atau performa.
- `references/contoh-transformasi.md` jika pola revisi belum jelas atau butuh pembanding lintas kasus.
- `references/pertahanan-parafrase-adversarial.md` dan `references/landasan.md` jika pengguna menyebut Turnitin, AI detector, skor, humanizer, atau pengelabuan.
- `scripts/validate_rewrite.py` jika ada pasangan naskah asli dan revisi dalam file teks.
- `scripts/test_validate_rewrite.py` hanya untuk konteks pengembangan validator.
- `agents/openai.yaml` dan `assets/icon.svg` hanya untuk konteks packaging/integrasi.

## Pipeline End-to-End

Ikuti urutan ini:

1. Identifikasi jenis teks: Bab 1, Bab 2, Bab 3, Bab 4, Bab 5, abstrak, metode, hasil, pembahasan, kajian pustaka, proposal, laporan, atau paragraf umum.
2. Tentukan pembaca: pakar, pembaca disiplin, akademik lintas bidang, atau umum. Default untuk skripsi S1 TI adalah akademik lintas bidang dengan kontrak pembaca ganda Informatika.
3. Catat elemen terlindungi:
   - angka;
   - satuan;
   - sitasi;
   - istilah teknis;
   - nama metode;
   - nama algoritma;
   - endpoint;
   - event;
   - variabel;
   - label;
   - konfigurasi;
   - negasi;
   - syarat;
   - batas klaim.
4. Audit kesetiaan makna dengan `references/qa-dan-integritas.md`.
5. Audit identitas teknis Informatika dengan `references/informatika-akademik.md` jika relevan.
6. Audit ragam akademik dan fungsi bagian dengan `references/ragam-akademik.md`.
7. Audit keterbacaan dengan `references/keterbacaan-akademik.md`.
8. Audit pola formulaik dengan `references/pola-bahasa-ai-indonesia.md`.
9. Audit residu retoris dengan `references/residu-retoris-akademik.md`.
10. Jika diminta checker/metrik, terapkan `references/checker-metriks-retoris.md`.
11. Cocokkan hasil dengan `references/contoh-uji-retoris-s1-ti.md` agar tidak terlalu formulaik, terlalu profesional, atau rusak makna.
12. Gunakan `references/contoh-transformasi.md` jika perlu contoh pembanding berbasis ledger fakta.
13. Jika user membahas detektor AI, gunakan `references/pertahanan-parafrase-adversarial.md` dan `references/landasan.md`; jangan menjanjikan skor atau label manusia.
14. Jika tersedia original dan revisi dalam file teks, gunakan validator sebagai alarm, bukan bukti final.
15. Jalankan sidang-ready check sebelum memberi output.

## Prioritas Mutlak

1. Jangan mengubah makna.
2. Jangan mengubah angka, satuan, sitasi, atau data.
3. Jangan mengubah istilah teknis, nama metode, endpoint, event, variabel, label, atau konfigurasi.
4. Jangan menambah detail teknis yang tidak tersedia.
5. Jangan menaikkan klaim.
6. Jangan mengubah rencana/proposal menjadi hasil.
7. Jangan menjanjikan lolos detektor AI.
8. Jangan menyatakan teks pasti manusia atau pasti AI.
9. Jangan menambahkan kesalahan buatan agar terlihat manusiawi.
10. Jangan membuat teks terlalu profesional untuk skripsi S1 TI.

## Kalibrasi S1 Teknik Informatika

Pertahankan jika wajar dan tidak berlebihan:

- `penelitian ini`;
- `sistem ini`;
- `aplikasi ini`;
- `pengujian dilakukan`;
- `hasil pengujian menunjukkan`;
- `sistem dirancang`;
- `data dikumpulkan`;
- istilah inti seperti `sistem`, `aplikasi`, `data`, `fitur`, `pengujian`, `hasil`, `pengguna`, `admin`, `petugas`.

Jangan mengganti istilah inti secara bergilir hanya untuk variasi.

Contoh yang harus dihindari:

- `sistem` -> `platform` -> `solusi` -> `ekosistem`;
- `pengujian` -> `evaluasi` -> `validasi` -> `asesmen`;
- `hasil pengujian` -> `temuan empiris` jika sumbernya sederhana.

## Klaim yang Harus Dijaga

Tinjau klaim berikut:

- `efektif`;
- `efisien`;
- `optimal`;
- `akurat`;
- `andal`;
- `aman`;
- `signifikan`;
- `lebih cepat`;
- `berhasil`;
- `sesuai harapan`.

Klaim tersebut harus punya metrik, skenario, tabel, data, pembanding, atau batas. Jika tidak ada, turunkan menjadi bentuk yang lebih aman.

## Status Checker

Gunakan status berikut jika mode audit/checker:

- `PASS`: aman.
- `INFO`: pola muncul tetapi wajar.
- `REVIEW`: perlu ditinjau atau direvisi.
- `FAIL`: merusak makna, istilah, bukti, atau klaim.

## Validator sebagai Alarm

Jika tersedia naskah asli dan revisi sebagai file teks, rencanakan atau jalankan validator sesuai konteks. Untuk skripsi Informatika dengan gaya impersonal, bentuk perintahnya:

```text
python scripts/validate_rewrite.py original.txt revised.txt --audience lintas-bidang --domain informatika --voice impersonal --strict
```

Jangan menjalankan validator jika pengguna hanya memberi satu teks, jika file tidak tersedia, atau jika perintah akan menulis/mengubah file. Hasil validator adalah alarm; `PASS` tidak membuktikan kesetaraan semantik lengkap.

## Output Default

Jika pengguna memberi teks dan meminta humanize/revisi, keluarkan:

```text
Versi revisi:
...

Catatan perubahan:
- ...

Risiko/verifikasi:
- ...
```

Jika tidak ada risiko/verifikasi, tulis `Tidak ada catatan verifikasi penting.`

## Output Audit

Jika pengguna meminta audit/review, keluarkan:

```text
Status:
...

Temuan utama:
- ...

Risiko makna/teknis:
- ...

Risiko retoris:
- ...

Kewajaran S1 TI:
- ...

Saran:
- ...

Contoh revisi:
...
```

## Output Checker

Jika pengguna meminta checker/metrik/rule, keluarkan:

```text
Rule:
Status:
Evidence:
Rationale:
Suggested action:
Protected terms:
```

## Output Validasi Original vs Revisi

Jika pengguna memberi original dan revisi, keluarkan:

```text
Status validasi:
Fidelity:
Style:
Accessibility:
Temuan kritis:
Tindakan lanjutan:
```

## Sidang-Ready Check

Sebelum final, pastikan jawaban tidak membuat penulis kesulitan menjawab:

- Apa yang dibuat atau diuji?
- Data, fitur, atau skenario mana yang dibahas?
- Metode, diagram, framework, endpoint, atau algoritma apa yang digunakan?
- Hasil mana yang mendukung klaim?
- Apakah klaim evaluatif punya metrik atau skenario?
- Apa batas penelitian?
- Apa pembeda dari penelitian terdahulu?
- Apakah istilah teknis masih bisa ditelusuri?

Jika ada informasi yang tidak tersedia, jangan mengarang. Beri catatan `[PERLU VERIFIKASI: ...]` jika perlu.

## Larangan Revisi

Jangan:

- menerjemahkan semua istilah asing secara buta;
- mengubah semua pasif menjadi aktif;
- menghapus semua frasa skripsi yang wajar;
- menambah endpoint, versi, nama kolom, event, konfigurasi, alasan metode, atau mekanisme;
- memakai istilah terlalu matang seperti `implikasi epistemik`, `konstruksi analitis`, atau `validitas eksternal` kecuali sumber menuntutnya;
- mengubah `uji Friedman` menjadi `uji statistik`;
- mengubah `latensi p95` menjadi `kecepatan sistem`;
- mengubah `wawancara semi-terstruktur` menjadi `wawancara`;
- menghapus hasil nol, negasi, syarat, atau pengecualian.

## Prinsip Final

Lebih baik revisi minimal tetapi setia daripada revisi indah yang mengubah makna.

Target akhir adalah teks yang:

- wajar untuk skripsi S1 Teknik Informatika;
- jelas bagi dosen penguji;
- tidak berlebihan;
- tetap akademik;
- tetap teknis;
- dan dapat dipertanggungjawabkan.
