---
title: "Nuxt 4: Evolusi Framework Vue untuk Aplikasi Modern"
description: "Panduan lengkap migrasi ke Nuxt 4 — fitur unggulan seperti nitro engine, hybrid rendering, dan bagaimana Nuxt 4 mengatasi bottleneck performa aplikasi Vue."
date: "2026-07-02"
author: "Ringga Septia Pribadi"
tags: ["Nuxt", "Vue", "Web Development", "Frontend"]
category: "Web Development"
image: "https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&q=80"
---

## Pendahuluan

Nuxt 4 telah dirilis dan membawa perubahan besar dalam ekosistem Vue. Framework ini tidak hanya update minor; inti framework disusun ulang demi performa dan developer experience yang lebih baik. Dirilis secara stabil pada Juli 2025, Nuxt 4.0 digambarkan tim pengembangnya sebagai major release yang fokus pada stabilitas, bukan pada penambahan fitur besar. Sebagian besar peningkatan performa justru sudah dikirim lebih dulu lewat rilis minor Nuxt 3, dan yang dilakukan di versi 4 adalah mengubah beberapa default agar perilaku framework lebih konsisten.

Ada empat pilar utama perubahan: struktur direktori baru dengan folder `app/`, data fetching yang lebih pintar, dukungan TypeScript yang dipisah per konteks, dan CLI serta dev server yang lebih cepat. Artikel ini membahas masing-masing beserta implikasinya untuk proyek nyata.

## Struktur Direktori Baru

Perubahan yang paling terlihat adalah kode aplikasi kini berada di dalam direktori `app/` secara default.

```
my-nuxt-app/
├─ app/
│  ├─ assets/
│  ├─ components/
│  ├─ composables/
│  ├─ layouts/
│  ├─ middleware/
│  ├─ pages/
│  ├─ plugins/
│  ├─ utils/
│  ├─ app.vue
│  ├─ app.config.ts
│  └─ error.vue
├─ content/
├─ public/
├─ shared/
├─ server/
└─ nuxt.config.ts
```

Tujuannya bukan estetika. Dengan memisahkan kode aplikasi dari `node_modules/` dan `.git/`, file watcher bekerja lebih cepat karena tidak perlu menyapu direktori besar tersebut setiap kali ada perubahan. IDE juga mendapat konteks yang lebih jelas apakah kamu sedang mengedit kode client atau kode server.

Pemisahan konfigurasi memengaruhi resolusi path. Secara default direktori sumber aplikasi menjadi `app/`, sementara direktori server tetap berada di root project. Karena itu `server/` dan `public/` tidak ikut berpindah ke dalam `app/`. Kalau kamu tidak mau migrasi, Nuxt mendeteksi struktur lama secara otomatis dan tetap bekerja seperti sebelumnya, sehingga upgrade bisa dilakukan bertahap.

## Hybrid Rendering

Nuxt 4 menggunakan route rules untuk memutuskan strategi render per path. Ini berarti satu aplikasi bisa memakai beberapa strategi sekaligus, bukan dipaksa memilih satu mode untuk seluruh situs.

```typescript
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/blog/**': { isr: 3600 },
    '/dashboard/**': { ssr: true },
    '/api/**': { cors: true }
  }
})
```

Penjelasan tiap strategi:

- **`prerender: true`** menghasilkan HTML statis pada waktu build. Halaman disajikan dari CDN, sehingga tidak ada beban server per request dan time to first byte sangat rendah. Cocok untuk landing page dan halaman yang jarang berubah.
- **`isr: 3600`** melakukan incremental static regeneration dengan masa berlaku 3600 detik. Request pertama setelah masa berlaku berakhir memicu regenerasi di background, sementara respons lama tetap dikirim ke pengunjung. Blog mendapat keuntungan terbesar dari mode ini: konten baru terbit tanpa rebuild penuh.
- **`ssr: true`** merender di server pada setiap request. Wajib untuk halaman yang menampilkan data spesifik per pengguna, seperti dashboard.
- **`cors: true`** menambahkan header CORS pada route yang bersangkutan, praktis untuk endpoint yang dikonsumsi aplikasi mobile.

Ada juga opsi `swr` (stale while revalidate) dan `redirect` yang berguna untuk migrasi URL. Yang perlu dihindari adalah mencampur `prerender` dengan route yang bergantung pada data per pengguna, karena HTML yang di-cache akan salah ditampilkan ke pengguna lain.

## Nitro sebagai Server Engine

Nuxt memakai Nitro sebagai server engine-nya. Penting untuk diluruskan soal versi: Nuxt 3 dan Nuxt 4 berjalan di atas Nitro v2 (paket `nitropack`) yang memakai h3 v1. Nitro v3 bersama h3 v2 direncanakan hadir di Nuxt 5. Jadi jangan salah menyebut Nuxt 4 sudah membawa Nitro 3.

Kemampuan Nitro yang relevan untuk keputusan arsitektur:

- **Target deployment yang banyak.** Satu basis kode bisa dibangun untuk Node.js, Deno, Bun, Cloudflare Workers, Vercel, dan Netlify.
- **Serverless tanpa konfigurasi tambahan.** Nitro menghasilkan handler yang sesuai dengan format tiap platform.
- **Code splitting otomatis.** Chunk dimuat secara async sehingga bundle awal lebih kecil.
- **Hybrid mode.** Kombinasi halaman statis dan route serverless dalam satu build.
- **Storage layer terpadu.** Abstraksi untuk key-value store, filesystem, dan driver lain lewat helper penyimpanan bawaan Nitro.

Karena API server-nya portable, penulisan endpoint sebaiknya mengimpor dari `nuxt/server` alih-alih langsung dari h3 atau nitropack. Sejak Nuxt 4.6, file yang hanya mengimpor dari `nuxt/server` bisa berjalan di Nitro v2 maupun Nitro v3, sehingga jalur upgrade ke Nuxt 5 menjadi lebih mulus.

```typescript
// server/api/posts/[id].get.ts
import { defineEventHandler, getRouterParam } from 'nuxt/server'

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  return { id, title: 'Contoh post' }
})
```

Pola `[id]` pada nama file otomatis dipetakan menjadi route parameter oleh Nitro, tanpa perlu mendaftarkan route secara manual.

## Data Fetching yang Lebih Cerdas

Bagian data layer mengalami reorganisasi besar. Beberapa perilaku barunya:

- **Shared refs dengan key yang sama.** Semua pemanggilan composable data fetching dengan key identik kini berbagi referensi `data`, `error`, dan `status` yang sama. Konsekuensinya, opsi seperti `deep`, `transform`, `pick`, dan `getCachedData` tidak boleh bertentangan antar pemanggilan yang memakai key yang sama.
- **Cleanup otomatis.** Saat komponen unmount, subscription dibersihkan sehingga tidak ada memory leak dari komponen yang sudah tidak dirender.
- **Reactive keys.** Mengubah key secara reaktif otomatis memicu refetch.

```vue
<script setup lang="ts">
const page = ref(1)
const { data, status, error } = await useAsyncData(
  () => `posts-${page.value}`,
  () => $fetch(`/api/posts?page=${page.value}`)
)
</script>
```

Pakai function sebagai key agar key berubah mengikuti `page.value`. Kalau key ditulis sebagai string statis `posts`, perubahan halaman tidak akan memicu request baru.

## Dukungan TypeScript yang Dipisah

Nuxt 4 membuat proyek TypeScript terpisah untuk kode app, kode server, folder `shared/`, dan kode konfigurasi. Hasilnya autocompletion lebih akurat dan error yang muncul lebih mudah dipahami karena tiap konteks punya aturan tipe sendiri. Di proyek baru kamu hanya perlu satu `tsconfig.json` di root.

Ini juga bagian yang paling sering mengejutkan saat upgrade: masalah tipe yang sebelumnya tersembunyi bisa muncul setelah migrasi. Siapkan waktu untuk memperbaiki error yang dilaporkan type checker setelah upgrade selesai.

## CLI dan Development Server yang Lebih Cepat

Peningkatan di area ini tidak terlihat dari luar, tapi dirasakan setiap hari:

- **Cold start lebih cepat.** Waktu boot dev server berkurang.
- **Node.js compile cache.** V8 compile cache dipakai ulang secara otomatis.
- **Native file watching.** Memakai API `fs.watch` sehingga penggunaan sumber daya sistem lebih rendah.
- **Komunikasi berbasis socket.** CLI dan Vite dev server berkomunikasi lewat internal socket, bukan network port, yang mengurangi overhead terutama di Windows.

Ekosistem Vue di sekitarnya ikut mendukung. Vue 3.5 menstabilkan reactive props destructure, jadi variabel hasil destructure dari macro definisi props bersifat reaktif tanpa perlu helper konversi ref manual, dan refactor sistem reaktivitas di versi tersebut mengurangi penggunaan memori secara signifikan. Di sisi UI, Nuxt UI v3 dibangun ulang di atas Reka UI dan Tailwind CSS dengan fokus pada aksesibilitas, menyediakan lebih dari seratus komponen siap pakai.

## Migrasi dari Nuxt 3

Proses upgrade dirancang agar seminimal mungkin, karena sebagian besar breaking change sudah bisa diuji lewat compatibility flag selama lebih dari setahun.

```bash
npx nuxt upgrade --dedupe
```

Flag `--dedupe` ikut membersihkan lockfile sehingga dependency ekosistem unjs ikut ter-update. Kalau ingin otomasi lebih lanjut, tersedia migration recipe berbasis codemod:

```bash
npx codemod@latest nuxt/4/migration-recipe
```

Langkah manual yang biasanya masih perlu dilakukan:

1. Pindahkan kode aplikasi ke direktori `app/`, atau biarkan Nuxt memakai struktur lama kalau memang belum siap.
2. Pastikan tidak ada `useAsyncData` dengan key sama tapi opsi yang bertentangan.
3. Hapus sisa dependensi pada Nuxt 2 compatibility di `@nuxt/kit` kalau kamu menulis modul.
4. Perbaiki error tipe yang muncul akibat pemisahan proyek TypeScript.

Bila ada modul pihak ketiga yang belum kompatibel, sebagian perilaku lama bisa dikembalikan lewat opsi konfigurasi sementara, sehingga migrasi bisa dilakukan bertahap per modul.

## Kapan Layak Upgrade

Upgrade masuk akal kalau dev server terasa lambat karena banyaknya file di root proyek, atau kalau kamu memang butuh hybrid rendering untuk menekan biaya server. Kalau proyek berjalan stabil dan tim sedang fokus pada fitur, tidak ada urgensi: Nuxt 3 tetap menerima maintenance update termasuk backport beberapa fitur dari Nuxt 4.

## Kesimpulan

Nuxt 4 adalah lompatan besar untuk Vue ecosystem. Hybrid rendering lewat route rules, struktur proyek yang lebih rapi, dan data fetching yang lebih konsisten menjadikannya pilihan utama untuk aplikasi web modern. Kuncinya bukan mengubah semuanya sekaligus: adopsi struktur baru, manfaatkan route rules untuk optimasi, dan rapikan type-safety satu konteks pada satu waktu.
