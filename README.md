# 🚀 MLOps: Sistem Prediksi Arah Harga BTC/USDT 
### Berdasarkan Data Klines Binance API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)
![Status](https://img.shields.io/badge/Status-Development-orange.svg)

---

## 📌 1. Deskripsi Proyek
Proyek ini merupakan implementasi pipeline **MLOps (Machine Learning Operations)** untuk memprediksi arah pergerakan harga (**klasifikasi biner: Naik/Turun**) pada pasangan aset kripto **BTC/USDT**. 

Sistem ini dirancang khusus untuk mengatasi tantangan data finansial yang dinamis (*non-stasioner*) dengan menerapkan strategi **Continuous Training (CT)** berdasarkan deteksi *data drift* dan *performance decay*.

### 🎯 Tujuan Utama:
* **Reproducibility:** Membangun fondasi teknis yang konsisten menggunakan GitHub Codespaces.
* **Automation:** Mengotomatisasi pengambilan data *time-series* dari Binance API secara berkala.
* **Lifecycle Management:** Mengelola siklus hidup model secara utuh (Eksperimen, Training, Serving, hingga Monitoring).

---

## 📂 2. Struktur Direktori (Standardisasi Industri)
Proyek ini mengikuti konvensi **Cookiecutter Data Science** untuk memastikan kerapian dan skalabilitas sistem:

```text
├── data/                # 🗄️ Penyimpanan dataset
│   ├── raw/             # 📥 Data mentah dari Binance API (Immutable)
│   └── processed/       # 🧹 Data setelah pembersihan & feature engineering
├── models/              # 🤖 Tempat menyimpan artefak model (.pkl, .joblib)
├── notebooks/           # 📓 Eksperimen EDA dan prototipe model awal
├── src/                 # 🚀 Kode sumber utama (Production-ready)
│   ├── data_ingestion.py   # 🏗️ Script penyerapan data dari API
│   ├── preprocessing.py    # ⚙️ Transformasi data & indikator teknis
│   └── model_training.py   # 🎓 Script pelatihan model
├── configs/             # 🔧 File konfigurasi (API keys, model parameters)
├── tests/               # 🧪 Script untuk unit testing sistem
├── docs/                # 📄 Dokumentasi tambahan proyek
├── requirements.txt     # 📋 Daftar dependensi library Python
└── README.md            # 📖 Panduan utama proyek

```
---

## 🛠️ 3. Tech Stack & Library
Penyusunan sistem ini menggunakan teknologi yang telah divalidasi pada proposal **LK 01**:

| Kategori | Teknologi / Library |
| :--- | :--- |
| **🌐 Data Source** | [Binance Klines API](https://data-api.binance.vision) |
| **🧹 Preprocessing** | Pandas, NumPy, Pandas TA (RSI, MACD, Bollinger Bands) |
| **🧠 Machine Learning** | XGBoost (Gradient Boosting) |
| **♾️ MLOps Tools** | MLflow (Tracking), DVC (Versioning), Evidently AI (Monitoring) |
| **📦 Deployment** | FastAPI & Docker |

---

## 💻 4. Panduan Penggunaan (GitHub Codespaces)
Ikuti langkah berikut untuk menjalankan proyek di lingkungan yang terstandar tanpa galat ketergantungan:

### ⚙️ A. Inisialisasi Environment
1.  Klik tombol **Code** (warna hijau) di bagian atas repositori ini.
2.  Pilih tab **Codespaces** dan klik **Create codespace on main**.
3.  Tunggu hingga setup selesai dan terminal muncul secara otomatis.

### 📥 B. Instalasi Dependensi
Jalankan perintah berikut di terminal untuk memasang seluruh library:
```bash
pip install -r requirements.txt
```

---

## 💻 4. Panduan Penggunaan & Pipeline Data (LK-04)

Bagian ini menjelaskan alur kerja penarikan data dinamis dan prapemrosesan otomatis.

### 📥 A. Penarikan Data (Data Ingestion)
Skrip `src/ingest_data.py` digunakan untuk mengambil data terbaru dari Binance API. Skrip ini menggunakan *timestamp* agar data lama tidak tertimpa.

**Cara Menjalankan:**
```bash
python src/ingest_data.py
```
Hasil: Data mentah disimpan di data/raw/btc_klines_YYYYMMDD_HHMMSS.json.

### 🧹 B. Prapemrosesan Otomatis (Preprocessing)
Skrip src/preprocess.py akan secara otomatis mendeteksi file mentah terbaru di folder data/raw/, melakukan pembersihan, dan konversi tipe data numerik.

Cara Menjalankan:

```bash
python src/preprocess.py
```
Hasil: Data bersih siap pakai disimpan di data/processed/btc_klines_cleaned.csv.

---
### 🖼️ C. Commit 
```bash
# Tambahkan semua perubahan (skrip dan data mentah)
git add.

# Lakukan commit dengan pesan yang informatif
git commit -m "feat: implement dynamic ingestion with timestamp and automated preprocessing for LK-04"

# Kirim ke branch eksperimen Anda
git push origin feat/data-pipeline
```
---

## 🔄 5. Branching Strategy (GitHub Flow)
Proyek ini menerapkan **GitHub Flow** untuk pengelolaan kode yang aman:

* **🌿 Branch `main`**: Berisi kode yang sudah stabil dan siap digunakan di produksi.
* **✨ Branch `feat/`**: Digunakan untuk pengembangan fitur baru (misal: `feat/initial-setup`).
* **⚖️ Pull Request (PR)**: Setiap perubahan harus melewati proses PR dan divalidasi sebelum di-merge ke branch utama.

---
## 📚6. Manajemen Versi Data (DVC - LK-05)
Proyek ini menggunakan Data Version Control (DVC) untuk mengelola dataset besar tanpa membebani repositori Git. DVC memungkinkan pelacakan perubahan data dengan cara yang mirip dengan cara Git melacak kode sumber.

### ⚙️ A. Persiapan dan Inisialisasi
Langkah pertama adalah menyiapkan lingkungan dan menginisialisasi DVC di dalam repositori:
```bash
# Membuat branch baru untuk pengerjaan DVC
git checkout -b feat/dvc-data-management 

# Instalasi DVC
pip install dvc 

# Inisialisasi DVC dalam proyek
dvc init 

# Commit konfigurasi awal DVC ke Git
git add .dvc .gitignore .dvcignore 
git commit -m "Initialize DVC for data versioning" 
```
---

### 📥 B. Pelacakan Dataset (Tracking)
DVC mengambil alih pengelolaan folder data dari Git agar repositori tetap ringan:
```bash
# Melepaskan folder data dari pantauan Git (tanpa menghapus file fisik)
git rm -r --cached data/raw data/processed 
git commit -m "Stop tracking data folders in Git to move them to DVC" 

# Mulai melacak folder data menggunakan DVC
dvc add data/raw data/processed 

# Menambahkan file pointer (.dvc) ke Git
git add data/raw.dvc data/processed.dvc data/.gitignore 
git commit -m "Track initial raw and processed datasets with DVC" 
```
---

### 🔄 C. Simulasi Pembaruan Data (Continual Learning)
Saat ada data baru dari hasil ingest atau prapemrosesan, DVC digunakan untuk mencatat versi terbaru tersebut:
```bash
# Jalankan pipeline data (LK-04) untuk mendapat data baru
python src/ingest_data.py 
python src/preprocess.py 

# Update pelacakan DVC untuk mencatat hash data terbaru
dvc add data/raw data/processed 

# Lihat perbedaan hash metadata
dvc status 
dvc diff

# Commit perubahan metadata (.dvc) ke Git
git add data/raw.dvc data/processed.dvc 
git commit -m "Update datasets with new kline batches (Continual Learning simulation)" 
```
---

### ☁️ D. Setup Remote Storage & Push
Data asli (fisik) disimpan di Remote Storage (dalam simulasi ini menggunakan folder lokal di luar repo):
```bash
# Membuat folder storage lokal sebagai simulasi remote
mkdir -p /tmp/dvc_remote

# Mendaftarkan storage tersebut sebagai remote default DVC
dvc remote add -d local_remote /tmp/dvc_remote 

# Simpan konfigurasi remote ke Git
git add .dvc/config 
git commit -m "Configure local DVC remote storage" 

# Upload (Push) data asli ke remote storage
dvc push 
```
---

## 👤 7. Identitas Pengembang
* 🏷️ **Nama:** Aurelia Salsabilla Yunanto P.
* 🆔 **NIM:** 235150201111075
* 📚 **Mata Kuliah:** Machine Learning Operations (CIF60048)
* 🏫 **Instansi:** Universitas Brawijaya
```
