---
title: "eBPF: Observabilitas dan Keamanan Kernel di Era Cloud-Native 2026"
description: "Cara eBPF mengubah monitoring, tracing, dan keamanan di Kubernetes tanpa mengubah kode aplikasi."
date: "2026-08-16"
author: "Ringga Septia Pribadi"
tags: ["eBPF", "Cloud Native", "Kubernetes", "Observability", "Cybersecurity"]
category: "Cloud & Infrastructure"
image: "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&q=80"
---

## Pendahuluan

Di tahun 2026, stack cloud-native makin kompleks: microservice ratusan, sidecar, dan node yang di-spin secara dinamis. Tool monitoring lama (agent berbasis push, log scraping) mulai kewalahan karena **overhead** dan **blind spot** di level kernel. Solusinya? **eBPF** (extended Berkeley Packet Filter).

eBPF memungkinkan kita menjalankan program kecil dan aman *di dalam* kernel Linux, menangkap syscall, event jaringan, dan operasi file secara real-time, tanpa mengubah satu baris pun kode aplikasi. Artikel ini membedah kenapa eBPF jadi tulang punggung observabilitas dan keamanan modern.

## Apa Itu eBPF Sebenarnya?

Bayangkan eBPF sebagai "plugin" untuk kernel. Program eBPF (ditulis dalam C, lalu di-compile ke bytecode) di-attach ke hook tertentu: syscall, kprobe, tracepoint, atau XDP (packet processing). Kernel memverifikasi bytecode tersebut aman (tidak boleh loop tak terbatas, tidak boleh akses memori sembarangan) sebelum dijalankan.

Siklus hidup sebuah program eBPF terdiri dari empat tahap:

1. **Kompilasi.** Kode C dikompilasi clang menjadi BPF bytecode, biasanya sebagai ELF object.
2. **Verifikasi.** Verifier kernel memeriksa setiap jalur eksekusi. Ia menjamin program berhenti (tidak ada loop tak terbatas), tidak dereference pointer null, dan tidak membaca di luar batas buffer. Verifier yang menolak program Anda dengan pesan seperti `invalid access to map value` atau `back-edge from insn X to Y` adalah hal biasa, dan bukan bug kernel.
3. **JIT.** Bytecode diterjemahkan menjadi instruksi native mesin sehingga berjalan dengan overhead minimal, bukan diinterpretasi.
4. **Attach.** Program dikaitkan ke hook, dan hasilnya dibaca dari user space lewat map, ring buffer, atau perf buffer.

Yang sering terlewat: verifier bukan formal proof. Ia menolak banyak program yang sebenarnya aman (false positive), dan itu memang harga dari jaminan keselamatan kernel. Menulis eBPF berarti belajar menulis ulang kode Anda agar verifier bisa membuktikan sifatnya.

## CO-RE: Satu Binary, Banyak Versi Kernel

Inilah fitur yang membuat eBPF layak produksi. Dulu setiap kernel versi punya offset field struct yang berbeda, sehingga program harus dikompilasi ulang per node. **CO-RE (Compile Once, Run Everywhere)** menyelesaikannya lewat **BTF (BPF Type Format)**.

Mekanismya: saat kompilasi, clang mencatat setiap akses field struct sebagai metadata relokasi. Saat program di-load, libbpf membandingkan relokasi itu dengan BTF kernel yang sedang berjalan (tersedia di `/sys/kernel/btf/vmlinux`) dan menambal offset yang benar. Hasilnya, satu objek file bisa jalan di cluster yang kernel-nya heterogen tanpa rekompilasi.

Dalam praktiknya:

```c
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>

SEC("tracepoint/syscalls/sys_enter_openat")
int trace_openat(struct trace_event_raw_sys_enter *ctx)
{
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    bpf_printk("pid=%d\n", pid);
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
```

Header `vmlinux.h` di-generate sekali dari BTF kernel Anda (`bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h`), sehingga Anda tidak perlu menyertakan header kernel versi tertentu. Deklarasi lisensi wajib ada, karena beberapa helper function hanya tersedia untuk program berlisensi GPL-compatible.

## Tipe Program dan Titik Attach

Kesalahpahaman umum: eBPF hanya untuk jaringan. Faktanya tipe programnya beragam, dan pilihan tipe menentukan kemampuan Anda.

| Tipe program | Titik attach | Kegunaan |
|--------------|--------------|----------|
| `kprobe` / `kretprobe` | Entry/return fungsi kernel | Instrumentasi dinamis, bisa berubah antar versi |
| `tracepoint` | Tracepoint stabil kernel | Lebih stabil dari kprobe untuk data lintas versi |
| `fentry` / `fexit` | Entry/exit fungsi, overhead rendah | Alternatif kprobe yang lebih cepat di kernel 5.5+ |
| `XDP` | Driver network, paling awal | Filtering dan load balancing pada kecepatan tinggi |
| `tc` / `tcx` | Traffic control ingress/egress | Packet mangling dan kebijakan jaringan |
| `LSM (BPF LSM)` | Hook Linux Security Module | Penegakan kebijakan, bisa menolak operasi |
| `uprobe` / `uretprobe` | Fungsi user-space | Tracing aplikasi tanpa library |

Perbedaan mendasar yang perlu dipahami tim security: kprobe dan tracepoint bersifat **pasif**, mereka hanya mengamati. BPF LSM bersifat **aktif**, karena bisa mengembalikan kode error seperti `-EPERM` atau `-EACCES` langsung ke dispatcher syscall sehingga operasi dibatalkan sebelum efek sampingnya terjadi. BPF LSM tersedia sejak kernel 5.7.

Ada juga perkembangan menarik di sisi jaringan: **TCX** yang masuk di kernel 6.6 mengubah program TC menjadi BPF link yang dimiliki file descriptor, dengan urutan eksplisit `BPF_F_BEFORE` dan `BPF_F_AFTER` menggantikan prioritas numerik yang rapuh. Cilium sudah memigrasikan datapath-nya ke TCX. Dan di kernel 6.16, bahkan sebuah queuing discipline utuh (enqueue, dequeue, init, reset, destroy) bisa ditulis dalam BPF lewat `struct_ops`.

## Keunggulan dibanding Tools Lama

| Aspek | Agen Tradisional | eBPF |
|-------|------------------|------|
| Titik pengukuran | User-space / log | Kernel-space (syscall) |
| Overhead | Tinggi (poll + push) | Sangat rendah (event-driven) |
| Visibilitas jaringan | Terbatas (L7 butuh proxy) | Penuh (L3-L7, tanpa sidecar) |
| Perubahan aplikasi | Sering perlu SDK | Nol (transparan) |

Alasan overhead rendah bukan karena polling dihapus, tapi karena **agregasi bisa terjadi di kernel**. Program eBPF bisa menghitung, membuat histogram, dan memfilter sebelum data menyeberang batas kernel ke user space. Yang dikirim ke user space hanyalah ringkasan, bukan setiap event mentah. Membandingkan ini dengan agent yang menarik ribuan baris log per detik bukan perbandingan yang setara.

Mekanisme pengangkut datanya sendiri juga berkembang. **Ring buffer** (`BPF_MAP_TYPE_RINGBUF`) menggantikan perf buffer lama karena memakai satu wilayah memori bersama dengan alokasi atomic lewat `bpf_ringbuf_reserve()` dan `bpf_ringbuf_submit()`, yang berarti tidak ada masalah urutan antar CPU yang mengganggu perf event array.

## Tiga Pilar Penggunaan eBPF

**1. Observabilitas & Tracing**

Alat seperti Cilium Hubble dan Pixie memakai eBPF untuk membuat service map otomatis dan distributed tracing, tanpa harus menyuntikkan library ke tiap service. Kita melihat latensi per-request dari kernel, bukan dari log aplikasi yang sering terlambat.

Pembagian lapisannya di 2026 cukup jelas:

- **Cilium** sebagai CNI, menggantikan kube-proxy berbasis iptables dengan pemrosesan paket eBPF. Cilium 1.19 dirilis 25 Februari 2026, membawa packet tracing lewat IP options untuk flow tertentu, penyaringan flow berdasarkan status enkripsi, serta mode IPsec dan WireGuard yang lebih ketat.
- **Hubble** sebagai lapisan observability flow. Setiap koneksi ditangkap program eBPF, tanpa instrumentasi aplikasi. Anda bisa menjawab pertanyaan seperti "service apa yang berbicara dengan PostgreSQL dalam satu jam terakhir" langsung dari data kernel, bukan dari menebak konfigurasi.
- **Pixie** dan **Beyla** untuk observabilitas tingkat aplikasi. Pixie memakai eBPF uprobe untuk melacak traffic HTTP/1.1, HTTP/2, gRPC, dan protokol database (PostgreSQL, MySQL, Redis, Kafka) tanpa perubahan kode. Beyla, dari keluarga Grafana, melakukan hal serupa dengan output yang langsung cocok ke ekosistem Prometheus dan OpenTelemetry.
- **Tetragon** untuk keamanan runtime.

Kombinasi tersebut menutup hampir seluruh permukaan observability sebuah deployment Kubernetes, semuanya dari level kernel, bukan dari sidecar atau instrumentasi manual.

**2. Keamanan (Runtime Threat Detection)**

Tetragon (dari Cilium) mendeteksi anomali seperti proses yang tiba-tiba membuka koneksi keluar ke IP asing, atau binary yang dieksekusi dari `/tmp`. Karena berjalan di kernel, deteksinya hampir mustahil di-bypass oleh attacker yang sudah masuk ke container.

Bedanya Tetragon dengan alat sejenis adalah **enforcement sinkron**. Sebagian besar sistem deteksi bersifat asinkron: event dikumpulkan, dikirim ke backend, dianalisis, baru alarm berbunyi. Tetragon menegakkan kebijakan langsung di kernel, sehingga proses berbahaya bisa dibunuh pada saat syscall-nya terjadi, sebelum ia menyelesaikan aksinya. Tetragon 1.7.0 (rilis 29 April 2026) menambahkan pengambilan variabel environment, sensor fentry baru, dan evaluasi ekspresi CEL langsung di dalam BPF.

Contoh kebijakan Tetragon dalam YAML:

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: block-shell-in-container
spec:
  kprobes:
    - call: "security_bprm_check"
      syscall: false
      selectors:
        - matchArgs:
            - operator: "Prefix"
              values:
                - "/bin/sh"
                - "/bin/bash"
          matchActions:
            - action: Override
              argError: -1
```

Kebijakan di atas menolak eksekusi shell di dalam container. Perhatikan bahwa hook yang dipakai adalah hook LSM (`security_bprm_check`), bukan kprobe biasa, karena hanya LSM yang bisa menghentikan operasi secara sinkron. Memakai kprobe untuk hal ini hanya memberi Anda catatan kejadian, bukan pencegahan.

**3. Networking & Load Balancing**

Cilium menggantikan kube-proxy dengan eBPF XDP, menangani jutaan packet per detik dengan latency jauh lebih rendah. Ini krusial untuk cluster berskala besar.

XDP beroperasi di titik paling awal dalam jalur paket, tepat setelah driver network kartu, sehingga paket yang akan dibuang tidak perlu melewati seluruh stack jaringan kernel. Untuk skenario dengan puluhan ribu service, pendekatan berbasis iptables menjadi bottleneck karena aturannya linear dan dievaluasi berurutan, sedangkan lookup berbasis eBPF map bersifat konstan. Cilium 1.19 juga menambahkan integrasi Ztunnel dalam beta untuk kasus sidecar-free service mesh, memungkinkan mutual authentication antar service tanpa proxy terpisah di setiap pod.

## Contoh: Menangkap Syscall dengan bpftrace

Salah satu cara termudah mencoba eBPF adalah `bpftrace`. Berikut script untuk melihat semua proses yang membuka file:

```bash
# Pantau syscall openat di seluruh sistem
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat {
    printf("%-16s %s\n", comm, str(args->filename));
}'
```

Output-nya langsung menunjukkan proses dan file target secara live. Berguna untuk debugging aplikasi yang "file not found" tanpa harus menebak lewat `strace` yang memperlambat proses target secara signifikan.

Versi sedikit lebih berguna, menghitung jumlah file yang dibuka setiap proses dalam histogram latensi:

```bash
sudo bpftrace -e '
tracepoint:syscalls:sys_enter_openat
{
    @opens[comm] = count();
}
interval:s:5 { print(@opens); clear(@opens); }
'
```

Perhatikan `@opens[comm]` adalah map bertipe hash yang diagregasi di kernel. Yang dikirim ke user space hanya 5 detik sekali, jadi beban overhead-nya jauh lebih rendah daripada mencetak setiap event.

Untuk inspeksi program yang sudah ter-load di node, gunakan:

```bash
sudo bpftool prog list
sudo bpftool map list
sudo bpftool net list          # program yang ter-attach ke jalur jaringan
sudo bpftool prog show id <ID>  # termasuk stats dan pinned path
```

## Cara Membangun Program Serius

Untuk produksi, jangan menulis script bpftrace saja. Alur kerja yang biasa dipakai:

1. Tulis program C dengan section `SEC("...")` sesuai tipe attach.
2. Compile dengan clang targeting BPF (`clang -target bpf -g -O2 -c prog.bpf.c -o prog.bpf.o`), dengan flag `-g` agar informasi BTF ikut ter-generate untuk relokasi CO-RE.
3. Generate skeleton header dari libbpf: `bpftool gen skeleton prog.bpf.o > prog.skel.h`.
4. Tulis user-space loader dalam C atau Rust (paket `aya` untuk Rust) yang me-load skeleton, mengisi map, dan meng-attach link.

Rust menjadi pilihan yang makin lazim karena type safety dan penanganan error yang lebih baik dibanding C, dengan `aya` menyediakan abstraksi libbpf. Namun verifier tetap berbicara bahasa yang sama, jadi batasan teknisnya tidak berubah.

## Tantangan yang Perlu Diwaspadai

eBPF bukan silver bullet. Beberapa catatan praktis:

- **Versi kernel.** eBPF butuh kernel Linux 4.9+ sebagai minimum, tetapi fitur yang Anda butuhkan menentukan versi nyata: BPF LSM perlu 5.7, TCX perlu 6.6, qdisc berbasis BPF perlu 6.16, program type `fsession` baru ada di 7.0. Targetkan kernel 5.15 atau lebih baru agar semua alat utama berfungsi penuh. Di Windows atau macOS butuh WSL2 atau virtual machine.
- **Privilege.** Memuat program eBPF memerlukan `CAP_BPF` atau `CAP_SYS_ADMIN`. Di Kubernetes ini berarti container privileged atau DaemonSet dengan capability spesifik, dan itu menimbulkan pertimbangan keamanan tersendiri yang harus dijawab sebelum rollout.
- **Skill tim.** Menulis program eBPF membutuhkan pemahaman kernel C dan toolchain (clang, libbpf, bpftool). Untungnya tooling tingkat tinggi seperti Cilium sudah menyiapkan semua, sehingga sebagian besar tim tidak perlu menulis bytecode sendiri.
- **Supply chain.** Pastikan image eBPF agent diverifikasi checksum-nya. Kode berjalan di kernel, jadi kompromi berarti akses penuh node. Ini menjadikan SBOM dan penandatanganan artefak bukan kemewahan, melainkan prasyarat, untuk komponen yang jalan di ruang kernel.
- **Jebakan rilis.** `fsession` di kernel 7.0 mengubah cara mengukur latensi satu fungsi: satu program berjalan di entry dan return, dengan session cookie menggantikan hash map berbasis timestamp entry. Pola lama yang memakai map timestamp entry menjadi tidak perlu, dan kode yang di-copy dari tutorial lama mungkin tetap jalan tapi sudah tidak efisien.

## Kapan eBPF Bukan Jawabannya

eBPF kuat untuk observabilitas dan kebijakan di level kernel, tetapi ada batasnya. Untuk kebutuhan yang menuntut transformasi payload kompleks, logika bisnis berlapis, atau analisis antar paket dengan state panjang, tetap lebih masuk akal di user space atau di service mesh penuh. Verifier akan melawan Anda setiap kali mencoba menjejalkan logika besar ke dalam satu program, dan penolakan itu biasanya memang benar.

## Kesimpulan

eBPF adalah infrastruktur tak terlihat di balik observabilitas dan keamanan cloud-native 2026. Dengan kemampuan menangkap event di level kernel secara transparan dan berbiaya rendah, ia menggeser alat lama yang berbasis agent berat.

Untuk tim DevOps dan Security, langkah awal yang masuk akal adalah memasang Cilium dengan Hubble di cluster staging untuk melihat service map terbentuk dari traffic nyata, lalu menambahkan Tetragon dengan satu kebijakan sederhana seperti larangan eksekusi shell di container. Keduanya tidak menuntut Anda menulis kode eBPF sama sekali, tapi sudah memberi gambaran konkret seberapa jauh visibilitas kernel bisa membedah sistem Anda.
