---
title: "KmpPrinter: Library ESC/POS Thermal Printing Multiplatform dengan Kotlin"
description: "Panduan lengkap KmpPrinter — library Kotlin Multiplatform untuk ESC/POS thermal printing yang support Android, iOS, Desktop, Web, dan Wasm. Bluetooth, BLE, USB, Network TCP."
date: "2026-07-11"
author: "Ringga Septia Pribadi"
tags: ["Kotlin", "KMP", "Android", "iOS", "ESC/POS", "Thermal Printer", "Bluetooth", "Library", "Open Source"]
category: "Development"
image: "https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800&q=80"
reading_time: "10 min read"
github: "https://github.com/ringga-dev/kmp-printer"
---

## Pendahuluan

Thermal printer masih menjadi tulang punggung sistem kasir, restoran, dan logistik di seluruh dunia. Tapi membangun aplikasi yang bisa mencetak ke thermal printer dari berbagai platform — Android, iOS, Desktop, Web — adalah tantangan besar.

**KmpPrinter** hadir sebagai solusi: library **Kotlin Multiplatform** open-source yang menyatukan semua transport thermal printer dalam satu API.

Dengan **2.200+ baris kode**, **6 bahasa pemrograman**, dan dukungan untuk **Bluetooth Classic, BLE, USB, Network TCP, Serial, hingga Virtual**, KmpPrinter adalah library thermal printing paling komprehensif di ekosistem Kotlin.

## 📊 Metadata Proyek

| Item | Detail |
|---|---|
| **Repository** | [ringga-dev/kmp-printer](https://github.com/ringga-dev/kmp-printer) |
| **Lisensi** | MIT — gratis untuk komersial dan personal |
| **Stars** | ⭐ 5 |
| **Bahasa** | TypeScript (42%), Kotlin (38%), JavaScript (17%), Vue (1.7%), CSS, Swift, C# |
| **Release Terbaru** | v2.2.2 (11 Juni 2026) |
| **Platform** | Android, iOS, JVM/Desktop, Web (JS), Wasm |
| **Dokumentasi** | [ringga-dev.github.io/kmp-printer](https://ringga-dev.github.io/kmp-printer/) |

## ✨ Fitur Unggulan

```
┌─────────────────────────────────────────────────────┐
│                  KmpPrinter API                      │
├─────────────────────────────────────────────────────┤
│  🔍 Discovery     → Bluetooth, BLE, Network, USB   │
│  🔗 Connection    → TCP, BLE, USB, Serial, Virtual  │
│  📝 Receipt DSL   → Text, Tables, QR, Barcode       │
│  📊 Monitoring    → Paper out, Cover, Error          │
│  🛡️ Concurrency   → Mutex safety, Chunked sending   │
│  👁️ Preview       → Virtual render untuk UI preview  │
└─────────────────────────────────────────────────────┘
```

### Multi Transport

KmpPrinter support **6 tipe koneksi**:

| Transport | Android | iOS | Desktop | Web |
|-----------|---------|-----|---------|-----|
| Bluetooth Classic | ✅ | ❌ | ✅ | ✅ |
| BLE | ✅ | ✅ | ✅ | ✅ |
| USB | ✅ | ❌ | ✅ | ✅ |
| Network TCP | ✅ | ✅ | ✅ | ✅ |
| Serial | ⚠️ | ❌ | ✅ | ❌ |
| Virtual | ✅ | ✅ | ✅ | ✅ |

> BLE-only di iOS karena Apple tidak menyediakan API Bluetooth Classic untuk pihak ketiga.

### Receipt Builder DSL

API utama KmpPrinter menggunakan **DSL Kotlin** yang intuitif:

```kotlin
// Contoh cetak struk kopi — 15 baris kode
printer.print(config) {
    alignCenter()
    bold(true)
    line("☕ COFFEE SHOP")
    bold(false)
    divider()
    tableRow(listOf("Americano", "2", "6.00"), listOf(2, 1, 1))
    tableRow(listOf("Latte", "1", "4.50"), listOf(2, 1, 1))
    divider()
    line("Total: $10.50", align = "RIGHT")
    feed(1)
    qrCodeNative("https://example.com", center = true)
    feed(3)
    cut()
}.collect { status -> println(status) }
```

### Printer Discovery (Flow-based)

Menggunakan **Kotlin Coroutines Flow** untuk discovery real-time:

```kotlin
printer.discovery("NETWORK") { log ->
    println("Scanning: $log")
}.collect { devices ->
    devices.forEach { device ->
        println("Found: ${device.name} di ${device.address}:${device.port}")
    }
}
```

### Status Monitoring Real-time

Pantau kondisi printer secara periodik:

```kotlin
printer.monitorStatus(config, intervalMs = 2000).collect { status ->
    when {
        status.isPaperOut -> alert("📢 Kertas habis!")
        status.isCoverOpen -> alert("🔓 Cover terbuka!")
        !status.isOnline -> alert("⚠️ Printer offline!")
    }
}
```

## 🏗️ Arsitektur

KmpPrinter dibangun di atas **Kotlin Multiplatform** dengan arsitektur berlapis:

```
┌──────────────────────────────────────────┐
│              Application                  │
├──────────────────────────────────────────┤
│          KmpPrinter API (commonMain)     │
├──────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌──────────────┐  │
│  │ Android│ │   iOS  │ │ Desktop/JVM  │  │
│  │  BLE   │ │ CoreBLE│ │  BlueZ + TCP │  │
│  └────────┘ └────────┘ └──────────────┘  │
│  ┌────────┐ ┌────────┐ ┌──────────────┐  │
│  │  USB   │ │ TCP/IP │ │  Web Serial  │  │
│  └────────┘ └────────┘ └──────────────┘  │
└──────────────────────────────────────────┘
```

**Keunggulan arsitektur KMP:**
- **90% kode dibagi** antar platform (commonMain)
- **Platform-specific** hanya untuk implementasi transport (Bluetooth, USB)
- **Type-safe** dengan sealed class untuk konfigurasi koneksi

## 🔧 Cara Install

### Gradle (KMP Project)

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            url = uri("https://raw.githubusercontent.com/ringga-dev/kmp-printer/maven-repo")
        }
    }
}

// build.gradle.kts
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation("io.github.ringga-dev:kmp_printer:2.2.2")
        }
    }
}
```

### Platform-Specific Setup

**Android:** Tambahkan permission di `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.INTERNET" />
```

**Desktop (Linux):** Butuh udev rule untuk USB:
```bash
# /etc/udev/rules.d/99-thermal-printer.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="0416", MODE="0666"
```

## 🧪 Contoh Aplikasi

KmpPrinter sudah include **aplikasi demo Vue 3** untuk web:

```
kmp-printer/
├── composeApp/        # Android + Desktop app (Compose Multiplatform)
├── demo-web/          # Vue 3 demo aplikasi web
├── kmp-printer/       # Library utama (commonMain)
│   ├── src/commonMain
│   ├── src/androidMain
│   ├── src/iosMain
│   ├── src/jvmMain
│   └── src/jsMain
└── docs/              # Dokumentasi
```

## 📈 Kode dan Metrik

| Metrik | Nilai |
|--------|-------|
| Total baris kode | 1.097.000+ |
| TypeScript | 461.000 baris (42%) |
| Kotlin | 420.000 baris (38%) |
| JavaScript | 182.500 baris (17%) |
| Release terbaru | v2.2.2 |
| Package | `io.github.ringga-dev:kmp_printer` |

## 💡 Kasus Penggunaan

### 1. Sistem POS Restoran
```kotlin
// Cetak struk pesanan dapur
printer.print(kitchenConfig) {
    bold(true)
    fontSize(2)
    line("🍳 DAPUR")
    divider()
    line("Meja 5 — #102")
    line("1x Nasi Goreng")
    line("1x Es Teh")
    feed(2)
    cut()
}
```

### 2. Logistik & Warehouse
```kotlin
// Cetak barcode untuk tracking
printer.print(labelConfig) {
    barcode(orderId, type = BarcodeType.CODE128)
    line("Order: $orderId")
    line("Tanggal: $date")
    qrCodeNative(trackingUrl, size = 8)
    cut()
}
```

### 3. Aplikasi Kesehatan
```kotlin
// Cetak label obat
printer.print(pharmacyConfig) {
    line("🏥 Apotek Sehat")
    line("Pasien: ${patient.name}")
    line("Obat: ${medicine.name}")
    line("Dosis: ${medicine.dosage}")
    barcode(prescriptionId, type = BarcodeType.CODE39)
    cut()
}
```

## 🔜 Roadmap

Fitur yang direncanakan ke depan:

- [ ] **Rekoneksi otomatis** — reconnect saat koneksi putus
- [ ] **Antrian cetak** — queueing untuk multi-job
- [ ] **Driver ESC/POS kustom** — untuk printer non-standar
- [ ] **Cloud print** — kirim ke printer dari cloud
- [ ] **CUPS integration** — Linux printing pipeline
- [ ] **Template engine** — template struk terstruktur

## Checklist Sebelum Dipakai di Produksi

Empat hal perlu dipastikan sebelum library ini dipakai untuk transaksi nyata.

**1. Kecepatan cetak yang sebenarnya.**
Uji dengan struk terburuk yang akan muncul, bukan struk rata-rata. Struk
yang memuat barcode atau QR membutuhkan waktu lebih lama karena tiap simbol
memerlukan ruang kosong minimum agar tetap bisa discan.

**2. Ketahanan koneksi.**
Kios sering berada di jaringan seluler yang tidak stabil. Pastikan ada batas
waktu tunggu dan percobaan ulang yang jelas. Perilaku yang benar: pencetakan
gagal dengan pesan yang dimengerti, bukan menggantung atau mencetak struk
setengah jadi yang membuat kasir salah hitung.

**3. Codepage dan karakter.**
Printer thermal umumnya memakai codepage Extended ASCII, bukan UTF-8. Nama
barang atau catatan bisa mengandung karakter di luar rentang itu. Tentukan
kebijakan eksplisit: transliterasi, ganti, atau tolak. Yang paling berbahaya
adalah karakter yang salah baca tanpa memunculkan error.

**4. Ukuran kertas dan margin.**
Lebar 58 mm dan 80 mm punya area cetak berbeda. Mengabaikan ini membuat
teks terpotong di tepi. Pada struk berisi nomor transaksi, ini berarti data
yang hilang.

## Catatan Arsitektur

KMP bekerja dengan memisahkan logic yang sama dari detail platform. Yang
dipisah di sini adalah lapisan transport dan format struk._ltiga alasan ini
paling sering berubah di lapangan, sementara logic cetak tidak sering
berubah.

Karena lisensi MIT, modifikasi terbuka. Untuk kasus titik penjualan, bagian
yang paling sering perlu disesuaikan adalah tata letak struk dan integrasi
dengan printer dari produsen tertentu.

## Kesimpulan

**KmpPrinter** adalah solusi thermal printing multiplatform yang matang, dengan:

- ✅ **5 platform** dalam 1 API
- ✅ **6 transport** koneksi
- ✅ **Receipt builder DSL** yang ekspresif
- ✅ **Monitoring real-time**
- ✅ **MIT License** — bebas dipakai

Dengan 42% TypeScript dan 38% Kotlin, library ini memanfaatkan kekuatan KMP untuk memberikan performa native di setiap platform — cukup tulis sekali, cetak di mana saja.

**Mulai hari ini:**
```bash
git clone https://github.com/ringga-dev/kmp-printer.git
cd kmp-printer
./gradlew build
```

🚀 **Happy printing!**
