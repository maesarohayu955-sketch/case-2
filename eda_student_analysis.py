import pandas as pd
import numpy as np

def run_eda(filepath: str = "dataset_profil_mahasiswa_1000.csv"):
    print("=" * 80)
    print(" BEDAH KASUS 2: ANALISIS MENDALAM DATASET PROFIL MAHASISWA (1.000 RECORDS)")
    print("=" * 80)

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan! Jalankan 'generate_student_data.py' terlebih dahulu.")
        return

    # 1. Tipe Data & Integritas
    print("\n[1] STRUKTUR DATA & INTEGRITAS:")
    print(f"- Total Baris Data     : {len(df):,}")
    print(f"- Missing / Null Values: {df.isnull().sum().to_dict()}")
    print(f"- Daftar Jurusan       : {df['Jurusan'].unique().tolist()}")
    print(f"- Urutan Semester      : {sorted(df['Semester'].unique().tolist())}")

    # 2. Statistik Deskriptif Variabel Numerik Kontinu (IPK & Usia)
    print("\n[2] RINGKASAN STATISTIK DESKRIPTIF (NUMERIK KONTINU):")
    print("-" * 80)
    for col in ["IPK", "Usia"]:
        series = df[col]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outliers = series[(series < lower_bound) | (series > upper_bound)]

        print(f"Variabel: {col.upper()}")
        print(f"  • Mean             : {series.mean():.3f}")
        print(f"  • Median           : {series.median():.2f}")
        print(f"  • Modus            : {series.mode().iloc[0]}")
        print(f"  • Standar Deviasi  : {series.std():.3f}")
        print(f"  • Min - Max        : {series.min()} s.d. {series.max()}")
        print(f"  • Q1 - Q3 (IQR)    : {q1:.2f} - {q3:.2f} (IQR = {iqr:.2f})")
        print(f"  • Outlier Detect   : {len(outliers)} record di luar rentang [{lower_bound:.2f}, {upper_bound:.2f}]")
        print("-" * 80)

    # 3. Distribusi Data Kategorik Ordinal (Semester)
    print("\n[3] DISTRIBUSI SEMESTER (KATEGORIK ORDINAL BERURUTAN):")
    sem_dist = df["Semester"].value_counts().sort_index().reset_index()
    sem_dist.columns = ["Semester", "Jumlah Mahasiswa"]
    sem_dist["Persentase (%)"] = (sem_dist["Jumlah Mahasiswa"] / len(df)) * 100
    for _, r in sem_dist.iterrows():
        print(f"  • Semester {int(r['Semester'])}: {int(r['Jumlah Mahasiswa']):3d} mahasiswa ({r['Persentase (%)']:.1f}%)")

    # 4. Analisis Korelasi Antar Variabel
    print("\n[4] ANALISIS KORELASI ANTAR VARIABEL:")
    print("-" * 80)
    corr_pearson = df[["Semester", "Usia", "IPK"]].corr(method="pearson")
    corr_spearman = df[["Semester", "Usia", "IPK"]].corr(method="spearman")
    
    print("Matriks Korelasi Pearson (Linearitas):")
    print(corr_pearson.round(4))
    print("\nMatriks Korelasi Spearman (Hubungan Monotonik / Ordinal):")
    print(corr_spearman.round(4))

    print("\nInterpretasi Korelasi:")
    r_sem_usia = corr_pearson.loc["Semester", "Usia"]
    r_sem_ipk = corr_pearson.loc["Semester", "IPK"]
    r_usia_ipk = corr_pearson.loc["Usia", "IPK"]
    print(f"  1. Semester vs Usia (r = {r_sem_usia:.3f}): Korelasi positif sangat kuat. Seiring kenaikan semester, usia mahasiswa bertambah secara konsisten.")
    print(f"  2. Semester vs IPK  (r = {r_sem_ipk:.3f}): Korelasi mendekati nol. Jenjang semester tidak mendikte pencapaian nilai IPK secara linear.")
    print(f"  3. Usia vs IPK      (r = {r_usia_ipk:.3f}): Tidak ada korelasi signifikan antara faktor usia mahasiswa terhadap performa IPK.")

    # 5. Analisis Performa Akademik Berdasarkan Jurusan
    print("\n[5] PERFORMA AKADEMIK BERDASARKAN JURUSAN:")
    jurusan_summary = df.groupby("Jurusan").agg(
        Total_Mahasiswa=("Semester", "count"),
        Rata_IPK=("IPK", "mean"),
        Median_IPK=("IPK", "median"),
        Min_IPK=("IPK", "min"),
        Max_IPK=("IPK", "max"),
        Cumlaude_Count=("IPK", lambda x: (x >= 3.50).sum()),
        Rata_Usia=("Usia", "mean")
    ).reset_index()

    jurusan_summary["Persen_Cumlaude"] = (jurusan_summary["Cumlaude_Count"] / jurusan_summary["Total_Mahasiswa"]) * 100
    jurusan_summary = jurusan_summary.sort_values(by="Rata_IPK", ascending=False).reset_index(drop=True)

    print(f"{'Jurusan':<26} | {'Total':<6} | {'Mean IPK':<10} | {'Median IPK':<10} | {'Rentang IPK':<14} | {'% Cum Laude':<12}")
    print("-" * 88)
    for _, r in jurusan_summary.iterrows():
        print(f"{r['Jurusan']:<26} | {r['Total_Mahasiswa']:<6} | {r['Rata_IPK']:<10.3f} | {r['Median_IPK']:<10.2f} | {r['Min_IPK']:.2f} - {r['Max_IPK']:.2f}  | {r['Persen_Cumlaude']:>9.1f}%")
    print("-" * 88)

    print("\n" + "=" * 80)
    print(" KESIMPULAN & INSIGHT DATA SCIENCE:")
    print("=" * 80)
    print("1. Distribusi IPK mendekati distribusi normal (Gaussian) berpusat di ~3.33.")
    print("2. Hubungan Semester dan Usia menunjukkan konsistensi tahapan akademik normal perguruan tinggi.")
    print(f"3. Jurusan dengan rata-rata IPK tertinggi adalah '{jurusan_summary.iloc[0]['Jurusan']}' ({jurusan_summary.iloc[0]['Rata_IPK']:.3f}).")
    print(f"4. Sebanyak {(df['IPK'] >= 3.50).sum()} dari {len(df)} mahasiswa ({(df['IPK'] >= 3.50).mean()*100:.1f}%) berada pada predikat Dengan Pujian (Cum Laude).")
    print("=" * 80)

if __name__ == "__main__":
    run_eda()
