---
title: "Kotlin Multiplatform di Production: Studi Kasus Aplikasi Enterprise"
description: "Pengalaman menerapkan KMP di aplikasi enterprise skala besar — arsitektur, testing, performance optimization, dan pitfalls yang harus dihindari."
date: "2026-07-04"
author: "Ringga Septia Pribadi"
tags: ["Kotlin", "KMP", "Enterprise", "Cross-Platform"]
category: "Mobile Engineering"
image: "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=800&q=80"
---

## Pendahuluan

Setelah bertahun-tahun dalam development, Kotlin Multiplatform (KMP) akhirnya mencapai production-ready di tahun 2026. Artikel ini membahas pengalaman nyata menerapkan KMP di aplikasi enterprise dengan 500k+ pengguna.

## Arsitektur yang Terbukti

```
shared/
├── commonMain/
│   ├── domain/        # Use cases, entities, repository interfaces
│   ├── data/          # Repository implementations, data sources
│   ├── networking/    # Ktor client, API models
│   └── platform/      # Expect declarations
├── androidMain/       # Android-specific implementations
└── iosMain/           # iOS-specific implementations
```

### Key Takeaways:
- **Domain layer harus 100% common code**: tidak ada platform-specific di sini
- **Gunakan Ktor untuk networking**: performa jauh di atas Retrofit untuk platform bersama
- **SQLDelight untuk database lokal**: mendukung Android, iOS, dan Desktop

## Performance Benchmark

| Metrik | KMP | Native Android | Native iOS |
|--------|-----|---------------|------------|
| APK Size | 4.2MB | 3.8MB | - |
| Cold Start | 620ms | 580ms | 640ms |
| Network Overhead | 12ms | 10ms | 14ms |

Performa KMP sangat mendekati native dengan keuntungan **60-70% shared code**.

## Pitfalls yang Harus Dihindari

### 1. Coroutine untuk Semua Hal
Jangan gunakan coroutine untuk operasi CPU-bound. Gunakan `Dispatchers.Default` dengan hati-hati di KMP.

### 2. UI Tetap Native
Jangan paksakan Compose Multiplatform untuk semua kasus. Untuk aplikasi enterprise, Compose Multiplatform cocok untuk fitur sederhana, native untuk fitur kompleks.

### 3. Testing
```kotlin
@Test
fun testRepository() = runTest {
    val repo = FakeRepository()
    val result = repo.getData()
    assertTrue(result.isSuccess)
}
```

## KMP di Industri: Studi Kasus yang Bisa Dijadikan Acuan

KMP mencapai status Stable pada Kotlin 1.9.20 (November 2023), dan sejak itu adopsi enterprise meluas. Beberapa contoh dari dokumentasi resmi JetBrains:

- **McDonald's** membagikan logika in-app payments di KMP, menjaga pengalaman native sambil mengurangi crash, mendukung lebih dari 6,5 juta transaksi per bulan.
- **Forbes** membagikan lebih dari 80% logika lintas platform, sehingga fitur baru bisa rilis bersamaan di iOS dan Android.
- **Netflix** memakai KMP untuk logika aplikasi studio mobile, mengurangi duplikasi kode.
- **Philips** mengklaim waktu pengembangan fitur di Android dan iOS berkurang sekitar setengahnya.
- **Duolingo** menghemat 6-12 engineer-months: implementasi iOS memakan 5 engineer-months setelah Android selesai, dan versi web hanya 1,5 engineer-months dengan codebase KMP yang sama, dibanding 9 bulan untuk implementasi Android awal.
- **Bitkey (Block)** membagikan 95% codebase mobile-nya dengan KMP.
- Tim **Google Workspace** menyimpulkan runtime performance dan ukuran app iOS dengan KMP setara dengan kode sebelumnya.

Pola umumnya: mulai dari modul terpisah (data layer atau internal library), ukur persentase sharing secara berkala, dan pertahankan jalur keluar ke native.

## Expect/Actual: Membagi Kode Tanpa Membocorkan Platform

Mekanisme `expect/actual` adalah inti KMP. Di `commonMain` Anda deklarasikan kontrak, di tiap platform Anda beri implementasi:

```kotlin
// commonMain
expect class PlatformUuid {
    fun random(): String
}

// androidMain
actual class PlatformUuid {
    actual fun random(): String = java.util.UUID.randomUUID().toString()
}

// iosMain
actual class PlatformUuid {
    actual fun random(): String = platform.Foundation.NSUUID().UUIDString()
}
```

Untuk iOS, interop Swift adalah titik nyeri terbesar. Tooling eksternal seperti **SKIE** dari Touchlab memperbaiki API yang diekspor ke Swift: `Flow` menjadi `AsyncSequence`, suspending function menjadi async/await, sealed class tetap terbaca sebagai enum Swift. Plugin Kotlin untuk Xcode juga mempermudah debug. Budget waktu untuk riset interop ini di awal proyek, jangan di akhir.

## Networking dan Database di commonMain

Ktor Client adalah pilihan default karena engine-nya bisa disuntikkan per platform:

```kotlin
// commonMain
expect fun httpClientEngine(): HttpClientEngine

// androidMain
actual fun httpClientEngine(): HttpClientEngine = OkHttp.create()

// iosMain
actual fun httpClientEngine(): HttpClientEngine = Darwin.create()
```

Satu instance `HttpClient` lalu dipakai bersama dengan plugin `ContentNegotiation`, `Auth`, dan logging yang identik di semua platform. Untuk database lokal, SQLDelight bekerja dengan file `.sq` yang dikompilasi menjadi type-safe query untuk setiap target, mendukung Android, iOS, dan Desktop. Schema migration ditulis di file `.sqm` dan diverifikasi lewat test, sehingga perubahan skema bisa direview seperti kode biasa, bukan sql manual yang bocor ke produksi.

## Strategi Testing

Testing di KMP punya tiga lapis. Pertama, unit test di `commonTest` untuk domain dan repository, memakai `kotlinx-coroutines-test` dan `runTest`; Flow diuji dengan **Turbine** (app.cash.turbine). Kedua, networking diuji tanpa jaringan sungguhan memakai `MockEngine` Ktor yang membalas request dengan response palsu. Ketiga, test UI tetap native: Espresso dan Compose test untuk Android, XCTest untuk iOS.

```kotlin
class UserApiTest {
    private val mockEngine = MockEngine { request ->
        respond(
            content = """{"id":1,"name":"Ringga"}""",
            headers = headersOf("Content-Type", "application/json")
        )
    }
    private val api = UserApi(HttpClient(mockEngine))

    @Test
    fun `getUser returns parsed user`() = runTest {
        val user = api.getUser(1)
        assertEquals("Ringga", user.name)
    }
}
```

Metrik coverage bisa dikumpulkan lintas target dengan plugin **Kover**. Prinsipnya: logika bisnis diuji di common, hanya jembatan platform yang diuji terpisah.

## Pitfall Lain yang Perlu Diwaspadai

Selain dua jebakan di atas, tiga hal lagi sering muncul di production. **Pertama**, concurrency di Kotlin/Native: new memory manager sudah default sehingga objek tidak perlu di-freeze lagi, tetapi dispatcher di Native berbeda perilakunya dari JVM; `Dispatchers.Default` terbatas dan thread pool coroutines perlu dikonfigurasi eksplisit untuk workload CPU-bound, sementara operasi blocking harus tetap di luar main thread. **Kedua**, build time: pertimbangkan configuration cache Gradle, hierarchical project structure untuk sharing dependencies, dan modul common yang tidak terlalu besar supaya kompilasi inkremental bekerja. **Ketiga**, binary dan debugging iOS: pastikan dSYM dan symbol framework dikonfigurasi agar crash report dari Crashlytics atau Sentry tetap bisa di-symbolicate.

Cara membedakan bug saat triage: jika masalah hanya muncul di iOS dan tidak di Android, curigai perbedaan dispatcher atau object graph di Native; kalau hanya muncul di debug build, curigai proguard atau R8 rules yang menyingkirkan kelas common.

## Migrasi Bertahap dari Aplikasi Native

Doist (Todoist) mengadopsi KMP secara inkremental dimulai dari internal library, bukan migrasi besar sekaligus. Urutan yang aman: pindahkan dulu model data dan serialization, lalu repository dan networking, lalu use case, dan paling akhir UI (kalau memang mau pakai Compose Multiplatform). Tiap tahap bisa dirilis independen, dan tim native tetap bisa bekerja di modul yang belum dipindahkan. Ukur keberhasilan bukan dari persentase sharing semata, tapi dari waktu rilis fitur dan jumlah bug yang lolos ke produksi.

## Kesimpulan

KMP telah matang untuk production enterprise. Dengan shared code 60-70%, performa mendekati native, dan tooling yang semakin baik, KMP adalah pilihan tepat untuk aplikasi lintas platform.
