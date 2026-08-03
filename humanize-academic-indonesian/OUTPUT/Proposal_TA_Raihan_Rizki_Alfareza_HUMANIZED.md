**IMPLEMENTASI TRANSACTIONAL OUTBOX DAN OPTIMISTIC CONCURRENCY CONTROL PADA MIGRASI MONOLITH KE EVENT-DRIVEN MICROSERVICES BERBASIS ASYNCHRONOUS I/O UNTUK MENJAGA KONSISTENSI DATA (STUDI KASUS: SISTEM POS DAN ERP APOTEK RETAIL, APOTEK BISMA, KABUPATEN MOJOKERTO)**

# **PROPOSAL TUGAS AKHIR**

**BENTUK: SKRIPSI**

Oleh

**Raihan Rizki Alfareza** NIM 23051204067

[Lambang UNESA]

## **UNIVERSITAS NEGERI SURABAYA FAKULTAS TEKNIK PROGRAM STUDI S1 TEKNIK INFORMATIKA**

**2026**

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

## **DAFTAR ISI**

[Perbarui daftar isi otomatis di Microsoft Word]

## **BAB I PENDAHULUAN**

## **A. Latar Belakang**

Apotek Bisma menjalankan tiga cabang dan satu gudang pusat. Berdasarkan keterangan awal pemilik atau pengelola, setiap cabang ditangani oleh dua pegawai, sedangkan kegiatan gudang dijalankan oleh empat pegawai. Operasional cabang saat ini menggunakan aplikasi Laravel 8 yang berjalan secara lokal pada masing-masing cabang dengan basis data yang berdiri sendiri, sementara pencatatan gudang masih dibantu spreadsheet. Kondisi tersebut membuat data transaksi, stok, dan laporan belum tersinkronisasi secara langsung. Rekonsiliasi antarcabang dan gudang baru dilakukan oleh petugas khusus pada akhir bulan sehingga ketidaksesuaian pencatatan berpotensi baru diketahui setelah periode operasional berjalan cukup lama.

Apotek Bisma memerlukan pengelolaan proses multicabang secara terpusat. Gudang memerlukan informasi penjualan dan saldo stok per lokasi sebagai dasar replenishment, sedangkan cabang memerlukan proses penjualan, reservasi, penerimaan transfer, dan pembayaran yang tetap dapat ditelusuri berdasarkan lokasi. Penambahan kanal transaksi melalui kasir, Self-Order Kiosk, Midtrans, dan QRIS statis juga memperluas kebutuhan koordinasi data yang sebelumnya berhenti pada satu proses lokal.

Pada monolith terpusat, perubahan beberapa tabel masih dapat diselesaikan melalui satu transaksi basis data. Setelah domain Sales, Inventory, dan Payment dipisahkan menjadi layanan dengan basis data masing-masing, transaksi lintas layanan tidak lagi memiliki rollback ACID global. Kegagalan setelah data bisnis tersimpan tetapi sebelum event dipublikasikan dapat menimbulkan masalah dual-write. Pengiriman event ulang dapat menghasilkan efek ganda apabila consumer tidak idempoten, sedangkan pembaruan stok secara konkuren dapat menyebabkan lost update atau oversell apabila konflik tidak ditangani. Oleh karena itu, konsistensi pada sistem terdistribusi perlu dirancang melalui transaksi lokal, pertukaran event yang andal, pengendalian konkurensi, dan mekanisme pemulihan (Richardson, 2018; Kleppmann, 2017).

Transactional Outbox menyimpan perubahan data bisnis dan catatan event dalam transaksi lokal yang sama sehingga event yang belum berhasil dipublikasikan tetap dapat dikirim ulang oleh worker (Richardson, t.t.-a). Pada sisi consumer, durable inbox atau idempotency menyimpan identitas event yang telah diproses agar redelivery tidak menimbulkan dampak bisnis kedua (Richardson, t.t.-c). Optimistic Concurrency Control (OCC) menggunakan atribut version untuk menolak pembaruan yang didasarkan pada versi lama. Saga Orchestrator mencatat state dan menentukan langkah lanjutan atau compensation ketika sebagian proses gagal untuk transaksi yang melintasi Sales, Inventory, dan Payment (Richardson, 2018; Richardson, t.t.-b). Gabungan mekanisme tersebut tidak menjadikan sistem selalu konsisten secara instan, tetapi dirancang agar seluruh proses dapat menuju keadaan akhir yang sah dan dapat ditelusuri.

Rochman dan Suartana (2026) menerapkan event-driven architecture pada sistem manajemen gudang dan menunjukkan bahwa pendekatan berbasis event relevan pada aliran persediaan. Penelitian ini menggunakan pola komunikasi yang sama untuk mengevaluasi konsistensi transaksi lintas layanan pada POS/ERP apotek dengan database per service, pembayaran asinkron, konflik stok, duplicate delivery, dual-write, dan partial failure. Sumbu pembedanya terletak pada pengujian gabungan Transactional Outbox, OCC, durable idempotency, Saga orchestration, compensation, retry, dan DLQ yang divalidasi melalui invariant bisnis serta fault injection, bukan pada pemilihan framework.

Tiga kondisi yang setara secara fungsional disusun agar perbandingan dapat dipertanggungjawabkan. Kondisi A adalah monolith terpusat terkontrol berbasis Laravel 8 dan satu basis data MySQL. Kondisi B adalah event-driven microservices berbasis NestJS dengan database per service tetapi tanpa mekanisme keandalan lengkap. Kondisi C menambahkan Outbox-Inbox, OCC, durable idempotency, Saga Orchestrator, compensation, retry, dan DLQ. Perbedaan runtime Laravel dan Node.js tetap diperlakukan sebagai faktor perancu sehingga hasil performa tidak akan diatribusikan hanya kepada satu pola arsitektur. Penilaian utama diarahkan pada kebenaran data, kemampuan pemulihan, konvergensi, serta biaya teknis mekanisme proteksi.

Empat use case menjadi sasaran pengujian: penjualan konkuren melalui POS dan kiosk, restock yang berdekatan dengan penjualan, pembayaran Midtrans, serta QRIS statis dengan konfirmasi admin. Keberhasilan Kondisi C tidak ditentukan hanya oleh latency atau throughput, melainkan terutama oleh tidak ditemukannya oversell, lost update, duplicate effect, untraceable event, dan permanent mismatch pada konfigurasi pengujian yang telah dikunci. Klaim penelitian dibatasi pada use case, dataset, beban, fault, dan lingkungan eksperimen yang diuji; penelitian tidak dimaksudkan untuk menyatakan microservices selalu lebih unggul daripada monolith.

## **B. Identifikasi Masalah**

1. Data transaksi, stok, dan laporan pada tiga cabang serta gudang belum dikelola dalam satu sistem multicabang terpusat sehingga rekonsiliasi masih dilakukan secara periodik.

2. Pemisahan Sales, Inventory, dan Payment ke database per service menghilangkan transaksi ACID global untuk proses bisnis lintas domain sehingga muncul risiko partial failure dan ketidakcocokan state antarlayanan.

3. Publikasi event secara langsung setelah penyimpanan data bisnis memiliki celah dual-write ketika service atau worker gagal pada titik di antara kedua operasi.

4. Redelivery event atau webhook dapat menimbulkan duplicate effect apabila identitas pesan yang telah diproses tidak disimpan secara durable.

5. Transaksi penjualan konkuren pada produk dan lokasi yang sama dapat menghasilkan lost update atau oversell apabila konflik pembaruan stok tidak dikendalikan.

6. Belum tersedia bukti terkontrol pada konteks Apotek Bisma mengenai trade-off konsistensi, pemulihan, konvergensi, latency, throughput, dan resource antara monolith terpusat, naive microservices, dan robust microservices.

## **C. Batasan Masalah**

7. Objek studi kasus dibatasi pada proses POS/ERP Apotek Bisma yang melibatkan tiga cabang dan satu gudang pusat.

8. Domain layanan dibatasi pada Sales, Inventory, Payment, serta Reporting/Notification sebagai read model; sumber kebenaran transaksi tetap berada pada service pemilik domain.

9. Stok dimodelkan per pasangan product_id dan location_id dengan on_hand, reserved, available = on_hand - reserved, serta version. Kesesuaian terhadap stok fisik hanya dapat dinilai melalui stock opname dan berada di luar eksperimen perangkat lunak.

10. Use case eksperimen dibatasi pada UC-1 penjualan konkuren POS-kiosk, UC-2 restock berdekatan dengan penjualan, UC-3 pembayaran Midtrans, dan UC-4 QRIS statis dengan konfirmasi admin.

11. Aspek batch/lot, FEFO, resep, obat keras, recall, dan otorisasi klinis apoteker tidak menjadi variabel penelitian.

12. Kondisi A, B, dan C disetarakan pada model data bisnis, endpoint, dataset awal, workload, pola request, serta target luaran. Perbedaan runtime Laravel dan Node.js dicatat sebagai faktor perancu performa.

13. Fault injection mencakup F1 crash setelah data bisnis tersimpan sebelum event terpublikasi, F2 duplicate event, F3 consumer crash sebelum ACK, F4 broker delay atau webhook terlambat, dan F5 konflik stok konkuren.

14. Kesimpulan penelitian dibatasi pada konfigurasi, dataset, beban, fault, dan lingkungan eksperimen yang diuji dan tidak digeneralisasi sebagai keunggulan universal microservices.

## **D. Rumusan Masalah**

15. Bagaimana merancang migrasi sistem Apotek Bisma menuju sistem terpusat berbasis event-driven microservices yang mendukung stok per lokasi dan transaksi lintas domain?

16. Bagaimana Transactional Outbox dan OCC, dengan dukungan durable idempotency serta Saga, menjaga konsistensi data ketika terjadi transaksi konkuren dan kegagalan parsial?

17. Bagaimana perbandingan konsistensi data, kemampuan pemulihan, konvergensi, dan performa antara monolith terpusat, naive event-driven microservices, dan robust event-driven microservices pada workload serta skenario gangguan yang setara?

## **E. Tujuan Penelitian**

18. Merancang artefak migrasi sistem Apotek Bisma menuju sistem terpusat berbasis event-driven microservices dengan pemisahan domain Sales, Inventory, Payment, dan Reporting/Notification serta model stok per lokasi.

19. Menerapkan dan mengevaluasi Transactional Outbox, OCC, durable idempotency, Saga Orchestrator, compensation, retry, dan DLQ dalam menjaga invariant bisnis pada transaksi konkuren dan partial failure.

20. Membandingkan tiga kondisi arsitektur pada metrik konsistensi, recovery, convergence lag, latency, throughput, error rate, CPU, dan RAM menggunakan workload, dataset, dan fault yang dikendalikan.

## **F. Manfaat Penelitian**

## **1. Manfaat Keilmuan**

Gabungan Outbox, OCC, durable idempotency, dan Saga pada transaksi lintas layanan yang melibatkan stok dan pembayaran diharapkan menghasilkan bukti empiris terkontrol. Bukti tersebut dapat menjadi rujukan kontekstual untuk menilai trade-off antara proteksi konsistensi, kemampuan pemulihan, konvergensi, dan overhead performa pada sistem terdistribusi.

## **2. Manfaat Praktis**

Bagi Apotek Bisma, artefak dan hasil evaluasi dapat menjadi dasar teknis untuk menentukan strategi migrasi dari beberapa sistem lokal menuju pengelolaan multicabang terpusat. Luaran berupa prototipe, test oracle, fault injector, skrip rekonsiliasi, serta laporan evaluasi juga dapat membantu proses verifikasi sebelum keputusan implementasi lebih lanjut.

## **G. Asumsi Penelitian**

21. Data awal eksperimen, aturan bisnis, dan skenario uji yang telah dikunci dapat direplikasi pada setiap kondisi melalui proses reset state dan seed yang sama.

22. Jam sistem pada komponen eksperimen berada pada lingkungan yang sama atau tersinkronisasi sehingga pengukuran lag dan recovery dapat dilakukan secara konsisten.

23. Informasi operasional mengenai jumlah cabang, pegawai, alur gudang, dan rekonsiliasi bulanan masih berstatus keterangan awal pemilik/pengelola dan akan dikonfirmasi melalui catatan wawancara sebelum requirement akhir dikunci.

## **BAB II KAJIAN PUSTAKA**

## **A. Kajian Teori**

## **1. Monolith Terpusat dan Migrasi ke Microservices**

Monolith terpusat menempatkan seluruh fungsi aplikasi dalam satu unit deployment dan memungkinkan satu transaksi basis data menangani perubahan lintas tabel. Pada penelitian ini, monolith diposisikan sebagai baseline terpusat yang sudah memiliki model stok per lokasi dan fungsi bisnis setara dengan kondisi microservices. Ketika domain dipisah menjadi layanan-layanan dengan basis data masing-masing, koordinasi lintas layanan tidak lagi dapat bergantung pada transaksi ACID global (Fowler, 2002; Richardson, 2018).

## **2. Event-Driven Architecture dan Asynchronous I/O**

Pada event-driven architecture, event merepresentasikan fakta bisnis yang telah terjadi dan memungkinkan komponen bereaksi secara asinkron. Command seperti ReserveStock meminta suatu tindakan dan dapat ditolak, sedangkan event seperti StockReserved merekam fakta yang sudah terjadi. Dalam implementasi Node.js/NestJS, asynchronous I/O membuat service dapat menangani operasi basis data, broker, webhook, dan WebSocket tanpa menahan thread selama menunggu respons I/O. Sifat ini berkaitan dengan model eksekusi, bukan jaminan konsistensi. Kebenaran data tetap bergantung pada transaksi lokal, constraint, Outbox, OCC, Inbox, dan Saga.

## **3. Database per Service dan Konsistensi Data**

Tiap service memegang data otoritatifnya sendiri. Sales mengelola order dan state Saga, Inventory mengelola saldo dan mutasi stok, Payment mengelola payment attempt beserta status pembayaran, sedangkan Reporting/Notification hanya menyimpan read model. Pemisahan ini mencegah satu service mengubah basis data service lain secara langsung, tetapi menuntut koordinasi tersendiri ketika satu proses bisnis perlu menyentuh lebih dari satu service.

## **4. Transactional Outbox**

Transactional Outbox mencatat perubahan data bisnis bersama event yang akan dikirim dalam satu transaksi lokal. Worker kemudian membaca tabel outbox dan mempublikasikan event ke broker sampai mendapat publisher confirm. Dengan cara ini, keadaan ketika data bisnis sudah tersimpan tetapi event belum tercatat akibat crash di tengah proses dual-write dapat dihindari (Richardson, t.t.-a).

## **5. Durable Inbox dan Idempotency**

Pada sistem yang menerapkan at-least-once delivery, pesan dapat terkirim lebih dari sekali. Durable inbox menyimpan event_id atau idempotency key yang sudah diproses sehingga consumer mengenali pengiriman ulang dan tidak menjalankan efek bisnis untuk kedua kalinya. Mekanisme ini diperlukan baik untuk event internal maupun webhook pembayaran yang dapat diterima berulang (Richardson, t.t.-c).

## **6. Optimistic Concurrency Control**

OCC memanfaatkan nilai version untuk mendeteksi apakah data telah berubah sejak terakhir dibaca. Pembaruan hanya berhasil jika version yang dibawa transaksi masih cocok dengan version yang tersimpan. Apabila version sudah berbeda, pembaruan ditolak dan proses perlu membaca ulang state terbaru sebelum mencoba kembali. Pada konteks stok, mekanisme ini menjaga agar pembaruan yang bertolak dari versi lama tidak menimpa mutasi yang lebih baru (Kleppmann, 2017).

## **7. Saga Orchestration dan Compensation**

Saga memecah transaksi lintas layanan menjadi rangkaian transaksi lokal. Saga Orchestrator menyimpan state dan menentukan command selanjutnya berdasarkan hasil langkah sebelumnya. Jika satu langkah gagal, compensation menjalankan aksi bisnis untuk memulihkan keadaan, misalnya melepas reservasi stok ketika pembayaran gagal atau kedaluwarsa. Compensation berbeda dari rollback global basis data karena setiap langkah merupakan transaksi lokal yang sudah tersimpan (Richardson, 2018; Richardson, t.t.-b).

## **8. RabbitMQ, Publisher Confirm, ACK, Retry, dan DLQ**

RabbitMQ berperan sebagai broker pesan. Publisher confirm memberitahu bahwa broker telah menerima pesan, sedangkan consumer ACK dikirim setelah pesan berhasil diproses. Pesan yang gagal diproses dapat dikirim ulang sesuai kebijakan retry; setelah melewati batas percobaan, pesan dipindahkan ke Dead Letter Queue. Event di DLQ masih terlacak, tetapi belum berarti proses bisnis berhasil. Pesan tersebut memerlukan replay atau rekonsiliasi (RabbitMQ/Broadcom Inc., t.t.).

## **9. Model Stok per Lokasi dan Invariant Bisnis**

Saldo stok dimodelkan melalui on_hand, reserved, dan available = on_hand - reserved untuk setiap pasangan product_id dan location_id. Invariant utama meliputi: available tidak boleh negatif; saldo setelah recovery harus sama dengan test oracle yang dihitung dari stok awal, mutasi masuk, mutasi keluar, dan kompensasi; satu order hanya memiliki satu pembayaran sah dan satu pemotongan stok final; status final tidak boleh kembali ke pending akibat pesan terlambat; dan setiap Saga harus mencapai terminal state yang sah.

## **10. Fault Injection, Recovery, dan Observability**

Fault injection menguji perilaku artefak pada titik kegagalan yang ditetapkan secara deterministik. Pengamatan tidak berhenti pada keberhasilan retry, tetapi memeriksa keadaan akhir di seluruh database, outbox, inbox, DLQ, ledger mutasi, dan status Saga berdasarkan correlation_id. Recovery time diukur dari saat fault dihentikan sampai invariant kembali terpenuhi, sedangkan read model lag mengukur jeda antara perubahan pada sumber kebenaran dan pembaruan proyeksi.

## **11. Design Science Research Methodology**

Design Science Research Methodology (DSRM) sesuai untuk penelitian yang sekaligus menghasilkan dan mengevaluasi artefak. Tahapnya meliputi identifikasi masalah, penetapan tujuan solusi, perancangan dan pengembangan, demonstrasi, evaluasi, serta komunikasi (Peffers et al., 2007). Eksperimen A-B-C ditempatkan pada tahap evaluasi artefak, bukan sebagai metode tersendiri di luar DSRM.

## **B. Penelitian yang Relevan**

Rochman dan Suartana (2026) mengembangkan sistem manajemen gudang berbasis web dengan event-driven architecture dan menunjukkan penerapan EDA pada aliran persediaan. Skripsi ini menggunakan pola komunikasi serupa, tetapi memfokuskan pengujian pada konsistensi transaksi lintas layanan dan perilaku sistem saat terjadi kegagalan terkontrol. Perbedaan sumbu evaluasi terletak pada mekanisme proteksi (Outbox, Inbox, OCC, Saga, compensation, retry, DLQ), skenario fault injection, serta invariant dan recovery sebagai kriteria keberhasilan.

|**Aspek**|**Rochman &**<br>**Suartana (2026)**|**Penelitian ini**|
|---|---|---|
|Domain|Manajemen gudang<br>dan aliran stok|POS/ERP apotek:<br>penjualan, reservasi,<br>restock,<br>pembayaran, kiosk|
|Batas sistem|EDA untuk<br>menghubungkan<br>modul sistem<br>gudang|Microservices<br>dengan basis kode<br>dan database<br>terpisah per domain|
|Masalah utama|Pengembangan alur<br>event dan respons<br>sistem|Concurrent update,<br>dual-write, duplicate<br>delivery, partial<br>failure|
|Mekanisme|Event broker|Outbox, durable<br>inbox, OCC, Saga<br>Orchestrator,<br>compensation, retry,<br>DLQ|
|Pembayaran|Bukan skenario<br>utama|Midtrans dan QRIS<br>statis human-in-the-<br>loop diuji eksplisit|
|Evaluasi|Fungsionalitas dan<br>performa EDA|Tiga kondisi evolusi,<br>fault injection,<br>invariant, recovery,<br>konvergensi,<br>performa|

Kontribusi yang ditargetkan ialah evaluasi terukur terhadap kombinasi mekanisme proteksi pada konteks transaksi apotek. Klaim kebaruan tetap dibatasi pada studi yang telah diperiksa; penelusuran literatur yang lebih luas perlu dilengkapi sebelum klaim state of the art dinyatakan final.

## **C. Kerangka Berpikir**

Titik berangkat penelitian ialah kondisi operasional Apotek Bisma yang masih menjalankan aplikasi dan basis data terpisah di setiap cabang, sementara pencatatan gudang belum terintegrasi. Dari kebutuhan sistem terpusat, model stok per lokasi dan pemisahan domain Sales, Inventory, Payment, serta Reporting/Notification diturunkan. Begitu database dipisah per service, risiko baru berupa dual-write, duplicate delivery, konflik stok, dan partial failure muncul. Risiko-risiko tersebut menjadi alasan diterapkannya Transactional Outbox, durable inbox/idempotency, OCC, dan Saga pada Kondisi C.

Tiga kondisi yang setara secara fungsional kemudian dievaluasi. Kondisi A menyediakan baseline monolith terpusat, Kondisi B memperlihatkan perilaku naive EDA sebelum mekanisme proteksi lengkap ditambahkan, dan Kondisi C menerapkan mekanisme robust. Keempat use case dijalankan pada workload dan fault yang dikendalikan. Data dari log, database, broker, resource, dan test oracle direkonsiliasi untuk menghasilkan metrik keselamatan data, recovery, convergence lag, latency, throughput, error rate, CPU, dan RAM. Hasilnya digunakan untuk menjawab apakah proteksi yang diterapkan memenuhi invariant yang ditetapkan dan berapa trade-off teknis yang menyertainya.

|**Tahap Logis**|**Isi**|
|---|---|
|Masalah operasional|Data cabang/gudang terpisah;<br>kebutuhan pengelolaan multi-<br>cabang terpusat|
|Masalah teknis|Database per service<br>menimbulkan risiko dual-write,<br>duplicate effect, concurrent<br>update, partial failure|
|Artefak|Robust EDA dengan Outbox-<br>Inbox, OCC, durable<br>idempotency, Saga,<br>compensation, retry, DLQ|
|Pembanding|A: monolith terpusat; B: naive<br>EDA; C: robust EDA|
|Evaluasi|UC-1 s.d. UC-4, workload low-<br>medium-high, fault F1-F5,<br>minimal 30 blok iterasi|
|Bukti|Invariant, test oracle,<br>rekonsiliasi, recovery, lag,<br>performa, resource, user testing|
|Batas kesimpulan|Hanya konfigurasi, dataset,<br>workload, fault, dan lingkungan<br>yang diuji|

## **D. Pertanyaan Penelitian**

Rumusan masalah pada Bab I sekaligus berfungsi sebagai pertanyaan penelitian. Hipotesis substantif tambahan tidak ditetapkan karena sasaran keselamatan Kondisi C dirumuskan sebagai kriteria penerimaan deterministik per metrik. Untuk metrik kontinu, pengujian statistik dipakai untuk menilai perbedaan antarkondisi tanpa mengubah target keselamatan data menjadi hipotesis keberhasilan.

## **BAB III METODE PENELITIAN**

## **A. Jenis dan Pendekatan Penelitian**

Penelitian menggunakan DSRM sebagai strategi utama karena menghasilkan dan mengevaluasi artefak perangkat lunak. Pendekatan data utama bersifat kuantitatif melalui eksperimen sistem terkontrol, sedangkan data pengguna digunakan sebagai evaluasi pendukung terhadap kesesuaian alur operasional. Studi kasus Apotek Bisma menyediakan konteks kebutuhan dan batas proses bisnis. Lima lapis metodologi terdiri atas DSRM sebagai strategi penelitian, pengembangan prototipe sebagai aktivitas pembangunan artefak, fault injection dan benchmark sebagai metode evaluasi teknis, user testing sebagai evaluasi pengguna, serta statistik deskriptif/inferensial dan audit invariant sebagai teknik analisis.

## **B. Rancangan Penelitian dan Model Pengembangan Perangkat Lunak**

## **1. Tahapan DSRM**

|**Tahap**|**Aktivitas Utama**|**Keluaran**|
|---|---|---|
|Identifikasi masalah|Konfirmasi alur cabang/gudang, sistem lokal, rekonsiliasi, kanal transaksi|Kebutuhan dan batas masalah|
|Tujuan solusi|Menetapkan invariant, recovery, konvergensi, dan kebutuhan multi-cabang|Kriteria desain/evaluasi|
|Perancangan & pengembangan|Membangun A, basis B-C, Outbox-Inbox, OCC, Saga dan pendukung|Artefak prototipe|
|Demonstrasi|Menjalankan UC-1 sampai UC-4|Bukti fungsi dan trace|
|Evaluasi|Eksperimen A-B-C, fault injection, rekonsiliasi, user testing|Dataset dan hasil evaluasi|
|Komunikasi|Analisis trade-off, batas, rekomendasi migrasi|Laporan penelitian|

## **2. Tiga Kondisi Eksperimen**

|**Kondisi**|**Implementasi**|**Tujuan**|
|---|---|---|
|A - Baseline|Monolith terpusat Laravel 8 + satu MySQL; transaksi lokal/locking|Baseline terpusat setara secara fungsional|
|B - Naive EDA|NestJS microservices + database per service; publish langsung ke RabbitMQ|Menunjukkan kerentanan sebelum proteksi lengkap|
|C - Robust EDA|B + Outbox-Inbox, OCC, durable idempotency, Saga Orchestrator, compensation, retry, DLQ|Menguji integritas, recovery, konvergensi, dan overhead proteksi|

## **3. Batas Domain**

|**Service**|**Data/Tanggung Jawab Otoritatif**|
|---|---|
|Sales|Order, item penjualan, status transaksi, state Saga|
|Inventory|on_hand, reserved, available, mutasi, version|
|Payment|payment attempt, nominal, status, webhook, idempotency key|
|Reporting/Notification|read model dashboard dan notifikasi; bukan sumber kebenaran stok|

## **4. Use Case**

24. UC-1: POS dan kiosk menjual produk yang sama secara konkuren.

25. UC-2: restock terjadi berdekatan dengan penjualan dan event dapat dikirim ulang.

26. UC-3: pembayaran Midtrans melalui webhook, termasuk duplicate webhook dan pembayaran setelah expiry.

27. UC-4: QRIS statis dengan konfirmasi admin, expiry reservasi, dan late approval yang diarahkan ke rekonsiliasi.

## **5. Fault Injection**

|**Kode**|**Gangguan**|**Bukti yang Dicari**|
|---|---|---|
|F1|Service/worker crash setelah data bisnis disimpan sebelum event berhasil dipublikasikan|Event tertahan tetap dapat dipublikasikan setelah recovery|
|F2|Event yang sama dikirim lebih dari satu kali|Tidak ada duplicate effect|
|F3|Consumer crash saat memproses event atau sebelum ACK|Retry berjalan; kegagalan persisten terlacak di DLQ|
|F4|Broker delay atau webhook tiba setelah timeout|Late payment tidak mengaktifkan order otomatis; masuk controlled exception|
|F5|Dua transaksi konkuren meminta total kuantitas melebihi available|A/B/C dibandingkan terhadap invariant dan test oracle|

## **C. Tempat dan Waktu Penelitian**

Pengambilan kebutuhan dan evaluasi pengguna mengacu pada konteks operasional Apotek Bisma, Kabupaten Mojokerto. Pengembangan dan eksperimen teknis berlangsung pada lingkungan komputasi terkontrol menggunakan Docker Compose. Periode kalender rinci mengikuti jadwal akademik dan akses operasional; rancangan kegiatan disusun dalam 16 minggu dan perlu diselaraskan dengan jadwal bimbingan serta seminar.

## **D. Subjek dan Sumber Data Penelitian**

Sumber data teknis mencakup log k6, log aplikasi, state database Sales/Inventory/Payment, tabel Outbox dan Inbox, data broker/DLQ, timestamp tracing, resource CPU/RAM, serta keluaran skrip rekonsiliasi dan test oracle. Unit eksperimen adalah satu run/blok pengujian yang menerima konfigurasi kondisi, workload, use case, fault, seed, dan titik gangguan tertentu. Ribuan request di dalam satu run tidak diperlakukan sebagai ribuan unit independen; request terlebih dahulu diringkas pada tingkat iterasi.

Evaluasi pengguna diarahkan pada enam pegawai cabang dan empat pegawai gudang yang berkaitan langsung dengan alur sistem. Jika seluruhnya tersedia, pengujian berlangsung secara sensus terhadap sepuluh pegawai. Jika keterbatasan jadwal tidak memungkinkan, purposive sampling digunakan dengan tetap mewakili setiap cabang dan fungsi gudang, kemudian jumlah peserta serta alasan pemilihannya dilaporkan secara terbuka. User testing menilai kesesuaian alur kerja, bukan menjadi bukti konsistensi data.

## **E. Variabel dan Definisi Operasional**

|**Jenis/Variabel**|**Definisi Operasional**|**Metrik/Satuan**|
|---|---|---|
|Bebas: kondisi arsitektur|A, B, C pada fungsi bisnis setara|Kategori|
|Bebas: workload|Low, medium, high; nilai final dikunci setelah pilot|VU/RPS sesuai protokol|
|Bebas: fault|F1-F5 pada titik deterministik|Kategori|
|Oversell|Total kuantitas committed melampaui available yang sah|Jumlah kejadian / peluang konflik|
|Lost update|Mutasi sah tertimpa sehingga saldo/ledger tidak sesuai oracle|Jumlah kejadian|
|Duplicate effect|Satu event/webhook menghasilkan efek bisnis lebih dari sekali|Jumlah efek / event duplikat|
|Permanent mismatch|State akhir lintas service tidak sesuai setelah recovery window|Jumlah mismatch|
|Untraceable event|Event tidak diproses dan tidak ditemukan di DLQ|Jumlah event|
|Terminal-state coverage|Saga mencapai COMPLETED/CANCELLED/EXPIRED/FAILED/REFUNDED setelah penyelesaian controlled exception|Persentase|
|Read model lag|Waktu pembaruan read model - waktu event/write model|ms|
|Recovery time|Waktu invariant kembali benar - waktu fault dihentikan|ms|
|Latency|Waktu respons - waktu request|median, p95, p99; ms|
|Throughput|Request selesai / durasi measurement|RPS|
|Error rate|Request gagal / seluruh attempt x 100%|%|
|CPU/RAM|Sampel resource tiap 1 detik diringkas per iterasi|median/p95; %/MB|

## **F. Instrumen Penelitian**

28. k6 menghasilkan workload dan merekam waktu request, respons, status, serta jumlah request selesai.

29. Fault injector deterministik memicu F1-F5 pada titik yang telah dikunci.

30. Structured application logging dan correlation_id menelusuri satu transaksi lintas Sales, Inventory, Payment, Outbox, Inbox, dan broker.

31. Test oracle dan skrip rekonsiliasi menghitung saldo yang seharusnya serta memeriksa invariant setelah recovery.

32. Pemantauan CPU dan RAM menggunakan sampling interval 1 detik pada lingkungan eksperimen.

33. Form user testing berbasis tugas mencatat task completion, waktu penyelesaian, kesalahan, penilaian Likert mengenai kesesuaian fungsi, kemudahan penggunaan, kejelasan status, serta komentar terbuka.

## **G. Teknik Pengumpulan Data**

Sebelum eksperimen utama, database direset menggunakan snapshot dan seed diverifikasi. Sistem menjalani warm-up agar koneksi dan cache berada pada kondisi stabil; data warm-up tidak dimasukkan ke perhitungan. Selama measurement, k6 menghasilkan pola request yang sama untuk kondisi yang dipasangkan. Fault kemudian disuntikkan pada titik deterministik. Setelah fault dihentikan, seluruh komponen dihidupkan kembali dan sistem menunggu recovery window. Producer dihentikan sebelum rekonsiliasi akhir agar keadaan yang diperiksa tidak terus berubah.

Setiap run menyimpan kode kondisi, use case, workload, fault, seed, nomor iterasi, correlation_id, timestamp, status order, mutasi stok, pembayaran, event, retry, DLQ, serta resource. Data pengguna dikumpulkan setelah peserta menjalankan tugas sesuai perannya. Informasi operasional awal mengenai Apotek Bisma dikonfirmasi melalui wawancara atau catatan kebutuhan sebelum requirement final dikunci.

## **H. Uji Coba dan Analisis**

## **1. Pilot Test dan Penguncian Protokol**

Konfigurasi awal pilot menggunakan 10 VU untuk beban rendah, 30 VU untuk beban sedang, dan 60 VU untuk beban tinggi, dengan warm-up 60 detik dan measurement 300 detik. Nilai tersebut merupakan konfigurasi awal, bukan hasil akhir. Beban high ditetapkan mendekati saturasi yang masih memungkinkan baseline menyelesaikan mayoritas request. Recovery window harus mencakup Saga timeout, seluruh jadwal retry, dan pemrosesan backlog. Convergence SLA, fault point, denominator metrik keselamatan, serta versi konfigurasi dibekukan sebelum eksperimen utama.

## **2. Replikasi, Pairing, dan Urutan**

Setiap kombinasi kondisi, workload, use case, dan fault yang ditetapkan diuji minimal 30 kali setelah pilot. A, B, dan C pada nomor iterasi yang sama menggunakan seed, dataset awal, pola request, dan titik gangguan yang sama sehingga membentuk blok berpasangan. Urutan kondisi diacak atau dirotasi untuk mengurangi bias waktu, suhu mesin, cache, garbage collection, dan proses latar belakang. Angka minimal 30 dipertahankan sebagai keputusan desain draft yang akan dikonfirmasi melalui pilot variance dan kelayakan sumber daya, bukan sebagai jaminan normalitas.

## **3. Analisis Metrik Kontinu**

Latency, throughput, read model lag, recovery time, CPU, dan RAM diringkas pada tingkat iterasi menggunakan median, IQR, serta p95/p99 sesuai metrik. Karena tiga kondisi dipasangkan dalam blok yang sama, perbandingan utama menggunakan Friedman test. Jika terdapat perbedaan, post-hoc Wilcoxon signed-rank diterapkan untuk A-B, A-C, dan B-C. Koreksi Benjamini-Hochberg diterapkan pada keluarga pengujian yang ditetapkan sebelum eksperimen. Kendall's W dan matched-pairs rank-biserial correlation dilaporkan sebagai effect size.

## **4. Confidence Interval**

Ketidakpastian median dan p95/p99 dihitung menggunakan bootstrap BCa 95% sebanyak 10.000 resample pada tingkat iterasi. Satu iterasi terlebih dahulu menghasilkan satu nilai ringkasan sehingga request dalam run yang sama tidak dianggap sebagai sampel independen. Histogram, Q-Q plot, dan Shapiro-Wilk dapat digunakan sebagai diagnosis distribusi, tetapi bukan satu-satunya dasar pemilihan uji.

## **5. Analisis Metrik Keselamatan Data**

Oversell, lost update, duplicate effect, untraceable event, dan permanent mismatch diperlakukan sebagai metrik keselamatan dengan target nol pada Kondisi C. Jumlah kejadian selalu dilaporkan bersama denominator yang ditetapkan sebelum eksperimen. Satu pelanggaran membuat Kondisi C tidak memenuhi kriteria penerimaan pada metrik dan konfigurasi tersebut. Jika tidak ditemukan pelanggaran, batas atas interval kepercayaan satu sisi exact binomial 95% tetap dilaporkan untuk menunjukkan keterbatasan daya bukti terhadap kejadian langka. Observasi nol tidak ditafsirkan sebagai probabilitas populasi nol.

## **6. Kriteria Penerimaan**

|**Tujuan**|**Kriteria Kondisi C**|
|---|---|
|Kebenaran stok|Oversell = 0; lost update = 0; saldo akhir = test oracle|
|Kecocokan lintas service|Permanent mismatch = 0 setelah recovery window|
|Efek tunggal|Duplicate effect = 0|
|Pemulihan Saga|Terminal-state coverage = 100% setelah controlled exception diselesaikan|
|Event tidak hilang|Untraceable event = 0; accounted-for rate = 100%; DLQ dilaporkan terpisah|
|Konvergensi|p95 read model lag berada di bawah SLA yang dikunci sebelum eksperimen|
|Performa/resource|Dilaporkan sebagai trade-off, bukan syarat keselamatan mutlak|

## **7. Evaluasi Pengguna**

Data task completion, waktu, kesalahan, Likert, dan komentar dibaca per peran dan tugas. Karena populasi operasional kecil dan tujuan utamanya adalah validasi kesesuaian alur, hasil pengguna dilaporkan secara deskriptif dengan denominator yang jelas. Data tersebut tidak digunakan untuk mengklaim konsistensi teknis atau generalisasi ke populasi pengguna apotek secara luas.

## **I. Jadwal Penelitian**

|**Minggu**|**Fokus**|**Output**|
|---|---|---|
|1-2|Konfirmasi kebutuhan dan kontrak penelitian|Catatan wawancara, requirement, invariant, scope|
|3-5|Perancangan dan arsitektur dasar|Model stok per lokasi, empat use case, Kondisi A dan basis B|
|6-9|Pengembangan mekanisme proteksi|Outbox-Inbox, OCC, Saga, compensation, retry, durable idempotency, DLQ|
|10-11|Integrasi, tracing, demonstrasi|Read model, observability, fault injector, rekonsiliasi|
|12|Pilot test dan penguncian protokol|Workload, recovery window, SLA, fault point, denominator|
|13-14|Evaluasi teknis dan pengguna|Eksperimen utama dan user testing|
|15-16|Analisis dan komunikasi|Statistik, trade-off, rekomendasi, keterbatasan, laporan|

## **DAFTAR PUSTAKA**

- Fowler, M. (2002). Patterns of enterprise application architecture. Addison-Wesley.

- Grafana Labs. (t.t.). k6 documentation: Scenarios, thresholds, checks, and test lifecycle. Diakses 15 Juli 2026, dari https://k6.io/docs

- Kleppmann, M. (2017). Designing data-intensive applications: The big ideas behind reliable, scalable, and maintainable systems. O'Reilly Media.

- Midtrans. (t.t.). Midtrans documentation: HTTP notification (webhook), signature verification, dan transaction status. Diakses 15 Juli 2026, dari https://docs.midtrans.com

- Oracle Corporation. (t.t.). MySQL 8.0 reference manual: InnoDB locking and locking reads. Diakses 15 Juli 2026, dari https://dev.mysql.com/doc/refman/8.0/en/innodblocking.html

- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302

- RabbitMQ / Broadcom Inc. (t.t.). RabbitMQ documentation: Consumer acknowledgements and publisher confirms; Reliability guide; Dead letter exchanges. Diakses 15 Juli 2026, dari https://www.rabbitmq.com/docs

- Richardson, C. (2018). Microservices patterns: With examples in Java. Manning Publications.

- Richardson, C. (t.t.-a). Pattern: Transactional outbox. Microservices.io. Diakses 15 Juli 2026, dari https://microservices.io/patterns/data/transactionaloutbox.html

- Richardson, C. (t.t.-b). Pattern: Saga. Microservices.io. Diakses 15 Juli 2026, dari https://microservices.io/patterns/data/saga.html

- Richardson, C. (t.t.-c). Pattern: Idempotent consumer. Microservices.io. Diakses 15 Juli 2026, dari https://microservices.io/patterns/communication-style/idempotent-consumer.html

- Rochman, C. B. A., & Suartana, I. M. (2026). Pengembangan sistem manajemen gudang berbasis web dengan eventdriven architecture. Journal of Informatics and Computer Science (JINACS), 7(4), 1044-1048.

## **LAMPIRAN**

Lampiran yang direncanakan mencakup catatan wawancara/konfirmasi kebutuhan, matriks requirement dan test case, kontrak event, matriks fault injection, instrumen user testing, konfigurasi workload, hasil pilot, serta format keluaran skrip rekonsiliasi. Lampiran aktual disertakan setelah artefak dan instrumen tersedia.
