---
title: "Software Supply Chain Security 2026: SBOM, SLSA, dan Sigstore sebagai Standar Baru"
description: "Ancaman rantai pasok software semakin nyata di 2026 — dari dependency poisoning hingga backdoor di library populer. Pelajari SBOM, SLSA Levels, dan Sigstore untuk mengamankan pipeline pengembangan Anda."
date: "2026-08-01"
author: "Ringga Septia Pribadi"
tags: ["Cybersecurity", "Supply Chain", "SBOM", "SLSA", "Sigstore", "DevSecOps"]
category: "Cybersecurity"
image: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&q=80"
---

## Pendahuluan

Serangan *software supply chain* telah menjadi ancaman siber paling mahal di dekade ini. Insiden seperti backdoor **xz-utils** (2024) yang hampir menyusup ke distribusi Linux utama membuktikan bahwa attacker tidak lagi menyerang kode Anda. Mereka menyerang **kode yang Anda gunakan**.

Yang membuat kelas serangan ini berbeda: Anda bisa punya kode sendiri yang sempurna, review ketat, dan tes lengkap, tetapi tetap dikompromikan lewat satu dependency yang Anda percaya. Trust Anda, bukan defens Anda, yang jadi permukaan serangan.

Di 2026, keamanan rantai pasok bukan lagi opsional. Regulasi seperti **US Executive Order 14028** dan **EU Cyber Resilience Act** mewajibkan produsen software menerbitkan SBOM dan membuktikan integritas artefak. Artikel ini membahas tiga pilarnya: **SBOM**, **SLSA**, dan **Sigstore**.

## Peta Tenggat Regulasi 2026

Sebelum masuk teknis, ada baiknya menyebut tanggalnya dengan tepat karena ini yang mengubah prioritas di banyak organisasi.

**EU Cyber Resilience Act (CRA).** Berlaku sejak 10 Desember 2024, dengan tiga gelombang kewajiban:

| Tahap | Tanggal berlaku | Isi |
|-------|-----------------|-----|
| Chapter IV | 11 Juni 2026 | Notifikasi badan penilaian kesesuaian |
| Pasal 14 | 11 September 2026 | Kewajiban pelaporan vulnerability dan insiden yang sedang dieksploitasi aktif |
| Ketentuan utama | 11 Desember 2027 | SBOM wajib, security by design, security by default |

Bentuk kewajiban SBOM di CRA spesifik: produsen harus membuat, memelihara, dan bila diperlukan berbagi dengan otoritas pengawas pasar SBOM untuk setiap produk elemen digital. SBOM harus dalam format yang umum dan machine-readable, mencakup **minimal dependency tingkat atas**, diperbarui sepanjang siklus hidup produk, dan dimasukkan ke dokumentasi teknis serta proses penanganan vulnerability.

Satu detail penting yang sering disalahpahami: **CRA tidak mewajibkan SBOM dipublikasikan**. SBOM diserahkan ke otoritas pengawas pasar bila diminta. Ini membuatnya berbeda dari transparansi penuh yang dicontohkan sebagian komunitas open source.

**US Executive Order 14028** tetap menjadi acuan bagi pemerintah federal AS, menuntut SBOM dan attestation untuk software yang dikonsumsi instansi federal.

Komisi Eropa juga menerbitkan panduan praktis CRA untuk membantu bisnis menerapkan aturannya, menjelaskan cakupan produk, apa yang dihitung sebagai substantial modification, dan cara memahami support period. Jadi alasan "belum ada kejelasan" mulai menipis.

## 1. SBOM: Inventaris Setiap Komponen

**Software Bill of Materials (SBOM)** adalah daftar formal seluruh komponen (library, container image, tooling) yang menyusun sebuah aplikasi. Format dominan di 2026: **SPDX** (ISO/IEC 5962) dan **CycloneDX**.

Pilihan formatnya bukan selera. SPDX lahir dari kebutuhan lisensi dan kepatuhan, jadi kuat untuk tim legal dan audit. CycloneDX dirancang untuk keamanan aplikasi dan mendukung OWASP secara native, dengan ekosistem tooling yang lebih matang untuk kerentanan dan VEX. Bila fokus Anda utama adalah vulnerability management, CycloneDX biasanya lebih nyaman. Bila Anda perlu menjawab pertanyaan lisensi sekaligus, SPDX lebih lengkap.

SBOM menjawab pertanyaan kritis saat CVE baru rilis: *"Apakah saya terdampak?"* Tanpa SBOM, tim harus mengaudit manual ribuan dependency. Dengan SBOM cukup jalankan scanner:

```bash
# Generate SBOM dari container image
syft scan docker.io/library/nginx:alpine -o spdx-json > sbom.json

# Scan SBOM terhadap database vulnerability, gagal bila ada high severity
grype sbom.json --fail-on high

# Ekspor ke CycloneDX dengan informasi lisensi
syft packages dir:. -o cyclonedx-json > sbom-cyclonedx.json
```

### Memakai SBOM dengan Benar

SBOM tanpa pemahaman field kunci cepat menjadi data mati. Beberapa yang perlu diperhatikan:

- **`purl` (Package URL).** Identifier standar seperti `pkg:golang/github.com/gin-gonic/gin@v1.9.1`. Inilah kunci untuk mencocokkan komponen dengan database CVE. SBOM tanpa purl yang benar sangat sulit dipakai otomatis.
- **`cpe` (Common Platform Enumeration).** Lebih cocok untuk komponen sistem operasi dan aplikasi yang terdaftar di katalog NVD.
- **Kedalaman dependency.** CRA hanya menuntut dependency tingkat atas, tapi SBOM tingkat atas saja hampir tidak berguna untuk keamanan, karena kerentanan serius biasanya berada di transitive dependency beberapa lapis ke bawah. Untuk kebutuhan keamanan internal, hasilkan SBOM lengkap; untuk kepatuhan, SBOM tingkat atas bisa memenuhi syarat regulator.
- **SBOM sebagai artefak pipeline, bukan dokumen.** Yang berguna adalah SBOM yang dihasilkan otomatis setiap build dan disimpan bersama artefaknya. SBOM yang dibuat manual sekali setahun akan kedaluwarsa sebelum dibaca.

VEX (Vulnerability Exploitability eXchange) melengkapi SBOM dengan menjawab pertanyaan yang tidak bisa dijawab SBOM: apakah kerentanan ini benar-benar bisa dieksploitasi di produk saya, atau kode yang rentan ada tapi tidak terjangkau. Ini yang memisahkan tim yang tenggelam di temuan dari tim yang bisa bertindak.

## 2. SLSA: Level Kematangan Pipeline

**Supply-chain Levels for Software Artifacts (SLSA)** menilai seberapa aman proses build Anda, dari Level 0 hingga 4. Spesifikasi terkini adalah versi 1.2.

| Level | Makna | Persyaratan Kunci |
|-------|-------|-------------------|
| L0 | Tanpa jaminan | - |
| L1 | Build terdokumentasi | Provenance dasar, no secret di log |
| L2 | Build ter-host | Build service terpusat, provenance terautentikasi |
| L3 | Build non-forgeable | Build terisolasi, tidak bisa dimodifikasi developer |
| L4 | Build reproducible | Hermetic build, reproducible, provenance di-hash |

Target realistis untuk tim modern adalah **SLSA Level 3**: build di CI terpusat, artefak ditandatangani, dan *provenance* dihasilkan otomatis, bukan dari laptop developer yang bisa dikompromikan.

### Provenance dan Aturan Distribusinya

Inti SLSA adalah **provenance**, yaitu informasi terverifikasi yang melacak artefak kembali ke source code yang menghasilkannya: di mana, kapan, dan bagaimana sesuatu diproduksi. SLSA membedakan dua jenis: build provenance (melacak output build ke source code) dan source provenance (melacak pembuatan revisi source dan proses manajemen perubahannya).

Beberapa aturan dari spesifikasi SLSA yang punya konsekuensi praktis:

- **Attestation sebaiknya immutable.** Setelah dipublikasikan untuk sebuah artefak, attestation tidak boleh bisa ditimpa dengan attestasi berbeda untuk artefak yang sama. Ini mencegah penyerang mengganti provenance palsu setelah artefak masuk registry.
- **Nama file terkait artefak.** Untuk artefak `<filename>.<extension>`, attestation-nya sebaiknya `<filename>.attestation`. in-toto merekomendasikan `<filename>.intoto.jsonl`.
- **Satu ke banyak.** Sebuah artefak bisa punya banyak attestation. Jangan rancang sistem yang mengasumsikan hubungan satu-ke-satu, karena Anda mungkin perlu attestation provenance, attestation hasil scan kerentanan, dan attestation kepatuhan lisensi untuk artefak yang sama.
- **Publikasi ke transparency log.** Hash attestation dan pointer lokasi index-nya sebaiknya dipublikasikan ke log transparansi pihak ketiga yang berada **di luar** source repository dan package registry. Rekor milik Sigstore adalah contohnya, karena bersifat immutable dan memudahkan monitoring. Proses verifikasi yang mensyaratkan kehadiran attestation di log terpantau membuat attestation jauh lebih dapat dipercaya, karena penyerang tidak bisa sekadar menghapusnya.

Format yang direkomendasikan adalah in-toto SLSA Build Provenance, dengan predicate type `https://slsa.dev/provenance/v1`.

## 3. Sigstore: Code Signing Tanpa Ribet

Masalah klasik *code signing* adalah manajemen kunci privat. Jika bocor, artefak bisa dipalsukan, dan Anda tidak punya cara mudah untuk membuktikan signature mana yang asli dan mana yang dibuat penyerang.

**Sigstore** mengubah paradigma ini dengan *keyless signing*: kunci ephemeral per-build, identitas diverifikasi via **OIDC** (misal `email@example.com`), dan semua tanda tangan tercatat di **transparency log** (Rekor) yang bisa diaudit publik.

Tiga komponennya bekerja bersama:

| Komponen | Peran |
|----------|-------|
| **Fulcio** | Certificate authority yang menerbitkan sertifikat bershort-lived, mengikat identitas OIDC ke public key |
| **Rekor** | Transparency log yang mencatat signed metadata, bisa dicari tapi tidak bisa diubah |
| **Cosign** | CLI untuk menandatangani dan memverifikasi artefak, termasuk penyimpanan di registry OCI |

```bash
# Sign tanpa menyimpan secret kunci
cosign sign --oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/org/app:v1.0.0

# Verifikasi sebelum deploy
cosign verify --certificate-identity \
  "https://github.com/org/app/.github/workflows/*" ghcr.io/org/app:v1.0.0
```

Dengan **cosign + OIDC**, CI menandatangani artefak tanpa menyimpan kunci di mana pun, menghilangkan salah satu vektor serangan terbesar.

### Timestamp: Bagian yang Sering Diabaikan

Karena sertifikat Fulcio bersifat short-lived, Anda tidak punya daftar pencabutan. Verifikasi bergantung pada bukti bahwa sertifikat masih valid **saat penandatanganan terjadi**. Tanpa timestamp tepercaya, masalah ini tidak bisa diselesaikan dengan bersih.

Solusinya adalah Timestamp Authority yang menerbitkan timestamp tertandatangan sesuai RFC 3161. Praktik yang direkomendasikan adalah *countersigning*, yaitu menandatangani di atas signature (bukan di atas artefak), sehingga yang dibuktikan adalah waktu pembuatan signature.

```bash
# Ambil timestamp saat signing
export TSA_URL=https://freetsa.org/tsr
cosign sign --timestamp-server-url $TSA_URL ghcr.io/org/app:v1.0.0

# Verifikasi dengan rantai sertifikat TSA
cosign verify --timestamp-certificate-chain ts_chain.pem ghcr.io/org/app:v1.0.0
```

Jika Anda melihat error `failed to verify timestamps: threshold not met for verified log entry integrated timestamps: 0 < 1`, penyebabnya bukan pipeline Anda rusak, melainkan signature yang diverifikasi memang memerlukan dukungan RFC 3161. Upgrade cosign atau tambahkan `--use-signed-timestamps` pada Cosign 2.6.x.

Kabar baiknya, siapapun bisa menjalankan TSA sendiri. Jika Anda perlu kontrol atas bagian dari trust root sambil tetap memakai Sigstore public good instance, Anda bisa mengoperasikan TSA sendiri dan timestampnya akan dipakai saat verifikasi.

### Attestation, Bukan Hanya Signature

Cosign juga mendukung in-toto attestation, yang menambahkan lapisan semantik di atas signature kriptografis biasa. Berguna untuk sistem kebijakan:

```bash
# Lampirkan hasil scan kerentanan sebagai attestation
cosign attest --predicate scan.json --type vuln \
  ghcr.io/org/app:v1.0.0@sha256:<digest>

# Di deploy, verifikasi provenance SLSA yang dihasilkan CI
cosign verify-attestation --type slsaprovenance \
  --certificate-identity-regexp 'https://github.com/org/app/.*' \
  ghcr.io/org/app:v1.0.0@sha256:<digest>
```

GitHub Actions menyediakan `attest-build-provenance` yang menghasilkan attestation SLSA langsung tanpa konfigurasi tambahan, jadi jalur termudah menuju SLSA L2 atau L3 sering kali sudah ada di tooling yang Anda pakai.

## Praktik Nyata di Pipeline 2026

1. **Pin dependency dengan lockfile.** `package-lock.json`, `go.sum`, `poetry.lock` di-commit dan diverifikasi di CI. Tanpa ini, dua build dari commit yang sama bisa menghasilkan artefak berbeda.
2. **Gunakan OIDC, bukan long-lived token.** `id-token: write` di GitHub Actions menggantikan PAT untuk publish artefak. PAT yang bocor memberi akses berkelanjutan; token OIDC short-lived kedaluwarsa sendiri.
3. **Vendor & mirror registry.** Jangan pull langsung dari registry publik saat build produksi. Mirror internal melindungi Anda dari registry takeover dan package yang dihapus mendadak.
4. **Dependabot/Renovate aktif.** Auto-merge hanya untuk patch, update besar tetap review manual.
5. **Reference image by digest, bukan tag.** Tag `:latest` bisa diubah diam-diam oleh penyerang yang menguasai akun registry. Digest SHA-256 bersifat immutable.
6. **Verifikasi di admission controller.** Signature yang baik tapi tidak pernah diverifikasi sebelum deploy tidak melindungi apa pun. Kyverno atau admission controller Cilium bisa menolak image tanpa attestation SLSA yang valid.
7. **Hasilkan SBOM setiap build.** Simpan sebagai artefak CI, indeks ke dalam database internal, dan hubungkan dengan pipeline VEX.

Contoh kebijakan Kyverno yang menolak image tanpa provenance terverifikasi:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-slsa-provenance
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-provenance
      match:
        any:
          - resources:
              kinds: [Pod]
      verifyImages:
        - imageReferences: ["ghcr.io/org/*"]
          attestations:
            - type: https://slsa.dev/provenance/v1
              conditions:
                - all:
                    - key: "{{ builder.id }}"
                      operator: Equals
                      value: "https://github.com/org/app/"
```

## Tantangan Baru 2026

**AI-generated code** membawa dimensi baru: model AI bisa menyarankan package *lookalike* berbahaya. Package *squatting* yang meniru nama library populer dengan variasi tipografis halus (`lodash` vs `1odash`) meningkat tajam. Solusinya: verifikasi **source dan publisher identity**, bukan hanya nama package.

Bahayanya lebih dalam dari sekadar typo. Model bahasa cenderung menyarankan paket yang sering muncul di data latihnya, yang kebetulan juga target favorit penyerang karena nama itu punya reputasi. Kombinasi "sering direkomendasikan AI" dan "sudah disquat penyerang" adalah resep injeksi dependency otomatis.

Respons teknisnya:

- **Blok dependency baru secara default.** Pull request yang menambah dependency baru butuh review eksplisit, sedangkan bump versi tidak.
- **Verifikasi ownership, bukan nama.** Cek apakah repository package memang dikelola organisasi yang Anda duga, lewat metadata registry dan history commit.
- **Waspadai kombinasi sinyal mencurigakan.** Paket dengan versi sangat baru, jumlah download rendah, tapi nama identik dengan paket besar, adalah pola klasik.
- **Wajibkan provenance untuk dependency internal.** Untuk paket yang Anda produksi sendiri, terima hanya yang punya attestation SLSA valid.

Satu lagi: **lockfile hash mismatch** yang tidak bisa dijelaskan adalah alarm, bukan gangguan. Bila hash di lockfile tidak cocok meski Anda tidak mengubah apa pun, perlakukan sebagai insiden potensial sampai terbukti sebaliknya.

## Kesimpulan

Supply chain security di 2026 bergerak dari *best practice* menjadi **kewajiban regulasi dan tuntutan pasar**. Dengan **SBOM** untuk visibilitas, **SLSA** sebagai roadmap keamanan build, dan **Sigstore** untuk integritas artefak, tim bisa membangun fondasi yang tahan serangan.

Tiga pilar itu saling melengkapi dan tidak ada yang cukup sendiri. SBOM memberi tahu Anda apa yang ada di dalam artefak, tapi tidak membuktikan artefaknya asli. SLSA mendefinisikan seberapa terpercaya proses build-nya, tapi tidak menyediakan mekanisme verifikasi. Sigstore menyediakan mekanisme kriptografis untuk membuktikan identitas dan integritas, tapi tanpa SBOM Anda tidak tahu apa yang Anda buktikan.

Kalau perlu urutan prioritas untuk tim yang mulai dari nol, urutannya begini: generate SBOM setiap build lebih dulu karena murah dan langsung berguna, aktifkan keyless signing dengan OIDC di satu workflow berikutnya, baru tambahkan verifikasi di admission controller sebagai penutup rantai. Semakin cepat dimulai, semakin murah.

---
*Ditulis untuk blog pribadi - Ringga Septia Pribadi*
