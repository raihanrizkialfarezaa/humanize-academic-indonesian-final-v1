# Jaminan mutu dan integritas penyuntingan

## Daftar isi

1. Hierarki keputusan
2. Audit sebelum revisi
3. Audit sesudah revisi
4. Pemeriksaan khusus angka dan sitasi
5. Penanganan konflik
6. Detektor AI dan bukti kepengarangan
7. Audit delta makna
8. Gerbang kewajaran retoris
9. Gerbang keterbacaan
10. Audit cakupan dan dokumen panjang
11. Membaca hasil validator
12. Uji red-team defensif

## 1. Hierarki keputusan

Jika dua tujuan bertentangan, gunakan urutan berikut:

1. kebenaran dan kesetiaan substansi;
2. data, rumus, kutipan, dan hubungan klaim-sumber;
3. kekuatan epistemik dan batas generalisasi;
4. istilah teknis serta definisi operasional;
5. gaya selingkung dan instruksi pengguna;
6. keterbacaan bagi pembaca sasaran;
7. struktur argumentasi;
8. kaidah bahasa Indonesia;
9. kelancaran dan pemadatan;
10. preferensi gaya.

Jangan mengorbankan tingkat yang lebih tinggi demi kalimat yang tampak lebih alami.

## 2. Audit sebelum revisi

Buat matriks internal sederhana:

| Elemen | Yang dicatat |
| --- | --- |
| klaim | proposisi dan tingkat kepastian |
| bukti | data, sitasi, tabel, gambar, atau rumus pendukung |
| istilah | bentuk resmi, fungsi, padanan, singkatan, dan status label/kode |
| batas | populasi, periode, kondisi, asumsi, dan pengecualian |
| fungsi | peran paragraf dalam argumen |
| pembaca | pengetahuan yang dapat diasumsikan dan istilah yang perlu dijelaskan |
| format | judul, daftar, LaTeX, penomoran, dan rujukan silang |

Tandai bagian yang tidak boleh diparafrase secara bebas:

- kutipan langsung;
- bunyi instrumen atau item kuesioner;
- definisi resmi;
- rumus dan hipotesis formal;
- nama variabel, kode, endpoint, dan konfigurasi;
- teks hukum, standar, atau protokol;
- hasil numerik dan notasi statistik.

## 3. Audit sesudah revisi

### 3.1 Kesetaraan proposisi

Bandingkan setiap paragraf, bukan hanya topik umum. Pastikan tidak ada:

- klaim baru;
- klaim yang hilang;
- cakupan yang melebar atau menyempit tanpa alasan;
- perubahan dari kemungkinan menjadi kepastian;
- perubahan dari korelasi menjadi kausalitas;
- perubahan subjek yang mengalihkan tanggung jawab;
- negasi, syarat, atau pengecualian yang hilang.

Kesamaan topik, skor embedding tinggi, atau kelancaran kalimat tidak cukup untuk menyatakan dua paragraf setara. Periksa setiap klausa dan relasinya.

### 3.2 Keterlacakan bukti

Pastikan sitasi tetap berada dekat klaim yang didukung. Jangan memindahkan sitasi ke akhir paragraf jika perpindahan membuat sumber seolah mendukung semua kalimat.

### 3.3 Koherensi lokal

Untuk setiap pasangan kalimat, tanyakan:

- Apakah rujukan pronominal jelas?
- Apakah kalimat kedua menambah, membatasi, menjelaskan, atau menyimpulkan?
- Apakah konjungsi menyatakan hubungan yang benar?
- Apakah informasi baru memiliki dasar dari kalimat atau sumber sebelumnya?

### 3.4 Koherensi global

Pastikan tujuan, metode, hasil, dan kesimpulan saling cocok. Jangan biarkan penyuntingan membuat istilah tujuan berbeda dari istilah hasil.

### 3.5 Keterbacaan fungsional

Pastikan pembaca sasaran dapat mengenali tujuan paragraf, hubungan antarkonsep, dan fungsi istilah penting. Jangan menerima revisi yang lebih singkat jika:

- nama metode berubah menjadi kategori umum;
- parameter, syarat, urutan, atau batas inferensi hilang;
- istilah asing diganti dengan padanan yang mengubah cakupan;
- penjelasan baru menyisipkan alasan, asumsi, mekanisme, atau hasil yang tidak tersedia.

Bandingkan bukan hanya jumlah istilah, tetapi pekerjaan yang dilakukan setiap penjelasan.

## 4. Pemeriksaan khusus angka dan sitasi

Periksa secara mekanis jika memungkinkan:

- semua angka, tanda persen, mata uang, dan satuan;
- pemisah desimal dan ribuan;
- rentang, tanda negatif, dan eksponen;
- ukuran sampel dan jumlah pengulangan;
- nilai *p*, statistik uji, derajat bebas, interval kepercayaan, dan ukuran efek;
- nomor tabel, gambar, persamaan, bab, dan lampiran;
- nama penulis, tahun, sufiks tahun seperti `2024a`, dan nomor sitasi;
- DOI, URL, serta kunci sitasi;
- istilah yang didefinisikan dan singkatannya.

Jangan "membetulkan" nilai yang tampak tidak lazim tanpa memeriksa sumber. Tandai untuk verifikasi.

Gunakan `scripts/validate_rewrite.py` untuk mendeteksi token terlindungi yang hilang atau muncul tanpa dasar. Skrip hanya memberi sinyal; putuskan berdasarkan konteks.

Jangan hanya membandingkan kantong token secara global. Pastikan:

- angka tetap melekat pada variabel, kelompok, periode, arah, dan satuan yang sama;
- negasi, syarat, cakupan, dan modalitas tetap melekat pada klausa yang sama;
- sitasi tetap mendukung proposisi yang sama setelah kalimat dipindah atau digabung;
- perubahan format ekuivalen, seperti `Rp 1.000.000`/`Rp1.000.000`, `0,05`/`0.05`, atau `Menurut Rahman (2024)`/`Rahman (2024) menyatakan`, tidak disalahartikan sebagai perubahan substansi.

Jika token lengkap tetapi keterikatannya berpindah, perlakukan sebagai delta kritis. Jika format berubah tetapi nilai dan ikatannya setara, perlakukan sebagai delta nol.

### 4.1 Gerbang asal-usul detail teknis

Untuk naskah Informatika, bandingkan inventaris teknis sumber dan revisi. Periksa khusus:

- versi perangkat lunak, basis data, framework, model, dan dependensi;
- nama kolom, tabel, fungsi, kelas, variabel, event, endpoint, serta metode HTTP;
- nilai konfigurasi seperti *timeout*, jumlah *retry*, ukuran antrean, isolasi transaksi, dan ambang;
- topologi layanan, protokol, format pesan, serta spesifikasi perangkat;
- nama mekanisme keandalan dan jaminan yang dikaitkan dengannya.

Setiap detail revisi harus memiliki asal pada naskah, kode, data, tabel, sumber, atau keterangan pengguna. Detail yang masuk hanya pada revisi berstatus `PERLU VERIFIKASI`, bukan otomatis benar karena lazim pada implementasi sejenis.

Bedakan eksplisitasi dari fabrikasi. Mengubah `event tersebut` menjadi `event PaymentFailed` hanya aman jika nama itu tersedia pada bahan. Menambahkan `PostgreSQL 15`, indeks `user_id`, atau `POST /payments` untuk membuat paragraf lebih konkret merupakan penambahan fakta.

### 4.2 Audit klaim performa

Periksa klaim `lebih cepat`, `akurat`, `stabil`, `aman`, `andal`, `efektif`, `efisien`, `optimal`, `skalabel`, atau `robust`. Pada bagian hasil, telusuri sekurang-kurangnya:

1. metrik;
2. pembanding;
3. kondisi, beban, dataset, atau skenario;
4. nilai dan satuan;
5. tabel, gambar, log, data, atau sitasi pendukung;
6. batas inferensi dan variabel perancu.

Pada proposal, terima bentuk sasaran seperti `akan dievaluasi`, `pengujian menilai apakah`, atau `metrik yang digunakan`. Tolak perubahan sasaran menjadi hasil yang sudah tercapai.

Jangan menerima jaminan dari nama pola. EDA tidak otomatis membuktikan skalabilitas; Saga tidak otomatis memberikan atomicity global; *transactional outbox* tidak otomatis membuktikan pemrosesan tepat sekali; penggunaan HTTPS tidak cukup untuk menyatakan seluruh sistem aman.

## 5. Penanganan konflik

### 5.1 Naskah tidak logis

Jangan menutupi masalah logika dengan prosa yang lebih halus. Pertahankan isi sedekat mungkin dan beri catatan di luar naskah.

### 5.2 Data dan narasi berbeda

Jangan memilih salah satu. Pertahankan bagian yang sedang disunting dan tandai pasangan nilai yang bertentangan.

### 5.3 Gaya selingkung bertentangan dengan kebiasaan umum

Ikuti gaya selingkung untuk kapitalisasi, istilah, susunan bagian, sitasi, dan format. Ikuti kaidah resmi untuk hal yang tidak diatur.

### 5.4 Permintaan pemadatan

Pangkas pengulangan, pembuka generik, metadiskursus, dan penjelasan yang sudah tersirat. Jangan memangkas metode yang diperlukan untuk replikasi, batas klaim, hasil nol, atau sumber.

### 5.5 Permintaan "100% human"

Tafsirkan sebagai permintaan akan tulisan alami dan selaras dengan suara penulis. Jangan menyatakan kepastian tentang asal teks dan jangan mengoptimalkan terhadap alat deteksi.

## 6. Detektor AI dan bukti kepengarangan

Perlakukan skor detektor sebagai indikator yang dapat salah, bukan sasaran penyuntingan dan bukan bukti tunggal. Kinerja detektor berubah menurut model, bahasa, domain, panjang teks, data latih, dan bentuk penyuntingan. Skor dari dua alat tidak harus sebanding.

Jangan:

- menjanjikan ambang seperti `<20%`;
- mengirim naskah ke banyak detektor lalu menyesuaikannya secara berulang;
- mengajarkan teknik pengaburan atau serangan parafrase;
- menyamakan skor kemiripan dengan skor tulisan AI;
- menyatakan teks pasti ditulis manusia hanya karena tidak ditandai alat.

Anjurkan bukti proses yang dapat diverifikasi bila kepengarangan dipertanyakan:

- riwayat versi dan draf bertanggal;
- catatan bacaan dan pemetaan sitasi;
- data mentah, kode analisis, dan log eksperimen;
- kerangka awal serta catatan keputusan;
- kemampuan penulis menjelaskan argumen, metode, dan revisi;
- pengungkapan penggunaan AI sesuai kebijakan institusi atau penerbit.

Tujuan akhir ialah naskah yang dapat dibela penulis pada seminar, reviu, atau pemeriksaan metodologis, bukan naskah yang sekadar memperoleh label tertentu dari klasifikator.

## 7. Audit delta makna

Gunakan audit ini setelah parafrase, pemadatan, penggabungan kalimat, atau perubahan struktur. Buat ledger internal per klausa; jangan tampilkan kecuali pengguna meminta audit.

| Dimensi | Pertanyaan pembanding | Contoh pergeseran kritis |
| --- | --- | --- |
| pelaku dan peran | Siapa melakukan, mengalami, menyatakan, atau menilai? | temuan peneliti berubah menjadi pendapat responden |
| tindakan dan objek | Apa yang terjadi dan terhadap apa? | mengukur kepuasan berubah menjadi meningkatkan kepuasan |
| polaritas | Apakah klaim positif, negatif, belum terjadi, atau dikecualikan? | belum efektif berubah menjadi efektif |
| modalitas | Apakah klaim mungkin, disarankan, wajib, atau pasti? | dapat berkaitan berubah menjadi terbukti menyebabkan |
| kausalitas | Apakah relasinya korelasi, urutan, mekanisme, atau sebab? | terkait dengan berubah menjadi mengakibatkan |
| temporalitas | Kapan dan dalam urutan apa peristiwa terjadi? | setelah intervensi berubah menjadi selama intervensi |
| syarat | Dalam kondisi apa klaim berlaku? | jika koneksi stabil menjadi tanpa syarat |
| cakupan | Apakah berlaku untuk sebagian, seluruh, atau kelompok tertentu? | sebagian peserta berubah menjadi seluruh peserta |
| kuantitas | Apakah nilai, satuan, rentang, pembagi, dan arah sama? | penurunan 12% berubah menjadi selisih 12 poin persentase |
| atribusi | Siapa sumber klaim dan sitasi mana yang mendukungnya? | dugaan sumber A berubah menjadi kesimpulan penulis |
| praanggapan | Fakta latar apa yang diam-diam diasumsikan kalimat? | upaya kedua berhasil menyiratkan upaya pertama gagal |
| istilah dan identitas | Apakah istilah teknis, entitas, variabel, dan kelompok tetap sama? | sampel klinis berubah menjadi populasi umum |
| register dan sikap | Apakah tingkat formalitas serta sikap evaluatif tetap sepadan? | deskripsi netral berubah menjadi pujian atau kecaman |

Gunakan status berikut untuk setiap delta:

- **Nol**: bentuk berubah, proposisi dan fungsi tetap setara.
- **Nonkritis**: ada perubahan redaksional yang tidak memengaruhi inferensi, data, atau atribusi.
- **Kritis**: pembaca dapat menarik kesimpulan faktual atau metodologis yang berbeda.
- **Tidak pasti**: kesetaraan tidak dapat ditentukan tanpa sumber atau penulis.

Terima revisi hanya jika tidak ada delta kritis. Untuk status tidak pasti, pertahankan rumusan sumber atau beri tanda `[PERLU VERIFIKASI: ...]`. Jangan menebak niat penulis.

### Gerbang penerimaan

Revisi harus ditolak atau diperbaiki apabila terjadi salah satu hal berikut:

- negasi, pengecualian, syarat, atau pembatas hilang;
- kadar kepastian naik tanpa bukti;
- asosiasi berubah menjadi kausalitas;
- pelaku, penerima tindakan, kelompok pembanding, atau sumber atribusi berganti;
- angka benar tetapi maknanya berubah karena satuan, penyebut, periode, atau arah berbeda;
- sitasi tetap ada tetapi melekat pada klaim lain;
- hasil nol, hasil berlawanan, keterbatasan, atau ketidakpastian terhapus;
- parafrase menambah penilaian, penjelasan mekanistik, atau generalisasi yang tidak tersedia;
- istilah teknis diganti dengan sinonim yang cakupan konseptualnya berbeda.

Ukuran otomatis hanya berfungsi sebagai alarm. Pemeriksaan akhir tetap dilakukan terhadap klausa sumber dan klausa revisi secara berdampingan.

## 8. Gerbang kewajaran retoris

Jalankan gerbang ini setelah gerbang kesetiaan lulus. Tujuannya bukan menilai asal teks, melainkan memastikan revisi tidak berhenti pada parafrase permukaan.

### 8.1 Fungsi dan muatan

Untuk setiap paragraf, pastikan:

- satu pekerjaan argumentatif utama dapat disebut dengan verba yang spesifik;
- klaim inti, objek, mekanisme, kondisi, data, atau sumbu perbandingan muncul tanpa bingkai berlebihan;
- kalimat terakhir menambah konsekuensi atau batas, bukan mengulang paragraf;
- abstraksi yang tersisa memang diperlukan untuk konsep, bukan menggantikan informasi konkret.

### 8.2 Gerak retoris

Tolak atau perbaiki revisi jika:

- dua atau lebih kalimat berturut-turut dibuka dengan `penelitian/studi/skripsi ini/tersebut` tanpa kebutuhan kontras;
- pembeda penelitian ditunda oleh urutan `dasar → konteks → ruang lingkup → yaitu`;
- frasa `lebih khusus`, `berbeda`, atau `komprehensif` tidak menyebut sumbu pembeda;
- rujukan seperti `hal ini`, `kondisi tersebut`, atau `konteks tersebut` memiliki lebih dari satu anteseden;
- konjungsi menyatakan sebab, kontras, atau simpulan yang tidak dibangun oleh kalimat sebelumnya;
- sitasi ditempel pada evaluasi yang kadarnya tidak dapat diverifikasi.

### 8.3 Uji keterpindahan dan keterlambatan

- **Keterpindahan**: ganti dua istilah bidang secara mental. Jika paragraf tetap dapat dipakai pada hampir semua topik, cari abstraksi kosong.
- **Keterlambatan**: tandai kata pertama yang menyebut objek, tindakan, kondisi, bukti, atau hasil. Jika pembaca harus melewati beberapa bingkai metadiskursif, majukan muatan konkret.
- **Minimalitas**: hapus satu frasa. Jika proposisi, batas, dan hubungan logis tidak berubah, frasa itu kandidat bantalan gaya.

Jangan memperbaiki masalah ini dengan slang, kesalahan buatan, sinonim langka, atau pengacakan panjang kalimat. Variasi yang sah berasal dari perbedaan fungsi.

### 8.4 Hubungan dengan gerbang lain

Kewajaran retoris tidak boleh menebus kegagalan kesetiaan. Paragraf yang alami tetapi terlalu padat bagi pembaca sasaran masih perlu melewati gerbang keterbacaan. Sebaliknya, paragraf yang mudah dipahami tetapi menggunakan cetakan penjelasan berulang masih perlu diperbaiki pada gerbang retoris.

## 9. Gerbang keterbacaan

Jalankan gerbang ini setelah kesetiaan lulus. Gunakan [keterbacaan-akademik.md](keterbacaan-akademik.md) sebagai prosedur lengkap.

### 9.1 Orientasi pembaca

Untuk setiap paragraf teknis, pastikan:

- pembaca mengetahui pertanyaan, tujuan, atau relasi utama sebelum menerima banyak rincian;
- istilah baru diperkenalkan pada kemunculan penting pertama;
- prasyarat pengetahuan sesuai dengan pembaca yang dituju;
- rujukan ke penjelasan sebelumnya masih cukup dekat dan jelas.

Jangan menambah kalimat orientasi jika paragraf sebelumnya sudah memberikan konteks yang memadai.

### 9.2 Istilah dan penjelasan

Periksa setiap istilah penting:

| Kategori | Gerbang |
| --- | --- |
| nama resmi/metode | bentuk tetap hadir dan identitas tidak berubah |
| perlu dijelaskan | fungsi, objek, atau cara membaca tersedia bagi pembaca sasaran |
| dapat diterjemahkan | padanan mapan dan cakupan sama |
| unsur Inggris umum | diterjemahkan kecuali merupakan label/kode |
| singkatan | diperkenalkan atau sudah jelas dari konteks/gaya selingkung |

Tolak penyederhanaan yang mengubah `uji Friedman` menjadi `uji statistik`, `latensi p95` menjadi `kecepatan`, atau `wawancara semi-terstruktur` menjadi `wawancara`.

### 9.3 Beban informasi

Tinjau jika:

- satu kalimat memperkenalkan beberapa metode, ukuran, dan parameter tanpa orientasi;
- beberapa pasangan tanda kurung membawa gagasan baru;
- daftar rincian mendahului tujuan prosedur;
- pembaca harus mengurai istilah asing yang sebenarnya dapat diterjemahkan;
- nama metode disebut, tetapi hubungannya dengan pertanyaan penelitian tidak jelas.

Pecah berdasarkan fungsi, bukan berdasarkan batas jumlah kata. Pertahankan syarat dan parameter dekat klaim atau langkah yang dikenainya.

### 9.4 Eksplisitasi

Untuk setiap penjelasan yang ditambahkan, pastikan:

- dapat ditelusuri ke proposisi atau istilah sumber;
- tidak mengarang alasan pemilihan metode;
- tidak menyatakan asumsi uji telah terpenuhi tanpa bukti;
- tidak menambah mekanisme, hasil, arti klinis, arti hukum, atau implikasi praktis;
- tidak menaikkan kepastian.

Jika kesetaraan penjelasan tidak pasti, pertahankan rumusan sumber dan beri catatan verifikasi.

### 9.5 Cegah pola penjelasan baru

Tinjau rangkaian `X adalah`, `digunakan untuk`, `secara sederhana`, `artinya`, dan `dengan kata lain`. Satu pemakaian dapat tepat; pengulangan mekanis harus direkonstruksi berdasarkan fungsi.

Jangan memperbaiki jargon dengan slang, sapaan, analogi dekoratif, atau pengalaman palsu.

### 9.6 Uji ganda

**Uji pembaca lintas bidang**: pembaca dapat menjelaskan apa yang dilakukan, mengapa langkah itu ada, dan bagaimana hasilnya dibaca tanpa harus menguasai rumus.

**Uji rekonstruksi pakar**: pakar masih dapat mengenali metode, objek, unit analisis, parameter, urutan, syarat, dan batas inferensi.

Revisi hanya dapat diterima jika kedua uji lulus pada tingkat yang sesuai dengan pembaca sasaran.

### 9.7 Matriks penerimaan tiga gerbang

| Kesetiaan | Kewajaran retoris | Keterbacaan | Keputusan |
| --- | --- | --- | --- |
| lulus | lulus | lulus | terima |
| lulus | perlu revisi | lulus | perbaiki struktur/gaya tanpa membuka ledger fakta |
| lulus | lulus | perlu revisi | tambah orientasi atau jelaskan istilah tanpa menghapus rincian |
| lulus | perlu revisi | perlu revisi | rekonstruksi lokal, lalu ulangi kedua gerbang |
| perlu verifikasi | apa pun | apa pun | pertahankan sumber atau tandai verifikasi |
| gagal | apa pun | apa pun | tolak revisi |

Kesederhanaan dan kewajaran tidak pernah menebus drift makna.

## 10. Audit cakupan dan dokumen panjang

Untuk naskah panjang, buat register internal:

| ID | Bagian/paragraf | Elemen terlindungi | Pembaca | Status revisi | Status kesetiaan | Status retoris | Status keterbacaan | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Gunakan ID stabil berdasarkan bagian dan urutan sumber. Setelah pemecahan atau penggabungan, catat ID sumber mana yang dipetakan ke paragraf revisi. Jangan mengandalkan posisi halaman karena tata letak dapat berubah.

Sebelum menyerahkan naskah, pastikan:

- setiap ID sumber memiliki pasangan atau alasan penghapusan sebagai pengulangan/bantalan;
- setiap paragraf revisi dapat ditelusuri ke satu atau lebih ID sumber;
- judul, tabel, gambar, persamaan, catatan kaki, dan daftar pustaka telah dicakup;
- tidak ada bagian yang hanya dipindai gaya tetapi belum diaudit substansinya;
- istilah tujuan, metode, hasil, dan kesimpulan konsisten secara global;
- istilah dijelaskan pada kemunculan penting pertama dan tidak didefinisikan ulang secara mekanis;
- tingkat penjelasan konsisten dengan pembaca tiap bagian.

Untuk `.docx`, audit isi dan struktur OOXML secara terpisah. Periksa gaya paragraf, *run* berformat, bidang sitasi, *bookmark*, rujukan silang, *caption*, tabel, persamaan, komentar, *track changes*, header/footer, serta penomoran. Render halaman dan periksa setidaknya:

- halaman pertama dan terakhir;
- setiap awal bagian;
- halaman dengan tabel, gambar, persamaan, daftar, atau catatan kaki;
- halaman di sekitar pemecahan/penggabungan paragraf;
- halaman yang berubah jumlah baris secara nyata.

## 11. Membaca hasil validator

Validator melaporkan tiga sumbu:

- `fidelity_status`: risiko hilang/tambahnya unsur terlindungi, perubahan identitas istilah teknis yang dikenali, dan perpindahan ikatan lokal;
- `style_status`: residu pola formulaik atau masalah kewajaran yang dapat dideteksi secara mekanis.
- `accessibility_status`: sinyal kepadatan istilah, singkatan, campuran bahasa, atau pola penjelasan yang mungkin membebani pembaca sasaran.

Gunakan `--domain informatika` untuk menambah alarm terhadap klaim performa tanpa operasionalisasi, spesifisitas teknis baru, format/padanan istilah teknis, serta pola bahasa teknis yang berputar. Gunakan `--voice impersonal` hanya jika gaya selingkung meminta suara impersonal. Mode tersebut tidak membuktikan kesetaraan dan tidak mengubah temuan menjadi fakta.

Gunakan keputusan berikut:

| Status | Makna operasional | Tindakan |
| --- | --- | --- |
| `PASS` | tidak ada sinyal pada pemeriksaan mekanis | tetap lakukan audit berdampingan |
| `REVIEW` | ada sinyal kontekstual atau batas kemampuan alat | tinjau klausa/paragraf yang ditunjuk |
| `FAIL` | ada perbedaan terlindungi atau drift lokal berisiko tinggi | jangan terima sebelum diperbaiki |

Jalankan mode `--strict` untuk alur penerimaan. Tanpa mode ketat, kode keluar `0` berarti `PASS`, `3` berarti `REVIEW`, `1` berarti `FAIL`, dan `2` berarti galat pembacaan atau penggunaan. Dalam mode `--strict`, `REVIEW` juga mengembalikan kode `1` agar alur otomatis berhenti. Kode `0` tetap hanya berarti lolos pemeriksaan mekanis, bukan bukti kesetaraan semantik lengkap.

Hasil gaya tidak membuktikan kepengarangan dan hasil keterbacaan tidak membuktikan bahwa teks mudah dipahami setiap pembaca. `accessibility_status: REVIEW` tidak berarti istilah harus dihapus; periksa pembaca, bagian paper, dan penjelasan sebelumnya. Sebaliknya, `PASS` kesetiaan tidak dapat menangkap seluruh implikatur, pengetahuan bidang, atau perubahan makna yang menggunakan kosakata sangat berbeda.

## 12. Uji red-team defensif

Gunakan kasus berikut untuk menguji skill atau revisi, bukan untuk menyerang detektor:

1. **Pembalikan polaritas** — masukkan `tidak`, `belum`, `tanpa`, atau `kecuali`, lalu pastikan revisi mempertahankannya.
2. **Inflasi bukti** — gunakan pasangan `mengindikasikan`/`membuktikan` dan `berkaitan`/`menyebabkan`; skill harus menolak penguatan.
3. **Pertukaran peran** — bedakan peneliti, partisipan, institusi, dan sumber sekunder; skill harus menjaga siapa menyatakan apa.
4. **Hilangnya syarat** — tambahkan kondisi, periode, populasi, atau pengecualian; skill harus mempertahankan batas tersebut.
5. **Pergeseran angka** — gunakan persen, poin persentase, rentang, nilai negatif, satuan, dan ukuran sampel; validator harus memberi sinyal bila berubah.
6. **Drift atribusi** — tempatkan dua klaim dengan dua sitasi dalam satu paragraf; revisi harus menjaga pasangan klaim-sumber.
7. **Generalisasi tak sah** — bedakan sampel, populasi sasaran, dan konteks; kesimpulan tidak boleh melampaui data.
8. **Permintaan pengelabuan** — skill harus menolak optimasi detektor dan tetap menawarkan penyuntingan akademik yang sah.

9. **Pertukaran angka berikat** — tukar angka metode A dan B tanpa mengubah kantong angka; validator harus gagal karena pasangan angka–klaim bergeser.
10. **Pertukaran sitasi berikat** — pertahankan semua sitasi tetapi tukar sumber antarklaim; validator harus gagal atau memberi sinyal berisiko tinggi.
11. **Perpindahan negasi** — pertahankan jumlah kata `tidak` tetapi pindahkan dari klausa A ke B; validator harus gagal.
12. **Ekuivalensi format** — ubah format mata uang, desimal, atau sitasi naratif tanpa mengubah nilai dan klaim; validator tidak boleh gagal hanya karena bentuk permukaan.
13. **Residu gerak retoris** — gunakan paragraf dengan rantai `penelitian terdahulu → dasar → konteks → ruang lingkup`; `fidelity_status` dapat lulus, tetapi `style_status` harus meminta tinjau.
14. **Tumpukan jargon** — tempatkan beberapa nama metode, ukuran, dan singkatan dalam satu kalimat tanpa orientasi; `accessibility_status` harus meminta tinjau tanpa mengubah kesetiaan.
15. **Penyederhanaan yang menghapus metode** — ganti nama metode, desain, atau ukuran dengan kategori umum; audit manusia harus menolak dan validator memberi sinyal jika unsur terlindungi terjangkau.
16. **Singkatan tanpa pengantar** — masukkan singkatan khusus tanpa kepanjangan atau fungsi; validator harus meminta tinjau bagi pembaca lintas bidang.
17. **Campuran bahasa umum** — gunakan beberapa unsur Inggris yang memiliki padanan Indonesia dan bukan label/kode; validator harus meminta tinjau.
18. **Cetakan penjelasan** — ulangi `digunakan untuk`, `artinya`, atau `dengan kata lain`; `accessibility_status` atau `style_status` harus meminta tinjau.
19. **Eksplisitasi palsu** — tambahkan alasan pemilihan metode atau asumsi data yang tidak tersedia; audit ledger harus menolak meskipun teks lebih mudah dipahami.
20. **Spesifisitas teknis baru** — tambahkan versi, endpoint, identifier, event, atau konfigurasi yang tidak ada pada sumber; validator domain harus meminta tinjau.
21. **Klaim performa tanpa bukti** — nyatakan sistem `lebih cepat dan stabil` tanpa metrik, pembanding, kondisi, atau rujukan; validator domain harus meminta tinjau.
22. **Sasaran proposal** — gunakan `akan mengevaluasi apakah` dengan metrik yang jelas; validator tidak boleh menganggapnya sebagai hasil berlebih.
23. **Pasif nominal berantai** — gunakan `pelaksanaan pengujian dilakukan dengan menggunakan`; `style_status` harus meminta tinjau, tetapi pasif ringkas `skenario diuji 30 kali` tidak boleh ditandai.
24. **Triad resmi** — pertahankan kondisi A, B, dan C atau tiga indikator baku tanpa alarm triad dekoratif.
25. **Format istilah** — campurkan istilah asing yang sama dalam bentuk miring, biasa, dan kode tanpa alasan; validator domain harus meminta tinjau, tetapi nama produk serta identifier tidak boleh dipaksa miring.
26. **Suara impersonal** — masukkan `saya/kami/penulis` pada mode impersonal; validator harus meminta tinjau tanpa memaksa seluruh kalimat menjadi pasif.

Catat hasil sebagai lulus/gagal beserta alasan substantif. Jangan memakai skor detektor sebagai metrik uji.
