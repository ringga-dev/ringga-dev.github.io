#!/usr/bin/env python3
"""
Gerbang mutu konten — WAJIB jalan sebelum deploy.

Tujuan: memastikan kesalahan yang sudah pernah terjadi tidak bisa lolos lagi.
Jenis bug yang dijaga:

  1. Konten kosong / stub — post atau berita di bawah ambang kata minimum
  2. Field wajib hilang — dllahulu /news balas 500 karena `updatedAt` hilang
     sementara 15 halaman /news/<slug> tetap normal
  3. Route gagal prerender tapi build tetap "sukses" — karena
     prerender.failOnError = false, route hilang dari dist tanpa error
  4. Gambar rusak / duplikat / kosong
  5. Merge conflict marker ikut ter-commit

Exit non-zero = deploy gagal. Script ini tidak bisa di-skip diam-diam.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "src" / "data" / "blog"
NEWS = ROOT / "src" / "data" / "news.json"
DIST = ROOT / "dist" / "public"

MIN_WORDS = 1000          # ambang isi minimum per halaman
BOILER = ("**Sumber:**", "**Dirangkum oleh:**", "**Dipetik dari RSS")
CONFLICT = re.compile(r"^<<<<<<< |^=======$|^>>>>>>> ", re.M)
IMG_RE = re.compile(r"^image:\s*[\"']?([^\"'\s]+)", re.M)

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  [GAGAL] {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"  [WARN ] {msg}")


def body_words(text: str) -> int:
    for marker in BOILER:
        text = text.split(marker)[0]
    return len(text.split())


def check_images(urls: list[str]) -> tuple[int, list[str]]:
    """Cek URL gambar hidup. Kembalikan (total, yang rusak)."""
    if not urls:
        return 0, []

    def probe(u: str):
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        try:
            r = urllib.request.urlopen(req, timeout=25)
            ok = r.status == 200 and "image" in r.headers.get("Content-Type", "").lower()
            return u, ok
        except Exception:
            return u, False

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(probe, urls))
    return len(results), [u for u, ok in results if not ok]


# ─────────────────────────── BLOG ───────────────────────────
print("=" * 66)
print("GERBANG MUTU KONTEN")
print(f"Ambang minimum: {MIN_WORDS} kata per halaman")
print("=" * 66)

print("\n[1/5] Post blog")
posts = sorted(BLOG.glob("*.md"))
print(f"  ditemukan {len(posts)} post")

short, blog_images, slugy = [], [], set()
for f in posts:
    raw = f.read_text(encoding="utf-8")

    if CONFLICT.search(raw):
        fail(f"{f.name}: masih ada merge conflict marker")

    if "\n---\n" not in raw:
        fail(f"{f.name}: frontmatter tidak bisa dibaca")
        continue

    words = body_words(raw.split("\n---\n", 1)[1])
    if words < MIN_WORDS:
        short.append((f.stem, words))

    m = IMG_RE.search(raw)
    if not m:
        fail(f"{f.name}: field image tidak ada")
    else:
        blog_images.append(m.group(1))

    title = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', raw, re.M)
    if not title:
        fail(f"{f.name}: field title tidak ada")
    elif f.stem not in slugy:
        slugy.add(f.stem)

if not posts:
    fail("tidak ada post blog sama sekali")

if short:
    short.sort(key=lambda x: x[1])
    for stem, w in short:
        fail(f"blog/{stem}: hanya {w} kata (min {MIN_WORDS})")
else:
    print(f"  semua {len(posts)} post >= {MIN_WORDS} kata")

if blog_images:
    if len(set(blog_images)) != len(blog_images):
        dupes = [u for u in set(blog_images) if blog_images.count(u) > 1]
        fail(f"gambar blog tidak unik: {len(dupes)} URL dipakai lebih dari sekali")
    else:
        print(f"  gambar blog unik: {len(blog_images)}/{len(blog_images)}")

# ─────────────────────────── NEWS ───────────────────────────
print("\n[2/5] Berita")
if not NEWS.exists():
    fail("src/data/news.json tidak ditemukan")
    news_items = []
else:
    doc = json.loads(NEWS.read_text(encoding="utf-8"))
    news_items = doc.get("items", [])

    # field level-level — biang pembunuh /news 500
    for key in ("title", "subtitle", "updatedAt"):
        if not doc.get(key):
            fail(f"news.json: field level-level '{key}' hilang atau kosong "
                 f"(NewsListing.vue memakainya — /news akan 500)")

    need = ["slug", "title", "excerpt", "category", "source", "sourceUrl",
            "date", "image", "tags", "summary", "keyFacts"]
    for item in news_items:
        missing = [k for k in need if not item.get(k)]
        if missing:
            fail(f"news/{item.get('slug', '?')[:40]}: field hilang {missing}")

print(f"  ditemukan {len(news_items)} berita")

nshort, news_images, news_slugs = [], [], []
for item in news_items:
    words = len((item.get("summary") or "").split())
    if words < MIN_WORDS:
        nshort.append((item.get("slug", "?")[:44], words))
    if item.get("image"):
        news_images.append(item["image"])
    news_slugs.append(item.get("slug"))

if nshort:
    nshort.sort(key=lambda x: x[1])
    for slug, w in nshort:
        fail(f"news/{slug}: hanya {w} kata (min {MIN_WORDS})")
else:
    print(f"  semua {len(news_items)} berita >= {MIN_WORDS} kata")

for label, vals in [("slug berita", news_slugs), ("gambar berita", news_images)]:
    real = [v for v in vals if v]
    if real and len(set(real)) != len(real):
        fail(f"{label} tidak unik")

if news_images and len(set(news_images)) == len(news_images):
    print(f"  gambar berita unik: {len(news_images)}/{len(news_images)}")

# ─────────────────── GAMBAR: URL hidup ───────────────────
print("\n[3/5] URL gambar (cek HTTP)")
all_imgs = sorted(set(blog_images) | set(news_images))
if all_imgs:
    total, broken = check_images(all_imgs)
    if broken:
        for u in broken[:8]:
            fail(f"gambar rusak: {u}")
        if len(broken) > 8:
            fail(f"...dan {len(broken) - 8} URL gambar rusak lainnya")
    else:
        print(f"  {total} URL gambar, semuanya hidup")

# ─────────── ROUTE: hasil prerender beneran ada ───────────
print("\n[4/5] Route hasil prerender")
if not DIST.exists():
    warn("dist/public belum ada — lewati (jalankan setelah nuxt build)")
else:
    import math

    expected = []
    nb = len(posts)
    nw = len(news_items)
    expected += [f"blog/index.html"] + [
        f"blog/page/{p}/index.html" for p in range(2, max(1, math.ceil(nb / 9)) + 1)]
    expected += [f"news/index.html"] + [
        f"news/page/{p}/index.html" for p in range(2, max(1, math.ceil(nw / 9)) + 1)]
    expected += [f"blog/{f.stem}/index.html" for f in posts]
    expected += [f"news/{s}/index.html" for s in news_slugs if s]

    missing = [r for r in expected if not (DIST / r).exists()]
    if missing:
        # ini persis kelas bug yang failOnError:false sembunyikan
        for r in missing[:10]:
            fail(f"route tidak ter-prerender: /{r} — build tetap sukses, "
                 f"tapi halamannya tidak akan ada")
        if len(missing) > 10:
            fail(f"...dan {len(missing) - 10} route lain tidak ter-prerender")
    else:
        print(f"  {len(expected)} route ada di dist")

# ─────────────────── RINGKASAN ───────────────────
print("\n" + "=" * 66)
print(f"GAGAL: {len(failures)}   WARN: {len(warnings)}")
if failures:
    print("\nDEPLOY DIBLOKIR. Perbaiki di atas lebih dulu:")
    for f in failures:
        print(f"  - {f}")
    print("=" * 66)
    sys.exit(1)

print("Lolos — deploy boleh jalan.")
print("=" * 66)
sys.exit(0)