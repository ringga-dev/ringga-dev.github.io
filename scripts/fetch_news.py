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

# ── Gambar berita: sub-tema granular (dicek sebelum kategori) ────────────
# Dipakai kalau RSS tidak menyediakan gambar sendiri (mis. Google News RSS).
NEWS_THEME_IMAGES = [
    (["game", "gim", "gacha", "free fire", "pubg", "valorant",
      "esport", "kode redeem", "gameplay", "steam", "mlbb", "ff ",
      "playstation", "xbox", "nintendo", "genshin", "honor of kings"],
     "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&q=80"),
    (["belanja", "tokopedia", "shopee", "lazada", "bukalapak", "blibli",
      "jualan", "murah", "diskon", "promo", "beli", "gratis ongkir",
      "e-commerce", "checkout", "keranjang"],
     "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80"),
    (["viral", "trending", "heboh", "terbongkar", "kejutan", "menyala",
      "gergeviral", "nampar", "dilukai", "salah paham"],
     "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=800&q=80"),
    (["pembunuhan", "tewas", "bunuh", "korban", "jasad", "lambak",
      "polisi", "tertangkap", "tersangka", "peliburan",
      "pemerasan", "perampokan", "kekerasan", "cidik", "siksa"],
     "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80"),
    (["fifa", "sepak bola", "bola", "liga", "persib", "persija", "tim nasional",
      "asian cup", "piala", "badminton", "tenis", "atletik", "marathon",
      "turnamen", "kejuaraan", "sea games", "olimpiade", "formula 1"],
     "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800&q=80"),
    (["gempa", "banjir", "kebakaran", "bencana", "erupsi", "gunung", "merapi",
      "krakatau", "tsunami", "tanah longsor", "angin=topan", "puting belah",
      "meteor", "hujan ekstrem", "kekeringan"],
     "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800&q=80"),
    (["sekolah", "universitas", "kampus", "mahasiswa", "guru", "murid",
      "pendidikan", "beasiswa", "ujian", "kelas", "sma", "sd", "smp"],
     "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&q=80"),
    (["obat", "rumah sakit", "hospital", "kesehatan", "dokter", "vaksin",
      "penyakit", "gizi", "medis", "klinik", "imunisasi"],
     "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80"),
    (["teknologi", "aplikasi", "gadget", "smartphone", "internet", "sinyal",
      "startup", "chip", "laptop", "komputer", "robot", "otomotif", "mobil",
      "motor", "pesawat", "kereta api", " whatsapp", "telegram",
      "siber", "hp android", "ai", "kecerdasan buatan", "otomatis"],
     "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80"),
    (["rupiah", "bursa", "saham", "bank", "ekonomi", "usaha", "bisnis",
      "investasi", "gaji", "upah", "harga", "warung", "dagang", "ekspor",
      "impor", "pajak", "umkm", "biaya", "subsidi", "pasar"],
     "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80"),
    (["hiburan", "musik", "film", "artis", "seleb", "drama", "konser",
      "sinema", "layar", "kreatif", "desain", "fesyen", "baju", "kebaya"],
     "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800&q=80"),
    (["cafe", "resto", "restaurant", "makan", "kuliner", "food", "goreng",
      "minum", "coffee", "hidangan", "dagel", "jajan"],
     "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80"),
    (["jalan", "transport", "terminal", "bandar", "pelabuhan", "lalu lintas",
      "tol", "parkir", "armada", "bus", "mikrolet", "kereta"],
     "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800&q=80"),
    (["pertanian", "padi", "tani", "ikan", "peternakan", "sawit",
      "kelapa", "panen"],
     "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80"),
]

# ── Gambar berita berdasarkan kategori (Unsplash) ─────────────────────────
NEWS_CATEGORY_IMAGES = {
    "Politik":   "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80",
    "Viral":     "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=800&q=80",
    "Kriminal":  "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80",
    "Ekonomi":   "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&q=80",
    "Bencana":   "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800&q=80",
    "Berita":    "https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&q=80",
}

# ── Gambar blog berdasarkan kategori (Unsplash) ────────────────────────────
TECH_CATEGORY_IMAGES = {
    "Artificial Intelligence":  "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
    "Cybersecurity":            "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
    "Cloud & DevOps":          "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80",
    "Open Source":             "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&q=80",
    "Mobile & Apps":           "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&q=80",
    "Teknologi Informasi":      "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&q=80",
}

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

    with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return existing


def pick_news_image(item: dict, title: str, category: str) -> str:
    """Pilih gambar berita: gambar asli RSS > sub-tema keyword > kategori.

    Google News RSS tidak menyertakan gambar, jadi butuh fallback tema.
    """
    # 1. Gambar asli dari RSS (paling relevan dengan judul)
    rss_img = (item.get("image") or "").strip()
    if rss_img.startswith("http"):
        return rss_img.replace("&amp;", "&")

    # 2. Sub-tema granular berdasarkan keyword di judul (word-boundary,
    #    supaya "ai" tidak match di "capai" dan "sd" tidak match di "sdri")
    title_lower = title.lower()
    for keywords, img in NEWS_THEME_IMAGES:
        for kw in keywords:
            kw = kw.strip().lower()
            if not kw:
                continue
            if re.search(rf"(?<!\w){re.escape(kw)}(?!\w)", title_lower):
                return img

    # 3. Fallback kategori
    return NEWS_CATEGORY_IMAGES.get(category, NEWS_CATEGORY_IMAGES["Berita"])


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

    rss_img = (item.get("image") or "").strip().replace("&amp;", "&")
    if not rss_img.startswith("http"):
        rss_img = ""

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
        f"image: \"{rss_img or TECH_CATEGORY_IMAGES.get(category, TECH_CATEGORY_IMAGES['Teknologi Informasi'])}\"\n"
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

    return written


# ─── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
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