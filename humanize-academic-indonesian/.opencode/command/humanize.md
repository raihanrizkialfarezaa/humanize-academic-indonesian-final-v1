---
description: Humanize naskah akademik Indonesia — rekonstruksi prosa dari proposisi, bukan sekadar koreksi ejaan.
---

# Perintah

Humanize naskah akademik Indonesia berikut secara end-to-end. **Rekonstruksi prosa dari proposisi dan jangkar konkret** — BUKAN sekadar memperbaiki typo atau mengganti sinonim pada cetakan kalimat asli.

Input pengguna:

$ARGUMENTS

---

# FASE 0 — Muat referensi wajib

Kamu HARUS membaca file-file berikut sebelum menulis satu kalimat pun. Baca setiap file secara penuh menggunakan tool Read. Jangan skip. Jangan ringkas. Jangan mengandalkan ingatan.

**Wajib dibaca (urut):**

1. `SKILL.md` — kontrak induk; ikuti alur 9 langkah di dalamnya.
2. `references/pola-bahasa-ai-indonesia.md` — katalog pola formulaik AI; gunakan untuk diagnosis.
3. `references/ragam-akademik.md` — register formal, fungsi bagian, kekuatan klaim, suara penulis.
4. `references/qa-dan-integritas.md` — hierarki keputusan, audit makna, angka, sitasi.
5. `references/keterbacaan-akademik.md` — kalibrasi pembaca, klasifikasi istilah, eksplisitasi aman.
6. `references/residu-retoris-akademik.md` — deteksi residu retoris, kewajaran S1 TI.
7. `references/contoh-uji-retoris-s1-ti.md` — bank contoh: terlalu formulaik / wajar / terlalu profesional / rusak makna.

**Wajib dibaca jika naskah membahas sistem, arsitektur, kode, basis data, endpoint, pengujian, atau performa:**

8. `references/informatika-akademik.md` — audit teknis Informatika, kontrak pembaca ganda.

**Opsional (baca jika dibutuhkan):**

9. `references/contoh-transformasi.md` — jika pola revisi belum jelas.
10. `references/checker-metriks-retoris.md` — jika diminta audit checker/metrik.
11. `references/pertahanan-parafrase-adversarial.md` + `references/landasan.md` — jika pengguna menyebut detektor AI.

⚠️ **CHECKPOINT**: Jika kamu belum membaca minimal file 1–7, BERHENTI dan baca sekarang. Jangan lanjut ke Fase 1.

---

# FASE 1 — Analisis naskah

Setelah semua referensi dimuat, analisis naskah input:

1. **Identifikasi struktur**: Bab berapa? Bagian apa (pendahuluan, kajian pustaka, metode, hasil, pembahasan, kesimpulan, abstrak, proposal)? Berapa paragraf?
2. **Tentukan pembaca**: Default = akademik lintas bidang. Jika Informatika, gunakan kontrak pembaca ganda (audiens seminar + penguji teknis).
3. **Buat daftar cakupan**: Tandai setiap bagian/paragraf sebagai `belum diproses`. Pastikan tidak ada yang terlewat di akhir.
4. **Kunci elemen terlindungi**: Catat semua angka, satuan, tanggal, sampel, nilai statistik, rumus, parameter, versi, arah perubahan, sitasi, pasangan klaim–sitasi, kutipan langsung, istilah teknis, singkatan, nama metode, endpoint, event, variabel, konfigurasi, tabel, gambar, rujukan silang, kode, daftar pustaka, negasi, syarat, batas klaim. JANGAN mengubah elemen ini.
5. **Pisahkan elemen non-parafrase**: Tabel, rumus, kode, daftar pustaka, kutipan langsung, dan elemen yang tidak boleh diparafrase bebas harus dipertahankan apa adanya.
6. **Klasifikasikan istilah** (ikuti `keterbacaan-akademik.md`):
   - `wajib dipertahankan`: nama resmi metode, konstruk, algoritma, metrik
   - `dipertahankan lalu dijelaskan`: istilah teknis pada kemunculan penting pertama
   - `dapat diberi padanan`: unsur Inggris umum yang punya padanan Indonesia mapan
   - `unsur Inggris yang tidak diperlukan`: kata Inggris non-teknis yang bisa diganti
   - `label/kode`: identifier, nama kolom, endpoint — pertahankan apa adanya
   Dahulukan tujuan, relasi, atau pertanyaan sebelum rangkaian nama metode jika pembaca belum punya orientasi. Bedakan eksplisitasi definisional yang aman dari alasan metodologis, mekanisme, atau asumsi baru yang memerlukan sumber.

---

# FASE 2 — Kunci proposisi (ledger internal)

Untuk setiap paragraf, bangun ledger internal (jangan tampilkan ke pengguna):

- Pelaku/sumber → tindakan → objek → penerima
- Polaritas, modalitas, kekuatan epistemik
- Waktu, urutan, syarat, pengecualian, cakupan
- Angka, satuan, parameter, versi, arah perubahan
- Pasangan klaim–sitasi
- Status: data, interpretasi, pendapat sumber, asumsi, sasaran, atau rekomendasi
- Asal detail teknis: naskah, kode, tabel, sumber, atau belum tersedia

---

# FASE 3 — Diagnosis pola formulaik

Gunakan `pola-bahasa-ai-indonesia.md` dan `residu-retoris-akademik.md` untuk mendiagnosis:

- Gugus formulaik (bukan kata tunggal): rentetan pembuka generik, transisi dekoratif, tumpukan abstraksi sebelum informasi konkret
- Register informal yang lolos: `bisa` → `dapat`, `lewat` → `melalui`, dsb. (lihat tabel §1.1 ragam-akademik.md)
- Simbol khas AI yang lolos: em dash `—`, en dash `–`, smart quotes `""''`, elipsis `…`, bullet `•`, dsb. (lihat tabel §8.5 pola-bahasa-ai-indonesia.md) — ganti dengan padanan konvensional Indonesia
- Klaim tanpa metrik/bukti: `efektif`, `optimal`, `akurat`, `signifikan` tanpa data pendukung
- Penutup optimistis generik, sintesis pustaka semu, simpulan mini berulang
- Struktur kalimat seragam karena cetakan sama (bukan karena fungsi ilmiahnya sama)

Uji keterpindahan: jika paragraf masih masuk akal pada topik lain setelah dua istilah diganti, paragraf itu terlalu generik → konkretkan.

---

# FASE 4 — Rekonstruksi dari fungsi

**INI ADALAH INTI PEKERJAAN. Bukan mengoreksi typo. Bukan mengganti sinonim. Bukan memoles permukaan.**

Untuk setiap paragraf, rekonstruksi dengan cara:

1. **Tentukan pekerjaan paragraf** dalam argumen keseluruhan.
2. **Identifikasi klaim inti** yang harus terbaca paling jelas.
3. **Gunakan jangkar konkret** yang sudah ada: objek, pelaku, mekanisme, kondisi, data, hasil.
4. **Susun kalimat baru** dari proposisi dan hubungan logis yang telah dikunci — bukan dari cetakan kalimat asli.
5. **Pilih subjek berdasarkan fokus informasi**; gunakan aktif/pasif secara fungsional.
6. **Majukan pembeda, mekanisme, kondisi uji, atau hasil** jika sumber sudah menyediakannya.
7. **Gabungkan** kalimat yang memecah satu proposisi; **pecah** kalimat yang memiliki beberapa pusat informasi.
8. **Pangkas** abstraksi kosong, transisi dekoratif, bingkai generik — ganti dengan pelaku, tindakan, objek, bukti.
9. **Ganti register informal** dengan padanan formal (tabel §1.1 ragam-akademik.md).
10. **Akhiri paragraf** pada konsekuensi analitis yang didukung, bukan penutup optimistis.
11. **Pertahankan nama metode**, lalu jelaskan fungsi, objek, atau cara membaca hasilnya secara lokal bila diperlukan pembaca sasaran.
12. **Berikan satu tindakan metodologis** atau satu hubungan konseptual utama per kalimat jika tumpukan istilah membebani pembaca.

**Yang TIDAK boleh dilakukan:**
- Mempertahankan sintaks asli dan hanya mengganti 1-2 kata (ini bukan humanisasi)
- Menambah fakta, contoh, mekanisme, atau sumber yang tidak ada di naskah
- Menaikkan klaim (`berkaitan` → `menyebabkan`, `mengindikasikan` → `membuktikan`)
- Mengubah sasaran proposal menjadi hasil yang sudah tercapai
- Mengganti istilah inti secara bergilir (`sistem` → `platform` → `solusi` → `ekosistem`)
- Menerjemahkan semua istilah asing secara buta
- Mengubah semua pasif menjadi aktif
- Menambah endpoint, versi, nama kolom, event, konfigurasi, atau alasan metode yang tidak ada di sumber
- Memakai istilah terlalu matang (`implikasi epistemik`, `konstruksi analitis`) kecuali sumber menuntut

---

# FASE 4b — Cocokkan suara penulis

Ikuti protokol pencocokan suara dari `ragam-akademik.md` §9:

1. **Jika tersedia sampel sah** dari penulis (sekurang-kurangnya 3 paragraf utuh / ~300 kata dari bagian akademik yang benar-benar ditulis penulis): petakan kecenderungan stabil — cara menjelaskan, memberi batas, memperkenalkan bukti, panjang unit informasi, kadar eksplisit. Terapkan secara selektif tanpa meniru kesalahan.
2. **Jika sampel tidak tersedia**: gunakan suara akademik netral dan pertahankan kecenderungan naskah yang tidak bermasalah. Jangan mengarang ciri personal.

Keluarkan kutipan langsung, daftar pustaka, definisi resmi, dan teks yang diketahui bukan tulisan penulis dari sampel acuan.

---

# FASE 5 — Tiga gerbang penerimaan

Sebelum menyerahkan output, jalankan tiga gerbang ini secara berurutan:

### Gerbang 1: Kesetiaan (harus lulus pertama)
- Setiap klausa revisi dapat ditelusuri ke sumber
- Pelaku, objek, polaritas, modalitas, waktu, syarat, cakupan, atribusi, dan praanggapan tetap setara
- Angka, satuan, rumus, sitasi, kutipan, serta penanda silang tetap melekat pada klaim yang benar
- Detail teknis baru dapat ditelusuri ke bahan pengguna dan tidak muncul hanya untuk membuat teks lebih konkret
- Tidak ada penguatan bukti, kausalitas baru, generalisasi, atau fakta tambahan

### Gerbang 2: Kewajaran retoris
- Klaim utama tidak tertunda oleh bingkai generik
- Tiap paragraf punya pekerjaan jelas dan jangkar konkret
- Tidak ada rantai subjek metadiskursif atau transisi mekanis yang tidak diperlukan
- Pembeda penelitian menyebut sumbu nyata
- Rujukan memiliki anteseden tunggal
- Variasi struktur mengikuti variasi fungsi, bukan pengacakan

### Gerbang 3: Keterbacaan
- Pembaca memperoleh orientasi sebelum tumpukan istilah atau rincian
- Singkatan dan istilah penting diperkenalkan pada kemunculan yang menentukan
- Nama metode memiliki fungsi atau cara membaca yang cukup bagi pembaca sasaran
- Campuran Indonesia–Inggris hanya dipertahankan untuk nama resmi, kode, atau istilah yang lebih tepat
- Penjelasan tambahan dapat ditelusuri dan tidak mengarang alasan, mekanisme, asumsi, atau hasil
- Pakar masih dapat merekonstruksi metode, parameter, syarat, dan batas inferensi

**Resolusi konflik**: Jika gerbang bertentangan, pertahankan kesetiaan. Perbaiki kewajaran dan keterbacaan tanpa membuka ledger fakta; jika itu tidak mungkin, beri catatan.

### Sidang-ready check
Pastikan mahasiswa bisa menjawab pertanyaan berikut dari naskah revisi:
- Apa yang dibuat atau diuji?
- Data, fitur, atau skenario mana yang dibahas?
- Metode, endpoint, atau algoritma apa yang digunakan?
- Hasil mana yang mendukung klaim?
- Apa batas penelitian?

Jika info tidak tersedia, jangan mengarang. Beri catatan `[PERLU VERIFIKASI: ...]`.

### Audit format dan cakupan
- Pastikan seluruh bagian dalam daftar cakupan telah berstatus `diproses`.
- Pertahankan Markdown, LaTeX, nomor persamaan, tabel, daftar, catatan kaki, sitasi, dan rujukan silang.
- Jangan memindahkan teks melewati tabel, gambar, atau batas bagian jika hubungan rujukannya dapat berubah.

### Validator (opsional)
Jika tersedia naskah asli dan revisi dalam file teks, jalankan validator sebagai alarm:
```
python scripts/validate_rewrite.py original.txt revised.txt --audience lintas-bidang --domain informatika --voice impersonal --strict
```
Hasil validator adalah alarm, bukan bukti kesetaraan semantik lengkap. Jangan jalankan jika file tidak tersedia.

---

# FASE 6 — Output

## Untuk naskah panjang (lebih dari ~10 paragraf)

Proses per bagian/bab. Untuk setiap bagian:

1. Tampilkan judul bagian yang diproses.
2. Tampilkan naskah revisi lengkap untuk bagian itu.
3. Setelah semua bagian selesai, berikan catatan perubahan dan risiko di akhir.

## Untuk naskah pendek

Keluarkan naskah revisi lengkap. Tambahkan catatan singkat setelah naskah **hanya jika** ada bagian yang perlu diverifikasi, konflik sumber, perubahan struktural penting, atau batas format:

```
[Naskah revisi lengkap]

Catatan (jika ada):
- ...
```

Jangan menampilkan draf perantara, daftar "ciri AI", skor kealamian, atau ledger internal.

## Jika pengguna meminta audit/review (bukan revisi)

```
Status: ...
Temuan utama: ...
Risiko makna/teknis: ...
Risiko retoris: ...
Kewajaran S1 TI: ...
Saran: ...
Contoh revisi: ...
```

---

# GUARD — Self-check sebelum output

Sebelum mengirim output, jawab pertanyaan ini secara internal:

1. **Apakah prosa benar-benar direkonstruksi dari proposisi, atau hanya typo yang diperbaiki?** Jika hanya typo → GAGAL. Ulangi Fase 4.
2. **Apakah semua paragraf sudah berstatus `diproses`?** Jika ada yang terlewat → proses sekarang.
3. **Apakah ada kata ragam percakapan (`bisa`, `lewat`, `kayak`, `bikin`, `nggak`, `cuma`, `soalnya`, dll.) yang lolos?** Jika ya → ganti padanan formal.
4. **Apakah ada simbol khas AI (`—`, `–`, `…`, `""''`, `•`, `→`) yang lolos?** Jika ya → ganti padanan konvensional Indonesia.
5. **Apakah ada klaim evaluatif tanpa metrik/bukti?** Jika ya → turunkan.
6. **Apakah ada elemen terlindungi yang berubah?** Jika ya → kembalikan.

Jika semua jawaban aman, kirim output.

---

# Prinsip

- Lebih baik rekonstruksi setia daripada poles permukaan yang mengubah makna.
- Kealamian akademik berasal dari kepadatan informasi dan keputusan retoris, bukan dari sinonim acak atau kalimat pendek.
- Target: wajar untuk skripsi S1 TI, jelas bagi dosen penguji, tidak berlebihan, tetap akademik, tetap teknis, dapat dipertanggungjawabkan.
