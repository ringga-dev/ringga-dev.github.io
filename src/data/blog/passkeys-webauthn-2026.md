---
title: "Passkeys & WebAuthn 2026: Mengakhiri Era Password dengan Autentikasi Tanpa Rahasia"
description: "Memahami cara kerja passkey berbasis WebAuthn FIDO2, mengapa lebih aman dari OTP dan password, serta langkah implementasi praktis di web app tahun 2026."
date: "2026-08-14"
author: "Ringga Septia Pribadi"
tags: ["Passkeys", "WebAuthn", "FIDO2", "Cybersecurity", "Web Development"]
category: "Web Development"
image: "https://images.unsplash.com/photo-1563013544-824ae1b704d3?q=80&w=2070&auto=format&fit=crop"
---

## Pendahuluan

Di tahun 2026, password mulai ditinggalkan secara masif. Google, Apple, dan Microsoft telah mengaktifkan dukungan **passkey** secara default di miliaran perangkat. Passkey adalah kredensial kriptografis berbasis standar **WebAuthn** (FIDO2) yang menggantikan password dengan pasangan kunci publik–privat. Yang penting: rahasia privat **tidak pernah** meninggalkan perangkat pengguna, sehingga phishing dan kebocoran database tidak lagi bisa mengekspos kredensial login.

## Bagaimana Passkey Bekerja

Saat registrasi, browser meminta authenticator (biometrik, PIN perangkat, atau security key) membuat sepasang kunci. Kunci publik dikirim ke server, kunci privat tetap terkunci di perangkat. Saat login, server mengirim *challenge* acak; perangkat menandatanganinya dengan kunci privat. Server memverifikasi tanda tangan via kunci publik yang tersimpan. Tidak ada password yang dikirim, tidak ada kode OTP yang bisa dicegat.

## Keunggulan vs Metode Lama

| Metode | Rentan Phishing | Rahasia di Server | UX |
|--------|-----------------|-------------------|-----|
| Password | 🔴 Ya | 🔴 Ya (hash) | 🟡 Ribet |
| OTP / SMS | 🟠 Ya (intercept) | 🟠 Ya (kode) | 🟡 Ribet |
| Passkey | ✅ Tidak | ✅ Tidak | ✅ Sekali tap |

Passkey mengikat domain secara kriptografis. Link phishing `paypa1.com` tidak bisa memancing respons valid karena *challenge* hanya berlaku untuk origin terdaftar.

## Implementasi Praktis di Web

Berikut contoh registrasi passkey menggunakan WebAuthn API murni di sisi klien:

```javascript
// 1. Minta opsi registrasi dari server
const opts = await fetch('/webauthn/register/options').then(r => r.json());

// 2. Buat credential baru
const cred = await navigator.credentials.create({
  publicKey: {
    challenge: base64ToBuf(opts.challenge),
    rp: { name: "Ringga App" },
    user: { id: base64ToBuf(opts.userId), name: opts.email, displayName: opts.email },
    pubKeyCredParams: [{ type: "public-key", alg: -7 }, { type: "public-key", alg: -257 }],
    authenticatorSelection: { residentKey: "required", userVerification: "preferred" }
  }
});

// 3. Kirim hasil ke server untuk disimpan
await fetch('/webauthn/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id: cred.id, rawId: bufToBase64(cred.rawId), response: cred.response })
});
```

Proses verifikasi login hampir identik, hanya menggunakan `navigator.credentials.get()` dan memvalidasi tanda tangan di server dengan library seperti `@simplewebauthn/server`.

## Tips Implementasi 2026

- **Wajib HTTPS**: WebAuthn hanya berjalan di origin aman.
- **Account recovery**: sediakan fallback (device binding atau backup passkey) agar pengguna tidak terkunci.
- **Conditional UI**: gunakan `username` autofill otomatis agar passkey muncul di keyboard tanpa layar login khusus.
- **Graceful degradation**: tetap sediakan password/OTP sementara untuk transisi.

## Kesimpulan

Passkey bukan sekadar tren, melainkan pergeseran paradigma ke *passwordless*. Dengan WebAuthn, autentikasi menjadi lebih aman sekaligus lebih nyaman. Mulai integrasikan passkey di aplikasi web Anda tahun ini — pengguna dan tim keamanan akan berterima kasih.
