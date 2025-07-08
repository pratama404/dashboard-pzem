import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ----------------- KONFIGURASI HALAMAN -----------------
st.set_page_config(
    page_title="Dashboard Analisis Energi",
    page_icon="💡",
    layout="wide",
)

# ------------------------------------------------------------------------------------
# 🔧 PENGATURAN KOLOM (SESUAIKAN JIKA NAMA DI SHEET BERBEDA)
# ------------------------------------------------------------------------------------
TIMESTAMP_COL = 'Timestamp'
V1_COL, I1_COL, P1_COL, PF1_COL = 'V1 (V)', 'I1 (A)', 'P1 (W)', 'PF1'
V2_COL, I2_COL, P2_COL, PF2_COL = 'V2 (V)', 'I2 (A)', 'P2 (W)', 'PF2'
V3_COL, I3_COL, P3_COL, PF3_COL = 'V3 (V)', 'I3 (A)', 'P3 (W)', 'PF3'
# ------------------------------------------------------------------------------------

# --- URL Google Sheet ---
SHEET_ID = "1UGRvNLl3MS75xgkHwNksAWEfG6VQELXChcO3POtwT7o"
SHEET_GID = "892185207" 
URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={SHEET_GID}'


@st.cache_data(ttl=60)
def load_data(url):
    """Membaca data dari URL Google Sheet dan memprosesnya."""
    try:
        df = pd.read_csv(url, decimal=',')
        df.dropna(how='all', inplace=True)
        df[TIMESTAMP_COL] = pd.to_datetime(df[TIMESTAMP_COL], errors='coerce')
        
        numeric_cols = [
            V1_COL, I1_COL, P1_COL, PF1_COL, V2_COL, I2_COL, P2_COL, PF2_COL, 
            V3_COL, I3_COL, P3_COL, PF3_COL
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        df.dropna(subset=[TIMESTAMP_COL], inplace=True)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data. Error: {e}")
        return pd.DataFrame()

# --- Memuat Data ---
df = load_data(URL)

# ====================================================================================
# --- SIDEBAR UNTUK FILTER ---
# ====================================================================================
st.sidebar.header("⚙️ Filter Tampilan")

if not df.empty:
    min_date = df[TIMESTAMP_COL].min().date()
    max_date = df[TIMESTAMP_COL].max().date()
    
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )
    
    start_date, end_date = date_range

    fasa_options = {
        "PZEM 1 (Fasa R)": (V1_COL, I1_COL, P1_COL, PF1_COL),
        "PZEM 2 (Fasa S)": (V2_COL, I2_COL, P2_COL, PF2_COL),
        "PZEM 3 (Fasa T)": (V3_COL, I3_COL, P3_COL, PF3_COL)
    }
    selected_fasa = st.sidebar.multiselect(
        "Pilih Fasa untuk Ditampilkan",
        options=list(fasa_options.keys()),
        default=list(fasa_options.keys())
    )

    df_filtered = df[
        (df[TIMESTAMP_COL].dt.date >= start_date) & 
        (df[TIMESTAMP_COL].dt.date <= end_date)
    ]
else:
    st.sidebar.warning("Data kosong, filter tidak dapat ditampilkan.")
    df_filtered = pd.DataFrame()

# ====================================================================================
# --- HALAMAN UTAMA DASHBOARD ---
# ====================================================================================
st.title("💡 Dashboard Analisis & Monitoring Energi")

if not df_filtered.empty and selected_fasa:
    
    v_cols_selected = [fasa_options[f][0] for f in selected_fasa]
    i_cols_selected = [fasa_options[f][1] for f in selected_fasa]
    p_cols_selected = [fasa_options[f][2] for f in selected_fasa]
    pf_cols_selected = [fasa_options[f][3] for f in selected_fasa]

    # --- BAGIAN RINGKASAN DATA TERAKHIR (KPI) ---
    st.markdown("### 📈 Ringkasan Data Terakhir (Sesuai Filter)")
    last_row = df_filtered.iloc[-1]
    
    kpi_cols = st.columns(len(selected_fasa))
    for i, fasa in enumerate(selected_fasa):
        with kpi_cols[i]:
            st.subheader(fasa)
            v_col, i_col, p_col, _ = fasa_options[fasa]
            st.metric("Tegangan", f"{last_row.get(v_col, 0):.2f} V")
            st.metric("Arus", f"{last_row.get(i_col, 0):.3f} A")
            st.metric("Daya Aktif", f"{last_row.get(p_col, 0):.2f} W")

    st.markdown("---") # Garis pemisah
    
    # --- PENJELASAN GRAFIK MONITORING TIME SERIES ---
    st.markdown("### 📉 Grafik Monitoring Time Series")
    st.info(
        """
        Bagian ini menampilkan bagaimana nilai-nilai kelistrikan (Tegangan, Arus, Daya, dan Faktor Daya) berubah dari waktu ke waktu.
        - **Tujuan**: Untuk memantau tren, mendeteksi lonjakan, penurunan, atau anomali lain secara visual.
        - **Gunakan Filter**: Anda dapat mengubah rentang tanggal atau memilih fasa tertentu di sidebar untuk fokus pada periode yang diinginkan.
        """
    )
    
    tab1, tab2, tab3, tab4 = st.tabs(["Tegangan", "Arus", "Daya", "Faktor Daya"])
    
    with tab1:
        st.plotly_chart(px.line(df_filtered, x=TIMESTAMP_COL, y=v_cols_selected, title="Monitoring Tegangan"), use_container_width=True)
    with tab2:
        st.plotly_chart(px.line(df_filtered, x=TIMESTAMP_COL, y=i_cols_selected, title="Monitoring Arus"), use_container_width=True)
    with tab3:
        st.plotly_chart(px.line(df_filtered, x=TIMESTAMP_COL, y=p_cols_selected, title="Monitoring Daya Aktif"), use_container_width=True)
    with tab4:
        fig_pf = px.line(df_filtered, x=TIMESTAMP_COL, y=pf_cols_selected, title="Monitoring Faktor Daya")
        fig_pf.update_yaxes(range=[0.7, 1])
        st.plotly_chart(fig_pf, use_container_width=True)
        
    st.markdown("---") # Garis pemisah
    
    # --- PENJELASAN ANALISIS DATA LEBIH LANJUT ---
    st.markdown("### 🔬 Analisis Data Lebih Lanjut")
    
    tab_dist, tab_pq = st.tabs(["Distribusi Data (Histogram)", "Segitiga Daya (P-Q Plot)"])
    
    with tab_dist:
        st.subheader("Distribusi Nilai Tegangan dan Arus")
        st.markdown(
            """
            **Histogram** menunjukkan seberapa sering suatu nilai muncul dalam rentang data yang Anda filter.
            - **Kegunaan**: Untuk melihat stabilitas sistem.
                - **Grafik Tinggi & Ramping**: Menandakan nilai sangat stabil dan konsisten (contoh: tegangan selalu di sekitar 220V).
                - **Grafik Lebar & Pendek**: Menandakan nilai sering berfluktuasi.
            - **Box Plot (di atas histogram)**: Menunjukkan ringkasan statistik: nilai minimum, maksimum, median (garis tengah), dan kuartil.
            """
        )
        col_dist1, col_dist2 = st.columns(2)
        with col_dist1:
            fig_dist_v = px.histogram(df_filtered, x=v_cols_selected, marginal="box", nbins=50, title="Distribusi Tegangan")
            st.plotly_chart(fig_dist_v, use_container_width=True)
        with col_dist2:
            fig_dist_i = px.histogram(df_filtered, x=i_cols_selected, marginal="box", nbins=50, title="Distribusi Arus")
            st.plotly_chart(fig_dist_i, use_container_width=True)

    with tab_pq:
        st.subheader("Analisis Segitiga Daya")
        st.markdown(
            """
            **Plot P-Q** memvisualisasikan hubungan antara **Daya Aktif (P)**, yang melakukan kerja nyata, dan **Daya Reaktif (Q)**, yang dibutuhkan untuk membangun medan magnet/listrik pada beban induktif/kapasitif.
            - **Sumbu X (Daya Aktif - P)**: Semakin ke kanan, semakin besar daya yang digunakan untuk kerja.
            - **Sumbu Y (Daya Reaktif - Q)**: Semakin ke atas, semakin besar daya reaktif yang dibutuhkan.
            - **Tujuan**: Menganalisis **Faktor Daya (PF)** secara visual. Titik-titik yang mendekati sumbu X (nilai Q kecil) menunjukkan PF yang baik (mendekati 1), yang berarti penggunaan energi lebih efisien.
            """
        )
        fig_pq = px.scatter(title="Plot Daya Aktif (P) vs Daya Reaktif (Q)")
        for fasa in selected_fasa:
            p_col = fasa_options[fasa][2]
            pf_col = fasa_options[fasa][3]
            q_values = df_filtered[p_col] * np.tan(np.arccos(df_filtered[pf_col]))
            fig_pq.add_scatter(x=df_filtered[p_col], y=q_values, mode='markers', name=fasa)
        
        fig_pq.update_xaxes(title_text="Daya Aktif (P) in Watts")
        fig_pq.update_yaxes(title_text="Daya Reaktif (Q) in VAR")
        st.plotly_chart(fig_pq, use_container_width=True)

    with st.expander("Tampilkan Data Mentah Terfilter"):
        st.dataframe(df_filtered)
else:
    st.warning("Data tidak dapat ditampilkan. Periksa filter atau sumber data Anda.")