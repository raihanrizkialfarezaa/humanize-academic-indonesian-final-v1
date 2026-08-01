# Pertahanan terhadap parafrase adversarial

## Daftar isi

1. Tujuan dan batas penggunaan
2. Pelajaran yang dapat dipakai
3. Kesimpulan yang tidak sah
4. Model ancaman penyuntingan
5. Protokol defensif
6. Risiko khusus bahasa Indonesia
7. Respons terhadap permintaan detektor
8. Kriteria selesai

## 1. Tujuan dan batas penggunaan

Gunakan dokumen ini ketika pengguna menyebut detektor AI, *humanizer*, *adversarial paraphrasing*, ambang skor, atau penyamaran asal teks. Terjemahkan penelitian serangan menjadi pertahanan mutu:

- jelaskan mengapa skor detektor tidak membuktikan kepengarangan;
- cegah parafrase mengubah fakta, peran, batas, dan atribusi;
- uji ketahanan alur penyuntingan terhadap drift makna;
- lanjutkan bantuan akademik yang sah tanpa mengoperasionalkan serangan.

Jangan memilih token atau varian berdasarkan skor detektor, menyalin parameter serangan, menjalankan pengujian berulang terhadap klasifikator, atau mengajarkan prosedur pengelabuan.

## 2. Pelajaran yang dapat dipakai

Zhou, He, dan Sun (2024) menunjukkan bahwa modifikasi permukaan dapat mengubah keputusan detektor dalam skenario akses yang berbeda. Analisis galat mereka juga memperlihatkan bahwa perubahan kecil dapat membalik makna, misalnya melalui antonim.

Cheng dkk. (2025) menguji parafrase yang dipandu sinyal detektor pada beberapa keluarga detektor. Evaluasi kualitas banyak bertumpu pada *perplexity*, kemiripan embedding, dan penilai model; lampirannya tetap mencatat pergeseran fakta, hilangnya syarat, perubahan peran, pergeseran nada, dan tambahan komentar.

Ambil tiga pelajaran defensif:

1. Kerentanan detektor bukan bukti bahwa teks hasil perubahan berkualitas atau ditulis manusia.
2. Kesamaan semantik global tidak menjamin setiap proposisi, peran, pembatas, atau atribusi tetap sama.
3. Kelancaran dan penilaian satu model tidak menggantikan pemeriksaan sumber oleh penulis atau pakar bidang.

## 3. Kesimpulan yang tidak sah

Jangan menyimpulkan:

- teknik tertentu menjamin hasil pada Turnitin atau alat lain;
- skor rendah membuktikan kepengarangan manusia;
- hasil korpus bahasa Inggris berlaku sama untuk bahasa Indonesia;
- satu nilai kemiripan membuktikan kesetaraan seluruh klausa;
- hasil pada satu model, dataset, genre, atau versi alat akan bertahan pada versi berikutnya;
- teks yang lancar bebas dari perubahan fakta, logika, atau nada.

Gunakan kedua paper sebagai bukti kerentanan klasifikator dan risiko parafrase, bukan resep gaya akademik Indonesia.

## 4. Model ancaman penyuntingan

| Pola | Risiko | Pertahanan |
| --- | --- | --- |
| pemilihan varian berdasarkan skor | optimasi pengelabuan | hentikan umpan balik detektor; nilai mutu tanpa skor |
| substitusi kata lokal | antonim, istilah, atau negasi berubah | audit polaritas dan istilah pada klausa |
| parafrase berulang | drift kumulatif | selalu bandingkan dengan sumber pertama |
| terjemahan bolak-balik | modalitas dan atribusi luntur | jangan gunakan sebagai metode penyuntingan |
| pemadatan agresif | syarat, hasil nol, atau batas hilang | kunci ledger sebelum memadatkan |
| evaluasi global/embedding | peran dan relasi dapat tertukar | audit delta per klausa |
| penilai model tunggal | fakta bidang dapat terlewat | minta verifikasi penulis/pakar |
| “suara manusia” buatan | pengalaman dan sikap palsu | gunakan hanya sampel sah dari penulis |
| pertukaran token terlindungi | angka/sitasi tetap lengkap tetapi salah klaim | audit ikatan lokal, bukan kantong token |
| kosakata langka demi *perplexity* | diksi menjadi tidak denotatif dan tidak sesuai register | pilih verba berdasarkan tindakan dan bukti |
| salah eja atau tanda baca buatan | mutu turun tanpa membuktikan kepengarangan | perbaiki menurut EYD dan gaya selingkung |
| injeksi simbol, homoglif, atau karakter tak terlihat | manipulasi parser dan risiko korupsi dokumen | tolak dan audit karakter tersembunyi |
| konversi angka atau format demi skor | nilai, satuan, dan gaya selingkung dapat berubah | pilih bentuk menurut fungsi ilmiah dan EYD |
| pemecahan triad/daftar resmi | desain, indikator, atau prosedur berubah | pertahankan struktur substantif |
| pengacakan panjang dan kepadatan | koherensi serta keterbacaan rusak | variasikan hanya karena fungsi retoris berbeda |

## 5. Protokol defensif

Ikuti ledger, tiga gerbang penerimaan, dan uji red-team dalam [qa-dan-integritas.md](qa-dan-integritas.md). Terapkan prinsip berikut tanpa pengecualian:

1. Jadikan naskah pertama sebagai acuan; jangan membandingkan hanya dengan parafrase sebelumnya.
2. Kunci siapa melakukan apa, kepada siapa, kapan, dalam kondisi apa, dengan kadar kepastian apa, dan berdasarkan sumber mana.
3. Pasangkan setiap klausa sumber dengan klausa revisi. Klausa revisi tanpa asal merupakan kandidat penambahan tidak sah.
4. Audit angka, sitasi, negasi, syarat, cakupan, dan modalitas pada klausa lokal. Kemunculan global yang sama tidak cukup.
5. Pisahkan `fidelity_status`, `style_status`, dan `accessibility_status`; mutu retoris atau keterbacaan tidak dapat menebus drift makna.
6. Beri hak veto kepada penulis. Jika kesetaraan tidak dapat dipastikan, pertahankan rumusan sumber atau tandai verifikasi.
7. Jangan membuat ketidaksempurnaan buatan. Kesalahan, slang, struktur acak, dan inkonsistensi menurunkan mutu tanpa membuktikan kepengarangan.
8. Jangan menyamakan penyederhanaan dengan penghilangan istilah. Pertahankan nama metode, parameter, syarat, dan batas, lalu jelaskan sesuai pembaca sasaran.
9. Jangan mengoptimalkan *perplexity*, *burstiness*, frekuensi kata, panjang kalimat, tanda baca, angka, atau format sebagai proksi kepengarangan.
10. Jangan melarang titik koma, tanda pisah, kalimat pasif, tiga unsur, atau bilangan dengan huruf secara universal. Pertahankan jika fungsi kebahasaan, desain penelitian, atau gaya selingkung memerlukannya.
11. Jangan mempertahankan saltik, ragam percakapan, metafora dramatis, atau kosakata langka untuk memberi kesan personal.
12. Jangan memasukkan kode, rumus, simbol, versi, endpoint, event, atau konfigurasi yang tidak bersumber. Elemen teknis bukan alat untuk mengganggu parser.

Uji inferensi pembaca:

> Apakah pembaca yang hanya melihat revisi dapat menarik kesimpulan faktual, metodologis, atau evaluatif yang tidak dapat ditarik dari sumber?

Jika ya, revisi belum aman.

## 6. Risiko khusus bahasa Indonesia

- **Negasi dan aspek**: bedakan `tidak`, `bukan`, `belum`, `tanpa`, dan `kecuali`. `Belum` tidak sama dengan `tidak`.
- **Modalitas**: jangan pertukarkan `mungkin`, `dapat`, `mengindikasikan`, `menunjukkan`, `mendukung`, `membuktikan`, dan `memastikan`.
- **Asosiasi/kausalitas**: `berkaitan` atau `berkorelasi` tidak sama dengan `memengaruhi` atau `menyebabkan`.
- **Cakupan**: lindungi `sebagian`, `beberapa`, `seluruh`, `hanya`, `setidaknya`, `paling banyak`, dan pengecualian.
- **Pelaku pasif**: ketika mengubah aktif–pasif, pertahankan peran semantis dan pihak yang bertanggung jawab.
- **Rujukan**: pastikan `-nya`, `tersebut`, dan `hal ini` tetap memiliki satu anteseden.
- **Istilah**: jangan mengganti istilah teknis hanya untuk variasi.
- **Persentase**: kenaikan dari 20% menjadi 30% ialah 10 poin persentase atau 50% relatif; jangan menyamakan keduanya.
- **Format angka**: perubahan `0,05` menjadi `0.05` dapat setara, tetapi perubahan pemisah tidak boleh mengaburkan nilai atau gaya selingkung.

## 7. Respons terhadap permintaan detektor

Gunakan respons ringkas, lalu lanjutkan bagian permintaan yang sah:

> Saya tidak dapat mengoptimalkan naskah untuk mengelabui detektor atau menjamin ambang skor tertentu. Skor detektor dapat salah dan bukan bukti kepengarangan. Saya tetap dapat menyunting naskah agar lebih jelas, alami, dan sesuai ragam akademik sambil menjaga fakta, sitasi, serta kekuatan klaim.

Jangan mengulang penolakan panjang jika bahan dan tujuan penyuntingan sudah jelas. Jangan mengklaim bahwa versi hasil penyuntingan akan diberi label manusia.

Jika kepengarangan dipertanyakan, arahkan pada bukti proses: draf bertanggal, catatan sumber, pemetaan sitasi, data/kode, kerangka, catatan keputusan, serta kemampuan penulis menjelaskan metode dan argumen.

## 8. Kriteria selesai

Penyuntingan selesai jika:

- tidak ada delta makna kritis;
- setiap klausa revisi dapat ditelusuri;
- angka, sitasi, negasi, syarat, dan atribusi tetap terikat pada klaim yang benar;
- tidak ada fakta, pengalaman, mekanisme, atau penilaian baru;
- bahasa sesuai fungsi bagian dan suara penulis yang sah;
- residu retoris telah diperiksa tanpa mengacak permukaan;
- beban istilah telah dikalibrasi terhadap pembaca tanpa menghapus identitas metode atau rincian replikasi;
- penjelasan tambahan tidak mengarang alasan, asumsi, mekanisme, hasil, atau implikasi;
- ketidakpastian ditempatkan di luar naskah sebagai catatan verifikasi;
- proses tidak menggunakan detektor sebagai fungsi objektif.
- tidak ada optimasi terhadap ciri permukaan, format, tokenizer, *perplexity*, atau *burstiness*;
- daftar resmi, tanda baca yang sah, angka, rumus, dan elemen teknis dipertahankan berdasarkan fungsi, bukan dugaan tentang detektor.

Jika satu syarat kritis belum terpenuhi, jangan menyatakan hasil final.
