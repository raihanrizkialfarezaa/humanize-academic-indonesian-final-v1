#!/usr/bin/env python3
"""Regression tests for the Indonesian academic rewrite auditor."""

from __future__ import annotations

import unittest

try:
    from .validate_rewrite import audit, exit_code_for_result
except ImportError:
    from validate_rewrite import audit, exit_code_for_result


def checks(result: dict[str, object], key: str) -> set[str]:
    return {item["check"] for item in result[key]}  # type: ignore[index]


class RewriteAuditTests(unittest.TestCase):
    def test_identical_text_passes_all_three_gates(self) -> None:
        text = "Model diuji pada 120 peserta (Rahman, 2024)."
        result = audit(text, text)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["fidelity_status"], "PASS")
        self.assertEqual(result["style_status"], "PASS")
        self.assertEqual(result["accessibility_status"], "PASS")

    def test_changed_number_and_citation_fail(self) -> None:
        original = "Akurasi mencapai 82% menurut Rahman (2024)."
        revised = "Akurasi mencapai 92% menurut Rahman (2025)."
        result = audit(original, revised)
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("angka/satuan", checks(result, "fidelity_errors"))
        self.assertIn("sitasi penulis-tahun", checks(result, "fidelity_errors"))

    def test_equivalent_currency_and_decimal_formats_pass(self) -> None:
        result = audit(
            "Biaya tercatat Rp 1.000.000 dengan alpha 0,05.",
            "Biaya tercatat Rp1.000.000 dengan alpha 0.05.",
        )
        self.assertEqual(result["fidelity_status"], "PASS")
        self.assertEqual(result["status"], "PASS")

    def test_equivalent_author_year_citation_formats_pass(self) -> None:
        result = audit(
            "Menurut Rahman (2024), model tetap stabil.",
            "Model tetap stabil (Rahman, 2024).",
        )
        self.assertEqual(result["fidelity_status"], "PASS")

    def test_equivalent_multi_author_citation_formats_pass(self) -> None:
        result = audit(
            "Rahman, Putra, dan Sari (2024) melaporkan pola yang sama.",
            "Pola yang sama dilaporkan (Rahman, Putra, dan Sari, 2024).",
        )
        self.assertEqual(result["fidelity_status"], "PASS")

    def test_swapped_numbers_fail_even_when_global_bag_is_equal(self) -> None:
        result = audit(
            "Metode A mencapai 82%, sedangkan metode B mencapai 91%.",
            "Metode A mencapai 91%, sedangkan metode B mencapai 82%.",
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("ikatan lokal unsur terlindungi", checks(result, "fidelity_errors"))

    def test_reordered_claims_keep_number_bindings(self) -> None:
        result = audit(
            "Metode A mencapai 82%. Metode B mencapai 91%.",
            "Metode B mencapai 91%. Metode A mencapai 82%.",
        )
        self.assertEqual(result["fidelity_status"], "PASS")

    def test_swapped_citations_fail_even_when_all_citations_remain(self) -> None:
        result = audit(
            "Metode A efektif (Rahman, 2024). Metode B stabil (Putra, 2023).",
            "Metode A efektif (Putra, 2023). Metode B stabil (Rahman, 2024).",
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("ikatan lokal unsur terlindungi", checks(result, "fidelity_errors"))

    def test_moved_negation_fails_even_when_count_is_equal(self) -> None:
        result = audit(
            "Metode A tidak menurunkan latensi, tetapi metode B menurunkannya.",
            "Metode A menurunkan latensi, tetapi metode B tidak menurunkannya.",
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("ikatan lokal penanda semantik", checks(result, "fidelity_errors"))

    def test_not_yet_cannot_be_replaced_with_not(self) -> None:
        result = audit(
            "Intervensi belum menurunkan tekanan darah pada kelompok kontrol.",
            "Intervensi tidak menurunkan tekanan darah pada kelompok kontrol.",
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("ikatan lokal penanda semantik", checks(result, "fidelity_errors"))

    def test_semantic_inflation_fails(self) -> None:
        result = audit(
            "Durasi penggunaan mungkin berkaitan dengan kelelahan pada sampel ini.",
            "Durasi penggunaan terbukti menyebabkan kelelahan pada sampel ini.",
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("ikatan lokal penanda semantik", checks(result, "fidelity_errors"))

    def test_modal_synonyms_in_same_category_do_not_fail(self) -> None:
        result = audit(
            "Pola tersebut mungkin menjelaskan variasi hasil.",
            "Pola tersebut dapat menjelaskan variasi hasil.",
        )
        self.assertNotEqual(result["fidelity_status"], "FAIL")

    def test_hidden_character_fails(self) -> None:
        result = audit("Hasil tetap.", "Ha\u200bsil tetap.")
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("karakter tersembunyi", checks(result, "fidelity_errors"))

    def test_changed_proper_name_requires_review(self) -> None:
        result = audit(
            "Penelitian dilakukan di Universitas Indonesia.",
            "Penelitian dilakukan di Universitas Airlangga.",
        )
        self.assertEqual(result["fidelity_status"], "REVIEW")
        self.assertIn("nama/entitas berhuruf kapital", checks(result, "fidelity_warnings"))

    def test_changed_factorial_operator_fails(self) -> None:
        result = audit(
            "Pengujian memakai 3 kondisi × 4 skenario.",
            "Pengujian memakai 3 kondisi + 4 skenario.",
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("operator/desain faktorial", checks(result, "fidelity_errors"))

    def test_changed_direct_quote_fails(self) -> None:
        result = audit(
            'Responden menyatakan, “layanan belum stabil”.',
            'Responden menyatakan, “layanan sudah stabil”.',
        )
        self.assertEqual(result["fidelity_status"], "FAIL")
        self.assertIn("kutipan langsung", checks(result, "fidelity_errors"))

    def test_formulaic_positioning_is_style_review_not_fidelity_failure(self) -> None:
        text = (
            "Perbedaan fokus membuat penelitian ini tidak diarahkan untuk menyanggah "
            "atau membuktikan kelemahan sistem sebelumnya. Penelitian tersebut justru "
            "menjadi dasar untuk membuktikan bahwa EDA cocok diterapkan pada pengelolaan "
            "persediaan. Skripsi ini melanjutkan konteks tersebut dengan ruang lingkup "
            "yang lebih khusus, yaitu menguji konsistensi transaksi lintas layanan ketika "
            "terjadi kegagalan sistem yang disuntikkan secara terkontrol."
        )
        result = audit(text, text)
        self.assertEqual(result["fidelity_status"], "PASS")
        self.assertEqual(result["style_status"], "REVIEW")
        style_checks = checks(result, "style_warnings")
        self.assertIn("urutan gerak retoris formulaik", style_checks)
        self.assertIn("rantai subjek metadiskursif", style_checks)
        self.assertIn("kepadatan abstraksi metadiskursif", style_checks)

    def test_single_necessary_meta_subject_does_not_trigger_chain(self) -> None:
        text = "Penelitian ini menguji 3 skenario gangguan jaringan."
        result = audit(text, text)
        self.assertNotIn("rantai subjek metadiskursif", checks(result, "style_warnings"))

    def test_formulaic_case_can_be_reconstructed_without_style_residue(self) -> None:
        original = (
            "Perbedaan fokus membuat penelitian ini tidak diarahkan untuk menyanggah "
            "atau membuktikan kelemahan sistem sebelumnya. Penelitian tersebut justru "
            "menjadi dasar untuk membuktikan bahwa EDA cocok diterapkan pada pengelolaan "
            "persediaan. Skripsi ini melanjutkan konteks tersebut dengan ruang lingkup "
            "yang lebih khusus, yaitu menguji konsistensi transaksi lintas layanan ketika "
            "terjadi kegagalan sistem yang disuntikkan secara terkontrol."
        )
        revised = (
            "Penelitian terdahulu membuktikan bahwa EDA cocok diterapkan pada pengelolaan "
            "persediaan. Penelitian ini tidak menyanggah ataupun membuktikan ulang kelemahan "
            "sistem sebelumnya. Fokus pengujiannya adalah konsistensi transaksi lintas "
            "layanan ketika kegagalan sistem diinjeksi secara terkontrol."
        )
        result = audit(original, revised)
        self.assertNotEqual(result["fidelity_status"], "FAIL")
        self.assertEqual(result["style_status"], "PASS")

    def test_methodological_formula_can_remain_unchanged(self) -> None:
        text = "Hipotesis nol ditolak apabila nilai p lebih kecil daripada 0,05."
        result = audit(text, text)
        self.assertEqual(result["status"], "PASS")

    def test_dense_technical_sentence_is_accessibility_review(self) -> None:
        text = (
            "Perbandingan A, B, dan C menggunakan Friedman test dan post-hoc "
            "Wilcoxon signed-rank A–B, A–C, serta B–C dengan Benjamini–Hochberg "
            "correction, sedangkan Kendall’s W dan matched-pairs rank-biserial "
            "correlation digunakan sebagai effect size."
        )
        result = audit(text, text)
        self.assertEqual(result["fidelity_status"], "PASS")
        self.assertEqual(result["style_status"], "PASS")
        self.assertEqual(result["accessibility_status"], "REVIEW")
        accessibility_checks = checks(result, "accessibility_warnings")
        self.assertIn("tumpukan istilah teknis", accessibility_checks)
        self.assertIn(
            "campuran bahasa yang dapat disederhanakan",
            accessibility_checks,
        )

    def test_clear_technical_sequence_passes_accessibility(self) -> None:
        original = (
            "Perbandingan A, B, dan C menggunakan Friedman test dan Wilcoxon "
            "signed-rank dengan Benjamini–Hochberg correction. Kendall’s W dan "
            "matched-pairs rank-biserial correlation dilaporkan sebagai effect size."
        )
        revised = (
            "Kondisi A, B, dan C dibandingkan sebagai data berpasangan. Uji Friedman "
            "digunakan untuk menilai perbedaan keseluruhan. Perbandingan pasangan "
            "kemudian dilakukan dengan uji Wilcoxon signed-rank. Nilai p disesuaikan "
            "menggunakan koreksi Benjamini–Hochberg. Kendall’s W dan matched-pairs "
            "rank-biserial correlation dilaporkan sebagai ukuran efek agar besar "
            "perbedaan dapat dibaca bersama nilai p."
        )
        result = audit(original, revised)
        self.assertNotEqual(result["fidelity_status"], "FAIL")
        self.assertEqual(result["style_status"], "PASS")
        self.assertEqual(result["accessibility_status"], "PASS")

    def test_removed_named_methods_require_fidelity_review(self) -> None:
        result = audit(
            "Perbedaan dinilai dengan uji Friedman dan uji Wilcoxon signed-rank.",
            "Perbedaan dinilai dengan beberapa uji statistik.",
        )
        self.assertEqual(result["fidelity_status"], "REVIEW")
        self.assertIn(
            "identitas istilah teknis",
            checks(result, "fidelity_warnings"),
        )

    def test_equivalent_technical_padanan_do_not_trigger_identity_warning(self) -> None:
        result = audit(
            "Effect size dan confidence interval dilaporkan bersama p-value.",
            "Ukuran efek dan interval kepercayaan dilaporkan bersama nilai p.",
        )
        self.assertNotIn(
            "identitas istilah teknis",
            checks(result, "fidelity_warnings"),
        )

    def test_unexplained_acronym_is_accessibility_review(self) -> None:
        text = "Sistem menggunakan EDA untuk mengirim peristiwa antarlayanan."
        result = audit(text, text)
        self.assertEqual(result["accessibility_status"], "REVIEW")
        self.assertIn(
            "singkatan belum diperkenalkan",
            checks(result, "accessibility_warnings"),
        )

    def test_defined_acronym_does_not_trigger_accessibility_review(self) -> None:
        text = (
            "Event-Driven Architecture (EDA) mengatur pertukaran peristiwa "
            "antarlayanan."
        )
        result = audit(text, text)
        self.assertEqual(result["accessibility_status"], "PASS")

    def test_expert_audience_relaxes_acronym_alarm(self) -> None:
        text = "EDA mengatur pertukaran peristiwa antarlayanan."
        result = audit(text, text, audience="pakar")
        self.assertEqual(result["accessibility_status"], "PASS")

    def test_expert_audience_accepts_compact_method_inventory(self) -> None:
        text = (
            "Perbandingan menggunakan Friedman test, Wilcoxon signed-rank, "
            "Benjamini–Hochberg correction, Kendall’s W, dan matched-pairs "
            "rank-biserial correlation sebagai effect size."
        )
        result = audit(text, text, audience="pakar")
        self.assertEqual(result["accessibility_status"], "PASS")

    def test_avoidable_language_mixing_requires_review(self) -> None:
        text = (
            "Setiap request dipantau pada load level selama fault testing, "
            "kemudian result disimpan."
        )
        result = audit(text, text)
        self.assertEqual(result["accessibility_status"], "REVIEW")
        self.assertIn(
            "campuran bahasa yang dapat disederhanakan",
            checks(result, "accessibility_warnings"),
        )

    def test_code_labels_are_excluded_from_language_mixing_alarm(self) -> None:
        text = (
            "Label `request`, `fault`, dan `result` dipertahankan sebagai nama kolom."
        )
        result = audit(text, text)
        self.assertEqual(result["accessibility_status"], "PASS")

    def test_repeated_explanation_template_requires_review(self) -> None:
        text = (
            "Uji Friedman digunakan untuk menilai perbedaan keseluruhan. "
            "Uji Wilcoxon digunakan untuk membandingkan pasangan. "
            "Koreksi Benjamini–Hochberg digunakan untuk menyesuaikan nilai p."
        )
        result = audit(text, text)
        self.assertEqual(result["accessibility_status"], "REVIEW")
        self.assertIn(
            "pola penjelasan mekanis",
            checks(result, "accessibility_warnings"),
        )

    def test_functional_variation_avoids_explanation_template_alarm(self) -> None:
        text = (
            "Perbedaan keseluruhan dinilai dengan uji Friedman. Jika analisis perlu "
            "dilanjutkan, pasangan kondisi dibandingkan menggunakan uji Wilcoxon. "
            "Nilai p kemudian disesuaikan dengan koreksi Benjamini–Hochberg."
        )
        result = audit(text, text)
        self.assertNotIn(
            "pola penjelasan mekanis",
            checks(result, "accessibility_warnings"),
        )

    def test_parenthetical_overload_requires_review_for_general_reader(self) -> None:
        text = (
            "Ukuran dilaporkan sebagai rasio (nilai relatif), median (nilai tengah), "
            "dan rentang (nilai minimum–maksimum) pada setiap kelompok."
        )
        result = audit(text, text, audience="umum")
        self.assertEqual(result["accessibility_status"], "REVIEW")
        self.assertIn(
            "beban tanda kurung",
            checks(result, "accessibility_warnings"),
        )

    def test_passive_nominal_chain_requires_style_review(self) -> None:
        text = "Pelaksanaan pengujian dilakukan dengan menggunakan k6."
        result = audit(text, text)
        self.assertIn("rantai pasif nominal", checks(result, "style_warnings"))

    def test_concise_methodological_passive_is_not_flagged(self) -> None:
        text = "Setiap skenario diuji 30 kali pada tingkat beban yang sama."
        result = audit(text, text)
        self.assertNotIn("rantai pasif nominal", checks(result, "style_warnings"))

    def test_unoperationalized_performance_claim_is_domain_review(self) -> None:
        text = "Arsitektur yang diusulkan lebih cepat dan lebih stabil."
        result = audit(text, text, domain="informatika")
        self.assertIn(
            "klaim performa tanpa operasionalisasi",
            checks(result, "style_warnings"),
        )

    def test_general_domain_skips_informatics_performance_alarm(self) -> None:
        text = "Program pendampingan dinilai lebih efektif oleh peserta."
        result = audit(text, text)
        self.assertNotIn(
            "klaim performa tanpa operasionalisasi",
            checks(result, "style_warnings"),
        )

    def test_performance_claim_with_metric_value_and_condition_passes_alarm(self) -> None:
        text = (
            "Pada beban 200 permintaan per detik, sistem lebih cepat karena "
            "latensi p95 turun dari 240 ms menjadi 180 ms."
        )
        result = audit(text, text, domain="informatika")
        self.assertNotIn(
            "klaim performa tanpa operasionalisasi",
            checks(result, "style_warnings"),
        )

    def test_cited_performance_claim_is_not_treated_as_unsupported(self) -> None:
        text = "Sistem lebih stabil menurut Rahman (2024)."
        result = audit(text, text, domain="informatika")
        self.assertNotIn(
            "klaim performa tanpa operasionalisasi",
            checks(result, "style_warnings"),
        )

    def test_proposal_target_is_not_treated_as_observed_result(self) -> None:
        text = (
            "Pengujian akan menilai apakah sistem lebih cepat berdasarkan "
            "latensi p95."
        )
        result = audit(text, text, domain="informatika")
        self.assertNotIn(
            "klaim performa tanpa operasionalisasi",
            checks(result, "style_warnings"),
        )

    def test_new_technical_version_requires_fidelity_review(self) -> None:
        result = audit(
            "Sistem menggunakan PostgreSQL.",
            "Sistem menggunakan PostgreSQL 15.",
            domain="informatika",
        )
        self.assertIn(
            "spesifisitas teknis baru",
            checks(result, "fidelity_warnings"),
        )

    def test_new_identifier_and_event_require_fidelity_review(self) -> None:
        result = audit(
            "Layanan mencatat event pembayaran.",
            "Layanan mencatat event `PaymentFailed` pada kolom `event_id`.",
            domain="informatika",
        )
        self.assertIn(
            "spesifisitas teknis baru",
            checks(result, "fidelity_warnings"),
        )

    def test_retained_technical_specificity_does_not_warn(self) -> None:
        text = "PostgreSQL 15 menyimpan event `PaymentFailed`."
        result = audit(text, text, domain="informatika")
        self.assertNotIn(
            "spesifisitas teknis baru",
            checks(result, "fidelity_warnings"),
        )

    def test_repeated_paragraph_transition_requires_review(self) -> None:
        text = (
            "Selain itu, sistem mencatat transaksi.\n\n"
            "Selain itu, layanan mengirim event.\n\n"
            "Selain itu, worker membaca antrean."
        )
        result = audit(text, text)
        self.assertIn(
            "transisi awal paragraf berulang",
            checks(result, "style_warnings"),
        )

    def test_single_paragraph_transition_is_not_banned(self) -> None:
        text = "Selain itu, sistem mencatat transaksi."
        result = audit(text, text)
        self.assertNotIn(
            "transisi awal paragraf berulang",
            checks(result, "style_warnings"),
        )

    def test_decorative_abstract_triad_requires_review(self) -> None:
        text = "Sistem dirancang agar efektif, efisien, dan optimal."
        result = audit(text, text)
        self.assertIn("triad abstrak dekoratif", checks(result, "style_warnings"))

    def test_official_three_conditions_are_not_a_decorative_triad(self) -> None:
        text = (
            "Kondisi A menggunakan monolit; Kondisi B menggunakan EDA; "
            "Kondisi C menggunakan OCC, Saga, dan transactional outbox."
        )
        result = audit(text, text, domain="informatika", audience="pakar")
        self.assertNotIn("triad abstrak dekoratif", checks(result, "style_warnings"))

    def test_inconsistent_foreign_term_format_requires_domain_review(self) -> None:
        text = (
            "Mekanisme *transactional outbox* mencatat pesan. "
            "Transactional outbox kemudian dibaca oleh worker."
        )
        result = audit(text, text, domain="informatika")
        self.assertIn(
            "format istilah teknis tidak konsisten",
            checks(result, "style_warnings"),
        )

    def test_consistent_foreign_term_format_is_not_flagged(self) -> None:
        text = (
            "Mekanisme *transactional outbox* mencatat pesan. "
            "Pesan *transactional outbox* kemudian dibaca oleh worker."
        )
        result = audit(text, text, domain="informatika")
        self.assertNotIn(
            "format istilah teknis tidak konsisten",
            checks(result, "style_warnings"),
        )

    def test_product_and_language_names_are_not_forced_to_italics(self) -> None:
        text = "PostgreSQL menyimpan data yang diproses oleh layanan JavaScript."
        result = audit(text, text, domain="informatika")
        self.assertNotIn(
            "format istilah teknis tidak konsisten",
            checks(result, "style_warnings"),
        )

    def test_mixed_padanan_requires_domain_review(self) -> None:
        text = "Setiap request masuk ke antrean. Permintaan kemudian diproses."
        result = audit(text, text, domain="informatika")
        self.assertIn("padanan istilah bercampur", checks(result, "style_warnings"))

    def test_code_label_is_excluded_from_mixed_padanan(self) -> None:
        text = "Kolom `request` menyimpan identitas permintaan."
        result = audit(text, text, domain="informatika")
        self.assertNotIn("padanan istilah bercampur", checks(result, "style_warnings"))

    def test_impersonal_voice_flags_personal_subject(self) -> None:
        text = "Kami menguji setiap skenario sebanyak 30 kali."
        result = audit(text, text, voice="impersonal")
        self.assertIn(
            "suara personal pada profil impersonal",
            checks(result, "style_warnings"),
        )

    def test_default_voice_does_not_ban_first_person(self) -> None:
        text = "Kami menguji setiap skenario sebanyak 30 kali."
        result = audit(text, text)
        self.assertNotIn(
            "suara personal pada profil impersonal",
            checks(result, "style_warnings"),
        )

    def test_accessibility_review_has_nonzero_exit_code(self) -> None:
        text = "Sistem menggunakan EDA untuk mengirim peristiwa antarlayanan."
        result = audit(text, text)
        self.assertEqual(exit_code_for_result(result), 3)
        self.assertEqual(exit_code_for_result(result, strict=True), 1)

    def test_unknown_audience_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            audit("Teks tetap.", "Teks tetap.", audience="semua-orang")

    def test_unknown_domain_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            audit("Teks tetap.", "Teks tetap.", domain="teknik-semua")

    def test_unknown_voice_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            audit("Teks tetap.", "Teks tetap.", voice="tanpa-subjek")

    def test_review_has_nonzero_exit_code(self) -> None:
        result = audit(
            "Penelitian dilakukan di Universitas Indonesia.",
            "Penelitian dilakukan di Universitas Airlangga.",
        )
        self.assertEqual(exit_code_for_result(result), 3)
        self.assertEqual(exit_code_for_result(result, strict=True), 1)

    def test_pass_and_fail_exit_codes(self) -> None:
        passed = audit("Data tetap.", "Data tetap.")
        failed = audit("Nilai 10%.", "Nilai 20%.")
        self.assertEqual(exit_code_for_result(passed), 0)
        self.assertEqual(exit_code_for_result(failed), 1)


if __name__ == "__main__":
    unittest.main()
