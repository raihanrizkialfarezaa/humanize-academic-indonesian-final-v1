# Ragam akademik untuk Informatika dan rekayasa perangkat lunak

## Daftar isi

1. Tujuan dan batas
2. Kontrak pembaca ganda
3. Ledger teknis dan asal-usul detail
4. Peta isi teknis
5. Rekonstruksi berdasarkan bagian naskah
6. Penjelasan komponen, alur, dan kegagalan
7. Mekanisme keandalan tanpa klaim berlebih
8. Klaim kinerja dan bukti
9. Istilah, format, dan konsistensi padanan
10. Suara impersonal yang tetap jelas
11. Audit dari sudut pandang penguji
12. Gerbang penerimaan

## 1. Tujuan dan batas

Gunakan referensi ini untuk skripsi, paper, proposal, laporan eksperimen, dan dokumen akademik yang membahas perangkat lunak, arsitektur sistem, basis data, jaringan, algoritma, kecerdasan buatan, kode, atau evaluasi kinerja.

Sasaran penyuntingan ialah membuat pembaca memahami:

1. masalah atau pertanyaan teknis yang ditangani;
2. komponen, mekanisme, atau prosedur yang digunakan;
3. kondisi berlakunya penjelasan;
4. bukti yang mendukung klaim;
5. batas inferensi dan detail yang masih perlu diverifikasi.

Pertahankan identitas teknis. Jangan mengganti nama pola, protokol, algoritma, metrik, event, endpoint, fungsi, variabel, atau konfigurasi dengan istilah umum yang menghapus perbedaannya. Jangan pula menambahkan rincian teknis agar tulisan tampak konkret.

## 2. Kontrak pembaca ganda

Untuk skripsi S1 Informatika, gunakan dua lapis pembaca secara bersamaan:

- **audiens seminar lintas subbidang** harus dapat mengikuti masalah, alur sistem, alasan evaluasi, dan arti hasil;
- **penguji teknis** harus tetap dapat menelusuri komponen, urutan, parameter, kondisi uji, metrik, serta batas kesimpulan.

Gunakan kalimat orientasi sebelum kepadatan teknis jika konteks belum tersedia. Setelah orientasi, pertahankan rincian yang diperlukan untuk menilai desain atau mereplikasi eksperimen. Jangan mengulang definisi umum pada setiap bagian.

Uji pembaca ganda:

- pembaca lintas subbidang dapat menjelaskan apa yang terjadi dan mengapa hal itu diperiksa;
- penguji teknis dapat menunjukkan komponen yang bertindak, data yang berubah, kondisi kegagalan, dan bukti yang dipakai.

Jika salah satu uji gagal, perbaiki orientasi atau pulihkan rincian. Jangan menebus kekurangan dengan kalimat promosi.

## 3. Ledger teknis dan asal-usul detail

Sebelum menyunting, catat setiap detail teknis beserta asalnya.

| Jenis detail | Contoh | Yang harus dikunci |
| --- | --- | --- |
| konteks sistem | jumlah cabang, peran pengguna, proses bisnis | pelaku, lokasi proses, urutan, dan batas sistem |
| arsitektur | monolit, EDA, mikroservis | unit pembanding, tanggung jawab komponen, pola komunikasi |
| mekanisme | OCC, Saga, *transactional outbox* | fungsi, pemicu, perubahan status, kegagalan yang ditangani |
| antarmuka | endpoint, event, webhook, skema pesan | ejaan, kapitalisasi, arah komunikasi, payload yang disebut |
| konfigurasi | versi, *timeout*, jumlah *retry*, isolasi transaksi | nilai, satuan, cakupan, dan kondisi penggunaan |
| eksperimen | beban, skenario, pengulangan, injeksi gangguan | unit analisis, urutan, kontrol, dan variabel perancu |
| hasil | latensi, *throughput*, error rate, inkonsistensi | metrik, angka, arah, pembanding, kondisi, dan sumber bukti |

Gunakan tiga status asal-usul:

- `TERSEDIA`: detail hadir pada naskah, kode, data, tabel, sumber, atau keterangan pengguna;
- `TERVERIFIKASI`: detail tidak tertulis pada paragraf, tetapi dapat dipastikan dari bahan yang memang diberikan dan relevan;
- `BELUM TERSEDIA`: detail mungkin berguna, tetapi tidak boleh dimasukkan ke naskah tanpa konfirmasi.

Jangan mengubah `BELUM TERSEDIA` menjadi fakta. Versi PostgreSQL, nama kolom, endpoint, nama event, jumlah *retry*, durasi *timeout*, topologi, dan spesifikasi perangkat tidak boleh dibuat untuk memberi kesan teknis. Tempatkan kebutuhan tersebut sebagai catatan verifikasi di luar naskah.

## 4. Peta isi teknis

Bedakan lima jenis pernyataan sebelum merekonstruksi kalimat.

| Jenis | Pertanyaan | Contoh fungsi |
| --- | --- | --- |
| tujuan | Apa yang hendak diketahui atau ditangani? | menilai konsistensi stok saat transaksi bersamaan |
| mekanisme | Bagaimana komponen bekerja? | versi data diperiksa sebelum pembaruan disimpan |
| konfigurasi | Dalam susunan atau nilai apa mekanisme dijalankan? | jumlah layanan, versi perangkat lunak, ambang, dan beban |
| observasi | Apa yang tercatat dari pengujian? | dua konflik pembaruan pada skenario tertentu |
| interpretasi | Apa arti observasi dan seberapa kuat dasarnya? | pola konsisten dengan fungsi deteksi konflik |

Jangan melebur kelimanya. Konfigurasi tidak membuktikan hasil, mekanisme yang dirancang tidak sama dengan mekanisme yang berhasil, dan observasi bersama tidak otomatis menunjukkan sebab.

Untuk paragraf teknis, petakan sekurang-kurangnya:

1. objek atau keadaan awal;
2. tindakan atau perubahan status;
3. komponen yang bertanggung jawab;
4. keluaran atau keadaan akhir;
5. kondisi normal, gangguan, atau pengecualian;
6. bukti atau cara pengukuran jika paragraf membuat klaim evaluatif.

## 5. Rekonstruksi berdasarkan bagian naskah

### 5.1 Pendahuluan

Turunkan masalah dari proses yang dapat diamati, bukan dari daftar teknologi. Susunan yang lazim:

1. proses atau objek yang diteliti;
2. masalah operasional atau teknis;
3. konsekuensi yang tersedia dalam sumber;
4. pengetahuan atau solusi terdahulu;
5. batas yang dapat diverifikasi;
6. tujuan dan sumbu kontribusi penelitian.

Jangan membuka dengan klaim bahwa teknologi berkembang pesat jika kalimat itu tidak menurunkan masalah. Jangan menyebut arsitektur sebagai solusi sebelum masalah dan tolok ukurnya jelas.

### 5.2 Kajian pustaka

Bandingkan studi pada sumbu yang sama: objek, arsitektur, kondisi, mekanisme, skala, metrik, atau hasil. Bedakan:

- `menerapkan` dari `mengevaluasi`;
- `mendemonstrasikan` dari `membuktikan`;
- `tidak dibahas` dari `gagal ditangani`;
- `berbeda runtime` dari `berbeda arsitektur`.

Jangan menyebut studi terdahulu sebagai landasan secara umum. Nyatakan konsep, artefak, metode, atau temuan yang benar-benar diteruskan.

### 5.3 Metode dan perancangan

Susun berdasarkan dependensi prosedural:

1. tujuan langkah;
2. unit atau komponen yang terlibat;
3. konfigurasi dan kondisi awal;
4. tindakan atau stimulus;
5. data yang dicatat;
6. metrik dan cara hitung;
7. kriteria interpretasi;
8. pengendalian variabel perancu dan batas desain.

Pertahankan rincian replikasi. Jangan menambahkan alasan pemilihan metode, klaim kesetaraan lingkungan, atau asumsi kontrol yang tidak tersedia.

### 5.4 Hasil

Dahulukan pertanyaan atau pola yang dijawab, lalu angka dan kondisi uji. Setiap klaim perbandingan idealnya memuat:

- metrik;
- arah dan besar perbedaan;
- pembanding;
- tingkat beban atau skenario;
- rujukan tabel, gambar, log, atau data jika tersedia.

Laporkan hasil nol, anomali, dan kegagalan. Jangan mengubah `tidak ditemukan perbedaan` menjadi `kinerja setara` tanpa dasar kesetaraan.

### 5.5 Pembahasan

Pisahkan urutan berikut:

1. observasi;
2. hubungan dengan mekanisme yang memang diuji;
3. penjelasan alternatif atau variabel perancu;
4. perbandingan dengan studi terdahulu;
5. implikasi dan batas generalisasi.

Gunakan `dapat menjelaskan`, `konsisten dengan`, atau `diduga berkaitan` jika mekanisme belum diisolasi. Jangan mengatribusikan selisih kinerja hanya pada arsitektur ketika runtime, framework, basis data, konfigurasi, atau implementasi juga berbeda.

### 5.6 Proposal dibanding laporan hasil

Pada proposal, rumuskan performa sebagai sasaran atau pertanyaan:

> Pengujian akan menilai apakah Kondisi C menurunkan jumlah inkonsistensi stok dibandingkan Kondisi A dan B.

Jangan menulis hasil yang belum diperoleh:

> Kondisi C menurunkan inkonsistensi stok dan meningkatkan keandalan sistem.

Pada laporan hasil, gunakan bentuk observasional yang terikat pada angka dan kondisi yang tersedia.

## 6. Penjelasan komponen, alur, dan kegagalan

Gunakan unit berikut untuk menjelaskan interaksi sistem:

1. **pemicu atau masukan**;
2. **komponen yang menerima**;
3. **tindakan atau validasi**;
4. **perubahan data/status**;
5. **keluaran, respons, atau event**;
6. **jalur gagal dan pemulihan**, jika relevan.

Satu kalimat sebaiknya memuat satu perpindahan utama atau satu hubungan sebab yang dapat dipertanggungjawabkan. Jika beberapa layanan berinteraksi, gunakan urutan kronologis atau dependensi. Jangan menyembunyikan lompatan status dengan `kemudian diproses` atau `hal ini diteruskan` tanpa menyebut pelaku dan objek.

Untuk alur normal dan alur gagal, nyatakan titik percabangannya. Jangan menggambarkan kompensasi seolah-olah transaksi awal tidak pernah terjadi; sebut tindakan pemulihan yang benar-benar tersedia pada sumber.

## 7. Mekanisme keandalan tanpa klaim berlebih

Nama mekanisme tidak boleh diperlakukan sebagai jaminan otomatis. Pertahankan fungsi yang didukung sumber dan batasi implikasinya.

| Mekanisme | Fungsi yang lazim dijelaskan | Klaim yang tidak otomatis sah |
| --- | --- | --- |
| OCC | mendeteksi konflik berdasarkan versi/kondisi pembaruan | menghapus semua *race condition* |
| Saga | mengoordinasikan langkah dan kompensasi lintas transaksi | memberikan atomicity ACID global |
| *transactional outbox* | mencatat perubahan domain dan pesan keluar dalam transaksi lokal | menjamin pemrosesan tepat sekali pada seluruh konsumen |
| idempotensi | mencegah efek ulang untuk permintaan/pesan yang dikenali sama | membuktikan tidak ada pesan hilang |
| *retry* | mengulang operasi sesuai kebijakan | selalu memulihkan kegagalan tanpa efek samping |
| *circuit breaker* | membatasi panggilan ketika kegagalan memenuhi kondisi | meningkatkan ketersediaan pada semua skenario |

Tabel ini hanya membantu menguji kadar klaim. Jangan memasukkan fungsi atau batas tersebut ke naskah jika mekanismenya tidak tersedia atau konteks implementasinya berbeda.

## 8. Klaim kinerja dan bukti

Klaim seperti `lebih cepat`, `akurat`, `stabil`, `aman`, `andal`, `efektif`, `efisien`, `optimal`, atau `robust` memerlukan operasionalisasi. Periksa unsur berikut:

| Unsur | Pertanyaan |
| --- | --- |
| metrik | Apa yang diukur: latensi p95, *throughput*, error rate, inkonsistensi, atau ukuran lain? |
| pembanding | Lebih baik daripada kondisi, baseline, atau versi apa? |
| kondisi | Pada beban, skenario, dataset, perangkat, dan durasi apa? |
| nilai | Berapa besar perbedaan dan apa satuannya? |
| ketidakpastian | Apakah ada variasi, interval, ukuran efek, atau uji yang relevan? |
| sumber | Apakah klaim berasal dari data, tabel, log, kode, atau sitasi? |

Jika unsur belum tersedia:

- pada proposal, ubah klaim menjadi sasaran evaluasi;
- pada metode, nyatakan metrik dan prosedur tanpa mengumumkan hasil;
- pada hasil, pertahankan observasi yang tersedia dan tandai kekurangannya;
- pada pembahasan, turunkan kadar klaim atau beri catatan verifikasi.

`Aman` tidak cukup dibuktikan oleh tidak adanya galat pada pengujian fungsional. `Stabil` tidak sama dengan satu nilai rata-rata. `Efisien` tidak dapat disimpulkan hanya dari latensi jika biaya sumber daya tidak diukur.

## 9. Istilah, format, dan konsistensi padanan

Ikuti gaya selingkung dan EYD untuk prosa, lalu pertahankan identitas artefak teknis.

| Kategori | Perlakuan umum | Contoh |
| --- | --- | --- |
| istilah Indonesia baku/serapan | huruf biasa | basis data, algoritma, latensi |
| kata atau ungkapan asing yang belum diserap | cetak miring jika gaya selingkung tidak mengatur lain | *transactional outbox*, *race condition* |
| nama resmi produk, bahasa, organisasi, standar | pertahankan ejaan resmi; tidak otomatis dimiringkan | PostgreSQL, Node.js, JavaScript, ISO 25010 |
| singkatan | definisikan pada kemunculan penting pertama | Event-Driven Architecture (EDA) |
| identifier dan literal kode | format kode | `user_id`, `PaymentFailed`, `POST /payments` |
| nama metrik/notasi | ikuti konvensi bidang | latensi p95, nilai *p*, Kendall’s W |

Jangan memiringkan semua unsur Inggris secara buta. Nama produk, merek, bahasa pemrograman, kode, URL, endpoint, dan identifier mengikuti identitas resminya. Jangan pula memakai cetak miring, tanda kurung, titik koma, angka, atau simbol sebagai cara mengubah keputusan detektor.

Pilih satu padanan untuk satu konsep. Jangan berganti antara `request` dan `permintaan`, `fault` dan `gangguan`, atau `flow` dan `alur` tanpa fungsi. Pertahankan bentuk Inggris jika merupakan label kode atau istilah resmi; gunakan padanan Indonesia untuk uraian umum.

## 10. Suara impersonal yang tetap jelas

Profil impersonal bukan kewajiban membuat semua kalimat pasif. Pilih subjek proses atau objek teknis ketika pelaku manusia tidak perlu disebut.

| Bentuk berat | Bentuk lebih langsung |
| --- | --- |
| Pelaksanaan pengujian dilakukan dengan menggunakan k6. | Pengujian menggunakan k6. |
| Proses penyimpanan data dilakukan oleh layanan stok. | Layanan stok menyimpan data. |
| Perancangan sistem dilakukan menggunakan EDA. | Sistem dirancang dengan EDA. |
| Dilakukan pengiriman event setelah transaksi berhasil. | Layanan pembayaran mengirim event setelah transaksi berhasil. |

Gunakan pasif jika objek atau prosedur memang menjadi topik:

> Setiap skenario diuji 30 kali pada tingkat beban yang sama.

Gunakan aktif nonpersonal jika pelaku teknis penting:

> Worker membaca pesan dari antrean dan memperbarui status transaksi.

Dalam profil impersonal, hindari `saya`, `kami`, `penulis`, dan `peneliti` jika gaya selingkung melarangnya. Jangan menghapus pelaku teknis yang diperlukan untuk memahami tanggung jawab atau alur.

## 11. Audit dari sudut pandang penguji

Uji setiap bagian dengan pertanyaan yang mungkin diajukan penguji:

- Apa objek yang berubah dan siapa yang mengubahnya?
- Istilah ini menyebut tujuan, mekanisme, konfigurasi, atau hasil?
- Bagaimana klaim ini diukur dan di mana buktinya?
- Apa baseline atau kondisi pembandingnya?
- Apakah angka mewakili rata-rata, persentil, proporsi, atau jumlah kasus?
- Apa unit analisis dan jumlah pengulangannya?
- Apakah variabel perancu diisolasi atau hanya diakui?
- Apakah mekanisme benar-benar diuji saat gagal, atau hanya dijelaskan dari desain?
- Apakah sitasi mendukung penerapan, efektivitas, atau hanya definisi?
- Sejauh mana hasil dapat digeneralisasi di luar konfigurasi uji?
- Detail mana yang berasal dari kode/data dan mana yang masih asumsi?

Jangan mengarang jawaban. Jika naskah belum menyediakan dasar, pertahankan klaim yang lebih sempit dan buat catatan verifikasi di luar naskah.

## 12. Gerbang penerimaan

Terima revisi Informatika hanya jika:

1. masalah, tujuan, mekanisme, konfigurasi, observasi, dan interpretasi tidak tertukar;
2. setiap detail teknis dapat ditelusuri ke bahan pengguna atau ditandai untuk verifikasi;
3. komponen, alur, perubahan status, dan jalur gagal dapat diikuti tanpa rujukan kabur;
4. istilah resmi, identifier, parameter, versi, angka, dan label tetap benar;
5. klaim performa terikat pada metrik, pembanding, kondisi, nilai, atau dirumuskan sebagai sasaran proposal;
6. pembaca lintas subbidang memperoleh orientasi tanpa kehilangan rincian bagi penguji;
7. bentuk aktif, pasif, dan impersonal dipilih berdasarkan fokus, bukan cetakan;
8. tidak ada fakta, konfigurasi, mekanisme, jaminan, atau hasil baru;
9. penulis dapat menjelaskan alasan, data, dan batas setiap klaim pada seminar atau ujian.

Jika satu syarat kritis belum terpenuhi, pertahankan rumusan sumber atau beri catatan verifikasi. Jangan menutupi kekurangan bukti dengan istilah teknis, bahasa megah, atau kepastian yang lebih tinggi.
