---
title: "Local-First Architecture 2026: Aplikasi Offline-First yang Tetap Real-Time"
description: "Mengapa local-first architecture menjadi tren arsitektur terpenting 2026 — CRDT, sync engine seperti ElectricSQL dan PowerSync, serta cara membangun aplikasi yang cepat, offline-ready, dan tetap sinkron real-time."
date: "2026-08-06"
author: "Ringga Septia Pribadi"
tags: ["Local-First", "Web Development", "CRDT", "Offline-First", "Sync"]
category: "Web Development"
image: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80"
---

## Pendahuluan

Selama satu dekade terakhir, hampir semua aplikasi web dibangun dengan satu asumsi: koneksi internet selalu ada. Data tinggal di server, UI menunggu respons API, dan pengguna dianggap tidak akan pernah membuka aplikasi di kereta bawah tanah atau area dengan sinyal buruk. Di tahun 2026, asumsi itu mulai runtuh. **Local-first architecture**, paradigma di mana logika utama dan database berjalan di perangkat pengguna dengan sinkronisasi sebagai lapisan kedua, telah menjadi salah satu tren arsitektur paling berpengaruh, dipakai oleh Figma, Linear, Notion, dan ratusan startup baru.

## Mengapa Local-First Mendominasi 2026?

Ada empat alasan utama yang mendorong adopsi massal:

1. **Latensi nol**. Interaksi lokal berjalan dalam hitungan milidetik, tanpa perlu round-trip ke server yang bisa memakan 100-500ms.
2. **Offline resilience**. Pengguna tetap produktif di pesawat, di daerah remote, atau saat server mengalami downtime.
3. **Privasi yang lebih baik**. Data sensitif tidak lagi wajib meninggalkan perangkat, ini sangat relevan di era regulasi seperti GDPR dan UU PDP di Indonesia.
4. **Biaya infrastruktur lebih rendah**. Beban komputasi dan bandwidth bergeser ke client, mengurangi kebutuhan server besar.

## CRDT: Fondasi Sinkronisasi Tanpa Konflik

Jantung dari local-first adalah **CRDT (Conflict-free Replicated Data Types)**, struktur data yang dapat dimodifikasi dari banyak perangkat secara paralel tanpa koordinasi pusat, lalu otomatis konvergen ke kondisi yang sama. Tidak ada "last write wins" yang merusak data; setiap operasi bersifat komutatif dan idempotent.

Dua implementasi yang paling matang di 2026 adalah **Automerge** dan **Yjs**. Yjs digunakan oleh Notion dan Linear untuk editor kolaboratif mereka, mendukung teks, array, map, dan bahkan rich-text dengan performa yang stabil meski dokumen berukuran besar.

```javascript
import * as Y from "yjs";
import { IndexeddbPersistence } from "y-indexeddb";

const doc = new Y.Doc();
new IndexeddbPersistence("my-app", doc); // persist lokal

const ytext = doc.getText("note");
ytext.insert(0, "Belum ada internet? Tidak masalah!");

// Sinkronisasi via WebRTC / WebSocket / y-sync
```

### Cara Kerja di Balik Layar

Ada dua keluarga pendekatan di pustaka CRDT:

- **State-based (CvRDT)**: seluruh state dokumen dikirim lalu di-merge. Implementasinya sederhana, tapi boros bandwidth untuk dokumen besar.
- **Operation-based (CmRDT)**: hanya operasi yang dikirim, misalnya "sisipkan karakter 'a' di posisi 12". Menuntut lapisan pengiriman yang andal, sehingga pustaka populer biasanya memakai campuran keduanya.

Yjs memakai algoritma **YATA**. Setiap item menyimpan identitas unik berupa pasangan client id dan logical clock, sehingga urutan penerimaan operasi tidak mengubah hasil akhir. **State vector**, yaitu ringkasan versi per client, dipakai untuk menanyakan "apa yang belum saya punya", dan yang dikirim ke peer adalah delta biner, bukan seluruh dokumen. Itulah sebabnya dokumen besar tetap ringan saat transit.

Automerge mengambil jalan berbeda dengan model dokumen bergaya JSON dan penyimpanan kolumnar. Versi 3 memakai inti Rust untuk menutup selisih performa dengan Yjs, sekaligus menawarkan model data yang lebih kaya untuk struktur bersarang.

Contoh menghitung delta yang perlu dikirim:

```javascript
import * as Y from "yjs";

const svA = Y.encodeStateVector(docA); // ringkasan versi lokal
const svB = Y.encodeStateVector(docB); // versi yang dimiliki peer

// Hanya kirim perubahan yang belum dimiliki peer
const update = Y.encodeStateAsUpdate(docA, svB);
Y.applyUpdate(docB, update);
```

## Menyimpan Data di Client: IndexedDB vs OPFS

Hampir semua sync engine menaruh database SQL sungguhan di perangkat. Pertanyaannya, backend penyimpanan mana yang menopangnya.

- **IndexedDB**: key-value store, bisa diakses dari main thread, tapi tidak punya API baca sinkron dan bukan mesin SQL. Throughput untuk transaksi besar terbatas.
- **OPFS (Origin Private File System)**: filesystem berskop origin dengan akses file sinkron, persis yang dibutuhkan lapisan VFS SQLite. Sync access handle tersedia mulai Chromium 108, Firefox 111, dan Safari 16.4.

Batasan penting dari build resmi SQLite WASM (`@sqlite.org/sqlite-wasm`):

1. Sync access handle OPFS hanya ada di Worker thread, jadi database ber-OPFS tidak bisa dibuka di main thread.
2. VFS default `opfs` memerlukan header COOP dan COEP karena bergantung pada `SharedArrayBuffer`: `Cross-Origin-Opener-Policy: same-origin` dan `Cross-Origin-Embedder-Policy: require-corp`. Tanpa header itu VFS tidak akan termuat.
3. `opfs-sahpool` tidak butuh header dan paling cepat untuk pekerjaan batch, tapi hanya mengizinkan satu koneksi terbuka, sehingga tab kedua yang membuka database sama akan gagal.
4. Safari di bawah versi 17 tidak kompatibel dengan VFS `opfs` karena bug browser pada penanganan storage dari sub-worker.
5. Kuota penyimpanan bergantung browser, dan persistensi menurun atau hilang sama sekali di mode incognito.

```javascript
// db.worker.js (harus Worker, bukan main thread)
import sqlite3InitModule from "@sqlite.org/sqlite-wasm";

const sqlite3 = await sqlite3InitModule({ print: console.log });

await sqlite3.installOpfsSAHPoolVfs(); // tanpa header COOP/COEP, 1 koneksi
// atau pakai VFS "opfs" bila perlu multi-tab

const db = new sqlite3.oo1.OpfsDb("app.db", "c");
db.exec(`
  PRAGMA journal_mode = WAL;
  CREATE TABLE IF NOT EXISTS note (
    id TEXT PRIMARY KEY,
    body TEXT,
    updated_at INTEGER
  );
`);
```

Jebakan yang paling sering ditemui: ketika OPFS tidak tersedia, aplikasi diam-diam jatuh ke database in-memory. Aplikasinya tetap jalan, tapi seluruh data pengguna hilang saat refresh. Lebih baik gagal keras dan tampilkan pesan daripada menyimpan sesuatu yang tidak akan bertahan.

## Pola Sinkronisasi dan Optimasi Bandwidth

Server sebaiknya mengirim delta, bukan full fetch:

- Kirim state vector saat handshake agar server tahu apa yang sudah dimiliki client.
- Batch perubahan dalam satu transaksi lokal, lalu kirim sebagai satu pesan, bukan satu pesan per keystroke.
- Pakai exponential backoff saat koneksi kembali, dan jangan kirim ulang operasi yang sudah di-ack dengan menyimpan offset terakhir di storage lokal.
- Pisahkan presence (posisi kursor, status online) dari data. Presence boleh dibuang, data tidak boleh.

Antrean tulis lokal harus bertahan melewati reload. PowerSync menangani ini lewat persistent upload queue. Kalau kamu membangun sendiri, simpan operasi yang belum terkirim di database lokal yang sama dan di dalam satu transaksi dengan perubahan pengguna, supaya keduanya tidak pernah berbeda.

## Sync Engine: Membawa CRDT ke Produksi

CRDT mentah saja tidak cukup untuk aplikasi produksi. Di sinilah peran **sync engine**, lapisan yang menghubungkan database lokal dengan server sebagai *system of record*:

- **ElectricSQL**: Postgres + CRDT, kini stabil di versi 1.x, dengan SQL yang bisa dijalankan offline.
- **PowerSync**: sinkronisasi Postgres/MongoDB ke SQLite di mobile dan web, production-grade.
- **Zero**: engine serverless untuk aplikasi real-time dengan permission bawaan.
- **Triplit, Instant, TinyBase**: alternatif yang lebih ringan untuk use case spesifik.

Pola umumnya: client menyimpan full database lokal (SQLite via WASM, IndexedDB, atau OPFS), lalu sync engine mengirim delta patch secara incremental, bukan full fetch, sehingga bandwidth tetap hemat.

Satu perbedaan yang perlu diperhatikan saat memilih: ElectricSQL (kini menyebut dirinya Electric, protokolnya Apache-2.0) menyinkronkan Postgres ke client memakai logical replication dan berfokus pada read path, bukan write path. Aplikasi yang butuh penulisan offline yang andal tetap perlu menaruh logika write di server, atau memakai engine dengan upload queue seperti PowerSync dan Zero. Zero memakai arsitektur query-driven: server menjalankan "mutator" yang memvalidasi dan menerapkan penulisan, client melihat optimistic update seketika, dan server masih bisa menolak atau menransformasi hasilnya.

## Authorization dan Validasi di Server

Client tidak bisa dipercaya, jadi authorization wajib ditegakkan di server.

```javascript
// Konsep mutator di sisi server (gaya Zero)
mutators.transfer.create(async ({ tx, args, ctx }) => {
  if (!ctx.userID) throw new Error("unauthenticated");
  if (args.amount <= 0) throw new Error("amount must be positive");

  const balance = await tx.query.balance.where("userId", ctx.userID).one();
  if (balance.value < args.amount) throw new Error("insufficient funds");

  await tx.mutate.balance.update(balance.id, {
    value: balance.value - args.amount,
  });
  await tx.mutate.ledger.insert({
    userId: ctx.userID,
    amount: args.amount,
    ts: Date.now(),
  });
});
```

Aturan praktisnya:

- Jangan pernah mempercayai validasi schema di client sebagai satu-satunya penjaga.
- Taruh aturan domain (saldo tidak boleh minus, kuota per tenant, hak akses per baris) sebagai fungsi di server.
- Pakai row-level security di Postgres sebagai lapis kedua bila sync engine meneruskan identitas pengguna.
- Audit log harus ditulis dari server, bukan dari client yang bisa dimodifikasi.

## Tantangan yang Masih Ada

Local-first bukan tanpa rintangan. **Conflict resolution untuk business logic** masih sulit, sebab menggabungkan dua edit teks itu mudah, tapi menggabungkan dua transaksi keuangan yang bentrok butuh aturan domain yang matang. **Authorization** juga wajib di-enforce di server, karena client tidak bisa dipercaya. Selain itu, **cold start** untuk dataset besar dan **migrasi schema** antar versi CRDT adalah masalah yang harus direncanakan sejak awal, misalnya dengan versioning pada setiap tipe data.

Migrasi schema layak dibahas lebih jauh. CRDT menyimpan riwayat, bukan snapshot, sehingga menghapus sebuah field bisa berarti memutus kompatibilitas dengan client versi lama yang masih mengirim operasi untuk field itu. Pola yang aman adalah menambah field baru, menjalankan migrasi di server, dan menunggu seluruh client memperbarui sebelum menonaktifkan jalur tulis lama. Gabungkan dengan penanda versi di setiap dokumen agar server bisa menolak operasi dari versi yang sudah tidak didukung.

## Kapan Local-Fast Justru Salah Pilihan

Local-first bukan obat untuk semua masalah:

- Dashboard analitik dengan query agregat besar di atas data yang jarang berubah tidak akan mendapat manfaat apa pun.
- Workload yang datanya sangat sensitif terhadap ukuran: menyalin seluruh dataset ke setiap klien bisa lebih mahal daripada satu server.
- Tim kecil tanpa kapasitas merawat logika sinkronisasi, konflik, dan migrasi schema.
- Kasus di mana sumber kebenaran wajib tunggal secara hukum atau regulasi, misalnya pembukuan yang harus final di satu titik.

Di kasus seperti itu, optimistic UI dengan cache biasa (React Query, SWR) sudah lebih dari cukup.

## Kesimpulan

Local-first bukan berarti meninggalkan server. Server tetap krusial untuk autentikasi, backup, dan kolaborasi. Tetapi arsitekturnya dibalik: client adalah warga kelas satu, bukan thin client yang hanya menampilkan HTML. Dengan kematangan CRDT, sync engine, dan dukungan browser modern seperti OPFS, 2026 adalah waktu yang tepat untuk mulai mengadopsi local-first, terutama untuk aplikasi yang mengutamakan pengalaman pengguna, ketahanan offline, dan privasi.
