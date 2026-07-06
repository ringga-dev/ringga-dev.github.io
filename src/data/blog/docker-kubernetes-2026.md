---
title: "Docker & Kubernetes 2026: Best Practice untuk Developer Indonesia"
description: "Panduan praktis containerization dan orchestration — dari Docker Compose hingga production-grade Kubernetes cluster untuk startup dan enterprise."
date: "2026-06-25"
author: "Ringga Septia Pribadi"
tags: ["Docker", "Kubernetes", "DevOps", "Cloud"]
category: "Cloud & Infrastructure"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?q=80&w=2070&auto=format&fit=crop"
---

## Pendahuluan

Containerization telah menjadi standar industri di tahun 2026. Docker dan Kubernetes tidak lagi opsional — mereka adalah fondasi infrastruktur modern.

## Dockerfile Multi-Stage Optimal

```dockerfile
# Stage 1: Build
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Stage 2: Runtime minimal
FROM gcr.io/distroless/base-debian12:nonroot
COPY --from=builder /app/main /main
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/main"]
```

**Hasil**: Image size dari 1.2GB → 12MB!

## Docker Compose untuk Development

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
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
```

## Best Practice untuk Developer Indonesia

### Resource Management
VPS di Indonesia memiliki harga kompetitif. Optimasi resource sangat penting:
- Gunakan image minimal (alpine, distroless)
- Set resource requests & limits di Kubernetes
- Monitor dengan Prometheus + Grafana

### CI/CD Pipeline
```yaml
- name: Build & Push
  run: |
    docker build -t ghcr.io/ringga-dev/app:${{ github.sha }} .
    docker push ghcr.io/ringga-dev/app:${{ github.sha }}

- name: Deploy
  run: |
    kubectl set image deployment/app \
      app=ghcr.io/ringga-dev/app:${{ github.sha }}
```

## Kesimpulan

Docker + Kubernetes bukan lagi untuk perusahaan besar saja. Developer Indonesia bisa mengadopsi container orchestration untuk berbagai skala proyek.
