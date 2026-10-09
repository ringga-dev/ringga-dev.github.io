---
title: "Teknik Web Security Reconnaissance untuk Bug Hunter 2026"
description: "Panduan lengkap web security reconnaissance — dari passive reconnaissance, subdomain enumeration, technology fingerprinting, hingga automated scanning tools terbaru."
date: "2026-06-28"
author: "Ringga Septia Pribadi"
tags: ["Security", "Bug Bounty", "Recon", "Penetration Testing"]
category: "Cybersecurity"
image: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80"
---

## Pendahuluan

Web security reconnaissance adalah fase paling krusial dalam bug hunting dan penetration testing. Di tahun 2026, tools dan teknik terus berevolusi seiring kompleksitas aplikasi web modern. Fase ini menentukan seberapa luas permukaan serangan yang berhasil kamu petakan. Sebuah subdomain yang terlupakan, sebuah endpoint API lama yang masih merespons, atau sebuah parameter yang tidak divalidasi bisa menjadi satu-satunya jalan masuk ke seluruh sistem.

Aturan praktisnya sederhana: semakin banyak aset valid yang ditemukan, semakin besar peluang menemukan bug. Tetapi recon yang tidak terkendali juga berisiko. Request berlebihan ke target bisa memicu rate limit, WAF, atau bahkan dianggap keluar dari rules of engagement program bug bounty. Artikel ini membedah pipeline recon dari tahap pasif sampai aktif, lengkap dengan perintah yang bisa langsung dicoba pada scope yang kamu miliki izinnya.

## Memetakan Permukaan Serangan

Permukaan serangan sebuah organisasi tidak lagi hanya satu domain utama. Ia tersebar ke subdomain, API gateway, environment staging, bucket object storage, CDN, dan aplikasi pihak ketiga yang terintegrasi. Pendekatan yang efektif adalah membangun inventory dulu, baru menyaringnya.

Alur kerja yang umum dipakai:

1. Kumpulkan kandidat host dari sumber pasif.
2. Resolusi DNS untuk memastikan host tersebut benar-benar ada.
3. Probe HTTP untuk melihat host mana yang hidup dan melayani konten.
4. Fingerprint teknologi pada setiap host yang hidup.
5. Crawl dan kumpulkan endpoint, lalu simpan sebagai target tahap pengujian.

Tahap 1 sampai 4 bisa sepenuhnya pasif. Tahap 5 mulai menyentuh infrastruktur target, jadi pastikan kamu sudah membaca scope program, rate limit yang ditetapkan, dan daftar aset yang dilarang disentuh.

## Passive Reconnaissance

Passive recon berarti mengumpulkan informasi tanpa mengirim request langsung ke infrastruktur target. Datanya datang dari pihak ketiga: certificate transparency logs, passive DNS, search engine, dan arsip web. Karena tidak ada paket yang mengalir ke server target, fase ini hampir selalu aman dari sisi teknis, dan umumnya diperbolehkan oleh program bug bounty.

### Certificate Transparency Logs

Setiap sertifikat TLS yang diterbitkan oleh Certificate Authority publik dicatat ke public CT log sebelum dipercaya browser. Log ini permanen, bisa dicari, dan memuat seluruh Subject Alternative Name (SAN) yang terdaftar pada sertifikat. Karena itu satu query bisa mengungkap banyak subdomain sekaligus.

```bash
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u
```

Flag `-r` pada `jq` membuat output berupa string mentah tanpa tanda kutip JSON. Pembersihan `*.` diperlukan karena sertifikat wildcard menyimpan entri seperti `*.target.com`, yang bukan host yang bisa langsung diresolusi.

Beberapa catatan praktis: endpoint JSON crt.sh bisa lambat pada domain yang sangat besar, dan sertifikat yang sudah expired tetap muncul di hasil. Jadi outputnya perlu diverifikasi, jangan langsung dianggap aset aktif.

### DNS Enumeration dan Passive DNS

Subfinder melakukan enumerasi pasif dengan menggabungkan banyak sumber sekaligus. Flag `-all` mengaktifkan seluruh sumber, bukan hanya default set.

```bash
subfinder -d target.com -all -recursive -silent
```

Flag `-recursive` membuat subfinder ikut mengecek subdomain dari subdomain yang sudah ditemukan, sehingga host bertingkat seperti `dev.internal.target.com` tidak terlewat. Untuk banyak domain sekaligus gunakan `-dL domains.txt`.

OWASP Amass membangun relasi graf antara domain, ASN, dan netblock, sehingga bisa menemukan host yang tidak terlihat oleh pencarian subdomain biasa.

```bash
amass enum -passive -d target.com -o amass-passive.txt
amass intel -org "Nama Perusahaan"
```

Perlu diingat bahwa kedua tool baru memakai daftar sumbernya secara penuh setelah API key dikonfigurasi. Subfinder membaca `~/.config/subfinder/provider-config.yaml`. Tanpa key, beberapa sumber dilewati diam-diam dan hasil enumerasi terlihat lebih sedikit dari yang seharusnya.

Passive DNS berguna untuk menemukan host yang sudah tidak dipublikasikan, misalnya subdomain yang dulu menunjuk ke sebuah IP internal dan sekarang hilang dari halaman utama, tapi masih tercatat pada pencatatan DNS historis.

### Technology Fingerprinting

Fingerprinting menentukan apa yang berjalan di balik setiap host, dan hasilnya menentukan teknik pengujian apa yang relevan. Aplikasi yang berjalan di belakang CDN akan diperlakukan berbeda dengan aplikasi yang terekspos langsung.

```bash
wappalyzer https://target.com
whatweb -a 1 https://target.com
```

`whatweb` dengan level agresivitas 1 mengurangi jumlah request yang dikirim. Untuk probing massal, httpx lebih tepat karena menerima input dari stdin:

```bash
cat hosts.txt | httpx -status-code -title -tech-detect -web-server -mc 200 -o live.txt
```

Flag `-mc 200` menyaring hanya host yang merespons 200, sedangkan `-tech-detect` mengisi kolom teknologi berdasarkan deteksi ala wappalyzer. Output JSON lewat `-json` lebih mudah diparser di pipeline lanjutan.

### Mengumpulkan URL dari Arsip

Sebelum menyentuh target, kamu bisa mengambil daftar URL yang sudah terindeks pihak ketiga. Tool `gau` (getallurls) menarik URL dari Wayback Machine, Common Crawl, AlienVault OTX, dan urlscan.

```bash
gau --subs target.com | sort -u > urls.txt
gau target.com --providers wayback,commoncrawl
```

Hasilnya sangat berguna untuk menemukan parameter query yang sudah tidak terpakai, file backup, atau endpoint versi lama. Saring dengan pola ekstensi supaya tidak menghabiskan waktu pada aset statis:

```bash
cat urls.txt | grep -E '\.(php|asp|aspx|jsp|json|action|do)(\?|$)' | sort -u
```

## Active Reconnaissance

Setelah inventory host dan URL terkumpul, tahap aktif dimulai. Di sini request mengalir ke target, jadi pacing dan rate limit wajib diperhatikan.

### Crawling dengan Katana

Katana adalah crawler dari ProjectDiscovery yang bisa mengekstrak endpoint dari HTML maupun JavaScript.

```bash
katana -u https://target.com -d 3 -jc -jsl -kf robotstxt,sitemapxml -o endpoints.txt
```

Penjelasan flag: `-d 3` membatasi kedalaman crawl sampai 3 level, `-jc` mengaktifkan parsing endpoint dari file JavaScript, `-jsl` memakai jsluice untuk ekstraksi yang lebih dalam tapi lebih borus memori, dan `-kf` menyertakan file standar seperti robots.txt dan sitemap.xml. Untuk target besar, batasi waktu dengan `-ct 120` (dalam detik).

### Directory dan Content Discovery

Bruteforce direktori tetap efektif untuk menemukan path yang tidak terlink dari mana pun.

```bash
ffuf -u https://target.com/FUZZ \
  -w directory-list-2.3-medium.txt \
  -fc 404,403 -t 50 -rate 100
```

Flag `-ac` mengaktifkan autocalibration, yaitu ffuf menyaring sendiri respons baseline sehingga kamu tidak perlu menentukan `-fs` manual:

```bash
ffuf -u https://target.com/FUZZ -w wordlist.txt -ac -mc all
```

Gunakan `-rate` untuk membatasi request per detik. Ini penting supaya scan tidak memicu proteksi anti-abuse di sisi target.

### Parameter Fuzzing

Parameter tersembunyi sering jadi sumber bug serius karena jarang divalidasi.

```bash
ffuf -u 'https://target.com/api/v1/users?FUZZ=test' \
  -w params.txt -fc 400 -fs 0
```

Kombinasikan dengan hasil `gau` untuk mendapatkan daftar parameter yang memang pernah ada di aplikasi, bukan tebakan buta:

```bash
cat urls.txt | unfurl keys | sort -u > params.txt
```

### CORS dan Header Misconfiguration

CORS yang salah konfigurasi bisa membuat aplikasi menerima request lintas origin dari domain penyerang. Yang perlu diperiksa adalah apakah server memantulkan nilai `Origin` tanpa validasi allowlist.

```bash
curl -sI "https://api.target.com/" \
  -H "Origin: https://evil.com" | grep -i "access-control"
```

Pola rentan yang umum:

- `Access-Control-Allow-Origin: https://evil.com` (memantulkan origin apa pun)
- `Access-Control-Allow-Origin: null` yang diterima dari sandbox iframe
- `Access-Control-Allow-Credentials: true` bersama origin yang dipantulkan

Ketiga kondisi sekaligus berarti kredensial pengguna bisa dibaca oleh domain lain. Periksa juga header keamanan lain seperti `Strict-Transport-Security`, `Content-Security-Policy`, dan `X-Frame-Options` untuk mendeteksi clickjacking dan downgrade attack.

## Vulnerability Scanning dengan Nuclei

Nuclei adalah scanner berbasis template YAML. Setiap template mendefinisikan request dan matcher yang menentukan apakah sebuah temuan valid, sehingga false positive bisa ditekan ke tingkat rendah.

```bash
nuclei -l live.txt -t cves/ -t exposures/ -severity critical,high -o findings.txt
```

Contoh template sederhana untuk memahami strukturnya:

```yaml
id: exposed-env-file

info:
  name: Exposed .env File
  author: ringga
  severity: high
  tags: exposure,config

http:
  - method: GET
    path:
      - "{{BaseURL}}/.env"

    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200

      - type: word
        words:
          - "DB_PASSWORD="
          - "APP_KEY="
```

Template custom simpan di direktori sendiri dan panggil dengan `-t ./my-templates/`. Untuk program bug bounty, batasi throughput agar tidak dianggap sebagai denial of service:

```bash
nuclei -l live.txt -t http/misconfiguration/ -rl 150 -c 25 -stats
```

`-rl` membatasi request per detik, `-c` membatasi jumlah template yang berjalan paralel, dan `-stats` menampilkan progres beserta statistik temuan secara berkala.

## Pipeline Automation

Gabungan tool ProjectDiscovery dirancang untuk saling mengirim output lewat pipe. Satu baris bisa mengubah satu domain menjadi daftar temuan.

```bash
subfinder -d target.com -all -silent \
  | httpx -status-code -title -tech-detect -silent \
  | nuclei -t cves/ -severity critical,high -o vulns.txt
```

Untuk pipeline yang lebih rapi, pakai script dengan penanganan error dan direktori kerja per target:

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="$1"
OUT="recon/$TARGET"
mkdir -p "$OUT"

subfinder -d "$TARGET" -all -silent | sort -u > "$OUT/subs.txt"
httpx -l "$OUT/subs.txt" -silent -json -o "$OUT/live.json"
jq -r 'select(.status_code==200) | .url' "$OUT/live.json" > "$OUT/live.txt"
gau --subs "$TARGET" | sort -u > "$OUT/urls.txt"
katana -u "https://$TARGET" -silent -d 2 | sort -u >> "$OUT/urls.txt"
nuclei -l "$OUT/live.txt" -t cves/ -rl 100 -o "$OUT/nuclei.txt"

echo "[+] Selesai: $OUT"
```

Simpan hasil per target supaya bisa dijalankan ulang tanpa mengulang query mahal, dan supaya mudah dibandingkan antar waktu untuk mendeteksi aset baru.

## Common Pitfalls

Beberapa kesalahan yang sering membuat recon tidak menghasilkan apa-apa:

- **Tidak mengonfigurasi API key.** Subfinder dan Amass hanya memakai sumber penuh setelah key diisi.
- **Langsung scan tanpa verifikasi.** Host hasil CT log bisa sudah mati, sehingga waktu terbuang untuk probe yang gagal semua.
- **Mengabaikan JavaScript.** Sebagian endpoint API modern hanya ada di dalam bundle JS, bukan di HTML.
- **Rate limit diabaikan.** Akun program bug bounty bisa ditangguhkan karena traffic berlebihan.
- **Tidak menyaring duplikat.** Tanpa `sort -u`, daftar host membengkak dan waktu scan membesar.

## Scope dan Etika

Semua teknik di atas hanya boleh dijalankan pada aset yang tercantum dalam scope program. Periksa juga hal berikut sebelum memulai: daftar wildcard domain yang diizinkan, apakah automated scanning diizinkan, batas request per menit, dan apakah subdomain pihak ketiga (seperti helpdesk terkelola vendor) dikecualikan.

Sebagian program mewajibkan akun User-Agent khusus pada header request. Nuclei mendukungnya lewat `-H 'User-Agent: ...'`, dan httpx lewat `-H` juga. Mencantumkan identitas dengan benar biasanya membuat tim keamanan lebih mudah membedakan aktivitas riset dari serangan sungguhan.

## Kesimpulan

Recon adalah kunci sukses bug hunting. Kombinasi passive + active reconnaissance dengan pipeline automation akan mengungkap permukaan serangan yang lebih luas. Bangun inventory yang konsisten, verifikasi sebelum menyerang lapisan berikutnya, dan jaga pacing supaya pekerjaanmu tetap di dalam aturan program. Tooling-nya sudah matang; pembedanya ada pada disiplin proses dan kedalaman analisis terhadap data yang berhasil dikumpulkan.
