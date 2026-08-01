# Skema Evaluasi dan Checker Metriks Retoris (Automated Rules)

## 0. Status Metrik, Unit Analisis, dan Output

Dokumen ini mendefinisikan sinyal mekanis untuk membantu audit retoris. Checker tidak boleh mengambil keputusan akhir tentang mutu akademik, kepengarangan, atau kesetaraan makna. Semua metrik berstatus alarm kerja dan harus dibaca bersama fungsi bagian, pembaca sasaran, istilah terlindungi, dan audit kesetiaan makna.

### Unit Analisis

Checker dapat bekerja pada lima unit:

- kalimat;
- paragraf;
- sliding window 300-500 kata;
- bagian naskah, misalnya pendahuluan, metode, hasil, atau pembahasan;
- dokumen keseluruhan untuk konsistensi istilah dan pola pembuka.

### Status Sinyal

| Status | Makna | Tindakan |
| :--- | :--- | :--- |
| PASS | Tidak ada sinyal mekanis penting | Tetap lakukan audit substansi jika revisi besar |
| INFO | Pola terdeteksi tetapi lazim secara genre atau teknis | Tidak wajib revisi |
| REVIEW | Pola berpotensi menjadi residu retoris atau beban baca | Tinjau konteks dan rekonstruksi lokal bila perlu |
| FAIL | Saran atau perubahan merusak makna, istilah, angka, sitasi, atau kadar klaim | Tolak revisi atau pulihkan sumber |

### Output Schema

Setiap temuan checker sebaiknya memakai struktur berikut.

| Field | Isi |
| :--- | :--- |
| `rule_id` | Kode aturan stabil, misalnya `DADS_ABSTRACT_DENSITY` |
| `status` | `PASS`, `INFO`, `REVIEW`, atau `FAIL` |
| `span` | Kalimat, paragraf, atau rentang kata yang memicu sinyal |
| `evidence` | Pola, token, atau struktur yang ditemukan |
| `rationale` | Alasan kontekstual mengapa pola perlu/tidak perlu ditinjau |
| `suggested_action` | Tindakan tinjauan, bukan rewrite otomatis |
| `protected_terms` | Istilah, angka, sitasi, kode, atau label yang tidak boleh diubah |

### Global Override

Jika tindakan perbaikan retoris menghilangkan atau mengubah angka, satuan, negasi, syarat, sitasi, istilah teknis, nama metode, identifier, endpoint, event, label, atau kadar klaim, status akhir menjadi FAIL meskipun skor retoris membaik.

---

## 1. Protected Context dan False Positive Guard

Checker harus menurunkan status menjadi `INFO` atau `PASS` jika pola yang terdeteksi berasal dari kebutuhan akademik atau teknis berikut:

- pengulangan nama metode, algoritma, variabel, konstruk, endpoint, event, tabel, skenario, atau label instrumen;
- pelaporan hasil yang sengaja paralel karena memuat metrik, pembanding, atau kondisi yang setara;
- urutan prosedur metodologis;
- daftar resmi indikator, kondisi eksperimen, item instrumen, kategori teori, atau hipotesis;
- pasif ringkas yang menjaga fokus pada prosedur atau objek;
- kepadatan notasi statistik, rumus, parameter, satuan, kode, atau konfigurasi;
- gaya selingkung yang memang meminta struktur impersonal atau paralel.

Checker tidak boleh menyarankan sinonim untuk istilah teknis yang perlu konsisten. Pengulangan istilah inti lebih aman daripada variasi yang mengubah acuan.

---

## 2. Dynamic Abstract Density Score (D-ADS)

`rule_id`: `DADS_ABSTRACT_DENSITY`

D-ADS mengevaluasi kerapatan nomina abstrak non-teknis sebagai alarm kerja. D-ADS bukan bukti asal teks dan bukan alasan otomatis untuk revisi.

### Target Awal

`kebutuhan`, `pengembangan`, `implementasi`, `pengelolaan`, `mekanisme`, `proses`, `pendekatan`, `strategi`, `upaya`, `peningkatan`, `pemanfaatan`, `penyesuaian`, `aspek`, `konteks`, `hal`, `ruang lingkup`, `kontribusi`.

### Klasifikasi Bobot

| Kategori | Contoh | Bobot Alarm | Catatan |
| :--- | :--- | :---: | :--- |
| Abstrak umum | `upaya`, `aspek`, `hal`, `konteks` | tinggi | kuat jika tidak diikuti objek spesifik |
| Nomina tindakan | `pengembangan`, `pengelolaan`, `penerapan`, `pelaksanaan` | sedang | kuat jika pelaku/objek/tindakan kabur |
| Istilah domain potensial | `proses bisnis`, `mekanisme autentikasi`, `implementasi algoritma` | rendah | pertahankan jika menjadi konsep teknis |

### Formula Kalkulasi

`D-ADS = (Jumlah Nomina Abstrak Target / Total Kata dalam Paragraf) * 100%`

D-ADS hanya dihitung sebagai alarm jika paragraf memiliki minimal 40 kata. Untuk paragraf pendek, gunakan hitungan absolut dan audit manual.

### Adaptive Threshold Table

| Kategori Teks / Sub-Bab | Ambang Ideal | Status Warning | Tindakan Tinjauan |
| :--- | :---: | :---: | :--- |
| Latar Belakang / Bisnis | < 12% | > 15% | Tinjau muatan konkret dan lakukan verb recovery bila tindakan kabur |
| Kajian Pustaka | < 14% | > 18% | Tinjau sumbu pembeda, atribusi, dan abstraksi seperti `dasar/konteks/ruang lingkup` |
| Metodologi / Arsitektur | < 18% | > 22% | Pertahankan jika berupa istilah teknis atau tahap prosedur |
| Hasil / Pembahasan | < 14% | > 18% | Tinjau apakah hasil, angka, atau mekanisme terkunci dalam nomina abstrak |

### False Positive

- nama tahap metode yang resmi;
- istilah teknis yang sudah didefinisikan;
- frasa seperti `proses bisnis` atau `mekanisme autentikasi` ketika menjadi objek pembahasan;
- paragraf metode yang sengaja berorientasi prosedur.

---

## 3. Structural Repetition and Window Detector (SRWD)

Audit ini memindai penggunaan pola retorika berulang dalam jendela pemeriksaan 300-500 kata.

### Rule 3.1: Polar Negation Limit

`rule_id`: `SRWD_POLAR_NEGATION`

- Deteksi: `(bukan|tidak) ... (melainkan|tetapi|namun|hanya)`.
- Batas alarm: lebih dari 1 kali per 300 kata, atau lebih dari 2 kali per bagian naskah (pendahuluan, metode, hasil, dst.).
- Status default: REVIEW.
- Tindakan: variasikan dengan alasan positif langsung jika sanggahan tidak perlu; pertahankan jika negasi membatasi klaim secara operasional.

Diagnosis tambahan untuk pola defensif berulang:

- Jika dua atau lebih kalimat `bukan/tidak X, melainkan Y` muncul dalam satu bagian dan sanggahan menanggapi asumsi yang tidak diajukan pembaca, naikkan ke REVIEW kuat.
- Periksa apakah kalimat sebelumnya memuat pernyataan yang memang perlu dibantah. Jika tidak, pola bersifat defensif kosong.
- Periksa apakah pola yang sama muncul lintas paragraf dan membentuk irama seragam. Irama defensif seragam merupakan sinyal formulaik yang kuat.

Rekonstruksi yang disarankan:

1. Majukan alasan positif sebagai kalimat utama.
2. Tempatkan pembatasan sebagai klausa pembatas setelah pernyataan positif.
3. Jika kontras membawa pembeda operasional (misalnya metrik keselamatan vs. metrik performa), pertahankan.

False positive:

- pembatasan definisi;
- pembeda konseptual yang memang membutuhkan kontras;
- negasi metodologis seperti `tidak ditemukan perbedaan` atau `hipotesis nol tidak ditolak`;
- kontras operasional yang membedakan dua kelompok metrik, dua jenis evaluasi, atau dua peran komponen yang dapat tertukar jika tidak dikontraskan.

### Rule 3.2: Consecutive Causal Openers

`rule_id`: `SRWD_CAUSAL_OPENERS`

- Target pembuka: `Oleh karena itu`, `Dengan demikian`, `Oleh sebab itu`, `Akibatnya`, `Berdasarkan hal tersebut`.
- Batas alarm: muncul berturut-turut pada 2 paragraf atau lebih.
- Status default: REVIEW.
- Tindakan: hapus transisi jika hubungan sudah jelas, atau ganti sesuai relasi semantis yang benar.

False positive:

- bagian kesimpulan bertahap yang setiap paragraf memang menutup argumen berbeda;
- gaya selingkung yang meminta penanda eksplisit;
- kalimat hasil yang benar-benar mengikuti sebab/akibat dari kalimat sebelumnya.

---

## 4. Paragraph Opener Diversity Index (PODI)

`rule_id`: `PODI_OPENER_MONOTONY`

PODI mencegah keseragaman pembuka paragraf. Pemeriksaan tidak cukup hanya mengambil tiga kata pertama; checker harus mengklasifikasikan orientasi semantis pembuka.

### Kategori Orientasi

| Orientasi | Contoh |
| :--- | :--- |
| Metadiskursif | `Penelitian ini...`, `Studi tersebut...` |
| Objek/domain | `Sistem persediaan...`, `Transaksi cabang...` |
| Kondisi | `Pada skenario gangguan...`, `Ketika koneksi terputus...` |
| Bukti/hasil | `Tabel 4 menunjukkan...`, `Hasil pengujian...` |
| Sumber | `Rahman (2024) menemukan...` |
| Implikasi | `Temuan ini mengindikasikan...` |
| Prosedur | `Pengujian dilakukan...` |

### Logika Pemeriksaan

1. Ambil pembuka setiap paragraf.
2. Klasifikasikan orientasi semantisnya.
3. Jika tiga paragraf berturut-turut memiliki orientasi sama tanpa alasan genre, status REVIEW.
4. Jika kesamaan terjadi pada langkah metode, daftar hasil paralel, atau format resmi, status INFO.

Tindakan aman: rotasi berdasarkan fungsi paragraf, misalnya kondisi, bukti, objek, sumber, atau batas. Jangan memindahkan kata transisi ke tengah kalimat hanya untuk variasi.

---

## 5. Verb-to-Noun Ratio (VNR) dan Sentence Boundary

### Rule 5.1: VNR Over-Nominalization Alarm

`rule_id`: `VNR_OVER_NOMINALIZATION`

Formula dasar: `VNR = Jumlah Kata Kerja / Jumlah Kata Benda`.

VNR rendah hanya menjadi sinyal kuat jika kalimat juga memenuhi satu atau lebih kondisi berikut:

- panjang lebih dari 25 kata;
- memiliki tiga atau lebih nomina tindakan;
- memakai verba kosong seperti `dilakukan`, `digunakan`, `memiliki`, `memberikan`, `menjadi`, atau `melakukan`;
- pelaku, objek, atau tindakan utama tidak jelas.

Ambang alarm: `VNR < 0.25` pada kalimat panjang dengan kondisi pendukung di atas.

Status default: REVIEW.

Tindakan: uraikan kalimat kompleks menjadi unit fungsi atau ubah nomina tindakan menjadi verba aktif/pasif jika pelaku dan objek tersedia.

False positive:

- kalimat statistik yang memuat nama uji, ukuran efek, parameter, dan satuan;
- definisi formal;
- prosedur metode yang harus mempertahankan istilah nominal;
- kalimat pendek yang jelas meskipun VNR rendah.

### Rule 5.2: Sentence Splitting Boundary

`rule_id`: `SLB_SENTENCE_SPLITTING_BOUNDARY`

Kalimat di bawah 8 kata tidak otomatis salah. Status REVIEW hanya diberikan jika kalimat pendek muncul beruntun dan kehilangan hubungan logis, atau jika pemecahan membuat syarat, sebab, objek, angka, atau pengecualian terlepas dari klaim utama.

Contoh kalimat pendek yang sah:

- *Perbedaannya tidak signifikan.*
- *Hipotesis nol tidak ditolak.*
- *Data kemudian dinormalisasi.*

Tindakan: gabungkan dengan klausa pendukung jika kalimat menjadi fragmen; pertahankan jika kalimat melaporkan hasil langsung atau langkah prosedur yang jelas.

---

## 6. Passive Voice Cascade

`rule_id`: `PVC_PASSIVE_VOICE_CASCADE`

Deteksi: tiga kalimat berurutan dalam satu paragraf memakai predikat pasif atau verba kosong seperti `dilakukan`, `digunakan`, `dilaksanakan`, `diimplementasikan`, `diterapkan`, atau `diberikan`.

Status default: REVIEW.

Tindakan:

- ubah satu kalimat menjadi aktif nonpersonal jika komponen/pelaku teknis penting;
- jadikan objek, hasil, atau kondisi sebagai titik masuk jika pelaku tidak relevan;
- pertahankan pasif ringkas ketika prosedur menjadi fokus.

False positive:

- metode yang berfokus pada objek/prosedur;
- laporan hasil yang sengaja impersonal;
- gaya selingkung yang melarang orang pertama;
- pasif ringkas seperti `Setiap skenario diuji 30 kali`.

Checker tidak boleh menyarankan perubahan semua kalimat menjadi aktif.

---

## 7. Metadiscursive Subject Chain

`rule_id`: `MSC_METADISCURSIVE_CHAIN`

Deteksi: dua kalimat atau lebih dalam satu paragraf dimulai dengan bentuk seperti `(penelitian|studi|skripsi|kajian) (ini|tersebut)` atau pembuka metadiskursif sejenis.

Status default: REVIEW.

Tindakan:

- jadikan objek, variabel, sistem, temuan, sumber, atau kondisi sebagai subjek jika perannya benar;
- pertahankan `penelitian ini` ketika perlu membedakan penelitian sekarang dari sumber lain;
- jangan mengganti secara mekanis dengan sinonim seperti `kajian ini` atau `riset ini`.

False positive:

- bagian tujuan penelitian;
- batasan penelitian;
- perbandingan eksplisit dengan studi terdahulu;
- abstrak yang harus menyebut penelitian secara ringkas.

---

## 8. Delayed Concrete Payload

`rule_id`: `DCP_DELAYED_CONCRETE_PAYLOAD`

Deteksi awal: kalimat dimulai dengan frasa seperti `berdasarkan hal tersebut`, `dalam konteks ini`, `pada dasarnya`, `sehubungan dengan`, `perbedaan fokus tersebut`, `ruang lingkup yang lebih khusus`, lalu diikuti `penelitian ini bertujuan`, `penelitian ini dilakukan`, `diarahkan untuk`, atau `berupaya untuk`.

Status default: REVIEW.

Tindakan:

- uji penghapusan frasa pembuka;
- jika proposisi, syarat, sumber, dan batas tetap sama, frasa menjadi kandidat pemangkasan;
- majukan objek, tindakan, kondisi, bukti, atau hasil yang sudah tersedia.

False positive:

- frasa pembuka memuat syarat penting;
- frasa pembuka menyebut sumber atau kontras yang diperlukan;
- kalimat berada setelah paragraf yang memang membutuhkan penanda kesinambungan eksplisit.

---

## 9. Axisless Difference Statement

`rule_id`: `ADS_AXISLESS_DIFFERENCE`

Deteksi: kata atau frasa `berbeda`, `lebih khusus`, `lebih luas`, `lebih komprehensif`, `ruang lingkup`, `konteks yang lebih spesifik`, atau `fokus lain` muncul tanpa sumbu pembeda yang dekat.

Sumbu pembeda yang dicari:

- objek atau unit analisis;
- populasi, lokasi, atau periode;
- metode, arsitektur, algoritma, atau instrumen;
- kondisi eksperimen atau skenario;
- skala, beban, dataset, atau konfigurasi;
- metrik evaluasi;
- jenis data atau sumber.

Status default: REVIEW.

Tindakan: minta sumbu pembeda yang tersedia pada sumber. Jika tidak tersedia, pertahankan rumusan lebih netral atau beri catatan verifikasi. Jangan menciptakan kesenjangan pustaka.

False positive:

- sumbu pembeda sudah disebut pada kalimat sebelumnya dan antesedennya tunggal;
- tabel atau daftar tepat sebelum paragraf sudah memberi sumbu pembeda;
- gaya selingkung membatasi panjang ringkasan, tetapi pembeda tersedia di bagian lain yang dekat.

---

## 10. Evaluative Adjective Claim

`rule_id`: `EAC_EVALUATIVE_ADJECTIVE_CLAIM`

Deteksi: adjektiva atau klaim evaluatif seperti `efektif`, `efisien`, `optimal`, `komprehensif`, `signifikan`, `strategis`, `robust`, `andal`, `aman`, `akurat`, `stabil`, atau `lebih cepat`.

Status default:

- REVIEW jika klaim tidak terikat pada metrik, pembanding, kondisi, bukti, definisi operasional, atau sitasi;
- FAIL jika revisi mengubah sasaran proposal menjadi hasil yang sudah tercapai;
- INFO jika kata tersebut bagian dari nama konstruk resmi atau gaya selingkung.

Tindakan:

- pada proposal, rumuskan sebagai sasaran evaluasi;
- pada metode, sebut metrik dan prosedur;
- pada hasil, ikat dengan angka, kondisi, tabel, atau sumber;
- pada pembahasan, turunkan kadar klaim jika bukti hanya indikatif.

False positive:

- `signifikan` dipakai dalam makna statistik dan nilai statistik tersedia;
- adjektiva merupakan label resmi instrumen atau variabel;
- klaim evaluatif sedang dikutip dari sumber dengan atribusi jelas.

---

## 11. Technical Identity Guard

`rule_id`: `TIG_TECHNICAL_IDENTITY_GUARD`

Rule ini mengungguli semua saran gaya.

Status FAIL diberikan jika checker atau revisi menyarankan perubahan berikut tanpa dasar eksplisit:

- nama metode, algoritma, teori, konstruk, instrumen, standar, produk, bahasa pemrograman, atau protokol diganti dengan istilah umum;
- identifier, endpoint, event, nama kolom, variabel, fungsi, kelas, atau literal kode berubah;
- angka, satuan, nilai statistik, jumlah pengulangan, versi, parameter, atau konfigurasi hilang;
- `latensi p95` diganti menjadi `kecepatan sistem`, `uji Friedman` menjadi `uji statistik`, atau `wawancara semi-terstruktur` menjadi `wawancara`;
- istilah asing resmi diterjemahkan secara sepihak sehingga cakupan konsep berubah.

Status REVIEW diberikan jika istilah teknis penting muncul tanpa fungsi atau pengantar pada pembaca akademik lintas bidang. Tindakan aman ialah mempertahankan nama teknis lalu menambahkan fungsi singkat jika sumber mendukung.

---

## 12. S1 TI Register Overpolish

`rule_id`: `S1TI_REGISTER_OVERPOLISH`

Rule ini mendeteksi revisi yang terlalu matang untuk skripsi S1 Teknik Informatika. Targetnya bukan membuat teks kurang baik, melainkan menjaga agar gaya final tetap wajar, formal, prosedural, dan dekat dengan pekerjaan skripsi.

Deteksi: revisi menambahkan atau menaikkan istilah meta-akademik seperti `implikasi`, `inferensi`, `konstruksi analitis`, `relasi semantis`, `validitas eksternal`, `kerangka epistemik`, `mekanisme konseptual`, `dinamika metodologis`, atau bentuk sejenis pada paragraf yang sumbernya hanya menjelaskan fitur, prosedur, implementasi, atau hasil uji sederhana.

Status default:

- REVIEW jika gaya menjadi jauh lebih abstrak daripada sumber;
- FAIL jika istilah baru mengubah klaim, mekanisme, atau tingkat kepastian;
- INFO jika istilah tersebut memang ada pada teori, gaya selingkung, atau pembahasan sumber.

Tindakan:

- turunkan ke bahasa akademik jernih yang dekat dengan sistem, data, fitur, metode, pengujian, hasil, dan batas penelitian;
- pertahankan kedalaman analisis hanya jika sumber atau bagian pembahasan memang mendukungnya;
- jangan menambahkan kesalahan buatan untuk membuat teks tampak manusiawi.

False positive:

- bagian pembahasan yang benar-benar membahas validitas, generalisasi, atau implikasi;
- kutipan atau ringkasan teori yang memakai istilah tersebut;
- naskah jurnal atau tesis yang memang menuntut register lebih matang.

---

## 13. S1 TI Procedural Style Guard

`rule_id`: `S1TI_PROCEDURAL_STYLE_GUARD`

Rule ini melindungi struktur prosedural yang wajar pada Bab 3 dan Bab 4 skripsi S1 TI. Kalimat seperti `pengujian dilakukan`, `sistem dirancang`, `data dikumpulkan`, atau `fitur diuji` tidak otomatis menjadi residu.

Deteksi: saran checker mengubah banyak kalimat prosedural metode, perancangan, implementasi, atau pengujian menjadi prosa analitis yang lebih abstrak.

Status default:

- INFO jika struktur prosedural jelas, urutan dapat diikuti, dan istilah teknis terjaga;
- REVIEW jika prosedur terlalu berulang atau memakai verba kosong tanpa objek/kondisi;
- FAIL jika revisi membuat urutan langkah, input, output, aktor, parameter, atau kondisi uji menjadi kabur.

Tindakan:

- pertahankan urutan langkah jika membantu keterulangan;
- pulihkan verba hanya pada kalimat yang mengaburkan tindakan;
- jelaskan aktor, komponen, input, output, skenario, atau kondisi jika tersedia;
- jangan mengubah seluruh bagian metode menjadi esai konseptual.

False positive:

- daftar tahapan resmi;
- prosedur pengujian yang sengaja paralel;
- gaya impersonal yang diwajibkan kampus;
- kalimat pasif ringkas yang menjaga fokus pada objek.

---

## 14. S1 TI Core Term Stability

`rule_id`: `S1TI_CORE_TERM_STABILITY`

Rule ini mencegah sinonim bergilir untuk istilah inti skripsi TI. Dalam banyak skripsi S1, konsistensi `sistem`, `aplikasi`, `data`, `fitur`, `pengujian`, `hasil`, `pengguna`, `admin`, atau `petugas` lebih alami daripada variasi leksikal yang tidak berfungsi.

Deteksi: satu acuan yang sama diganti-ganti dengan sinonim seperti:

- `sistem` -> `platform` -> `solusi` -> `ekosistem`;
- `aplikasi` -> `perangkat lunak` -> `sistem informasi` tanpa pembeda;
- `data` -> `informasi` -> `rekaman` -> `entitas` tanpa fungsi;
- `pengujian` -> `evaluasi` -> `validasi` -> `asesmen` tanpa perbedaan operasional;
- `hasil pengujian` -> `temuan empiris` pada laporan uji sederhana.

Status default:

- REVIEW jika variasi membuat acuan tidak stabil;
- FAIL jika perubahan istilah mengubah konsep teknis;
- INFO jika variasi membedakan konsep yang memang berbeda.

Tindakan:

- pilih istilah inti sesuai sumber dan gunakan konsisten;
- variasikan struktur kalimat melalui fungsi, bukan sinonim;
- pertahankan istilah teknis resmi walaupun berulang.

False positive:

- `sistem` dan `aplikasi` memang mengacu pada tingkat berbeda, misalnya sistem keseluruhan dan aplikasi mobile;
- `validasi` berarti pemeriksaan input, sedangkan `pengujian` berarti uji sistem;
- `data` dan `informasi` dibedakan oleh teori atau definisi operasional.

---

## 15. S1 TI Chapter Function Guard

`rule_id`: `S1TI_CHAPTER_FUNCTION_GUARD`

Rule ini menyesuaikan sinyal retoris dengan fungsi bab skripsi S1 TI. Pola yang tampak formulaik dapat wajar jika sesuai fungsi bab dan tidak berlebihan.

| Bagian | Frasa yang Dapat Wajar | Status Default | Naikkan ke REVIEW Jika |
| :--- | :--- | :---: | :--- |
| Bab 1 | `penelitian ini bertujuan`, `permasalahan yang terjadi`, `sistem dibutuhkan` | INFO | tujuan tidak operasional, masalah generik, manfaat promosi |
| Bab 2 | `penelitian terdahulu`, `perbedaan penelitian`, `metode yang digunakan` | INFO | pembeda tanpa sumbu, atribusi kabur, klaim sumber naik |
| Bab 3 | `sistem dirancang`, `data dikumpulkan`, `tahapan penelitian` | INFO | aktor, input, output, kondisi, atau urutan tidak jelas |
| Bab 4 | `pengujian dilakukan`, `hasil pengujian menunjukkan`, `fitur berjalan` | INFO | klaim efektif/optimal/andal tanpa metrik atau skenario |
| Bab 5 | `berdasarkan hasil`, `saran untuk penelitian selanjutnya` | INFO | menambah hasil baru, saran terlalu luas, batas hilang |

Status FAIL diberikan jika revisi mengubah fungsi bab, misalnya sasaran proposal menjadi hasil yang sudah tercapai, atau hasil sederhana menjadi klaim performa umum.

Tindakan:

- baca pola berdasarkan fungsi bab;
- revisi hanya jika frasa menunda muatan konkret, mengaburkan klaim, atau muncul berantai;
- jangan menghapus semua frasa skripsi yang lazim hanya agar teks tampak lebih unik.

---

## 16. S1 TI Naturalness Gate

`rule_id`: `S1TI_NATURALNESS_GATE`

Gate ini dipakai setelah kesetiaan, technical identity, dan keterbacaan lulus. Tujuannya memastikan hasil akhir tidak terlalu generik, tidak terlalu promosi, dan tidak terlalu over-polished untuk skripsi S1 TI.

Gunakan [contoh-uji-retoris-s1-ti.md](contoh-uji-retoris-s1-ti.md) sebagai bank kasus untuk menguji rule `S1TI_*`, `DCP_DELAYED_CONCRETE_PAYLOAD`, `ADS_AXISLESS_DIFFERENCE`, `EAC_EVALUATIVE_ADJECTIVE_CLAIM`, dan `TIG_TECHNICAL_IDENTITY_GUARD`.

Status REVIEW diberikan jika dua atau lebih kondisi berikut muncul:

- gaya final jauh lebih abstrak daripada sumber;
- hampir semua kalimat dibuat sangat padat dan editorial;
- istilah inti diganti-ganti demi variasi;
- prosedur metode/perancangan kehilangan urutan sederhana;
- pembahasan sederhana diubah menjadi interpretasi teoretis tanpa dukungan;
- frasa skripsi yang wajar dihapus semua sehingga teks terasa seperti artikel profesional;
- klaim hasil terdengar lebih kuat daripada data, skenario, atau metrik.

Status PASS diberikan jika:

- teks formal tetapi masih dekat dengan objek, sistem, fitur, data, pengujian, dan hasil;
- pengulangan istilah inti terkendali dan konsisten;
- prosedur tetap mudah diikuti;
- klaim tidak promosi dan tidak melebihi bukti;
- suara akhir tidak jauh lebih megah daripada sumber atau sampel penulis.

Gate ini tidak boleh digunakan untuk menambahkan kesalahan, slang, pengalaman palsu, atau ketidakkonsistenan. Kewajaran mahasiswa berasal dari kalibrasi register dan fungsi skripsi, bukan dari cacat buatan.

---

## 16b. Mechanical Italic Consistency Guard

`rule_id`: `MIC_MECHANICAL_ITALIC_GUARD`

Rule ini mendeteksi penambahan cetak miring (italic) yang terlalu konsisten dan mekanis pada revisi, terutama jika naskah asli tidak menggunakan italic atau menggunakannya secara sporadis.

### Masalah

Penambahan italic secara 100% konsisten pada semua istilah asing merupakan sinyal proses editorial otomatis yang kuat. Mahasiswa S1 TI yang menulis sendiri biasanya:

- tidak konsisten 100% dalam memformat italic;
- menganggap beberapa istilah sudah cukup umum di domain TI tanpa perlu italic;
- mengikuti gaya selingkung kampus, yang sering tidak mengharuskan italic pada semua istilah asing;
- kadang lupa memformat beberapa kemunculan.

### Deteksi

Hitung jumlah italic tunggal (bukan bold) pada naskah asli dan naskah revisi. Jika naskah asli memiliki 0 atau sangat sedikit italic, tetapi revisi menambahkan italic secara merata pada hampir semua istilah asing, status REVIEW.

Perhatikan pola berikut:

- italic yang diulang pada setiap kemunculan istilah yang sama, tanpa pernah terlewat;
- italic pada istilah yang sudah sangat umum di domain TI dan sudah mapan (consumer, service, update, state, retry, version, crash, request, run, seed, cache, thread, worker, broker);
- italic pada nama produk atau bahasa pemrograman yang seharusnya tidak dicetak miring (RabbitMQ, NestJS, Laravel, Node.js, MySQL, Docker Compose).

### Status Default

- REVIEW jika naskah asli tidak menggunakan italic tetapi revisi menambahkan italic secara masif dan merata;
- INFO jika revisi hanya menambahkan italic pada kemunculan pertama istilah asing yang belum diserap;
- PASS jika pola italic konsisten dengan gaya selingkung yang telah ditentukan.

### Tindakan Aman

1. Sesuaikan pola italic revisi dengan pola italic naskah asli. Jika naskah asli tidak menggunakan italic, revisi sebaiknya juga tidak atau sangat minim.
2. Jika gaya selingkung kampus mengharuskan italic pada istilah asing, italic hanya pada kemunculan penting pertama, lalu konsisten tanpa italic pada kemunculan selanjutnya — kecuali istilah yang memang jarang muncul.
3. Jangan memiringkan nama produk, bahasa pemrograman, merek, kode, URL, endpoint, dan identifier.
4. Biarkan sedikit inkonsistensi kecil yang wajar — manusia tidak 100% konsisten.

### False Positive

- gaya selingkung yang memang mengharuskan italic pada semua istilah asing;
- naskah jurnal yang mengikuti standar penerbitan tertentu;
- revisi yang diminta pengguna secara eksplisit untuk menambahkan italic.

### 16b-2. Mechanical Backtick/Code Format Guard

`rule_id`: `MIC_MECHANICAL_BACKTICK_GUARD`

Pantau penambahan format kode (backtick) pada identifier, variabel, atau nama field yang pada naskah asli ditulis sebagai teks biasa. Penambahan backtick secara konsisten pada semua identifier tanpa pernah melewatkan satu pun merupakan sinyal proses editorial otomatis.

Deteksi: naskah asli menulis `product_id`, `correlation_id`, `on_hand`, atau identifier lain tanpa backtick, tetapi revisi menambahkan backtick pada semua kemunculan secara merata.

Status default:

- REVIEW jika naskah asli tidak menggunakan backtick tetapi revisi menambahkannya secara masif;
- INFO jika format backtick sudah ada pada naskah asli dan revisi mempertahankannya;
- PASS jika gaya selingkung memang mengharuskan format kode pada identifier.

Tindakan aman: sesuaikan format revisi dengan format naskah asli. Jika asli tidak pakai backtick, revisi juga tidak. Mahasiswa yang menulis sendiri biasanya tidak konsisten 100% dalam memformat identifier sebagai kode.

---

## 17. Safe Suggestion Policy

Checker boleh menyarankan tindakan berikut:

- pulihkan verba tindakan jika pelaku dan objek tersedia;
- majukan objek, kondisi, data, atau hasil yang sudah disebut;
- hapus transisi jika hubungan sudah jelas;
- ulangi nomina inti jika anteseden kabur;
- pertahankan istilah teknis dan beri fungsi singkat pada kemunculan penting;
- turunkan klaim evaluatif menjadi sasaran, observasi, atau indikasi sesuai bukti;
- untuk skripsi S1 TI, pertahankan gaya prosedural yang jelas dan istilah inti yang stabil jika keduanya membantu pembaca.

Checker tidak boleh menyarankan tindakan berikut:

- mengganti istilah teknis dengan sinonim untuk variasi;
- mengacak panjang kalimat atau tanda baca;
- menerjemahkan semua unsur asing;
- mengubah semua pasif menjadi aktif;
- memoles semua kalimat menjadi prosa konseptual yang terlalu matang untuk skripsi S1 TI;
- menambah endpoint, versi, nama kolom, event, konfigurasi, alasan metode, atau mekanisme yang tidak tersedia;
- menghapus angka, syarat, negasi, hasil nol, atau sitasi agar kalimat lebih ringan.

---

## 18. Safety Interlock

Setiap saran perbaikan dari skrip atau modul wajib melewati urutan pemeriksaan berikut.

1. Evaluasi makna: apakah perubahan mengubah batas masalah, angka, peran, polaritas, modalitas, kausalitas, syarat, atau logika asli?
   - Jika ya, status FAIL.
2. Evaluasi istilah teknis: apakah ada istilah resmi/domain seperti `monolith`, `database`, `framework`, `microservices`, `endpoint`, `event`, nama algoritma, nama uji, atau identifier yang diubah sepihak?
   - Jika ya, status FAIL.
3. Evaluasi asal-usul detail: apakah revisi menambah detail teknis, alasan metode, klaim performa, atau implikasi yang tidak tersedia?
   - Jika ya, status FAIL atau REVIEW dengan catatan verifikasi, sesuai risiko.
4. Evaluasi konteks retoris: apakah sinyal berasal dari residu formulaik atau dari kebutuhan genre/metode?
   - Jika kebutuhan genre/metode, status INFO atau PASS.
   - Jika residu formulaik, status REVIEW dan lakukan rekonstruksi lokal.

Kode keluar atau status otomatis tidak membuktikan kesetaraan semantik lengkap. Keputusan akhir tetap membutuhkan pembacaan berdampingan antara sumber dan revisi.
