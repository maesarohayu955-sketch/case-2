import os
import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Mengabaikan warning deprecation agar terminal dan UI bersih sempurna
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Profil Mahasiswa 2024",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CUSTOM CSS: MODERN, ELEGAN, & HARMONIS (DEEP INDIGO / TEAL / SLATE)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Creator Badge di Sidebar (Minimalis, Halus, & Elegan) */
    .creator-badge {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .creator-badge-icon {
        font-size: 1.25rem;
    }
    .creator-badge-text {
        font-size: 0.86rem;
        color: #1e293b;
        font-weight: 600;
        letter-spacing: 0.2px;
    }
    .creator-badge-nim {
        color: #4338ca;
        font-weight: 700;
    }

    /* Hero Header: Navy / Deep Indigo / Teal Gradien Profesional */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 55%, #0f766e 100%);
        border-radius: 16px;
        padding: 24px 30px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 20px -5px rgba(15, 23, 42, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #cbd5e1;
        margin: 6px 0 0 0;
        font-weight: 500;
    }
    .hero-pill {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #e2e8f0;
        backdrop-filter: blur(8px);
    }

    /* KPI Cards Layout & Responsive Typography */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    @media (max-width: 1200px) {
        .kpi-container { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
        .kpi-container { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 500px) {
        .kpi-container { grid-template-columns: 1fr; }
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        border-top: 4px solid #4338ca;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    }
    .kpi-card.indigo  { border-top-color: #4f46e5; }
    .kpi-card.teal    { border-top-color: #0d9488; }
    .kpi-card.violet  { border-top-color: #7c3aed; }
    .kpi-card.amber   { border-top-color: #d97706; }
    .kpi-card.emerald { border-top-color: #059669; }

    .kpi-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. PENJANAAN DATA SINTESIS (1.000 BARIS) & CACHING DATASET
# ==============================================================================
def create_student_dataset(num_records: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Menghasilkan 1.000 data profil mahasiswa sintetik yang realistis dan konsisten secara statistik."""
    np.random.seed(seed)

    jurusan_list = [
        "Teknik Informatika",
        "Sistem Informasi",
        "Manajemen",
        "Akuntansi",
        "Ilmu Komunikasi",
        "Desain Komunikasi Visual"
    ]
    jurusan_weights = [0.22, 0.20, 0.20, 0.16, 0.12, 0.10]

    semesters = np.arange(1, 9)
    # Distribusi alami piramida mahasiswa (sedikit lebih padat di semester awal)
    semester_weights = [0.15, 0.15, 0.14, 0.14, 0.12, 0.11, 0.10, 0.09]

    records = []
    for _ in range(num_records):
        jur = np.random.choice(jurusan_list, p=jurusan_weights)
        sem = int(np.random.choice(semesters, p=semester_weights))

        # Usia bertambah konsisten sejalan jenjang semester (r ~ 0.85)
        base_age = 17.5 + (sem * 0.5)
        raw_age = base_age + np.random.normal(0.3, 0.6)
        usia = int(np.clip(np.round(raw_age), 18, 25))

        # IPK berdistribusi normal realistis (skala 2.05 s.d. 4.00)
        mean_ipk = 3.32
        raw_ipk = np.random.normal(mean_ipk, 0.36)
        ipk = float(np.round(np.clip(raw_ipk, 2.05, 4.00), 2))

        records.append({
            "Jurusan": jur,
            "Semester": sem,
            "IPK": ipk,
            "Usia": usia
        })

    df = pd.DataFrame(records).sort_values(by=["Semester", "Jurusan"]).reset_index(drop=True)
    return df


@st.cache_data
def load_student_dataset(filepath: str = "dataset_profil_mahasiswa_1000.csv") -> pd.DataFrame:
    """Membaca dataset profil mahasiswa atau membuatnya otomatis jika belum ada / kurang dari 1.000 baris."""
    need_create = False
    if not os.path.exists(filepath):
        need_create = True
    else:
        try:
            df_exist = pd.read_csv(filepath)
            if len(df_exist) < 1000:
                need_create = True
        except Exception:
            need_create = True

    if need_create:
        df = create_student_dataset(1000, seed=42)
        df.to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)

    df["Semester_Label"] = "Semester " + df["Semester"].astype(str)
    df["Kategori_IPK"] = pd.cut(
        df["IPK"],
        bins=[0, 2.75, 3.00, 3.50, 4.00],
        labels=["Cukup (< 2.76)", "Memuaskan (2.76 - 3.00)", "Sangat Memuaskan (3.01 - 3.50)", "Dengan Pujian / Cum Laude (≥ 3.50)"],
        include_lowest=True
    )
    return df


df_raw = load_student_dataset()


# ==============================================================================
# 4. SIDEBAR: IDENTITAS PEMBUAT (MINIMALIS & ELEGAN) & FILTER INTERAKTIF
# ==============================================================================
with st.sidebar:
    # 🎓 CUKUP TAMPILKAN SATU KALI SAJA: Badge Profil Minimalis & Elegan
    st.markdown("""
    <div class="creator-badge">
        <span class="creator-badge-icon">🎓</span>
        <span class="creator-badge-text">
            <strong>Ayu Maesaroh</strong> • <span class="creator-badge-nim">NIM 241041010</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Parameter Filter")
    st.caption("Gunakan filter di bawah untuk memfokuskan analisis data:")

    # Tombol Reset Filter
    if st.button("🔄 Reset Semua Filter"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")

    # Filter 1: Jurusan (Kategorik Nominal)
    all_jurusan = sorted(df_raw["Jurusan"].unique().tolist())
    pilih_semua_jurusan = st.checkbox("Pilih Semua Jurusan", value=True)

    if pilih_semua_jurusan:
        selected_jurusan = st.multiselect("Program Studi / Jurusan:", options=all_jurusan, default=all_jurusan)
    else:
        selected_jurusan = st.multiselect("Program Studi / Jurusan:", options=all_jurusan, default=[all_jurusan[0]])

    # Filter 2: Semester (Kategorik Ordinal: 1 s.d. 8)
    min_sem, max_sem = int(df_raw["Semester"].min()), int(df_raw["Semester"].max())
    selected_semester = st.slider("Rentang Semester (Ordinal):", min_value=min_sem, max_value=max_sem, value=(min_sem, max_sem))

    # Filter 3: IPK (Numerik Kontinu)
    min_ipk_val = float(df_raw["IPK"].min())
    max_ipk_val = float(df_raw["IPK"].max())
    selected_ipk = st.slider("Rentang Nilai IPK:", min_value=2.00, max_value=4.00, value=(min_ipk_val, max_ipk_val), step=0.05)

    st.markdown("---")
    st.markdown("### 📌 Ringkasan Basis Data")
    st.caption(f"• **Total Sampel:** {len(df_raw):,} Mahasiswa")
    st.caption("• **Jenjang Pendidikan:** Strata 1 (S1)")
    st.caption("• **Variabel Utama:** Nominal, Ordinal, & Rasio")


# ==============================================================================
# 5. FILTERING LOGIC
# ==============================================================================
df_filtered = df_raw[
    (df_raw["Jurusan"].isin(selected_jurusan)) &
    (df_raw["Semester"] >= selected_semester[0]) &
    (df_raw["Semester"] <= selected_semester[1]) &
    (df_raw["IPK"] >= selected_ipk[0]) &
    (df_raw["IPK"] <= selected_ipk[1])
].copy()

if df_filtered.empty:
    st.warning("⚠️ Tidak ada catatan mahasiswa yang cocok dengan parameter filter. Silakan sesuaikan kembali filter di sidebar.")
    st.stop()


# ==============================================================================
# 6. HERO HEADER (RINGKAS & PROFESIONAL)
# ==============================================================================
st.markdown(f"""
<div class="hero-container">
    <div>
        <h1 class="hero-title">🎓 Executive Student Profile Analytics</h1>
        <p class="hero-subtitle">Bedah Kasus 2: Analisis Karakteristik Akademik, Demografi Usia, dan Progresi Semester Mahasiswa</p>
    </div>
    <div class="hero-pill">
        📊 Data Aktif: {len(df_filtered):,} dari {len(df_raw):,} Mahasiswa
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 7. KPI METRICS CARDS: FORMAT RAPI, TEGAS, & TIDAK TERPOTONG
# ==============================================================================
total_mhs = len(df_filtered)
mean_ipk = df_filtered["IPK"].mean()
median_ipk = df_filtered["IPK"].median()
mean_usia = df_filtered["Usia"].mean()
cumlaude_count = (df_filtered["IPK"] >= 3.50).sum()
cumlaude_pct = (cumlaude_count / total_mhs) * 100

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card indigo">
        <div class="kpi-label">👥 Total Mahasiswa</div>
        <div class="kpi-value">{total_mhs:,}</div>
        <div class="kpi-sub">Populasi aktif terfilter</div>
    </div>
    <div class="kpi-card teal">
        <div class="kpi-label">🎯 Rata-Rata IPK</div>
        <div class="kpi-value">{mean_ipk:.2f}</div>
        <div class="kpi-sub">Delta {mean_ipk - 3.00:+.2f} vs Standar 3.00</div>
    </div>
    <div class="kpi-card violet">
        <div class="kpi-label">📊 Median IPK</div>
        <div class="kpi-value">{median_ipk:.2f}</div>
        <div class="kpi-sub">Titik tengah sebaran nilai</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">🎂 Rata-Rata Usia</div>
        <div class="kpi-value">{mean_usia:.1f} Thn</div>
        <div class="kpi-sub">Rentang {df_filtered['Usia'].min()} – {df_filtered['Usia'].max()} tahun</div>
    </div>
    <div class="kpi-card emerald">
        <div class="kpi-label">🏅 Cum Laude (≥ 3.50)</div>
        <div class="kpi-value">{cumlaude_pct:.1f}%</div>
        <div class="kpi-sub">{cumlaude_count:,} mahasiswa berprestasi</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 8. TAB VISUALISASI INTERAKTIF
# ==============================================================================
tab_ordinal, tab_nominal, tab_kontinu, tab_table = st.tabs([
    "📈 1. Distribusi Ordinal (Semester 1–8)",
    "🏛️ 2. Program Studi (Nominal)",
    "📦 3. Sebaran Numerik Kontinu (IPK & Usia)",
    "📋 4. Dataframe Interaktif & Export"
])


# ------------------------------------------------------------------------------
# TAB 1: KATEGORIK ORDINAL (SEMESTER BERURUTAN)
# ------------------------------------------------------------------------------
with tab_ordinal:
    st.markdown("#### Analisis Variabel Kategorik Ordinal: Progresi Semester Berurutan (1 s.d. 8)")
    st.caption("Data semester memiliki hierarki bertingkat alami yang disajikan berurutan secara kronologis.")

    col_o1, col_o2 = st.columns([3, 2])

    with col_o1:
        st.markdown("**A. Distribusi Jumlah Mahasiswa per Semester (Berurutan)**")
        sem_agg = df_filtered.groupby(["Semester", "Semester_Label"], as_index=False).size()
        sem_agg = sem_agg.sort_values(by="Semester").reset_index(drop=True)
        sem_agg.rename(columns={"size": "Jumlah Mahasiswa"}, inplace=True)
        sem_agg["Persentase"] = (sem_agg["Jumlah Mahasiswa"] / sem_agg["Jumlah Mahasiswa"].sum()) * 100

        fig_sem = px.bar(
            sem_agg,
            x="Semester_Label",
            y="Jumlah Mahasiswa",
            text="Jumlah Mahasiswa",
            color="Semester",
            color_continuous_scale="Tealgrn",
            labels={"Semester_Label": "Jenjang Semester (Ordinal)", "Jumlah Mahasiswa": "Jumlah Mahasiswa"}
        )
        fig_sem.update_traces(
            texttemplate="%{text} org<br>(%{customdata[0]:.1f}%)",
            textposition="outside",
            customdata=sem_agg[["Persentase"]].values,
            hovertemplate="<b>%{x}</b><br>Jumlah: %{y:,} Mahasiswa (%{customdata[0]:.1f}%)<extra></extra>"
        )
        fig_sem.update_layout(
            height=410,
            autosize=True,
            coloraxis_showscale=False,
            xaxis=dict(categoryorder="array", categoryarray=["Semester " + str(i) for i in range(1, 9)]),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=20, b=30)
        )
        st.plotly_chart(fig_sem, theme="streamlit")

    with col_o2:
        st.markdown("**B. Komposisi Semester Berdasarkan Program Studi**")
        fig_stack = px.bar(
            df_filtered,
            x="Semester",
            color="Jurusan",
            labels={"Semester": "Semester", "count": "Jumlah Mahasiswa"},
            barmode="stack",
            color_discrete_sequence=["#4f46e5", "#0d9488", "#d97706", "#7c3aed", "#e11d48", "#0284c7"]
        )
        fig_stack.update_layout(
            height=410,
            autosize=True,
            xaxis=dict(tickmode="linear", tick0=1, dtick=1),
            legend=dict(orientation="h", y=-0.25, x=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=20, b=45)
        )
        st.plotly_chart(fig_stack, theme="streamlit")


# ------------------------------------------------------------------------------
# TAB 2: KATEGORIK NOMINAL (JURUSAN / PROGRAM STUDI)
# ------------------------------------------------------------------------------
with tab_nominal:
    st.markdown("#### Analisis Variabel Kategorik Nominal: Jurusan / Program Studi")
    st.caption("Evaluasi proporsi mahasiswa dan komparasi performa akademik per program studi.")

    col_n1, col_n2 = st.columns(2)

    with col_n1:
        st.markdown("**A. Proporsi Mahasiswa per Program Studi (Donut Chart)**")
        jur_dist = df_filtered["Jurusan"].value_counts().reset_index()
        jur_dist.columns = ["Jurusan", "Total"]

        palette_jur = ["#4f46e5", "#0d9488", "#d97706", "#7c3aed", "#e11d48", "#0284c7"]
        fig_donut_jur = px.pie(
            jur_dist,
            names="Jurusan",
            values="Total",
            hole=0.48,
            color="Jurusan",
            color_discrete_sequence=palette_jur
        )
        fig_donut_jur.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Mahasiswa: %{value:,} Orang (%{percent})<extra></extra>"
        )
        fig_donut_jur.update_layout(
            height=400,
            autosize=True,
            showlegend=True,
            legend=dict(orientation="h", y=-0.15),
            margin=dict(l=15, r=15, t=20, b=30),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_donut_jur, theme="streamlit")

    with col_n2:
        st.markdown("**B. Komparasi Rata-rata IPK per Program Studi**")
        jur_ipk = df_filtered.groupby("Jurusan", as_index=False).agg(
            Mean_IPK=("IPK", "mean"),
            Median_IPK=("IPK", "median")
        ).sort_values(by="Mean_IPK", ascending=True)

        fig_bar_ipk = px.bar(
            jur_ipk,
            x="Mean_IPK",
            y="Jurusan",
            orientation="h",
            color="Mean_IPK",
            color_continuous_scale="Viridis",
            text="Mean_IPK",
            labels={"Mean_IPK": "Rata-rata IPK", "Jurusan": "Program Studi"}
        )
        fig_bar_ipk.update_traces(texttemplate="%{x:.3f}", textposition="inside")
        fig_bar_ipk.add_vline(x=mean_ipk, line_dash="dash", line_color="#ef4444", annotation_text=f"Rata-rata Kampus ({mean_ipk:.2f})")
        fig_bar_ipk.update_layout(
            height=400,
            autosize=True,
            coloraxis_showscale=False,
            margin=dict(l=15, r=15, t=20, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bar_ipk, theme="streamlit")


# ------------------------------------------------------------------------------
# TAB 3: NUMERIK KONTINU (IPK & USIA)
# ------------------------------------------------------------------------------
with tab_kontinu:
    st.markdown("#### Analisis Variabel Numerik Kontinu: Sebaran Nilai IPK & Usia")
    st.caption("Pemeriksaan central tendency, rentang interkuartil (IQR), dan identifikasi nilai ekstrem (outlier).")

    col_k1, col_k2 = st.columns(2)

    with col_k1:
        st.markdown("**A. Box Plot Distribusi IPK per Jurusan (Deteksi Outlier)**")
        fig_box_ipk = px.box(
            df_filtered,
            x="Jurusan",
            y="IPK",
            color="Jurusan",
            points="outliers",
            color_discrete_sequence=palette_jur,
            labels={"IPK": "Indeks Prestasi Kumulatif", "Jurusan": "Program Studi"}
        )
        fig_box_ipk.add_hline(y=3.50, line_dash="dash", line_color="#059669", annotation_text="Batas Cum Laude (3.50)")
        fig_box_ipk.update_layout(
            height=410,
            autosize=True,
            showlegend=False,
            plot_bgcolor="rgba(248, 250, 252, 0.6)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=20, b=30)
        )
        st.plotly_chart(fig_box_ipk, theme="streamlit")
        st.caption("ℹ️ *Titik di luar whisker (1.5 × IQR) menandai mahasiswa outlier dengan nilai khusus yang memerlukan perhatian pembimbing.*")

    with col_k2:
        st.markdown("**B. Histogram Distribusi Nilai IPK**")
        fig_hist_ipk = px.histogram(
            df_filtered,
            x="IPK",
            nbins=30,
            marginal="box",
            color_discrete_sequence=["#4f46e5"],
            labels={"IPK": "Indeks Prestasi Kumulatif (IPK)", "count": "Jumlah Mahasiswa"}
        )
        fig_hist_ipk.update_layout(
            height=410,
            autosize=True,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=20, b=20)
        )
        st.plotly_chart(fig_hist_ipk, theme="streamlit")
        st.caption("ℹ️ *Bentuk histogram memperlihatkan kurva lonceng normal (Gaussian) berpusat di rata-rata 3.32.*")

    st.markdown("---")
    st.markdown("**C. Scatter Plot: Hubungan Usia vs IPK (Dengan Garis Tren OLS)**")
    col_sc1, col_sc2 = st.columns([3, 2])

    with col_sc1:
        fig_scatter = px.scatter(
            df_filtered,
            x="Usia",
            y="IPK",
            color="Jurusan",
            size="Semester",
            trendline="ols",
            hover_data=["Semester", "Jurusan"],
            color_discrete_sequence=palette_jur,
            labels={"Usia": "Usia Mahasiswa (Tahun)", "IPK": "IPK Mahasiswa"}
        )
        fig_scatter.update_layout(
            height=380,
            autosize=True,
            legend=dict(orientation="h", y=-0.2),
            plot_bgcolor="rgba(248, 250, 252, 0.6)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=15, b=40)
        )
        st.plotly_chart(fig_scatter, theme="streamlit")

    with col_sc2:
        fig_box_age = px.box(
            df_filtered,
            x="Semester_Label",
            y="Usia",
            color="Semester_Label",
            color_discrete_sequence=px.colors.sequential.Tealgrn,
            labels={"Semester_Label": "Semester", "Usia": "Usia (Tahun)"}
        )
        fig_box_age.update_layout(
            height=380,
            autosize=True,
            showlegend=False,
            xaxis=dict(categoryorder="array", categoryarray=["Semester " + str(i) for i in range(1, 9)]),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=15, b=20)
        )
        st.plotly_chart(fig_box_age, theme="streamlit")


# ------------------------------------------------------------------------------
# TAB 4: DATAFRAME INTERAKTIF & EXPORT CSV
# ------------------------------------------------------------------------------
with tab_table:
    st.markdown("#### Basis Data Profil Mahasiswa Terfilter")
    st.caption(f"Menampilkan {len(df_filtered):,} rekaman mahasiswa yang sesuai dengan kriteria aktif.")

    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search_query = st.text_input("🔍 Cari Cepat (Jurusan / Predikat):", placeholder="Ketik kata kunci pencarian...")
    with col_s2:
        st.write("")
        st.write("")
        csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Unduh Data CSV",
            data=csv_bytes,
            file_name=f"profil_mahasiswa_filtered_{len(df_filtered)}_records.csv",
            mime="text/csv"
        )

    if search_query:
        df_display = df_filtered[
            df_filtered["Jurusan"].str.contains(search_query, case=False, na=False) |
            df_filtered["Kategori_IPK"].astype(str).str.contains(search_query, case=False, na=False)
        ]
    else:
        df_display = df_filtered

    tabel_view = df_display[["Jurusan", "Semester", "IPK", "Usia", "Kategori_IPK"]].copy()
    st.dataframe(
        tabel_view.style.format({
            "IPK": "{:.2f}",
            "Semester": "Semester {:d}",
            "Usia": "{:d} Tahun"
        }),
        height=420
    )

# ==============================================================================
# 9. FOOTER BERSIH & FORMAL
# ==============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94a3b8; font-size: 0.85rem; padding-bottom: 15px;'>"
    "Bedah Kasus 2: Dataset Profil Mahasiswa • Sistem Analisis Data & Visualisasi Interaktif Akademik"
    "</div>",
    unsafe_allow_html=True
)
