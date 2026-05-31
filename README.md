# SinomiAI Dashboard 🌿♻️

Dashboard analitik interaktif untuk proyek Capstone **SinomiAI** — platform klasifikasi dan rekomendasi pengolahan limbah berbasis AI.

---

## 📦 Cara Deploy ke Streamlit Cloud

### 1. Upload ke GitHub
Buat repository baru dan upload dua file ini:
```
sinomi_dashboard/
├── app.py
└── requirements.txt
```

### 2. Deploy di Streamlit Community Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Klik **"New app"**
3. Hubungkan repository GitHub Anda
4. Set **Main file path** → `app.py`
5. Klik **"Deploy!"**

### 3. Akses Dashboard
Setelah deploy, Anda akan mendapatkan URL publik seperti:
`https://sinomi-ai-dashboard.streamlit.app`

---

## 🗂️ Isi Dashboard

| Halaman | Konten |
|---|---|
| 🏠 **Overview** | Hero banner, KPI cards, ringkasan proyek & pipeline |
| 📊 **Dataset & EDA** | Distribusi kelas, sub-kelas material, analisis resolusi |
| ⚙️ **Preprocessing** | Data cleaning, feature engineering, augmentasi |
| 🤖 **Model & Performa** | Arsitektur CNN, kurva training, classification report |
| 📋 **Ringkasan** | Temuan utama, roadmap, kesimpulan |

---

## 🎨 Desain

- **Tema**: Dark mode dengan aksen hijau (#56D364) dan biru (#58A6FF)
- **Tipografi**: Syne (heading) + DM Sans (body)
- **Visualisasi**: Plotly interactive charts (pie, bar, scatter, heatmap, radar)
- **Layout**: Responsive multi-column dengan card components

---

## 👥 Tim CC26-PSU343

- Riana Shofiatul Khoeriyah
- Mohammad Fahriza Pratama
- Yildi Andriana
- Muhammad Irsyad Mustaqim
- Madda Athia Rahman
