LINK STREAMLIT : https://case-2-8kmrsw2z5xcif7xreka2z5.streamlit.app/
# Panduan Eksekusi Bedah Kasus 2: Dataset Profil Mahasiswa

## 📁 Struktur Direktori
```text
bedah_kasus_mahasiswa/
├── generate_student_data.py            # Generator 1.000 data sintesis profil mahasiswa
├── dataset_profil_mahasiswa_1000.csv    # File CSV 1.000 baris record mahasiswa
├── eda_student_analysis.py             # Analisis statistik deskriptif & korelasi (Pandas/NumPy)
├── app2.py                             # Aplikasi Web Dashboard Interaktif Streamlit
├── requirements.txt                    # Dependensi pustaka Python
└── README.md                           # Dokumentasi & panduan
```

## 🚀 Perintah Menjalankan Aplikasi di Terminal

1. **Masuk ke folder proyek:**
   ```bash
   cd "C:\Users\User_PC\.gemini\antigravity\scratch\bedah_kasus_mahasiswa"
   ```

2. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate data mahasiswa (1.000 records):**
   ```bash
   python generate_student_data.py
   ```

4. **Jalankan analisis data mendalam (EDA & Korelasi):**
   ```bash
   python eda_student_analysis.py
   ```

5. **Jalankan aplikasi Streamlit:**
   ```bash
   streamlit run app2.py
   ```

## 🌐 Tautan Akses Lokal:
Setelah perintah di atas dijalankan, aplikasi Streamlit dapat diakses melalui browser pada:
- **Local URL:** `http://localhost:8501`
- **Network URL:** `http://<ip-lokal-anda>:8501`
