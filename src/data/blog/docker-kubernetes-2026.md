---
title: "Docker & Kubernetes 2026: Best Practice untuk Developer Indonesia"
description: "Panduan praktis containerization dan orchestration — dari Docker Compose hingga production-grade Kubernetes cluster untuk startup dan enterprise."
date: "2026-06-25"
author: "Ringga Septia Pribadi"
tags: ["Docker", "Kubernetes", "DevOps", "Cloud"]
category: "Cloud & Infrastructure"
image: "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=800&q=80"
---

## Pendahuluan

Containerization telah menjadi standar industri di tahun 2026. Docker dan Kubernetes tidak lagi opsional; mereka adalah fondasi infrastruktur modern. Container memecahkan masalah "works on my machine" dengan membungkus aplikasi beserta dependency-nya ke dalam satu artefak yang identik di laptop developer maupun di produksi. Kubernetes kemudian menyelesaikan masalah berikutnya: bagaimana menjalankan puluhan sampai ribuan container tersebut secara andal, dengan scheduling, health checking, scaling, dan rollout otomatis.

Artikel ini membahas praktik yang benar-benar dipakai di produksi: cara menulis Dockerfile yang menghasilkan image kecil dan aman, cara memakai Compose untuk development tanpa menyiksa laptop, dan pola dasar deployment di Kubernetes termasuk fitur-fitur terbaru yang sudah stabil.

## Dockerfile Multi-Stage Optimal

Multi-stage build memisahkan lingkungan build dari lingkungan runtime. Stage builder memuat seluruh toolchain, sedangkan stage final hanya berisi binary dan file yang dibutuhkan aplikasi untuk berjalan.

```dockerfile
# Stage 1: Build
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o main .

# Stage 2: Runtime minimal
FROM gcr.io/distroless/base-debian12:nonroot
COPY --from=builder /app/main /main
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/main"]
```

Beberapa hal yang membuat Dockerfile di atas efektif:

- **Urutan COPY yang benar.** `go.mod` dan `go.sum` disalin lebih dulu, sehingga layer `go mod download` bisa di-cache Docker dan tidak diulang setiap kali ada perubahan satu baris kode.
- **Flag build.** `-trimpath` menghapus path absolut dari binary sehingga build menjadi reproducible, `-ldflags="-s -w"` membuang symbol table dan debug info.
- **Base image distroless.** Tidak ada shell, tidak ada package manager, sehingga permukaan serangan jauh lebih kecil dibanding image alpine yang tetap membawa busybox.
- **User non-root.** Container yang berjalan sebagai root akan menjadi masalah serius jika ada container escape. Variant `nonroot` sudah menyediakan user dengan UID non-nol.

Perbedaan ukuran antara image `golang:1.23` penuh dengan image distroless yang berisi satu binary biasanya satu sampai dua orde magnitudo. Untuk aplikasi Go sederhana, ukuran akhir umumnya berada di puluhan megabyte atau kurang.

### Optimasi Lanjutan

Gunakan `.dockerignore` supaya direktori lokal yang tidak perlu tidak ikut terkirim ke build context:

```
.git
node_modules
dist
.env
*.md
coverage
```

Tanpa file ini, build context bisa membengkak dan invalidasi cache terjadi tanpa alasan. Tambahkan juga BuildKit untuk build paralel dan cache yang lebih baik:

```bash
export DOCKER_BUILDKIT=1
docker build -t app:latest --progress=plain .
```

## Docker Compose untuk Development

Compose tetap cara tercepat untuk menyiapkan lingkungan lokal dengan database, cache, dan message broker tanpa menginstal semuanya langsung ke host.

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=devpass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 10

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]

volumes:
  pgdata:
```

Poin penting di sini adalah `healthcheck` bersama `depends_on.condition: service_healthy`. Tanpa itu, container aplikasi bisa start sebelum Postgres siap menerima koneksi, dan yang terjadi adalah crash loop di detik-detik pertama.

### Compose Watch

Sejak Docker Compose mendukung atribut `develop.watch`, kamu tidak perlu rebuild manual setiap kali menyimpan file.

```yaml
services:
  app:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: ./package.json
```

`sync` menyalin perubahan file ke container yang sedang berjalan, sedangkan `rebuild` hanya dipicu ketika file yang benar-benar mengubah hasil build berubah, misalnya `package.json`. Jalankan dengan `docker compose up --watch`.

## Kubernetes: Konsep yang Wajib Dipahami

Kubernetes bekerja dengan model deklaratif: kamu mendeskripsikan keadaan yang diinginkan di dalam manifest, dan controller plane terus bekerja untuk mendekatkan keadaan nyata ke keadaan tersebut.

Objek inti yang perlu dikuasai:

- **Pod.** Unit terkecil, satu atau beberapa container yang berbagi network namespace dan volume.
- **Deployment.** Mengelola ReplicaSet, menangani rolling update dan rollback untuk aplikasi stateless.
- **StatefulSet.** Untuk aplikasi stateful dengan identitas jaringan dan storage yang stabil, misalnya database.
- **Service.** Abstraksi jaringan dengan label selector, tipe ClusterIP, NodePort, LoadBalancer, atau headless.
- **ConfigMap dan Secret.** Menyimpan konfigurasi dan kredensial di luar image.
- **Ingress atau Gateway API.** Mengatur routing HTTP dari luar cluster ke Service.

### Deployment dengan Probe yang Benar

Banyak kegagalan produksi berasal dari probe yang salah dikonfigurasi, bukan dari kode aplikasinya.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: ghcr.io/ringga-dev/api:v1.4.2
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /livez
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          securityContext:
            runAsNonRoot: true
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
```

Perbedaan readiness dan liveness sering keliru:

- **Readiness probe** menentukan apakah Pod siap menerima traffic. Gagal berarti Pod dikeluarkan dari endpoint Service, tapi tidak direstart.
- **Liveness probe** menentukan apakah aplikasi masih sehat. Gagal berkali-kali berarti container direstart.

Jangan pernah mengarahkan liveness probe ke endpoint yang bergantung pada dependency eksternal. Kalau database sedang down dan pemeriksaan itu ikut gagal, seluruh Pod direstart bersamaan, dan justru memperparah keadaan.

### Resource Requests dan Limits

`requests` dipakai scheduler untuk memutuskan di node mana Pod ditempatkan. `limits` adalah batas keras yang ditegakkan oleh runtime container. Kalau container melewati memory limit, kubelet akan membunuhnya dengan status `OOMKilled`.

Best practice yang aman: set `requests` mendekati konsumsi normal, dan `limits` cukup longgar untuk menampung lonjakan. Untuk CPU, hindari set `limits` terlalu ketat karena akan menyebabkan throttling yang sulit didiagnosis. Kubernetes 1.34 menjadikan Pod-level resources berstatus beta dan aktif secara default, sehingga untuk kasus tertentu kamu bisa mendeklarasikan resource di level Pod alih-alih per container.

### Native Sidecar Containers

Pola sidecar dulu diimplementasikan sebagai container biasa di dalam Pod, yang punya masalah: sidecar ikut direstart saat aplikasi mati, dan urutan start tidak terjamin. Kubernetes menyelesaikan ini dengan native sidecar melalui KEP-753. Sebuah sidecar native adalah entri pada daftar init container dengan kebijakan restart Always, dan fitur ini sudah stabil sejak Kubernetes 1.33.

```yaml
spec:
  initContainers:
    - name: log-shipper
      image: fluent/fluent-bit:2.2
      restartPolicy: Always
  containers:
    - name: app
      image: ghcr.io/ringga-dev/api:v1.4.2
```

Sidecar native dijalankan lebih dulu, tetap hidup selama siklus Pod, dan dimatikan hanya setelah container utama keluar. Ini membuat service mesh proxy dan log collector menjadi jauh lebih stabil.

### Ingress vs Gateway API

Ingress API lama punya keterbatasan ekspresif dan hanya mendukung routing dasar. Gateway API, yang mencapai GA pada versi 1.4, menyediakan model role-oriented: infrastruktur tim mengelola `GatewayClass` dan `Gateway`, sementara tim aplikasi hanya mengelola `HTTPRoute`.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
spec:
  parentRefs:
    - name: main-gateway
  hostnames:
    - "api.ringga.dev"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /v1
      backendRefs:
        - name: api-v1
          port: 8080
```

Pemisahan peran ini mengurangi gesekan antar tim dan menghindari satu manifest raksasa yang harus diedit bersama.

## CI/CD Pipeline

Integrasi Docker dengan CI adalah bagian yang paling sering menentukan kecepatan rilis. Prinsip utamanya: image di-tag dengan commit SHA, bukan `latest`.

```yaml
name: build
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/ringga-dev/app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy
        run: |
          kubectl set image deployment/app \
            app=ghcr.io/ringga-dev/app:${{ github.sha }} \
            -n production
          kubectl rollout status deployment/app -n production --timeout=180s
```

Tag dengan commit SHA membuat setiap deployment bisa dilacak ke commit spesifik, dan rollback menjadi sesederhana menjalankan ulang pipeline pada commit sebelumnya. Atribut `cache-from` dan `cache-to` memanfaatkan cache layer GitHub Actions sehingga build berikutnya tidak mengulang tahap yang tidak berubah.

### Multi-Architecture Build

Kalau kamu menjalankan sebagian workload di server ARM, satu image untuk semua arsitektur menghindari duplication Dockerfile.

```bash
docker buildx create --use --name multi
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/ringga-dev/app:${{ github.sha }} \
  --push .
```

Hasilnya adalah satu tag dengan manifest list di atasnya, dan setiap host otomatis menarik varian yang sesuai dengan arsitekturnya.

## Resource Management untuk VPS

Optimasi resource sangat penting agar biaya tetap terkendali:

- Gunakan image minimal (alpine, distroless)
- Set resource requests dan limits di Kubernetes agar scheduler bisa menempatkan Pod dengan benar
- Monitor dengan Prometheus + Grafana, termasuk container memory usage dan restart count
- Aktifkan cluster autoscaler atau scale deployment secara terjadwal pada jam sibuk
- Gunakan HPA berbasis metrik kustom, bukan hanya CPU, kalau traffic-mu dipengaruhi ukuran queue

Sebelum menambah node, periksa dulu apakah masalahnya memang kapasitas atau kebocoran memori. `kubectl top pod` memberikan gambaran cepat, dan grafik restart count sering lebih informatif daripada angka penggunaan CPU.

## Kesimpulan

Docker + Kubernetes bukan lagi untuk perusahaan besar saja. Developer Indonesia bisa mengadopsi container orchestration untuk berbagai skala proyek, mulai dari satu VPS sampai multi-node cluster. Kuncinya bukan memakai semua fitur yang tersedia, melainkan menguasai fondasinya: image yang kecil dan aman, konfigurasi probe yang benar, resource yang terukur, dan pipeline yang bisa dilacak ke setiap commit.
