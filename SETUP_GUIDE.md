# PANDUAN SETUP LENGKAP
## Sistem Auto-Income AI — $0 Biaya, Jalan Sendiri Setiap Hari

---

## GAMBARAN BESAR

Setelah setup selesai, sistem ini akan:
- Generate 1 artikel AI setiap hari jam 08:00 WIB
- Publish otomatis ke Medium, Dev.to, dan Hashnode sekaligus
- Produk Gumroad kamu menjual dan mengirim otomatis 24/7
- Uang masuk ke rekening tanpa kamu lakukan apapun

**Total waktu setup: 2–3 jam (sekali seumur hidup)**
**Biaya: $0**

---

## LANGKAH 1: Buat Akun GitHub (10 menit)

1. Buka https://github.com → Sign up (gratis)
2. Buat repository baru:
   - Klik "+" → "New repository"
   - Nama: `auto-income-engine`
   - Pilih: **Public** (penting! private repo GitHub Actions ada batasnya)
   - Centang "Add README"
   - Klik "Create repository"

3. Upload semua file dari folder ini:
   - Klik "uploading an existing file"
   - Drag semua file (pertahankan struktur folder)
   - Commit

---

## LANGKAH 2: Dapatkan Google Gemini API Key (5 menit)

1. Buka https://aistudio.google.com
2. Login dengan akun Google
3. Klik "Get API Key" → "Create API key"
4. Pilih project (buat baru jika belum ada)
5. **COPY API KEY** — simpan, akan dipakai di Langkah 5

**Catatan:** Gemini 1.5 Flash gratis: 15 request/menit, 1 juta token/hari
Lebih dari cukup untuk 1 artikel/hari.

---

## LANGKAH 3: Setup Medium (15 menit)

1. Buka https://medium.com → Sign up (gratis)
2. **Wajib:** Apply untuk Medium Partner Program:
   - Settings → Partner Program → Apply
   - Butuh: Stripe account (gratis dibuat) + nomor telepon
   - Approval: 1–3 hari kerja
3. Dapatkan Integration Token:
   - https://medium.com/me/settings → Integration tokens
   - Klik "Get integration token"
   - Beri nama: "auto-publish"
   - **COPY TOKEN**

---

## LANGKAH 4: Setup Dev.to (5 menit)

1. Buka https://dev.to → Sign up (gratis)
2. Dapatkan API Key:
   - https://dev.to/settings/extensions
   - Scroll ke "DEV Community API Keys"
   - Generate API Key, beri nama "auto-publish"
   - **COPY API KEY**

---

## LANGKAH 5: Setup Hashnode (10 menit)

1. Buka https://hashnode.com → Sign up (gratis)
2. Buat blog baru:
   - Dashboard → "Create a blog"
   - Pilih subdomain, misal: `yourblog.hashnode.dev` (gratis)
3. Dapatkan Token:
   - https://hashnode.com/settings/developer
   - "Generate New Token"
   - **COPY TOKEN**
4. Dapatkan Publication ID:
   - Buka blog kamu → Settings → General
   - Lihat URL: `hashnode.com/PUBLICATION-ID/settings`
   - **COPY PUBLICATION ID**

---

## LANGKAH 6: Setup Gumroad (20 menit)

1. Buka https://gumroad.com → Sign up (gratis)
2. Hubungkan rekening bank:
   - Settings → Payouts → Add bank account
   - Untuk Indonesia: tambahkan via Wise (wise.com) atau PayPal
3. Buat produk digital:
   - Products → New Product → Digital product
   - Nama: "200 AI Prompts untuk Bisnis Indonesia"
   - Harga: $7
   - Upload file PDF prompt pack
   - Copy sales page dari file `gumroad_sales_page.txt`
4. Salin URL produk kamu
5. **Update file** `scripts/publish_devto.py` baris:
   ```
   👉 **[Get the 200 AI Prompts Pack ($7)](https://gumroad.com/l/YOUR-PRODUCT-SLUG)**
   ```
   Ganti `YOUR-PRODUCT-SLUG` dengan slug produk kamu.

---

## LANGKAH 7: Setup Rekening Penerimaan (30 menit)

### Opsi A: Wise (Recommended untuk Indonesia)
1. Daftar di wise.com (gratis)
2. Buat akun USD
3. Dapatkan nomor rekening virtual USD
4. Gunakan nomor ini untuk:
   - Medium Partner Program (Stripe)
   - Gumroad payout

### Opsi B: PayPal
1. Daftar di paypal.com
2. Verifikasi akun dengan KTP
3. Gunakan email PayPal untuk Gumroad payout

---

## LANGKAH 8: Masukkan Semua Secrets ke GitHub (10 menit)

1. Buka repository GitHub kamu
2. Settings → Secrets and variables → Actions → "New repository secret"
3. Tambahkan satu per satu:

| Secret Name | Value |
|-------------|-------|
| `GEMINI_API_KEY` | [dari Langkah 2] |
| `MEDIUM_TOKEN` | [dari Langkah 3] |
| `DEVTO_API_KEY` | [dari Langkah 4] |
| `HASHNODE_TOKEN` | [dari Langkah 5] |
| `HASHNODE_PUBLICATION_ID` | [dari Langkah 5] |
| `GOOGLE_SHEETS_CREDENTIALS` | [opsional, lihat bawah] |
| `SPREADSHEET_ID` | [opsional] |

**Google Sheets (opsional tapi recommended):**
1. Buka https://console.cloud.google.com
2. Buat project baru → Enable "Google Sheets API"
3. Create Service Account → Download JSON credentials
4. Base64-encode: `base64 credentials.json | pbcopy`
5. Paste sebagai value `GOOGLE_SHEETS_CREDENTIALS`
6. Buat Google Sheet baru, share dengan email service account
7. Ambil Spreadsheet ID dari URL

---

## LANGKAH 9: Test Run (2 menit)

1. Di GitHub repository → Actions tab
2. Klik workflow "AI Content Engine — Daily Auto-Publish"
3. Klik "Run workflow" → Run workflow
4. Tunggu 2–3 menit
5. Cek: apakah artikel muncul di Medium, Dev.to, dan Hashnode?

Jika berhasil → sistem sudah aktif! Akan jalan otomatis setiap hari.

---

## SCHEDULE OTOMATIS

Sistem akan berjalan setiap hari jam **08:00 WIB** (01:00 UTC) secara otomatis.
Kamu tidak perlu melakukan apapun.

Untuk melihat progress: GitHub → Actions → pilih run terbaru

---

## PROYEKSI PENDAPATAN REALISTIS

### Bulan 1 (30 artikel):
- Medium reads: 500–2.000 total → $2–10
- Gumroad: 5–15 penjualan → $35–105
- **Total: $37–115**

### Bulan 2–3 (60–90 artikel):
- Medium reads: 3.000–15.000 total (compound) → $15–75/bulan
- Gumroad: 15–30 penjualan/bulan → $105–210
- Dev.to traffic → tambah Gumroad sales
- **Total: $120–285/bulan ($4–10/hari)**

### Bulan 4–6 (120–180 artikel):
- Beberapa artikel mulai viral
- Medium: $30–150/bulan
- Gumroad: $100–400/bulan
- **Total: $130–550/bulan ($4–18/hari)**

---

## FAQ

**Q: Apakah ini melanggar ToS platform?**
A: Tidak. Medium, Dev.to, dan Hashnode semuanya memiliki API resmi untuk auto-publishing. Yang penting: konten harus original dan berkualitas (bukan spam). Gemini menghasilkan konten original setiap hari.

**Q: Apakah Google Gemini benar-benar gratis?**
A: Ya. Gemini 1.5 Flash: gratis 15 request/menit, 1 juta token/hari. Untuk 1 artikel/hari, kamu tidak akan pernah kena biaya.

**Q: Bagaimana uang keluar dari Medium/Gumroad ke saya?**
A: Medium bayar via Stripe setiap bulan → Wise/PayPal → rekening bank. Gumroad transfer setiap minggu ke Wise/PayPal → rekening bank. Semua otomatis.

**Q: Bagaimana jika konten AI terdeteksi?**
A: Medium dan platform lain tidak melarang konten yang dibantu AI selama konten informatif dan berharga. Kualitas konten Gemini 1.5 Flash cukup baik untuk pass review.

**Q: Bisa dapat lebih dari $10/hari?**
A: Sangat bisa. Begitu beberapa artikel mulai viral dan Gumroad punya reviews, pendapatan bisa 3–5x lebih tinggi. Sistem ini scalable tanpa tambahan biaya.

---

## SUPPORT

Jika ada error saat menjalankan workflow, cek:
1. GitHub Actions → klik run yang failed → lihat log detail
2. Pastikan semua Secrets sudah diisi dengan benar
3. Pastikan akun Medium sudah approved untuk Partner Program
