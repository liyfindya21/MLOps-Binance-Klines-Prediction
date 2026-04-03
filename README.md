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

## 👤 6. Identitas Pengembang
* 🏷️ **Nama:** Aurelia Salsabilla Yunanto P.
* 🆔 **NIM:** 235150201111075
* 📚 **Mata Kuliah:** Machine Learning Operations (CIF60048)
* 🏫 **Instansi:** Universitas Brawijaya
```
