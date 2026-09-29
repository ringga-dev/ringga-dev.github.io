#!/usr/bin/env python3
"""
Fetch trending posts from Reddit (social media) and generate:
- src/data/news.json  (berita dari subreddit Indonesia/berita)
- src/data/blog/*.md   (teknologi dari subreddit technology/opensource/sysadmin)

Reddit public JSON API - no auth required, ~100 req/jam limit, cukup untuk sekali/hari.
"""

import json
import re
import html
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

# ─── Config ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
NEWS_JSON_PATH = REPO_ROOT / "src" / "data" / "news.json"
BLOG_DIR = REPO_ROOT / "src" / "data" / "blog"

# Reddit subreddits — berita (script filter "firal/viral")
NEWS_SUBREDDITS = [
    "Indonesia",
    "berita",
    "Indonesiaindigo",
]

# Reddit subreddits — teknologi/IT
TECH_SUBREDDITS = [
    "technology",
    "opensource",
    "sysadmin",
    "programming",
]

# User-agent wajib untuk Reddit API
UA = "RinggaDevPortfolioBot/1.0 (social media news aggregator; contact: ringga@example.com)"

# Berapa posting yang diambil per subreddit
POSTS_PER_SUB = 5

# Kapan terakhir konten di-fetch (di-bypass, kita ambil yang terbaru)
PAST_DAYS = 1  # ambil posting dalam 24 jam terakhir

# Kata-kata yang menandakan "firal/viral" di judul
VIRAL_KEYWORDS = [
    "viral", "fenomenal", "heboh", "borok", "baru terungkap",
    "menyala", "geger", "krisis", "skandal", "terbongkar",
    "menghebohkan", "menohok", "syok", "kebocoran",
]

# ─── Helpers ───────────────────────────────────────────────────────────────

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def reddit_timestamp_to_date(ts: int) -> str:
    """Convert Reddit unix timestamp to YYYY-MM-DD."""
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d")


def is_recent(ts: int) -> bool:
    cutoff = utc_now() - timedelta(days=PAST_DAYS)
    return datetime.fromtimestamp(ts, tz=timezone.utc) >= cutoff


def clean_html(text: str) -> str:
    """Strip HTML tags, decode entities, basic cleanup."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_viral_title(title: str) -> bool:
    lower = title.lower()
    return any(kw in lower for kw in VIRAL_KEYWORDS)


def sanitize_slug(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    # batasi panjang
    return slug[:80]


def slug_from_title_and_subreddit(title: str, subreddit: str, index: int) -> str:
    base = sanitize_slug(title)
    if not base:
        base = f"post-{index}"
    return f"{subreddit}-{base}"


# ─── Fetch Reddit ─────────────────────────────────────────────────────────

def fetch_subreddit_posts(subreddit: str, limit: int = POSTS_PER_SUB) -> list[dict]:
    """Fetch hot posts from a subreddit, return list of simplified post dicts."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": limit, "t": "day"}
    headers = {"User-Agent": UA}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [WARN] Gagal fetch r/{subreddit}: {e}", file=sys.stderr)
        return []

    data = resp.json()
    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        title = post.get("title", "")
        is_self = post.get("is_self", False) and post.get("selftext", "")

        # Skip video-only / image-only posts kalau nggak ada teks
        body = post.get("selftext", "") if is_self else ""
        if not body and not is_self:
            # external link — ambil judul aja sebagai excerpt
            body = ""

        created = post.get("created_utc", 0)

        posts.append({
            "title": title,
            "body": clean_html(body),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "source_url": post.get("url", ""),
            "subreddit": subreddit,
            "author": post.get("author", "[deleted]"),
            "created_utc": created,
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "is_self": is_self,
            "is_video": post.get("is_video", False),
            "is_self_op": is_self,
        })

    return posts


# ─── Generate News JSON ────────────────────────────────────────────────────

def build_news_item(post: dict, index: int) -> dict:
    """Convert Reddit post (berita) to news.json item format."""
    subreddit = post["subreddit"]
    title = post["title"]
    body = post["body"]
    created = post["created_utc"]
    score = post["score"]
    comments = post["num_comments"]

    date_str = reddit_timestamp_to_date(created)
    slug = slug_from_title_and_subreddit(title, subreddit, index)

    # Excerpt dari body atau judul
    excerpt = body[:200] if body else title[:200]

    # Summary lebih panjang
    summary = body[:600] if body else title[:300] + " (posting viral dari Reddit)"

    # Kategori berdasarkan subreddit
    if subreddit in ("Indonesia", "berita", "Indonesiaindigo"):
        category = "Indonesia" if subreddit == "Indonesia" else "Berita"
    else:
        category = "Sosial Media"

    # Tags dari judul
    tags = []
    lower_title = title.lower()
    if any(kw in lower_title for kw in ["politik", "gov", "dnp", "partai"]):
        tags.append("Politik")
    if any(kw in lower_title for kw in ["ekonomi", "harga", "rupiah"]):
        tags.append("Ekonomi")
    if is_viral_title(title):
        tags.append("Viral")
    tags.append("Reddit")
    tags.append(subreddit)
    tags = list(dict.fromkeys(tags))[:5]

    # Key facts dari body
    key_facts = []
    for line in body.split("\n")[:5]:
        line = line.strip()
        if len(line) > 20 and len(line) < 200:
            key_facts.append(line)

    return {
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
        "category": category,
        "source": f"Reddit r/{subreddit}",
        "sourceUrl": f"https://reddit.com{post['permalink']}",
        "date": date_str,
        "image": "",  # nggak ada image dari Reddit API tanpa OAuth
        "tags": tags,
        "summary": summary,
        "keyFacts": key_facts if key_facts else [f"Score: {score} | Komentar: {comments}"],
    }


def update_news_json(news_items: list[dict]) -> None:
    """Update src/data/news.json with new items (prepend, max 10 items)."""
    if NEWS_JSON_PATH.exists():
        with open(NEWS_JSON_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {
            "title": "Berita dari Sosial Media",
            "subtitle": "Kompilasi berita terbaru dari Reddit — isu politik, berkah, dan tren sosial media.",
            "updatedAt": utc_now().strftime("%Y-%m-%d"),
            "items": [],
        }

    existing["updatedAt"] = utc_now().strftime("%Y-%m-%d")

    # Merge: items baru di depan, duplikat berdasarkan slug di-skip
    existing_slugs = {item["slug"] for item in existing.get("items", [])}
    merged = []
    for item in news_items:
        if item["slug"] not in existing_slugs:
            merged.append(item)

    # Prepend new items
    merged = merged + existing.get("items", [])
    # Limit max 10 items
    existing["items"] = merged[:10]

    with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"  [news.json] {len(news_items)} item baru disaring, total: {len(existing['items'])}")


# ─── Generate Blog Markdown ────────────────────────────────────────────────

def build_blog_frontmatter(post: dict, index: int) -> str:
    """Build YAML frontmatter untuk blog post."""
    subreddit = post["subreddit"]
    title = post["title"]
    body = post["body"]
    created = post["created_utc"]
    date_str = reddit_timestamp_to_date(created)

    slug = slug_from_title_and_subreddit(title, subreddit, index)

    # Category dari subreddit
    cat_map = {
        "technology": "Technology",
        "opensource": "Open Source",
        "sysadmin": "DevOps & Sysadmin",
        "programming": "Programming",
    }
    category = cat_map.get(subreddit, "Technology")

    # Tags
    tags = [subreddit, "Reddit", "Trending"]
    if is_viral_title(title):
        tags.append("Viral")
    tags = list(dict.fromkeys(tags))[:6]

    # Excerpt
    excerpt = body[:160] if body else title[:160]

    return (
        f"---\n"
        f"title: \"{title}\"\n"
        f"description: \"{excerpt}\"\n"
        f"date: \"{date_str}\"\n"
        f"author: \"Ringga Septia Pribadi\"\n"
        f"tags: [{', '.join(json.dumps(t) for t in tags)}]\n"
        f"category: \"{category}\"\n"
        f"image: \"https://images.unsplash.com/photo-1555066931-4365d14bab6c?q=80&w=2070&auto=format&fit=crop\"\n"
        f"---\n"
    )


def build_blog_body(post: dict) -> str:
    """Build markdown body dari Reddit post."""
    title = post["title"]
    body = post["body"]
    subreddit = post["subreddit"]
    author = post["author"]
    score = post["score"]
    comments = post["num_comments"]
    url = f"https://reddit.com{post['permalink']}"

    lines = [
        f"\n## Pendahuluan\n\n",
        f"Posting ini diambil dari **r/{subreddit}** di Reddit — sosial media diskusi teknologi terbesar di dunia. "
        f" Konten asli ditulis oleh u/{author}.\n\n",
    ]

    if body:
        # Split body menjadi paragraf
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        for p in paragraphs[:8]:  # max 8 paragraf
            # Convert mentions ke format yang lebih rapi
            p = re.sub(r"/u/(\w+)", r"u/\1", p)
            p = re.sub(r"/r/(\w+)", r"r/\1", p)
            lines.append(f"{p}\n\n")

    # Info footer
    lines.extend([
        "\n---\n\n",
        f"**Sumber:** [r/{subreddit}]({url}) | Reddit\n",
        f"**Author:** u/{author} | Score: {score} | Komentar: {comments}\n",
        f"**Dipetik oleh:** Ringga Dev Portfolio — agregator berita teknologi harian\n",
    ])

    return "".join(lines)


def generate_blog_md(post: dict, index: int) -> str:
    """Return full markdown content untuk blog post."""
    fm = build_blog_frontmatter(post, index)
    body = build_blog_body(post)
    return fm + "\n" + body


def write_new_blog_posts(posts: list[dict]) -> int:
    """Write new .md files ke src/data/blog/ yang belum ada. Return count."""
    existing_files = set(f.name for f in BLOG_DIR.glob("*.md"))
    written = 0

    for idx, post in enumerate(posts):
        slug = slug_from_title_and_subreddit(post["title"], post["subreddit"], idx)
        filename = f"{slug}.md"

        if filename in existing_files:
            continue

        md_content = generate_blog_md(post, idx)
        filepath = BLOG_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        written += 1
        print(f"  [blog] Created: {filename}")

    return written


# ─── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"[*] Reddit Social Media Fetcher — {utc_now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"[*] Repo root: {REPO_ROOT}")
    print()

    # ── 1. Fetch berita dari subreddit Indonesia ──────────────────────────
    print("[1/2] Fetch berita dari r/Indonesia, r/berita, ...")
    all_news_posts = []
    for sub in NEWS_SUBREDDITS:
        print(f"  Fetching r/{sub} ...")
        posts = fetch_subreddit_posts(sub, POSTS_PER_SUB)
        # Filter: hanya yang recent + punya isi
        recent_posts = [p for p in posts if is_recent(p["created_utc"])]
        all_news_posts.extend(recent_posts)
        print(f"    → {len(posts)} posts, {len(recent_posts)} yang dalam 24 jam terakhir")

    # Filter lagi: cukup yang ada title-nya
    all_news_posts = [p for p in all_news_posts if p["title"].strip()]
    print(f"  Total berita candidates: {len(all_news_posts)}")

    # Build news items
    news_items = [build_news_item(p, i) for i, p in enumerate(all_news_posts[:10])]
    update_news_json(news_items)
    print()

    # ── 2. Fetch tech dari subreddit teknologi ────────────────────────────
    print("[2/2] Fetch teknologi dari r/technology, r/opensource, ...")
    all_tech_posts = []
    for sub in TECH_SUBREDDITS:
        print(f"  Fetching r/{sub} ...")
        posts = fetch_subreddit_posts(sub, POSTS_PER_SUB)
        recent_posts = [p for p in posts if is_recent(p["created_utc"])]
        all_tech_posts.extend(recent_posts)
        print(f"    → {len(posts)} posts, {len(recent_posts)} dalam 24 jam")

    all_tech_posts = [p for p in all_tech_posts if p["title"].strip()]
    print(f"  Total tech candidates: {len(all_tech_posts)}")

    written = write_new_blog_posts(all_tech_posts[:10])
    print(f"\n[*] Blog posts baru dibuat: {written}")
    print(f"[*] Selesai. Commit + push untuk trigger deploy ke GitHub Pages.")


if __name__ == "__main__":
    main()
