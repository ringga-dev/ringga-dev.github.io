---
title: "eBPF Runtime Security & Observability 2026: Wajah Baru Proteksi Kernel"
description: "eBPF melampaui observabilitas — kini jadi lapisan keamanan runtime yang menjaga kernel tanpa agent berat."
date: "2026-09-07"
author: "Ringga Septia Pribadi"
tags: ["eBPF", "Security", "Cloud", "Observability", "Linux"]
category: "Cloud & Infrastructure"
image: "https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=800&q=80"
---

## Awal Mula: Dari Observabilitas ke Keamanan

eBPF (extended Berkeley Packet Filter) memasuki tahun 2026 sebagai salah satu teknologi paling berdampak di ekosistem Linux. Awalnya dirancang untuk packet filtering dan observability, kini eBPF menjadi tulang punggung runtime security — memberi visibilitas penuh ke kernel tanpa perlu mengubah kode aplikasi atau menginstal agent yang berat.

Pada 2025–2026, adopsi eBPF dalam produk keamanan meledak. Platform seperti CrowdStrike, Datadog, dan Azure Defender luas mana menggunakan eBPF untuk deteksi ancaman level kernel. Cloud-native security startup juga membuild whole stack di atasnya.

## Mengapa eBPF Berbeda dari Agent Tradisional

Agent keamanan tradisional (EDR, host-based IDS) biasanya berjalan sebagai layanan di user space, memonitor log sistem, file access, dan proses. Pendekatan ini punya kelemahan mendasar:

| Aspek | Agent Tradisional | eBPF |
|---|---|---|
| Overhead | Tinggi, interupsi sistem call | Rendah, kernel-side hook |
| Visibilitas | Terbatas ke user-space events | Full kernel & user-space |
| Boot time | Butuh bootstrap | Hooked sejak init |
| evasion resistance | Mudah dimatikan proses | Sulit di-kill dari user space |
| konfigurasi | Install, configure, update | Load program via syscall |

Dengan eBPF, program keamanan bisa me-hook syscall, medication point, dan VM exits tanpa memodifikasi kode kernel atau aplikasi. Program itu dijalankan di sandbox kernel yang aman — verifier memastikan tidak ada infinite loop, pointer abuse, atau akses memori ilegal.

## Konsep Kunci Runtime Security dengan eBPF

### 1. Syscall Monitoring & Anomaly Detection

Semua interaksi antara aplikasi dan kernel melewati syscall. Dengan eBPF, kita bisa:

```c
// Contoh hook execve untuk lacak proses execution
SEC("tracepoint/syscalls/sys_enter_execve")
int trace_execve(struct trace_event_raw_sys_enter *ctx) {
    char comm[16];
    bpf_get_current_comm(&comm, sizeof(comm));
    bpf_printk("Process %s executing command\n", comm);
    return 0;
}
```

Di produksi, program ini dilengkapi dengan policy engine yang mendeteksi pola anomali — misalkan proses web server yang tiba-tiba menjalankan `/bin/sh`, atau child process yang mencoba modify `/etc/passwd`.

### 2. Network Policy Enforcement

eBPF bisa intercept packet di berbagai hook point (XDP, TC, socket filter) dan membuat keputusan allow/deny berdasarkan konten, bukan cuma IP/port. Ini memungkinkan:

- **L7 policy**: blocking HTTP request ke endpoint tertentu tanpa proxy
- **Process-aware network policy**: hanya proses tertentu boleh bind port tertentu
- **Encrypted traffic inspection**: melihat metadata tanpa decrypt (via pattern matching di packet metadata)

### 3. Memory & File Integrity Monitoring

Dengan eBPF, kita bisa monitor write ke file sensitif (SECURE_FILE, config file, key store) dan detect injection attempt di memory region proses. Ini complement dari file integrity monitoring (FIM) tradisional — lebih real-time dan lebih sulit di-bypass.

### 4. Container & Kubernetes Visibility

Di lingkungan Kubernetes, eBPF memberikan visibility tanpa perlu sidecar atau modify pod spec. Tool seperti Cilium mengadopsi eBPF untuk:

- Mengganti kube-proxy (lebih efisien, lebih aman)
- Network policy enforcement di layer yang lebih dalam
- Detect anomalous service-to-service communication
- Visibility ke encrypt traffic via Hubble

## Threat Detection Patterns yang Berjalan di eBPF

Berbagai pola deteksi ancaman yang feasible dijalankan via eBPF:

| Threat Pattern | eBPF Hook Point | Deteksi |
|---|---|---|
| Privilege escalation via exec | `sys_enter_execve` | Process spawn shell dari web server |
| Reverse shell connection | Socket filter / tracepoint | Outbound connection ke IP mencurigakan dari proses tak dikenal |
| Kernel rootkit | LSM hooks (security_*()) | Hook ke security_file_open, security_inode_follow_link |
| Container breakout | Namespace / cgroup monitoring | Process melewati namespace boundary |
| Data exfiltration | Socket write / sendmsg | Large outbound payload ke external IP dari service internal |
| Credential dumping | Memory access monitoring | Akses ke `/proc/<pid>/mem` dari proses external |

## Tantangan & Pitfall

eBPF bukan silver bullet. Ada beberapa tantangan nyata di lapangan:

1. **Kernel version compatibility** — fitur eBPF tertentu hanya tersedia di kernel ≥5.8. Di lingkungan dengan kernel lama, fitur limited.
2. **Verifier strictness** — program eBPF harus lolos verifier yang ketat. Debugging program yang gagal verifikasi bisa rumit.
3. **Performance dalam high-throughput** — walaupun ringan, program eBPF yang terlalu kompleks di setiap packet bisa jadi bottleneck di link dengan throughput sangat tinggi.
4. **Privilege requirement** — loading program eBPF butuh `CAP_BPF` atau root. Di lingkungan multitenant, ini masalah trust.
5. **Auditability** — log eBPF perlu diinstrument dengan baik; tanpa proper logging, event hilang.

## Tools & Ecosystem 2026

| Tool | Fokus | Use Case |
|---|---|---|
| Cilium | Network, k8s | Service mesh, network policy, observability |
| Falco | Runtime security | Anomaly detection via syscall rules |
| Tetragon | Security observability | Process, network, file monitoring + enforcement |
| Pixie | Observability | Application-level tracing tanpa code modifikasi |
| bpftrace | Tracing & debug | One-liner script untuk investigasi ad-hoc |
| Tracee | Runtime security | Signatures-based detection, forensics |

## Arah ke Depan: 2026–2027

Beberapa tren yang terlihat:

- **eBPF + AI/ML**: feeding eBPF telemetry ke model ML untuk deteksi anomaly yang lebih canggih. Datadog dan Elastic sudah mulai integrasi.
- **WASI di eBPF** (WASI-eBPF): memungkinkan program bernavigasi di environment yang lebih terkontrol, potensi untuk multi-language eBPF program.
- **Hardware offload**: NIC vendor mulai explore offloading eBPF program ke hardware (SmartNIC, DPU). Ini masih early stage tapi menjanjikan untuk performance-critical environment.
- **Standardisasi**: Linux kernel community terus meningkatkan stabilitas API eBPF. CO-RE (Compile Once, Run Everywhere) sudah standard, mengurangi masalah portability.

## Batasan yang Perlu Diketahui

eBPF punya batasan nyata yang menentukan apakah
programnya bisa berjalan di produksi.

**Kernel harus menyediakan BTF.**
Program modern memerlukan metadata tipe untuk memverifikasi akses pointer
dengan aman. Tanpa itu, sebagian program ditolak._distribusi lama dan banyak
citra container lama tidak menyediakannya.

**Verifier menolak program yang tidak bisa dibuktikan aman secara statis.**
Ini yang paling sering mengejutkan. Program yang terlihat benar secara
logika bisa ditolak karena loop dengan batas yang tidak dapat dibuktikan.
Mulailah dari program sekecil mungkin lalu tambahkan satu per satu.

**Tracepoint lebih portabel daripada kprobe, tapi tidak selalu tersedia.**
Kprobe bergantung pada simbol kernel dan bisa hilang saat kernel diperbarui.
Tracepoint punya kontrak yang lebih stabil, tetapi tidak semua fungsi punya
tracepoint. Kombinasi keduanya biasanya diperlukan.

**Overhead bukan nol dan tidak selalu dapat diprediksi.**
Program yang dipanggil terlalu sering bisa menimbulkan biaya nyata. Profilkan
sebelum menyimpulkan overhead suatu program rendah, karena frekuensi
peristiwa dan pekerjaan per peristiwa sama-sama berpengaruh.

## Kesimpulan

eBPF di 2026 bukan sekadar observability tool — ini adalah fondasi runtime security di lingkungan cloud-native. Dengan kemampuan hook ke kernel tanpa overhead agent tradisional, eBPF memungkinkan visibilitas yang sebelumnya impossible, deteksi ancaman yang lebih dini, dan enforcement yang lebih granular.

Untuk tim keamanan cloud atau platform engineer, memahami eBPF sekarang adalah investasi yang tepat. Dari kernel tracing sederhana hingga security enforcement yang kompleks, teknologi ini akan semakin become critical infrastructure di tahun-tahun ke depan.
