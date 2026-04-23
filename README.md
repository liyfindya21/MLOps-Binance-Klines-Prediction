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
## 📋7. Manajemen Eksperimen dan Pelacakan Metrik Pemodelan dengan MLflow (LK- 06)
LK-06 meminta membuat file train.py yang melatih model ML (sesuai rencana di LK-01 yaitu klasifikasi biner arah harga BTC), lalu mencatat setiap eksperimen ke MLflow. Kemudian harus menjalankan minimal 3 run dengan hyperparameter berbeda, membandingkan hasilnya di MLflow UI, lalu mendaftarkan model terbaik ke Model Registry.

### 💻 Langkah 1: Manajemen Branch
Buka terminal di GitHub Codespaces, lalu jalankan:
```bash
# 1. Pastikan berada di main terbaru
git checkout main
git pull origin main

# 2. Buat branch baru untuk LK-06
git checkout -b feat/mlflow-experiment
```
---

### ✍️ Langkah 2: Tambahkan MLflow ke requirements.txt
```bash
# Buka requirements.txt dan tambahkan mlflow (jika belum ada)
cat requirements.txt
```
Lalu install:
```bash
pip install -r requirements.txt
```
---

### 📅 Langkah 3: Buat File src/train.py
Buat file baru:
```bash
touch src/train.py
```
Lalu buka dan isi dengan kode berikut:

```bash
nano src/train.py
```
Isi lengkap src/train.py:
```bash
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import os
import warnings
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, roc_auc_score
)

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────────
def create_features(df):
    """Membuat indikator teknis sebagai fitur prediksi."""
    df = df.copy()

    for col in ['close', 'high', 'low', 'volume', 'open']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # RSI-14
    delta = df['close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(14).mean()
    loss  = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['rsi_14'] = 100 - (100 / (1 + gain / loss))

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    macd  = ema12 - ema26
    df['macd_diff'] = macd - macd.ewm(span=9, adjust=False).mean()

    # Bollinger Bands Width
    bb_mid         = df['close'].rolling(20).mean()
    bb_std         = df['close'].rolling(20).std()
    df['bb_width'] = (bb_mid + 2*bb_std - (bb_mid - 2*bb_std)) / bb_mid

    # Volume Change
    df['vol_change'] = df['volume'].pct_change()

    # Taker Ratio
    if 'taker_buy_base' in df.columns:
        df['taker_ratio'] = pd.to_numeric(
            df['taker_buy_base'], errors='coerce') / df['volume']
    else:
        df['taker_ratio'] = 0.5   # fallback

    # Target: 1 jika harga berikutnya naik
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    return df


# ─────────────────────────────────────────────
# SATU EKSPERIMEN RUN
# ─────────────────────────────────────────────
def run_experiment(params: dict, experiment_name: str, run_name: str):
    data_path = "data/processed/btc_klines_cleaned.csv"

    if not os.path.exists(data_path):
        print(f"[ERROR] File tidak ditemukan: {data_path}")
        print("        Pastikan sudah menjalankan src/preprocess.py terlebih dahulu.")
        return

    df = pd.read_csv(data_path)
    df = create_features(df)
    df = df.dropna()

    feature_cols = ['rsi_14', 'macd_diff', 'bb_width', 'vol_change', 'taker_ratio']
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols]
    y = df['target']

    # Split tanpa shuffle agar urutan waktu terjaga
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    # Pilih algoritma
    model_type = params.get('model_type', 'random_forest')
    if model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators = params.get('n_estimators', 100),
            max_depth    = params.get('max_depth', 5),
            random_state = 42
        )
    else:  # gradient_boosting
        model = GradientBoostingClassifier(
            n_estimators  = params.get('n_estimators', 100),
            learning_rate = params.get('learning_rate', 0.1),
            max_depth     = params.get('max_depth', 3),
            random_state  = 42
        )

    # ── MLflow tracking ──
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name):

        # Log semua parameter
        for k, v in params.items():
            mlflow.log_param(k, v)
        mlflow.log_param("n_features", len(feature_cols))
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size",  len(X_test))

        # Latih model
        model.fit(X_train_sc, y_train)

        # Evaluasi
        y_pred = model.predict(X_test_sc)
        y_prob = model.predict_proba(X_test_sc)[:, 1]

        metrics = {
            "accuracy"  : accuracy_score(y_test, y_pred),
            "f1_score"  : f1_score(y_test, y_pred),
            "precision" : precision_score(y_test, y_pred),
            "recall"    : recall_score(y_test, y_pred),
            "roc_auc"   : roc_auc_score(y_test, y_prob),
        }

        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        # Simpan artefak model
        mlflow.sklearn.log_model(model, artifact_path="model")

        print(f"\n{'='*45}")
        print(f"  RUN  : {run_name}")
        print(f"{'='*45}")
        for k, v in metrics.items():
            print(f"  {k:<12}: {v:.4f}")
        print(f"{'='*45}")


# ─────────────────────────────────────────────
# MAIN — 3 VARIASI RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":

    EXP = "BTC-USDT-Price-Direction"

    # Run 1 — Random Forest kecil
    run_experiment(
        params    = {"model_type": "random_forest",
                     "n_estimators": 100, "max_depth": 5},
        experiment_name = EXP,
        run_name        = "RF-n100-depth5"
    )

    # Run 2 — Random Forest lebih dalam
    run_experiment(
        params    = {"model_type": "random_forest",
                     "n_estimators": 200, "max_depth": 10},
        experiment_name = EXP,
        run_name        = "RF-n200-depth10"
    )

    # Run 3 — Gradient Boosting learning rate rendah
    run_experiment(
        params    = {"model_type": "gradient_boosting",
                     "n_estimators": 100,
                     "learning_rate": 0.05, "max_depth": 3},
        experiment_name = EXP,
        run_name        = "GB-n100-lr005"
    )

    # Run 4 — Gradient Boosting agresif (opsional, nilai lebih)
    run_experiment(
        params    = {"model_type": "gradient_boosting",
                     "n_estimators": 150,
                     "learning_rate": 0.1, "max_depth": 5},
        experiment_name = EXP,
        run_name        = "GB-n150-lr01"
    )

    print("\n✅ Semua eksperimen selesai! Jalankan: mlflow ui")
```
Simpan file (Ctrl+X → Y → Enter jika pakai nano).
---

### 📊 Langkah 4: Pastikan Data Tersedia, Lalu Jalankan Training
```bash
# Pastikan data processed tersedia dari LK-05
python src/ingest_data.py
python src/preprocess.py

# Jalankan semua eksperimen
python src/train.py
```
Lalu akan melihat output seperti ini di terminal:
```bash
=============================================
  RUN  : RF-n100-depth5
=============================================
  accuracy    : 0.5312
  f1_score    : 0.5489
  precision   : 0.5601
  recall      : 0.5382
  roc_auc     : 0.5714
=============================================
```
---
### 💡 Langkah 5: Buka MLflow UI dan Ambil Screenshot
```bash
python -m mlflow ui --port 5000
```
### 📌 Langkah 6: Daftarkan Model Terbaik ke Model Registry
Dari hasil MLflow UI, pilih run dengan F1-Score dan ROC-AUC tertinggi. Klik run tersebut → klik tab Artifacts → klik model → klik tombol "Register Model" → beri nama BTC-Direction-Classifier → klik Register.
Atau lewat terminal:
```bash
# Jalankan di terminal python (python3)
import mlflow

# Ganti <RUN_ID> dengan ID run terbaik dari MLflow UI
run_id = "<RUN_ID>"
model_uri = f"runs:/{run_id}/model"

mlflow.register_model(
    model_uri = model_uri,
    name      = "BTC-Direction-Classifier"
)
print("Model berhasil didaftarkan ke Model Registry!")
```
---
### ⏳ Langkah 7: Commit dan Push ke GitHub
```bash
# Tambahkan semua file baru
git add src/train.py requirements.txt

# Jangan commit folder mlruns (log MLflow) ke git
echo "mlruns/" >> .gitignore
git add .gitignore

git commit -m "feat: implement MLflow experiment tracking for LK-06"
git push origin feat/mlflow-experiment
```
---
### 🚧 Langkah 8: Buat Pull Request & Merge
1. Buka GitHub repo : https://github.com/liyfindya21/MLOps-Binance-Klines-Prediction
2. Klik notif kuning "feat/mlflow-experiment had recent pushes"
3. Klik "Compare & pull request"
4. Judul PR: feat: MLflow experiment tracking and model registry - LK-06
5. Klik "Create pull request" → "Merge pull request" → "Confirm merge"
---

## 👤 8. Identitas Pengembang
* 🏷️ **Nama:** Aurelia Salsabilla Yunanto P.
* 🆔 **NIM:** 235150201111075
* 📚 **Mata Kuliah:** Machine Learning Operations (CIF60048)
* 🏫 **Instansi:** Universitas Brawijaya
```
