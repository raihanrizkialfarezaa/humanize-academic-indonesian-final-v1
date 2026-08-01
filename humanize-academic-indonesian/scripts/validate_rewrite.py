#!/usr/bin/env python3
"""Audit preservation, rhetorical, and accessibility risks in Indonesian rewrites.

The auditor is deliberately deterministic. It does not classify authorship,
predict detector scores, or prove semantic equivalence. It normalizes harmless
formatting variants, checks protected anchors globally, and then checks whether
numbers, citations, and semantic markers remain attached to comparable local
claims. Accessibility signals are audience-calibrated alarms, never instructions
to delete technical terms.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


NUMBER_RE = re.compile(
    r"(?<![\w])(?P<currency>Rp\s*)?(?P<sign>[+-]?)"
    r"(?P<number>(?:\d{1,3}(?:[.,\s]\d{3})+|\d+)(?:[.,]\d+)?)"
    r"(?P<unit>\s*%|\s*(?:ms|detik|menit|jam|hari|minggu|bulan|tahun|"
    r"MB|GB|TB|Hz|kHz|MHz|GHz|VA|W|kW|V|A|°C))?",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s)>\]}]+", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
NUMERIC_CITATION_RE = re.compile(r"\[(?:\s*\d+[a-z]?(?:\s*[-,;]\s*\d+[a-z]?)*\s*)\]")
PANDOC_CITATION_RE = re.compile(r"\[(?:[^\]\n]*?)@[\w:./-]+(?:[^\]\n]*?)\]")
LATEX_CITATION_RE = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*)?\{[^}]+\}")
AUTHOR = r"[A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ'’-]+"
AUTHOR_GROUP = (
    rf"{AUTHOR}(?:\s*,\s*{AUTHOR})*"
    rf"(?:\s*,?\s*(?:(?:dan|&)\s+{AUTHOR}|dkk\.|et\s+al\.))?"
)
NARRATIVE_CITATION_RE = re.compile(
    rf"(?P<authors>{AUTHOR_GROUP})\s*\((?P<year>(?:19|20)\d{{2}}[a-z]?)\)"
)
PAREN_CITATION_RE = re.compile(
    r"\((?P<body>[^()\n]{0,220}\b(?:19|20)\d{2}[a-z]?[^()\n]{0,120})\)"
)
PAREN_CITATION_ITEM_RE = re.compile(
    rf"(?P<authors>{AUTHOR_GROUP})\s*,?\s*(?P<year>(?:19|20)\d{{2}}[a-z]?)"
)
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9_-]{1,15}\b")
MULTIWORD_PROPER_RE = re.compile(
    r"\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ'’-]+"
    r"(?:\s+(?:(?:bin|binti|van|von|de|da|al-)\s+)?"
    r"[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ'’-]+){1,4}\b"
)
INLINE_MATH_RE = re.compile(r"(?<!\\)\$[^$\n]+(?<!\\)\$|\\\([^\n]+?\\\)|\\\[[\s\S]+?\\\]")
BLOCK_MATH_RE = re.compile(
    r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}[\s\S]+?"
    r"\\end\{(?:equation\*?|align\*?|gather\*?)\}"
)
QUOTE_RE = re.compile(r"“[^”\n]+”|\"[^\"\n]+\"")
CROSS_REFERENCE_RE = re.compile(
    r"\b(?:Tabel|Gambar|Persamaan|Lampiran|Bab|Bagian)\s+"
    r"(?:[A-Z]?\d+(?:[.:-]\d+)*|[IVXLCDM]+)\b",
    re.IGNORECASE,
)
STAT_EXPRESSION_RE = re.compile(
    r"(?:\b(?:p|q|r|R|t|F|U|W|z|Z|χ²|chi-square)\s*"
    r"(?:\([^\n)]{1,30}\))?\s*(?:=|<|>|≤|≥)\s*"
    r"[+-]?(?:\d+(?:[,.]\d+)?|\.\d+))|"
    r"(?:\b(?:CI|IK)\s*\d*\s*%?\s*[:=]?\s*\[[^\]\n]+\])",
    re.IGNORECASE,
)

HIDDEN_CHARS = {
    "\u00ad": "SOFT HYPHEN",
    "\u034f": "COMBINING GRAPHEME JOINER",
    "\u061c": "ARABIC LETTER MARK",
    "\u180e": "MONGOLIAN VOWEL SEPARATOR",
    "\u200b": "ZERO WIDTH SPACE",
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
    "\u200e": "LEFT-TO-RIGHT MARK",
    "\u200f": "RIGHT-TO-LEFT MARK",
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202c": "POP DIRECTIONAL FORMATTING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2060": "WORD JOINER",
    "\u2061": "FUNCTION APPLICATION",
    "\u2062": "INVISIBLE TIMES",
    "\u2063": "INVISIBLE SEPARATOR",
    "\u2064": "INVISIBLE PLUS",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
    "\ufeff": "ZERO WIDTH NO-BREAK SPACE/BOM",
}

SEMANTIC_PATTERNS: dict[str, re.Pattern[str]] = {
    "negasi": re.compile(r"\b(?:tidak|tak|bukan|tanpa|gagal|ketiadaan)\b", re.I),
    "belum": re.compile(r"\bbelum\b", re.I),
    "pengecualian": re.compile(r"\bkecuali\b", re.I),
    "ketidakpastian": re.compile(
        r"\b(?:mungkin|barangkali|dapat|bisa|mampu|berpotensi|diduga|"
        r"diperkirakan|tampaknya|cenderung|kemungkinan)\b",
        re.I,
    ),
    "bukti_indikatif": re.compile(
        r"\b(?:mengindikasikan|menunjukkan|menyiratkan|mengisyaratkan|"
        r"mendukung|mengarah\s+pada)\b",
        re.I,
    ),
    "kepastian_kuat": re.compile(
        r"\b(?:membuktikan|memastikan|terbukti|pasti|niscaya|"
        r"tanpa\s+keraguan)\b",
        re.I,
    ),
    "asosiasi": re.compile(
        r"\b(?:berkaitan|terkait|berhubungan|berasosiasi|berkorelasi|"
        r"korelasi|asosiasi)\b",
        re.I,
    ),
    "kausalitas": re.compile(
        r"\b(?:menyebabkan|mengakibatkan|memicu|memengaruhi|mempengaruhi|"
        r"berdampak|disebabkan|diakibatkan|karena|sehingga|akibat)\b",
        re.I,
    ),
    "syarat": re.compile(
        r"\b(?:jika|apabila|bila|asalkan|dengan\s+syarat|bergantung\s+pada)\b",
        re.I,
    ),
    "cakupan_parsial": re.compile(
        r"\b(?:sebagian|beberapa|mayoritas|minoritas|umumnya|kebanyakan)\b",
        re.I,
    ),
    "cakupan_universal": re.compile(
        r"\b(?:semua|seluruh|setiap|senantiasa|selalu|sepenuhnya)\b",
        re.I,
    ),
    "pembatas_kuantitas": re.compile(
        r"\b(?:hanya|setidaknya|sekurang-kurangnya|paling\s+sedikit|"
        r"paling\s+banyak|maksimal|minimal)\b",
        re.I,
    ),
    "temporalitas": re.compile(
        r"\b(?:sebelum|sesudah|setelah|selama|ketika|sejak|hingga|"
        r"sementara|kemudian|sebelumnya)\b",
        re.I,
    ),
    "atribusi": re.compile(
        r"\b(?:menurut|menyatakan|melaporkan|berpendapat|menemukan|"
        r"mengemukakan|menjelaskan|menegaskan|mengklaim)\b",
        re.I,
    ),
}

CRITICAL_LOCAL_CATEGORIES = {
    "negasi",
    "belum",
    "pengecualian",
    "kepastian_kuat",
    "asosiasi",
    "kausalitas",
    "syarat",
    "cakupan_parsial",
    "cakupan_universal",
    "pembatas_kuantitas",
    "temporalitas",
}

STYLE_PATTERNS: dict[str, re.Pattern[str]] = {
    "pembuka generik": re.compile(
        r"\b(?:pada era (?:digital|globalisasi)|seiring dengan perkembangan zaman|"
        r"tidak dapat dimungkiri bahwa|di tengah pesatnya perkembangan)\b",
        re.I,
    ),
    "ungkapan mubazir": re.compile(
        r"\b(?:adalah merupakan|dapat mampu|guna untuk|demi untuk|agar supaya|"
        r"bertujuan untuk dapat|diharapkan dapat mampu)\b",
        re.I,
    ),
    "penghubung di mana": re.compile(r",\s*di mana\b", re.I),
    "penghubung yang mana": re.compile(r",\s*yang mana\b", re.I),
    "rujukan abstrak": re.compile(
        r"\b(?:hal ini|kondisi tersebut|fenomena ini|konteks tersebut|"
        r"aspek ini|upaya tersebut)\b",
        re.I,
    ),
    "pemposisian defensif": re.compile(
        r"\b(?:tidak\s+(?:diarahkan|dimaksudkan)\s+untuk\s+"
        r"(?:menyanggah|membuktikan\s+kelemahan)|justru\s+menjadi\s+"
        r"(?:dasar|landasan|pijakan))\b",
        re.I,
    ),
    "pembeda abstrak": re.compile(
        r"\b(?:ruang\s+lingkup|cakupan)\s+(?:yang\s+)?lebih\s+"
        r"(?:khusus|spesifik|terarah)\s*,?\s*(?:yaitu|yakni)\b",
        re.I,
    ),
    "ragam nonakademik": re.compile(
        r"\b(?:nggak|gak|banget|kayak|bikin|kok|dong|aja|deh)\b",
        re.I,
    ),
    "rantai pasif nominal": re.compile(
        r"\b(?:pelaksanaan|proses\s+pelaksanaan|kegiatan|pengujian|"
        r"perancangan|implementasi|penerapan)\b[^.!?\n]{0,90}?"
        r"\b(?:dilakukan|dilaksanakan)\b[^.!?\n]{0,55}?"
        r"\b(?:dengan\s+)?(?:menggunakan|melakukan|pemberian|penerapan)\b",
        re.I,
    ),
}

FORMULAIC_POSITIONING_RE = re.compile(
    r"(?:menjadi|merupakan)\s+(?:dasar|landasan|pijakan)[\s\S]{0,260}?"
    r"(?:melanjutkan|meneruskan)[\s\S]{0,180}?"
    r"(?:konteks|ruang\s+lingkup|cakupan)",
    re.I,
)
META_SUBJECT_RE = re.compile(
    r"^(?:menurut\s+)?(?:penelitian|studi|kajian|skripsi)\s+"
    r"(?:ini|tersebut)\b",
    re.I,
)
DELAYED_PAYLOAD_RE = re.compile(
    r"^(?:berdasarkan|dengan\s+mengacu\s+pada|sehubungan\s+dengan)\b"
    r".{0,120}?\b(?:penelitian|studi|kajian)\s+ini\b"
    r".{0,100}?\b(?:diarahkan|bertujuan|dilakukan)\b",
    re.I,
)
ABSTRACT_BRIDGE_RE = re.compile(
    r"\b(?:fokus|dasar|landasan|pijakan|konteks|arah|aspek|"
    r"ruang\s+lingkup|cakupan)\b",
    re.I,
)

PARAGRAPH_TRANSITION_RE = re.compile(
    r"^(?:selain\s+itu|lebih\s+lanjut|di\s+sisi\s+lain|oleh\s+karena\s+itu|"
    r"dengan\s+demikian|berdasarkan\s+hal\s+tersebut|namun\s+demikian)\b",
    re.I,
)
DECORATIVE_TRIAD_RE = re.compile(
    r"\b(?:efektif|efisien|optimal|adaptif|dinamis|robust|komprehensif|"
    r"inovatif|strategis|andal|akurat|stabil)\s*,\s*"
    r"(?:efektif|efisien|optimal|adaptif|dinamis|robust|komprehensif|"
    r"inovatif|strategis|andal|akurat|stabil)\s*,?\s*"
    r"(?:dan|serta)\s+"
    r"(?:efektif|efisien|optimal|adaptif|dinamis|robust|komprehensif|"
    r"inovatif|strategis|andal|akurat|stabil)\b",
    re.I,
)

PERFORMANCE_CLAIM_RE = re.compile(
    r"\b(?:lebih\s+(?:cepat|lambat|aman|stabil|akurat|andal|efektif|efisien|"
    r"optimal|robust|skalabel)|(?:sistem|arsitektur|metode|mekanisme|aplikasi|"
    r"model|layanan|implementasi|kondisi\s+[A-Z])\s+(?:sangat\s+)?"
    r"(?:cepat|aman|stabil|akurat|andal|efektif|efisien|optimal|robust|"
    r"skalabel)|meningkatkan\s+(?:kinerja|"
    r"performa|keandalan|keamanan|akurasi|efisiensi)|menurunkan\s+(?:latensi|"
    r"waktu\s+respons|tingkat\s+kesalahan|jumlah\s+inkonsistensi))\b",
    re.I,
)
PERFORMANCE_METRIC_RE = re.compile(
    r"\b(?:latensi(?:\s+p\d{2})?|waktu\s+respons|throughput|"
    r"permintaan\s+per\s+detik|transaksi\s+per\s+detik|error\s+rate|"
    r"tingkat\s+(?:kesalahan|kegagalan)|akurasi|precision|recall|f1(?:-score)?|"
    r"inkonsistensi|konflik\s+pembaruan|cpu|memori|bandwidth|persentil|"
    r"p\d{2}|tps|rps)\b",
    re.I,
)
PROPOSAL_EVALUATION_RE = re.compile(
    r"\b(?:akan\s+(?:mengukur|menilai|mengevaluasi|menguji)|"
    r"(?:sasaran|tujuan)\s+(?:pengujian|evaluasi)|"
    r"(?:untuk|guna)\s+(?:menilai|menguji|mengevaluasi)\s+apakah|"
    r"dirumuskan\s+sebagai\s+(?:sasaran|hipotesis))\b",
    re.I,
)
RESULT_REFERENCE_RE = re.compile(
    r"\b(?:Tabel|Gambar|Lampiran|log|hasil\s+pengujian|data\s+pengujian)\b",
    re.I,
)
IMPERSONAL_VOICE_RE = re.compile(r"\b(?:saya|kami|penulis|peneliti)\b", re.I)

CODE_RE = re.compile(r"```[\s\S]*?```|`[^`\n]+`")

KNOWN_TECHNICAL_TERM_RE = re.compile(
    r"\b(?:"
    r"Friedman(?:\s+test)?|"
    r"Wilcoxon(?:\s+signed[-– ]rank)?|"
    r"Benjamini[-– ]Hochberg(?:\s+correction)?|"
    r"Bonferroni(?:\s+correction)?|"
    r"Kendall['’]s\s+W|"
    r"(?:matched[-– ]pairs\s+)?rank[-– ]biserial\s+correlation|"
    r"Shapiro[-– ]Wilk|Kolmogorov[-– ]Smirnov|Mann[-– ]Whitney|"
    r"Kruskal[-– ]Wallis|ANOVA|ANCOVA|MANOVA|"
    r"bootstrap(?:\s+BCa)?|Q[-– ]Q\s+plot|"
    r"hazard\s+ratio|confidence\s+interval|interval\s+kepercayaan|"
    r"effect\s+size|ukuran\s+efek|p[- ]?value|nilai\s+p|"
    r"latensi\s+p\d{2}|p\d{2}\s+latency|"
    r"Event[- ]Driven\s+Architecture|circuit\s+breaker|correlation\s+ID|"
    r"optimistic\s+concurrency\s+control|transactional\s+outbox|"
    r"idempoten(?:cy|si)(?:\s+key)?|idempotency\s+key|"
    r"message\s+broker|webhook|race\s+condition|fault\s+injection|"
    r"Saga(?:\s+(?:orchestrator|orchestration))?|microservices?|mikroservis|"
    r"open\s+coding|axial\s+coding|pengodean\s+terbuka|pengodean\s+aksial|"
    r"triangulasi\s+sumber|"
    r"lex\s+specialis\s+derogat\s+legi\s+generali|"
    r"structural\s+equation\s+model(?:ing)?"
    r")\b",
    re.I,
)

TECHNICAL_VERSION_RE = re.compile(
    r"\b(?:PostgreSQL|MySQL|MariaDB|MongoDB|Node(?:\.js)?|Python|Java|"
    r"JavaScript|TypeScript|PHP|Laravel|React|Next\.js|Express|Prisma|"
    r"Sequelize|Redis|Kafka|RabbitMQ|Docker|Kubernetes|Ubuntu|Windows)"
    r"\s+v?\d+(?:\.\d+){0,3}\b",
    re.I,
)
HTTP_ENDPOINT_RE = re.compile(
    r"\b(?:GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s+"
    r"/(?:[A-Za-z0-9_{}:.-]+/?)+",
    re.I,
)
EVENT_NAME_RE = re.compile(
    r"\b(?:event|peristiwa)\s+`?(?P<name>[A-Z][A-Za-z0-9]+)`?\b"
)
CONFIG_ASSIGNMENT_RE = re.compile(
    r"\b(?:timeout|max[_-]?retries|retry[_-]?count|isolation[_-]?level|"
    r"queue[_-]?size|batch[_-]?size)\s*[:=]\s*`?[A-Za-z0-9_.-]+`?\b",
    re.I,
)
INLINE_CODE_TOKEN_RE = re.compile(r"`(?P<token>[^`\n]+)`")
IDENTIFIER_TOKEN_RE = re.compile(
    r"^(?:[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+|"
    r"[a-z]+[A-Z][A-Za-z0-9]*|[A-Z][a-z]+(?:[A-Z][A-Za-z0-9]+)+|"
    r"/(?:[A-Za-z0-9_{}:.-]+/?)+)$"
)

FOREIGN_FORMAT_TERM_RE = re.compile(
    r"\b(?:transactional\s+outbox|optimistic\s+concurrency\s+control|"
    r"race\s+condition|circuit\s+breaker|correlation\s+ID|"
    r"fault\s+injection|message\s+broker|idempotency\s+key)\b",
    re.I,
)

PADANAN_PAIRS: tuple[tuple[str, re.Pattern[str], re.Pattern[str]], ...] = (
    ("request/permintaan", re.compile(r"\brequests?\b", re.I), re.compile(r"\bpermintaan\b", re.I)),
    ("fault/gangguan", re.compile(r"\bfaults?\b", re.I), re.compile(r"\b(?:gangguan|kegagalan)\b", re.I)),
    ("flow/alur", re.compile(r"\bflows?\b", re.I), re.compile(r"\balur\b", re.I)),
    ("result/hasil", re.compile(r"\bresults?\b", re.I), re.compile(r"\bhasil\b", re.I)),
    ("testing/pengujian", re.compile(r"\btesting\b", re.I), re.compile(r"\bpengujian\b", re.I)),
)

DOMAINS = ("umum", "informatika")
VOICES = ("default", "impersonal")
GENERIC_NAMED_TERM_RE = re.compile(
    r"\b(?:uji|koreksi|metode|algoritma|koefisien|indeks|rasio|"
    r"arsitektur|protokol|teori|model)\s+"
    r"[A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ'’–-]{1,}"
    r"(?:\s+[A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ'’–-]+){0,3}\b"
)
FUNCTION_CUE_RE = re.compile(
    r"\b(?:"
    r"(?:digunakan|diterapkan|dipakai|dilaporkan|dihitung|disesuaikan|"
    r"dibandingkan|diukur|dinilai|diperiksa|ditelusuri)\s+"
    r"(?:untuk|sebagai|agar|menggunakan|dengan)|"
    r"(?:untuk|agar)\s+(?:menilai|membandingkan|mengukur|menguji|"
    r"mengendalikan|menyesuaikan|memperkirakan|menentukan|menelusuri|"
    r"mengidentifikasi|memeriksa|menunjukkan|melaporkan|menghubungkan)|"
    r"(?:menilai|membandingkan|mengukur|menguji|mengendalikan|"
    r"menyesuaikan|memperkirakan|menentukan|menelusuri|mengidentifikasi|"
    r"memeriksa|menunjukkan|melaporkan|menghubungkan|mengatur)\b|"
    r"(?:perbandingan|pengukuran|penilaian|pengujian|analisis)\s+"
    r"(?:menggunakan|memakai|dengan)|"
    r"berfungsi\s+sebagai|menunjukkan\s+(?:besar|batas|arah|hubungan)"
    r")",
    re.I,
)
EXPLANATION_TEMPLATE_RE = re.compile(
    r"^(?:"
    r"(?:uji|metode|algoritma|model|teknik|koreksi|koefisien|indeks)\b"
    r".{0,100}?\b(?:digunakan|berfungsi)\s+(?:untuk|sebagai)|"
    r"secara\s+sederhana\b|artinya\b|dengan\s+kata\s+lain\b|"
    r"hal\s+ini\s+berarti\b"
    r")",
    re.I,
)

AVOIDABLE_ENGLISH_TERMS: tuple[tuple[re.Pattern[str], tuple[str, ...]], ...] = (
    (re.compile(r"\brequests?\b", re.I), ("permintaan",)),
    (re.compile(r"\bfaults?\b", re.I), ("gangguan", "kegagalan")),
    (re.compile(r"\blevels?\b", re.I), ("tingkat",)),
    (re.compile(r"\bflows?\b", re.I), ("alur",)),
    (re.compile(r"\bsamples?\b", re.I), ("sampel",)),
    (re.compile(r"\bresults?\b", re.I), ("hasil",)),
    (re.compile(r"\btesting\b", re.I), ("pengujian",)),
    (re.compile(r"\btraining\b", re.I), ("pelatihan",)),
    (re.compile(r"\boutputs?\b", re.I), ("keluaran",)),
    (re.compile(r"\binputs?\b", re.I), ("masukan",)),
    (re.compile(r"\berrors?\b", re.I), ("galat", "kesalahan")),
    (re.compile(r"\buse\s+cases?\b", re.I), ("skenario penggunaan", "kasus penggunaan")),
    (re.compile(r"\bload(?:\s+levels?)?\b", re.I), ("beban", "tingkat beban")),
    (re.compile(r"\bmetrics?\b", re.I), ("metrik",)),
    (re.compile(r"\bfamil(?:y|ies)\b", re.I), ("keluarga",)),
    (re.compile(r"\bcorrections?\b", re.I), ("koreksi", "penyesuaian")),
    (re.compile(r"\btests?\b", re.I), ("uji", "pengujian")),
    (re.compile(r"\beffect\s+sizes?\b", re.I), ("ukuran efek",)),
    (re.compile(r"\bconfidence\s+intervals?\b", re.I), ("interval kepercayaan",)),
    (re.compile(r"\bfalse\s+positives?\b", re.I), ("positif palsu",)),
)

COMMON_ACRONYMS = {
    "DOI", "URL", "URI", "PDF", "ISBN", "ISSN", "HTTP", "HTTPS", "ID",
}

AUDIENCE_SETTINGS: dict[str, dict[str, int]] = {
    "pakar": {
        "technical_stack": 8,
        "method_without_function": 5,
        "unexplained_acronyms": 99,
        "foreign_terms": 6,
        "templates": 5,
        "parentheticals": 5,
    },
    "bidang": {
        "technical_stack": 6,
        "method_without_function": 3,
        "unexplained_acronyms": 2,
        "foreign_terms": 4,
        "templates": 4,
        "parentheticals": 4,
    },
    "lintas-bidang": {
        "technical_stack": 5,
        "method_without_function": 2,
        "unexplained_acronyms": 1,
        "foreign_terms": 3,
        "templates": 3,
        "parentheticals": 3,
    },
    "umum": {
        "technical_stack": 4,
        "method_without_function": 1,
        "unexplained_acronyms": 1,
        "foreign_terms": 2,
        "templates": 2,
        "parentheticals": 2,
    },
}

STOPWORDS = {
    "ada", "adalah", "agar", "akan", "antara", "atau", "bagi", "bahwa",
    "dalam", "dan", "dari", "dengan", "di", "dilakukan", "ini", "itu",
    "juga", "ke", "kepada", "lebih", "melalui", "mengenai", "merupakan",
    "oleh", "pada", "para", "sebagai", "secara", "sebuah", "serta", "suatu",
    "telah", "terhadap", "tersebut", "untuk", "yang", "penelitian", "studi",
    "kajian", "skripsi", "hasil", "menjadi", "memberikan", "melakukan",
    "tetapi", "namun", "sedangkan", "sementara", "adapun",
}


@dataclass(frozen=True)
class Segment:
    text: str
    start: int
    end: int
    index: int


@dataclass(frozen=True)
class RawAnchor:
    kind: str
    key: str
    raw: str
    start: int
    end: int


@dataclass(frozen=True)
class BoundAnchor:
    kind: str
    key: str
    raw: str
    start: int
    end: int
    segment_index: int
    context: frozenset[str]
    segment_text: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_unicode(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", normalize_unicode(value)).strip()


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def overlaps(span: tuple[int, int], blocked: Iterable[tuple[int, int]]) -> bool:
    start, end = span
    return any(start < other_end and end > other_start for other_start, other_end in blocked)


def canonical_authors(value: str) -> str:
    value = normalize_unicode(value).casefold()
    value = re.sub(r"\bet\s+al\.?\b|\bdkk\.?\b", "dkk", value)
    value = value.replace("&", " dan ")
    value = re.sub(r"\b(?:lihat|misalnya|bandingkan)\b", " ", value)
    value = re.sub(r"[^\wà-öø-ÿ'’-]+", " ", value, flags=re.UNICODE)
    return normalize_space(value)


def extract_citations(text: str) -> list[RawAnchor]:
    anchors: list[RawAnchor] = []
    occupied: list[tuple[int, int]] = []

    for kind, pattern, canonicalizer in (
        (
            "sitasi LaTeX",
            LATEX_CITATION_RE,
            lambda raw: "latex:" + ",".join(
                sorted(
                    part.strip().casefold()
                    for part in re.search(r"\{([^}]+)\}", raw).group(1).split(",")  # type: ignore[union-attr]
                )
            ),
        ),
        (
            "sitasi Pandoc",
            PANDOC_CITATION_RE,
            lambda raw: "pandoc:" + ",".join(
                sorted(re.findall(r"@([\w:./-]+)", raw.casefold()))
            ),
        ),
        (
            "sitasi numerik",
            NUMERIC_CITATION_RE,
            lambda raw: "numeric:" + ",".join(re.findall(r"\d+[a-z]?", raw.casefold())),
        ),
    ):
        for match in pattern.finditer(text):
            anchors.append(
                RawAnchor(kind, canonicalizer(match.group(0)), match.group(0), match.start(), match.end())
            )
            occupied.append((match.start(), match.end()))

    narrative_spans: list[tuple[int, int]] = []
    for match in NARRATIVE_CITATION_RE.finditer(text):
        if overlaps((match.start(), match.end()), occupied):
            continue
        key = f"author-year:{canonical_authors(match.group('authors'))}|{match.group('year').casefold()}"
        anchors.append(RawAnchor("sitasi penulis-tahun", key, match.group(0), match.start(), match.end()))
        narrative_spans.append((match.start(), match.end()))
        occupied.append((match.start(), match.end()))

    for outer in PAREN_CITATION_RE.finditer(text):
        if overlaps((outer.start(), outer.end()), occupied):
            continue
        found = False
        for item in PAREN_CITATION_ITEM_RE.finditer(outer.group("body")):
            found = True
            key = f"author-year:{canonical_authors(item.group('authors'))}|{item.group('year').casefold()}"
            anchors.append(
                RawAnchor("sitasi penulis-tahun", key, outer.group(0), outer.start(), outer.end())
            )
        if found:
            occupied.append((outer.start(), outer.end()))

    return sorted(anchors, key=lambda item: (item.start, item.end, item.key))


def canonical_decimal(raw: str, currency: bool = False) -> str:
    raw = raw.replace(" ", "")
    sign = ""
    if raw.startswith(("+", "-")):
        sign, raw = raw[0], raw[1:]

    dots = raw.count(".")
    commas = raw.count(",")
    integer = raw
    fraction = ""

    if dots and commas:
        decimal_separator = "." if raw.rfind(".") > raw.rfind(",") else ","
        thousands_separator = "," if decimal_separator == "." else "."
        integer, fraction = raw.rsplit(decimal_separator, 1)
        integer = integer.replace(thousands_separator, "")
    elif dots or commas:
        separator = "." if dots else ","
        parts = raw.split(separator)
        repeated_thousands = len(parts) > 2 and all(len(part) == 3 for part in parts[1:])
        single_thousands = (
            len(parts) == 2
            and len(parts[1]) == 3
            and parts[0].lstrip("0") not in {"", "+", "-"}
        )
        if repeated_thousands or single_thousands or (currency and len(parts[-1]) == 3):
            integer = "".join(parts)
        else:
            integer, fraction = parts[0], parts[1]

    integer = integer.lstrip("0") or "0"
    fraction = fraction.rstrip("0")
    normalized = sign + integer
    if fraction:
        normalized += "." + fraction
    return normalized


def canonical_number(match: re.Match[str]) -> str:
    currency = bool(match.group("currency"))
    value = canonical_decimal(match.group("sign") + match.group("number"), currency)
    unit = normalize_space(match.group("unit") or "").casefold()
    prefix = "rp:" if currency else "num:"
    return f"{prefix}{value}|{unit}"


def extract_numbers(text: str, citation_spans: Iterable[tuple[int, int]]) -> list[RawAnchor]:
    anchors: list[RawAnchor] = []
    blocked = list(citation_spans)
    for match in NUMBER_RE.finditer(text):
        if overlaps((match.start(), match.end()), blocked):
            continue
        anchors.append(
            RawAnchor("angka/satuan", canonical_number(match), match.group(0), match.start(), match.end())
        )
    return anchors


def canonical_stat(raw: str) -> str:
    value = normalize_space(raw).casefold().replace(" ", "")
    value = re.sub(r"(?<=\d),(?=\d)", ".", value)
    return value


def exact_pattern_anchors(
    text: str,
    kind: str,
    pattern: re.Pattern[str],
    canonicalizer: Callable[[str], str] = normalize_space,
) -> list[RawAnchor]:
    return [
        RawAnchor(kind, canonicalizer(match.group(0)), match.group(0), match.start(), match.end())
        for match in pattern.finditer(text)
    ]


def extract_all_anchors(text: str) -> dict[str, list[RawAnchor]]:
    citations = extract_citations(text)
    result: dict[str, list[RawAnchor]] = defaultdict(list)
    for anchor in citations:
        result[anchor.kind].append(anchor)

    citation_spans = [(item.start, item.end) for item in citations]
    result["angka/satuan"].extend(extract_numbers(text, citation_spans))

    specs: tuple[tuple[str, re.Pattern[str], Callable[[str], str]], ...] = (
        ("URL", URL_RE, lambda raw: raw.rstrip(".,;").casefold()),
        ("DOI", DOI_RE, lambda raw: raw.rstrip(".,;").casefold()),
        ("rujukan silang", CROSS_REFERENCE_RE, lambda raw: normalize_space(raw).casefold()),
        ("ekspresi statistik", STAT_EXPRESSION_RE, canonical_stat),
        ("rumus inline", INLINE_MATH_RE, normalize_space),
        ("rumus blok", BLOCK_MATH_RE, normalize_space),
        ("kutipan langsung", QUOTE_RE, normalize_space),
    )
    for kind, pattern, canonicalizer in specs:
        result[kind].extend(exact_pattern_anchors(text, kind, pattern, canonicalizer))

    for match in re.finditer("×", text):
        result["operator/desain faktorial"].append(
            RawAnchor("operator/desain faktorial", "×", "×", match.start(), match.end())
        )
    return dict(result)


def split_segments(text: str) -> list[Segment]:
    boundary = re.compile(
        r"(?:[.!?;](?:[”\"']|\))?\s+(?=[A-ZÀ-ÖØ-Þ0-9])|\n+|"
        r",\s*(?=(?:sedangkan|tetapi|namun|sementara|adapun)\b)|"
        r"\s+(?=(?:sedangkan|tetapi|namun)\b))",
        re.I,
    )
    segments: list[Segment] = []
    start = 0
    for match in boundary.finditer(text):
        end = match.start()
        chunk = text[start:end].strip(" \t\r\n,;.")
        if chunk:
            leading = len(text[start:end]) - len(text[start:end].lstrip(" \t\r\n,;."))
            actual_start = start + leading
            segments.append(Segment(chunk, actual_start, end, len(segments)))
        start = match.end()
    chunk = text[start:].strip(" \t\r\n,;.")
    if chunk:
        leading = len(text[start:]) - len(text[start:].lstrip(" \t\r\n,;."))
        segments.append(Segment(chunk, start + leading, len(text), len(segments)))
    if not segments and text.strip():
        stripped = text.strip()
        offset = text.find(stripped)
        segments.append(Segment(stripped, offset, offset + len(stripped), 0))
    return segments


def sentence_segments(text: str) -> list[Segment]:
    boundary = re.compile(r"(?:[.!?](?:[”\"']|\))?\s+(?=[A-ZÀ-ÖØ-Þ0-9])|\n+)")
    result: list[Segment] = []
    start = 0
    for match in boundary.finditer(text):
        end = match.start() + (1 if text[match.start()] in ".!?" else 0)
        chunk = text[start:end].strip()
        if chunk:
            actual_start = text.find(chunk, start, end + 1)
            result.append(Segment(chunk, actual_start, actual_start + len(chunk), len(result)))
        start = match.end()
    chunk = text[start:].strip()
    if chunk:
        actual_start = text.find(chunk, start)
        result.append(Segment(chunk, actual_start, actual_start + len(chunk), len(result)))
    return result


def segment_for_offset(segments: list[Segment], offset: int) -> Segment:
    for segment in segments:
        if segment.start <= offset <= segment.end:
            return segment
    return min(segments, key=lambda item: abs(item.start - offset))


def mask_protected(text: str) -> str:
    masked = text
    patterns = (
        LATEX_CITATION_RE,
        PANDOC_CITATION_RE,
        NUMERIC_CITATION_RE,
        NARRATIVE_CITATION_RE,
        PAREN_CITATION_RE,
        URL_RE,
        DOI_RE,
        NUMBER_RE,
        INLINE_MATH_RE,
        BLOCK_MATH_RE,
    )
    for pattern in patterns:
        masked = pattern.sub(" ", masked)
    return masked


def light_normalize_word(word: str) -> str:
    word = normalize_unicode(word).casefold().strip("-_'’")
    for suffix in ("-nya", "nya", "lah", "kah"):
        if word.endswith(suffix) and len(word) > len(suffix) + 3:
            word = word[: -len(suffix)]
            break
    return word


def content_tokens(text: str) -> frozenset[str]:
    masked = mask_protected(text)
    for pattern in SEMANTIC_PATTERNS.values():
        masked = pattern.sub(" ", masked)
    tokens: set[str] = set()
    for raw in re.findall(r"\b[\wÀ-ÖØ-öø-ÿ'’-]+\b", masked, flags=re.UNICODE):
        token = light_normalize_word(raw)
        if not token or token in STOPWORDS:
            continue
        if len(token) == 1 and token not in {"a", "b", "x", "y", "z"}:
            continue
        tokens.add(token)
    return frozenset(tokens)


def context_similarity(left: frozenset[str], right: frozenset[str]) -> tuple[float, int]:
    if not left or not right:
        return 0.0, 0
    common = len(left & right)
    union = len(left | right)
    jaccard = common / union
    containment = common / min(len(left), len(right))
    return 0.7 * jaccard + 0.3 * containment, common


def bind_anchors(
    anchors: dict[str, list[RawAnchor]], segments: list[Segment]
) -> dict[str, list[BoundAnchor]]:
    result: dict[str, list[BoundAnchor]] = defaultdict(list)
    if not segments:
        return result
    for kind, items in anchors.items():
        for item in items:
            segment = segment_for_offset(segments, item.start)
            result[kind].append(
                BoundAnchor(
                    item.kind,
                    item.key,
                    item.raw,
                    item.start,
                    item.end,
                    segment.index,
                    content_tokens(segment.text),
                    segment.text,
                )
            )
    return dict(result)


def compare_anchor_multisets(
    original: dict[str, list[RawAnchor]],
    revised: dict[str, list[RawAnchor]],
    errors: list[dict[str, object]],
) -> None:
    for kind in sorted(set(original) | set(revised)):
        before = Counter(item.key for item in original.get(kind, []))
        after = Counter(item.key for item in revised.get(kind, []))
        if before == after:
            continue
        missing_keys = list((before - after).elements())
        added_keys = list((after - before).elements())
        original_raw = defaultdict(list)
        revised_raw = defaultdict(list)
        for item in original.get(kind, []):
            original_raw[item.key].append(item.raw)
        for item in revised.get(kind, []):
            revised_raw[item.key].append(item.raw)
        errors.append(
            {
                "check": kind,
                "missing": [original_raw[key].pop(0) if original_raw[key] else key for key in missing_keys],
                "added": [revised_raw[key].pop(0) if revised_raw[key] else key for key in added_keys],
                "action": "Pulihkan unsur terlindungi atau verifikasi bahwa perubahan benar-benar ekuivalen.",
            }
        )


def short_context(value: str, limit: int = 180) -> str:
    value = normalize_space(value)
    return value if len(value) <= limit else value[: limit - 1] + "…"


def detect_anchor_binding_swaps(
    original: dict[str, list[BoundAnchor]],
    revised: dict[str, list[BoundAnchor]],
    errors: list[dict[str, object]],
) -> None:
    comparable_kinds = {
        "angka/satuan",
        "sitasi penulis-tahun",
        "sitasi numerik",
        "sitasi Pandoc",
        "sitasi LaTeX",
    }
    for kind in comparable_kinds:
        before = original.get(kind, [])
        after = revised.get(kind, [])
        if len({item.key for item in before}) < 2:
            continue
        if Counter(item.key for item in before) != Counter(item.key for item in after):
            continue

        flagged: set[str] = set()
        for source in before:
            same = [item for item in after if item.key == source.key]
            alternatives = [item for item in after if item.key != source.key]
            if not same or not alternatives:
                continue
            own_score = max(context_similarity(source.context, item.context)[0] for item in same)
            alt_item, alt_score, alt_common = max(
                (
                    (item, *context_similarity(source.context, item.context))
                    for item in alternatives
                ),
                key=lambda item: item[1],
            )
            if alt_score >= 0.72 and alt_common >= 2 and alt_score >= own_score + 0.20:
                signature = f"{kind}:{source.key}"
                if signature in flagged:
                    continue
                flagged.add(signature)
                expected = max(same, key=lambda item: context_similarity(source.context, item.context)[0])
                errors.append(
                    {
                        "check": "ikatan lokal unsur terlindungi",
                        "kind": kind,
                        "anchor": source.raw,
                        "source_claim": short_context(source.segment_text),
                        "revised_claim": short_context(expected.segment_text),
                        "closer_to_other_anchor": alt_item.raw,
                        "risk": "Unsur tetap ada, tetapi konteksnya lebih menyerupai klaim milik unsur lain; periksa kemungkinan pertukaran.",
                    }
                )


def semantic_signature(text: str) -> dict[str, int]:
    return {label: len(list(pattern.finditer(text))) for label, pattern in SEMANTIC_PATTERNS.items()}


def align_segments(
    original: list[Segment], revised: list[Segment]
) -> list[tuple[Segment, Segment, float, int]]:
    candidates: list[tuple[float, int, int, int]] = []
    original_tokens = [content_tokens(item.text) for item in original]
    revised_tokens = [content_tokens(item.text) for item in revised]
    for i, left in enumerate(original_tokens):
        for j, right in enumerate(revised_tokens):
            score, common = context_similarity(left, right)
            if score >= 0.48 and common >= 2:
                candidates.append((score, common, i, j))
    used_left: set[int] = set()
    used_right: set[int] = set()
    aligned: list[tuple[Segment, Segment, float, int]] = []
    for score, common, i, j in sorted(candidates, reverse=True):
        if i in used_left or j in used_right:
            continue
        used_left.add(i)
        used_right.add(j)
        aligned.append((original[i], revised[j], score, common))
    return aligned


def audit_local_semantics(
    original_segments: list[Segment],
    revised_segments: list[Segment],
    original_anchors: dict[str, list[BoundAnchor]],
    revised_anchors: dict[str, list[BoundAnchor]],
    errors: list[dict[str, object]],
    warnings: list[dict[str, object]],
) -> None:
    def citation_map(anchors: dict[str, list[BoundAnchor]]) -> dict[int, Counter[str]]:
        mapped: dict[int, Counter[str]] = defaultdict(Counter)
        for kind, items in anchors.items():
            if not kind.startswith("sitasi"):
                continue
            for item in items:
                mapped[item.segment_index][item.key] += 1
        return mapped

    before_citations = citation_map(original_anchors)
    after_citations = citation_map(revised_anchors)
    before_citation_bag = sum(before_citations.values(), Counter())
    after_citation_bag = sum(after_citations.values(), Counter())

    before_global = semantic_signature("\n".join(item.text for item in original_segments))
    after_global = semantic_signature("\n".join(item.text for item in revised_segments))
    global_changes = {
        label: {"original": before_global[label], "revised": after_global[label]}
        for label in SEMANTIC_PATTERNS
        if before_global[label] != after_global[label]
        and not (
            label == "atribusi"
            and before_citation_bag
            and before_citation_bag == after_citation_bag
        )
    }
    if global_changes:
        warnings.append(
            {
                "check": "inventaris penanda semantik",
                "changes": global_changes,
                "action": "Bandingkan klausa sumber dan revisi; sinonim dapat aman, tetapi kadar dan relasinya harus setara.",
            }
        )

    seen: set[tuple[int, int, tuple[str, ...]]] = set()
    for source, target, score, common in align_segments(original_segments, revised_segments):
        if score < 0.72 or common < 2:
            continue
        before = semantic_signature(source.text)
        after = semantic_signature(target.text)
        changed_labels = [
            label for label in SEMANTIC_PATTERNS if before[label] != after[label]
        ]
        if (
            "atribusi" in changed_labels
            and before_citations.get(source.index)
            and before_citations.get(source.index) == after_citations.get(target.index)
        ):
            changed_labels.remove("atribusi")
        changed = tuple(changed_labels)
        if not changed:
            continue
        key = (source.index, target.index, changed)
        if key in seen:
            continue
        seen.add(key)

        critical = sorted(set(changed) & CRITICAL_LOCAL_CATEGORIES)
        directional = (
            after["kepastian_kuat"] > before["kepastian_kuat"]
            or (
                after["kausalitas"] > before["kausalitas"]
                and after["asosiasi"] < before["asosiasi"]
            )
        )
        item = {
            "check": "ikatan lokal penanda semantik",
            "source_claim": short_context(source.text),
            "revised_claim": short_context(target.text),
            "changed_categories": list(changed),
            "similarity": round(score, 3),
            "action": "Pastikan penanda tetap melekat pada pelaku, tindakan, objek, dan kondisi yang sama.",
        }
        if critical or directional:
            errors.append(item)
        else:
            warnings.append(item)


def audit_entities(original: str, revised: str, warnings: list[dict[str, object]]) -> None:
    before_acronyms = set(ACRONYM_RE.findall(original))
    after_acronyms = set(ACRONYM_RE.findall(revised))
    if before_acronyms != after_acronyms:
        warnings.append(
            {
                "check": "singkatan",
                "missing": sorted(before_acronyms - after_acronyms),
                "added": sorted(after_acronyms - before_acronyms),
            }
        )

    false_leads = {
        "Akurasi", "Berdasarkan", "Biaya", "Dalam", "Hasil", "Jika", "Metode",
        "Model", "Menurut", "Pada", "Penelitian", "Sistem", "Studi", "Tabel",
        "Gambar", "Intervensi", "Setiap", "Tiga", "Dua",
    }

    def proper_names(text: str) -> set[str]:
        names: set[str] = set()
        for candidate in MULTIWORD_PROPER_RE.findall(text):
            parts = candidate.split()
            if parts[0] in false_leads or any(part == "Rp" for part in parts):
                continue
            names.add(candidate)
        return names

    before_names = proper_names(original)
    after_names = proper_names(revised)
    if before_names != after_names:
        warnings.append(
            {
                "check": "nama/entitas berhuruf kapital",
                "missing": sorted(before_names - after_names),
                "added": sorted(after_names - before_names),
                "action": "Pastikan identitas entitas tidak berubah; abaikan judul biasa yang terjaring.",
            }
        )


def pattern_matches(text: str, pattern: re.Pattern[str]) -> list[dict[str, object]]:
    return [
        {"text": normalize_space(match.group(0)), "line": line_number(text, match.start())}
        for match in pattern.finditer(text)
    ]


def mask_code(text: str) -> str:
    return CODE_RE.sub(
        lambda match: re.sub(r"[^\n]", " ", match.group(0)),
        text,
    )


def technical_mentions(text: str) -> list[tuple[int, int, str]]:
    """Return non-overlapping method/term mentions for accessibility alarms."""

    masked = mask_code(text)
    candidates: list[tuple[int, int, str]] = []
    for pattern in (KNOWN_TECHNICAL_TERM_RE, GENERIC_NAMED_TERM_RE):
        for match in pattern.finditer(masked):
            candidates.append((match.start(), match.end(), match.group(0)))
    for match in ACRONYM_RE.finditer(masked):
        if match.group(0) in COMMON_ACRONYMS:
            continue
        if acronym_is_defined(masked, match.group(0), match.start()):
            continue
        candidates.append((match.start(), match.end(), match.group(0)))

    selected: list[tuple[int, int, str]] = []
    for candidate in sorted(
        candidates,
        key=lambda item: (-(item[1] - item[0]), item[0], item[1]),
    ):
        span = (candidate[0], candidate[1])
        if overlaps(span, ((item[0], item[1]) for item in selected)):
            continue
        selected.append(candidate)
    return sorted(selected, key=lambda item: (item[0], item[1]))


def canonical_technical_term(raw: str) -> str:
    value = normalize_space(raw).casefold()
    value = value.replace("–", "-").replace("—", "-").replace("’", "'")
    value = re.sub(r"\s+", " ", value)

    if "friedman" in value:
        return "friedman"
    if "wilcoxon" in value:
        return "wilcoxon-signed-rank" if "signed" in value else "wilcoxon"
    if "benjamini-hochberg" in value:
        return "benjamini-hochberg"
    if "bonferroni" in value:
        return "bonferroni"
    if "kendall" in value and re.search(r"\bw\b", value):
        return "kendall-w"
    if "matched-pairs" in value and "rank-biserial" in value:
        return "matched-pairs-rank-biserial-correlation"
    if "rank-biserial" in value:
        return "rank-biserial-correlation"
    if "shapiro-wilk" in value:
        return "shapiro-wilk"
    if "kolmogorov-smirnov" in value:
        return "kolmogorov-smirnov"
    if "mann-whitney" in value:
        return "mann-whitney"
    if "kruskal-wallis" in value:
        return "kruskal-wallis"
    if value in {"anova", "ancova", "manova"}:
        return value
    if "bootstrap" in value:
        return "bootstrap-bca" if "bca" in value else "bootstrap"
    if re.search(r"\bq-q\s+plot\b", value):
        return "q-q-plot"
    if "hazard ratio" in value:
        return "hazard-ratio"
    if value in {"confidence interval", "interval kepercayaan"}:
        return "confidence-interval"
    if value in {"effect size", "ukuran efek"}:
        return "effect-size"
    if re.fullmatch(r"(?:p[- ]?value|nilai p)", value):
        return "p-value"
    latency = re.search(r"\bp(\d{2})\b", value)
    if latency and ("latensi" in value or "latency" in value):
        return f"latency-p{latency.group(1)}"
    if "event-driven architecture" in value:
        return "event-driven-architecture"
    if "circuit breaker" in value:
        return "circuit-breaker"
    if "correlation id" in value:
        return "correlation-id"
    if "optimistic concurrency control" in value:
        return "optimistic-concurrency-control"
    if "transactional outbox" in value:
        return "transactional-outbox"
    if "idempot" in value:
        return "idempotency-key" if "key" in value else "idempotency"
    if "message broker" in value:
        return "message-broker"
    if value == "webhook":
        return "webhook"
    if "race condition" in value:
        return "race-condition"
    if "fault injection" in value:
        return "fault-injection"
    if value.startswith("saga"):
        return "saga"
    if value in {"microservice", "microservices", "mikroservis"}:
        return "microservices"
    if value in {"open coding", "pengodean terbuka"}:
        return "open-coding"
    if value in {"axial coding", "pengodean aksial"}:
        return "axial-coding"
    if value == "triangulasi sumber":
        return "source-triangulation"
    if value == "lex specialis derogat legi generali":
        return "lex-specialis"
    if value.startswith("structural equation model"):
        return "structural-equation-modeling"
    return re.sub(r"[^\w]+", "-", value).strip("-")


def technical_term_inventory(
    text: str,
) -> tuple[Counter[str], dict[str, list[str]]]:
    masked = mask_code(text)
    inventory: Counter[str] = Counter()
    raw_by_key: dict[str, list[str]] = defaultdict(list)
    for match in KNOWN_TECHNICAL_TERM_RE.finditer(masked):
        key = canonical_technical_term(match.group(0))
        inventory[key] += 1
        raw_by_key[key].append(normalize_space(match.group(0)))
    return inventory, raw_by_key


def audit_technical_identity(
    original: str,
    revised: str,
    warnings: list[dict[str, object]],
) -> None:
    before, before_raw = technical_term_inventory(original)
    after, after_raw = technical_term_inventory(revised)
    if before == after:
        return

    missing_keys = list((before - after).elements())
    added_keys = list((after - before).elements())
    missing = [
        before_raw[key].pop(0) if before_raw.get(key) else key for key in missing_keys
    ]
    added = [
        after_raw[key].pop(0) if after_raw.get(key) else key for key in added_keys
    ]
    warnings.append(
        {
            "check": "identitas istilah teknis",
            "missing": missing,
            "added": added,
            "action": (
                "Pastikan nama metode, ukuran, teori, atau pola tidak diganti "
                "dengan kategori umum. Abaikan hanya jika padanannya benar-benar ekuivalen."
            ),
        }
    )


def technical_specificity_inventory(
    text: str,
) -> dict[str, dict[str, str]]:
    """Return distinct implementation details that should not appear from invention."""

    inventory: dict[str, dict[str, str]] = defaultdict(dict)

    def add(kind: str, raw: str) -> None:
        key = normalize_space(raw).casefold().replace("’", "'")
        inventory[kind].setdefault(key, normalize_space(raw))

    for match in TECHNICAL_VERSION_RE.finditer(text):
        add("versi perangkat lunak", match.group(0))
    for match in HTTP_ENDPOINT_RE.finditer(text):
        add("endpoint", match.group(0))
    for match in EVENT_NAME_RE.finditer(text):
        add("nama event", match.group("name"))
    for match in CONFIG_ASSIGNMENT_RE.finditer(text):
        add("konfigurasi", match.group(0))
    for match in INLINE_CODE_TOKEN_RE.finditer(text):
        token = normalize_space(match.group("token"))
        if IDENTIFIER_TOKEN_RE.fullmatch(token):
            add("identifier kode", token)
    return dict(inventory)


def audit_technical_specificity(
    original: str,
    revised: str,
    warnings: list[dict[str, object]],
) -> None:
    before = technical_specificity_inventory(original)
    after = technical_specificity_inventory(revised)
    added: dict[str, list[str]] = {}
    for kind, values in after.items():
        new_keys = sorted(set(values) - set(before.get(kind, {})))
        if new_keys:
            added[kind] = [values[key] for key in new_keys]
    if added:
        warnings.append(
            {
                "check": "spesifisitas teknis baru",
                "added": added,
                "action": (
                    "Pastikan setiap versi, endpoint, event, identifier, atau "
                    "konfigurasi berasal dari naskah, kode, data, sumber, atau "
                    "keterangan pengguna; jangan menerima detail yang hanya lazim."
                ),
            }
        )


def term_format(text: str, start: int, end: int) -> str:
    before = text[start - 1] if start > 0 else ""
    after = text[end] if end < len(text) else ""
    if before == "`" and after == "`":
        return "kode"
    if before in {"*", "_"} and after == before:
        return "miring"
    return "biasa"


def inconsistent_foreign_term_formats(text: str) -> list[dict[str, object]]:
    formats: dict[str, set[str]] = defaultdict(set)
    raws: dict[str, str] = {}
    lines: dict[str, set[int]] = defaultdict(set)
    for match in FOREIGN_FORMAT_TERM_RE.finditer(text):
        key = normalize_space(match.group(0)).casefold()
        formats[key].add(term_format(text, match.start(), match.end()))
        raws.setdefault(key, normalize_space(match.group(0)))
        lines[key].add(line_number(text, match.start()))
    return [
        {
            "term": raws[key],
            "formats": sorted(values),
            "lines": sorted(lines[key]),
        }
        for key, values in sorted(formats.items())
        if len(values) > 1
    ]


def has_definition_pair(text: str, english: re.Pattern[str], indonesian: re.Pattern[str]) -> bool:
    for match in english.finditer(text):
        window = text[max(0, match.start() - 70) : min(len(text), match.end() + 70)]
        if indonesian.search(window) and ("(" in window or ")" in window):
            return True
    return False


def mixed_padanan(text: str) -> list[dict[str, object]]:
    masked = mask_code(text)
    matches: list[dict[str, object]] = []
    for label, english, indonesian in PADANAN_PAIRS:
        english_matches = list(english.finditer(masked))
        indonesian_matches = list(indonesian.finditer(masked))
        if not english_matches or not indonesian_matches:
            continue
        if has_definition_pair(masked, english, indonesian):
            continue
        matches.append(
            {
                "pair": label,
                "english_lines": sorted(
                    {line_number(masked, item.start()) for item in english_matches}
                ),
                "indonesian_lines": sorted(
                    {line_number(masked, item.start()) for item in indonesian_matches}
                ),
            }
        )
    return matches


def audit_informatics_style(revised: str) -> list[dict[str, object]]:
    warnings: list[dict[str, object]] = []
    unsupported_claims: list[dict[str, object]] = []
    for sentence in sentence_segments(revised):
        if not PERFORMANCE_CLAIM_RE.search(sentence.text):
            continue
        if PROPOSAL_EVALUATION_RE.search(sentence.text):
            continue
        has_metric = bool(PERFORMANCE_METRIC_RE.search(sentence.text))
        has_reference = bool(
            RESULT_REFERENCE_RE.search(sentence.text)
            or extract_citations(sentence.text)
        )
        has_value = bool(
            NUMBER_RE.search(sentence.text)
            or STAT_EXPRESSION_RE.search(sentence.text)
        )
        has_evidence = has_reference or has_value
        if has_reference or (has_metric and has_value):
            continue
        unsupported_claims.append(
            {
                "line": line_number(revised, sentence.start),
                "text": short_context(sentence.text),
                "metric_present": has_metric,
                "evidence_present": has_evidence,
            }
        )
    if unsupported_claims:
        warnings.append(
            {
                "check": "klaim performa tanpa operasionalisasi",
                "matches": unsupported_claims,
                "action": (
                    "Ikat klaim hasil pada metrik, pembanding, kondisi, angka, "
                    "tabel, log, atau sumber. Pada proposal, rumuskan sebagai sasaran evaluasi."
                ),
            }
        )

    format_issues = inconsistent_foreign_term_formats(revised)
    if format_issues:
        warnings.append(
            {
                "check": "format istilah teknis tidak konsisten",
                "matches": format_issues,
                "action": (
                    "Bedakan istilah asing, nama resmi, dan identifier; ikuti EYD "
                    "serta gaya selingkung tanpa memaksa nama produk menjadi miring."
                ),
            }
        )

    padanan_issues = mixed_padanan(revised)
    if padanan_issues:
        warnings.append(
            {
                "check": "padanan istilah bercampur",
                "matches": padanan_issues,
                "action": (
                    "Pilih satu padanan untuk satu konsep. Pertahankan bentuk Inggris "
                    "hanya jika merupakan label, kode, atau istilah resmi."
                ),
            }
        )
    return warnings


def is_markdown_heading(text: str, offset: int) -> bool:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end < 0:
        end = len(text)
    return text[start:end].lstrip().startswith("#")


def acronym_is_defined(text: str, acronym: str, first_offset: int) -> bool:
    escaped = re.escape(acronym)
    long_form_first = re.compile(
        rf"(?:[A-Za-zÀ-ÖØ-öø-ÿ][\wÀ-ÖØ-öø-ÿ'’–-]*[ \t]+)"
        rf"{{1,10}}\({escaped}\)"
    )
    acronym_first = re.compile(
        rf"\b{escaped}\s*\((?=[^)\n]*[a-zà-öø-ÿ])[^)\n]{{3,120}}\)"
    )
    for pattern in (long_form_first, acronym_first):
        for match in pattern.finditer(text):
            if match.start() <= first_offset <= match.end():
                return True
            if match.end() <= first_offset:
                return True
    return False


def unexplained_acronyms(text: str) -> list[dict[str, object]]:
    masked = mask_code(text)
    first_matches: dict[str, re.Match[str]] = {}
    for match in ACRONYM_RE.finditer(masked):
        acronym = match.group(0)
        if acronym in COMMON_ACRONYMS or is_markdown_heading(masked, match.start()):
            continue
        first_matches.setdefault(acronym, match)

    result: list[dict[str, object]] = []
    for acronym, match in sorted(first_matches.items(), key=lambda item: item[1].start()):
        if acronym_is_defined(masked, acronym, match.start()):
            continue
        result.append(
            {
                "acronym": acronym,
                "line": line_number(masked, match.start()),
            }
        )
    return result


def avoidable_english_matches(text: str) -> list[dict[str, object]]:
    masked = mask_code(text)
    result: list[dict[str, object]] = []
    occupied: list[tuple[int, int]] = []
    for pattern, equivalents in AVOIDABLE_ENGLISH_TERMS:
        for match in pattern.finditer(masked):
            if overlaps((match.start(), match.end()), occupied):
                continue
            window_start = max(0, match.start() - 90)
            window_end = min(len(masked), match.end() + 90)
            window = masked[window_start:window_end].casefold()
            if any(equivalent.casefold() in window for equivalent in equivalents):
                continue
            result.append(
                {
                    "text": match.group(0),
                    "line": line_number(masked, match.start()),
                }
            )
            occupied.append((match.start(), match.end()))
    return result


def audit_accessibility(
    revised: str,
    audience: str = "lintas-bidang",
) -> list[dict[str, object]]:
    """Return contextual readability alarms without deleting technical identity."""

    if audience not in AUDIENCE_SETTINGS:
        raise ValueError(
            f"Unknown audience {audience!r}; choose from {', '.join(AUDIENCE_SETTINGS)}."
        )
    settings = AUDIENCE_SETTINGS[audience]
    warnings: list[dict[str, object]] = []
    sentences = sentence_segments(revised)

    stacked: list[dict[str, object]] = []
    method_without_function: list[dict[str, object]] = []
    parenthetical_load: list[dict[str, object]] = []
    for index, sentence in enumerate(sentences):
        mentions = technical_mentions(sentence.text)
        if len(mentions) >= settings["technical_stack"]:
            stacked.append(
                {
                    "line": line_number(revised, sentence.start),
                    "count": len(mentions),
                    "terms": [normalize_space(item[2]) for item in mentions],
                    "text": short_context(sentence.text),
                }
            )

        previous = sentences[index - 1].text if index else ""
        local_orientation = f"{previous} {sentence.text}"
        if (
            len(mentions) >= settings["method_without_function"]
            and not FUNCTION_CUE_RE.search(local_orientation)
            and len(re.findall(r"\b\w+\b", sentence.text, flags=re.UNICODE)) >= 12
        ):
            method_without_function.append(
                {
                    "line": line_number(revised, sentence.start),
                    "terms": [normalize_space(item[2]) for item in mentions],
                    "text": short_context(sentence.text),
                }
            )

        without_protected = mask_protected(mask_code(sentence.text))
        pairs = len(re.findall(r"\([^()\n]+\)", without_protected))
        if pairs >= settings["parentheticals"]:
            parenthetical_load.append(
                {
                    "line": line_number(revised, sentence.start),
                    "pairs": pairs,
                    "text": short_context(sentence.text),
                }
            )

    if stacked:
        warnings.append(
            {
                "check": "tumpukan istilah teknis",
                "audience": audience,
                "matches": stacked,
                "action": (
                    "Pertahankan nama metode, tetapi pisahkan tujuan, urutan, "
                    "parameter, dan cara membaca sesuai pembaca sasaran."
                ),
            }
        )
    if method_without_function:
        warnings.append(
            {
                "check": "nama metode tanpa fungsi yang cukup",
                "audience": audience,
                "matches": method_without_function,
                "action": (
                    "Pada kemunculan yang menentukan, nyatakan apa yang dinilai, "
                    "dibandingkan, dikendalikan, atau ditunjukkan; jangan mengarang alasan pemilihan."
                ),
            }
        )
    if parenthetical_load:
        warnings.append(
            {
                "check": "beban tanda kurung",
                "audience": audience,
                "matches": parenthetical_load,
                "action": "Pindahkan penjelasan yang membawa gagasan tersendiri ke kalimat baru.",
            }
        )

    acronyms = unexplained_acronyms(revised)
    if len(acronyms) >= settings["unexplained_acronyms"]:
        warnings.append(
            {
                "check": "singkatan belum diperkenalkan",
                "audience": audience,
                "matches": acronyms,
                "action": (
                    "Berikan kepanjangan atau fungsi pada kemunculan penting pertama "
                    "jika tersedia; jangan menebak kepanjangan."
                ),
            }
        )

    foreign_terms = avoidable_english_matches(revised)
    if len(foreign_terms) >= settings["foreign_terms"]:
        warnings.append(
            {
                "check": "campuran bahasa yang dapat disederhanakan",
                "audience": audience,
                "matches": foreign_terms,
                "action": (
                    "Gunakan padanan Indonesia untuk unsur umum, tetapi pertahankan "
                    "nama resmi, label, kode, fungsi, event, dan istilah tanpa padanan setara."
                ),
            }
        )

    template_matches: list[dict[str, object]] = []
    for paragraph_match in re.finditer(r"(?ms)(?:^|\n\s*\n)(.*?)(?=\n\s*\n|\Z)", revised):
        paragraph = paragraph_match.group(1).strip()
        if not paragraph:
            continue
        paragraph_sentences = sentence_segments(paragraph)
        matched_sentences = [
            item for item in paragraph_sentences if EXPLANATION_TEMPLATE_RE.search(item.text.strip())
        ]
        if len(matched_sentences) >= settings["templates"]:
            template_matches.append(
                {
                    "line": line_number(revised, paragraph_match.start(1)),
                    "count": len(matched_sentences),
                    "sentences": [short_context(item.text, 140) for item in matched_sentences],
                }
            )
    if template_matches:
        warnings.append(
            {
                "check": "pola penjelasan mekanis",
                "audience": audience,
                "matches": template_matches,
                "action": (
                    "Variasikan urutan berdasarkan fungsi konsep; jangan mengulang "
                    "'digunakan untuk', 'artinya', atau 'dengan kata lain' sebagai cetakan."
                ),
            }
        )

    return warnings


def audit_style(
    revised: str,
    domain: str = "umum",
    voice: str = "default",
) -> list[dict[str, object]]:
    if domain not in DOMAINS:
        raise ValueError(f"Unknown domain {domain!r}; choose from {', '.join(DOMAINS)}.")
    if voice not in VOICES:
        raise ValueError(f"Unknown voice {voice!r}; choose from {', '.join(VOICES)}.")
    warnings: list[dict[str, object]] = []
    for label, pattern in STYLE_PATTERNS.items():
        matches = pattern_matches(revised, pattern)
        if matches:
            warnings.append({"check": label, "matches": matches})

    positioning = pattern_matches(revised, FORMULAIC_POSITIONING_RE)
    if positioning:
        warnings.append(
            {
                "check": "urutan gerak retoris formulaik",
                "matches": positioning,
                "action": "Nyatakan kontribusi sumber, batas, fokus sekarang, dan sumbu pembeda secara langsung.",
            }
        )

    sentences = sentence_segments(revised)
    meta_flags = [bool(META_SUBJECT_RE.match(item.text.strip())) for item in sentences]
    chains: list[dict[str, object]] = []
    start = 0
    while start < len(sentences):
        if not meta_flags[start]:
            start += 1
            continue
        end = start + 1
        while end < len(sentences) and meta_flags[end]:
            end += 1
        if end - start >= 2:
            chains.append(
                {
                    "line": line_number(revised, sentences[start].start),
                    "sentences": [short_context(item.text, 120) for item in sentences[start:end]],
                }
            )
        start = end
    if chains:
        warnings.append(
            {
                "check": "rantai subjek metadiskursif",
                "matches": chains,
                "action": "Pertimbangkan sumber, objek, mekanisme, kondisi, atau temuan sebagai titik berangkat.",
            }
        )

    delayed = [
        {"line": line_number(revised, item.start), "text": short_context(item.text)}
        for item in sentences
        if DELAYED_PAYLOAD_RE.search(item.text.strip())
    ]
    if delayed:
        warnings.append(
            {
                "check": "muatan konkret terlambat",
                "matches": delayed,
                "action": "Majukan tindakan, objek, kondisi, atau hasil jika bingkai awal tidak membawa batas penting.",
            }
        )

    transition_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for paragraph_match in re.finditer(r"(?ms)(?:^|\n\s*\n)(.*?)(?=\n\s*\n|\Z)", revised):
        paragraph = paragraph_match.group(1).strip()
        if not paragraph:
            continue
        transition = PARAGRAPH_TRANSITION_RE.match(paragraph)
        if transition:
            key = normalize_space(transition.group(0)).casefold()
            transition_groups[key].append(
                {
                    "line": line_number(revised, paragraph_match.start(1)),
                    "text": normalize_space(transition.group(0)),
                }
            )
        paragraph_sentences = sentence_segments(paragraph)
        meta_count = sum(bool(META_SUBJECT_RE.match(item.text.strip())) for item in paragraph_sentences)
        abstract_count = len(ABSTRACT_BRIDGE_RE.findall(paragraph))
        if meta_count >= 2 and abstract_count >= 4:
            warnings.append(
                {
                    "check": "kepadatan abstraksi metadiskursif",
                    "line": line_number(revised, paragraph_match.start(1)),
                    "meta_subjects": meta_count,
                    "abstract_bridges": abstract_count,
                    "action": "Ganti jembatan abstrak dengan jangkar konkret yang sudah tersedia dalam sumber.",
                }
            )
        lengths = [len(re.findall(r"\b\w+\b", item.text)) for item in paragraph_sentences]
        if meta_count >= 2 and len(lengths) >= 3 and max(lengths) - min(lengths) <= 7:
            warnings.append(
                {
                    "check": "ritme seragam dalam gugus metadiskursif",
                    "line": line_number(revised, paragraph_match.start(1)),
                    "sentence_lengths": lengths,
                    "action": "Variasikan struktur hanya berdasarkan fungsi kalimat; jangan mengacak panjang.",
                }
            )

    repeated_transitions = [
        {"transition": key, "occurrences": items}
        for key, items in sorted(transition_groups.items())
        if len(items) >= 3
    ]
    if repeated_transitions:
        warnings.append(
            {
                "check": "transisi awal paragraf berulang",
                "matches": repeated_transitions,
                "action": (
                    "Periksa hubungan antargagasan; hapus penanda yang tidak perlu "
                    "atau pilih hubungan semantis yang benar, bukan sekadar memindahkannya."
                ),
            }
        )

    decorative_triads = pattern_matches(revised, DECORATIVE_TRIAD_RE)
    if decorative_triads:
        warnings.append(
            {
                "check": "triad abstrak dekoratif",
                "matches": decorative_triads,
                "action": (
                    "Pertahankan hanya sifat yang memiliki arti atau ukuran berbeda. "
                    "Jangan memecah daftar resmi, kondisi, variabel, atau tahap prosedur."
                ),
            }
        )

    if domain == "informatika":
        warnings.extend(audit_informatics_style(revised))

    if voice == "impersonal":
        personal_matches = pattern_matches(revised, IMPERSONAL_VOICE_RE)
        if personal_matches:
            warnings.append(
                {
                    "check": "suara personal pada profil impersonal",
                    "matches": personal_matches,
                    "action": (
                        "Gunakan proses, data, sistem, metode, atau komponen sebagai "
                        "subjek jika perannya benar; jangan mengganti semuanya dengan pasif."
                    ),
                }
            )
    return warnings


def audit(
    original: str,
    revised: str,
    audience: str = "lintas-bidang",
    domain: str = "umum",
    voice: str = "default",
) -> dict[str, object]:
    if domain not in DOMAINS:
        raise ValueError(f"Unknown domain {domain!r}; choose from {', '.join(DOMAINS)}.")
    if voice not in VOICES:
        raise ValueError(f"Unknown voice {voice!r}; choose from {', '.join(VOICES)}.")
    fidelity_errors: list[dict[str, object]] = []
    fidelity_warnings: list[dict[str, object]] = []

    original_segments = split_segments(original)
    revised_segments = split_segments(revised)
    original_raw_anchors = extract_all_anchors(original)
    revised_raw_anchors = extract_all_anchors(revised)

    compare_anchor_multisets(original_raw_anchors, revised_raw_anchors, fidelity_errors)
    original_bound = bind_anchors(original_raw_anchors, original_segments)
    revised_bound = bind_anchors(revised_raw_anchors, revised_segments)
    detect_anchor_binding_swaps(original_bound, revised_bound, fidelity_errors)
    audit_local_semantics(
        original_segments,
        revised_segments,
        original_bound,
        revised_bound,
        fidelity_errors,
        fidelity_warnings,
    )
    audit_entities(original, revised, fidelity_warnings)
    audit_technical_identity(original, revised, fidelity_warnings)
    if domain == "informatika":
        audit_technical_specificity(original, revised, fidelity_warnings)

    for character, name in HIDDEN_CHARS.items():
        for match in re.finditer(character, revised):
            fidelity_errors.append(
                {
                    "check": "karakter tersembunyi",
                    "character": name,
                    "line": line_number(revised, match.start()),
                }
            )

    original_words = re.findall(r"\b\w+\b", original, flags=re.UNICODE)
    revised_words = re.findall(r"\b\w+\b", revised, flags=re.UNICODE)
    length_ratio = len(revised_words) / max(len(original_words), 1)
    if length_ratio < 0.65 or length_ratio > 1.50:
        fidelity_warnings.append(
            {
                "check": "perubahan panjang",
                "original_words": len(original_words),
                "revised_words": len(revised_words),
                "ratio": round(length_ratio, 3),
                "action": "Periksa klaim yang hilang atau muncul; perubahan panjang saja tidak membuktikan drift.",
            }
        )

    style_warnings = audit_style(revised, domain=domain, voice=voice)
    accessibility_warnings = audit_accessibility(revised, audience=audience)
    fidelity_status = (
        "FAIL" if fidelity_errors else "REVIEW" if fidelity_warnings else "PASS"
    )
    style_status = "REVIEW" if style_warnings else "PASS"
    accessibility_status = "REVIEW" if accessibility_warnings else "PASS"
    overall_status = (
        "FAIL"
        if fidelity_status == "FAIL"
        else "REVIEW"
        if (
            fidelity_status == "REVIEW"
            or style_status == "REVIEW"
            or accessibility_status == "REVIEW"
        )
        else "PASS"
    )

    return {
        "status": overall_status,
        "fidelity_status": fidelity_status,
        "style_status": style_status,
        "accessibility_status": accessibility_status,
        "audience": audience,
        "domain": domain,
        "voice": voice,
        "fidelity_errors": fidelity_errors,
        "fidelity_warnings": fidelity_warnings,
        "style_warnings": style_warnings,
        "accessibility_warnings": accessibility_warnings,
        # Backward-compatible aliases for callers of the previous validator.
        "errors": fidelity_errors,
        "warnings": fidelity_warnings + style_warnings + accessibility_warnings,
        "note": (
            "Alarm mekanis, bukan bukti kepengarangan, keterbacaan universal, "
            "atau kesetaraan semantik lengkap. Bandingkan klausa sumber dan revisi "
            "berdasarkan pembaca serta konteks disiplin."
        ),
    }


def render_text(result: dict[str, object]) -> str:
    lines = [
        f"STATUS: {result['status']}",
        f"FIDELITY_STATUS: {result['fidelity_status']}",
        f"STYLE_STATUS: {result['style_status']}",
        f"ACCESSIBILITY_STATUS: {result['accessibility_status']}",
        f"AUDIENCE: {result['audience']}",
        f"DOMAIN: {result['domain']}",
        f"VOICE: {result['voice']}",
    ]
    groups = (
        ("FIDELITY_ERROR", "fidelity_errors"),
        ("FIDELITY_WARNING", "fidelity_warnings"),
        ("STYLE_WARNING", "style_warnings"),
        ("ACCESSIBILITY_WARNING", "accessibility_warnings"),
    )
    for label, key in groups:
        for item in result[key]:  # type: ignore[index]
            lines.append(f"{label}: {json.dumps(item, ensure_ascii=False)}")
    lines.append(str(result["note"]))
    return "\n".join(lines)


def exit_code_for_result(result: dict[str, object], strict: bool = False) -> int:
    status = result["status"]
    if status == "PASS":
        return 0
    if status == "FAIL":
        return 1
    return 1 if strict else 3


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit fidelity, rhetorical, and audience-calibrated accessibility "
            "risks in Indonesian academic rewrites."
        )
    )
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 for REVIEW as well as FAIL.",
    )
    parser.add_argument(
        "--audience",
        choices=tuple(AUDIENCE_SETTINGS),
        default="lintas-bidang",
        help=(
            "Calibrate accessibility alarms for pakar, bidang, lintas-bidang "
            "(default), or umum."
        ),
    )
    parser.add_argument(
        "--domain",
        choices=DOMAINS,
        default="umum",
        help=(
            "Use umum (default) or informatika to enable implementation-detail, "
            "performance-claim, and terminology alarms."
        ),
    )
    parser.add_argument(
        "--voice",
        choices=VOICES,
        default="default",
        help=(
            "Use default or impersonal to flag first-person/author subjects when "
            "the house style requires an impersonal voice."
        ),
    )
    args = parser.parse_args()

    try:
        result = audit(
            read_text(args.original),
            read_text(args.revised),
            audience=args.audience,
            domain=args.domain,
            voice=args.voice,
        )
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return exit_code_for_result(result, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
