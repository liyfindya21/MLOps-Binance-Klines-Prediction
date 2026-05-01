# src/verify_inference.py
"""
LK-07: Verifikasi bahwa model berstatus Production
dapat dipanggil secara programatik menggunakan mlflow.pyfunc.load_model
sebagai simulasi kesiapan sistem inferensi.
"""
import mlflow
import mlflow.pyfunc
import pandas as pd
import numpy as np
from mlflow.tracking import MlflowClient

MODEL_NAME  = "BTC-Direction-Classifier"
MODEL_STAGE = "Production"

print("=" * 55)
print("  LK-07: Verifikasi Kesiapan Inferensi")
print("=" * 55)

# ── 1. Load model dari Production stage ──────────────────
model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
print(f"\n[1] Memuat model dari: {model_uri}")

try:
    model = mlflow.pyfunc.load_model(model_uri)
    print(f"    ✅ Model berhasil dimuat!")
except Exception as e:
    print(f"    ❌ Gagal memuat model: {e}")
    exit(1)

# ── 2. Cek info model dari registry ──────────────────────
client = MlflowClient()
versions = client.get_latest_versions(MODEL_NAME, stages=[MODEL_STAGE])
for v in versions:
    print(f"\n[2] Info Model Production:")
    print(f"    Nama    : {v.name}")
    print(f"    Version : v{v.version}")
    print(f"    Stage   : {v.current_stage}")
    print(f"    Run ID  : {v.run_id}")

# ── 3. Buat data dummy untuk simulasi inferensi ───────────
print(f"\n[3] Membuat data dummy untuk simulasi inferensi...")

# Simulasi 5 data point dengan 5 fitur
np.random.seed(42)
dummy_data = pd.DataFrame({
    'rsi_14'     : np.random.uniform(30, 70, 5),
    'macd_diff'  : np.random.uniform(-50, 50, 5),
    'bb_width'   : np.random.uniform(0.01, 0.05, 5),
    'vol_change' : np.random.uniform(-0.3, 0.3, 5),
    'taker_ratio': np.random.uniform(0.4, 0.6, 5),
})

print(f"\n    Data Input (5 sampel):")
print(dummy_data.to_string(index=False))

# ── 4. Lakukan prediksi ───────────────────────────────────
print(f"\n[4] Menjalankan inferensi...")
predictions = model.predict(dummy_data)

print(f"\n    Hasil Prediksi Arah Harga BTC/USDT:")
print(f"    {'Sampel':<10} {'Prediksi':<12} {'Interpretasi'}")
print(f"    {'-'*45}")
for i, pred in enumerate(predictions):
    arah = "📈 NAIK" if pred == 1 else "📉 TURUN"
    print(f"    Sampel {i+1:<4} {str(pred):<12} {arah}")

# ── 5. Kesimpulan ─────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  ✅ VERIFIKASI INFERENSI BERHASIL!")
print(f"  Model '{MODEL_NAME}' v{versions[0].version} (Production)")
print(f"  siap digunakan untuk inferensi sistem nyata.")
print(f"{'='*55}\n")# src/verify_inference.py
"""
LK-07: Verifikasi bahwa model berstatus Production
dapat dipanggil secara programatik menggunakan mlflow.pyfunc.load_model
sebagai simulasi kesiapan sistem inferensi.
"""
import mlflow
import mlflow.pyfunc
import pandas as pd
import numpy as np
from mlflow.tracking import MlflowClient

MODEL_NAME  = "BTC-Direction-Classifier"
MODEL_STAGE = "Production"

print("=" * 55)
print("  LK-07: Verifikasi Kesiapan Inferensi")
print("=" * 55)

# ── 1. Load model dari Production stage ──────────────────
model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
print(f"\n[1] Memuat model dari: {model_uri}")

try:
    model = mlflow.pyfunc.load_model(model_uri)
    print(f"    ✅ Model berhasil dimuat!")
except Exception as e:
    print(f"    ❌ Gagal memuat model: {e}")
    exit(1)

# ── 2. Cek info model dari registry ──────────────────────
client = MlflowClient()
versions = client.get_latest_versions(MODEL_NAME, stages=[MODEL_STAGE])
for v in versions:
    print(f"\n[2] Info Model Production:")
    print(f"    Nama    : {v.name}")
    print(f"    Version : v{v.version}")
    print(f"    Stage   : {v.current_stage}")
    print(f"    Run ID  : {v.run_id}")

# ── 3. Buat data dummy untuk simulasi inferensi ───────────
print(f"\n[3] Membuat data dummy untuk simulasi inferensi...")

# Simulasi 5 data point dengan 5 fitur
np.random.seed(42)
dummy_data = pd.DataFrame({
    'rsi_14'     : np.random.uniform(30, 70, 5),
    'macd_diff'  : np.random.uniform(-50, 50, 5),
    'bb_width'   : np.random.uniform(0.01, 0.05, 5),
    'vol_change' : np.random.uniform(-0.3, 0.3, 5),
    'taker_ratio': np.random.uniform(0.4, 0.6, 5),
})

print(f"\n    Data Input (5 sampel):")
print(dummy_data.to_string(index=False))

# ── 4. Lakukan prediksi ───────────────────────────────────
print(f"\n[4] Menjalankan inferensi...")
predictions = model.predict(dummy_data)

print(f"\n    Hasil Prediksi Arah Harga BTC/USDT:")
print(f"    {'Sampel':<10} {'Prediksi':<12} {'Interpretasi'}")
print(f"    {'-'*45}")
for i, pred in enumerate(predictions):
    arah = "📈 NAIK" if pred == 1 else "📉 TURUN"
    print(f"    Sampel {i+1:<4} {str(pred):<12} {arah}")

# ── 5. Kesimpulan ─────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  ✅ VERIFIKASI INFERENSI BERHASIL!")
print(f"  Model '{MODEL_NAME}' v{versions[0].version} (Production)")
print(f"  siap digunakan untuk inferensi sistem nyata.")
print(f"{'='*55}\n")