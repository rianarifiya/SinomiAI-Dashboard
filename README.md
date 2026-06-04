# SinomiAI Dashboard
---

**SinomiAI Dashboard** adalah dashboard interaktif berbasis Streamlit yang menampilkan hasil analisis data dan performa model machine learning dari proyek capstone **CC26-PSU343**. Dashboard ini memvisualisasikan seluruh pipeline data science mulai dari eksplorasi data, pemrosesan fitur, hingga evaluasi model CNN untuk klasifikasi sampah **Organik** dan **Anorganik**.

---

## Tampilan Dashboard

Dashboard terdiri dari **5 halaman utama**:

| Halaman | Deskripsi |
|---|---|
| Ringkasan Proyek | KPI utama, deskripsi proyek, teknologi, dan capaian model |
| Eksplorasi Data | Distribusi kelas, resolusi gambar, aspect ratio, dan sub-kelas material |
| Pemrosesan & Fitur | Pipeline data wrangling, hasil cleaning, dan teknik augmentasi |
| Performa Model | Kurva akurasi & loss (A/B Testing), classification report, arsitektur CNN |
| Tim Peneliti | Profil anggota tim dan informasi proyek |

---

## Cara Menjalankan

### Prasyarat
- Python 3.9 atau lebih baru
- pip

### Install Dependensi

```bash
pip install -r requirements.txt
```

### Jalankan Dashboard

```bash
streamlit run dashboard.py
```

Buka browser lokal di `http://localhost:8501`

atau

Buka di browser melalui tautan berikut 

---

## 📁 Struktur Folder

```
SinomiAI Dashboard/
├── dashboard.py          # File utama Streamlit
├── requirements.txt      # Daftar dependensi Python
├── README.md             # Dokumentasi proyek
└── assets/
    └── logo_sinomiai.png # Logo SinomiAI
```

---

## 📦 Dependensi

| Package | Versi Minimum | Kegunaan |
|---|---|---|
| streamlit | 1.33.0 | Framework dashboard |
| pandas | 2.0.0 | Pengolahan data tabular |
| numpy | 1.24.0 | Komputasi numerik |
| plotly | 5.18.0 | Visualisasi interaktif |

---

## ☁️ Deploy ke Streamlit Cloud

1. Fork atau push repository ini ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Login dengan akun GitHub
4. Klik **"New app"** dan isi:
   - **Repository**: `username/nama-repo`
   - **Branch**: `main`
   - **Main file path**: `dashboard.py`
5. Klik **Deploy** — selesai ✅

> Pastikan folder `assets/` ikut ter-push ke GitHub agar logo tampil dengan benar.

---

## 📊 Dataset

| Kategori | Jumlah Gambar | Proporsi |
|---|---|---|
| Anorganik | 1.010 | 56,17% |
| Organik | 788 | 43,83% |
| **Total** | **1.798** | **100%** |

- Format gambar: `.jpg`, `.jpeg`, `.png`
- Ukuran input model: `150 × 150` piksel
- Split dataset: **80% latih / 20% validasi**

---

## 🤖 Hasil Model CNN

| Metrik | Anorganik | Organik | Weighted Avg |
|---|---|---|---|
| Precision | 0.99 | 0.98 | 0.99 |
| Recall | 0.99 | 0.99 | 0.99 |
| F1-Score | 0.99 | 0.98 | 0.99 |
| **Akurasi** | — | — | **99%** |

Arsitektur: CNN 3 lapisan konvolusi (32 → 64 → 128 filter) + Dense 512 + Dropout 0.5, dilatih selama **10 epoch**.

---

## 👥 Tim

| Nama | ID |
|---|---|
| Riana Shofiatul Khoeriyah | CDCC222D6X0570 |
| Mohammad Fahriza Pratama | CFCC222D6Y1056 |
| Yildi Andriana | CDCC222D6Y1231 |
| Muhammad Irsyad Mustaqim | CACC222D6Y1363 |
| Madda Athia Rahman | CFCC222D6Y2794 |

**Tim:** CC26-PSU343

---


*© 2025 SinomiAI · Tim CC26-PSU343*
