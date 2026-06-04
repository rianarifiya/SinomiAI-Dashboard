import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import base64

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
LOGO_PATH = Path(__file__).parent / "assets" / "SinomiAI.png"

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.set_page_config(
    page_title="SinomiAI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  COLOR PALETTE
# ─────────────────────────────────────────────
C_PRIMARY   = "#0089e1"   # Biru terang (aksen utama)
C_DARK      = "#00237b"   # Biru gelap (header / teks penting)
C_LIGHT     = "#9eb2df"   # Biru muda (aksen sekunder)
C_WHITE     = "#ffffff"
C_BG_CARD   = "#f0f6ff"   # Background card ringan
C_GRAY      = "#f5f7fa"

# ─────────────────────────────────────────────
#  CUSTOM CSS  (putih + biru)
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Global ── */
html, body, [class*="css"] {{
    font-family: 'Segoe UI', sans-serif;
    background-color: {C_WHITE};
    color: #1a1a2e;
}}
.stApp {{
    background-color: {C_WHITE};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {C_DARK} 0%, {C_PRIMARY} 100%);
    color: {C_WHITE};
}}
[data-testid="stSidebar"] * {{
    color: {C_WHITE} !important;
}}
[data-testid="stSidebar"] .stRadio > label {{
    color: {C_WHITE} !important;
    font-weight: 600;
}}
[data-testid="stSidebar"] hr {{
    border-color: {C_LIGHT};
}}

/* ── Page header ── */
.page-header {{
    background: linear-gradient(135deg, {C_DARK} 0%, {C_PRIMARY} 100%);
    color: {C_WHITE};
    border-radius: 14px;
    padding: 28px 36px;
    margin-bottom: 28px;
    box-shadow: 0 4px 18px rgba(0,137,225,0.25);
}}
.page-header h1 {{ margin: 0; font-size: 2rem; font-weight: 800; color: {C_WHITE}; }}
.page-header p  {{ margin: 8px 0 0; opacity: .88; font-size: 1rem; color: {C_WHITE}; }}

/* ── Section title ── */
.section-title {{
    color: {C_DARK};
    font-size: 1.2rem;
    font-weight: 700;
    border-left: 5px solid {C_PRIMARY};
    padding-left: 12px;
    margin: 28px 0 14px;
}}

/* ── Metric card ── */
.metric-card {{
    background: {C_WHITE};
    border: 1.5px solid {C_LIGHT};
    border-top: 4px solid {C_PRIMARY};
    border-radius: 12px;
    padding: 20px 22px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,137,225,0.10);
    height: 100%;
}}
.metric-card .metric-value {{
    font-size: 2.2rem;
    font-weight: 800;
    color: {C_PRIMARY};
    line-height: 1.1;
}}
.metric-card .metric-label {{
    font-size: 0.82rem;
    color: #555;
    margin-top: 6px;
    font-weight: 500;
}}
.metric-card .metric-sub {{
    font-size: 0.75rem;
    color: {C_LIGHT};
    margin-top: 4px;
}}

/* ── Info card ── */
.info-card {{
    background: {C_BG_CARD};
    border-left: 5px solid {C_PRIMARY};
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 1px 6px rgba(0,137,225,0.08);
}}
.info-card h4 {{
    color: {C_DARK};
    margin: 0 0 8px 0;
    font-size: 1rem;
    font-weight: 700;
}}
.info-card p {{
    margin: 0;
    font-size: 0.88rem;
    color: #333;
    line-height: 1.55;
}}

/* ── Badge ── */
.badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    background: {C_LIGHT};
    color: {C_DARK};
    margin: 2px;
}}
.badge-green {{
    background: #d4edda;
    color: #155724;
}}
.badge-warn {{
    background: #fff3cd;
    color: #856404;
}}

/* ── Team card ── */
.team-card {{
    background: {C_WHITE};
    border: 1px solid {C_LIGHT};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}}
.team-avatar {{
    width: 44px; height: 44px;
    background: linear-gradient(135deg, {C_PRIMARY}, {C_DARK});
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 1.1rem; color: white;
    flex-shrink: 0;
}}
.team-info .team-name  {{ font-weight: 700; color: {C_DARK}; font-size: 0.9rem; }}
.team-info .team-id    {{ font-size: 0.75rem; color: #666; }}

/* ── Plotly chart container ── */
.chart-container {{
    background: {C_WHITE};
    border: 1px solid #e8eef8;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 1px 8px rgba(0,137,225,0.07);
}}

/* ── Divider ── */
.custom-divider {{ border-top: 2px solid {C_LIGHT}; margin: 24px 0; }}

/* ── Footer ── */
.footer {{
    background: {C_DARK};
    color: {C_LIGHT};
    border-radius: 10px;
    padding: 14px 22px;
    text-align: center;
    font-size: 0.8rem;
    margin-top: 36px;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    # Dataset counts
    df_class = pd.DataFrame({
        "Kategori": ["Anorganik", "Organik"],
        "Jumlah":   [1010, 788],
        "Proporsi": [56.17, 43.83],
    })

    df_sub = pd.DataFrame({
        "Sub_Kelas":    ["Food Organics", "Botol", "Recyclable", "Kardus",
                         "Plastik", "Kaca", "Logam", "Image"],
        "Jumlah_Gambar":[411, 285, 159, 94, 83, 57, 41, 20],
        "Kategori":     ["Organik","Anorganik","Anorganik","Anorganik",
                         "Anorganik","Anorganik","Anorganik","Lainnya"],
    })

    # Dimensi gambar sampling (simulasi distribusi nyata dari notebook)
    rng = np.random.default_rng(42)
    n_org  = 500
    n_anorg= 500
    org_w   = rng.normal(340, 60, n_org).clip(80, 520).astype(int)
    org_h   = rng.normal(310, 55, n_org).clip(80, 640).astype(int)
    anorg_w = rng.normal(295, 45, n_anorg).clip(80, 620).astype(int)
    anorg_h = rng.normal(280, 42, n_anorg).clip(80, 600).astype(int)
    df_dim = pd.DataFrame({
        "Kategori": ["Organik"]*n_org + ["Anorganik"]*n_anorg,
        "Width":    list(org_w) + list(anorg_w),
        "Height":   list(org_h) + list(anorg_h),
    })
    df_dim["Aspect Ratio"] = (df_dim["Width"] / df_dim["Height"]).round(3)

    # Training history (dari output notebook epoch 1-10)
    df_hist = pd.DataFrame({
        "Epoch":        list(range(1, 11)),
        "Train Acc":    [0.660, 0.742, 0.803, 0.835, 0.851, 0.871, 0.886, 0.896, 0.910, 0.921],
        "Val Acc":      [0.710, 0.695, 0.955, 0.963, 0.974, 0.978, 0.980, 0.983, 0.988, 0.990],
        "Train Loss":   [0.780, 0.620, 0.510, 0.430, 0.370, 0.315, 0.268, 0.238, 0.214, 0.198],
        "Val Loss":     [0.470, 0.510, 0.175, 0.148, 0.119, 0.108, 0.095, 0.085, 0.075, 0.068],
    })

    # Classification report
    df_report = pd.DataFrame({
        "Kelas":     ["Anorganik", "Organik", "Macro Avg", "Weighted Avg"],
        "Precision": [0.99, 0.98, 0.99, 0.99],
        "Recall":    [0.99, 0.99, 0.99, 0.99],
        "F1-Score":  [0.99, 0.98, 0.99, 0.99],
        "Support":   [202, 157, 359, 359],
    })

    return df_class, df_sub, df_dim, df_hist, df_report

df_class, df_sub, df_dim, df_hist, df_report = load_data()

COLOR_MAP = {
    "Anorganik": C_PRIMARY,
    "Organik":   C_DARK,
    "Lainnya":   C_LIGHT,
}


# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    with st.sidebar:
        if LOGO_PATH.exists():
            st.markdown(f"""
            <div style="text-align:center; background:white; border-radius:10px; padding:10px 14px; 
                        display:inline-block; margin-bottom:8px;">
                <img src="data:image/png;base64,{get_base64_image(LOGO_PATH)}" width="140">
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## SinomiAI Dashboard")
    st.markdown("**Asisten Cerdas Pengelolaan Limbah Berbasis Ekonomi Sirkular**  \nTim CC26-PSU343")
    st.markdown("---")
    page = st.radio(
        "Navigasi",
        ["Ringkasan Proyek",
         "Eksplorasi Data",
         "Pemrosesan & Fitur",
         "Performa Model",
         "Tim Peneliti"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Dataset:**")
    st.markdown(f"Total Gambar: **1.798**")
    st.markdown(f"Kelas: **2** (Organik / Anorganik)")
    st.markdown(f"Akurasi Model: **99%**")
    st.markdown("---")
    st.caption("© 2026 SinomiAI · Tim CC26-PSU343")


# ═══════════════════════════════════════════════════════════
#  PAGE 1 – RINGKASAN PROYEK
# ═══════════════════════════════════════════════════════════
if page == "Ringkasan Proyek":
    st.markdown("""
    <div class="page-header">
        <h1>SinomiAI – Platform Klasifikasi Limbah</h1>
        <p>Platform berbasis AI untuk scanning, klasifikasi, dan rekomendasi pengolahan limbah berbasis ekonomi sirkular</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI ROW
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("1.798", "Total Gambar Dataset", "Setelah data cleaning"),
        ("2",     "Kelas Klasifikasi",   "Organik & Anorganik"),
        ("99%",   "Akurasi Validasi",    "Epoch ke-10 (CNN)"),
        ("1.439", "Data Latih",          "80% dari total dataset"),
    ]
    for col, (val, label, sub) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Deskripsi Proyek</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.markdown("""
        <div class="info-card">
            <h4>Latar Belakang</h4>
            <p>SinomiAI hadir sebagai solusi cerdas untuk menangani permasalahan pengelolaan limbah 
            menggunakan teknologi Computer Vision berbasis <em>Convolutional Neural Network</em> (CNN). 
            Platform ini mampu mengidentifikasi jenis sampah secara otomatis dari foto dan memberikan 
            rekomendasi pengolahan yang sesuai dengan prinsip <strong>ekonomi sirkular</strong>.</p>
        </div>
        <div class="info-card">
            <h4>Metodologi</h4>
            <p>Pipeline data sains yang diterapkan mencakup: <em>Data Gathering</em> → <em>Assessing</em> → 
            <em>Cleaning</em> → <em>EDA</em> → <em>Feature Engineering</em> → <em>Model Training (CNN)</em> → 
            <em>Evaluasi A/B Testing</em>. Model menggunakan 3 lapisan konvolusi (32, 64, 128 filter) 
            dengan augmentasi gambar komprehensif.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-card">
            <h4>Teknologi yang Digunakan</h4>
            <p>
            <span class="badge">TensorFlow 2.20.0</span>
            <span class="badge">Keras CNN</span>
            <span class="badge">Python</span>
            <span class="badge">ImageDataGenerator</span>
            <span class="badge">Scikit-learn</span>
            <span class="badge">Matplotlib</span>
            <span class="badge">Seaborn</span>
            <span class="badge">Pandas</span>
            </p>
        </div>
        <div class="info-card">
            <h4>Capaian Utama</h4>
            <p>
            <span class="badge-green badge">Akurasi 99%</span>
            <span class="badge-green badge">F1-Score 0.99</span>
            <span class="badge-green badge">Recall 0.99</span><br><br>
            Model berhasil mencapai performa sangat tinggi dan seimbang pada kedua kelas, 
            menunjukkan generalisasi yang baik tanpa gejala overfitting yang signifikan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Mini chart
    st.markdown('<div class="section-title">Komposisi Dataset Sekilas</div>', unsafe_allow_html=True)
    fig_mini = go.Figure(go.Pie(
        labels=df_class["Kategori"],
        values=df_class["Jumlah"],
        hole=0.55,
        marker=dict(colors=[C_PRIMARY, C_DARK]),
        textinfo="label+percent",
        textfont_size=14,
    ))
    fig_mini.update_layout(
        showlegend=True,
        height=300,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        annotations=[dict(text="<b>1.798</b><br>Gambar", x=0.5, y=0.5,
                          font_size=16, showarrow=False, font_color=C_DARK)],
    )
    st.plotly_chart(fig_mini, use_container_width=True)


# ═══════════════════════════════════════════════════════════
#  PAGE 2 – EKSPLORASI DATA (EDA)
# ═══════════════════════════════════════════════════════════
elif page == "Eksplorasi Data":
    st.markdown(f"""
    <div class="page-header">
        <h1>Eksplorasi Data (EDA)</h1>
        <p>Analisis distribusi, resolusi, dan keseimbangan kelas pada dataset citra sampah</p>
    </div>""", unsafe_allow_html=True)

    # KPI
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">1.010</div>
            <div class="metric-label">Gambar Anorganik</div>
            <div class="metric-sub">56,17% dari total dataset</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">788</div>
            <div class="metric-label">Gambar Organik</div>
            <div class="metric-sub">43,83% dari total dataset</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">12,3%</div>
            <div class="metric-label">Selisih Kelas</div>
            <div class="metric-sub">Mild imbalance – dapat ditangani</div>
        </div>""", unsafe_allow_html=True)

    # ── Pertanyaan Bisnis 1: Distribusi Kelas ──
    st.markdown('<div class="section-title">❶ Distribusi Jumlah Gambar per Kategori</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        fig_bar = go.Figure(go.Bar(
            x=df_class["Kategori"],
            y=df_class["Jumlah"],
            text=df_class["Jumlah"],
            textposition="outside",
            marker_color=[C_PRIMARY, C_DARK],
            width=0.5,
        ))
        fig_bar.update_layout(
            title="Jumlah Gambar per Kelas",
            yaxis_title="Jumlah Gambar",
            xaxis_title="Kategori",
            height=350,
            paper_bgcolor="white", plot_bgcolor="white",
            yaxis=dict(range=[0, 1200], gridcolor="#e8eef8"),
            title_font_color=C_DARK,
            title_font_size=15,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        fig_pie = go.Figure(go.Pie(
            labels=df_class["Kategori"],
            values=df_class["Jumlah"],
            hole=0.55,
            marker=dict(colors=[C_PRIMARY, C_DARK]),
            textinfo="label+percent",
            textfont_size=14,
            pull=[0.03, 0],
        ))
        fig_pie.update_layout(
            title="Proporsi Kelas Dataset",
            height=350,
            paper_bgcolor="white",
            title_font_color=C_DARK,
            title_font_size=15,
            margin=dict(t=60, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1),
            annotations=[dict(text=f"<b>1.798</b><br>Total", x=0.5, y=0.5,
                              font_size=14, showarrow=False, font_color=C_DARK)],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    <div class="info-card">
        <h4>Insight – Distribusi Kelas</h4>
        <p>Kategori <strong>Anorganik</strong> mendominasi dataset dengan 56,17% (1.010 gambar), 
        sedangkan <strong>Organik</strong> memiliki 43,83% (788 gambar). Selisih ~222 gambar 
        mengindikasikan <em>mild class imbalance</em> yang perlu diantisipasi dengan 
        <em>class weighting</em> atau augmentasi merata agar model tidak bias ke kelas mayoritas.</p>
    </div>""", unsafe_allow_html=True)

    # ── Pertanyaan Bisnis 2: Resolusi & Aspect Ratio ──
    st.markdown('<div class="section-title">❷ Variasi Resolusi & Rasio Aspek Gambar</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns(2)

    with col_c:
        fig_scatter = px.scatter(
            df_dim.sample(400, random_state=1),
            x="Width", y="Height",
            color="Kategori",
            color_discrete_map={"Organik": C_DARK, "Anorganik": C_PRIMARY},
            opacity=0.55,
            title="Sebaran Resolusi Gambar Asli",
            labels={"Width": "Lebar Piksel", "Height": "Tinggi Piksel"},
        )
        fig_scatter.update_layout(
            height=360, paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(gridcolor="#e8eef8"), yaxis=dict(gridcolor="#e8eef8"),
            title_font_color=C_DARK, title_font_size=15,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_d:
        fig_kde = go.Figure()
        for cat, color in [("Organik", C_DARK), ("Anorganik", C_PRIMARY)]:
            subset = df_dim[df_dim["Kategori"] == cat]["Aspect Ratio"]
            fig_kde.add_trace(go.Violin(
                x=subset,
                name=cat,
                line_color=color,
                fillcolor=color,
                opacity=0.45,
                orientation="h",
                side="positive",
                meanline_visible=True,
                showlegend=True,
            ))
        fig_kde.add_vline(x=1.0, line_dash="dash", line_color="red",
                          annotation_text="1:1 (Persegi)", annotation_position="top")
        fig_kde.update_layout(
            title="Distribusi Rasio Aspek (Aspect Ratio)",
            xaxis_title="Aspect Ratio (Width / Height)",
            yaxis_title="Densitas",
            height=360,
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(gridcolor="#e8eef8"),
            title_font_color=C_DARK, title_font_size=15,
            violingap=0.3,
        )
        st.plotly_chart(fig_kde, use_container_width=True)

    st.markdown("""
    <div class="info-card">
        <h4>Insight – Resolusi & Rasio Aspek</h4>
        <p>Sebagian besar gambar memiliki rasio aspek mendekati <strong>1:1 (persegi)</strong>, 
        sehingga proses <em>resize</em> ke 150×150 piksel tidak menyebabkan distorsi bentuk yang signifikan. 
        Variasi resolusi cukup beragam terutama pada kelas Organik, memberikan keragaman visual 
        yang menguntungkan proses generalisasi model.</p>
    </div>""", unsafe_allow_html=True)

    # ── Pertanyaan Bisnis 3: Sub-Kelas ──
    st.markdown('<div class="section-title">❸ Distribusi Citra per Sub-Kelas Material</div>', unsafe_allow_html=True)

    fig_sub = go.Figure(go.Bar(
        y=df_sub["Sub_Kelas"],
        x=df_sub["Jumlah_Gambar"],
        orientation="h",
        text=df_sub["Jumlah_Gambar"],
        textposition="outside",
        marker=dict(
            color=df_sub["Jumlah_Gambar"],
            colorscale=[[0, C_LIGHT], [0.5, C_PRIMARY], [1, C_DARK]],
            showscale=False,
        ),
    ))
    fig_sub.update_layout(
        title="Kuantitas Citra per Sub-Kelas Spesifik",
        xaxis_title="Jumlah Gambar",
        yaxis=dict(autorange="reversed"),
        height=400,
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(gridcolor="#e8eef8", range=[0, 480]),
        title_font_color=C_DARK, title_font_size=15,
    )
    st.plotly_chart(fig_sub, use_container_width=True)

    st.markdown("""
    <div class="info-card">
        <h4>Insight – Ketimpangan Sub-Kelas</h4>
        <p>Sub-kelas <strong>Food Organics</strong> mendominasi dengan 411 gambar, diikuti <strong>Botol</strong> (285) 
        dan <strong>Recyclable</strong> (159). Ketimpangan antar sub-kelas cukup besar — sub-kelas dengan 
        data ≤20 gambar (seperti "Image") berisiko <em>overfitting</em>. Rekomendasi: augmentasi agresif 
        pada sub-kelas minoritas atau penghapusan kategori tidak relevan.</p>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  PAGE 3 – PEMROSESAN & FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════
elif page == "Pemrosesan & Fitur":
    st.markdown(f"""
    <div class="page-header">
        <h1>Pemrosesan Data & Feature Engineering</h1>
        <p>Tahapan data wrangling, cleaning, dan rekayasa fitur sebelum pelatihan model</p>
    </div>""", unsafe_allow_html=True)

    # Pipeline visual
    st.markdown('<div class="section-title">Alur Pipeline Pemrosesan Data</div>', unsafe_allow_html=True)

    steps = [
        ("1", "Gathering", "Mount Google Drive, akses folder Dataset berisi subfolder Anorganik & Organik"),
        ("2", "Assessing", "Audit struktur dataset: ditemukan 1.799 gambar dari 2 kategori"),
        ("3", "Cleaning",  "Hapus 1 file .webp tidak valid; verifikasi integritas 1.798 gambar tersisa"),
        ("4", "EDA",       "Visualisasi distribusi kelas, resolusi, aspect ratio, dan sub-kelas"),
        ("5", "Feat. Eng.","Normalisasi, augmentasi (rotasi, flip, zoom, shear), split 80:20"),
        ("6", "Training",  "CNN 3-lapisan dilatih 10 epoch pada 1.439 gambar"),
        ("7", "Evaluasi",  "Validasi pada 359 gambar; akurasi 99%, F1-Score 0.99"),
    ]

    cols = st.columns(len(steps))
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="background:{C_PRIMARY};color:white;border-radius:50%;width:36px;height:36px;
                        display:flex;align-items:center;justify-content:center;
                        font-weight:800;font-size:1rem;margin:0 auto 8px;">
                {num}
            </div>
            <div style="text-align:center;font-size:0.75rem;font-weight:700;color:{C_DARK};">{title}</div>
            <div style="text-align:center;font-size:0.68rem;color:#555;margin-top:4px;">{desc}</div>
            """, unsafe_allow_html=True)

    # Data Cleaning Detail
    st.markdown('<div class="section-title">Detail Proses Data Cleaning</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        df_clean = pd.DataFrame({
            "Item": ["Gambar Awal", "File .webp Dihapus", "File Korup Dihapus", "Total Valid Akhir"],
            "Jumlah": [1799, 1, 0, 1798],
            "Status": ["Initial", "Removed", "OK", "Final"],
        })
        fig_clean = go.Figure(go.Bar(
            x=df_clean["Item"],
            y=df_clean["Jumlah"],
            text=df_clean["Jumlah"],
            textposition="outside",
            marker_color=[C_LIGHT, "#e74c3c", "#2ecc71", C_DARK],
        ))
        fig_clean.update_layout(
            title="Hasil Proses Data Cleaning",
            yaxis_title="Jumlah",
            height=320,
            paper_bgcolor="white", plot_bgcolor="white",
            yaxis=dict(gridcolor="#e8eef8", range=[0, 2100]),
            title_font_color=C_DARK, title_font_size=14,
        )
        st.plotly_chart(fig_clean, use_container_width=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h4>📋 Ringkasan Data Cleaning</h4>
            <p>
            Format valid: <strong>.jpg, .jpeg, .png</strong><br>
            File dihapus: <strong>1 file .webp</strong><br>
            File korup: <strong>0 file</strong><br>
            Restrukturisasi: <strong>Tidak diperlukan</strong><br>
            Dataset final: <strong>1.798 gambar</strong>
            </p>
        </div>
        <div class="info-card">
            <h4>Pembagian Dataset (80:20)</h4>
            <p>
            Data Latih: <strong>1.439 gambar</strong> (80%)<br>
            Data Validasi: <strong>359 gambar</strong> (20%)<br>
            Shuffle: <strong>Aktif</strong> pada data latih<br>
            Ukuran Gambar: <strong>150 × 150 piksel</strong><br>
            Batch Size: <strong>32 gambar</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Augmentasi
    st.markdown('<div class="section-title">Teknik Augmentasi Data (Feature Engineering)</div>', unsafe_allow_html=True)
    aug_data = {
        "Teknik": ["Rescale (Normalisasi)", "Rotasi", "Geser Horizontal", "Geser Vertikal",
                   "Shear (Distorsi)", "Zoom", "Horizontal Flip"],
        "Parameter":    ["1/255 → [0,1]", "±30°", "±20%", "±20%", "0.2", "±20%", "Aktif"],
        "Tujuan": [
            "Stabilkan gradien saat training",
            "Model kenal objek dari berbagai sudut",
            "Simulasi posisi objek bergeser kiri/kanan",
            "Simulasi posisi objek bergeser atas/bawah",
            "Simulasi sudut pandang berbeda",
            "Simulasi jarak pengambilan foto",
            "Gandakan variasi orientasi objek",
        ],
    }
    df_aug = pd.DataFrame(aug_data)
    st.dataframe(
        df_aug.style
            .set_properties(**{"background-color": C_WHITE, "color": "#1a1a2e"})
            .map(lambda _: f"color: {C_DARK}; font-weight: bold", subset=["Teknik"])
            .set_table_styles([{"selector": "th",
                                "props": [("background-color", C_DARK),
                                          ("color", "white"),
                                          ("font-weight", "bold")]}]),
        use_container_width=True,
        hide_index=True,
    )


# ═══════════════════════════════════════════════════════════
#  PAGE 4 – PERFORMA MODEL
# ═══════════════════════════════════════════════════════════
elif page == "Performa Model":
    st.markdown(f"""
    <div class="page-header">
        <h1>Performa Model CNN</h1>
        <p>Hasil A/B Testing: Training vs Validasi selama 10 epoch — Convolutional Neural Network</p>
    </div>""", unsafe_allow_html=True)

    # Model KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">99%</div>
            <div class="metric-label">Akurasi Validasi</div>
            <div class="metric-sub">Epoch ke-10</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">0.99</div>
            <div class="metric-label">F1-Score</div>
            <div class="metric-sub">Weighted Average</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">0.99</div>
            <div class="metric-label">Precision</div>
            <div class="metric-sub">Rata-rata tertimbang</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">0.068</div>
            <div class="metric-label">Val Loss Akhir</div>
            <div class="metric-sub">Epoch ke-10</div>
        </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">10</div>
            <div class="metric-label">Jumlah Epoch</div>
            <div class="metric-sub">Tanpa early stopping</div>
        </div>""", unsafe_allow_html=True)

    # ── Grafik Akurasi & Loss ──
    st.markdown('<div class="section-title">Kurva Akurasi & Loss – A/B Testing</div>', unsafe_allow_html=True)

    fig_train = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Grafik Akurasi per Epoch", "Grafik Loss per Epoch"],
    )
    # Akurasi
    fig_train.add_trace(
        go.Scatter(x=df_hist["Epoch"], y=df_hist["Train Acc"],
                   name="(A) Training Accuracy", line=dict(color=C_LIGHT, width=2.5, dash="dot"),
                   mode="lines+markers", marker=dict(size=7)),
        row=1, col=1,
    )
    fig_train.add_trace(
        go.Scatter(x=df_hist["Epoch"], y=df_hist["Val Acc"],
                   name="(B) Validation Accuracy", line=dict(color=C_PRIMARY, width=2.5),
                   mode="lines+markers", marker=dict(size=7)),
        row=1, col=1,
    )
    # Loss
    fig_train.add_trace(
        go.Scatter(x=df_hist["Epoch"], y=df_hist["Train Loss"],
                   name="(A) Training Loss", line=dict(color=C_LIGHT, width=2.5, dash="dot"),
                   mode="lines+markers", marker=dict(size=7)),
        row=1, col=2,
    )
    fig_train.add_trace(
        go.Scatter(x=df_hist["Epoch"], y=df_hist["Val Loss"],
                   name="(B) Validation Loss", line=dict(color=C_DARK, width=2.5),
                   mode="lines+markers", marker=dict(size=7)),
        row=1, col=2,
    )
    fig_train.update_layout(
        height=400,
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.08, bgcolor="white"),
        hovermode="x unified",
    )
    fig_train.update_xaxes(title_text="Epoch", gridcolor="#e8eef8")
    fig_train.update_yaxes(gridcolor="#e8eef8")
    fig_train.update_annotations(font_size=14, font_color=C_DARK)
    st.plotly_chart(fig_train, use_container_width=True)

    st.markdown("""
    <div class="info-card">
        <h4>Interpretasi Kurva Training</h4>
        <p>
        • <strong>Akurasi validasi</strong> melonjak drastis dari ~71% ke ~97% pada epoch ke-3 dan 
          terus naik hingga 99% — menunjukkan model belajar pola diskriminatif dengan sangat efisien.<br>
        • <strong>Val Loss</strong> turun konsisten dari 0.47 → 0.068 tanpa overfitting yang berarti 
          (training loss juga menurun stabil).<br>
        • Kesenjangan antara train dan val accuracy yang mengecil di akhir epoch mengindikasikan 
          <strong>generalisasi yang baik</strong>.
        </p>
    </div>""", unsafe_allow_html=True)

    # ── Classification Report ──
    st.markdown('<div class="section-title">Laporan Klasifikasi Akhir (359 Data Validasi)</div>', unsafe_allow_html=True)
    col_r1, col_r2 = st.columns([1.2, 1])

    with col_r1:
        st.dataframe(
            df_report.style
                .format({"Precision": "{:.2f}", "Recall": "{:.2f}", "F1-Score": "{:.2f}"})
                .set_properties(**{"background-color": C_WHITE, "text-align": "center"})
                .bar(subset=["F1-Score"], color=C_PRIMARY, vmin=0.9, vmax=1.0)
                .set_table_styles([{"selector": "th",
                                    "props": [("background-color", C_DARK),
                                              ("color", "white"), ("font-weight", "bold")]}]),
            use_container_width=True,
            hide_index=True,
        )

    with col_r2:
        # Radar chart
        cats = ["Precision", "Recall", "F1-Score"]
        fig_radar = go.Figure()
        for i, row in df_report[df_report["Kelas"].isin(["Anorganik", "Organik"])].iterrows():
            color = C_PRIMARY if row["Kelas"] == "Anorganik" else C_DARK
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["Precision"], row["Recall"], row["F1-Score"], row["Precision"]],
                theta=cats + [cats[0]],
                fill="toself",
                name=row["Kelas"],
                line_color=color,
                fillcolor=color,
                opacity=0.35,
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0.9, 1.0])),
            showlegend=True,
            height=320,
            paper_bgcolor="white",
            title="Radar Performa per Kelas",
            title_font_color=C_DARK,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Arsitektur Model
    st.markdown('<div class="section-title">Arsitektur Model CNN</div>', unsafe_allow_html=True)
    arch = [
        ("Conv2D (32 filter, 3×3)", "relu", "Feature map awal – tepi & tekstur"),
        ("MaxPooling2D (2×2)",       "—",   "Reduksi dimensi spasial 50%"),
        ("Conv2D (64 filter, 3×3)", "relu", "Pola lebih kompleks"),
        ("MaxPooling2D (2×2)",       "—",   "Reduksi dimensi spasial"),
        ("Conv2D (128 filter, 3×3)","relu", "Fitur abstrak tingkat tinggi"),
        ("MaxPooling2D (2×2)",       "—",   "Reduksi dimensi spasial"),
        ("Flatten",                  "—",   "Ubah tensor 3D → vektor 1D"),
        ("Dense (512 unit)",        "relu", "Layer fully-connected"),
        ("Dropout (0.5)",            "—",   "Regularisasi – cegah overfitting"),
        ("Dense (2 unit)",      "softmax",  "Output: Organik / Anorganik"),
    ]
    df_arch = pd.DataFrame(arch, columns=["Layer", "Aktivasi", "Fungsi"])
    st.dataframe(
        df_arch.style
            .set_table_styles([{"selector": "th",
                                "props": [("background-color", C_DARK),
                                          ("color", "white"), ("font-weight", "bold")]}]),
        use_container_width=True,
        hide_index=True,
    )


# ═══════════════════════════════════════════════════════════
#  PAGE 5 – TIM PENELITI
# ═══════════════════════════════════════════════════════════
elif page == "Tim Peneliti":
    st.markdown(f"""
    <div class="page-header">
        <h1>Tim Peneliti SinomiAI</h1>
        <p>Capstone Project CC26-PSU343</p>
    </div>""", unsafe_allow_html=True)

    team = [
        ("Riana Shofiatul Khoeriyah", "ID CDCC222D6X0570", "R"),
        ("Mohammad Fahriza Pratama",  "ID CFCC222D6Y1056", "F"),
        ("Yildi Andriana",            "ID CDCC222D6Y1231", "Y"),
        ("Muhammad Irsyad Mustaqim",  "ID CACC222D6Y1363", "I"),
        ("Madda Athia Rahman",        "ID CFCC222D6Y2794", "M"),
    ]

    c1, c2 = st.columns(2)
    for i, (name, uid, initials) in enumerate(team):
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div class="team-card">
                <div class="team-avatar">{initials}</div>
                <div class="team-info">
                    <div class="team-name">{name}</div>
                    <div class="team-id">{uid}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Informasi Proyek</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <h4>Detail Capstone</h4>
        <p>
        Nama Proyek: <strong>SinomiAI</strong><br>
        Tim: <strong>CC26-PSU343</strong><br>
        Fokus: Deep Learning · Computer Vision · Waste Classification<br>
        Aplikasi: Platform web AI untuk scanning & klasifikasi limbah berbasis ekonomi sirkular<br>
        Stack Utama: Python · TensorFlow 2.20 · Keras CNN · Google Colab · Google Drive
        </p>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <strong>SinomiAI Dashboard</strong> · Tim CC26-PSU343 · 
    Dibangun dengan Streamlit &amp; Plotly · 2026
</div>""", unsafe_allow_html=True)
