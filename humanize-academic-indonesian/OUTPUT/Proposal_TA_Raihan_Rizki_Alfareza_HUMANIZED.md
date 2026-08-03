**IMPLEMENTASI TRANSACTIONAL OUTBOX DAN OPTIMISTIC CONCURRENCY CONTROL PADA MIGRASI MONOLITH KE EVENT-DRIVEN MICROSERVICES BERBASIS ASYNCHRONOUS I/O UNTUK MENJAGA KONSISTENSI DATA (STUDI KASUS: SISTEM POS DAN ERP APOTEK RETAIL, APOTEK BISMA, KABUPATEN MOJOKERTO)** 

# **PROPOSAL TUGAS AKHIR** 

**BENTUK: SKRIPSI** 

Oleh 

**Raihan Rizki Alfareza** NIM 23051204067 

[Lambang UNESA] 

## **UNIVERSITAS NEGERI SURABAYA FAKULTAS TEKNIK PROGRAM STUDI S1 TEKNIK INFORMATIKA** 

**2026** 

1 

## **HALAMAN PERSETUJUAN PROPOSAL TUGAS AKHIR** 

|**Keterangan**|**Isi**|
|---|---|
|Nama Mahasiswa|Raihan Rizki Alfareza|
|NIM|23051204067|
|Program Studi|S1 Teknik Informatika|
|Judul Penelitian|Implementasi Transactional<br>Outbox dan Optimistic<br>Concurrency Control pada<br>Migrasi Monolith ke Event-<br>Driven Microservices Berbasis<br>Asynchronous I/O untuk<br>Menjaga Konsistensi Data (Studi<br>Kasus: Sistem POS dan ERP<br>Apotek Retail, Apotek Bisma,<br>Kabupaten Mojokerto)|
|Proposal ini disusun|untuk diajukan dalam proses|
|bimbingan dan seminar<br>S1 Teknik Informatika,|proposal Tugas Akhir Program Studi<br>Fakultas Teknik, Universitas Negeri|
|Surabaya.||



Mojokerto/Surabaya, [tanggal persetujuan] Pembimbing, 

**I Made Suartana, S.Kom., M.Kom.** NIP [PERLU VERIFIKASI] 

2 

## **DAFTAR ISI** 

[Perbarui daftar isi otomatis di Microsoft Word] 

3 

## **BAB I PENDAHULUAN** 

## **A. Latar Belakang** 

Apotek Bisma mengoperasikan tiga cabang dan satu gudang pusat. Menurut keterangan awal pemilik, dua pegawai menangani tiap cabang, sementara empat pegawai bekerja di gudang. Masing-masing cabang menjalankan aplikasi Laravel 8 secara lokal dengan basis data tersendiri; pencatatan gudang masih menggunakan spreadsheet. Akibatnya, data transaksi, stok, dan laporan belum saling terhubung. Petugas khusus baru melakukan rekonsiliasi antarcabang dan gudang di akhir bulan, sehingga selisih pencatatan dapat terlambat diketahui berminggu-minggu. 

Apotek Bisma membutuhkan satu sistem terpusat yang mengoordinasikan operasional ketiga cabang dan gudang. Gudang perlu mengetahui penjualan dan saldo stok per lokasi agar dapat menentukan jadwal pengisian ulang. Cabang memerlukan proses penjualan, reservasi, penerimaan transfer, dan pembayaran yang tetap tercatat berdasarkan lokasinya. Kanal transaksi juga bertambah — kasir, Self-Order Kiosk, Midtrans, dan QRIS statis — sehingga koordinasi data yang sebelumnya cukup berjalan di satu proses lokal perlu menjangkau beberapa titik sekaligus. Arsitektur monolith yang ada tetap dijadikan acuan fungsional; perpindahan ke arsitektur baru didorong oleh kebutuhan koordinasi data lintas cabang dan gudang. 

4 

Pada monolith terpusat, perubahan beberapa tabel masih dapat diselesaikan melalui satu transaksi basis data. Setelah domain Sales, Inventory, dan Payment dipisah menjadi layanan dengan basis data masing-masing, transaksi lintas layanan kehilangan rollback ACID global. Jika data bisnis sudah tersimpan tetapi event gagal terkirim, muncul masalah dual-write. Event yang terkirim lebih dari sekali dapat menghasilkan efek ganda apabila consumer tidak idempoten. Pembaruan stok yang terjadi bersamaan pun berpotensi menimpa satu sama lain atau menjual melebihi ketersediaan. Oleh karena itu, konsistensi pada sistem terdistribusi perlu dijaga melalui transaksi lokal, pertukaran event yang andal, pengendalian konkurensi, dan mekanisme pemulihan (Richardson, 2018; Kleppmann, 2017). 

Transactional Outbox menyimpan perubahan data bisnis dan catatan event dalam satu transaksi lokal; worker kemudian membaca catatan tersebut dan mengirim event ke broker sampai mendapat publisher confirm, sehingga event yang tertunda tetap dapat dikirim ulang (Richardson, t.t.-a). Di sisi penerima, durable inbox menyimpan identitas event yang telah diproses agar pengiriman ulang tidak menimbulkan efek bisnis kedua (Richardson, t.t.-c). Optimistic Concurrency Control (OCC) memanfaatkan atribut version untuk menolak pembaruan yang bertolak dari versi lama. Saga Orchestrator, yang mencatat state dan menentukan langkah lanjutan atau compensation ketika sebagian proses gagal, mengoordinasikan transaksi yang melintasi Sales, Inventory, dan Payment (Richardson, 2018; Richardson, t.t.-b). Gabungan mekanisme tersebut tidak membuat sistem selalu 

5 

konsisten secara instan; yang dirancang ialah agar setiap proses dapat menuju keadaan akhir yang sah dan dapat ditelusuri. 

Rochman dan Suartana (2026) menerapkan event-driven architecture pada sistem manajemen gudang, yang menunjukkan bahwa pendekatan berbasis event relevan untuk aliran persediaan. Fokus penelitian ini berada pada aspek yang berbeda: konsistensi transaksi lintas layanan pada POS/ERP apotek yang memakai database per service, melibatkan pembayaran asinkron, konflik stok, duplicate delivery, dual-write, dan partial failure. Pembedanya bukan pada framework yang dipakai, melainkan pada pengujian gabungan Transactional Outbox, OCC, durable idempotency, Saga orchestration, compensation, retry, dan DLQ yang divalidasi melalui invariant bisnis dan fault injection. 

Agar perbandingan dapat dipertanggungjawabkan, tiga kondisi yang setara secara fungsional disusun. Kondisi A berupa monolith terpusat terkontrol berbasis Laravel 8 dengan satu basis data MySQL. Kondisi B berupa event-driven microservices berbasis NestJS dengan database per service tetapi tanpa mekanisme keandalan lengkap. Kondisi C menambahkan Outbox-Inbox, OCC, durable idempotency, Saga Orchestrator, compensation, retry, dan DLQ di atas Kondisi B. Perbedaan runtime Laravel dan Node.js diperlakukan sebagai faktor perancu; hasil performa tidak akan diatribusikan pada satu pola arsitektur saja. Penilaian utama diarahkan pada kebenaran data, kemampuan pemulihan, konvergensi, dan biaya teknis mekanisme proteksi. 

6 

Empat use case menjadi sasaran pengujian: penjualan konkuren melalui POS dan kiosk, restock yang berdekatan dengan penjualan, pembayaran Midtrans, serta QRIS statis dengan konfirmasi admin. Kondisi C dianggap berhasil bukan semata-mata berdasarkan latency atau throughput, melainkan terutama berdasarkan tidak ditemukannya oversell, lost update, duplicate effect, untraceable event, dan permanent mismatch pada konfigurasi pengujian yang telah dikunci. Klaim penelitian hanya berlaku untuk use case, dataset, beban, fault, dan lingkungan eksperimen yang diuji; bukan untuk menyatakan bahwa microservices selalu lebih unggul daripada monolith. 

## **B. Identifikasi Masalah** 

1. Data transaksi, stok, dan laporan pada tiga cabang serta gudang belum dikelola dalam satu sistem multicabang terpusat sehingga rekonsiliasi masih dilakukan secara periodik. 

2. Pemisahan Sales, Inventory, dan Payment ke database per service menghilangkan transaksi ACID global untuk proses bisnis lintas domain sehingga muncul risiko partial failure dan ketidakcocokan state antarlayanan. 

3. Publikasi event secara langsung setelah penyimpanan data bisnis memiliki celah dual-write ketika service atau worker gagal pada titik di antara kedua operasi. 

4. Redelivery event atau webhook dapat menimbulkan duplicate effect apabila identitas pesan yang telah diproses tidak disimpan secara durable. 

7 

5. Transaksi penjualan konkuren pada produk dan lokasi yang sama dapat menghasilkan lost update atau oversell apabila konflik pembaruan stok tidak dikendalikan. 

6. Belum tersedia bukti terkontrol pada konteks Apotek Bisma mengenai trade-off konsistensi, pemulihan, konvergensi, latency, throughput, dan resource antara monolith terpusat, naïve microservices, dan robust microservices. 

## **C. Batasan Masalah** 

7. Objek studi kasus dibatasi pada proses POS/ERP Apotek Bisma yang melibatkan tiga cabang dan satu gudang pusat. 

8. Domain layanan dibatasi pada Sales, Inventory, Payment, serta Reporting/Notification sebagai read model; sumber kebenaran transaksi tetap berada pada service pemilik domain. 

9. Stok dimodelkan per pasangan product_id dan location_id dengan on_hand, reserved, available = on_hand - reserved, serta version. Kesesuaian terhadap stok fisik hanya dapat dinilai melalui stock opname dan berada di luar eksperimen perangkat lunak. 

10. Use case eksperimen dibatasi pada UC-1 penjualan konkuren POS-kiosk, UC-2 restock berdekatan dengan penjualan, UC-3 pembayaran Midtrans, dan UC-4 QRIS statis dengan konfirmasi admin. 

11. Aspek batch/lot, FEFO, resep, obat keras, recall, dan otorisasi klinis apoteker tidak menjadi variabel penelitian. 

8 

12. Kondisi A, B, dan C disetarakan pada model data bisnis, endpoint, dataset awal, workload, pola request, serta target luaran. Perbedaan runtime Laravel dan Node.js dicatat sebagai faktor perancu performa. 

13. Fault injection mencakup F1 crash setelah data bisnis tersimpan sebelum event terpublikasi, F2 duplicate event, F3 consumer crash sebelum ACK, F4 broker delay atau webhook terlambat, dan F5 konflik stok konkuren. 

14. Kesimpulan penelitian dibatasi pada konfigurasi, dataset, beban, fault, dan lingkungan eksperimen yang diuji dan tidak digeneralisasi sebagai keunggulan universal microservices. 

## **D. Rumusan Masalah** 

15. Bagaimana merancang migrasi sistem Apotek Bisma menuju sistem terpusat berbasis event-driven microservices yang mendukung stok per lokasi dan transaksi lintas domain? 

16. Bagaimana Transactional Outbox dan OCC, dengan dukungan durable idempotency serta Saga, menjaga konsistensi data ketika terjadi transaksi konkuren dan kegagalan parsial? 

17. Bagaimana perbandingan konsistensi data, kemampuan pemulihan, konvergensi, dan performa antara monolith terpusat, naïve event-driven microservices, dan robust event-driven microservices pada workload serta skenario gangguan yang setara? 

9 

## **E. Tujuan Penelitian** 

18. Merancang artefak migrasi sistem Apotek Bisma menuju sistem terpusat berbasis event-driven microservices dengan pemisahan domain Sales, Inventory, Payment, dan Reporting/Notification serta model stok per lokasi. 

19. Menerapkan dan mengevaluasi Transactional Outbox, OCC, durable idempotency, Saga Orchestrator, compensation, retry, dan DLQ dalam menjaga invariant bisnis pada transaksi konkuren dan partial failure. 

20. Membandingkan tiga kondisi arsitektur pada metrik konsistensi, recovery, convergence lag, latency, throughput, error rate, CPU, dan RAM menggunakan workload, dataset, dan fault yang dikendalikan. 

## **F. Manfaat Penelitian** 

## **1. Manfaat Keilmuan** 

Penelitian ini diharapkan menghasilkan bukti empiris terkontrol tentang perilaku gabungan Outbox, OCC, durable idempotency, dan Saga ketika diterapkan pada transaksi lintas layanan yang melibatkan stok dan pembayaran. Bukti tersebut dapat menjadi rujukan kontekstual bagi pihak lain yang perlu menimbang trade-off antara proteksi konsistensi, kemampuan pemulihan, konvergensi, dan overhead performa pada sistem terdistribusi. 

## **2. Manfaat Praktis** 

Artefak dan hasil evaluasi dapat menjadi dasar teknis bagi Apotek Bisma untuk menentukan strategi migrasi dari beberapa sistem lokal ke pengelolaan multicabang terpusat. Luaran berupa prototipe, test oracle, fault 

10 

injector, skrip rekonsiliasi, dan laporan evaluasi juga dapat membantu proses verifikasi sebelum keputusan implementasi lebih lanjut diambil. 

## **G. Asumsi Penelitian** 

21. Data awal eksperimen, aturan bisnis, dan skenario uji yang telah dikunci dapat direplikasi pada setiap kondisi melalui proses reset state dan seed yang sama. 

22. Jam sistem pada komponen eksperimen berada pada lingkungan yang sama atau tersinkronisasi sehingga pengukuran lag dan recovery dapat dilakukan secara konsisten. 

23. Informasi operasional mengenai jumlah cabang, pegawai, alur gudang, dan rekonsiliasi bulanan masih berstatus keterangan awal pemilik/pengelola dan akan dikonfirmasi melalui catatan wawancara sebelum requirement akhir dikunci. 

11 

## **BAB II KAJIAN PUSTAKA** 

## **A. Kajian Teori** 

## **1. Monolith Terpusat dan Migrasi ke Microservices** 

Monolith terpusat menempatkan seluruh fungsi aplikasi dalam satu unit deployment dan memungkinkan satu transaksi basis data menangani perubahan lintas tabel. Pada penelitian ini, monolith diposisikan sebagai baseline terpusat yang sudah memiliki model stok per lokasi dan fungsi bisnis setara dengan kondisi microservices. Ketika domain dipisah menjadi layanan-layanan yang masing-masing memiliki basis data sendiri, koordinasi lintas layanan tidak lagi dapat bergantung pada transaksi ACID global (Fowler, 2002; Richardson, 2018). 

## **2. Event-Driven Architecture dan Asynchronous I/O** 

Pada event-driven architecture, event merepresentasikan fakta bisnis yang telah terjadi dan memungkinkan komponen bereaksi secara asinkron. Command seperti ReserveStock meminta suatu tindakan dan dapat ditolak; event seperti StockReserved merekam fakta yang sudah terjadi. Dalam implementasi Node.js/NestJS, asynchronous I/O membuat service dapat menangani operasi basis data, broker, webhook, dan WebSocket tanpa menahan thread selama menunggu respons I/O. Sifat ini berkaitan dengan model eksekusi, bukan jaminan konsistensi; 

12 

kebenaran data tetap bergantung pada transaksi lokal, constraint, Outbox, OCC, Inbox, dan Saga. 

## **3. Database per Service dan Konsistensi Data** 

Tiap service memegang data otoritatifnya sendiri. Sales mengelola order dan state Saga; Inventory mengelola saldo dan mutasi stok; Payment mengelola payment attempt beserta status pembayaran; Reporting/Notification hanya menyimpan read model. Pemisahan semacam ini mencegah satu service mengubah basis data service lain secara langsung, tetapi menuntut koordinasi tersendiri ketika satu proses bisnis perlu menyentuh lebih dari satu service. 

## **4. Transactional Outbox** 

Transactional Outbox mencatat perubahan data bisnis bersama event yang akan dikirim dalam satu transaksi lokal. Worker lalu membaca tabel outbox dan mempublikasikan event ke broker sampai mendapat publisher confirm. Dengan cara ini, keadaan ketika data bisnis sudah tersimpan tetapi event belum tercatat akibat crash di tengah proses dual-write dapat dihindari (Richardson, t.t.-a). 

## **5. Durable Inbox dan Idempotency** 

Pada sistem yang menerapkan at-least-once delivery, pesan dapat terkirim lebih dari sekali. Durable inbox menyimpan event_id atau idempotency key yang sudah diproses sehingga consumer mengenali pengiriman ulang dan tidak menjalankan efek bisnis untuk kedua kalinya. Mekanisme ini diperlukan baik untuk event internal maupun webhook pembayaran yang dapat diterima berulang (Richardson, t.t.-c). 

13 

## **6. Optimistic Concurrency Control** 

OCC memanfaatkan nilai version untuk mendeteksi apakah data telah berubah sejak terakhir dibaca. Pembaruan hanya berhasil jika version yang dibawa transaksi masih cocok dengan version yang tersimpan. Apabila version telah berbeda, pembaruan ditolak dan proses perlu membaca ulang state terbaru sebelum mencoba kembali. Pada konteks stok, mekanisme ini menjaga agar pembaruan yang bertolak dari versi lama tidak menimpa mutasi yang lebih baru (Kleppmann, 2017). 

## **7. Saga Orchestration dan Compensation** 

Saga memecah transaksi lintas layanan menjadi rangkaian transaksi lokal. Saga Orchestrator menyimpan state dan menentukan command selanjutnya berdasarkan hasil langkah sebelumnya. Jika satu langkah gagal, compensation menjalankan aksi bisnis untuk memulihkan keadaan — misalnya melepas reservasi stok ketika pembayaran gagal atau kedaluwarsa. Compensation berbeda dari rollback global basis data karena setiap langkah merupakan transaksi lokal yang telah tersimpan (Richardson, 2018; Richardson, t.t.-b). 

## **8. RabbitMQ, Publisher Confirm, ACK, Retry, dan DLQ** 

RabbitMQ berperan sebagai broker pesan. Publisher confirm memberitahu bahwa broker telah menerima pesan, sedangkan consumer ACK dikirim setelah pesan berhasil diproses. Pesan yang gagal diproses dapat dikirim ulang sesuai kebijakan retry; setelah melewati batas percobaan, pesan dipindahkan ke Dead Letter Queue. Event di DLQ masih terlacak, tetapi bukan berarti proses bisnis berhasil — 

14 

pesan tersebut memerlukan replay atau rekonsiliasi (RabbitMQ/Broadcom Inc., t.t.). 

## **9. Model Stok per Lokasi dan Invariant Bisnis** 

Saldo stok dimodelkan melalui on_hand, reserved, dan available = on_hand - reserved untuk setiap pasangan product_id dan location_id. Invariant utama meliputi: available tidak boleh negatif; saldo setelah recovery harus sama dengan test oracle yang dihitung dari stok awal, mutasi masuk, mutasi keluar, dan kompensasi; satu order hanya memiliki satu pembayaran sah dan satu pemotongan stok final; status final tidak boleh kembali ke pending akibat pesan terlambat; dan setiap Saga harus mencapai terminal state yang sah. 

## **10. Fault Injection, Recovery, dan Observability** 

Fault injection menguji perilaku artefak pada titik kegagalan yang ditetapkan secara deterministik. Pengamatan tidak berhenti pada keberhasilan retry, tetapi memeriksa keadaan akhir di seluruh database, outbox, inbox, DLQ, ledger mutasi, dan status Saga berdasarkan correlation_id. Recovery time diukur dari saat fault dihentikan sampai invariant kembali terpenuhi, sedangkan read model lag mengukur jeda antara perubahan pada sumber kebenaran dan pembaruan proyeksi. 

## **11. Design Science Research Methodology** 

Design Science Research Methodology (DSRM) cocok untuk penelitian yang sekaligus menghasilkan dan mengevaluasi artefak. Tahapnya meliputi identifikasi masalah, penetapan tujuan solusi, perancangan dan 

15 

pengembangan, demonstrasi, evaluasi, serta komunikasi (Peffers et al., 2007). Eksperimen A-B-C dalam penelitian ini ditempatkan pada tahap evaluasi artefak, bukan sebagai metode tersendiri di luar DSRM. 

## **B. Penelitian yang Relevan** 

Rochman dan Suartana (2026) membangun sistem manajemen gudang berbasis web dengan event-driven architecture. Studi tersebut menunjukkan bahwa EDA dapat digunakan pada aliran persediaan. Penelitian ini memanfaatkan pijakan tersebut untuk mengarahkan fokus ke masalah yang lebih spesifik: konsistensi transaksi lintas layanan dan perilaku sistem saat terjadi kegagalan. 

|**Aspek**|**Rochman &**<br>**Suartana (2026)**|**Penelitian ini**|
|---|---|---|
|Domain|Manajemen gudang<br>dan aliran stok|POS/ERP apotek:<br>penjualan, reservasi,<br>restock,<br>pembayaran, kiosk|
|Batas sistem|EDA untuk<br>menghubungkan<br>modul sistem<br>gudang|Microservices<br>dengan basis kode<br>dan database<br>terpisah per domain|
|Masalah utama|Pengembangan alur<br>event dan respons<br>sistem|Concurrent update,<br>dual-write, duplicate<br>delivery, partial<br>failure|
|Mekanisme|Event broker|Outbox, durable<br>inbox, OCC, Saga<br>Orchestrator,<br>compensation, retry,|



16 

|||DLQ|
|---|---|---|
|Pembayaran|Bukan skenario<br>utama|Midtrans dan QRIS<br>statis human-in-the-<br>loop diuji eksplisit|
|||Tiga kondisi evolusi,|
|Evaluasi|Fungsionalitas dan<br>performa EDA|fault injection,<br>invariant, recovery,<br>konvergensi,<br>performa|



Kontribusi yang ditargetkan ialah evaluasi terukur terhadap kombinasi mekanisme proteksi pada konteks transaksi apotek. Klaim kebaruan tetap dibatasi pada studi yang telah diperiksa; penelusuran literatur yang lebih luas perlu dilengkapi sebelum klaim state of the art dinyatakan final. 

## **C. Kerangka Berpikir** 

Titik berangkat penelitian ialah kondisi operasional Apotek Bisma yang masih menjalankan aplikasi dan basis data terpisah di setiap cabang, sementara pencatatan gudang belum terintegrasi. Dari kebutuhan sistem terpusat, model stok per lokasi dan pemisahan domain Sales, Inventory, Payment, serta Reporting/Notification diturunkan. Begitu database dipisah per service, risiko baru berupa dual-write, duplicate delivery, konflik stok, dan partial failure muncul. Risiko-risiko tersebut menjadi alasan diterapkannya Transactional Outbox, durable inbox/idempotency, OCC, dan Saga pada Kondisi C. 

Tiga kondisi yang setara secara fungsional kemudian dievaluasi. Kondisi A menyediakan baseline monolith terpusat; Kondisi B memperlihatkan perilaku naïve EDA 

17 

sebelum mekanisme proteksi lengkap ditambahkan; Kondisi C menerapkan mekanisme robust. Keempat use case dijalankan pada workload dan fault yang dikendalikan. Data dari log, database, broker, resource, dan test oracle direkonsiliasi untuk menghasilkan metrik keselamatan data, recovery, convergence lag, latency, throughput, error rate, CPU, dan RAM. Hasilnya digunakan untuk menjawab apakah proteksi yang diterapkan memenuhi invariant yang ditetapkan dan berapa trade-off teknis yang menyertainya. 

|**Tahap Logis**|**Isi**|
|---|---|
|Masalah operasional|Data cabang/gudang terpisah;<br>kebutuhan pengelolaan multi-<br>cabang terpusat|
|Masalah teknis|Database per service<br>menimbulkan risiko dual-write,<br>duplicate effect, concurrent<br>update, partial failure|
|Artefak|Robust EDA dengan Outbox-<br>Inbox, OCC, durable<br>idempotency, Saga,<br>compensation, retry, DLQ|
|Pembanding|A: monolith terpusat; B: naïve<br>EDA; C: robust EDA|
|Evaluasi|UC-1 s.d. UC-4, workload low-<br>medium-high, fault F1-F5,<br>minimal 30 blok iterasi|
|Bukti|Invariant, test oracle,<br>rekonsiliasi, recovery, lag,<br>performa, resource, user testing|
||Hanya konfigurasi, dataset,|
|Batas kesimpulan|workload, fault, dan lingkungan<br>yang diuji|



18 

## **D. Pertanyaan Penelitian** 

Rumusan masalah pada Bab I sekaligus berfungsi sebagai pertanyaan penelitian. Hipotesis substantif tambahan tidak ditetapkan karena sasaran keselamatan Kondisi C dirumuskan sebagai kriteria penerimaan deterministik per metrik. Untuk metrik kontinu, pengujian statistik dipakai untuk menilai perbedaan antarkondisi tanpa mengubah target keselamatan data menjadi hipotesis keberhasilan. 

19 

## **BAB III METODE PENELITIAN** 

## **A. Jenis dan Pendekatan Penelitian** 

DSRM digunakan sebagai strategi utama karena penelitian ini menghasilkan sekaligus mengevaluasi artefak perangkat lunak. Data utama bersifat kuantitatif dan berasal dari eksperimen sistem terkontrol; data pengguna berfungsi sebagai evaluasi pendukung terhadap kesesuaian alur operasional. Studi kasus Apotek Bisma menyediakan konteks kebutuhan dan batas proses bisnis. Lima lapis metodologi dipisahkan: DSRM sebagai strategi penelitian, pengembangan prototipe sebagai aktivitas pembangunan artefak, fault injection dan benchmark sebagai metode evaluasi teknis, user testing sebagai evaluasi pengguna, serta statistik deskriptif/inferensial dan audit invariant sebagai teknik analisis. 

## **B. Rancangan Penelitian dan Model Pengembangan Perangkat Lunak** 

## **1. Tahapan DSRM** 

|**Tahap**|**Aktivitas Utama**<br>|**Keluaran**|
|---|---|---|
|Identifikasi masalah|Konfirmasi alur<br>cabang/gudang,<br>sistem lokal,<br>rekonsiliasi, kanal<br>transaksi|Kebutuhan dan<br>batas masalah|
|Tujuan solusi|Menetapkan|Kriteria|



20 

||invariant, recovery,<br>konvergensi, dan<br>kebutuhan multi-<br>cabang|desain/evaluasi|
|---|---|---|
|Perancangan &<br>pengembangan|Membangun A, basis<br>B-C, Outbox-Inbox,<br>OCC, Saga dan<br>pendukung|Artefak prototipe|
|Demonstrasi|Menjalankan UC-1<br>sampai UC-4|Bukti fungsi dan<br>trace|
|Evaluasi|Eksperimen A-B-C,<br>fault injection,<br>rekonsiliasi, user<br>testing<br>|Dataset dan hasil<br>evaluasi|
|Komunikasi|Analisis trade-off,<br>batas, rekomendasi<br>migrasi|Laporan penelitian|



## **2. Tiga Kondisi Eksperimen** 

|**Kondisi**|**Implementasi**|**Tujuan**|
|---|---|---|
|A - Baseline|Monolith terpusat<br>Laravel 8 + satu<br>MySQL; transaksi<br>lokal/locking|Baseline terpusat<br>setara secara<br>fungsional|
|B - Naïve EDA|NestJS microservices<br>+ database per<br>service; publish<br>langsung ke<br>RabbitMQ|Menunjukkan<br>kerentanan sebelum<br>proteksi lengkap|
|C - Robust EDA|B + Outbox-Inbox,<br>OCC, durable<br>idempotency, Saga<br>Orchestrator,<br>compensation, retry,<br>DLQ|Menguji integritas,<br>recovery,<br>konvergensi, dan<br>overhead proteksi|



21 

## **3. Batas Domain** 

|**Service**|**Data/Tanggung Jawab**<br>**Otoritatif**|
|---|---|
|Sales|Order, item penjualan, status<br>transaksi, state Saga|
|Inventory|on_hand, reserved, available,<br>mutasi, version|
||payment attempt, nominal,|
|Payment|status, webhook, idempotency<br>key|
||read model dashboard dan|
|Reporting/Notification|notifikasi; bukan sumber<br>kebenaran stok|



## **4. Use Case** 

24. UC-1: POS dan kiosk menjual produk yang sama secara konkuren. 

25. UC-2: restock terjadi berdekatan dengan penjualan dan event dapat dikirim ulang. 

26. UC-3: pembayaran Midtrans melalui webhook, termasuk duplicate webhook dan pembayaran setelah expiry. 

27. UC-4: QRIS statis dengan konfirmasi admin, expiry reservasi, dan late approval yang diarahkan ke rekonsiliasi. 

## **5. Fault Injection** 

||**Kode**|**Gangguan**|**Bukti yang Dicari**|
|---|---|---|---|
|||Service/worker crash||
|||setelah data bisnis|Event tertahan tetap|
|F1||disimpan sebelum|dapat dipublikasikan|
|||event berhasil|setelah recovery|
|||dipublikasikan||
|F2||Event yang sama|Tidak ada duplicate|



22 

||dikirim lebih dari<br>satu kali|effect|
|---|---|---|
|F3|Consumer crash saat<br>memproses event<br>atau sebelum ACK|Retry berjalan;<br>kegagalan persisten<br>terlacak di DLQ|
|F4|Broker delay atau<br>webhook tiba setelah<br>timeout|Late payment tidak<br>mengaktifkan order<br>otomatis; masuk<br>controlled exception|
|F5|Dua transaksi<br>konkuren meminta<br>total kuantitas<br>melebihi available|A/B/C dibandingkan<br>terhadap invariant<br>dan test oracle|



## **C. Tempat dan Waktu Penelitian** 

Pengambilan kebutuhan dan evaluasi pengguna berlangsung di lingkungan operasional Apotek Bisma, Kabupaten Mojokerto. Pengembangan dan eksperimen teknis dilaksanakan pada lingkungan komputasi terkontrol menggunakan Docker Compose. Periode kalender mengikuti jadwal akademik dan akses operasional; kegiatan dirancang dalam 16 minggu dan perlu diselaraskan dengan jadwal bimbingan serta seminar. 

## **D. Subjek dan Sumber Data Penelitian** 

Sumber data teknis meliputi log k6, log aplikasi, state database Sales/Inventory/Payment, tabel Outbox dan Inbox, data broker/DLQ, timestamp tracing, pemakaian CPU/RAM, serta keluaran skrip rekonsiliasi dan test oracle. Satu unit eksperimen ialah satu run/blok pengujian yang menerima konfigurasi kondisi, workload, use case, fault, seed, dan titik gangguan tertentu. Ribuan request di dalam satu run tidak 

23 

diperlakukan sebagai ribuan unit independen; request diringkas terlebih dahulu pada tingkat iterasi. 

Evaluasi pengguna melibatkan enam pegawai cabang dan empat pegawai gudang yang berkaitan langsung dengan alur sistem. Jika semuanya tersedia, pengujian bersifat sensus terhadap sepuluh pegawai. Jika jadwal tidak memungkinkan, purposive sampling diterapkan dengan tetap mewakili setiap cabang dan fungsi gudang; jumlah peserta serta alasan pemilihannya dilaporkan secara terbuka. User testing menilai kesesuaian alur kerja, bukan membuktikan konsistensi data. 

## **E. Variabel dan Definisi Operasional** 

|**Jenis/Variabel**|**Definisi**<br>**Operasional**|**Metrik/Satuan**|
|---|---|---|
|Bebas: kondisi<br>arsitektur|A, B, C pada fungsi<br>bisnis setara|Kategori|
|Bebas: workload|Low, medium, high;<br>nilai final dikunci<br>setelah pilot|VU/RPS sesuai<br>protokol|
|Bebas: fault|F1-F5 pada titik<br>deterministik|Kategori|
|Oversell|Total kuantitas<br>committed<br>melampaui available<br>yang sah|Jumlah kejadian /<br>peluang konflik|
|Lost update|Mutasi sah tertimpa<br>sehingga<br>saldo/ledger tidak<br>sesuai oracle|Jumlah kejadian|
|Duplicate effect|Satu event/webhook|Jumlah efek / event|



24 

||menghasilkan efek<br>bisnis lebih dari<br>sekali|duplikat|
|---|---|---|
|Permanent<br>mismatch|State akhir lintas<br>service tidak sesuai<br>setelah recovery<br>window|Jumlah mismatch|
|Untraceable event|Event tidak diproses<br>dan tidak ditemukan<br>di DLQ|Jumlah event|
||Saga mencapai<br>COMPLETED/CANCE||
|Terminal-state<br>coverage|LLED/EXPIRED/FAIL<br>ED/REFUNDED<br>setelah penyelesaian<br>controlled exception|Persentase|
|Read model lag|Waktu pembaruan<br>read model - waktu<br>event/write model|ms|
|Recovery time|Waktu invariant<br>kembali benar -<br>waktu fault<br>dihentikan|ms|
|Latency|Waktu respons -<br>waktu request|median, p95, p99; ms|
|Throughput|Request selesai /<br>durasi measurement|RPS|
||Request gagal /||
|Error rate|seluruh attempt x<br>100%|%|
||Sampel resource tiap||
|CPU/RAM|1 detik diringkas per<br>iterasi|median/p95; %/MB|



25 

## **F. Instrumen Penelitian** 

28. k6 untuk menghasilkan workload dan merekam waktu request, respons, status, serta jumlah request selesai. 

29. Fault injector deterministik untuk memicu F1-F5 pada titik yang telah dikunci. 

30. Structured application logging dan correlation_id untuk menelusuri satu transaksi lintas Sales, Inventory, Payment, Outbox, Inbox, dan broker. 

31. Test oracle dan skrip rekonsiliasi untuk menghitung saldo yang seharusnya serta memeriksa invariant setelah recovery. 

32. Pemantauan CPU dan RAM dengan sampling interval 1 detik pada lingkungan eksperimen. 

33. Form user testing berbasis tugas yang mencatat task completion, waktu penyelesaian, kesalahan, penilaian Likert mengenai kesesuaian fungsi, kemudahan penggunaan, kejelasan status, serta komentar terbuka. 

## **G. Teknik Pengumpulan Data** 

Sebelum eksperimen utama dimulai, database direset menggunakan snapshot dan seed diverifikasi. Sistem menjalani warm-up agar koneksi dan cache berada pada kondisi stabil; data warm-up tidak dimasukkan ke perhitungan. Selama measurement, k6 menghasilkan pola request yang sama untuk kondisi yang dipasangkan. Fault kemudian disuntikkan pada titik deterministik. Setelah fault dihentikan, seluruh komponen dihidupkan kembali dan sistem menunggu recovery window. Producer dihentikan sebelum rekonsiliasi akhir agar keadaan yang diperiksa tidak terus berubah. 

26 

Setiap run mencatat kode kondisi, use case, workload, fault, seed, nomor iterasi, correlation_id, timestamp, status order, mutasi stok, pembayaran, event, retry, DLQ, dan resource. Data pengguna dikumpulkan setelah peserta menjalankan tugas sesuai perannya. Informasi operasional awal tentang Apotek Bisma dikonfirmasi melalui wawancara atau catatan kebutuhan sebelum requirement final dikunci. 

## **H. Uji Coba dan Analisis** 

## **1. Pilot Test dan Penguncian Protokol** 

Konfigurasi awal pilot menetapkan 10 VU untuk beban rendah, 30 VU untuk beban sedang, dan 60 VU untuk beban tinggi, dengan warm-up 60 detik dan measurement 300 detik. Angka-angka ini merupakan konfigurasi awal yang masih dapat berubah. Beban high akan ditetapkan mendekati titik saturasi yang masih memungkinkan baseline menyelesaikan sebagian besar request. Recovery window harus cukup mencakup Saga timeout, seluruh jadwal retry, dan pemrosesan backlog. Convergence SLA, fault point, denominator metrik keselamatan, dan versi konfigurasi dibekukan sebelum eksperimen utama. 

## **2. Replikasi, Pairing, dan Urutan** 

Setiap kombinasi kondisi, workload, use case, dan fault diuji minimal 30 kali setelah pilot. Pada nomor iterasi yang sama, Kondisi A, B, dan C menggunakan seed, dataset awal, pola request, dan titik gangguan yang sama sehingga membentuk blok berpasangan. Urutan kondisi diacak atau dirotasi untuk mengurangi bias waktu, suhu mesin, cache, 

27 

garbage collection, dan proses latar belakang. Angka 30 merupakan keputusan desain draft yang akan dikonfirmasi melalui pilot variance dan kelayakan sumber daya, bukan jaminan normalitas. 

## **3. Analisis Metrik Kontinu** 

Latency, throughput, read model lag, recovery time, CPU, dan RAM diringkas pada tingkat iterasi menggunakan median, IQR, serta p95/p99 sesuai metrik. Karena ketiga kondisi dipasangkan dalam blok yang sama, perbandingan utama menggunakan uji Friedman untuk menilai perbedaan keseluruhan. Jika perbedaan ditemukan, perbandingan pasangan A-B, A-C, dan B-C dilakukan dengan uji Wilcoxon signed-rank. Nilai p kemudian disesuaikan menggunakan koreksi Benjamini-Hochberg pada keluarga pengujian yang ditetapkan sebelum eksperimen. Kendall's W dan matched-pairs rank-biserial correlation dilaporkan sebagai ukuran efek agar besar perbedaan dapat dibaca bersama nilai p. 

## **4. Confidence Interval** 

Ketidakpastian median dan p95/p99 dihitung dengan bootstrap BCa 95% sebanyak 10.000 resample pada tingkat iterasi. Satu iterasi menghasilkan satu nilai ringkasan terlebih dahulu sehingga request dalam run yang sama tidak dianggap sebagai sampel independen. Histogram, Q-Q plot, dan Shapiro-Wilk dapat dipakai untuk mendiagnosis distribusi, tetapi bukan satu-satunya dasar memilih uji. 

## **5. Analisis Metrik Keselamatan Data** 

Oversell, lost update, duplicate effect, untraceable event, dan permanent mismatch diperlakukan sebagai metrik keselamatan dengan target nol pada Kondisi C. Jumlah 

28 

kejadian selalu dilaporkan bersama denominator yang ditetapkan sebelum eksperimen. Satu pelanggaran saja membuat Kondisi C tidak memenuhi kriteria penerimaan pada metrik dan konfigurasi tersebut. Apabila tidak ditemukan pelanggaran, batas atas interval kepercayaan satu sisi exact binomial 95% tetap dilaporkan untuk menunjukkan keterbatasan daya bukti terhadap kejadian langka. Observasi nol tidak ditafsirkan sebagai probabilitas populasi nol. 

## **6. Kriteria Penerimaan** 

|**Tujuan**|**Kriteria Kondisi C**|
|---|---|
|Kebenaran stok|Oversell = 0; lost update = 0;<br>saldo akhir = test oracle|
|Kecocokan lintas service|Permanent mismatch = 0 setelah<br>recovery window|
|Efek tunggal|Duplicate effect = 0|
||Terminal-state coverage = 100%|
|Pemulihan Saga|setelah controlled exception<br>diselesaikan|
||Untraceable event = 0;|
|Event tidak hilang|accounted-for rate = 100%; DLQ<br>dilaporkan terpisah|
|Konvergensi|p95 read model lag berada di<br>bawah SLA yang dikunci<br>sebelum eksperimen|
||Dilaporkan sebagai trade-off,|
|Performa/resource|bukan syarat keselamatan<br>mutlak|



## **7. Evaluasi Pengguna** 

Data task completion, waktu, kesalahan, Likert, dan komentar dibaca per peran dan tugas. Karena populasi operasional kecil dan tujuan utamanya ialah menilai 

29 

kesesuaian alur kerja, hasil pengguna dilaporkan secara deskriptif dengan denominator yang jelas. Data tersebut tidak dipakai untuk mengklaim konsistensi teknis atau menggeneralisasi ke populasi pengguna apotek secara luas. 

## **I. Jadwal Penelitian** 

|**Minggu**|**Fokus**|**Output**|
|---|---|---|
|1-2|Konfirmasi<br>kebutuhan dan<br>kontrak penelitian|Catatan wawancara,<br>requirement,<br>invariant, scope|
|3-5|Perancangan dan<br>arsitektur dasar|Model stok per<br>lokasi, empat use<br>case, Kondisi A dan<br>basis B|
|6-9|Pengembangan<br>mekanisme proteksi|Outbox-Inbox, OCC,<br>Saga, compensation,<br>retry, durable<br>idempotency, DLQ|
|10-11|Integrasi, tracing,<br>demonstrasi|Read model,<br>observability, fault<br>injector, rekonsiliasi|
|12|Pilot test dan<br>penguncian protokol|Workload, recovery<br>window, SLA, fault<br>point, denominator|
|13-14|Evaluasi teknis dan<br>pengguna|Eksperimen utama<br>dan user testing|
|15-16|Analisis dan<br>komunikasi|Statistik, trade-off,<br>rekomendasi,<br>keterbatasan,<br>laporan|



30 

## **DAFTAR PUSTAKA** 

- Fowler, M. (2002). Patterns of enterprise application architecture. Addison-Wesley. 

- Grafana Labs. (t.t.). k6 documentation: Scenarios, thresholds, checks, and test lifecycle. Diakses 15 Juli 2026, dari https://k6.io/docs 

- Kleppmann, M. (2017). Designing data-intensive applications: The big ideas behind reliable, scalable, and maintainable systems. O'Reilly Media. 

- Midtrans. (t.t.). Midtrans documentation: HTTP notification (webhook), signature verification, dan transaction status. Diakses 15 Juli 2026, dari https://docs.midtrans.com 

- Oracle Corporation. (t.t.). MySQL 8.0 reference manual: InnoDB locking and locking reads. Diakses 15 Juli 2026, dari https://dev.mysql.com/doc/refman/8.0/en/innodblocking.html 

- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302 

- RabbitMQ / Broadcom Inc. (t.t.). RabbitMQ documentation: Consumer acknowledgements and publisher confirms; Reliability guide; Dead letter exchanges. Diakses 15 Juli 2026, dari https://www.rabbitmq.com/docs 

31 

Richardson, C. (2018). Microservices patterns: With examples in Java. Manning Publications. 

Richardson, C. (t.t.-a). Pattern: Transactional outbox. Microservices.io. Diakses 15 Juli 2026, dari https://microservices.io/patterns/data/transactionaloutbox.html 

Richardson, C. (t.t.-b). Pattern: Saga. Microservices.io. Diakses 15 Juli 2026, dari https://microservices.io/patterns/data/saga.html Richardson, C. (t.t.-c). Pattern: Idempotent consumer. Microservices.io. Diakses 15 Juli 2026, dari https://microservices.io/patterns/communication-style/id empotent-consumer.html 

Rochman, C. B. A., & Suartana, I. M. (2026). Pengembangan sistem manajemen gudang berbasis web dengan eventdriven architecture. Journal of Informatics and Computer Science (JINACS), 7(4), 1044-1048. 

32 

## **LAMPIRAN** 

Lampiran yang direncanakan mencakup catatan wawancara/konfirmasi kebutuhan, matriks requirement dan test case, kontrak event, matriks fault injection, instrumen user testing, konfigurasi workload, hasil pilot, serta format keluaran skrip rekonsiliasi. Lampiran aktual disertakan setelah artefak dan instrumen tersedia. 

33 
