"""Pemindai korupi teks.

Generasi teks panjang rawan memunculkan artefak: karakter non-Latin yang
bocor (Mandarin, Korea, Siril), kata campuran huruf, kalimat terpotong, dan
penanda yang tertinggal. Semua harus nol sebelum konten di-deploy.

Jalankan: python3 scan_mojibake.py <file...>
"""
import re
import sys
from pathlib import Path

# huruf yang sah dalam bahasa Indonesia + istilah teknis umum
ALLOWED_EXTRA = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

MOJIBAKE_CHARS = re.compile(
    "["
    "\u2e80-\u2fdf"   # CJK radicals & punctuation
    "\u3000-\u303f"   # CJK symbols, Hiragana start
    "\u3040-\u30ff"   # Hiragana + Katakana
    "\u3100-\u312f"   # Bopomofo
    "\u3130-\u318f"   # Hangul compatibility Jamo
    "\u3400-\u4dbf"   # CJK ext A
    "\u4e00-\u9fff"   # CJK unified
    "\ua960-\ua97f"   # Hangul Jamo ext A
    "\uac00-\ud7af"   # Hangul syllables
    "\uf900-\ufaff"   # CJK compatibility
    "\uff00-\uffef"   # Fullwidth forms
    "\u0530-\u058f"   # Armenian
    "\u0600-\u06ff"   # Arabic
    "\u0900-\u097f"   # Devanagari
    "\u0e00-\u0e7f"   # Thai
    "]"
)

# kata campuran huruf di tengah kata (tidak sah dalam bahasa Indonesia)
CAMEL = re.compile(r"\b[a-z]{2,}[A-Z][a-z]{2,}\b")

# tanda pengalorean yang tertinggal
LEFTOVER = re.compile(
    r"\{[a-zA-Z_]+\}|\bTODO\b|\bPLACEHOLDER\b|___|\bFIXME\b|"
    r"<<|>>|\bundefined\b|\bNaN\b|\[object"
)

# kalimat yang berakhir tanpa kata (terpotong)
TRUNCATED = re.compile(r"\b(?:yang|dengan|untuk|pada|ke|di|dan|atau)\s*[.,;:]")


def scan(text: str) -> list[str]:
    issues = []
    body = re.sub(r"```.*?```", "", text, flags=re.S)  # abaikan blok kode
    body = re.sub(r"^---.*?^---", "", body, flags=re.S | re.M)

    for m in MOJIBAKE_CHARS.finditer(body):
        ctx = body[max(0, m.start() - 25):m.start() + 25].replace("\n", " ")
        issues.append(f"karakter non-Latin {m.group()!r} (U+{ord(m.group()):04X}) di: …{ctx}…")

    allowed_camel = {
        "APIs", "IPv4", "IPv6", "WebGPU", "PyTorch", "NodeJS", "iOS",
        # identifier Kotlin/TypeScript yang memang CamelCase
        "consolidateAfter", "commonMain", "sourceSets", "jvmTarget",
    }
    for m in CAMEL.finditer(body):
        w = m.group()
        if w in allowed_camel:
            continue
        issues.append(f"kata campuran huruf: {w!r}")

    for m in LEFTOVER.finditer(body):
        issues.append(f"penanda tertinggal: {m.group()!r}")

    return issues


def main(paths):
    total = 0
    for p in paths:
        path = Path(p)
        files = [path] if path.is_file() else sorted(path.rglob("*.md"))
        for f in files:
            found = scan(f.read_text(encoding="utf-8"))
            if found:
                total += len(found)
                print(f"\n  {f}")
                for x in found[:6]:
                    print(f"     - {x}")
                if len(found) > 6:
                    print(f"     …dan {len(found) - 6} lagi")
    print(f"\ntotal masalah: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    args = sys.argv[1:] or ["src/data/blog"]
    sys.exit(main(args))