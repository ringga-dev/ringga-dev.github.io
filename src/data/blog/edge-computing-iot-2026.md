---
title: "Edge Computing & IoT: Arsitektur Masa Depan Aplikasi Real-Time"
description: "Bagaimana edge computing merevolusi IoT di tahun 2026 — dari AI processing di perangkat edge hingga 5G-enabled smart infrastructure."
date: "2026-07-01"
author: "Ringga Septia Pribadi"
tags: ["Edge Computing", "IoT", "Cloud", "5G", "Infrastructure"]
category: "Cloud & Infrastructure"
image: "https://images.unsplash.com/photo-1531497865144-0464ef8fb9a9?w=800&q=80"
---

## Pendahuluan

Edge computing telah menjadi fondasi utama Internet of Things (IoT) di tahun 2026. Dengan miliaran perangkat terhubung, memproses data di cloud saja tidak lagi cukup. Model klasik, yaitu semua sensor mengirim data mentah ke satu pusat data, runtuh begitu jumlah perangkat dan laju data meningkat. Ongkos bandwidth membengkak, latensi menumpuk di jalur pulang-pergi, dan satu gangguan jaringan bisa mematikan seluruh sistem.

Edge computing memindahkan pemrosesan lebih dekat ke sumber data. Artikel ini membedah mengapa pendekatan ini perlu, bagaimana AI bisa berjalan di perangkat dengan RAM di bawah satu megabyte, apa yang sebenarnya ditawarkan 5G, dan pola arsitektur yang bisa langsung diterapkan.

## Mengapa Edge Computing?

### Masalah dengan Cloud-Centric IoT

- **Latency.** Satu perjalanan data sensor ke pusat data dan kembali biasanya berada di rentang ratusan milidetik. Untuk sistem yang harus merespons dalam milidetik, ini sudah terlambat.
- **Bandwidth.** Satu kamera CCTV beresolusi penuh bisa menghasilkan puluhan gigabyte per hari. Mengirim semua frame ke cloud hanya untuk analisis adalah pemborosan, karena sebagian besar frame tidak mengandung kejadian menarik.
- **Privacy.** Data yang berkaitan dengan wajah, suara, atau lokasi individu seringkali tidak boleh meninggalkan lokasi fisik tempat data diambil, baik karena regulasi maupun kebijakan perusahaan.
- **Offline.** Pabrik, kapal, dan lokasi tambang sering berada di area dengan koneksi tidak stabil. Sistem yang bergantung pada koneksi permanen ke cloud akan berhenti bekerja tepat saat dibutuhkan.

### Solusi Edge Computing

```
Sensor → Edge Gateway (AI Processing) → Cloud (Analytics)
         ↓
    Real-time Action (2-5ms)
```

Prinsipnya adalah menyaring di tepi dan mengirim yang bermakna ke cloud. Edge gateway melakukan inferensi pada data mentah, lalu hanya mengirim hasil agregat, event, atau frame yang ditandai sebagai anomali. Cloud tetap dipakai, tetapi untuk apa yang memang cocok di cloud: pelatihan model, analisis jangka panjang, dan dashboard lintas lokasi.

## Arsitektur Berlapis

Sistem edge yang sehat biasanya punya tiga lapis, dan setiap lapis punya karakteristik yang berbeda.

### Lapis Perangkat

Sensor dan aktuator dengan daya terbatas. Di lapis ini komputasi dihemat sebisanya, dan komunikasi biasanya memakai protokol ringan seperti MQTT di atas Wi-Fi, atau LoRaWAN dan NB-IoT untuk jarak jauh dengan konsumsi daya sangat rendah.

ESP32-S3 adalah contoh SoC yang populer di lapis ini: dual-core Xtensa LX7 sampai 240 MHz dengan 512 KB SRAM internal, ditambah instruksi akselerasi untuk neural network, Wi-Fi 2.4 GHz, dan Bluetooth LE. Kombinasi itu membuat inferensi kecil bisa dijalankan tanpa modul tambahan.

### Lapis Gateway

Perangkat dengan daya lebih besar, misalnya mini PC industri atau single board computer. Di sinilah model AI yang lebih besar dijalankan, data dari banyak sensor dinormalisasi, dan keputusan real-time diambil. Gateway juga bertindak sebagai buffer saat koneksi ke cloud terputus.

### Lapis Cloud

Menjadi tempat agregasi lintas lokasi, pelatihan dan pembaruan model, penyimpanan historis, dan orkestrasi. Peran cloud bukan lagi memproses setiap event, melainkan mengelola siklus hidup sistem secara keseluruhan.

## Protokol Komunikasi: MQTT

MQTT tetap menjadi protokol standar untuk telemetri IoT karena model publish-subscribe-nya yang tidak menuntut perangkat selalu online bersamaan. Broker menjadi titik temu, sehingga sensor yang tidur dalam deep sleep tetap bisa mempublish dan data-nya disimpan untuk subscriber yang baru connect.

Konsep yang perlu dikuasai:

- **Topic hierarchy.** Struktur seperti `pabrik/lini-1/mesin-3/suhu` memudahkan filtering dan manajemen hak akses.
- **Wildcard.** `+` mencocokkan satu level, `#` mencocokkan semua level di bawahnya.
- **QoS 0, 1, 2.** At most once, at least once, dan exactly once. Untuk telemetri berkala, QoS 0 sudah memadai karena data berikutnya segera datang. Untuk perintah aktuator, gunakan QoS 1.
- **Retained message.** Menyimpan pesan terakhir pada topic sehingga subscriber baru langsung mendapat state terakhir tanpa menunggu publish berikutnya.
- **Shared subscription.** Membagi beban satu topic ke beberapa instance consumer, praktis untuk worker yang memproses event secara paralel.

MQTT 5.0 menambahkan reason code pada ACK, session expiry interval, topic alias untuk mengurangi overhead, user properties untuk metadata, dan subscription option seperti flag no local. Topic alias khususnya penting untuk perangkat dengan bandwidth kecil karena topic string yang panjang tidak perlu diulang di setiap paket.

Eclipse Mosquitto adalah broker open source yang mendukung MQTT 5.0, 3.1.1, dan 3.1, serta cukup ringan untuk berjalan di single board computer maupun server penuh.

```bash
# Broker Mosquitto dijalankan dengan konfigurasi eksplisit
mosquitto -c /etc/mosquitto/mosquitto.conf -v

# Publish data suhu dengan QoS 1 dan retained
mosquitto_pub -h broker.local -t 'pabrik/lini-1/mesin-3/suhu' \
  -q 1 -r -m '{"c":78.4,"ts":1751328000}'

# Subscribe semua sensor pada satu lini
mosquitto_sub -h broker.local -t 'pabrik/lini-1/+/suhu' -v
```

## AI di Edge: TinyML

TinyML merujuk pada machine learning yang berjalan di microcontroller dengan memori sangat terbatas. Kematangannya datang dari tiga hal: arsitektur model yang memang dirancang kecil, kuantisasi, dan kernel inferensi yang dioptimalkan untuk ARM.

### Kuantisasi

Model dilatih dalam float32. Sebelum dideploy ke perangkat kecil, model dikonversi ke int8. Hasilnya ukuran turun sekitar empat kali lipat dibanding float32, dan inferensi menjadi lebih cepat pada hardware tanpa floating point unit, dengan penurunan akurasi yang biasanya dapat diterima untuk tugas klasifikasi sederhana.

### Runtime

TensorFlow Lite for Microcontrollers adalah runtime yang banyak dipakai. Contoh paling dikenal adalah `micro_speech`, yang menjalankan model sekitar 20 kilobyte untuk mengenali dua kata, dengan footprint kode sekitar 22 kilobyte pada Cortex-M3 dan penggunaan RAM kerja sekitar 10 kilobyte. Angka tersebut menunjukkan betapa kecilnya kebutuhan memori yang bisa dipenuhi.

Edge Impulse menyediakan pipeline lengkap dari akuisisi data sampai deployment, dan menawarkan EON Compiler yang menghilangkan overhead interpreter TFLM sehingga penggunaan RAM dan flash bisa ditekan lebih jauh tanpa kehilangan akurasi.

| Platform | Chip | RAM | Model Size |
|----------|------|-----|------------|
| TensorFlow Lite Micro | ESP32, RP2040 | 256KB | < 50KB |
| Edge Impulse | STM32, nRF52 | 128KB | < 30KB |
| OpenMV | i.MX RT | 1MB | < 200KB |

### Trade-off yang Perlu Diketahui

Menjalankan model di perangkat bukan tanpa konsekuensi. Model kecil berarti kapasitas representasi terbatas, sehingga tugas yang membutuhkan banyak kelas atau input berdimensi tinggi tetap perlu dijalankan di gateway atau cloud. Selain itu pembaruan model menjadi lebih lambat karena harus didistribusikan ke banyak perangkat, dan versi model yang berjalan di lapangan bisa tidak seragam.

Pola yang umum dipakai: model kecil di perangkat untuk deteksi awal, dan ketika model kecil tidak yakin, frame atau sinyal dikirim ke gateway atau cloud untuk analisis lebih dalam. Ini menekan bandwidth tanpa mengorbankan akurasi pada kasus yang benar-benar ambigu.

## 5G dan Multi-access Edge Computing

5G sering dijelaskan hanya dari sisi kecepatan, padahal untuk IoT yang lebih relevan adalah tiga area lain.

Menurut requirement IMT-2020 yang diterbitkan ITU, target teknisnya antara lain user plane latency 1 ms untuk URLLC dan 4 ms untuk eMBB, serta connection density 1.000.000 perangkat per km persegi untuk mMTC. Angka densitas itulah yang membuat IoT skala kota menjadi memungkinkan secara teori, karena tidak ada batasan praktis jumlah perangkat per sel.

Tiga kategori penggunaan 5G:

- **eMBB** untuk throughput tinggi, misalnya video analytics.
- **URLLC** untuk latensi sangat rendah dengan reliabilitas tinggi, misalnya kendali robot atau sistem keselamatan.
- **mMTC** untuk jumlah perangkat sangat besar dengan payload kecil, misalnya meteran dan sensor lingkungan.

Network slicing memungkinkan satu infrastruktur fisik dibagi menjadi beberapa jaringan logis dengan karakteristik berbeda. Satu slice bisa dikonfigurasi untuk latensi rendah, slice lain untuk kapasitas besar, dan slice ketiga dengan prioritas lebih rendah untuk perangkat non-kritis. Dari sisi bisnis, ini berarti layanan mission-critical tidak saling mengganggu dengan trafik konsumen.

MEC (Multi-access Edge Computing) menempatkan komputasi di titik presence operator, lebih dekat ke pengguna dibanding pusat data regional. Efeknya latensi turun tanpa harus membangun fasilitas sendiri di setiap lokasi.

### Kenapa Cloudflare Workers Menarik untuk Tepi Aplikasi

Di sisi aplikasi web, tepi bukan berarti perangkat fisik. Platform seperti Cloudflare Workers menjalankan kode di V8 isolate yang tersebar di banyak kota, dengan cold start yang sangat rendah karena tidak ada proses container yang perlu dihidupkan. Model bayarnya per CPU time, bukan waktu idle.

Durable Objects melengkapi ini dengan menyediakan koordinasi berstate pada satu lokasi, sehingga kasus seperti WebSocket, penghitung, dan antrean bisa ditangani tanpa mengorbankan konsistensi. Untuk aplikasi yang penggunanya tersebar secara geografis, memindahkan logika ringan ke tepi jaringan berarti waktu pulang-pergi ke satu region tunggal hilang sepenuhnya.

## Orchestrasi di Edge: K3s dan KubeEdge

Ketika beban kerja di gateway memakai container, muncul pertanyaan bagaimana cara mengelolanya tanpa menginstal Kubernetes penuh di perangkat dengan resource terbatas.

**K3s** adalah distribusi Kubernetes ringan dari Rancher yang dikemas menjadi satu binary, dengan ukuran footprint memori dan disk yang jauh lebih kecil. Cocok untuk gateway dan lokasi yang butuh Kubernetes API yang familier tanpa kompleksitas cluster penuh. Studi komparatif akademik menunjukkan distribusi ringan seperti K3s dan k0s unggul dalam kemudahan pengembangan berkat kesederhanaannya.

**KubeEdge** mengambil pendekatan berbeda. Arsitektinya memisahkan CloudCore yang berjalan di pusat dan EdgeCore yang berjalan di node edge, dengan lapisan messaging di antaranya. Fitur utamanya adalah edge autonomy: node edge tetap bisa menjalankan workload meski terputus dari control plane, dan metadata disimpan secara lokal. Device management dilakukan lewat Device CRD pada Kubernetes API, sehingga perangkat bisa dikelola dengan cara yang sama seperti resource Kubernetes lain. EdgeMesh menyediakan service discovery dan traffic proxy antar pod di edge tanpa perlu mengetahui topologi jaringan di belakangnya.

Konsekuensinya untuk pemilihan tooling: kalau kamu butuh Kubernetes API yang familier dengan overhead minimal, K3s sudah cukup. Kalau butuh manajemen perangkat IoT skala besar dengan toleransi terputus jangka panjang, KubeEdge lebih sesuai. Perlu dicatat bahwa KubeEdge memiliki konsumsi resource yang lebih tinggi dibanding distribusi ringan, jadi pastikan spesifikasi gateway memadai.

## Use Case: Smart Manufacturing

Pabrik modern menggunakan edge computing untuk predictive maintenance. Pola implementasinya kira-kira sebagai berikut.

Satu mesin industri bisa dipasangi ratusan sensor yang mengukur getaran, suhu, arus, dan tekanan. Data dikirim ke gateway lokal yang menjalankan model deteksi anomali. Model dilatih di cloud menggunakan data historis kerusakan, lalu di-deploy ke gateway dalam bentuk terkuantisasi.

Saat pola getaran menyimpang dari baseline, gateway menandai potensi masalah dan mengirim alert ke sistem maintenance. Karena deteksi terjadi lokal, tindakan bisa diambil dalam hitungan milidetik, misalnya menurunkan beban mesin atau menghentikan siklus sebelum komponen rusak total. Hanya data ringkasan dan event anomali yang dikirim ke cloud, sehingga kebutuhan bandwidth turun drastis dibanding mengalirkan semua data sensor.

Dampak ekonominya datang dari dua sisi: biaya perbaikan darurat yang jauh lebih mahal daripada perawatan terjadwal bisa dihindari, dan waktu henti produksi yang tidak direncanakan berkurang. Angka pastinya bergantung pada jenis industri dan nilai output per jam, jadi perlu dihitung per kasus, bukan diasumsikan.

## Kesimpulan

Edge computing + IoT adalah fondasi smart infrastructure masa depan. Dengan TinyML dan 5G, implementasi menjadi semakin terjangkau untuk berbagai skala industri. Yang menentukan keberhasilan bukan pemilihan hardware termahal, melainkan keputusan di lapis mana data harus diproses. Saring di tepi, agregasi di cloud, dan pastikan sistem tetap berfungsi saat jaringan mati.
