---
title: "Integrasi Google Gemini AI ke Aplikasi Android: Panduan Lengkap"
description: "Tutorial step-by-step mengintegrasikan Gemini AI API ke aplikasi Android menggunakan Ktor Client, dari setup hingga implementasi fitur AI canggih."
date: "2026-06-22"
author: "Ringga Septia Pribadi"
tags: ["Gemini", "AI", "Android", "Kotlin", "Ktor"]
category: "AI & Machine Learning"
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=2070&auto=format&fit=crop"
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
Gunakan **BuildConfig** atau **remote config** — jangan pernah hardcode API key!

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

Gemini 2.0 mendukung multimodal — teks + gambar:

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

1. **API Key Protection** — jangan hardcode, gunakan BuildConfig atau proxy backend
2. **Rate Limiting** — implementasikan throttling untuk mencegah abuse
3. **Content Filtering** — gunakan safety settings Gemini untuk konten sensitif

## Kesimpulan

Integrasi Gemini AI ke Android membuka potensi fitur yang luar biasa. Dengan Ktor Client dan arsitektur yang clean, Anda bisa membangun AI-powered app dengan performa tinggi.
