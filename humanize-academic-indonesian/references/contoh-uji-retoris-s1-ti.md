# Contoh Uji Retoris S1 Teknik Informatika

## 0. Tujuan dan Cara Pakai

Dokumen ini berisi bank contoh untuk mengalibrasi revisi akademik S1 Teknik Informatika. Gunakan contoh ini untuk membedakan teks yang terlalu formulaik, wajar untuk skripsi S1 TI, terlalu profesional, atau rusak makna. Contoh tidak dimaksudkan sebagai template yang disalin mentah ke naskah pengguna.

Prinsip penggunaan:

- gunakan sebagai kasus uji untuk [residu-retoris-akademik.md](residu-retoris-akademik.md) dan [checker-metriks-retoris.md](checker-metriks-retoris.md);
- pertahankan makna, istilah teknis, angka, kondisi, dan batas klaim;
- jangan menambah detail teknis yang tidak tersedia pada sumber;
- jangan membuat teks sengaja salah agar terlihat manusiawi;
- pilih gaya formal, jelas, prosedural, dan wajar untuk skripsi S1 TI.

Status contoh:

| Status | Makna |
| :--- | :--- |
| Terlalu formulaik | Perlu direkonstruksi karena berputar, kosong, atau menunda muatan utama |
| Wajar S1 TI | Dapat diterima untuk skripsi jika makna sesuai sumber |
| Terlalu profesional | Secara bahasa baik, tetapi terlalu matang/abstrak untuk banyak skripsi S1 TI |
| Rusak makna | Harus ditolak karena mengubah fakta, klaim, istilah, atau batas |

---

## 1. Muatan Konkret yang Terlambat

### Kasus 1.1 Tujuan Penelitian

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Berdasarkan permasalahan yang telah dijelaskan, penelitian ini pada dasarnya diarahkan untuk dapat melakukan pengembangan terhadap suatu sistem informasi persediaan yang diharapkan mampu membantu proses pengelolaan data. |
| Wajar S1 TI | Penelitian ini mengembangkan sistem informasi persediaan untuk membantu pencatatan dan pemantauan data stok. |
| Terlalu profesional | Penelitian ini merancang artefak sistem informasi untuk mengoptimalkan visibilitas persediaan melalui konsolidasi data stok berbasis proses. |
| Rusak makna | Penelitian ini membuktikan bahwa sistem informasi persediaan meningkatkan efisiensi operasional apotek. |

Catatan: versi wajar tetap harus diturunkan jika sumber hanya menyebut rencana, bukan implementasi selesai. Versi rusak makna menambah klaim hasil.

### Kasus 1.2 Pembeda Penelitian

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Perbedaan fokus tersebut menjadi dasar dalam pengembangan konteks penelitian yang memiliki ruang lingkup lebih khusus dibandingkan penelitian sebelumnya. |
| Wajar S1 TI | Penelitian ini berfokus pada pengujian pencatatan stok pada tiga cabang, sedangkan penelitian sebelumnya hanya membahas pencatatan pada satu lokasi. |
| Terlalu profesional | Penelitian ini mempersempit cakupan evaluasi melalui diferensiasi unit analisis lintas lokasi untuk menguji konsistensi proses persediaan. |
| Rusak makna | Penelitian sebelumnya gagal menangani pencatatan stok lintas cabang. |

Catatan: jangan memakai versi wajar jika jumlah cabang atau pembeda tidak tersedia pada sumber.

---

## 2. Nominalisasi dan Pusat Tindakan

### Kasus 2.1 Metode Pengujian

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Pelaksanaan pengujian dilakukan dengan menggunakan metode black box untuk melakukan pengecekan terhadap fungsi-fungsi yang terdapat pada sistem. |
| Wajar S1 TI | Pengujian dilakukan dengan metode black box untuk memeriksa fungsi pada sistem. |
| Terlalu profesional | Pengujian black box memverifikasi kesesuaian perilaku fungsional sistem terhadap skenario validasi yang telah ditetapkan. |
| Rusak makna | Pengujian black box membuktikan bahwa seluruh fungsi sistem berjalan optimal. |

Catatan: versi profesional dapat dipakai jika naskah memang menuntut register lebih tinggi dan skenario validasi tersedia. Untuk skripsi S1, versi wajar sering cukup.

### Kasus 2.2 Perancangan Sistem

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Proses perancangan sistem dilakukan melalui pembuatan diagram yang digunakan untuk memberikan gambaran terhadap alur dari sistem yang dikembangkan. |
| Wajar S1 TI | Sistem dirancang menggunakan diagram untuk menggambarkan alur kerja aplikasi. |
| Terlalu profesional | Model perancangan memvisualisasikan alur kerja aplikasi sebagai representasi awal dari interaksi proses dan pengguna. |
| Rusak makna | Diagram membuktikan bahwa alur kerja aplikasi sudah sesuai dengan kebutuhan pengguna. |

Catatan: jangan menambah jenis diagram seperti use case, activity, atau sequence jika sumber tidak menyebutnya.

---

## 3. Rantai Subjek Metadiskursif

### Kasus 3.1 Paragraf Pendahuluan

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Penelitian ini membahas sistem persediaan. Penelitian ini menggunakan metode waterfall. Penelitian ini menghasilkan aplikasi berbasis web. |
| Wajar S1 TI | Penelitian ini membahas sistem persediaan berbasis web. Pengembangan dilakukan dengan metode waterfall, mulai dari analisis kebutuhan hingga pengujian. |
| Terlalu profesional | Kajian ini mengonstruksi artefak perangkat lunak berbasis web melalui pendekatan waterfall sebagai kerangka rekayasa kebutuhan hingga validasi. |
| Rusak makna | Penelitian ini membandingkan waterfall dengan agile untuk menentukan metode terbaik. |

Catatan: versi wajar mengurangi rantai `penelitian ini` tanpa mengubah metode atau keluaran.

### Kasus 3.2 Kajian Pustaka

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Penelitian terdahulu tersebut menjadi dasar penelitian ini. Penelitian ini memiliki perbedaan pada fokus yang lebih khusus. Penelitian ini melanjutkan konteks tersebut. |
| Wajar S1 TI | Penelitian terdahulu digunakan sebagai acuan karena sama-sama membahas sistem persediaan. Perbedaannya terletak pada objek penelitian dan fitur laporan stok yang dikembangkan. |
| Terlalu profesional | Studi terdahulu diposisikan sebagai referensi konseptual untuk membangun diferensiasi objek dan keluaran fungsional penelitian saat ini. |
| Rusak makna | Penelitian terdahulu tidak lengkap karena belum menyediakan fitur laporan stok. |

Catatan: `tidak lengkap` adalah penilaian yang perlu bukti eksplisit.

---

## 4. Stabilitas Istilah Inti

### Kasus 4.1 Sistem atau Aplikasi

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Sistem ini merupakan aplikasi yang menjadi platform solusi dalam mendukung proses pengelolaan data pengguna. |
| Wajar S1 TI | Aplikasi ini digunakan untuk mengelola data pengguna. |
| Terlalu profesional | Platform perangkat lunak ini memfasilitasi manajemen data pengguna melalui antarmuka operasional. |
| Rusak makna | Aplikasi ini mengamankan seluruh data pengguna dari risiko kebocoran. |

Catatan: pilih `sistem` atau `aplikasi` sesuai sumber. Jangan berganti istilah hanya untuk variasi.

### Kasus 4.2 Pengujian, Evaluasi, dan Validasi

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Evaluasi dilakukan melalui proses validasi pengujian untuk memastikan sistem dapat berjalan dengan baik. |
| Wajar S1 TI | Pengujian dilakukan untuk memeriksa apakah fitur sistem berjalan sesuai skenario. |
| Terlalu profesional | Evaluasi fungsional dilakukan untuk menilai kesesuaian respons sistem terhadap skenario operasional yang telah ditentukan. |
| Rusak makna | Validasi membuktikan sistem bebas dari kesalahan. |

Catatan: `validasi` boleh dipakai jika yang dimaksud pemeriksaan input atau kebenaran data. Jangan dipakai sebagai sinonim acak dari `pengujian`.

---

## 5. Klaim Evaluatif dan Performa

### Kasus 5.1 Efektif dan Efisien

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Sistem ini diharapkan mampu memberikan solusi yang efektif dan efisien dalam meningkatkan kualitas pengelolaan data secara optimal. |
| Wajar S1 TI | Sistem ini diharapkan dapat membantu petugas mencatat dan mencari data stok dengan lebih mudah. |
| Terlalu profesional | Sistem ini diproyeksikan meningkatkan efisiensi operasional melalui reduksi beban pencatatan dan percepatan akses data persediaan. |
| Rusak makna | Sistem ini terbukti meningkatkan efisiensi pencatatan stok. |

Catatan: pada proposal, gunakan `diharapkan` atau `akan diuji`. Pada hasil, klaim efisiensi butuh metrik, pembanding, dan kondisi.

### Kasus 5.2 Akurasi

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Penerapan sistem ini memberikan hasil yang akurat dan signifikan terhadap proses pengolahan data. |
| Wajar S1 TI | Hasil pengujian menunjukkan bahwa sistem menghasilkan keluaran sesuai dengan data masukan pada skenario yang diuji. |
| Terlalu profesional | Hasil pengujian mengindikasikan kesesuaian keluaran sistem terhadap input pada skenario validasi yang tersedia. |
| Rusak makna | Sistem memiliki akurasi 100% pada seluruh kondisi penggunaan. |

Catatan: `akurasi` perlu definisi, rumus, atau skenario. Jangan menambahkan persentase tanpa sumber.

---

## 6. Bab Skripsi S1 TI

### Kasus 6.1 Bab 1 Tujuan

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Berdasarkan uraian tersebut, tujuan dari penelitian ini adalah untuk dapat melakukan perancangan dan pembangunan sistem yang mampu memberikan manfaat bagi berbagai pihak. |
| Wajar S1 TI | Tujuan penelitian ini adalah merancang dan membangun sistem pencatatan stok berbasis web. |
| Terlalu profesional | Penelitian ini bertujuan menghasilkan artefak perangkat lunak berbasis web untuk mendukung tata kelola persediaan. |
| Rusak makna | Tujuan penelitian ini adalah membuktikan bahwa sistem web lebih baik daripada pencatatan manual. |

Catatan: versi rusak makna menambah pembanding dan klaim pembuktian.

### Kasus 6.2 Bab 3 Tahapan

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Tahapan penelitian dilakukan dengan melakukan beberapa proses yang meliputi analisis, perancangan, implementasi, dan pengujian. |
| Wajar S1 TI | Tahapan penelitian meliputi analisis kebutuhan, perancangan sistem, implementasi, dan pengujian. |
| Terlalu profesional | Alur penelitian disusun sebagai rangkaian rekayasa perangkat lunak yang mencakup identifikasi kebutuhan hingga validasi artefak. |
| Rusak makna | Tahapan penelitian menggunakan metode eksperimen untuk membandingkan beberapa algoritma. |

Catatan: jangan mengganti tahapan menjadi metode lain jika sumber hanya menyebut tahapan pengembangan sistem.

### Kasus 6.3 Bab 4 Hasil Black Box

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Berdasarkan hasil dari pengujian yang telah dilakukan, dapat diketahui bahwa seluruh fitur yang terdapat pada sistem dapat berjalan dengan baik dan sesuai harapan. |
| Wajar S1 TI | Berdasarkan hasil pengujian black box, seluruh fitur yang diuji berjalan sesuai skenario. |
| Terlalu profesional | Hasil pengujian black box memperlihatkan kesesuaian respons fungsional sistem terhadap seluruh skenario uji yang tersedia. |
| Rusak makna | Pengujian black box membuktikan bahwa sistem bebas dari bug. |

Catatan: `seluruh fitur` hanya sah jika semua fitur memang diuji. Jika hanya sebagian, tulis `fitur yang diuji`.

### Kasus 6.4 Bab 5 Saran

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Penelitian selanjutnya diharapkan dapat mengembangkan sistem ini agar menjadi lebih baik, lebih lengkap, dan lebih optimal di masa depan. |
| Wajar S1 TI | Penelitian selanjutnya dapat menambahkan fitur notifikasi stok minimum agar petugas mengetahui barang yang perlu dipesan kembali. |
| Terlalu profesional | Pengembangan lanjutan dapat diarahkan pada mekanisme peringatan persediaan untuk meningkatkan respons operasional terhadap ambang stok. |
| Rusak makna | Penelitian selanjutnya harus menggunakan machine learning agar sistem menjadi lebih akurat. |

Catatan: saran harus turun dari keterbatasan atau kebutuhan yang tersedia, bukan dari teknologi yang terdengar maju.

---

## 7. Interferensi Bahasa Inggris dan Istilah Teknis

### Kasus 7.1 Unsur Inggris Umum

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | User dapat melakukan request data melalui fitur search yang tersedia pada sistem. |
| Wajar S1 TI | Pengguna dapat mencari data melalui fitur pencarian pada sistem. |
| Terlalu profesional | Pengguna dapat melakukan penelusuran data melalui fungsi pencarian yang tersedia pada antarmuka sistem. |
| Rusak makna | Pengguna dapat mengakses seluruh data melalui fitur pencarian. |

Catatan: `user`, `request`, dan `search` dapat diterjemahkan jika bukan label antarmuka atau kode. `seluruh data` menambah cakupan.

### Kasus 7.2 Endpoint dan Kode

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Endpoint `POST /login` digunakan untuk melakukan proses login user ke dalam sistem aplikasi. |
| Wajar S1 TI | Endpoint `POST /login` digunakan untuk memproses login pengguna. |
| Terlalu profesional | Endpoint `POST /login` menangani autentikasi awal pengguna sebelum sistem memberikan akses sesi. |
| Rusak makna | Endpoint `POST /login` mengenkripsi seluruh data pengguna. |

Catatan: pertahankan endpoint sebagai kode. Jangan menambah autentikasi sesi atau enkripsi jika tidak tersedia pada sumber.

---

## 8. Negasi Polar Defensif Berulang

### Kasus 8.1 Motivasi Penelitian

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Kebutuhan pengembangan tidak berangkat dari asumsi bahwa arsitektur monolith selalu tidak memadai, melainkan dari kebutuhan Apotek Bisma untuk mengelola proses multicabang secara terpusat. |
| Wajar S1 TI | Apotek Bisma memerlukan pengelolaan proses multicabang secara terpusat. Arsitektur monolith yang ada tetap menjadi baseline fungsional; migrasi didorong oleh kebutuhan koordinasi data lintas cabang dan gudang, bukan oleh asumsi bahwa monolith tidak memadai. |
| Terlalu profesional | Motivasi migrasi arsitektural diposisikan pada kebutuhan orkestrasi data lintas cabang, bukan pada inferensi kegagalan inheren arsitektur monolitik terpusat. |
| Rusak makna | Arsitektur monolith tidak memadai sehingga Apotek Bisma memerlukan migrasi ke microservices. |

Catatan: versi formulaik memakai pola `tidak X, melainkan Y` yang menanggapi asumsi yang belum diajukan pembaca. Versi wajar memajukan alasan positif, lalu menempatkan pembatasan sebagai klausa akhir. Versi rusak makna menghilangkan pembatasan dan mengubah posisi penulis terhadap monolith.

### Kasus 8.2 Kontribusi Penelitian

| Status | Contoh |
| :--- | :--- |
| Terlalu formulaik | Kontribusi yang ditargetkan bukan pola baru, melainkan evaluasi terukur terhadap kombinasi mekanisme proteksi pada konteks transaksi apotek. |
| Wajar S1 TI | Kontribusi yang ditargetkan adalah evaluasi terukur terhadap kombinasi mekanisme proteksi pada konteks transaksi apotek. |
| Terlalu profesional | Kontribusi penelitian diposisikan sebagai evaluasi empiris terukur terhadap integrasi mekanisme proteksi konsistensi dalam domain transaksional farmasi retail. |
| Rusak makna | Penelitian ini menghasilkan pola baru untuk proteksi konsistensi pada transaksi apotek. |

Catatan: versi formulaik menyangkal hal yang tidak dituduhkan pembaca (`bukan pola baru`). Cukup nyatakan apa kontribusinya secara langsung. Versi rusak makna justru mengklaim pola baru.

### Kasus 8.3 Negasi Operasional yang Sah

| Status | Contoh |
| :--- | :--- |
| Wajar S1 TI | Keberhasilan Kondisi C tidak ditentukan hanya oleh latency atau throughput, melainkan terutama oleh tidak ditemukannya oversell, lost update, duplicate effect, untraceable event, dan permanent mismatch pada konfigurasi pengujian yang telah dikunci. |

Catatan: pola `tidak...hanya...melainkan terutama` dipertahankan karena membedakan dua kelompok metrik sebagai kriteria keberhasilan. Tanpa kontras ini pembaca dapat salah menilai keberhasilan hanya dari metrik performa. Ini bukan pola defensif kosong.

---

## 9. Test Case Ringkas untuk Checker

Gunakan daftar ini sebagai red-team kecil untuk rule otomatis.

| ID | Input Singkat | Rule yang Diharapkan | Status Minimal |
| :--- | :--- | :--- | :--- |
| TC-01 | *Penelitian ini membahas sistem. Penelitian ini menggunakan waterfall. Penelitian ini menghasilkan aplikasi.* | `MSC_METADISCURSIVE_CHAIN` | REVIEW |
| TC-02 | *Sistem dirancang menggunakan use case diagram dan activity diagram.* | `S1TI_CHAPTER_FUNCTION_GUARD` | INFO |
| TC-03 | *Pengujian dilakukan untuk memeriksa fitur login.* | `S1TI_PROCEDURAL_STYLE_GUARD` | INFO |
| TC-04 | *Pelaksanaan pengujian dilakukan dengan melakukan pengecekan terhadap proses sistem.* | `VNR_OVER_NOMINALIZATION` | REVIEW |
| TC-05 | *Aplikasi ini menjadi platform solusi ekosistem digital.* | `S1TI_CORE_TERM_STABILITY` | REVIEW |
| TC-06 | *Hasil ini memiliki implikasi epistemik terhadap validitas eksternal sistem stok.* | `S1TI_REGISTER_OVERPOLISH` | REVIEW |
| TC-07 | *Sistem terbukti efisien tanpa metrik pembanding.* | `EAC_EVALUATIVE_ADJECTIVE_CLAIM` | REVIEW/FAIL |
| TC-08 | *Uji Friedman digunakan untuk membandingkan tiga kondisi.* | `TIG_TECHNICAL_IDENTITY_GUARD` | PASS/INFO |
| TC-09 | *Uji Friedman diganti menjadi uji statistik agar lebih mudah dibaca.* | `TIG_TECHNICAL_IDENTITY_GUARD` | FAIL |
| TC-10 | *Berdasarkan hal tersebut, penelitian ini pada dasarnya diarahkan untuk dapat melakukan pengembangan...* | `DCP_DELAYED_CONCRETE_PAYLOAD` | REVIEW |
| TC-11 | *Penelitian ini lebih khusus dibandingkan penelitian sebelumnya.* | `ADS_AXISLESS_DIFFERENCE` | REVIEW |
| TC-12 | *Berdasarkan hasil pengujian black box, fitur yang diuji berjalan sesuai skenario.* | `S1TI_NATURALNESS_GATE` | PASS |
| TC-13 | *Kebutuhan pengembangan tidak berangkat dari asumsi bahwa monolith tidak memadai, melainkan dari kebutuhan apotek. Kontribusi bukan pola baru, melainkan evaluasi terukur.* | `SRWD_POLAR_NEGATION` | REVIEW |
| TC-14 | *Keberhasilan Kondisi C tidak ditentukan hanya oleh latency, melainkan terutama oleh tidak ditemukannya oversell.* | `SRWD_POLAR_NEGATION` | INFO/PASS |

---

## 10. Rubrik Sidang-Ready

Sebelum menerima revisi skripsi S1 TI, tanyakan apakah penulis dapat menjawab pertanyaan berikut tanpa menambah fakta baru:

- Apa yang dibuat atau diuji?
- Data, fitur, atau skenario mana yang dibahas?
- Metode, diagram, framework, endpoint, atau algoritma apa yang benar-benar digunakan?
- Hasil mana yang mendukung klaim?
- Apakah klaim `efektif`, `efisien`, `akurat`, `andal`, atau `optimal` punya metrik atau skenario?
- Apa batas penelitian yang tidak boleh dilampaui?
- Jika dosen bertanya "berbeda dari penelitian terdahulu pada bagian apa?", apakah sumbunya jelas?
- Jika istilah teknis dihapus atau diganti, apakah penguji masih dapat menelusuri metode dan implementasi?

Jika jawaban bergantung pada informasi yang tidak ada di sumber, revisi harus diturunkan atau diberi catatan verifikasi. Teks yang terdengar lancar tetapi tidak dapat dipertanggungjawabkan saat sidang tidak boleh diterima.
