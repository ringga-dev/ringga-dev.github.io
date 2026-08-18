---
title: "Modern CSS 2026: Container Queries, :has(), dan View Transitions"
description: "Tahun 2026 menandai kedewasaan CSS sebagai bahasa layout mandiri. Pelajari fitur baru yang mengubah cara kita membangun UI responsif tanpa JavaScript."
date: "2026-08-19"
author: "Ringga Septia Pribadi"
tags: ["CSS", "Web Development", "Frontend", "Container Queries", "Responsive Design"]
category: "Web Development"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=2070&auto=format&fit=crop"
---

## Pendahuluan

Selama bertahun-tahun, responsivitas di web bergantung pada satu pertanyaan: **seberapa lebar viewport browser?** Media query `@media (max-width: 768px)` memaksa kita berpikir tentang perangkat, bukan tentang konteks komponen. Di tahun 2026, paradigma itu runtuh. CSS kini memiliki kemampuan layout yang dulunya mustahil tanpa JavaScript: *container queries*, pseudo-class `:has()`, *cascade layers*, dan *view transitions*.

Artikel ini membahas empat fitur modern CSS yang sudah didukung semua browser utama per 2026, lengkap dengan contoh kode nyata dan alasan mengapa ini mengurangi beban JavaScript di aplikasi web Anda.

---

## 1. Container Queries: Responsif Berdasarkan Komponen

Container query memungkinkan suatu elemen menyesuaikan gayanya berdasarkan **lebar kontainernya sendiri**, bukan lebar viewport. Ini krusial untuk komponen yang bisa muncul di sidebar sempit, kolom tengah, maupun layout penuh.

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

---

## 2. :has() — Selector "Parent" yang Dinantikan

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

Dengan `:has()`, banyak pola interaktif — seperti *accordion*, validasi form real-time, hingga conditional styling — kini bisa dilakukan murni CSS tanpa listener `change` atau `input` di JavaScript.

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

---

## 4. View Transitions API: Animasi Halaman Mulus

Dulu pindah halaman atau mengubah DOM besar butuh library animasi berat. View Transitions API — kini tersedia di CSS + sedikit JS panggilan — memungkinkan transisi halus antar state.

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

---

## Perbandingan Pendekatan

| Fitur | Pendekatan Lama (JS-heavy) | Modern CSS 2026 |
|-------|----------------------------|-----------------|
| Layout responsif | Resize observer + JS | Container queries |
| Conditional styling | Event listener + class toggle | `:has()` |
| Prioritas style | `!important` & spesifisitas | `@layer` eksplisit |
| Transisi halaman | Library animasi | View Transitions API |

---

## Dampak ke Performa

Menggeser logika layout ke CSS membawa manfaat nyata:

- **Bundle JS lebih kecil** — tidak perlu polyfill atau library observer.
- **Paint lebih cepat** — browser mengoptimalkan style komputasi di main thread渲染.
- **Aksesibilitas lebih baik** — perilaku responsif konsisten tanpa *hydration* error.

Untuk situs statis seperti portfolio Nuxt 4, ini berarti halaman ringan yang tetap interaktif.

---

## Kesimpulan

CSS di 2026 bukan lagi "pelengkap" HTML — ia adalah mesin layout mandiri. Container queries, `:has()`, cascade layers, dan view transitions menyingkirkan banyak JavaScript yang selama ini kita tulis hanya untuk membuat UI yang responsif dan mulus. Mulailah mengadopsi keempat fitur ini; browser modern sudah siap, dan pengguna Anda akan merasakan perbedaannya melalui performa yang lebih baik.
