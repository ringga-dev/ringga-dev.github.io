---
title: "Modern CSS 2026: Container Queries, :has(), dan View Transitions"
description: "Tahun 2026 menandai kedewasaan CSS sebagai bahasa layout mandiri. Pelajari fitur baru yang mengubah cara kita membangun UI responsif tanpa JavaScript."
date: "2026-08-19"
author: "Ringga Septia Pribadi"
tags: ["CSS", "Web Development", "Frontend", "Container Queries", "Responsive Design"]
category: "Web Development"
image: "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800&q=80"
---

## Pendahuluan

Selama bertahun-tahun, responsivitas di web bergantung pada satu pertanyaan: **seberapa lebar viewport browser?** Media query `@media (max-width: 768px)` memaksa kita berpikir tentang perangkat, bukan tentang konteks komponen. Di tahun 2026, paradigma itu runtuh. CSS kini memiliki kemampuan layout yang dulunya mustahil tanpa JavaScript: *container queries*, pseudo-class `:has()`, *cascade layers*, dan *view transitions*.

Artikel ini membahas fitur modern CSS yang sudah didukung semua browser utama per 2026, lengkap dengan contoh kode nyata dan alasan mengapa ini mengurangi beban JavaScript di aplikasi web Anda.

---

## 1. Container Queries: Responsif Berdasarkan Komponen

Container query memungkinkan suatu elemen menyesuaikan gayanya berdasarkan **lebar kontainernya sendiri**, bukan lebar viewport. Ini kruscial untuk komponen yang bisa muncul di sidebar sempit, kolom tengah, maupun layout penuh.

```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  gap: 1rem;
}

@container card (max-width: 400px) {
  .card {
    grid-template-columns: 1fr;
  }
  .card__title {
    font-size: 1.1rem;
  }
}
```

Keuntungan utama: komponen `.card` bisa dipakai ulang di mana saja tanpa perlu tahu di layout mana ia berada. Tidak ada lagi *magic breakpoint* global yang rapuh.

### Jebakan yang Sering Dilupakan

Ada tiga hal yang biasanya bikin container query "tidak jalan":

1. **`container-type` tidak diwarisi**. Ancestor terdekat dengan `container-type` yang valid itulah containment context-nya. Kalau kamu lupa menaruhnya di wrapper, query akan naik lebih jauh ke atas dan hasilnya membingungkan.
2. **`container-type: size` menambah containment di kedua axis**. Ini membuat browser boleh mengabaikan ukuran konten saat menghitung layout, dan kalau di dalamnya ada elemen yang mengikuti aliran normal, bisa muncul overflow. Untuk kasus umum, `inline-size` lebih aman.
3. **Container tidak bisa query dirinya sendiri**. Elemen yang menangani style dan elemen yang jadi container harus berbeda.

Selain size queries, ada **style queries** yang menanyakan nilai custom property atau computed style:

```css
.theme-wrapper {
  container-type: inline-size;
  container-name: theme;
  --variant: compact;
}

@container theme style(--variant: compact) {
  .card__meta {
    display: none;
  }
}
```

Style queries menjadi Baseline pada Mei 2026, sehingga polanya aman dipakai untuk varian komponen tanpa harus menambahkan class tambahan di setiap tempat.

---

## 2. :has(), Selector "Parent" yang Dinantikan

Selama satu dekade, CSS tidak bisa memilih elemen berdasarkan anaknya. `:has()` mengubah itu. Ia sering disebut "selector parent" karena menargetkan elemen yang **memiliki** anak tertentu.

```css
/* Style form hanya jika ada input invalid di dalamnya */
form:has(input:invalid) {
  border-color: #e11d48;
}

/* Tampilkan badge hanya saat card punya gambar */
.card:has(img) .card__badge {
  display: inline-block;
}
```

Dengan `:has()`, banyak pola interaktif seperti *accordion*, validasi form real-time, hingga conditional styling bisa dilakukan murni CSS tanpa listener `change` atau `input` di JavaScript.

### Sisi Performa

`:has()` dievaluasi saat setiap perubahan DOM yang relevan, jadi selector yang terlalu luas di dokumen besar punya biaya. Praktik yang wajar:

- Sebisa mungkin berikan penanda kelas atau atribut, misalnya `.form:has(> .field input:invalid)` daripada `*:has(input)`.
- Hindari menaruh `:has()` di selektor yang cocok dengan ribuan elemen pada halaman panjang.
- Ingat bahwa `:has()` menerima relative selector di dalamnya, jadi `:has(> img)`, `:has(+ p)`, dan `:has(~ ul)` semuanya valid.

Kombinasi yang berguna untuk state form tanpa JS:

```css
fieldset:has(input:placeholder-shown) .field__hint {
  display: none;
}

fieldset:has(input:user-invalid) {
  --border: #e11d48;
}
```

`user-invalid` hanya aktif setelah pengguna benar-benar berinteraksi dengan field, sehingga form tidak langsung merah saat halaman dimuat.

---

## 3. Cascade Layers (@layer): Mengatur Spesifisitas

Konflik spesifisitas adalah mimpi buruk CSS. `@layer` memberi kita kontrol eksplisit atas urutan kaskade, sehingga utility class tidak lagi kalah oleh selektor tak terduga.

```css
@layer base, components, utilities;

@layer base {
  h1 { font-size: 2rem; }
}

@layer utilities {
  .text-sm { font-size: 0.875rem; }
}
```

Urutan deklarasi layer di baris pertama menentukan prioritas: `utilities` menang atas `base` meski spesifisitasnya lebih rendah. Ini menyelamatkan tim dari !important war yang tak berujung.

### Pola Struktur Layer yang Terbukti

Susunan yang dipakai banyak design system:

```css
@layer reset, tokens, base, layout, components, utilities, overrides;
```

Beberapa aturan yang perlu diingat:

- Style di luar `@layer` apa pun punya prioritas lebih tinggi daripada style di dalam layer mana pun. Layer bukan cara untuk mengalahkan inline style, tapi cara untuk mengatur urutan antar stylesheet.
- Layer bisa bersarang, dan nama layer di dalam file terpisah tetap mengacu pada layer yang sama asalkan namanya identik.
- Import CSS pihak ketiga bisa dimasukkan ke layer terendah supaya mudah ditimpa: `@import url("vendor.css") layer(vendor);`

Kalau tim memakai Tailwind, layer membuat konflik dengan komponen kustom jauh lebih mudah dirawat karena utility class tidak lagi perlu memperbesar spesifisitas.

---

## 4. View Transitions API: Animasi Halaman Tanpa Flash

Dulu pindah halaman atau mengubah DOM besar butuh library animasi berat. View Transitions API, kini tersedia di CSS plus sedikit JS panggilan, memungkinkan transisi halus antar state.

```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}
```

```js
document.startViewTransition(() => {
  updateDOM();
});
```

Hasilnya: navigasi terasa seperti aplikasi native tanpa *flash* putih atau *layout jump*. Di Nuxt dan framework SSG modern, ini bisa diintegrasikan sebagai progressive enhancement.

Ada dua jenis yang perlu dibedakan:

- **Same-document view transitions**, untuk perubahan state di satu halaman. Ini sudah Baseline sejak Oktober 2025 (Chrome 111, Safari 18, Firefox menyusul belakangan di 144), jadi paling aman dipakai.
- **Cross-document view transitions**, untuk navigasi antar halaman biasa (MPA). Statusnya masih limited: Chrome 126 dan Safari 18.2 mendukung, Firefox belum sama sekali.

### Memberi Nama Elemen agar Ter-animasi

Secara default hanya snapshot root yang ikut transisi. Untuk mengubah thumbnail menjadi gambar besar, beri nama elemennya:

```css
.product__thumb {
  view-transition-name: product-hero;
}

.product__detail-hero {
  view-transition-name: product-hero;
}
```

```css
@keyframes expand-from-thumb {
  from { transform: scale(0.3); }
  to   { transform: scale(1); }
}

::view-transition-old(product-hero),
::view-transition-new(product-hero) {
  animation-duration: 0.35s;
  animation-timing-function: cubic-bezier(0.2, 0, 0, 1);
}
```

Satu nama hanya boleh dipakai satu elemen pada satu waktu. Kalau ada daftar 20 produk dan semuanya bernama sama, transisi akan dibatalkan browser. Solusinya menamai hanya elemen yang benar-benar terlihat.

---

## 5. Fitur Pendukung Lain yang Layak Dipakai

### interpolate-size dan animasi ke height: auto

Selama ini menganimasi `height: auto` mustahil dan orang memakai trik `max-height: 9999px`. Properti `interpolate-size: allow-keywords` mengizinkan browser menghitung nilai `auto` sebagai titik animasi:

```css
:root {
  interpolate-size: allow-keywords;
}

.collapse {
  overflow: hidden;
  transition: height 0.3s ease;
  height: 3rem;
}

.collapse[data-open="true"] {
  height: auto;
}
```

Dukungannya masih terbatas di Chromium, jadi bungkus dengan `@supports`:

```css
@supports (interpolate-size: allow-keywords) {
  :root { interpolate-size: allow-keywords; }
  /* versi CSS murni di sini */
}
```

### text-wrap: balance dan pretty

`text-wrap: balance` sudah Baseline luas sejak Maret 2024 dan sangat berguna untuk heading, caption, dan blockquote. Browser melakukan pencarian biner untuk lebar terkecil yang tidak menambah baris, dan biayanya dibatasi dengan hanya menerapkan pada jumlah baris terbatas (enam baris di Chromium, sepuluh baris di Firefox). Jangan pernah menerapkannya ke seluruh paragraf tubuh artikel.

```css
h1, h2, h3, h4, h5, h6 {
  text-wrap: balance;
}

.card__caption {
  text-wrap: pretty;   /* menghindari orphan di baris terakhir */
}
```

`pretty` lebih baru dan belum didukung Firefox, jadi perlakukan sebagai enhancement.

### Scroll-driven animations

`animation-timeline: view()` dan `scroll()` memungkinkan animasi bergantung pada posisi scroll, tanpa `IntersectionObserver` atau listener scroll:

```css
.progress-bar {
  transform-origin: left;
  animation: grow linear both;
  animation-timeline: scroll(root block);
}

@keyframes grow {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```

Perlu dicatat jujur: dukungannya belum merata. Chrome mengirim sejak 115, Safari sejak 26 (September 2025), dan Firefox belum menyediakannya, bahkan masih berbendera. Kalau efeknya dekoratif, versi statis sebagai fallback sudah wajar. Kalau efeknya fungsional, jangan jadikan ini satu-satunya implementasi.

---

## Perbandingan Pendekatan

| Fitur | Pendekatan Lama (JS-heavy) | Modern CSS 2026 |
|-------|----------------------------|-----------------|
| Layout responsif | Resize observer + JS | Container queries |
| Conditional styling | Event listener + class toggle | `:has()` |
| Prioritas style | `!important` & spesifisitas | `@layer` eksplisit |
| Transisi halaman | Library animasi | View Transitions API |
| Tooltip positioning | Floating UI / Popper.js | Anchor positioning |
| Animate to height auto | Trik `max-height` | `interpolate-size` |
| Scroll animation | IntersectionObserver | Scroll-driven animations |

Anchor positioning layak disebut terpisah. Pola dasarnya:

```css
.tooltip-trigger {
  anchor-name: --trigger;
}

.tooltip {
  position: absolute;
  position-anchor: --trigger;
  position-area: block-start;
  position-try-fallbacks: flip-block, block-end;
}
```

Browser menjaga elemen tetap ter-anchor saat scroll, resize, dan layout shift, plus bisa membalik posisi otomatis lewat `position-try`. Fitur ini masuk Baseline Januari 2026, tapi bagian lanjutan seperti `position-try` masih bergulir bertahap, jadi siapkan fallback posisi statis untuk browser yang belum mendukung.

---

## Dampak ke Performa

Menggeser logika layout ke CSS membawa manfaat nyata:

- **Bundle JS lebih kecil**, tidak perlu polyfill atau library observer.
- **Paint lebih cepat**, browser mengoptimalkan style komputasi di main thread.
- **Aksesibilitas lebih baik**, perilaku responsif konsisten tanpa *hydration* error.

Untuk situs statis seperti portfolio Nuxt 4, ini berarti halaman ringan yang tetap interaktif.

Ada satu manfaat yang sering tidak dihitung: **konsistensi antar developer**. Dengan `@layer`, dua orang yang mengerjakan file CSS berbeda tidak lagi saling menimpa gaya secara diam-diam, karena urutan prioritas sudah ditetapkan di satu tempat.

Strategi adopsi yang masuk akal bagi tim yang sudah punya codebase lama:

1. Tambahkan deklarasi `@layer` di entry CSS tanpa memindahkan kode dulu. Ini sudah mengubah urutan prioritas dan biasanya langsung menyelesaikan konflik `!important`.
2. Ganti satu pola JS sekaligus, misalnya listener resize untuk layout card, dengan container query.
3. Baru sentuh animasi halaman, karena itu yang paling terlihat dampaknya pada UX.

---

## Kesimpulan

CSS di 2026 bukan lagi "pelengkap" HTML, ia adalah mesin layout mandiri. Container queries, `:has()`, cascade layers, dan view transitions menyingkirkan banyak JavaScript yang selama ini kita tulis hanya untuk membuat UI yang responsif dan mulus. Mulailah mengadopsi fitur-fitur ini; browser modern sudah siap, dan pengguna Anda akan merasakan perbedaannya melalui performa yang lebih baik.

Satu prinsip yang perlu dipegang: bedakan mana yang sudah Baseline dan mana yang masih bergulir bertahap. Container query, `:has()`, `@layer`, dan `text-wrap: balance` bisa dipakai langsung. View transitions dan anchor positioning aman sebagai progressive enhancement. Scroll-driven animations dan `interpolate-size` masih perlu `@supports` dan fallback yang jelas.
