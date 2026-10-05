#!/usr/bin/env python3
"""Bersihkan kredit & sisa navigasi dari isi berita.

Portal berita menyisipkan blok seperti:

    Comment SHARE url telah tercopy Redaksi, CNBC Indonesia 04 October
    2026 09:00 Foto: Jay Clayton, Jaksa AS ... (Ken Cedeno / AFP)

Blok itu bukan kalimat berita. Kalau dibiarkan, credibilitySources hilang
dan pembaca melihat potongan yang tidak masuk akal di awal artikel.

Strategi: pecah per kalimat, buang kalimat yang mengandung penanda kredit.
Kalau kalimat itu memuat berita juga, ambil bagian setelah penandanya —
bukan memotong seluruhnya.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEWS = ROOT / "src" / "data" / "news.json"

MARK = re.compile(
    r"Comment\s+SHARE|telah\s+tercopy|^\s*Foto:"
    r"|\(\s*(?:Dokumen|REUTERS|AFP|AP|Getty|istimewa)\b",
    re.I,
)

BYLINE = re.compile(
    r"^(?:\s*[A-Z][\w.'-]*\s*){0,4}", re.I)


def strip_credit(text: str) -> str:
    out = []
    for para in text.split("\n\n"):
        keep = []
        for sent in re.split(r"(?<=[.!?])\s+", para):
            m = MARK.search(sent)
            if not m:
                keep.append(sent)
                continue
            # kalimat tercemar: coba simpan bagian setelah penanda
            tail = sent[m.end():]
            if ")" in tail[:180]:
                tail = re.sub(r"^.*?\)\s*", "", tail)
            tail = BYLINE.sub("", tail)
            if len(tail.split()) >= 12 and not MARK.search(tail):
                keep.append(tail.strip())
        joined = " ".join(x for x in keep if x.strip())
        if len(joined.split()) >= 8:
            out.append(joined)
    return "\n\n".join(out)


def main() -> int:
    doc = json.loads(NEWS.read_text(encoding="utf-8"))
    cleaned = 0
    for item in doc["items"]:
        new = re.sub(r"\s{2,}", " ", strip_credit(item["summary"])).strip()
        if new and new != item["summary"]:
            cleaned += 1
        if new:
            item["summary"] = new
        item["excerpt"] = re.sub(r"\s{2,}", " ", new or item["summary"])[:200]
        facts = [f for f in item.get("keyFacts", []) if not MARK.search(f)]
        if facts:
            item["keyFacts"] = facts

    left = [i["slug"] for i in doc["items"] if MARK.search(i["summary"])]
    NEWS.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{cleaned} item dibersihkan; sisa penanda kredit: {left or 'tidak ada'}")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())