---
title: "Self-Hosting AI Infrastructure di ARM: Panduan Lengkap 2026"
description: "Panduan lengkap membangun infrastruktur AI self-hosted di perangkat ARM — dari AI Gateway, coding assistant, hingga automation dengan OmniRouter dan Hermes Agent."
date: "2026-07-11"
author: "Ringga Septia Pribadi"
tags: ["AI", "Self-Hosted", "ARM", "DevOps", "Docker", "Infrastructure"]
category: "Technology"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=2068&auto=format&fit=crop"
reading_time: "12 min read"
---

## Pendahuluan

Di tahun 2026, AI bukan lagi domain eksklusif perusahaan besar dengan GPU cluster raksasa. Dengan perangkat ARM seperti Amlogic, Raspberry Pi 5, atau Orange Pi, kamu bisa membangun **infrastruktur AI self-hosted** yang powerful — hanya dengan SD card 28GB dan SSD eksternal.

Artikel ini adalah panduan lengkap dari pengalaman nyata membangun AI infrastructure di atas Armbian (Amlogic SBC) dengan **$0 biaya operasional** untuk 90+ AI model gratis.

## Arsitektur Infrastruktur AI Self-Hosted

```
┌─────────────────────────────────────────────────────────┐
│                   ARM Single Board Computer              │
│                      (Amlogic SBC)                       │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────────────────────┐  │
│  │   Casa OS    │  │         Hermes Agent            │  │
│  │  (Dashboard) │  │  (AI Agent Framework)           │  │
│  └──────────────┘  └─────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐   │
│  │          OmniRouter (AI Gateway)                 │   │
│  │  port 20129 — 237 AI Providers — 90+ Free       │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Docker Containers (PostgreSQL, etc)      │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Storage: SD Card (28GB) → SSD (/mnt/ssd, 220GB free) │
└─────────────────────────────────────────────────────────┘
```

## Komponen Utama

### 1. Sistem Operasi: Armbian

Armbian adalah distribusi Debian-optimized untuk ARM SBC. Kelebihannya:

- Kernel terbaru (6.12.x Ophub)
- Support hardware acceleration
- Community aktif untuk Amlogic, Rockchip, Allwinner
- Package management via apt

```bash
# Cek versi
uname -a
# Linux 6.12.68-ophub aarch64 GNU/Linux

# Cek resource
free -h
# total        used        free
# RAM: 1.8Gi   1.2Gi      600Mi
# Swap: 4.9Gi  200Mi      4.7Gi

df -h /
# Filesystem      Size  Used Avail Use%
# /dev/mmcblk2p2  29G   15G   14G  51%
```

### 2. AI Gateway: OmniRouter

OmniRouter adalah **open-source AI gateway** yang menggabungkan 237 provider AI dalam satu endpoint. Ini adalah otak dari infrastruktur AI self-hosted.

**Fitur Utama:**
- ✅ 90+ free AI providers
- ✅ 17 routing strategies
- ✅ Auto-fallback antar provider
- ✅ 15-95% token savings via Caveman Compression
- ✅ Dashboard web untuk management

```bash
# Deploy via Docker
docker run -d \
  --name omniroute \
  -p 20129:20128 \
  -v /mnt/ssd/omniroute-data:/app/data \
  diegosouzapw/omniroute:latest
```

### 3. AI Agent Framework: Hermes Agent

Hermes Agent adalah **open-source AI agent** yang bisa berjalan di CLI, Telegram, Discord, dan platform lainnya. Dengan Hermes, kamu bisa:

- Mengotomatiskan tugas coding, research, dan reporting
- Menjadwalkan cron job untuk laporan harian
- Mengakses tools system (terminal, file, web)
- Berkomunikasi via Telegram dari mana saja

```bash
# Install
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Konfigurasi model
hermes config set model.provider custom:OmniRouter
hermes config set model.base_url http://localhost:20129/v1
```

### 4. Storage Strategy: SD Card + SSD

Keterbatasan SD Card (28GB) adalah tantangan utama di ARM SBC. Solusinya:

```bash
# 1. Redirect Docker ke SSD
sudo mkdir -p /mnt/ssd/docker
cat > /etc/docker/daemon.json << 'EOF'
{ "data-root": "/mnt/ssd/docker" }
EOF

# 2. Redirect cache ke SSD
ln -sf /mnt/ssd/cache/xdg-cache ~/.cache
ln -sf /mnt/ssd/cache/npm ~/.npm

# 3. Environment variables di ~/.profile
export XDG_CACHE_HOME=/mnt/ssd/cache/xdg-cache
export NPM_CONFIG_CACHE=/mnt/ssd/cache/npm
export PIP_CACHE_DIR=/mnt/ssd/cache/pip
```

## Setup Step-by-Step

### Langkah 1: Persiapan Sistem

```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y curl git docker.io docker-compose

# Enable Docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### Langkah 2: Deploy OmniRouter

```bash
# Buat direktori data
sudo mkdir -p /mnt/ssd/omniroute-data
sudo chown -R $USER:$USER /mnt/ssd/omniroute-data

# Generate JWT Secret
JWT_SECRET=$(openssl rand -hex 64)
API_KEY_SECRET=$(openssl rand -hex 32)

# Deploy container
docker run -d \
  --name omniroute \
  --restart unless-stopped \
  -p 20129:20128 \
  -e JWT_SECRET=$JWT_SECRET \
  -e API_KEY_SECRET=$API_KEY_SECRET \
  -v /mnt/ssd/omniroute-data:/app/data \
  diegosouzapw/omniroute:latest

# Verifikasi
curl http://localhost:20129/v1/models | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']), 'models available')"
```

### Langkah 3: Konfigurasi Hermes Agent

```bash
# Install Hermes
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Set provider OmniRouter
hermes config set model.default auto
hermes config set model.provider custom:OmniRouter
hermes config set model.base_url http://100.72.114.31:20129/v1
hermes config set model.api_key sk-your-key-here

# Aktifkan Telegram gateway
hermes gateway setup
```

### Langkah 4: Optimasi Tools

Hermes punya banyak tools yang bisa diaktifkan per platform:

```yaml
# ~/.hermes/config.yaml
platform_toolsets:
  cli:
    - terminal
    - file
    - web
    - browser
    - code_execution
    - delegation
    - cronjob
    - memory
  telegram:
    - terminal
    - file
    - web
    - cronjob
    - delegation
```

## Model Free Terbaik untuk Coding

Dari 90+ free providers, ini 5 model **terbaik untuk coding** yang support tool_calling:

| Model | Provider | Context | Kelebihan |
|-------|----------|---------|-----------|
| `qwen/qwen3-coder:free` | OpenRouter | 1M | Coding specialist, context besar |
| `openrouter/openai/gpt-oss-120b:free` | OpenAI | 128K | Multi-purpose, stabil |
| `openrouter/meta-llama/llama-3.3-70b-instruct:free` | Meta | 128K | Reasoning kuat |
| `openrouter/google/gemma-4-31b-it:free` | Google | 262K | Vision + coding |
| `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | Nvidia | 1M | Context 1M, kuat |

### Cara Testing Model Baru

```bash
# Test via curl
curl http://localhost:20129/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen3-coder:free",
    "messages": [
      {"role": "user", "content": "Write a hello world in Python"}
    ],
    "max_tokens": 100
  }'
```

## Automation: Cron Job untuk Laporan Otomatis

Salah satu kekuatan self-hosted AI adalah **automation**. Contoh: laporan saham otomatis setiap hari.

```bash
# Setup cron job di Hermes
hermes cron create "0 16 * * 1-5" \
  --name "daily-stock-report" \
  --prompt "Generate closing stock report PDF..." \
  --deliver "telegram:-1003994290708:394"
```

Fitur cron job Hermes:
- ✅ Support 5-field cron syntax
- ✅ One-shot atau recurring
- ✅ Multi-platform delivery
- ✅ Script hooks untuk data collection
- ✅ Per-job model/provide override

## Tips Optimasi untuk ARM SBC

### 1. Manajemen RAM (1.8GB)

```bash
# Aktifkan swap lebih besar
sudo fallocate -l 8G /mnt/ssd/swapfile
sudo mkswap /mnt/ssd/swapfile
sudo swapon /mnt/ssd/swapfile

# Batasi memory Docker container
docker run -d --memory="512m" --memory-swap="1g" ...
```

### 2. Manajemen Storage

```bash
# Bersihkan cache Docker secara berkala
docker system prune -af --volumes

# Redirect apt cache ke SSD
sudo mount --bind /mnt/ssd/apt-archives /var/cache/apt/archives

# Hapus package manager cache
sudo apt clean
```

### 3. Network Optimization

Untuk akses dari luar rumah, gunakan **Tailscale**:

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Cek IP Tailscale
tailscale ip -4
# 100.x.x.x
```

Dengan Tailscale, semua service bisa diakses dari mana saja via IP Tailscale — tanpa port forwarding, tanpa DDNS.

## Monitoring

Cek kesehatan infrastruktur secara berkala:

```bash
#!/bin/bash
# health-check.sh

echo "=== System ==="
echo "Uptime: $(uptime -p)"
echo "RAM: $(free -h | grep Mem | awk '{print $3"/"$2}')"
echo "SD: $(df -h / | tail -1 | awk '{print $3"/"$2 " ("$5")"}')"
echo "SSD: $(df -h /mnt/ssd | tail -1 | awk '{print $3"/"$2 " ("$5")"}')"

echo "=== Docker ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo "=== OmniRouter ==="
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:20129/v1/models

echo "=== Hermes ==="
hermes status 2>/dev/null || echo "hermes-cli not running"
```

## Kesimpulan

Self-hosting AI infrastructure di ARM SBC di tahun 2026 bukan hanya mungkin — tapi **sangat powerful** dan **gratis**. Dengan kombinasi:

1. 🖥️ **Armbian** sebagai OS yang stabil
2. 🌐 **OmniRouter** sebagai AI Gateway (237 providers)
3. 🤖 **Hermes Agent** untuk automation
4. 💾 **SSD** sebagai storage utama
5. 🏠 **Tailscale** untuk akses remote

Kamu punya infrastruktur AI pribadi yang bisa diakses dari mana saja, kapan saja — tanpa bergantung layanan cloud berbayar.

**Biaya operasional: $0/bulan** (hanya listrik untuk ARM SBC ~5W).

Mulai hari ini dan bangun AI infrastructure-mu sendiri! 🚀
