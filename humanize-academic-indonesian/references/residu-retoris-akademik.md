# Residu Retoris Akademik (Context-Aware Edition)

## 0. Tujuan, Batas, dan Hubungan Dokumen

Dokumen ini dipakai setelah audit kesetiaan makna lulus. Tujuannya ialah menemukan residu retoris formulaik, bukan membuktikan asal teks, mengoptimalkan skor detektor, atau membuat variasi permukaan. Semua tindakan tunduk pada hierarki keputusan di [qa-dan-integritas.md](qa-dan-integritas.md), ragam bagian di [ragam-akademik.md](ragam-akademik.md), kalibrasi pembaca di [keterbacaan-akademik.md](keterbacaan-akademik.md), serta perlindungan detail teknis di [informatika-akademik.md](informatika-akademik.md).

Revisi retoris hanya sah jika pola yang terdeteksi:

- berulang dalam konteks lokal;
- tidak membawa fungsi argumentatif;
- mengaburkan pelaku, tindakan, objek, syarat, bukti, atau hubungan logis;
- menunda muatan konkret di balik bingkai metadiskursif;
- atau membuat paragraf dapat dipindahkan ke topik lain tanpa perubahan berarti.

Jangan merevisi hanya karena satu kata, satu bentuk pasif, satu transisi, atau satu kalimat panjang muncul. Keteraturan yang berasal dari metode, disiplin, gaya selingkung, atau identitas teknis harus dipertahankan.

---

## 1. Prinsip Utama dan Adaptivitas Kontekstual

Audit residu retoris dilakukan secara non-destruktif. Penggunaan nomina, konjungsi, pasif, dan struktur kalimat disesuaikan dengan fungsi akademik tiap bagian.

| Bagian | Fokus audit | Hal yang wajib dijaga |
| :--- | :--- | :--- |
| Pendahuluan / Latar Belakang | alur masalah-ke-solusi, muatan konkret, sumbu kesenjangan | konteks, batas masalah, sitasi, kadar klaim |
| Kajian Pustaka | hubungan sumber, pembeda, sintesis, atribusi | siapa menyatakan apa, batas sumber, sumbu perbandingan |
| Metodologi / Arsitektur Sistem | urutan prosedur, tanggung jawab komponen, keterulangan | istilah teknis, parameter, versi, endpoint, event, nama metode |
| Hasil | pola temuan, angka, arah perubahan, kondisi uji | nilai, satuan, tabel/gambar, statistik, hasil nol |
| Pembahasan | interpretasi, mekanisme, alternatif penjelasan, batas inferensi | modalitas, kausalitas, generalisasi, hubungan dengan bukti |

Status audit:

| Status | Makna | Tindakan |
| :--- | :--- | :--- |
| PASS | Tidak ada residu penting setelah konteks diperiksa | Terima dari sisi retoris |
| REVIEW | Ada pola yang berpotensi formulaik atau membebani pembaca | Rekonstruksi lokal jika pola tidak berfungsi |
| FAIL | Perbaikan retoris merusak makna, istilah, angka, sitasi, atau kadar klaim | Tolak revisi atau pulihkan sumber |

---

## 2. False Positive yang Wajib Dijaga

Jangan menandai bentuk berikut sebagai residu tanpa bukti kontekstual:

- pengulangan nama metode, algoritma, variabel, konstruk, endpoint, event, tabel, skenario, atau label instrumen;
- struktur pelaporan hasil yang harus konsisten karena memuat metrik, satuan, pembanding, atau tabel;
- urutan prosedur metodologis yang sengaja paralel;
- istilah teknis yang sudah didefinisikan dan harus tetap konsisten;
- daftar resmi indikator, kondisi eksperimen, kategori teori, atau item instrumen;
- kalimat pasif ringkas pada metode ketika prosedur atau objek menjadi fokus;
- kepadatan notasi statistik, rumus, parameter, satuan, kode, atau konfigurasi;
- pembuka paragraf yang seragam karena gaya selingkung atau format laporan memang mengharuskannya.

Jika ada konflik antara variasi retoris dan identitas teknis, pertahankan identitas teknis. Jika ada konflik antara kelancaran kalimat dan kesetiaan makna, pertahankan kesetiaan makna.

---

## 3. Ledger Residu Retoris

Gunakan ledger internal berikut sebelum merekonstruksi paragraf.

| Elemen | Pertanyaan Audit | Risiko Umum | Tindakan Aman |
| :--- | :--- | :--- | :--- |
| Fungsi paragraf | Apa pekerjaan utama paragraf? | Paragraf hanya "menjelaskan penelitian" tanpa fungsi spesifik | Nyatakan fungsi: membatasi, membandingkan, melaporkan, menafsirkan, atau menguji |
| Muatan konkret | Di mana objek, tindakan, kondisi, bukti, atau hasil pertama muncul? | Muatan inti tertunda oleh dasar/konteks/ruang lingkup | Majukan muatan yang sudah tersedia |
| Titik masuk | Apakah beberapa paragraf dimulai dari orientasi sama? | Semua paragraf dibuka dari "penelitian ini" atau "hal ini" | Rotasi berdasarkan fungsi, bukan variasi acak |
| Pusat tindakan | Apakah tindakan terkunci dalam nomina? | "Pelaksanaan pengujian dilakukan..." | Pulihkan verba jika pelaku/objek tersedia |
| Rujukan | Apakah "ini/tersebut/hal ini" punya anteseden tunggal? | Rujukan dapat menunjuk dua klaim | Ulangi nomina inti |
| Konjungsi | Apakah transisi menyatakan hubungan yang benar? | "Oleh karena itu" tanpa sebab sebelumnya | Hapus atau ganti sesuai hubungan |
| Sumbu pembeda | Jika ada "berbeda/lebih khusus", berbeda pada apa? | Pembeda tidak menyebut objek/metode/kondisi/metrik | Sebut sumbu yang tersedia atau tandai verifikasi |
| Portabilitas | Apakah paragraf tetap cocok jika dua istilah bidang diganti? | Paragraf terlalu generik | Tambahkan jangkar yang sudah ada, bukan fakta baru |

---

## 4. Audit Muatan Konkret yang Terlambat

Tandai kata pertama yang menyebut objek, tindakan, kondisi, data, bukti, atau hasil. Jika pembaca harus melewati beberapa bingkai seperti `berdasarkan hal tersebut`, `dalam konteks ini`, `pada dasarnya`, `sehubungan dengan`, `perbedaan fokus tersebut`, atau `ruang lingkup yang lebih khusus`, periksa apakah bingkai itu benar-benar membawa syarat, sumber, atau kontras.

### Pola Berisiko

- `Berdasarkan hal tersebut, penelitian ini pada dasarnya diarahkan untuk dapat melakukan pengujian terhadap...`
- `Dalam konteks pengembangan ruang lingkup tersebut, kajian ini berupaya memberikan kontribusi...`
- `Perbedaan fokus tersebut menjadi dasar dalam pelaksanaan penelitian yang lebih khusus...`

### Rekonstruksi Aman

- Majukan objek dan tindakan yang sudah tersedia.
- Pertahankan keterangan awal jika memuat syarat, sumber, periode, populasi, atau kontras yang tidak dapat disimpulkan pembaca.
- Jangan menambah detail baru hanya agar paragraf tampak konkret.

Contoh:

- Kurang efektif: *Berdasarkan perbedaan fokus tersebut, penelitian ini pada dasarnya diarahkan untuk melakukan pengujian terhadap konsistensi transaksi lintas layanan.*
- Lebih langsung: *Penelitian ini menguji konsistensi transaksi lintas layanan berdasarkan sumbu pembeda yang telah dijelaskan sebelumnya.*

Kalimat kedua hanya sah jika `konsistensi transaksi lintas layanan` dan sumbu pembeda memang tersedia pada sumber.

---

## 5. Audit Pengulangan Abstraksi Lokal

### A. Klasifikasi Abstraksi

| Kategori | Contoh | Perlakuan |
| :--- | :--- | :--- |
| Abstrak umum | `upaya`, `aspek`, `hal`, `konteks`, `pendekatan`, `strategi` | Tinjau jika berulang atau menggantikan muatan konkret |
| Nomina tindakan | `pengembangan`, `pengelolaan`, `penerapan`, `pelaksanaan`, `peningkatan` | Pulihkan verba jika tindakan, pelaku, atau objek menjadi kabur |
| Istilah domain potensial | `proses bisnis`, `mekanisme autentikasi`, `implementasi algoritma` | Pertahankan jika menjadi konsep teknis atau unit pembahasan |

### B. Pengulangan Nomina Non-Teknis yang Wajib Diurai

Pengulangan kata abstrak umum dalam satu konstruksi kalimat perlu diperbaiki jika tidak membawa nilai informasi substantif.

- Pola: `[Nomina Abstrak A] ... [Nomina Abstrak A]`
- Analisis: pengulangan abstraksi umum tanpa alasan teknis.
- Contoh:
  - Kurang efektif: *Kebutuhan pengembangan aplikasi ini muncul dari kebutuhan Apotek Bisma untuk...*
  - Lebih ringkas: *Pengembangan aplikasi ini didasari oleh kebutuhan Apotek Bisma untuk...*

### C. Exception Rule untuk Presisi Teknis

Jangan ubah pengulangan jika kata tersebut adalah istilah teknis domain, entitas data, variabel, label skenario, atau nama komponen.

- Boleh diulang: *Tabel transaksi cabang direkonsiliasi dengan tabel transaksi gudang.*
- Boleh diulang: *Endpoint pembayaran mengirim event pembayaran setelah status pembayaran berubah.*

Pada contoh kedua, variasi sinonim dapat merusak hubungan antara endpoint, event, dan status jika istilah itu mengacu pada artefak teknis yang berbeda.

---

## 6. Audit Pusat Tindakan dan Pasif

Nominalisasi sering mengubur tindakan utama di balik tumpukan kata benda. Namun, pasif dan nominalisasi tidak otomatis buruk dalam ragam akademik.

### A. Algoritma Keputusan Pemulihan Verba

1. Identifikasi frasa nominal bertumpuk, terutama tiga nomina atau lebih secara berdekatan.
2. Tentukan kata yang mewakili tindakan utama.
3. Periksa apakah pelaku, objek, dan kondisi tersedia pada sumber.
4. Jika tindakan utama terkunci dalam nomina non-spesifik seperti `pengelolaan`, `pelaksanaan`, `pembuatan`, atau `penerapan`, pulihkan menjadi verba aktif atau pasif yang sesuai fokus.
5. Jangan mengubah nama metode, istilah resmi, atau label teknis menjadi verba umum.

Contoh:

- Kurang efektif: *Pelaksanaan proses integrasi data cabang dilakukan oleh petugas...*
- Lebih langsung: *Petugas mengintegrasikan data cabang...*
- Tetap sah jika prosedur menjadi fokus: *Data cabang diintegrasikan pada tahap rekonsiliasi...*

### B. Rotasi Klausa Pasif Beruntun

Jika tiga kalimat berurutan dalam satu paragraf semuanya menggunakan predikat pasif dengan prefiks `di-` atau bentuk kosong seperti `dilakukan`, `digunakan`, `dilaksanakan`, dan `diimplementasikan`, tinjau apakah alur tindakan menjadi kabur.

Rekonstruksi minimal:

- ubah satu kalimat menjadi aktif nonpersonal jika komponen/pelaku teknis penting;
- jadikan objek atau hasil sebagai titik masuk jika pelaku tidak relevan;
- pertahankan pasif ringkas pada metode jika prosedur memang menjadi fokus.

Jangan mengaktifkan semua kalimat secara mekanis. Kalimat seperti *Setiap skenario diuji 30 kali* tetap alami dan presisi.

---

## 7. Audit Orientasi Paragraf

Mencegah monotonitas dilakukan dengan merotasi titik masuk paragraf berdasarkan fungsi, bukan dengan mengacak sinonim atau panjang kalimat. Jika tiga paragraf berurutan memiliki orientasi sama tanpa alasan genre, lakukan tinjauan.

| Orientasi | Contoh Titik Masuk | Fungsi yang Lazim |
| :--- | :--- | :--- |
| Masalah / kondisi lapangan | *Dengan terpisahnya basis data di setiap lokasi...* | menurunkan masalah dari kondisi nyata |
| Akibat / implikasi | *Keterlambatan deteksi selisih stok menjadi implikasi utama...* | menunjukkan konsekuensi |
| Aksi / tindakan sistem | *Penyelarasan arsitektur dilakukan melalui...* | menjelaskan respons atau prosedur |
| Entitas / subjek | *Apotek Bisma mengoperasikan tiga cabang...* | memberi jangkar domain |
| Bukti / hasil | *Tabel 4 menunjukkan...* | melaporkan observasi |
| Sumber | *Rahman (2024) menemukan...* | menjaga atribusi |
| Batas | *Pada skenario gangguan jaringan...* | membatasi cakupan klaim |

Rotasi tidak wajib jika bagian tersebut memang berupa langkah metode, butir hasil paralel, atau daftar kondisi eksperimen.

---

## 8. Rantai Subjek Metadiskursif

Tinjau dua atau lebih kalimat berdekatan yang dibuka dengan `penelitian ini`, `penelitian tersebut`, `studi ini`, `studi tersebut`, `skripsi ini`, `kajian ini`, atau bentuk sejenis. Bentuk tersebut tidak salah secara individual, tetapi rantainya sering membuat paragraf membicarakan naskah alih-alih objek, mekanisme, temuan, atau kondisi uji.

Rekonstruksi yang sah:

- jadikan objek, variabel, data, sistem, sumber, atau temuan sebagai subjek jika peran semantisnya benar;
- pertahankan `penelitian ini` ketika perlu membedakan penelitian sekarang dari sumber lain;
- jangan mengganti secara mekanis dengan `kajian ini`, `studi ini`, atau `riset ini`.

Contoh:

- Kurang efektif: *Penelitian ini membahas sistem persediaan. Penelitian ini menggunakan EDA. Penelitian ini menguji konsistensi transaksi.*
- Lebih fungsional: *Sistem persediaan menjadi objek utama penelitian. Arsitektur EDA digunakan untuk mengatur komunikasi antarlayanan. Konsistensi transaksi kemudian diuji pada skenario yang telah ditetapkan.*

Contoh revisi hanya sah jika EDA, antarlayanan, dan skenario uji memang tersedia pada bahan sumber.

---

## 9. Audit Konjungsi dan Negasi Polar

Pola sanggahan seperti `bukan X, melainkan Y` berguna untuk membatasi klaim, tetapi jika berulang dapat terasa defensif dan formulaik.

| Pola Formulaik | Risiko | Alternatif Kontekstual |
| :--- | :--- | :--- |
| `X bukan dari anggapan bahwa Y, melainkan...` | terdengar defensif atau seperti respons prompt | nyatakan alasan positif secara langsung jika Y tidak perlu disanggah |
| `kontribusi bukan X, melainkan Y` | menyangkal hal yang tidak dituduhkan pembaca | nyatakan kontribusi secara langsung |
| `bukan hanya X, tetapi juga Y` | memperbesar klaim tanpa bukti | pertahankan hanya jika X dan Y benar-benar dua kontribusi berbeda |
| `Oleh karena itu` berturut-turut | transisi terasa mekanis | gunakan transisi implisit, `dampaknya`, `atas dasar ini`, atau hapus jika hubungan sudah jelas |
| `Dengan demikian` setelah kalimat non-kausal | simpulan tidak dibangun | ganti dengan hubungan yang benar atau pisahkan klaim |

### Negasi polar defensif berulang

Jika pola `tidak/bukan X, melainkan/tetapi Y` muncul dua kali atau lebih dalam satu bagian, tinjau apakah sanggahan diperlukan untuk mencegah kesalahpahaman nyata atau hanya menjadi cetakan retoris. Cetakan ini menjadi sinyal kuat jika:

- sanggahan menanggapi tuduhan yang belum diajukan pembaca;
- kalimat sebelumnya tidak memuat pernyataan atau asumsi yang perlu dibantah;
- pola yang sama muncul pada paragraf berbeda sehingga membentuk irama defensif yang seragam.

Rekonstruksi aman:

1. Majukan alasan positif sebagai kalimat utama.
2. Tempatkan pembatasan sebagai klausa setelah pernyataan positif, bukan sebagai cetakan `bukan X, melainkan Y`.
3. Pertahankan pola jika kontras membawa pembeda operasional atau metodologis yang tidak dapat dinyatakan tanpa negasi—misalnya membedakan metrik keselamatan dari metrik performa sebagai kriteria keberhasilan.

Contoh:

- Defensif berulang: *Kebutuhan pengembangan tidak berangkat dari asumsi bahwa arsitektur monolith selalu tidak memadai, melainkan dari kebutuhan Apotek Bisma untuk mengelola proses multicabang secara terpusat.*
- Lebih langsung: *Apotek Bisma memerlukan pengelolaan proses multicabang secara terpusat. Arsitektur monolith yang ada tetap menjadi baseline fungsional; migrasi didorong oleh kebutuhan koordinasi data, bukan oleh asumsi bahwa monolith tidak memadai.*

Contoh yang dipertahankan karena kontras operasional:

- Sah: *Keberhasilan Kondisi C tidak ditentukan hanya oleh latency atau throughput, melainkan terutama oleh tidak ditemukannya oversell, lost update, duplicate effect, untraceable event, dan permanent mismatch.* — Negasi di sini membedakan dua kelompok metrik sebagai kriteria keberhasilan; tanpa kontras ini pembaca dapat salah menilai keberhasilan hanya dari performa.

Jangan menghapus negasi yang membawa batas substansi. Kata `tidak`, `belum`, `tanpa`, `kecuali`, dan `bukan` termasuk elemen terlindungi jika mengubah polaritas atau cakupan.

---

## 10. Pembeda Tanpa Sumbu

Jika paragraf menyatakan `berbeda`, `lebih khusus`, `lebih luas`, `lebih komprehensif`, `ruang lingkup berbeda`, atau `konteks lebih spesifik`, harus tersedia sumbu pembeda yang dapat diverifikasi.

Sumbu yang sah:

- objek atau unit analisis;
- populasi, lokasi, atau periode;
- metode, arsitektur, algoritma, atau instrumen;
- kondisi eksperimen atau skenario;
- skala, beban, dataset, atau konfigurasi;
- metrik evaluasi;
- jenis data atau sumber.

Contoh:

- Kurang efektif: *Penelitian ini memiliki fokus yang lebih khusus dibandingkan penelitian terdahulu.*
- Lebih informatif: *Penelitian ini membatasi pengujian pada konsistensi transaksi lintas layanan saat terjadi gangguan jaringan.*

Kalimat kedua hanya sah jika batas tersebut memang tersedia. Jangan menciptakan kesenjangan pustaka untuk mengisi sumbu yang tidak ada.

---

## 11. Klaim Evaluatif Dekoratif

Tinjau adjektiva seperti `efektif`, `efisien`, `optimal`, `komprehensif`, `signifikan`, `strategis`, `robust`, `andal`, dan `aman`. Kata-kata ini sah jika terikat pada definisi operasional, metrik, pembanding, kondisi, bukti, atau gaya selingkung.

Perlakuan aman:

- pada proposal, ubah klaim menjadi sasaran evaluasi jika hasil belum tersedia;
- pada metode, sebut metrik dan prosedur, bukan hasil;
- pada hasil, ikat klaim dengan angka, kondisi, tabel, atau sumber;
- pada pembahasan, turunkan kadar klaim jika bukti hanya indikatif.

Jangan menganggap nama teknologi sebagai bukti. Penggunaan EDA, Saga, indeks, caching, atau HTTPS tidak otomatis membuktikan skalabilitas, konsistensi, efisiensi, atau keamanan.

---

## 12. Kalibrasi Suara Mahasiswa S1 Teknik Informatika

Gunakan ragam akademik jernih-presisi dengan tingkat kematangan wajar untuk skripsi S1 Teknik Informatika. Tujuannya bukan menambahkan kesalahan buatan, melainkan mencegah revisi menjadi terlalu editorial, terlalu abstrak, atau terlalu matang dibanding sumber dan konteks skripsi. Teks akhir harus tetap dapat dipertanggungjawabkan saat sidang: jelas bagi penguji, cukup formal, teknisnya terlacak, tetapi tidak berubah menjadi prosa riset senior yang berlebihan.

Gunakan [contoh-uji-retoris-s1-ti.md](contoh-uji-retoris-s1-ti.md) sebagai bank contoh untuk membedakan teks yang terlalu formulaik, wajar S1 TI, terlalu profesional, dan rusak makna.

### A. Ciri yang Wajar Dipertahankan

| Ciri | Boleh Dipertahankan Jika | Risiko Jika Dipoles Berlebihan |
| :--- | :--- | :--- |
| `penelitian ini`, `sistem ini`, `aplikasi ini` | tidak muncul berantai dan membantu rujukan | teks menjadi terlalu abstrak atau kehilangan subjek yang mudah dilacak |
| `sistem`, `aplikasi`, `data`, `fitur`, `pengujian`, `hasil`, `pengguna` | mengacu pada konsep inti yang sama | sinonim bergilir membuat acuan tidak stabil |
| kalimat prosedural | menjelaskan urutan metode, perancangan, implementasi, atau pengujian | urutan kerja menjadi kabur karena dipaksa menjadi prosa analitis |
| pasif ringkas | prosedur atau objek menjadi fokus | semua kalimat menjadi aktif dan tidak sesuai gaya skripsi |
| transisi eksplisit sesekali | membantu alur Bab 1-5 | hubungan antarkalimat menjadi terlalu implisit bagi pembaca skripsi |
| pembahasan dekat dengan hasil uji | data yang tersedia memang sederhana | interpretasi menjadi terlalu teoretis atau mengarang mekanisme |

Revisi tidak perlu membuat semua kalimat sangat padat, sangat elegan, atau penuh istilah konseptual. Untuk skripsi S1 TI, bentuk seperti *Pengujian dilakukan untuk mengetahui...*, *Sistem dirancang untuk...*, atau *Hasil pengujian menunjukkan...* masih wajar jika tidak berulang secara mekanis dan tetap menyebut objek, kondisi, atau skenario yang jelas.

### B. Batas Atas Kematangan Gaya

Tinjau revisi yang menaikkan bahasa sumber menjadi terlalu abstrak. Istilah seperti `implikasi`, `inferensi`, `konstruksi analitis`, `relasi semantis`, `validitas eksternal`, `kerangka epistemik`, atau `mekanisme konseptual` jangan masuk ke naskah final S1 TI kecuali memang diperlukan oleh sumber, teori, atau pembahasan.

Prioritaskan kosakata yang dekat dengan pekerjaan skripsi TI:

- sistem, aplikasi, pengguna, admin, data, transaksi, fitur, halaman, layanan, basis data;
- kebutuhan, perancangan, implementasi, pengujian, skenario, hasil, kesimpulan;
- metode, algoritma, framework, endpoint, event, tabel, konfigurasi, metrik jika memang tersedia.

Contoh kalibrasi:

- Terlalu matang: *Temuan ini mengindikasikan implikasi arsitektural terhadap stabilitas mekanisme sinkronisasi dalam distribusi data.*
- Lebih wajar S1 TI: *Hasil pengujian menunjukkan bahwa mekanisme sinkronisasi membantu menjaga kesesuaian data pada skenario yang diuji.*

Kalimat kedua tetap harus diturunkan lagi jika sumber hanya menunjukkan sebagian skenario atau belum mengukur `kesesuaian data` secara langsung.

### C. Bab Skripsi dan Fungsi Retorisnya

Audit residu harus membaca fungsi bab, bukan hanya pola kata.

| Bagian Skripsi S1 TI | Bentuk yang Wajar | Tinjau Jika |
| :--- | :--- | :--- |
| Bab 1 Latar Belakang | `penelitian ini bertujuan`, `sistem dibutuhkan`, `permasalahan yang terjadi` | masalah terlalu umum, manfaat promosi, tujuan tidak operasional |
| Bab 2 Kajian Pustaka | perbandingan objek, metode, fitur, dataset, atau hasil | hanya menyebut `lebih khusus/berbeda` tanpa sumbu |
| Bab 3 Metode/Perancangan | `sistem dirancang`, `data dikumpulkan`, `pengujian dilakukan` | urutan, aktor, input, output, atau kondisi tidak jelas |
| Bab 4 Implementasi/Pengujian | `hasil pengujian menunjukkan`, `fitur berjalan sesuai skenario` | klaim `efektif/optimal/andal` tidak punya metrik atau skenario |
| Bab 5 Kesimpulan/Saran | jawaban tujuan, keterbatasan, saran langsung | menambah hasil baru atau rekomendasi terlalu luas |

Jangan menandai frasa yang lazim pada bab tertentu hanya karena tampak formulaik. Frasa tersebut perlu direvisi jika muncul berantai, tidak membawa fungsi, menunda muatan utama, atau menaikkan klaim.

### D. Stabilitas Istilah Inti S1 TI

Untuk skripsi S1 TI, pengulangan istilah inti lebih aman daripada sinonim bergilir. Pilih satu istilah untuk satu acuan dan pertahankan.

| Acuan | Stabilkan | Hindari Jika Mengacu pada Hal yang Sama |
| :--- | :--- | :--- |
| perangkat lunak yang dibuat | `sistem` atau `aplikasi` sesuai sumber | berganti menjadi `platform`, `solusi`, `mekanisme`, `ekosistem` |
| informasi yang diolah | `data` | berganti menjadi `informasi`, `rekaman`, `entitas` tanpa fungsi |
| proses validasi | `pengujian` | berganti menjadi `evaluasi`, `validasi`, `asesmen` tanpa beda makna |
| keluaran uji | `hasil pengujian` | berganti menjadi `temuan empiris` jika sumber sederhana |
| pengguna sistem | `pengguna`, `admin`, `petugas` | berganti menjadi `aktor`, `subjek`, `entitas pengguna` tanpa kebutuhan |

Sinonim boleh dipakai jika benar-benar membedakan konsep. Misalnya, `validasi` berbeda dari `pengujian` jika yang dimaksud adalah pemeriksaan input, bukan uji sistem.

### E. Tiga Bentuk Revisi yang Harus Dibedakan

| Status | Contoh | Keputusan |
| :--- | :--- | :--- |
| Terlalu formulaik | *Pelaksanaan pengujian dilakukan untuk melakukan pengecekan terhadap proses sistem.* | Perbaiki pusat tindakan dan objek |
| Wajar S1 TI | *Pengujian dilakukan untuk mengetahui apakah sistem mencatat transaksi dengan benar.* | Pertahankan atau perjelas skenario jika perlu |
| Terlalu profesional | *Evaluasi fungsional memverifikasi kesesuaian perilaku sistem terhadap spesifikasi transaksi pada kondisi operasional terkontrol.* | Turunkan jika sumber/sampel suara penulis lebih sederhana |

Kalibrasi S1 TI bukan izin untuk mempertahankan klaim kabur, manfaat promosi, atau kesalahan logika. Revisi tetap harus menjaga kesetiaan, bukti, istilah teknis, dan keterbacaan.

### F. Gerbang Kewajaran S1 TI

Sebelum menerima revisi untuk skripsi S1 TI, pastikan:

- [ ] kalimat final masih dekat dengan objek, fitur, metode, pengujian, hasil, atau batas penelitian;
- [ ] tidak ada istilah meta-akademik tingkat lanjut yang masuk tanpa kebutuhan;
- [ ] pengulangan istilah inti dipertahankan jika membantu konsistensi;
- [ ] prosedur metode/perancangan tetap mudah diikuti secara berurutan;
- [ ] klaim hasil tidak lebih kuat daripada skenario, metrik, tabel, atau data yang tersedia;
- [ ] suara akhir tidak jauh lebih megah, padat, atau abstrak daripada sumber dan sampel penulis.

---

## 13. Gerbang Penerimaan Retoris

Revisi diterima dari sisi retoris apabila seluruh syarat berikut terpenuhi:

- [ ] Makna dasar, batas masalah, angka, sitasi, dan konteks teknis tetap identik.
- [ ] Tidak ada istilah teknis, nama metode, label, endpoint, event, variabel, atau konfigurasi yang diganti secara sepihak.
- [ ] Tindakan utama, objek, kondisi, dan bukti dapat dikenali tanpa bingkai berlebihan.
- [ ] Variasi struktur muncul karena fungsi kalimat berbeda, bukan karena pengacakan sinonim atau panjang kalimat.
- [ ] Paragraf tidak portabel ke topik lain setelah istilah bidang diganti secara mental.
- [ ] Rujukan `ini/tersebut/hal ini` memiliki anteseden tunggal dan dekat.
- [ ] Konjungsi sebab, akibat, kontras, dan simpulan sesuai relasi yang dibangun.
- [ ] Klaim evaluatif terikat pada bukti atau diturunkan kadarnya.
- [ ] Pembaca sasaran dapat membaca teks lisan tanpa tersendat akibat tumpukan frasa nominal, tetapi pakar masih dapat mengenali rincian wajib.
- [ ] Untuk skripsi S1 TI, gaya akhir tetap formal, prosedural, dan wajar; tidak terlalu generik, tidak terlalu promosi, dan tidak terlalu over-polished.

Jika revisi retoris membuat teks lebih lancar tetapi mengubah proposisi, statusnya FAIL. Jika sinyal residu terdeteksi tetapi bentuk tersebut diperlukan oleh metode, istilah teknis, atau gaya selingkung, statusnya INFO atau PASS sesuai konteks.
