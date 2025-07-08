# Implementasi Sistem Logger dan Proteksi pada Panel Kontrol Laboratorium Navigasi dan Komunikasi

## 🚀 Akses Dashboard

**Dashboard monitoring dapat diakses secara langsung melalui link berikut:**

[**https://dashboard-pzem.streamlit.app/**](https://dashboard-pzem.streamlit.app/)

---

## 📜 Deskripsi Proyek

Proyek ini bertujuan untuk merancang dan mengimplementasikan sebuah sistem **data logger** dan **dashboard monitoring** secara *real-time* untuk panel kontrol di Laboratorium Navigasi dan Komunikasi. Sistem ini secara kontinu mencatat parameter-parameter kelistrikan penting seperti **Tegangan (V)**, **Arus (A)**, **Daya (W)**, dan **Faktor Daya (PF)** dari tiga fasa yang berbeda (R, S, T) menggunakan sensor PZEM.

Data yang tercatat kemudian dikirim ke Google Sheets dan divisualisasikan melalui sebuah **dashboard interaktif** yang dibangun menggunakan **Streamlit**. Dashboard ini tidak hanya berfungsi sebagai alat monitoring, tetapi juga sebagai alat analisis untuk memahami kesehatan dan efisiensi sistem kelistrikan laboratorium.

**Teknologi yang Digunakan:**
- **Sensor**: PZEM-004T
- **Mikrokontroler**: (Sebutkan di sini, misal: ESP32, NodeMCU)
- **Penyimpanan Data**: Google Sheets
- **Framework Dashboard**: Streamlit (Python)
- **Deployment**: Streamlit Community Cloud

---

## 📊 Dashboard Monitoring & Analisis

Dashboard ini dirancang untuk memberikan wawasan mendalam mengenai kondisi kelistrikan panel kontrol. Berikut adalah penjelasan untuk setiap komponen visualisasi yang ada di dalam dashboard:

### ⚙️ Panel Filter
Di sisi kiri dashboard, terdapat panel filter yang memungkinkan pengguna untuk:
1.  **Memilih Rentang Tanggal**: Menganalisis data pada periode waktu tertentu, misalnya hanya data hari ini, minggu lalu, atau pada saat terjadi anomali.
2.  **Memilih Fasa**: Fokus pada satu atau lebih fasa (R/S/T) untuk perbandingan atau analisis yang lebih spesifik.

### 📈 Ringkasan Data Terakhir (KPI)
Bagian ini menampilkan nilai-nilai terukur paling akhir dari data yang telah difilter. Tujuannya adalah untuk memberikan gambaran cepat (*at-a-glance*) mengenai kondisi sistem saat ini.

### 📉 Grafik Monitoring Time Series
Visualisasi ini adalah inti dari fungsi monitoring, menampilkan bagaimana parameter kelistrikan berubah seiring waktu.
-   **Tujuan**:
    -   **Monitoring Tren**: Melihat pola penggunaan energi harian, mingguan, atau bulanan.
    -   **Deteksi Anomali**: Mengidentifikasi lonjakan atau penurunan tegangan/arus yang tidak wajar yang bisa mengindikasikan adanya masalah pada peralatan atau jaringan.
    -   **Analisis Beban**: Memahami kapan beban puncak (*peak load*) terjadi di laboratorium.

### 🔬 Analisis Data Lebih Lanjut

#### 1. Distribusi Data (Histogram)
Histogram menunjukkan frekuensi kemunculan suatu nilai dalam rentang data yang dipilih.
-   **Analisis Tegangan**: Idealnya, grafik histogram untuk tegangan akan berbentuk **tinggi dan ramping** di sekitar 220V. Ini menandakan bahwa suplai tegangan ke laboratorium sangat **stabil**. Jika grafik lebar, artinya terjadi fluktuasi tegangan yang signifikan.
-   **Analisis Arus**: Grafik distribusi arus memberikan gambaran tentang **karakteristik beban**. Jika laboratorium menggunakan peralatan dengan daya konstan, grafiknya akan ramping. Jika penggunaan daya sangat bervariasi, grafiknya akan lebih lebar.

#### 2. Segitiga Daya (Plot P-Q)
Visualisasi ini memetakan hubungan antara **Daya Aktif (P)** pada sumbu-X dan **Daya Reaktif (Q)** pada sumbu-Y. Ini adalah alat analisis fundamental dalam teknik elektro.
-   **Daya Aktif (P - Watt)**: Daya yang benar-benar digunakan untuk melakukan kerja (misalnya, menyalakan lampu, memutar motor).
-   **Daya Reaktif (Q - VAR)**: Daya yang dibutuhkan oleh beban induktif (seperti motor, trafo) untuk membentuk medan magnet. Daya ini tidak melakukan kerja nyata tetapi membebani jaringan.
-   **Interpretasi**:
    -   Titik-titik yang **mendekati sumbu-X** (nilai Q rendah) menunjukkan **Faktor Daya (PF) yang baik** (mendekati 1). Ini artinya, hampir semua daya yang ditarik dari jaringan digunakan secara efisien untuk kerja nyata.
    -   Titik-titik yang **jauh dari sumbu-X** (nilai Q tinggi) menandakan **PF yang buruk**. Ini berarti banyak daya "terbuang" di jaringan sebagai daya reaktif, yang dapat menyebabkan denda dari penyedia listrik dan efisiensi yang rendah.

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/pratama404/dashboard-pzem.git](https://github.com/pratama404/dashboard-pzem.git)
    cd dashboard-pzem
    ```
2.  **Install library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Jalankan aplikasi Streamlit:**
    ```bash
    streamlit run dashboard.py
    ```
Aplikasi akan terbuka secara otomatis di browser Anda.