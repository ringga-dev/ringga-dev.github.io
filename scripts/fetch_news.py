#!/usr/bin/env python3
"""
Fetch berita dari RSS portal berita swasta Indonesia + Google News RSS.
Generates:
- src/data/news.json  (berita: politik, viral, sosial media, kriminal)
- src/data/blog/*.md   (teknologi informasi)

Sumber bersifat independen/swasta (tidak terafiliasi pemerintah):
  Berita: Detik, Kompas, Liputan6, Okezone, Tempo, CNBC Indonesia
  Teknologi: DetikTekno, Kompas Tekno, Liputan6 Tech, Google News RSS

Python stdlib only: urllib, xml.etree.ElementTree, json, re, datetime.
"""

import json
import re
import html
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── Config ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
NEWS_JSON_PATH = REPO_ROOT / "src" / "data" / "news.json"
BLOG_DIR = REPO_ROOT / "src" / "data" / "blog"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ── Sources: Berita (swasta/independen, tidak terafiliasi pemerintah) ──────
# Format: (label, url_rss)
# Hanya sumber yang RSS-nya terkonfirmasi bekerja dimasukkan.
# Sumber government (Kemdikbud, Kemenag, Kemenkominfo, dll.) TIDAK digunakan.

NEWS_SOURCES = [
    ("Detik",         "https://news.detik.com/berita/rss"),
    ("CNBC Indonesia","https://www.cnbcindonesia.com/rss"),
]

# ── Sources: Teknologi ─────────────────────────────────────────────────────
TECH_SOURCES = []

# Tambah Google News RSS untuk topik tech & berita Indonesia (Bahasa Indonesia)
# Google News RSS adalah agregator — menyarikan berita dari banyak sumber swasta.
TECH_GNEWS_QUERIES = [
    ("teknologi informasi 2026",   "Teknologi"),
    ("artificial intelligence AI", "AI"),
    ("open source software",       "Open Source"),
    ("cybersecurity threat",       "Keamanan Siber"),
    ("devops cloud computing",     "DevOps"),
]

# Query berita Indonesia via Google News (seluruh topik, bukan hanya tech)
BERITA_GNEWS_QUERIES = [
    ("politik Indonesia 2026",     "Politik"),
    ("berita viral Indonesia",     "Viral"),
    ("kriminal Indonesia",         "Kriminal"),
    ("ekonomi Indonesia 2026",     "Ekonomi"),
    ("bencana Indonesia 2026",     "Bencana"),
]

# ─── Constants ─────────────────────────────────────────────────────────────

MAX_ITEMS_PER_SOURCE = 3   # maks item per sumber RSS/Query
MAX_NEWS_ITEMS = 15        # maks total items di news.json
MAX_BLOG_NEW = 6           # maks blog post baru per hari
PAST_DAYS = 1              # hanya ambil dalam 24 jam terakhir

# ── Pool gambar per tema (semua ID diverifikasi HTTP 200) ───────────────
# Syarat: satu item berita harus punya gambar BERBEDA dari item lain.
# Picking memakai index Rotary per tema + fallback silang antar tema
# supaya tetap unik walau banyak beritabertema sama.
UNSPLASH_PREFIX = "https://images.unsplash.com/photo-"

NEWS_IMAGE_POOL = {
    "game": [
        f"{UNSPLASH_PREFIX}1542751371-adc38448a05e?w=800&q=80", f"{UNSPLASH_PREFIX}1511512578047-dfb367046420?w=800&q=80", f"{UNSPLASH_PREFIX}1493711662062-fa541adb3fc8?w=800&q=80",
        f"{UNSPLASH_PREFIX}1550745165-9bc0b252726f?w=800&q=80", f"{UNSPLASH_PREFIX}1600080972464-8e5f35f63d08?w=800&q=80", f"{UNSPLASH_PREFIX}1598550476439-6847785fcea6?w=800&q=80",
        f"{UNSPLASH_PREFIX}1612287230202-1ff1d85d1bdf?w=800&q=80", f"{UNSPLASH_PREFIX}1538481199705-c710c4e965fc?w=800&q=80", f"{UNSPLASH_PREFIX}1547394765-185e1e68f34e?w=800&q=80",
        f"{UNSPLASH_PREFIX}1560419015-7c427e8ae5ba?w=800&q=80",
    ],
    "ecommerce": [
        f"{UNSPLASH_PREFIX}1556742049-0cfed4f6a45d?w=800&q=80", f"{UNSPLASH_PREFIX}1556742044-3c52d6e88c62?w=800&q=80", f"{UNSPLASH_PREFIX}1563013544-824ae1b704d3?w=800&q=80",
        f"{UNSPLASH_PREFIX}1523205771623-e0faa4d2813d?w=800&q=80", f"{UNSPLASH_PREFIX}1607083206869-4c7672e72a8a?w=800&q=80", f"{UNSPLASH_PREFIX}1441986300917-64674bd600d8?w=800&q=80",
        f"{UNSPLASH_PREFIX}1472851294608-062f824d29cc?w=800&q=80", f"{UNSPLASH_PREFIX}1519996529931-28324d5a630e?w=800&q=80",
    ],
    "viral": [
        f"{UNSPLASH_PREFIX}1513151233558-d860c5398176?w=800&q=80", f"{UNSPLASH_PREFIX}1522075469751-3a6694fb2f61?w=800&q=80", f"{UNSPLASH_PREFIX}1516467508483-a7212febe31a?w=800&q=80",
        f"{UNSPLASH_PREFIX}1517245386807-bb43f82c33c4?w=800&q=80", f"{UNSPLASH_PREFIX}1495020689067-958852a7765e?w=800&q=80", f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80",
        f"{UNSPLASH_PREFIX}1517841905240-472988babdf9?w=800&q=80", f"{UNSPLASH_PREFIX}1522071820081-009f0129c71c?w=800&q=80",
    ],
    "kriminal": [
        f"{UNSPLASH_PREFIX}1450101499163-c8848c66ca85?w=800&q=80", f"{UNSPLASH_PREFIX}1589829545856-d10d557cf95f?w=800&q=80", f"{UNSPLASH_PREFIX}1589578527966-fdac0f44566c?w=800&q=80",
        f"{UNSPLASH_PREFIX}1568454537842-d933259bb258?w=800&q=80", f"{UNSPLASH_PREFIX}1505664194779-8beaceb93744?w=800&q=80", f"{UNSPLASH_PREFIX}1519681393784-d120267933ba?w=800&q=80",
    ],
    "olahraga": [
        f"{UNSPLASH_PREFIX}1579952363873-27f3bade9f55?w=800&q=80", f"{UNSPLASH_PREFIX}1461896836934-ffe607ba8211?w=800&q=80", f"{UNSPLASH_PREFIX}1574629810360-7efbbe195018?w=800&q=80",
        f"{UNSPLASH_PREFIX}1531415074968-036ba1b575da?w=800&q=80", f"{UNSPLASH_PREFIX}1546519638-68e109498ffc?w=800&q=80", f"{UNSPLASH_PREFIX}1519861531473-9200262188bf?w=800&q=80",
        f"{UNSPLASH_PREFIX}1517649763962-0c623066013b?w=800&q=80", f"{UNSPLASH_PREFIX}1526232761682-d26e03ac148e?w=800&q=80", f"{UNSPLASH_PREFIX}1553778263-73a83bab9b0c?w=800&q=80",
    ],
    "bencana": [
        f"{UNSPLASH_PREFIX}1547683905-f686c993aae5?w=800&q=80", f"{UNSPLASH_PREFIX}1611273426858-450d8e3c9fce?w=800&q=80", f"{UNSPLASH_PREFIX}1473445361085-b9a07f55608b?w=800&q=80",
        f"{UNSPLASH_PREFIX}1500534314209-a25ddb2bd429?w=800&q=80", f"{UNSPLASH_PREFIX}1534274988757-a28bf1a57c17?w=800&q=80", f"{UNSPLASH_PREFIX}1621451537084-482c73073a0f?w=800&q=80",
        f"{UNSPLASH_PREFIX}1519681393784-d120267933ba?w=800&q=80",
    ],
    "pendidikan": [
        f"{UNSPLASH_PREFIX}1509062522246-3755977927d7?w=800&q=80", f"{UNSPLASH_PREFIX}1497633762265-9d179a990aa6?w=800&q=80", f"{UNSPLASH_PREFIX}1503676260728-1c00da094a0b?w=800&q=80",
        f"{UNSPLASH_PREFIX}1546410531-bb4caa6b424d?w=800&q=80", f"{UNSPLASH_PREFIX}1571260899304-425eee4c7efc?w=800&q=80", f"{UNSPLASH_PREFIX}1588072432836-e10032774350?w=800&q=80",
    ],
    "kesehatan": [
        f"{UNSPLASH_PREFIX}1576091160399-112ba8d25d1d?w=800&q=80", f"{UNSPLASH_PREFIX}1516841273335-e39b37888115?w=800&q=80", f"{UNSPLASH_PREFIX}1631217868264-e5b90bb7e133?w=800&q=80",
        f"{UNSPLASH_PREFIX}1584982751601-97dcc096659c?w=800&q=80", f"{UNSPLASH_PREFIX}1505751172876-fa1923c5c528?w=800&q=80", f"{UNSPLASH_PREFIX}1579684385127-1ef15d508118?w=800&q=80",
        f"{UNSPLASH_PREFIX}1538108149393-fbbd81895907?w=800&q=80", f"{UNSPLASH_PREFIX}1559757175-0eb30cd8c063?w=800&q=80",
    ],
    "teknologi": [
        f"{UNSPLASH_PREFIX}1518770660439-4636190af475?w=800&q=80", f"{UNSPLASH_PREFIX}1550751827-4bd374c3f58b?w=800&q=80", f"{UNSPLASH_PREFIX}1555066931-4365d14bab8c?w=800&q=80",
        f"{UNSPLASH_PREFIX}1526374965328-7f61d4dc18c5?w=800&q=80", f"{UNSPLASH_PREFIX}1558494949-ef010cbdcc31?w=800&q=80", f"{UNSPLASH_PREFIX}1555949963-aa79dcee981c?w=800&q=80",
        f"{UNSPLASH_PREFIX}1531297484001-80022131f5a1?w=800&q=80", f"{UNSPLASH_PREFIX}1512941937669-90a1b58e7e9c?w=800&q=80", f"{UNSPLASH_PREFIX}1487058792275-0ad4aaf24ca7?w=800&q=80",
        f"{UNSPLASH_PREFIX}1461749280684-dccba630e2f6?w=800&q=80", f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80", f"{UNSPLASH_PREFIX}1451187580459-43490279c0fa?w=800&q=80",
    ],
    "ekonomi": [
        f"{UNSPLASH_PREFIX}1611974789855-9c2a0a7236a3?w=800&q=80", f"{UNSPLASH_PREFIX}1590283603385-17ffb3a7f29f?w=800&q=80", f"{UNSPLASH_PREFIX}1526304640581-d334cdbbf45e?w=800&q=80",
        f"{UNSPLASH_PREFIX}1579621970563-ebec7560ff3e?w=800&q=80", f"{UNSPLASH_PREFIX}1559526324-4b87b5e36e44?w=800&q=80", f"{UNSPLASH_PREFIX}1541354329998-f4d9a9f9297f?w=800&q=80",
        f"{UNSPLASH_PREFIX}1618044733300-9472054094ee?w=800&q=80",
    ],
    "hiburan": [
        f"{UNSPLASH_PREFIX}1485846234645-a62644f84728?w=800&q=80", f"{UNSPLASH_PREFIX}1492684223066-81342ee5ff30?w=800&q=80", f"{UNSPLASH_PREFIX}1470225620780-dba8ba36b745?w=800&q=80",
        f"{UNSPLASH_PREFIX}1516450360452-9312f5e86fc7?w=800&q=80", f"{UNSPLASH_PREFIX}1459749411175-04bf5292ceea?w=800&q=80", f"{UNSPLASH_PREFIX}1493225457124-a3eb161ffa5f?w=800&q=80",
        f"{UNSPLASH_PREFIX}1506157786151-b8491531f063?w=800&q=80", f"{UNSPLASH_PREFIX}1514525253161-7a46d19cd819?w=800&q=80",
    ],
    "kuliner": [
        f"{UNSPLASH_PREFIX}1414235077428-338989a2e8c0?w=800&q=80", f"{UNSPLASH_PREFIX}1504674900247-0877df9cc836?w=800&q=80", f"{UNSPLASH_PREFIX}1467003909585-2f8a72700288?w=800&q=80",
        f"{UNSPLASH_PREFIX}1546069901-ba9599a7e63c?w=800&q=80", f"{UNSPLASH_PREFIX}1551782450-a2132b4ba21d?w=800&q=80", f"{UNSPLASH_PREFIX}1555939594-58d7cb561ad1?w=800&q=80",
        f"{UNSPLASH_PREFIX}1482049016688-2d3e1b311543?w=800&q=80", f"{UNSPLASH_PREFIX}1565299624946-b28f40a0ae38?w=800&q=80",
    ],
    "transportasi": [
        f"{UNSPLASH_PREFIX}1544620347-c4fd4a3d5957?w=800&q=80", f"{UNSPLASH_PREFIX}1494412685616-a5d310fbb07d?w=800&q=80", f"{UNSPLASH_PREFIX}1473445361085-b9a07f55608b?w=800&q=80",
        f"{UNSPLASH_PREFIX}1513828583688-c52646db42da?w=800&q=80", f"{UNSPLASH_PREFIX}1541888946425-d81bb19240f5?w=800&q=80", f"{UNSPLASH_PREFIX}1502920917128-1aa500764cbd?w=800&q=80",
        f"{UNSPLASH_PREFIX}1533473359331-0135ef1b58bf?w=800&q=80",
    ],
    "pertanian": [
        f"{UNSPLASH_PREFIX}1500382017468-9049fed747ef?w=800&q=80", f"{UNSPLASH_PREFIX}1625246333195-78d9c38ad449?w=800&q=80", f"{UNSPLASH_PREFIX}1464226184884-fa280b87c399?w=800&q=80",
        f"{UNSPLASH_PREFIX}1495107334309-fcf20504a5ab?w=800&q=80", f"{UNSPLASH_PREFIX}1523741543316-beb7fc7023d8?w=800&q=80", f"{UNSPLASH_PREFIX}1471193945509-9ad0617afabf?w=800&q=80",
    ],
    "umum": [
        f"{UNSPLASH_PREFIX}1495020689067-958852a7765e?w=800&q=80", f"{UNSPLASH_PREFIX}1504711434969-e33886168f5c?w=800&q=80", f"{UNSPLASH_PREFIX}1485846234645-a62644f84728?w=800&q=80",
        f"{UNSPLASH_PREFIX}1497366216548-37526070297c?w=800&q=80", f"{UNSPLASH_PREFIX}1521737711867-e3b97375f902?w=800&q=80", f"{UNSPLASH_PREFIX}1522071820081-009f0129c71c?w=800&q=80",
        f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80", f"{UNSPLASH_PREFIX}1454165804606-c3d57bc86b40?w=800&q=80",
    ],
}
NEWS_IMAGE_POOL["default"] = NEWS_IMAGE_POOL["umum"]
NEWS_IMAGE_POOL.setdefault("politik", NEWS_IMAGE_POOL["umum"])

# Kategori berita -> pool tema, untuk judul yang tidak kena keyword tema.
CATEGORY_THEME_MAP = {
    "Politik": "politik",
    "Viral": "viral",
    "Kriminal": "kriminal",
    "Ekonomi": "ekonomi",
    "Bencana": "bencana",
    "Berita": "umum",
}

# ── Keyword → nama pool gambar (dicek berurutan; yang pertama cocok) ─────
NEWS_THEME_KEYWORDS = [
    ("game", ["game", "gim", "gacha", "mlbb", "free fire", "pubg", "valorant",
              "esport", "kode redeem", "gameplay", "steam", "playstation",
              "xbox", "nintendo", "genshin", "honor of kings", "mobile legends"]),
    ("ecommerce", ["belanja", "tokopedia", "shopee", "lazada", "bukalapak",
                   "blibli", "jualan", "murah", "diskon", "promo",
                   "gratis ongkir", "e-commerce", "checkout", "keranjang"]),
    ("viral", ["viral", "trending", "heboh", "terbongkar", "kejutan", "menyala",
               "dilukai", "salah paham", "ramai dibicarakan", "nampar"]),
    ("kriminal", ["pembunuhan", "tewas", "bunuh", "korban", "jasad", "lambak",
                  "polisi", "tertangkap", "tersangka", "pemerasan", "perampokan",
                  "kekerasan", "cidik", "siksa", "jerat"]),
    ("olahraga", ["fifa", "sepak bola", "bola", "liga", "persib", "persija",
                  "tim nasional", "asian cup", "piala", "badminton", "tenis",
                  "atletik", "marathon", "turnamen", "kejuaraan", "sea games",
                  "olimpiade", "formula 1", "timnas"]),
    ("bencana", ["gempa", "banjir", "kebakaran", "bencana", "erupsi", "gunung",
                 "merapi", "krakatau", "tsunami", "tanah longsor", "puting belah",
                 "meteor", "hujan ekstrem", "kekeringan", "evakuasi", "korban jiwa"]),
    ("pendidikan", ["sekolah", "universitas", "kampus", "mahasiswa", "guru",
                    "murid", "pendidikan", "beasiswa", "ujian", "kelas", "sma",
                    "smp", "sd", "rektor", "fakultas", "dosen"]),
    ("kesehatan", ["obat", "rumah sakit", "hospital", "kesehatan", "dokter",
                   "vaksin", "penyakit", "gizi", "medis", "klinik", "imunisasi",
                   "stunting", "centering", "pasien"]),
    ("teknologi", ["teknologi", "aplikasi", "gadget", "smartphone", "internet",
                   "sinyal", "startup", "chip", "laptop", "komputer", "robot",
                   "otomotif", "mobil", "motor", "pesawat", " whatsapp",
                   "telegram", "siber", "hp android", "ai",
                   "kecerdasan buatan", "otomatis", "satelit", "antena"]),
    ("ekonomi", ["rupiah", "bursa", "saham", "bank", "ekonomi", "usaha",
                 "bisnis", "investasi", "gaji", "upah", "harga", "warung",
                 "dagang", "ekspor", "impor", "pajak", "umkm", "biaya",
                 "subsidi", "pasar", "ihsg", "inflasi", "devisa"]),
    ("hiburan", ["hiburan", "musik", "film", "artis", "seleb", "drama",
                 "konser", "sinema", "layar", "kreatif", "desain", "fesyen",
                 "baju", "kebaya", "penyanyi", "band", "album"]),
    ("kuliner", ["cafe", "resto", "restaurant", "makan", "kuliner", "food",
                 "goreng", "minum", "coffee", "hidangan", "jajan", "bakso",
                 "sate", "nasi", "restoran"]),
    ("transportasi", ["jalan", "transport", "terminal", "bandar", "pelabuhan",
                      "lalu lintas", "tol", "parkir", "armada", "bus",
                      "mikrolet", "kereta"]),
    ("pertanian", ["pertanian", "padi", "tani", "ikan", "peternakan", "sawit",
                   "kelapa", "panen", "peranian"])
]

# ── Rotary counter per tema: item berikutnya dalam tema sama dapat gambar
#    berbeda dari pool tema itu, jadi tidak ada dua item berbagi satu foto.
_theme_cursor: dict[str, int] = {}

# ── Pool gambar per tema TEKNOLOGI (semua ID diverifikasi HTTP 200) ────
# Aturan yang sama seperti berita: satu post blog = satu gambar berbeda.
# Picking rotary per tema + fallback silang, dijamin uniqueness oleh
# rebalance_unique_blog_images().
TECH_IMAGE_POOL = {
    "ai": [
        f"{UNSPLASH_PREFIX}1677442136019-21780ecad995?w=800&q=80", f"{UNSPLASH_PREFIX}1620712943543-bcc4688e7485?w=800&q=80", f"{UNSPLASH_PREFIX}1451187580459-43490279c0fa?w=800&q=80",
        f"{UNSPLASH_PREFIX}1555949963-aa79dcee981c?w=800&q=80", f"{UNSPLASH_PREFIX}1516116216624-53e697fedbea?w=800&q=80", f"{UNSPLASH_PREFIX}1593508512255-86ab42a8e620?w=800&q=80",
        f"{UNSPLASH_PREFIX}1507146426996-ef05306b995a?w=800&q=80", f"{UNSPLASH_PREFIX}1639762681485-074b7f938ba0?w=800&q=80", f"{UNSPLASH_PREFIX}1581091226825-a6a2a5aee158?w=800&q=80",
        f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80", f"{UNSPLASH_PREFIX}1591453089816-0fbb971b454c?w=800&q=80", f"{UNSPLASH_PREFIX}1518770660439-4636190af475?w=800&q=80",
        f"{UNSPLASH_PREFIX}1485827404703-89b55fcc595e?w=800&q=80", f"{UNSPLASH_PREFIX}1531746790731-6c087fecd65a?w=800&q=80", f"{UNSPLASH_PREFIX}1526628953301-3e589a6a8b74?w=800&q=80",
        f"{UNSPLASH_PREFIX}1638913662180-afc4334cf422?w=800&q=80", f"{UNSPLASH_PREFIX}1635070041078-e363dbe005cb?w=800&q=80",
    ],
    "cloud": [
        f"{UNSPLASH_PREFIX}1451187580459-43490279c0fa?w=800&q=80", f"{UNSPLASH_PREFIX}1558494949-ef010cbdcc31?w=800&q=80", f"{UNSPLASH_PREFIX}1667372393119-3d4c48d07fc9?w=800&q=80",
        f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80", f"{UNSPLASH_PREFIX}1454165804606-c3d57bc86b40?w=800&q=80", f"{UNSPLASH_PREFIX}1544197150-b99a580bb7a8?w=800&q=80",
        f"{UNSPLASH_PREFIX}1573804633927-bfcbcd909acd?w=800&q=80", f"{UNSPLASH_PREFIX}1560472354-b33ff0c44a43?w=800&q=80", f"{UNSPLASH_PREFIX}1526628953301-3e589a6a8b74?w=800&q=80",
        f"{UNSPLASH_PREFIX}1531497865144-0464ef8fb9a9?w=800&q=80", f"{UNSPLASH_PREFIX}1526374965328-7f61d4dc18c5?w=800&q=80", f"{UNSPLASH_PREFIX}1487058792275-0ad4aaf24ca7?w=800&q=80",
        f"{UNSPLASH_PREFIX}1573164713988-8665fc963095?w=800&q=80", f"{UNSPLASH_PREFIX}1605379399642-870262d3d051?w=800&q=80", f"{UNSPLASH_PREFIX}1518770660439-4636190af475?w=800&q=80",
        f"{UNSPLASH_PREFIX}1543722530-d2c3201371e7?w=800&q=80", f"{UNSPLASH_PREFIX}1614064641938-3bbee52942c7?w=800&q=80", f"{UNSPLASH_PREFIX}1607472586893-edb57bdc0e39?w=800&q=80",
    ],
    "security": [
        f"{UNSPLASH_PREFIX}1550751827-4bd374c3f58b?w=800&q=80", f"{UNSPLASH_PREFIX}1563986768609-322da13575f3?w=800&q=80", f"{UNSPLASH_PREFIX}1563013544-824ae1b704d3?w=800&q=80",
        f"{UNSPLASH_PREFIX}1635070041078-e363dbe005cb?w=800&q=80", f"{UNSPLASH_PREFIX}1614064641938-3bbee52942c7?w=800&q=80", f"{UNSPLASH_PREFIX}1544197150-b99a580bb7a8?w=800&q=80",
        f"{UNSPLASH_PREFIX}1526628953301-3e589a6a8b74?w=800&q=80", f"{UNSPLASH_PREFIX}1451187580459-43490279c0fa?w=800&q=80", f"{UNSPLASH_PREFIX}1667372393119-3d4c48d07fc9?w=800&q=80",
        f"{UNSPLASH_PREFIX}1560419015-7c427e8ae5ba?w=800&q=80", f"{UNSPLASH_PREFIX}1573164713988-8665fc963095?w=800&q=80", f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80",
        f"{UNSPLASH_PREFIX}1531746790731-6c087fecd65a?w=800&q=80", f"{UNSPLASH_PREFIX}1605379399642-870262d3d051?w=800&q=80", f"{UNSPLASH_PREFIX}1543722530-d2c3201371e7?w=800&q=80",
        f"{UNSPLASH_PREFIX}1516116216624-53e697fedbea?w=800&q=80",
    ],
    "mobile": [
        f"{UNSPLASH_PREFIX}1512941937669-90a1b58e7e9c?w=800&q=80", f"{UNSPLASH_PREFIX}1511707171634-5f897ff02aa9?w=800&q=80", f"{UNSPLASH_PREFIX}1555774698-0b77e0d5fac6?w=800&q=80",
        f"{UNSPLASH_PREFIX}1518709268805-4e9042af9f23?w=800&q=80", f"{UNSPLASH_PREFIX}1533228100845-08145b01de14?w=800&q=80", f"{UNSPLASH_PREFIX}1510557880182-3d4d3cba35a5?w=800&q=80",
        f"{UNSPLASH_PREFIX}1523206489230-c012c64b2b48?w=800&q=80", f"{UNSPLASH_PREFIX}1517336714731-489689fd1ca8?w=800&q=80", f"{UNSPLASH_PREFIX}1461749280684-dccba630e2f6?w=800&q=80",
        f"{UNSPLASH_PREFIX}1484417894907-623942c8ee29?w=800&q=80", f"{UNSPLASH_PREFIX}1499951360447-b19be8fe80f5?w=800&q=80", f"{UNSPLASH_PREFIX}1526374965328-7f61d4dc18c5?w=800&q=80",
        f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80", f"{UNSPLASH_PREFIX}1593508512255-86ab42a8e620?w=800&q=80", f"{UNSPLASH_PREFIX}1581091226825-a6a2a5aee158?w=800&q=80",
        f"{UNSPLASH_PREFIX}1573804633927-bfcbcd909acd?w=800&q=80", f"{UNSPLASH_PREFIX}1516116216624-53e697fedbea?w=800&q=80", f"{UNSPLASH_PREFIX}1521737711867-e3b97375f902?w=800&q=80",
        f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80", f"{UNSPLASH_PREFIX}1519389950473-47ba0277781c?w=800&q=80", f"{UNSPLASH_PREFIX}1523275335684-37898b6baf30?w=800&q=80",
    ],
    "web": [
        f"{UNSPLASH_PREFIX}1555066931-4365d14bab8c?w=800&q=80", f"{UNSPLASH_PREFIX}1627398242454-45a1465c2479?w=800&q=80", f"{UNSPLASH_PREFIX}1633356122544-f134324a6cee?w=800&q=80",
        f"{UNSPLASH_PREFIX}1518770660439-4636190af475?w=800&q=80", f"{UNSPLASH_PREFIX}1498050108023-c5249f4df085?w=800&q=80", f"{UNSPLASH_PREFIX}1487058792275-0ad4aaf24ca7?w=800&q=80",
        f"{UNSPLASH_PREFIX}1484417894907-623942c8ee29?w=800&q=80", f"{UNSPLASH_PREFIX}1499951360447-b19be8fe80f5?w=800&q=80", f"{UNSPLASH_PREFIX}1467232004584-a241de8bcf5d?w=800&q=80",
        f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80", f"{UNSPLASH_PREFIX}1521737711867-e3b97375f902?w=800&q=80", f"{UNSPLASH_PREFIX}1542838132-92c53300491e?w=800&q=80",
        f"{UNSPLASH_PREFIX}1552664730-d307ca884978?w=800&q=80", f"{UNSPLASH_PREFIX}1553877522-43269d4ea984?w=800&q=80", f"{UNSPLASH_PREFIX}1523474253046-8cd2748b5fd2?w=800&q=80",
        f"{UNSPLASH_PREFIX}1526374965328-7f61d4dc18c5?w=800&q=80", f"{UNSPLASH_PREFIX}1504639725590-34d0984388bd?w=800&q=80", f"{UNSPLASH_PREFIX}1461749280684-dccba630e2f6?w=800&q=80",
        f"{UNSPLASH_PREFIX}1516116216624-53e697fedbea?w=800&q=80", f"{UNSPLASH_PREFIX}1618477388954-7852f32655ec?w=800&q=80",
    ],
    "opensource": [
        f"{UNSPLASH_PREFIX}1526374965328-7f61d4dc18c5?w=800&q=80", f"{UNSPLASH_PREFIX}1531297484001-80022131f5a1?w=800&q=80", f"{UNSPLASH_PREFIX}1461749280684-dccba630e2f6?w=800&q=80",
        f"{UNSPLASH_PREFIX}1556075798-4825dfaaf498?w=800&q=80", f"{UNSPLASH_PREFIX}1516116216624-53e697fedbea?w=800&q=80", f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80",
        f"{UNSPLASH_PREFIX}1484417894907-623942c8ee29?w=800&q=80", f"{UNSPLASH_PREFIX}1517180102446-f3ece451e9d8?w=800&q=80", f"{UNSPLASH_PREFIX}1526628953301-3e589a6a8b74?w=800&q=80",
        f"{UNSPLASH_PREFIX}1611162617474-5b21e879e113?w=800&q=80", f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80", f"{UNSPLASH_PREFIX}1498050108023-c5249f4df085?w=800&q=80",
        f"{UNSPLASH_PREFIX}1467232004584-a241de8bcf5d?w=800&q=80", f"{UNSPLASH_PREFIX}1573804633927-bfcbcd909acd?w=800&q=80", f"{UNSPLASH_PREFIX}1552664730-d307ca884978?w=800&q=80",
        f"{UNSPLASH_PREFIX}1544197150-b99a580bb7a8?w=800&q=80", f"{UNSPLASH_PREFIX}1618477388954-7852f32655ec?w=800&q=80", f"{UNSPLASH_PREFIX}1518432031352-d6fc5c10da5a?w=800&q=80",
        f"{UNSPLASH_PREFIX}1581091226825-a6a2a5aee158?w=800&q=80",
    ],
    "data": [
        f"{UNSPLASH_PREFIX}1551288049-bebda4e38f71?w=800&q=80", f"{UNSPLASH_PREFIX}1633356122544-f134324a6cee?w=800&q=80", f"{UNSPLASH_PREFIX}1518186285589-2f7649de83e0?w=800&q=80",
        f"{UNSPLASH_PREFIX}1543286386-713bdd548da4?w=800&q=80", f"{UNSPLASH_PREFIX}1454165804606-c3d57bc86b40?w=800&q=80", f"{UNSPLASH_PREFIX}1544197150-b99a580bb7a8?w=800&q=80",
        f"{UNSPLASH_PREFIX}1504868584819-f8e8b4b6d7e3?w=800&q=80", f"{UNSPLASH_PREFIX}1523474253046-8cd2748b5fd2?w=800&q=80", f"{UNSPLASH_PREFIX}1543722530-d2c3201371e7?w=800&q=80",
        f"{UNSPLASH_PREFIX}1605379399642-870262d3d051?w=800&q=80", f"{UNSPLASH_PREFIX}1519389950473-47ba0277781c?w=800&q=80", f"{UNSPLASH_PREFIX}1553877522-43269d4ea984?w=800&q=80",
        f"{UNSPLASH_PREFIX}1526628953301-3e589a6a8b74?w=800&q=80", f"{UNSPLASH_PREFIX}1618477388954-7852f32655ec?w=800&q=80", f"{UNSPLASH_PREFIX}1573164713988-8665fc963095?w=800&q=80",
        f"{UNSPLASH_PREFIX}1552664730-d307ca884978?w=800&q=80", f"{UNSPLASH_PREFIX}1518432031352-d6fc5c10da5a?w=800&q=80", f"{UNSPLASH_PREFIX}1531297484001-80022131f5a1?w=800&q=80",
        f"{UNSPLASH_PREFIX}1460925895917-afdab827c52f?w=800&q=80", f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80",
    ],
    "iot": [
        f"{UNSPLASH_PREFIX}1518770660439-4636190af475?w=800&q=80", f"{UNSPLASH_PREFIX}1581091226825-a6a2a5aee158?w=800&q=80", f"{UNSPLASH_PREFIX}1516116216624-53e697fedbea?w=800&q=80",
        f"{UNSPLASH_PREFIX}1544197150-b99a580bb7a8?w=800&q=80", f"{UNSPLASH_PREFIX}1531297484001-80022131f5a1?w=800&q=80", f"{UNSPLASH_PREFIX}1526374965328-7f61d4dc18c5?w=800&q=80",
        f"{UNSPLASH_PREFIX}1519389950473-47ba0277781c?w=800&q=80", f"{UNSPLASH_PREFIX}1558494949-ef010cbdcc31?w=800&q=80", f"{UNSPLASH_PREFIX}1573164713988-8665fc963095?w=800&q=80",
        f"{UNSPLASH_PREFIX}1552664730-d307ca884978?w=800&q=80", f"{UNSPLASH_PREFIX}1605379399642-870262d3d051?w=800&q=80", f"{UNSPLASH_PREFIX}1526628953301-3e589a6a8b74?w=800&q=80",
        f"{UNSPLASH_PREFIX}1531746790731-6c087fecd65a?w=800&q=80", f"{UNSPLASH_PREFIX}1620712943543-bcc4688e7485?w=800&q=80", f"{UNSPLASH_PREFIX}1451187580459-43490279c0fa?w=800&q=80",
        f"{UNSPLASH_PREFIX}1593508512255-86ab42a8e620?w=800&q=80", f"{UNSPLASH_PREFIX}1485827404703-89b55fcc595e?w=800&q=80", f"{UNSPLASH_PREFIX}1553877522-43269d4ea984?w=800&q=80",
        f"{UNSPLASH_PREFIX}1607799279861-4dd421887fb3?w=800&q=80", f"{UNSPLASH_PREFIX}1523275335684-37898b6baf30?w=800&q=80", f"{UNSPLASH_PREFIX}1498049794561-7780e7231661?w=800&q=80",
        f"{UNSPLASH_PREFIX}1550009158-9ebf69173e03?w=800&q=80",
    ],
    "umum": [
        f"{UNSPLASH_PREFIX}1497366216548-37526070297c?w=800&q=80", f"{UNSPLASH_PREFIX}1521737711867-e3b97375f902?w=800&q=80", f"{UNSPLASH_PREFIX}1454165804606-c3d57bc86b40?w=800&q=80",
        f"{UNSPLASH_PREFIX}1519389950473-47ba0277781c?w=800&q=80", f"{UNSPLASH_PREFIX}1495020689067-958852a7765e?w=800&q=80", f"{UNSPLASH_PREFIX}1504711434969-e33886168f5c?w=800&q=80",
        f"{UNSPLASH_PREFIX}1497215728101-856f4ea42174?w=800&q=80", f"{UNSPLASH_PREFIX}1524758631624-e2822e304c36?w=800&q=80", f"{UNSPLASH_PREFIX}1497366754035-f200968a6e72?w=800&q=80",
        f"{UNSPLASH_PREFIX}1517245386807-bb43f82c33c4?w=800&q=80", f"{UNSPLASH_PREFIX}1541746972996-4e0b0f43e02a?w=800&q=80", f"{UNSPLASH_PREFIX}1531973576160-7125cd663d86?w=800&q=80",
        f"{UNSPLASH_PREFIX}1560472354-b33ff0c44a43?w=800&q=80", f"{UNSPLASH_PREFIX}1486406146926-c627a92ad1ab?w=800&q=80", f"{UNSPLASH_PREFIX}1522071820081-009f0129c71c?w=800&q=80",
        f"{UNSPLASH_PREFIX}1600607687939-ce8a6c25118c?w=800&q=80", f"{UNSPLASH_PREFIX}1504384308090-c894fdcc538d?w=800&q=80", f"{UNSPLASH_PREFIX}1521737604893-d14cc237f11d?w=800&q=80",
        f"{UNSPLASH_PREFIX}1522202176988-66273c2fd55f?w=800&q=80", f"{UNSPLASH_PREFIX}1600880292203-757bb62b4baf?w=800&q=80", f"{UNSPLASH_PREFIX}1556761175-b413da4baf72?w=800&q=80",
    ],
}

TECH_IMAGE_POOL["default"] = TECH_IMAGE_POOL["umum"]

# ── Nama kategori blog (lama & baru) -> nama pool tema ────────────────────
# Kategori lama ("AI & ML", "AI & Machine Learning", "Artificial Intelligence")
# dinormalkan ke satu tema supaya tidak ada 3 nama untuk 1 hal.
TECH_CATEGORY_THEME = {
    "ai": "ai",
    "ai & ml": "ai",
    "ai & machine learning": "ai",
    "artificial intelligence": "ai",
    "machine learning": "ai",
    "cloud": "cloud",
    "cloud & infrastructure": "cloud",
    "cloud & devops": "cloud",
    "infrastructure": "cloud",
    "devops": "cloud",
    "cybersecurity": "security",
    "security": "security",
    "keamanan siber": "security",
    "mobile": "mobile",
    "mobile engineering": "mobile",
    "mobile & apps": "mobile",
    "android": "mobile",
    "ios": "mobile",
    "web": "web",
    "web development": "web",
    "frontend": "web",
    "open source": "opensource",
    "opensource": "opensource",
    "data": "data",
    "data engineering": "data",
    "database": "data",
    "backend": "data",
    "iot": "iot",
    "embedded": "iot",
    "edge": "iot",
}

# ── Keyword -> nama pool tema, dipakai kalau kategori tidak dikenali ───────
TECH_THEME_KEYWORDS = [
    ("ai", ["ai", "artificial intelligence", "machine learning", "llm", "gpt",
            "neural", "deep learning", "chatbot", "agent", "model", "training",
            "inference", "transformer", "diffusion", "prompt", "openai",
            "anthropic", "gemini", "claude", "llama"]),
    ("security", ["cyber", "security", "keamanan", "serangan", "hack",
                  "malware", "ransomware", "threat", "vulnerability", "exploit",
                  "bug bounty", "forensic", "siber", "zero trust", "passkey",
                  "passkeys", "auth", "enkripsi", "kriptografi"]),
    ("cloud", ["cloud", "devops", "server", "aws", "azure", "gcp", "docker",
               "kubernetes", "microservice", "container", "terraform",
               "serverless", "s3", "lambda", "sre", "cluster", "infrastruktur",
               "on-premise", "hosting"]),
    ("mobile", ["android", "ios", "mobile", "smartphone", "app", "aplikasi",
                "play store", "app store", "flutter", "kotlin", "swift",
                "jetpack", "compose", "react native", "xr", "watch"]),
    ("web", ["web", "browser", "css", "html", "javascript", "typescript",
             "vue", "nuxt", "react", "svelte", "frontend", "wasm", "webassembly",
             "webgpu", "sveltekit", "nextjs", "tailwind", "dom"]),
    ("opensource", ["open source", "opensource", "github", "gitlab", "repo",
                    "library", "framework", "apache", "linux", "bsd", "gnu",
                    "contributor", "pull request", "backstage", "spi"]),
    ("data", ["data", "database", "sql", "postgresql", "postgres", "mysql",
              "mongodb", "redis", "kafka", "pipeline", "etl", "big data",
              "analytics", "olap", "schema", "query", "storage"]),
    ("iot", ["iot", "embedded", "edge computing", "edge ai", "sensor",
             "raspberry", "arduino", "firmware", "telemetri", "perangkat",
             "wearable", "robotika", "robot"]),
]

# Cursor rotary per tema + pencatat gambar yang sudah dipakai di run ini.
_tech_cursor: dict[str, int] = {}
_tech_assigned: set[str] = set()



JUNK_KEYWORDS_IN_TITLE = [
    "lowongan kerja", "lowongan", "universitas", "kampus",
    "pegawai", "staf", "bidang", "program studi",
    "mahasiswa", "lulusan", "dosen", "fakultas",
    "politeknik", "akademi", "sekolah", "pinjaman",
    "rekrutmen", "rekrut", "cpns", "jabatan",
    "tes seleksi", "dana kuliah", "beasiswa",
    "kuliah", "kata pengantar", "surat izin",
    "pengumuman", "pemberitahuan", "nota dinas",
    # Institusi pemerintah yang muncul di judul
    "kementerian", "kemdikbud", "kemdiktisaintek", "kemenag",
    "kemenkominfo", "kemenkeu", "kemenlu", "kemenperin",
    "kemnaker", "kemendag", "kemendikdasmen", "kemendikbudristek",
    "kemendesa", "kemening", "kemenhub", "kemendagri",
    "bnn", "polri", "polda", "polsek", "bripka",
    "bpbd", "bnpb", "bangda", "kabinet", "presiden",
    "menteri", "wakil presiden", "dewan perwakilan",
    "dpr ri", "dpd", "kepolisian", "tentara", "tni",
    "daerah", "pemerintah daerah", "pemda",
    "instansi pemerintah", "lembaga negara",
    # Diskominfes / Dinas Komunikasi Informasi (pemerintah daerah)
    "diskominfes", "diskominfo", "dinas komunikasi",
    "humas", "info kota", "info kabupaten", "info provinsi",
    # HMTI = Himpunan Mahasiswa Teknologi Informasi (kampus)
    "hmti", "himpunan mahasiswa teknik",
    # POLBENG = Politeknik Negeri Bengkalis (kampus)
    "polbeng", "politeknik negeri",
    # Kakanwil = Kanwil (Kementerian Agama wilayah)
    "kakanwil", "kanwil",
]

# Sumber yang dianggap terafiliasi pemerintah — eksplisit diblokir.
# Items dari sumber ini TIDAK diproses untuk blog dan news.
GOVERNMENT_SOURCES = [
    "kementerian", "kemdikbud", "kemdiktisaintek", "kemenag",
    "kemenkominfo", "kemenkeu", "kemenlu", "kemenperin",
    "kemnaker", "kemendag", "kemendikdasmen", "kemendikbudristek",
    "kemendesa", "kemening", "kemenhub", "kemendagri",
    "bnn", "polri", "bripka", "polda", "polsek",
    "bpbd", "bnpb", "bangda", " Kemendikbud ", " kemendikbud",
    "kompas kemendikbud", "mediakom", "dpk", "kabinet",
    "presiden", " Wakil Presiden", "menteri",
]


# ─── Helpers ───────────────────────────────────────────────────────────────

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_rss_date_to_date(date_str: str) -> str:
    """Parse berbagai format tanggal RSS jadi YYYY-MM-DD."""
    if not date_str:
        return utc_now().strftime("%Y-%m-%d")
    date_str = date_str.strip()
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%d %b %Y %H:%M:%S %z",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
    ]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    m = re.search(r"(\d{4})[-/](\d{2})[-/](\d{2})", date_str)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return utc_now().strftime("%Y-%m-%d")


def is_recent(date_str: str) -> bool:
    if not date_str:
        return True
    try:
        parsed = datetime.strptime(
            re.sub(r"\s+WIB$", "", date_str), "%a, %d %b %Y %H:%M:%S"
        )
        parsed = parsed.replace(tzinfo=timezone.utc)
        cutoff = utc_now() - timedelta(days=PAST_DAYS)
        return parsed >= cutoff
    except (ValueError, TypeError):
        return True


def clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:600]


def trim_title(title: str) -> str:
    """Hapus suffix seperti '- Detik', '- Kompas', '- Liputan6', dll."""
    title = re.sub(
        r"\s*[-–—]\s*(Detik|Kompas|Liputan6|Okezone|Tempo|CNBC|Viva|"
        r"Media Indonesia|ANTARA|News|Jawa Pos|Tribunnews|Galeri|Photo|"
        r"Foto|Viral|com)$",
        "",
        title,
        flags=re.IGNORECASE,
    )
    return title.strip()


def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug[:80]


def make_slug(title: str, source_label: str, index: int) -> str:
    base = slugify(trim_title(title))
    if not base:
        base = f"item-{index}"
    return f"{source_label}-{base}" if source_label else base


def is_junk_title(title: str) -> bool:
    """Skip item jika judulnya junk (konten non-berita: lowongan, kampus, pinjaman, dll.)
    atau dari institusi pemerintah."""
    title_lower = title.lower()

    # Keyword utama: konten non-berita (lowongan, kampus, pinjaman, dll.)
    for kw in JUNK_KEYWORDS_IN_TITLE:
        if kw in title_lower:
            return True

    # Deteksi institusi pemerintah: "Pemerintah Kabupaten/Provinsi/Kota/Daerah ..."
    if re.search(
        r"pemerintah\s+(kabupaten|provinsi|kota|daerah|kotamadya|"
        r"lembaga|dewan|komite|nasional|internasional)",
        title_lower,
    ):
        return True

    # Deteksi "Nama Instansi + (Kabupaten/Provinsi/Kota)"
    if re.search(r"\([a-z\s]+kabupaten\)|\([a-z\s]+provinsi\)|\([a-z\s]+kota\)", title_lower):
        return True

    return False


def is_government_source(source_label: str) -> bool:
    """Deteksi apakah sumber ini terafiliasi pemerintah. Skip jika ya."""
    label_lower = source_label.lower()
    for gov_kw in GOVERNMENT_SOURCES:
        if gov_kw.lower() in label_lower:
            return True
    return False


def fetch_rss(url: str) -> list[dict]:
    """Fetch dan parse RSS/Atom feed, return list item dicts."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"    [WARN] Gagal fetch {url}: {e}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        print(f"    [WARN] Parse error untuk {url}", file=sys.stderr)
        return []

    items = []

    # RSS 2.0: item di bawah channel
    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        desc_el = item.find("description")
        pub_el = item.find("pubDate")
        guid_el = item.find("guid")

        title = (
            html.unescape(title_el.text.strip())
            if title_el is not None and title_el.text
            else ""
        )
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        desc = clean_html(desc_el.text) if desc_el is not None and desc_el.text else ""
        pub = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
        guid = guid_el.text.strip() if guid_el is not None and guid_el.text else ""

        if not title:
            continue

        if not link and link_el is not None:
            link = link_el.get("href", "")

        if not link and guid:
            link = guid

        img = ""
        enc_el = item.find("enclosure")
        if enc_el is not None and enc_el.get("url"):
            if "image" in enc_el.get("type", "").lower():
                img = enc_el.get("url")
        if not img:
            # <media:content>/<media:thumbnail> (namespace media)
            for child in item:
                if child.tag.endswith("}content") or child.tag.endswith("}thumbnail"):
                    if child.get("url"):
                        img = child.get("url")
                        break

        items.append({
            "title": title,
            "url": link,
            "description": desc,
            "pubDate": pub,
            "image": img,
        })

    # Atom: entry di bawah feed (jika RSS gagal dapat item)
    if not items:
        for entry in root.findall(".//entry"):
            title_el = entry.find("title")
            link_el = entry.find("link")
            content_el = entry.find("content")
            published_el = entry.find("published")
            updated_el = entry.find("updated")

            title = (
                html.unescape(title_el.text.strip())
                if title_el is not None and title_el.text
                else ""
            )
            link = ""
            if link_el is not None:
                link = link_el.get("href", "")
                if not link:
                    for child in link_el:
                        link = child.get("href", "")
                        if link:
                            break

            desc = ""
            if content_el is not None and content_el.text:
                desc = clean_html(content_el.text)

            pub = ""
            for el in [published_el, updated_el]:
                if el is not None and el.text:
                    pub = el.text.strip()
                    break

            if not title:
                continue

            items.append({
                "title": title,
                "url": link,
                "description": desc,
                "pubDate": pub,
                "image": "",
            })

    return items


# ─── News JSON ─────────────────────────────────────────────────────────────

def rebalance_unique_images(data: dict) -> int:
    """Pastikan tiap item berita punya gambar BERBEDA.

    some item masih berbagi satu foto (mis. dua berita ekonomi dapat gambar
    yang sama). Ganti duplikat dengan gambar lain dari pool temaJudulnya.
    """
    items = data.get("items", [])
    seen: set[str] = set()
    changed = 0

    for it in items:
        img = it.get("image", "")
        if img and img not in seen:
            seen.add(img)
            continue

        # duplikat (atau kosong) -> pilih gambar lain dari pool tema
        theme = _theme_for(it.get("title", ""), it.get("category", "Berita"))
        pool = NEWS_IMAGE_POOL.get(theme) or NEWS_IMAGE_POOL["default"]
        replacement = next((u for u in pool if u not in seen), None)
        if replacement is None:
            for name, plist in NEWS_IMAGE_POOL.items():
                replacement = next((u for u in plist if u not in seen), None)
                if replacement:
                    break
        if replacement:
            it["image"] = replacement
            seen.add(replacement)
            changed += 1

    return changed


def update_news_json(new_items: list[dict]) -> dict:
    """Update news.json: prepend items baru, skip duplikat, batasi maks."""
    if NEWS_JSON_PATH.exists():
        with open(NEWS_JSON_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {
            "title": "Berita dari Portal Berita Swasta",
            "subtitle": (
                "Kompilasi berita terbaru dari portal berita independen Indonesia — "
                "isu politik, viral, dan sosial media."
            ),
            "updatedAt": utc_now().strftime("%Y-%m-%d"),
            "items": [],
        }

    existing["updatedAt"] = utc_now().strftime("%Y-%m-%d")
    existing_slugs = {item["slug"] for item in existing.get("items", [])}

    merged = []
    for item in new_items:
        if item["slug"] not in existing_slugs:
            merged.append(item)

    merged = merged + existing.get("items", [])
    existing["items"] = merged[:MAX_NEWS_ITEMS]

    rebalanced = rebalance_unique_images(existing)
    if rebalanced:
        print(f"  [image] {rebalanced} item diberi gambar unik baru")

    with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return existing


def _theme_for(title: str, category: str) -> str:
    """Tentukan nama pool gambar dari keyword di judul (word-boundary)."""
    title_lower = title.lower()
    for theme, keywords in NEWS_THEME_KEYWORDS:
        for kw in keywords:
            kw = kw.strip().lower()
            if kw and re.search(rf"(?<!\w){re.escape(kw)}(?!\w)", title_lower):
                return theme
    # tidak ada keyword tema -> pakai pool berdasarkan kategori berita
    return CATEGORY_THEME_MAP.get(category, "default")


def pick_news_image(item: dict, title: str, category: str) -> str:
    """Pilih gambar berita. Prioritas:

    1. Gambar asli dari RSS (paling relevan dengan judul).
    2. Pool gambar per tema, dipilih rotary supaya tiap item dalam tema
       yang sama dapat foto BERBEDA.
    3. Kalau pool tema habis, ambil dari pool tema lain yang belum terpakai.
    """
    # 1. Gambar asli RSS
    rss_img = (item.get("image") or "").strip()
    if rss_img.startswith("http"):
        rss_img = rss_img.replace("&amp;", "&")
        _assigned_this_run.add(rss_img)
        return rss_img

    # 2/3. Pool tema dengan rotary + fallback silang
    theme = _theme_for(title, category)
    pool = NEWS_IMAGE_POOL.get(theme) or NEWS_IMAGE_POOL["default"]

    used = _used_images()
    for step in range(len(pool) * 2):
        idx = (_theme_cursor.get(theme, 0) + step) % len(pool)
        url = pool[idx]
        if url not in used:
            _theme_cursor[theme] = idx + 1
            _assigned_this_run.add(url)
            return url

    # semua gambar tema terpakai -> scan semua pool sampai ketemu yang belum dipakai
    for name, plist in NEWS_IMAGE_POOL.items():
        for url in plist:
            if url not in used:
                _assigned_this_run.add(url)
                return url

    # pool benar-benar habis (tidak mungkin: 118 gambar vs max 15 item)
    return pool[_theme_cursor.get(theme, 0) % len(pool)]


_assigned_this_run: set[str] = set()


def _used_images() -> set[str]:
    """Gambar yang sudah dipakai: item lain di news.json + item run ini."""
    try:
        with open(NEWS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return set()
    items = data if isinstance(data, list) else data.get("items", [])
    used = {it.get("image", "") for it in items if it.get("image")}
    return used | _assigned_this_run


def build_news_item(item: dict, source_label: str, index: int) -> dict:
    """Convert RSS item ke format news.json."""
    title = trim_title(item["title"])
    desc = item["description"]
    url = item["url"] or ""
    pub_date = item["pubDate"]

    date_str = parse_rss_date_to_date(pub_date)
    slug = make_slug(title, source_label, index)
    excerpt = desc[:200] if desc else title[:200]

    title_lower = title.lower()
    if any(kw in title_lower for kw in [
        "politik", "dpr", "presiden", "menteri", "partai",
        "pil", "legislasi", "ujaran", "demo", "protes",
        "eksekutif", "legislatif", "yudikatif", "kabinet", "dewan",
    ]):
        category = "Politik"
    elif any(kw in title_lower for kw in [
        "viral", "heboh", "fenomenal", "menyala", "geger",
        "white", "baru terungkap", "terbongkar", "syok",
        "trending", "hoaks", "kejutan", "menghebohkan",
    ]):
        category = "Viral"
    elif any(kw in title_lower for kw in [
        "kriminal", "polis", "narkoba", "pidana", "korupsi",
        "tersangka", "kasus", "penyidikan", "narkotika",
        "cemas", "amnesti", "hukum", "jaksa", "hakim",
    ]):
        category = "Kriminal"
    elif any(kw in title_lower for kw in [
        "ekonomi", "harga", "rupiah", "bank", "bursa",
        "financial", "stock", "IHSG", "swasta", "usaha",
        "bisnis", "investasi", "uang", "rupiah",
    ]):
        category = "Ekonomi"
    elif any(kw in title_lower for kw in [
        "banjir", "gempa", "kebakaran", "bencana", "bmkg",
        "BNPB", "evakuasi", "darurat", "korban", "selamatkan",
        "erupsi", "gunung", "merapi", "krakatau",
    ]):
        category = "Bencana"
    else:
        category = "Berita"

    tags = [source_label]
    if any(kw in title_lower for kw in ["politik", "dpr", "presiden"]):
        tags.append("Politik")
    if any(kw in title_lower for kw in ["viral", "heboh", "trending"]):
        tags.append("Viral")
    if any(kw in title_lower for kw in ["ekonomi", "bank", "harga"]):
        tags.append("Ekonomi")
    tags = list(dict.fromkeys(tags))[:4]

    key_facts = []
    if desc:
        for sentence in re.split(r"[.!?]+\s+", desc):
            sentence = sentence.strip()
            if 20 < len(sentence) < 200:
                key_facts.append(sentence)
            if len(key_facts) >= 3:
                break
    if not key_facts and title:
        key_facts.append(title[:150])

    return {
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
        "category": category,
        "source": source_label,
        "sourceUrl": url,
        "date": date_str,
        "image": pick_news_image(item, title, category),
        "tags": tags,
        "summary": desc[:600] if desc else title[:300],
        "keyFacts": key_facts,
    }


# ─── Blog Markdown ─────────────────────────────────────────────────────────

def _tech_theme_for(category: str, title: str) -> str:
    """Tentukan pool tema dari kategori frontmatter, lalu keyword judul."""
    cat = (category or "").strip().lower()
    if cat in TECH_CATEGORY_THEME:
        return TECH_CATEGORY_THEME[cat]

    title_lower = (title or "").lower()
    for theme, keywords in TECH_THEME_KEYWORDS:
        for kw in keywords:
            kw = kw.strip().lower()
            if kw and re.search(rf"(?<!\w){re.escape(kw)}(?!\w)", title_lower):
                return theme
    return "default"


def _blog_images_in_use(exclude_slug: str = "") -> set[str]:
    """Gambar yang dipakai post blog lain (dari frontmatter file)."""
    used: set[str] = set()
    for f in BLOG_DIR.glob("*.md"):
        if exclude_slug and f.stem == exclude_slug:
            continue
        try:
            head = f.read_text(encoding="utf-8")[:1200]
        except Exception:
            continue
        mm = re.search(r'^image:\s*"(.*?)"', head, re.M)
        if mm:
            used.add(mm.group(1))
    return used


def pick_blog_image(item: dict, category: str, title: str, slug: str) -> str:
    """Pilih gambar blog: RSS asli > pool rotary per tema > fallback silang."""
    rss_img = (item.get("image") or "").strip()
    if rss_img.startswith("http"):
        return rss_img.replace("&amp;", "&")

    theme = _tech_theme_for(category, title)
    pool = TECH_IMAGE_POOL.get(theme) or TECH_IMAGE_POOL["default"]
    used = _blog_images_in_use() | _tech_assigned

    for step in range(len(pool) * 2):
        idx = (_tech_cursor.get(theme, 0) + step) % len(pool)
        url = pool[idx]
        if url not in used:
            _tech_cursor[theme] = idx + 1
            _tech_assigned.add(url)
            return url

    for name, plist in TECH_IMAGE_POOL.items():
        for url in plist:
            if url not in used:
                _tech_assigned.add(url)
                return url

    return pool[_tech_cursor.get(theme, 0) % len(pool)]


def rebalance_unique_blog_images() -> int:
    """Jaminan: tiap post blog punya gambar BERBEDA. Kembalikan jumlah yang diubah."""
    posts = sorted(BLOG_DIR.glob("*.md"))
    seen: set[str] = set()
    changed = 0

    for f in posts:
        try:
            txt = f.read_text(encoding="utf-8")
        except Exception:
            continue
        m_img = re.search(r'^image:\s*"(.*?)"', txt, re.M)
        m_cat = re.search(r'^category:\s*"(.*?)"', txt, re.M)
        m_ttl = re.search(r'^title:\s*"(.*?)"', txt, re.M)
        if not m_img:
            continue

        img = m_img.group(1)
        if img and img not in seen:
            seen.add(img)
            continue

        theme = _tech_theme_for(m_cat.group(1) if m_cat else "",
                                m_ttl.group(1) if m_ttl else "")
        pool = TECH_IMAGE_POOL.get(theme) or TECH_IMAGE_POOL["default"]
        repl = next((u for u in pool if u not in seen), None)
        if repl is None:
            for name, plist in TECH_IMAGE_POOL.items():
                repl = next((u for u in plist if u not in seen), None)
                if repl:
                    break
        if repl:
            txt = txt[:m_img.start()] + f'image: "{repl}"' + txt[m_img.end():]
            f.write_text(txt, encoding="utf-8")
            seen.add(repl)
            changed += 1

    return changed


def build_blog_frontmatter(item: dict, source_label: str) -> str:
    """Build YAML frontmatter untuk blog post teknologi."""
    title = trim_title(item["title"])
    desc = item["description"]
    pub_date = item["pubDate"]

    date_str = parse_rss_date_to_date(pub_date)
    slug = slugify(title) or f"tech-{source_label}"
    excerpt = desc[:160] if desc else title[:160]

    title_lower = title.lower()
    if any(kw in title_lower for kw in [
        "ai", "artificial intelligence", "machine learning",
        "llm", "gpt", "bert", "neural network", "deep learning",
    ]):
        category = "Artificial Intelligence"
    elif any(kw in title_lower for kw in [
        "cyber", "security", "serangan", "hack", "malware",
        "ransomware", "threat", "vulnerability", "serangan siber",
    ]):
        category = "Cybersecurity"
    elif any(kw in title_lower for kw in [
        "cloud", "devops", "server", "aws", "azure", "gcp",
        "docker", "kubernetes", "microservice", "container",
    ]):
        category = "Cloud & DevOps"
    elif any(kw in title_lower for kw in [
        "open source", "opensource", "github", "gitlab", "repo",
        "library", "framework", "apache", "linux",
    ]):
        category = "Open Source"
    elif any(kw in title_lower for kw in [
        "android", "iOS", "mobile", "smartphone", "app",
        "aplikasi", "play store", "app store",
    ]):
        category = "Mobile & Apps"
    else:
        category = "Teknologi Informasi"

    blog_image = pick_blog_image(item, category, title, slug)

    tags = [source_label, "RSS"]
    if any(kw in title_lower for kw in ["ai", "artificial intelligence"]):
        tags.append("AI")
    if any(kw in title_lower for kw in ["teknologi", "tech", "digital"]):
        tags.append("Teknologi")
    if any(kw in title_lower for kw in ["cyber", "security"]):
        tags.append("Keamanan Siber")
    tags = list(dict.fromkeys(tags))[:5]

    return (
        "---\n"
        f"title: \"{title}\"\n"
        f"description: \"{excerpt}\"\n"
        f"date: \"{date_str}\"\n"
        f"author: \"Ringga Septia Pribadi\"\n"
        f'tags: [{", ".join(json.dumps(t) for t in tags)}]\n'
        f"category: \"{category}\"\n"
        f"image: \"{blog_image}\"\n"
        "---\n"
    )


def build_blog_body(item: dict, source_label: str) -> str:
    """Build isi markdown dari RSS item."""
    title = trim_title(item["title"])
    desc = item["description"]
    url = item["url"] or ""
    pub_date = parse_rss_date_to_date(item["pubDate"])

    lines = [
        "\n## Pendahuluan\n\n",
        f"**{title}**\n\n",
        f"Berita ini dikumpulkan dari RSS portal *{source_label}* — "
        f"sumber berita independen Indonesia. "
        f"Tanggal: {pub_date}.\n\n",
    ]

    # Gunakan deskripsi jika punya konten substantif (lebih dari sekadar judul)
    if desc and len(desc) > len(title) + 20:
        paragraphs = [
            p.strip()
            for p in re.split(r"[.!?]+\s+", desc)
            if p.strip() and len(p.strip()) > 30
        ]
        for p in paragraphs[:4]:
            lines.append(f"{p}.\n\n")

    if lines and not lines[-1].endswith("\n\n"):
        lines.append("\n")

    lines.extend([
        "\n---\n\n",
        f"**Sumber:** [{source_label}]({url})\n" if url else f"**Sumber:** {source_label}\n",
        f"**Dirangkum oleh:** Ringga Dev Portfolio\n",
        "**Dipetik dari RSS portal berita independen Indonesia**\n",
    ])

    return "".join(lines)


def generate_blog_md(item: dict, source_label: str) -> str:
    fm = build_blog_frontmatter(item, source_label)
    body = build_blog_body(item, source_label)
    return fm + "\n" + body


def write_new_blog_posts(new_items: list[dict]) -> int:
    """Write file .md baru ke src/data/blog/. Skip kalau sudah ada."""
    existing_files = set(f.name for f in BLOG_DIR.glob("*.md"))
    written = 0

    for idx, item in enumerate(new_items[:MAX_BLOG_NEW]):
        title = trim_title(item["title"])
        slug = slugify(title) or f"tech-{idx}"
        filename = f"{slug}.md"

        if filename in existing_files:
            continue

        md_content = generate_blog_md(item, item.get("_source_label", "RSS"))
        filepath = BLOG_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        written += 1
        print(f"  [blog] Created: {filename}")

    if written:
        fixed = rebalance_unique_blog_images()
        if fixed:
            print(f"  [blog] {fixed} post diberi gambar unik baru")

    return written


# ─── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    # reset cache gambar supaya tiap run menghasilkan rotasi baru
    _theme_cursor.clear()
    _assigned_this_run.clear()
    _tech_cursor.clear()
    _tech_assigned.clear()

    print(f"[*] RSS News Fetcher — {utc_now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"[*] Repo root: {REPO_ROOT}")
    print()

    # ── 1. Berita dari portal berita swasta + Google News RSS ───────────────
    print("[1/2] Fetch berita dari portal berita independen Indonesia")
    all_news = []

    # Dari portal berita swasta (RSS langsung — hanya sumber yang bekerja)
    for source_label, url in NEWS_SOURCES:
        print(f"  Source: {source_label} → {url}")
        items = fetch_rss(url)
        recent = [i for i in items if is_recent(i["pubDate"])]
        recent = [i for i in recent if not is_junk_title(i["title"])]
        recent = [i for i in recent if not is_government_source(i.get("_source_label", source_label))]
        recent = recent[:MAX_ITEMS_PER_SOURCE]
        print(f"    → {len(items)} items, {len(recent)} dalam 24 jam (setelah filter junk+gov)")

        for idx, item in enumerate(recent):
            item["_source_label"] = source_label
            all_news.append(build_news_item(item, source_label, idx))

    # Dari Google News RSS (berita Indonesia — agregator swasta)
    for query, label in BERITA_GNEWS_QUERIES:
        url = (
            f"https://news.google.com/rss/search?"
            f"q={urllib.parse.quote(query)}&hl=id&gl=ID&ceid=ID:id"
        )
        print(f"  Google News Berita: {query} → {label}")
        items = fetch_rss(url)
        recent = [i for i in items if is_recent(i["pubDate"])]
        recent = [i for i in recent if not is_junk_title(i["title"])]
        recent = [i for i in recent if not is_government_source(label)]
        recent = recent[:MAX_ITEMS_PER_SOURCE]
        print(f"    → {len(items)} items, {len(recent)} dalam 24 jam (setelah filter junk+gov)")

        for item in recent:
            item["_source_label"] = label
            all_news.append(build_news_item(item, label, len(all_news)))

    print(f"  Total berita candidates: {len(all_news)}")

    existing_news = update_news_json(all_news)
    print(f"  news.json: {len(existing_news['items'])} total items")
    print()

    # ── 2. Teknologi ─────────────────────────────────────────────────────────
    print("[2/2] Fetch teknologi dari Google News RSS")
    all_tech = []

    # Dari Google News RSS (topik tech global)
    for query, label in TECH_GNEWS_QUERIES:
        url = (
            f"https://news.google.com/rss/search?"
            f"q={urllib.parse.quote(query)}&hl=id&gl=ID&ceid=ID:id"
        )
        print(f"  Google News Tech: {query} → {label}")
        items = fetch_rss(url)
        recent = [i for i in items if is_recent(i["pubDate"])]
        recent = [i for i in recent if not is_junk_title(i["title"])]
        recent = [i for i in recent if not is_government_source(label)]
        recent = recent[:MAX_ITEMS_PER_SOURCE]
        print(f"    → {len(items)} items, {len(recent)} dalam 24 jam (setelah filter junk+gov)")

        for item in recent:
            item["_source_label"] = label
            all_tech.append(item)

    print(f"  Total tech candidates: {len(all_tech)}")
    print()

    # Filter: ambil item yang belum ada di blog, bukan junk, bukan government
    existing_files = set(f.name for f in BLOG_DIR.glob("*.md"))
    new_posts = []
    for item in all_tech[:MAX_BLOG_NEW * 3]:
        title = trim_title(item["title"])
        source_label = item.get("_source_label", "")
        if is_junk_title(title):
            continue
        if is_government_source(source_label):
            continue
        slug = slugify(title) or "tech-unknown"
        filename = f"{slug}.md"
        if filename not in existing_files:
            new_posts.append(item)

    written = write_new_blog_posts(new_posts)
    print(f"[*] Blog posts baru dibuat: {written}")
    print(f"[*] Selesai. File berubah: commit + push → GitHub Actions deploy ke Pages.")


if __name__ == "__main__":
    main()