---
title: "Teknik Web Security Reconnaissance untuk Bug Hunter 2026"
description: "Panduan lengkap web security reconnaissance — dari passive reconnaissance, subdomain enumeration, technology fingerprinting, hingga automated scanning tools terbaru."
date: "2026-06-28"
author: "Ringga Septia Pribadi"
tags: ["Security", "Bug Bounty", "Recon", "Penetration Testing"]
category: "Cybersecurity"
image: "https://images.unsplash.com/photo-1563013544-824ae1b704d3?q=80&w=2070&auto=format&fit=crop"
---

## Pendahuluan

Web security reconnaissance adalah fase paling krusial dalam bug hunting dan penetration testing. Di tahun 2026, tools dan teknik terus berevolusi seiring kompleksitas aplikasi web modern.

## Passive Reconnaissance

### Certificate Transparency Logs
```bash
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq '.[].name_value' | sort -u
```

### DNS Enumeration
```bash
subfinder -d target.com -all -silent
amass enum -passive -d target.com
```

### Technology Fingerprinting
```bash
wappalyzer https://target.com
whatweb https://target.com
```

## Active Reconnaissance

### Directory Bruteforce
```bash
ffuf -u https://target.com/FUZZ \
  -w directory-list-2.3-medium.txt \
  -fc 404,403 -t 100
```

### Parameter Fuzzing
```bash
ffuf -u 'https://target.com/api/v1/users?FUZZ=test' \
  -w params.txt -fc 400
```

### CORS Testing
```bash
curl -sI "https://api.target.com/" \
  -H "Origin: https://evil.com" | grep -i "access-control"
```

## Tools Wajib 2026

| Tool | Fungsi |
|------|--------|
| Subfinder | Passive subdomain enum |
| ffuf | Fast web fuzzer |
| nuclei | Vulnerability scanner |
| httpx | HTTP probe + technology detect |
| katana | Web crawler |
| gau/waybackurl | Archive URL gathering |

## Pipeline Automation

```bash
subfinder -d target.com | httpx | nuclei -t cves/ -o vulns.txt
```

## Kesimpulan

Recon adalah kunci sukses bug hunting. Kombinasi passive + active reconnaissance dengan pipeline automation akan mengungkap permukaan serangan yang lebih luas.
