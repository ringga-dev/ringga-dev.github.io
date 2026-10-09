---
title: "Integrasi Google Gemini AI ke Aplikasi Android: Panduan Lengkap"
description: "Tutorial step-by-step mengintegrasikan Gemini AI API ke aplikasi Android menggunakan Ktor Client, dari setup hingga implementasi fitur AI canggih."
date: "2026-06-22"
author: "Ringga Septia Pribadi"
tags: ["Gemini", "AI", "Android", "Kotlin", "Ktor"]
category: "Artificial Intelligence"
image: "https://images.unsplash.com/photo-1591453089816-0fbb971b454c?w=800&q=80"
---

## Pendahuluan

Google Gemini AI telah menjadi salah satu AI model paling powerful di tahun 2026. Mengintegrasikannya ke aplikasi Android membuka kemungkinan fitur yang luar biasa.

## Setup Project

### Dependencies
```kotlin
dependencies {
    implementation("io.ktor:ktor-client-core:3.2.0")
    implementation("io.ktor:ktor-client-okhttp:3.2.0")
    implementation("io.ktor:ktor-client-content-negotiation:3.2.0")
    implementation("io.ktor:ktor-serialization-kotlinx-json:3.2.0")
}
```

### API Key
Gunakan **BuildConfig** atau **remote config**: jangan pernah hardcode API key!

## Implementasi Ktor Client

```kotlin
object GeminiClient {
    private const val BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    private val client = HttpClient(OkHttp) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 60_000
        }
    }
    
    suspend fun generateResponse(prompt: String): Result<GeminiResponse> {
        return try {
            val response = client.post(BASE_URL) {
                parameter("key", BuildConfig.GEMINI_API_KEY)
                contentType(ContentType.Application.Json)
                setBody(GeminiRequest(
                    contents = listOf(Content(
                        role = "user",
                        parts = listOf(Part(text = prompt))
                    ))
                ))
            }
            Result.success(response.body())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

## Fitur Canggih: Multimodal Input

Gemini 2.0 mendukung multimodal, teks + gambar:

```kotlin
suspend fun analyzeImage(imageBitmap: Bitmap, prompt: String): GeminiResponse {
    val base64Image = imageBitmap.toBase64()
    return client.post(BASE_URL) {
        parameter("key", BuildConfig.GEMINI_API_KEY)
        setBody(GeminiMultimodalRequest(
            contents = listOf(MultimodalContent(
                parts = listOf(
                    Part(text = prompt),
                    Part(inlineData = InlineData(
                        mimeType = "image/jpeg",
                        data = base64Image
                    ))
                )
            ))
        ))
    }.body()
}
```

## Security Best Practice

1. **API Key Protection**: jangan hardcode, gunakan BuildConfig atau proxy backend
2. **Rate Limiting**: implementasikan throttling untuk mencegah abuse
3. **Content Filtering**: gunakan safety settings Gemini untuk konten sensitif

## Memilih Model Gemini yang Tepat

Nama model di Gemini API berubah cepat, jadi jangan hardcode model lama. Berdasarkan dokumentasi resmi pada Oktober 2026, model Flash seri terbaru tersedia dengan id seperti `gemini-3.8-flash` sebagai default Flash, sementara `gemini-3.1-pro-preview` ditujukan untuk task reasoning kompleks. Keluarga 2.5 masih dilayani, tetapi Google membatasi aksesnya ke akun yang sudah pernah menggunakannya, sehingga proyek baru sebaiknya memakai model seri terbaru. Cara paling aman untuk mengetahui daftar model adalah memanggil endpoint listing:

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" | grep '"name":'
```

Alias seperti `gemini-flash-latest` juga tersedia jika Anda ingin selalu mengikuti rilis Flash terbaru tanpa mengubah kode.

Catatan penting soal endpoint: Google memperkenalkan **Interactions API** di path `/v1beta/interactions` dan menjadikannya antarmuka default untuk proyek baru sejak Juni 2026, sedangkan `generateContent` yang dipakai contoh di atas tetap didukung penuh. Jika memulai modul baru, pertimbangkan Interactions API; jika aplikasi sudah berjalan di `generateContent`, tidak ada urgensi migrasi.

## Structured Output: JSON yang Deterministik

Kalau output AI mau masuk ke database atau di-parse lebih lanjut, jangan andalkan teks bebas. Kirim `responseMimeType` bernilai `application/json` beserta `responseSchema` di dalam `generationConfig`. Model akan membatasi output ke skema yang Anda definisikan.

```kotlin
val body = mapOf(
    "contents" to listOf(mapOf(
        "parts" to listOf(mapOf("text" to prompt))
    )),
    "generationConfig" to mapOf(
        "responseMimeType" to "application/json",
        "responseSchema" to mapOf(
            "type" to "object",
            "properties" to mapOf(
                "judul" to mapOf("type" to "string"),
                "ringkasan" to mapOf("type" to "string"),
                "skor" to mapOf("type" to "integer")
            ),
            "required" to listOf("judul", "ringkasan", "skor")
        )
    )
)
```

Structured output juga bisa distreaming: chunk yang datang adalah JSON parsial yang valid dan tinggal digabung sampai objek akhir utuh. Untuk Android, ini berarti UI bisa mulai memproses data saat respons masih berjalan, bukan menunggu semua token selesai.

## System Instruction dan Parameter Generasi

Selain prompt user, Anda bisa menetapkan `systemInstruction` untuk mengatur persona dan batasan perilaku model, misalnya "jawab singkat dalam Bahasa Indonesia". Parameter lain di `generationConfig`: `temperature`, `topP`, `topK`, `maxOutputTokens`. Untuk model Gemini 3 ada parameter `thinking_level` (misalnya `low` atau `high`) yang mengontrol kedalaman penalaran internal sebelum jawaban keluar; gunakan `low` untuk latensi rendah dan `high` untuk task sulit.

Safety setting tetap perlu diaktifkan meski audiens internal. Kategori yang tersedia antara lain `HARM_CATEGORY_HARASSMENT`, `HARM_CATEGORY_HATE_SPEECH`, `HARM_CATEGORY_SEXUALLY_EXPLICIT`, dan `HARM_CATEGORY_DANGEROUS_CONTENT`, dengan threshold dari `BLOCK_NONE` sampai `BLOCK_LOW_AND_ABOVE`. Sebagian kategori juga menerima nilai `OFF` di endpoint tertentu.

## Streaming Response dengan SSE

Untuk pengalaman chat yang terasa responsif, pakai streaming. Tambahkan parameter `alt=sse` pada URL `streamGenerateContent`, lalu konsumsi baris per baris:

```kotlin
suspend fun streamResponse(prompt: String, onChunk: (String) -> Unit) {
    client.preparePost("$BASE_URL:streamGenerateContent") {
        parameter("key", BuildConfig.GEMINI_API_KEY)
        parameter("alt", "sse")
        contentType(ContentType.Application.Json)
        setBody(GeminiRequest(listOf(Content("user", listOf(Part(text = prompt))))))
    }.execute { response ->
        val channel = response.bodyAsChannel()
        while (!channel.isClosedForRead) {
            val line = channel.readUTF8Line() ?: continue
            if (line.startsWith("data:")) {
                val json = Json.parseToJsonElement(line.removePrefix("data:").trim())
                val text = json.jsonObject["candidates"]?.jsonArray
                    ?.firstOrNull()?.jsonObject?.get("content")
                    ?.jsonObject?.get("parts")?.jsonArray
                    ?.firstOrNull()?.jsonObject?.get("text")?.jsonPrimitive?.content
                text?.let(onChunk)
            }
        }
    }
}
```

Tampilkan tiap chunk langsung ke UI lewat `MutableStateFlow<String>` yang diobserve oleh composable chat, sehingga teks muncul bertahap seperti mesin tik.

## Function Calling: Menghubungkan Model ke Fitur Aplikasi

Function calling dipakai ketika model perlu "meminta" aplikasi melakukan sesuatu sebelum menjawab, misalnya mencari pesanan atau mengecek stok. Alurnya: deklarasikan tools, kirim prompt, model membalas dengan `functionCall`, aplikasi mengeksekusi fungsi itu sendiri, lalu kirim hasilnya kembali sebagai `functionResponse`.

```kotlin
val tools = listOf(mapOf(
    "functionDeclarations" to listOf(mapOf(
        "name" to "cari_pesanan",
        "description" to "Cari status pesanan berdasarkan nomor invoice",
        "parameters" to mapOf(
            "type" to "object",
            "properties" to mapOf("invoice" to mapOf("type" to "string")),
            "required" to listOf("invoice")
        )
    ))
))
```

Perlu dibedakan dari structured output: structured output memformat jawaban final, function calling untuk mengambil aksi di tengah percakapan. Untuk model Gemini 3, keduanya bahkan bisa digabung dengan tool bawaan seperti Google Search grounding, URL Context, dan Code Execution.

## Rate Limiting, Retry, dan Kontrol Biaya

API publik punya kuota per menit. Bungkus pemanggilan dengan `Semaphore` untuk membatasi request paralel, dan implementasikan exponential backoff untuk HTTP 429 dan 503. Di Android, request yang gagal sementara sebaiknya diantrikan lewat `WorkManager` supaya tetap jalan walau app ditutup.

Kontrol biaya dimulai dari token. Setiap response mengandung `usageMetadata` dengan jumlah token prompt dan output. Simpan angka ini untuk dashboard biaya internal. Ada juga endpoint `countTokens` untuk menghitung token prompt sebelum request dikirim, berguna untuk memotong konteks percakapan panjang secara proaktif.

## Error Handling yang Jelas

Jangan tangkap semua exception jadi satu pesan generik. Periksa `promptFeedback.blockReason` untuk konten yang diblok safety filter, dan `finishReason` pada candidate (`STOP`, `MAX_TOKENS`, `SAFETY`, `RECITATION`) untuk menentukan apakah jawaban terpotong atau ditolak. Dengan begitu pesan error di UI bisa informatif, misalnya "respons terpotong karena batas token, coba pertanyaan lebih pendek" alih-alih "terjadi kesalahan".

## Alternatif Resmi: Google AI Client SDK dan Firebase AI Logic

Selain memanggil REST API manual lewat Ktor, Google menyediakan SDK resmi. Untuk Android, Firebase AI Logic (`com.google.firebase:firebase-ai`) mengemas akses Gemini dengan manajemen kunci, logging, dan integrasi App Check untuk membatasi penyalahgunaan. Alternatifnya Google AI Client SDK (`com.google.ai.client.generativeai`) untuk akses langsung ke Gemini API tanpa backend Firebase. Keduanya cocok dipakai kalau tim tidak ingin memelihara serialisasi request dan response sendiri, sementara pendekatan Ktor manual tetap menang soal kontrol penuh atas payload dan ketahanan terhadap perubahan SDK.

## Kesimpulan

Integrasi Gemini AI ke Android membuka potensi fitur yang luar biasa. Dengan Ktor Client dan arsitektur yang clean, Anda bisa membangun AI-powered app dengan performa tinggi.
