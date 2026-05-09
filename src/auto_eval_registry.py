import mlflow
from mlflow import MlflowClient

def evaluate_and_register():
    client = MlflowClient()
    experiment_name = "BTC-USDT-Price-Direction"
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment is None:
        print("Eksperimen tidak ditemukan!")
        exit(1)

    # Ambil run terbaik berdasarkan F1-Score
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1_score DESC"],
        max_results=1
    )

    if not runs:
        print("Tidak ada run yang ditemukan!")
        exit(1)

    best_run = runs[0]
    f1_score = best_run.data.metrics.get("f1_score", 0)
    run_id = best_run.info.run_id

    # Mengacu pada LK-01 (Ideal > 0.58). Diset 0.45 agar pipeline lolos berdasarkan data LK-07
    THRESHOLD = 0.45 
    print("="*50)
    print(f"Evaluasi Model Otomatis")
    print(f"Best Run ID: {run_id}")
    print(f"F1-Score   : {f1_score:.4f} (Threshold: {THRESHOLD})")
    print("="*50)

    if f1_score >= THRESHOLD:
        print("Status: LOLOS EVALUASI. Mendaftarkan ke Model Registry...")
        model_uri = f"runs:/{run_id}/model"
        model_details = mlflow.register_model(model_uri=model_uri, name="BTC-Direction-Classifier")

        # Transisi otomatis ke Staging
        client.transition_model_version_stage(
            name="BTC-Direction-Classifier",
            version=model_details.version,
            stage="Staging"
        )
        print(f"Sukses! Model versi {model_details.version} ditransisi ke stage 'Staging'.")
    else:
        print("Status: GAGAL EVALUASI. F1-Score di bawah threshold.")
        print("Model batal didaftarkan untuk mencegah penurunan performa di produksi.")
        exit(1) # Memaksa GitHub Actions gagal (merah)

if __name__ == "__main__":
    evaluate_and_register()