# src/transition_stage.py
import mlflow
from mlflow.tracking import MlflowClient
import time

client    = MlflowClient()
MODEL_NAME = "BTC-Direction-Classifier"

def show_versions():
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    print(f"\n{'='*55}")
    print(f"  Daftar Versi Model: {MODEL_NAME}")
    print(f"{'='*55}")
    for v in versions:
        print(f"  v{v.version} | Stage: {v.current_stage:<12} | Run: {v.run_id[:8]}...")
    print(f"{'='*55}")

# --- Tampilkan kondisi awal ---
print("\n[1] Kondisi awal semua versi:")
show_versions()

# --- Transisi v1 (GB-n150-lr01) ke Production ---
# v1 adalah champion model dari LK-06
print("\n[2] Transisi v1 -> Staging...")
client.transition_model_version_stage(
    name    = MODEL_NAME,
    version = 1,
    stage   = "Staging"
)
time.sleep(1)
show_versions()

print("\n[3] Transisi v1 -> Production...")
client.transition_model_version_stage(
    name    = MODEL_NAME,
    version = 1,
    stage   = "Production"
)
time.sleep(1)
show_versions()

# --- v2 ke Staging (sebagai challenger) ---
print("\n[4] Transisi v2 -> Staging (sebagai Challenger)...")
client.transition_model_version_stage(
    name    = MODEL_NAME,
    version = 2,
    stage   = "Staging"
)
time.sleep(1)

# --- Tambahkan deskripsi pada v1 ---
client.update_model_version(
    name        = MODEL_NAME,
    version     = 1,
    description = (
        "Champion model LK-07. GB-n150-lr01: n_estimators=150, "
        "learning_rate=0.1, max_depth=5. "
        "F1-Score=0.565, Accuracy=0.538, ROC-AUC=0.532. "
        "Dipilih sebagai model produksi utama."
    )
)

# --- Tambahkan deskripsi pada v2 ---
client.update_model_version(
    name        = MODEL_NAME,
    version     = 2,
    description = (
        "Challenger model LK-07. GB-n200-lr008: n_estimators=200, "
        "learning_rate=0.08, max_depth=4. "
        "Status: Staging — menunggu evaluasi lebih lanjut."
    )
)

print("\n✅ Semua transisi stage selesai!")
print("\n[5] Kondisi akhir semua versi:")
show_versions()