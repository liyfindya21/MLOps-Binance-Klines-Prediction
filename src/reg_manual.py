import mlflow
from mlflow.tracking import MlflowClient

# Tembak langsung ke database fisik SQLite tanpa lewat port 5000!
mlflow.set_tracking_uri("sqlite:///mlflow_docker.db")
client = MlflowClient()

# Ambil eksperimen aktif
experiments = client.search_experiments()
if not experiments:
    print("\n❌ Database SQLite kosong. Jalankan training ulang.")
    exit(1)

experiment = experiments[0]
print(f"\n📡 Menghubungkan ke Eksperimen: {experiment.name} (ID: {experiment.experiment_id})")

# Cari run terbaik berdasarkan F1-score hasil training kamu
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_score DESC"]
)

if not runs:
    print("❌ Run tidak ditemukan di dalam database.")
    exit(1)

best_run = runs[0]
print(f"🏆 Model Terbaik Terbaca: {best_run.info.run_name} | ID: {best_run.info.run_id}")

# Daftarkan langsung ke Model Registry lokal
model_uri = f"runs:/{best_run.info.run_id}/model"
registered_model = mlflow.register_model(model_uri=model_uri, name="BTC-Direction-Classifier")

# Kunci statusnya ke Production sesuai aturan LK-07!
client.transition_model_version_stage(
    name="BTC-Direction-Classifier",
    version=registered_model.version,
    stage="Production"
)
print("\n✅ GOAL MUTLAK: Model v1 resmi masuk takhta Production di Database MLflow!")
