MLOps: Sistem Prediksi Arah Harga BTC/USDT Berdasarkan Data Klines Binance API

(https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

1. Deskripsi Proyek
Proyek ini merupakan implementasi pipeline MLOps (Machine Learning Operations) untuk memprediksi arah pergerakan harga (klasifikasi biner: Naik/Turun) pada pasangan aset kripto BTC/USDT. Sistem ini dirancang untuk mengatasi tantangan data finansial yang dinamis (non-stasioner) dengan menerapkan strategi Continuous Training (CT) berdasarkan deteksi data drift dan performance decay.

Tujuan Utama:

Membangun fondasi teknis yang reproducible menggunakan GitHub Codespaces.

Mengotomatisasi pengambilan data time-series dari Binance API secara berkala.

Mengelola siklus hidup model secara utuh (Eksperimen, Training, Serving, Monitoring).

2. Struktur Direktori (Standardisasi Industri)
Proyek ini mengikuti konvensi struktur direktori standar industri (Cookiecutter Data Science) untuk memastikan kerapian dan skalabilitas sistem :

├── data/               # Penyimpanan dataset
│   ├── raw/            # Data mentah langsung dari Binance API (Immutable) 
│   └── processed/      # Data setelah pembersihan & feature engineering
├── models/             # Tempat menyimpan artefak model (.pkl,.joblib) 
├── notebooks/          # Eksperimen EDA dan prototipe model awal 
├── src/                # Kode sumber utama (Production-ready) 
│   ├── data_ingestion.py  # Script penyerapan data dari API
│   ├── preprocessing.py   # Transformasi data & indikator teknis
│   └── model_training.py  # Script pelatihan model
├── configs/            # File konfigurasi (API keys, model parameters) 
├── tests/              # Script untuk unit testing sistem
├── docs/               # Dokumentasi tambahan proyek
├── requirements.txt    # Daftar dependensi library Python
└── README.md           # Panduan utama proyek

3. Tech Stack & Library
Penyusunan sistem ini menggunakan teknologi yang telah divalidasi pada proposal LK 01:

Data Source:(https://data-api.binance.vision) (Klines Endpoint) .

Preprocessing: Pandas, NumPy, Pandas TA (RSI, MACD, Bollinger Bands) .

Machine Learning: XGBoost (Gradient Boosting) untuk data tabular.

MLOps Tools: MLflow (Experiment Tracking), DVC (Data Versioning), Evidently AI (Monitoring).

Deployment: FastAPI & Docker.

4. Panduan Penggunaan (GitHub Codespaces)
Untuk menjalankan proyek ini di lingkungan yang terstandar tanpa galat ketergantungan (dependency error), ikuti langkah berikut :

A. Inisialisasi Environment
Klik tombol Code hijau di bagian atas repositori ini.

Pilih tab Codespaces dan klik Create codespace on main.

Tunggu hingga setup selesai (terminal akan muncul otomatis).

B. Instalasi Dependensi
Jalankan perintah berikut di terminal Codespaces untuk memasang seluruh library yang dibutuhkan:
pip install -r requirements.txt

C. Menjalankan Eksperimen Awal
Dapat mencoba menjalankan script pengambilan data (PoC) untuk memverifikasi koneksi ke API:
python src/data_ingestion.py

(Hasil data JSON akan tersimpan otomatis di folder data/raw/)

5. Branching Strategy (GitHub Flow)
Proyek ini menerapkan GitHub Flow untuk pengelolaan kode yang aman :

Branch main: Berisi kode yang sudah stabil dan siap digunakan di produksi.

Branch feat/: Digunakan untuk pengembangan fitur baru (misal: feat/initial-setup).

Pull Request (PR): Setiap perubahan harus melewati proses PR dan divalidasi sebelum di-merge ke branch utama.

6. Identitas Pengembang
Nama: Aurelia Salsabilla Yunanto P.

NIM: 235150201111075

Mata Kuliah: Machine Learning Operations (CIF60048)

Instansi: Universitas Brawijaya

