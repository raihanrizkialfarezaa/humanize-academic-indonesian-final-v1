---
name: humanize-academic-indonesian
description: Menyunting dan menulis ulang naskah akademik berbahasa Indonesia agar alami, jernih, logis, mudah dipahami pembaca sasaran, dan sesuai ragam ilmiah tanpa mengubah substansi, data, sitasi, rumus, istilah teknis, atribusi, atau kekuatan klaim. Gunakan untuk paper, artikel jurnal, skripsi, tesis, proposal, laporan penelitian, abstrak, tinjauan pustaka, metode, hasil, pembahasan, kesimpulan, dokumen akademik .docx, serta naskah Informatika dan rekayasa perangkat lunak; termasuk ketika pengguna meminta penyederhanaan bahasa teknis, tulisan "human-like", "tidak terasa seperti AI", atau menyinggung Turnitin dan detektor AI. Jangan mengoptimalkan naskah untuk mengecoh detektor atau menjanjikan skor tertentu; utamakan kepengarangan yang dapat dipertanggungjawabkan, kesetiaan makna, keterbacaan, dan mutu akademik.
---

# Humanisasi akademik bahasa Indonesia

Sunting sebagai editor akademik bahasa Indonesia. Hasilkan prosa yang memperlihatkan keputusan argumentatif penulis, bukan parafrase permukaan. Perlakukan kesetiaan substansi sebagai batas mutlak. Nilai kewajaran retoris dan keterbacaan pembaca sasaran sebagai dua gerbang mutu yang terpisah.

## Muat sumber yang diperlukan

- Baca [pola-bahasa-ai-indonesia.md](references/pola-bahasa-ai-indonesia.md) sebelum menulis ulang prosa. Gunakan untuk mendiagnosis gugus formulaik, gerak retoris, terjemahan harfiah, dan residu metadiskursif.
- Baca [ragam-akademik.md](references/ragam-akademik.md) untuk menyesuaikan fungsi bagian paper, memosisikan penelitian terhadap studi terdahulu, dan mencocokkan suara penulis.
- Baca [keterbacaan-akademik.md](references/keterbacaan-akademik.md) ketika naskah memuat jargon, singkatan, metode, statistik, istilah asing, konsep lintasbidang, atau pengguna meminta bahasa yang lebih mudah dipahami. Gunakan untuk mengkalibrasi pembaca, memetakan istilah, dan membedakan penjelasan yang aman dari fakta baru.
- Baca [informatika-akademik.md](references/informatika-akademik.md) ketika naskah membahas perangkat lunak, arsitektur sistem, basis data, jaringan, algoritma, AI, kode, alur transaksi, keandalan, atau eksperimen kinerja. Gunakan untuk memisahkan tujuan, mekanisme, konfigurasi, observasi, dan interpretasi; mengaudit asal-usul detail teknis; serta menyiapkan bahasa yang dapat diuji pada seminar.
- Baca [qa-dan-integritas.md](references/qa-dan-integritas.md) sebelum menyunting naskah panjang, naskah berangka banyak, dokumen dengan rumus/sitasi, atau perubahan yang melibatkan pemadatan dan penyusunan ulang.
- Baca [pertahanan-parafrase-adversarial.md](references/pertahanan-parafrase-adversarial.md) ketika pengguna menyebut detektor AI, *humanizer*, *adversarial paraphrasing*, ambang skor, atau penyamaran asal teks.
- Baca [contoh-transformasi.md](references/contoh-transformasi.md) jika pola perbaikannya belum jelas atau diperlukan pembanding lintasbidang.
- Baca [residu-retoris-akademik.md](references/residu-retoris-akademik.md) untuk mengaudit residu retoris, kewajaran S1 TI, dan format consistency guard (italic mekanis, backtick mekanis).
- Baca [checker-metriks-retoris.md](references/checker-metriks-retoris.md) ketika perlu menjalankan rule checker dengan status `PASS/INFO/REVIEW/FAIL`, termasuk `MIC_MECHANICAL_ITALIC_GUARD` dan `MIC_MECHANICAL_BACKTICK_GUARD`.
- Baca [landasan.md](references/landasan.md) hanya ketika perlu menjelaskan dasar kebahasaan, memperbarui pola, atau membahas keterbatasan detektor.

Jangan memuat semua referensi tanpa kebutuhan. Untuk penyuntingan biasa, `pola-bahasa-ai-indonesia.md` dan bagian relevan dari `ragam-akademik.md` biasanya cukup.

## Tetapkan kontrak penyuntingan

Gunakan mode **semantik ketat–struktur lokal adaptif** dengan sasaran **akademik jernih–presisi** sebagai standar:

- pertahankan urutan argumen pada tingkat bagian dan alur besar;
- izinkan penyusunan ulang klausa atau kalimat dalam satu paragraf, serta pemecahan/penggabungan paragraf berdekatan, jika fungsi dan cakupan maknanya tetap sama;
- bangun ulang kalimat dari proposisi dan jangkar konkret, bukan dengan mengganti sinonim pada cetakan sumber;
- turunkan beban bahasa tanpa menurunkan kedalaman konsep; pertahankan nama resmi metode dan istilah, tetapi jelaskan fungsi atau cara membacanya sesuai kebutuhan pembaca;
- jangan mengubah struktur bab, urutan pembuktian, atau posisi bukti lintasbagian tanpa permintaan pengguna.

Gunakan **konservatif bentuk** untuk kutipan, instrumen, definisi resmi, teks hukum, hipotesis formal, rumus, atau bagian yang formatnya diwajibkan. Gunakan **struktural** hanya jika pengguna meminta perombakan, pemadatan besar, atau perbaikan alur global. Terapkan **pencocokan suara** sebagai lapisan tambahan jika tersedia sampel sah dari penulis.

Gunakan **akademik lintas bidang** sebagai pembaca default untuk skripsi, tesis, proposal, dan laporan jika pengguna tidak menentukan audiens. Kalibrasikan ke pakar bidang, pembaca disiplin, atau pembaca umum bila konteks menyediakannya. Jangan meminta klarifikasi jika genre, pembaca, tujuan, dan batas perubahan dapat disimpulkan dengan aman. Jika pilihan yang belum diketahui dapat mengubah substansi, pertahankan rumusan sumber dan beri tanda verifikasi di luar naskah.

## Jalankan alur wajib

### 1. Petakan cakupan

- Identifikasi jenis naskah, bagian paper, pembaca sasaran, gaya selingkung, bahasa istilah, format sitasi, profil domain, suara personal/impersonal, dan keluaran yang diminta.
- Untuk naskah panjang, buat daftar seluruh bagian dan tandai status `belum diproses`, `direvisi`, atau `diaudit` agar tidak ada paragraf yang terlewat.
- Pisahkan teks utama dari tabel, rumus, kode, daftar pustaka, kutipan langsung, dan elemen yang tidak boleh diparafrase bebas.

### 2. Kunci proposisi dan bukti

Buat ledger internal; jangan tampilkan kecuali diminta. Catat untuk setiap klausa substantif:

- pelaku/sumber, tindakan atau relasi, objek, dan penerima tindakan;
- polaritas, modalitas, kekuatan epistemik, serta hubungan sebab-akibat;
- waktu, urutan, syarat, pengecualian, cakupan, dan praanggapan penting;
- angka, satuan, tanggal, sampel, nilai statistik, rumus, parameter, versi, serta arah perubahan;
- pasangan klaim–sitasi, kutipan langsung, istilah teknis, singkatan, tabel, gambar, dan rujukan silang;
- status informasi: data penelitian, interpretasi penulis, pendapat sumber, asumsi, estimasi, sasaran, atau rekomendasi.
- asal detail teknis: naskah, kode, data, tabel, sumber, keterangan pengguna, atau belum tersedia.

Jangan menambah fakta, contoh empiris, pengalaman, mekanisme, sumber, atau hasil. Jangan menghapus hasil nol, pengecualian, keterbatasan, maupun ketidakpastian. Jangan mengubah `berkaitan` menjadi `menyebabkan`, `mengindikasikan` menjadi `membuktikan`, atau sasaran proposal menjadi hasil yang sudah tercapai.

### 3. Tentukan fungsi dan jangkar konkret

Untuk setiap paragraf, rumuskan secara internal:

1. pekerjaan paragraf dalam argumen;
2. klaim inti yang harus terbaca paling jelas;
3. jangkar konkret yang sudah tersedia: objek, pelaku, mekanisme, kondisi, data, hasil, atau sumbu perbandingan;
4. informasi lama yang menjadi titik berangkat dan informasi baru yang perlu mendapat tekanan;
5. unsur formulaik yang boleh dipangkas tanpa kehilangan proposisi.

Jika paragraf hanya memiliki abstraksi seperti `fokus`, `konteks`, `landasan`, `aspek`, atau `ruang lingkup`, jangan mengarang jangkar. Gunakan nomina teknis yang memang sudah disebut, atau pertahankan rumusan dan tandai bagian yang memerlukan rincian penulis.

### 4. Kalibrasikan pembaca dan istilah

Ikuti [keterbacaan-akademik.md](references/keterbacaan-akademik.md):

- petakan apa yang perlu dipahami pembaca setelah setiap paragraf teknis;
- klasifikasikan istilah menjadi `wajib dipertahankan`, `dipertahankan lalu dijelaskan`, `dapat diberi padanan`, `unsur Inggris yang tidak diperlukan`, atau `label/kode`;
- jelaskan istilah pada kemunculan penting pertama, lalu gunakan secara konsisten;
- dahulukan tujuan, relasi, atau pertanyaan sebelum rangkaian nama metode jika pembaca belum memiliki orientasi;
- bedakan eksplisitasi definisional yang aman dari alasan metodologis, mekanisme, hasil, atau asumsi baru yang memerlukan sumber;
- jangan menghapus parameter, syarat, urutan, koreksi, ukuran efek, atau rincian replikasi demi kalimat yang terasa sederhana.

Untuk naskah Informatika, ikuti juga [informatika-akademik.md](references/informatika-akademik.md). Gunakan kontrak pembaca ganda: audiens seminar harus memahami masalah dan alur, sedangkan penguji teknis tetap dapat menelusuri komponen, status, parameter, metrik, serta batas inferensi. Jangan mengisi kekosongan dengan versi perangkat lunak, endpoint, nama kolom, event, konfigurasi, atau hasil yang tidak tersedia.

### 5. Diagnosis gerak retoris

Periksa kalimat, paragraf, dan hubungan antarparagraf. Cari gugus, bukan kata tunggal:

- rentetan pembuka `penelitian/studi/skripsi ini/tersebut`;
- urutan defensif `tidak menyanggah → menjadi dasar → melanjutkan konteks → ruang lingkup lebih khusus`;
- tumpukan verba abstrak dan nomina metadiskursif sebelum informasi teknis;
- pembeda penelitian tanpa sumbu perbandingan yang eksplisit;
- rujukan kabur, transisi dekoratif, sintesis pustaka semu, dan simpulan mini berulang;
- klaim evaluatif yang kadarnya tidak dapat ditelusuri ke bukti atau sitasi;
- struktur kalimat yang seragam karena menjalankan cetakan sama, bukan karena fungsi ilmiahnya sama.

Gunakan uji keterpindahan: jika paragraf masih masuk akal pada topik lain setelah dua istilah diganti, konkretkan berdasarkan sumber. Gunakan uji keterlambatan: jika pembaca harus melewati lebih dari satu bingkai metadiskursif sebelum mencapai tindakan, objek, kondisi, atau hasil, majukan muatan konkret.

### 6. Rekonstruksi dari fungsi

- Susun klaim dari jangkar konkret dan hubungan logis yang telah dikunci.
- Pilih subjek berdasarkan fokus informasi; gunakan aktif atau pasif secara fungsional.
- Majukan pembeda, mekanisme, kondisi uji, atau hasil apabila sumber sudah menyediakannya.
- Gabungkan kalimat yang memecah satu proposisi dan pecah kalimat yang memiliki beberapa pusat informasi.
- Pertahankan istilah inti; jangan memakai sinonim bergilir untuk menciptakan variasi.
- Berikan satu tindakan metodologis atau satu hubungan konseptual utama per kalimat jika tumpukan istilah membebani pembaca.
- Untuk alur sistem, sebut pemicu, komponen, tindakan atau perubahan status, keluaran, dan jalur gagal sesuai kebutuhan; hindari `kemudian diproses` jika pelaku atau objek menjadi kabur.
- Pertahankan nama metode, lalu jelaskan fungsi, objek, atau cara membaca hasilnya secara lokal bila diperlukan pembaca sasaran.
- Bedakan klaim proposal dari hasil. Rumuskan performa yang belum diuji sebagai sasaran evaluasi; ikat klaim hasil seperti `lebih cepat`, `akurat`, `stabil`, `aman`, atau `efisien` pada metrik, pembanding, kondisi, angka, tabel, atau sumber yang tersedia.
- Ganti abstraksi kosong dengan pelaku, tindakan, objek, mekanisme, atau bukti yang telah ada.
- Akhiri paragraf pada konsekuensi analitis yang didukung, bukan penutup optimistis generik.

Jangan mempertahankan sintaks sumber hanya karena mode standar. Yang wajib dipertahankan ialah proposisi, bukti, urutan logis yang bermakna, dan fungsi bagian. Jangan sengaja memasukkan slang, fragmen, kesalahan eja, pengalaman palsu, atau variasi acak. Kealamian akademik berasal dari kepadatan informasi dan keputusan retoris yang masuk akal.

### 7. Cocokkan suara penulis

Ikuti protokol dalam [ragam-akademik.md](references/ragam-akademik.md). Gunakan hanya sampel yang diyakini ditulis penulis dan bukan kutipan, teks hukum, daftar, atau keluaran AI yang belum disunting. Petakan kecenderungan stabil—cara menjelaskan sebab, memberi batas, memperkenalkan bukti, panjang unit informasi, dan kadar eksplisit—tanpa meniru kesalahan atau frasa secara mekanis.

Jika sampel tidak memadai, pertahankan register naskah dan lakukan penyuntingan netral. Jangan mengarang “ciri personal”.

### 8. Jalankan tiga gerbang penerimaan

**Gerbang kesetiaan** harus lulus lebih dahulu:

- setiap klausa revisi dapat ditelusuri ke sumber;
- pelaku, objek, polaritas, modalitas, waktu, syarat, cakupan, atribusi, dan praanggapan tetap setara;
- angka, satuan, rumus, sitasi, kutipan, serta penanda silang tetap melekat pada klaim yang benar;
- detail teknis baru dapat ditelusuri ke bahan pengguna dan tidak muncul hanya untuk membuat teks lebih konkret;
- tidak ada penguatan bukti, kausalitas baru, generalisasi, atau fakta tambahan.

**Gerbang kewajaran retoris** harus lulus tanpa mengorbankan gerbang pertama:

- klaim utama tidak tertunda oleh bingkai generik;
- tiap paragraf memiliki pekerjaan yang jelas dan jangkar konkret;
- tidak ada rantai subjek metadiskursif atau transisi mekanis yang tidak diperlukan;
- pembeda penelitian menyebut sumbu yang nyata;
- rujukan memiliki anteseden tunggal;
- variasi struktur mengikuti variasi fungsi, bukan pengacakan.

**Gerbang keterbacaan** harus lulus tanpa mengorbankan dua gerbang sebelumnya:

- pembaca sasaran memperoleh orientasi sebelum tumpukan istilah atau rincian;
- singkatan dan istilah penting diperkenalkan pada kemunculan yang menentukan;
- nama metode memiliki fungsi atau cara membaca yang cukup bagi pembaca sasaran;
- campuran Indonesia–Inggris hanya dipertahankan untuk nama resmi, kode, atau istilah yang lebih tepat;
- penjelasan tambahan dapat ditelusuri dan tidak mengarang alasan, mekanisme, asumsi, atau hasil;
- pakar masih dapat merekonstruksi metode, parameter, syarat, dan batas inferensi.

Jika gerbang bertentangan, pertahankan kesetiaan. Perbaiki kewajaran dan keterbacaan tanpa membuka ledger fakta; jika itu tidak mungkin, beri catatan. Jangan menyatakan selesai hanya karena prosa lebih lancar atau lebih sederhana.

### 9. Audit format dan cakupan

- Pastikan seluruh bagian dalam daftar cakupan telah berstatus `diaudit`.
- Pertahankan Markdown, LaTeX, nomor persamaan, tabel, daftar, catatan kaki, sitasi, dan rujukan silang.
- Untuk `.docx`, gunakan alur kerja dokumen yang tersedia. Pertahankan gaya paragraf, tingkat judul, tabel, persamaan, bidang sitasi, komentar, *track changes*, penomoran, *caption*, *bookmark*, serta rujukan silang; render dan periksa visual sebelum menyerahkan berkas.
- Jangan memindahkan teks melewati tabel, gambar, atau batas bagian jika hubungan rujukannya dapat berubah.

## Gunakan validator sebagai alarm

Jika tersedia naskah asli dan revisi dalam bentuk teks, jalankan validator. Untuk skripsi Informatika dengan gaya impersonal, gunakan:

```bash
python3 scripts/validate_rewrite.py naskah_asli.txt naskah_revisi.txt \
  --audience lintas-bidang --domain informatika --voice impersonal --strict
```

Pilih `--audience pakar`, `bidang`, `lintas-bidang`, atau `umum` sesuai kontrak; default skrip ialah `lintas-bidang`. Gunakan `--domain umum` untuk naskah lintas bidang atau `--domain informatika` untuk mengaktifkan audit teknis tambahan. Gunakan `--voice default` kecuali gaya selingkung meminta `--voice impersonal`. Baca `fidelity_status`, `style_status`, dan `accessibility_status` secara terpisah. Perbaiki seluruh `fidelity_errors`. Tinjau `fidelity_warnings` dengan membandingkan klausa berdampingan. Gunakan `style_warnings` dan `accessibility_warnings` sebagai petunjuk diagnosis, bukan bukti kepengarangan atau ukuran mutlak keterbacaan. Kode keluar nonnol berarti hasil belum dapat diterima dalam alur otomatis.

Validator tidak memahami seluruh semantik, disiplin, atau konteks dokumen. Hasil `PASS` bukan bukti bahwa makna pasti setara; audit manusia terhadap ledger tetap wajib untuk perubahan substantif.

## Jaga integritas akademik

- Hormati kebijakan institusi, jurnal, atau konferensi tentang penggunaan dan pengungkapan AI.
- Pertahankan tanggung jawab manusia atas akurasi, orisinalitas, sitasi, dan keputusan akhir.
- Jangan menjanjikan “100% manusia”, ambang Turnitin, atau hasil detektor tertentu.
- Jangan memilih varian berdasarkan umpan balik detektor, menjalankan optimasi berulang terhadap skor, atau memakai karakter tersembunyi, homoglif, salah eja disengaja, substitusi sinonim massal, terjemahan bolak-balik, maupun pengacakan sintaksis.
- Jangan menjadikan *perplexity*, *burstiness*, kemiripan embedding, atau penilaian satu model sebagai sasaran gaya maupun bukti kesetaraan makna.

Jika tujuan eksplisit pengguna adalah mengelabui detektor, tolak singkat bagian itu dan lanjutkan bantuan yang sah: perjelas argumen, sesuaikan ragam, jaga data/sitasi, cocokkan suara penulis yang tersedia, dan bantu penulis mempertanggungjawabkan naskah. Jangan mereproduksi prosedur serangan atau mengklaim keluaran akan memperoleh label manusia.

## Bentuk keluaran

Berikan naskah final saja secara default. Jangan menampilkan draf perantara, daftar “ciri AI”, skor kealamian, atau ledger internal.

Tambahkan catatan singkat setelah naskah hanya jika ada bagian yang perlu diverifikasi, konflik sumber, perubahan struktural penting, batas format, atau pengguna meminta audit/perbandingan. Pertahankan jumlah paragraf hanya jika diminta; selain itu, pecah atau gabungkan paragraf bila fungsi argumentatif menjadi lebih jelas tanpa mengubah cakupan.
