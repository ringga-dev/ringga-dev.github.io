---
title: "eBPF: Observabilitas dan Keamanan Kernel di Era Cloud-Native 2026"
description: "Cara eBPF mengubah monitoring, tracing, dan keamanan di Kubernetes tanpa mengubah kode aplikasi."
date: "2026-08-16"
author: "Ringga Septia Pribadi"
tags: ["eBPF", "Cloud Native", "Kubernetes", "Observability", "Cybersecurity"]
category: "Cloud & Infrastructure"
image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop"
---

## Pendahuluan

Di tahun 2026, stack cloud-native makin kompleks: microservice ratusan, sidecar, dan node yang di-spin secara dinamis. Tool monitoring lama (agent berbasis push, log scraping) mulai kewalahan karena **overhead** dan **blind spot** di level kernel. Solusinya? **eBPF** (extended Berkeley Packet Filter).

eBPF memungkinkan kita menjalankan program kecil dan aman *di dalam* kernel Linux — menangkap syscall, event jaringan, dan operasi file secara real-time — tanpa mengubah satu baris pun kode aplikasi. Artikel ini membedah kenapa eBPF jadi tulang punggung observabilitas dan keamanan modern.

## Apa Itu eBPF Sebenarnya?

Bayangkan eBPF sebagai "plugin" untuk kernel. Program eBPF (ditulis dalam C, lalu di-compile ke bytecode) di-attach ke hook tertentu: syscall, kprobe, tracepoint, atau XDP (packet processing). Kernel memverifikasi bytecode tersebut aman (tidak boleh loop tak terbatas, tidak boleh akses memori sembarangan) sebelum dijalankan.

Keunggulan utama dibanding tools lama:

| Aspek | Agen Tradisional | eBPF |
|-------|------------------|------|
| Titik pengukuran | User-space / log | Kernel-space (syscall) |
| Overhead | Tinggi (poll + push) | Sangat rendah (event-driven) |
| Visibilitas jaringan | Terbatas (L7 butuh proxy) | Penuh (L3–L7, tanpa sidecar) |
| Perubahan aplikasi | Sering perlu SDK | Nol (transparan) |

## Tiga Pilar Penggunaan eBPF

**1. Observabilitas & Tracing**
Alat seperti Cilium Hubble dan Pixie memakai eBPF untuk membuat service map otomatis dan distributed tracing — tanpa harus menyuntikkan library ke tiap service. Kita lihat latensi per-request dari kernel, bukan dari log aplikasi yang sering terlambat.

**2. Keamanan (Runtime Threat Detection)**
Tetragon (dari Cilium) mendeteksi anomali seperti proses yang tiba-tiba membuka koneksi keluar ke IP asing, atau binary yang dieksekusi dari `/tmp`. Karena berjalan di kernel, deteksinya hampir mustahil di-bypass oleh attacker yang sudah masuk ke container.

**3. Networking & Load Balancing**
Cilium menggantikan kube-proxy dengan eBPF XDP, menangani jutaan packet per detik dengan latency jauh lebih rendah. Ini krusial untuk cluster berskala besar.

## Contoh: Menangkap Syscall dengan bpftrace

Salah satu cara termudah mencoba eBPF adalah `bpftrace`. Berikut script untuk melihat semua proses yang membuka file:

```bash
# Pantau syscall openat di seluruh sistem
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat {
    printf("%-16s %s\n", comm, str(args->filename));
}'
```

Output-nya langsung menunjukkan proses dan file target secara live — berguna untuk debugging aplikasi yang "file not found" tanpa harus menebak lewat `strace` yang lambat.

## Tantangan yang Perlu Diwaspadai

eBPF bukan silver bullet. Beberapa catatan praktis:

- **Versi kernel**: eBPF butuh kernel Linux 4.9+ (idealnya 5.x ke atas). Di Windows atau macOS butuh WSL2/virtual machine.
- **Skill tim**: Menulis program eBPF membutuhkan pemahaman kernel C dan toolchain (clang, libbpf). Untungnya tooling tinggi seperti Cilium sudah menyiapkan semua.
- **Supply chain**: Pastikan image eBPF agent diverifikasi checksum-nya — kode berjalan di kernel, jadi kompromi = akses penuh node.

## Kesimpulan

eBPF adalah infrastruktur tak terlihat di balik observabilitas dan keamanan cloud-native 2026. Dengan kemampuan menangkap event di level kernel secara transparan dan berbiaya rendah, ia menggeser alat lama yang berbasis agent berat. Untuk tim DevOps dan Security, mulai mencoba Cilium atau Tetragon di cluster staging adalah investasi yang sangat sepadan tahun ini.
