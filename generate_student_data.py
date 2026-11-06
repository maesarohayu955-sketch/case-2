import numpy as np
import pandas as pd

def generate_student_dataset(num_records: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Menghasilkan dataset profil mahasiswa sintetis yang realistis dan konsisten secara statistik.
    
    Variabel:
    1. Jurusan: Kategorik Nominal (6 program studi)
    2. Semester: Kategorik Ordinal (Semester 1 s.d. 8)
    3. IPK: Numerik Kontinu (Skala 0.00 - 4.00, berdistribusi normal realistis)
    4. Usia: Numerik Kontinu / Diskrit (18 - 25 tahun, berkorelasi positif dengan Semester)
    """
    np.random.seed(seed)

    jurusan_list = [
        "Teknik Informatika",
        "Sistem Informasi",
        "Manajemen",
        "Akuntansi",
        "Ilmu Komunikasi",
        "Desain Komunikasi Visual"
    ]
    # Bobot proporsi jurusan di perguruan tinggi
    jurusan_weights = [0.22, 0.20, 0.20, 0.16, 0.12, 0.10]

    # Distribusi Semester (1 sampai 8)
    semesters = np.arange(1, 9)
    # Sedikit lebih banyak mahasiswa di tingkat awal (retention funnel alami)
    semester_weights = [0.15, 0.15, 0.14, 0.14, 0.12, 0.11, 0.10, 0.09]

    records = []

    for _ in range(num_records):
        # 1. Jurusan (Kategorik Nominal)
        jurusan = np.random.choice(jurusan_list, p=jurusan_weights)

        # 2. Semester (Kategorik Ordinal)
        semester = int(np.random.choice(semesters, p=semester_weights))

        # 3. Usia (Numerik Kontinu/Diskrit)
        # Mahasiswa baru (Semester 1-2) rata-rata berusia 18-19 tahun.
        # Bertambah seiring semester dengan variasi acak (gap year / akselerasi).
        base_age = 17.5 + (semester * 0.5)
        age_noise = np.random.normal(loc=0.3, scale=0.6)
        raw_age = base_age + age_noise
        # Batasi usia realistis mahasiswa sarjana S1 (18 - 25 tahun)
        usia = int(np.clip(np.round(raw_age), 18, 25))

        # 4. IPK (Numerik Kontinu)
        # Rata-rata IPK nasional berkisar antara 3.20 - 3.40 dengan standar deviasi ~0.35
        # Tiap jurusan memiliki sedikit variasi karakteristik rata-rata
        jurusan_ipk_offset = {
            "Teknik Informatika": -0.05,
            "Sistem Informasi": 0.02,
            "Manajemen": 0.05,
            "Akuntansi": 0.00,
            "Ilmu Komunikasi": 0.06,
            "Desain Komunikasi Visual": 0.04
        }
        
        mean_ipk = 3.32 + jurusan_ipk_offset.get(jurusan, 0.0)
        std_ipk = 0.36
        raw_ipk = np.random.normal(loc=mean_ipk, scale=std_ipk)
        # Bounding IPK pada rentang 2.00 - 4.00 dan dibulatkan 2 desimal
        ipk = float(np.round(np.clip(raw_ipk, 2.05, 4.00), 2))

        records.append({
            "Jurusan": jurusan,
            "Semester": semester,
            "IPK": ipk,
            "Usia": usia
        })

    df = pd.DataFrame(records)
    # Urutkan berdasarkan Semester (Ordinal) lalu Jurusan untuk kerapian data
    df = df.sort_values(by=["Semester", "Jurusan"]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    output_csv = "dataset_profil_mahasiswa_1000.csv"
    print("Menghasilkan 1.000 baris dataset profil mahasiswa sintetik...")
    df_students = generate_student_dataset(1000, seed=42)
    df_students.to_csv(output_csv, index=False)
    print(f"[SUKSES] Dataset berhasil disimpan di: {output_csv}")
    print("\n--- 5 Baris Pertama ---")
    print(df_students.head())
    print("\n--- Statistik Deskriptif ---")
    print(df_students.describe())
