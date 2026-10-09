---
title: "Passkeys & WebAuthn 2026: Mengakhiri Era Password dengan Autentikasi Tanpa Rahasia"
description: "Memahami cara kerja passkey berbasis WebAuthn FIDO2, mengapa lebih aman dari OTP dan password, serta langkah implementasi praktis di web app tahun 2026."
date: "2026-08-14"
author: "Ringga Septia Pribadi"
tags: ["Passkeys", "WebAuthn", "FIDO2", "Cybersecurity", "Web Development"]
category: "Web Development"
image: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80"
---

## Pendahuluan

Di tahun 2026, password mulai ditinggalkan secara masif. Google, Apple, dan Microsoft telah mengaktifkan dukungan **passkey** secara default di miliaran perangkat. Passkey adalah kredensial kriptografis berbasis standar **WebAuthn** (FIDO2) yang menggantikan password dengan pasangan kunci publik-privat. Yang penting: rahasia privat **tidak pernah** meninggalkan perangkat pengguna, sehingga phishing dan kebocoran database tidak lagi bisa mengekspos kredensial login.

Sebelum masuk ke implementasi, penting meluruskan istilah yang sering tertukar, karena ketiganya hidup di lapisan berbeda:

- **WebAuthn** adalah API JavaScript yang distandarisasi W3C. Inilah satu-satunya lapisan yang benar-benar disentuh kode frontend Anda. Level 3 sudah masuk tahap Candidate Recommendation Snapshot pada Januari 2026, membawa fitur baru seperti conditional create, Signal API, dan related origin requests.
- **CTAP2** (Client to Authenticator Protocol) adalah protokol komunikasi antara browser atau sistem operasi dengan authenticator eksternal, seperti security key USB atau NFC. Standar ini milik FIDO Alliance dan Anda tidak pernah berinteraksi dengannya secara langsung.
- **Passkey** hanyalah nama produk untuk kredensial WebAuthn yang bisa tersinkronisasi antar perangkat lewat penyedia cloud seperti iCloud Keychain, Google Password Manager, atau 1Password. Passkey bukan standar baru; ia adalah WebAuthn dengan pengalaman pengguna yang mapan.

Pembedaan ini praktis saat debugging. Kalau `navigator.credentials.create()` gagal, masalahnya di lapisan browser atau RP ID. Kalau kunci hardware tidak terbaca sama sekali, masalahnya di lapisan CTAP.

## Bagaimana Passkey Bekerja

Saat registrasi, browser meminta authenticator (biometrik, PIN perangkat, atau security key) membuat sepasang kunci. Kunci publik dikirim ke server, kunci privat tetap terkunci di perangkat. Saat login, server mengirim *challenge* acak; perangkat menandatanganinya dengan kunci privat. Server memverifikasi tanda tangan via kunci publik yang tersimpan. Tidak ada password yang dikirim, tidak ada kode OTP yang bisa dicegat.

Mari kita bedah data yang benar-benar berpindah. Pada registrasi, server mengirim objek `PublicKeyCredentialCreationOptions` yang memuat beberapa field wajib:

| Field | Fungsi | Catatan praktis |
|-------|--------|-----------------|
| `rp.id` | Menentukan domain scope kredensial | Semua subdomain di bawahnya dapat memakai kredensial yang sama |
| `challenge` | Nilai acak minimal 16 byte | Wajib di-generate server-side, sekali pakai |
| `user.id` | Identifier pengguna, bukan email | Jangan pakai email sebagai `user.id` agar akun tetap stabil walau email berganti |
| `pubKeyCredParams` | Algoritma tanda tangan yang diterima | `-7` (ES256) dan `-257` (RS256) adalah pilihan paling aman |
| `authenticatorSelection` | Preferensi jenis authenticator | Lihat bahasan di bawah |

Pada tahap verifikasi, yang diperiksa server bukan hanya "tanda tangan valid", melainkan rantai properti sekaligus: `clientDataJSON.challenge` harus sama persis dengan yang dikirim, `clientDataJSON.origin` harus sama dengan origin Anda, dan `authenticatorData.flags` harus menandakan user presence atau user verification sesuai kebijakan. Banyak implementasi rumahan gagal justru di pemeriksaan origin ini, sehingga celah replay lintas-domain terbuka.

## Keunggulan vs Metode Lama

| Metode | Rentan Phishing | Rahasia di Server | UX |
|--------|-----------------|-------------------|-----|
| Password | Ya | Ya (hash) | Ribet |
| OTP / SMS | Ya (intercept) | Ya (kode) | Ribet |
| Passkey | Tidak | Tidak | Sekali tap |

Passkey mengikat domain secara kriptografis. Link phishing `paypa1.com` tidak bisa memancing respons valid karena *challenge* hanya berlaku untuk origin terdaftar.

Perhatikan nuansa penting: kredensial WebAuthn tidak terikat pada halaman, melainkan pada **origin**. Artinya `https://app.example.com` dan `https://evil.com` tidak bisa saling meminjam kredensial. Namun dua origin berbeda di bawah domain yang sama juga tidak otomatis saling berbagi, kecuali Anda memanfaatkan `rp.id` di tingkat parent domain atau fitur related origin requests dari WebAuthn L3.

Fitur related origin requests memerlukan file JSON di URL well-known `.well-known/webauthn` pada RP ID, disajikan lewat HTTPS dengan content type `application/json`. Inilah cara resmi untuk memungkinkan satu passkey dipakai lintas beberapa aplikasi milik organisasi yang sama tanpa meminta pengguna mendaftar ulang.

## Jenis Authenticator dan Implikasi Kebijakan

`authenticatorSelection` sering diisi asal, padahal nilainya menentukan karakter keamanan kredensial:

```javascript
authenticatorSelection: {
  authenticatorAttachment: "platform",  // atau "cross-platform"
  residentKey: "required",
  requireResidentKey: true,
  userVerification: "required"
}
```

- `authenticatorAttachment: "platform"` membatasi ke authenticator internal perangkat, misalnya Touch ID, Windows Hello, atau fingerprint Android. Keunggulannya: biometrik tidak pernah keluar dari secure enclave. Kerugiannya: kredensial tidak bisa dipindah ke laptop lain.
- `authenticatorAttachment: "cross-platform"` berarti security key fisik. Cocok untuk lingkungan berregulasi karena perangkat bisa dicabut.
- `userVerification: "required"` memastikan ada verifikasi biometrik atau PIN pada setiap login. Tanpa ini, seseorang yang memegang laptop Anda yang sudah terbuka bisa langsung masuk. Untuk aplikasi finansial atau admin panel, nilai ini sebaiknya `required`, bukan `preferred`.

Aturan praktis: simpan nilai `userVerification` yang tercapai pada setiap kredensial di database Anda, lalu terapkan step-up authentication. Login biasa boleh `preferred`, tapi saat pengguna akan mentransfer dana atau mengubah email, minta sesi baru dengan `userVerification: "required"`.

## Attestation: Kapan Benar-Benar Dibutuhkan

Salah satu keputusan yang paling sering salah adalah memaksa attestation. Attestation adalah mekanisme opsional di mana authenticator membuktikan secara kriptografis model perangkatnya lewat `attestationObject` pada respons registrasi.

Ada empat tingkat: `none` (tanpa attestation, nilai default), `indirect` (attestation teranonimkan), `direct` (attestation pabrikan apa adanya), dan `enterprise` (mengidentifikasi perangkat individual untuk deployment yang sudah disepakati).

Kenyataannya di lapangan: passkey yang tersinkronisasi lewat iCloud Keychain atau Google Password Manager umumnya **tidak menyediakan attestation**. Menerapkan `attestation: "direct"` akan memblokir seluruh passkey platform, dan pengguna akan tersandung error registrasi tanpa penjelasan. Default `none` adalah pilihan yang benar untuk hampir semua layanan konsumen.

Baru pakai `direct` bila ada alasan regulasi atau kebijakan internal, misalnya bank yang wajib memastikan kredensial dibuat di security key bersertifikat FIDO L2. Pada kasus itu, bandingkan rantai sertifikat pada attestation statement terhadap metadata dari FIDO Metadata Service untuk memvalidasi AAGUID dan level sertifikasi authenticator.

## Implementasi Praktis di Web

Berikut contoh registrasi passkey menggunakan WebAuthn API murni di sisi klien:

```javascript
// 1. Minta opsi registrasi dari server
const opts = await fetch('/webauthn/register/options').then(r => r.json());

// 2. Buat credential baru
const cred = await navigator.credentials.create({
  publicKey: {
    challenge: base64ToBuf(opts.challenge),
    rp: { name: "Ringga App", id: "example.com" },
    user: { id: base64ToBuf(opts.userId), name: opts.email, displayName: opts.email },
    pubKeyCredParams: [{ type: "public-key", alg: -7 }, { type: "public-key", alg: -257 }],
    authenticatorSelection: { residentKey: "required", userVerification: "preferred" },
    timeout: 120000
  }
});

// 3. Kirim hasil ke server untuk disimpan
await fetch('/webauthn/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id: cred.id, rawId: bufToBase64(cred.rawId), response: cred.response })
});
```

Perlu dicatat, `cred.response` pada dasarnya adalah objek `AuthenticatorAttestationResponse` yang tidak bisa di-`JSON.stringify` secara langsung. Anda harus mengambil `attestationObject` dan `clientDataJSON` dari dalamnya, lalu encode base64url satu per satu. Mengabaikan hal ini adalah sumber error paling umum saat pertama kali mencoba implementasi manual.

Proses verifikasi login hampir identik, hanya menggunakan `navigator.credentials.get()` dan memvalidasi tanda tangan di server dengan library seperti `@simplewebauthn/server`. Untuk login, isi `allowCredentials` hanya bila Anda memang sudah mengetahui kredensial mana yang dimaksud; bila dikosongkan dan `residentKey: "required"`, pengguna akan melihat pemilih akun.

```javascript
const assertion = await navigator.credentials.get({
  publicKey: {
    challenge: base64ToBuf(challenge),
    rpId: "example.com",
    allowCredentials: [],           // kosong = biarkan pengguna memilih
    userVerification: "required",
    timeout: 120000
  }
});
```

## Conditional UI: Faktor Paling Menentukan Adopsi

Ini bagian yang paling sering dilewatkan dan paling berdampak. Conditional UI (`mediation: "conditional"`) memunculkan passkey yang tersimpan langsung di dropdown autofill browser, berdampingan dengan username yang sudah tersimpan. Pengguna tidak perlu menemukan tombol "Sign in with passkey", mereka hanya memilih saran di bawah field email.

```javascript
// Deteksi kapabilitas dulu, jangan langsung kirim opsi conditional
const available = await PublicKeyCredential.isConditionalMediationAvailable();

if (available) {
  const assertion = await navigator.credentials.get({
    publicKey: { challenge: base64ToBuf(challenge), rpId: "example.com" },
    mediation: "conditional"
  });
  // lanjutkan proses login
}
```

Field input juga wajib diberi hint autocomplete yang benar:

```html
<input type="email" name="email" autocomplete="username webauthn" />
```

Tanpa token `webauthn`, sebagian browser tidak akan menyertakan passkey pada permukaan autofill meski `mediation: "conditional"` sudah aktif.

Riwayat pendukungannya juga patut diketahui: Safari 16 memperkenalkan conditional UI lebih dulu, diikuti Chrome dan Edge pada versi 108, sedangkan Firefox baru menyusul lewat Firefox 122 yang rilis Januari 2024. Setelah itu dukungan lintas browser lengkap, sehingga pada 2026 tidak ada lagi alasan teknis untuk melewatinya.

Selain conditional UI untuk login, ada **conditional create** untuk registrasi: pengguna yang login dengan password bisa langsung di-upgrade ke passkey tanpa prompt khusus, karena `navigator.credentials.create()` dipanggil dengan mediation conditional saat halaman dimuat. Ini mengubah alur onboarding dari proyek tersendiri menjadi efek samping dari login yang sudah ada.

## Signal API dan Sinkronisasi State

Masalah klasik passkey: pengguna menghapus passkey dari password manager, server Anda masih menyimpan kredensial yang tidak ada lagi. WebAuthn L3 memperkenalkan Signal API untuk menyinkronkan kondisi ini.

Server mengirim sinyal saat kredensial tidak dikenal (`unknown credential`), saat kredensial berhasil dipakai, atau saat pengguna menambah kredensial baru. Implementasinya memerlukan perubahan kecil di sisi penyedia dan browser, dan tidak semua kombinasi sudah mendukungnya. Meski demikian, jika Anda memakai penyedia yang sudah mendukung, manfaatnya nyata: daftar kredensial di server Anda berhenti menjadi catatan basi yang terus membengkak.

## Ekstensi yang Layak Dipertimbangkan

Beberapa ekstensi WebAuthn layak masuk radar tim Anda di 2026:

- **PRF extension** memungkinkan Anda menurunkan 32 byte output deterministik dari sebuah passkey. Karena output selalu sama untuk input yang sama dan bergantung pada kredensial tersebut, ia bisa dipakai sebagai key material untuk enkripsi end-to-end. Ini membuka pola menarik: satu passkey yang sekaligus jadi kunci enkripsi catatan sensitif, tanpa perlu membangun sistem manajemen kunci terpisah.
- **largeBlob** menyimpan data kecil (skala kilobyte) di samping kredensial, berguna untuk menyimpan sertifikat atau state yang harus ikut berpindah bersama passkey tanpa database server.
- **credProps** melaporkan apakah kredensial yang baru dibuat bersifat discoverable. Sangat berguna bila Anda mendaftarkan dengan `residentKey: "preferred"` dan perlu tahu apakah passkey benar-benar bisa dipakai untuk login tanpa username.

Deteksi kapabilitas klien dilakukan lewat `PublicKeyCredential.getClientCapabilities()`, yang mengembalikan objek berisi flag seperti dukungan conditional UI, PRF, dan related origins. Pakai ini untuk menyesuaikan UI, bukan untuk memblokir pengguna.

## Tips Implementasi 2026

- **Wajib HTTPS**: WebAuthn hanya berjalan di origin aman.
- **Account recovery**: sediakan fallback (device binding atau backup passkey) agar pengguna tidak terkunci. Alur recovery sebaiknya minimal setara kuatnya login itu sendiri, kalau tidak ia jadi pintu belakang.
- **Conditional UI**: gunakan `username` autofill otomatis agar passkey muncul di keyboard tanpa layar login khusus.
- **Graceful degradation**: tetap sediakan password/OTP sementara untuk transisi.
- **Simpan beberapa passkey per akun**: anjurkan pengguna mendaftarkan perangkat kedua. Akun dengan satu passkey saja adalah akun dengan satu titik kegagalan.
- **Timeout eksplisit**: selalu isi `timeout` (umumnya 60 sampai 120 detik) agar permukaan UI tidak menggantung ketika pengguna ragu menyentuh sensor biometrik.
- **Rate limit endpoint challenge**: setiap permintaan challenge harus tercatat dan dibatasi, karena challenge yang bisa di-request tanpa batas membuka celah untuk enumerasi dan kelelahan resource.

## Kesimpulan

Passkey bukan sekadar tren, melainkan pergeseran paradigma ke *passwordless*. Dengan WebAuthn, autentikasi menjadi lebih aman sekaligus lebih nyaman. Mulai integrasikan passkey di aplikasi web Anda tahun ini, dan utamakan conditional UI sebagai langkah pertama karena justru di sanalah perbedaan adopsi terbentuk. Pengguna dan tim keamanan akan berterima kasih.
