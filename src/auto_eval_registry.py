import mlflow
from mlflow import MlflowClient

def evaluate_and_register():
    client = MlflowClient()
    experiment_name = "BTC-USDT-Price-Direction"
    model_name = "BTC-Direction-Classifier"
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment is None:
        print("Eksperimen tidak ditemukan!")
        exit(1)

    # 1. Ambil run terbaru (Model Baru hasil retraining) berdasarkan F1-Score
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1_score DESC"],
        max_results=1
    )

    if not runs:
        print("Tidak ada run yang ditemukan!")
        exit(1)

    best_run = runs[0]
    new_f1_score = best_run.data.metrics.get("f1_score", 0)
    run_id = best_run.info.run_id

    # 2. Ambil performa model LAMA yang saat ini berstatus 'Production'
    production_f1_score = 0.0
    try:
        production_versions = client.get_latest_versions(name=model_name, stages=["Production"])
        if production_versions:
            prod_run_id = production_versions[0].run_id
            prod_run = client.get_run(prod_run_id)
            production_f1_score = prod_run.data.metrics.get("f1_score", 0)
            print(f"Model Production Lama Ditemukan! F1-Score: {production_f1_score:.4f}")
        else:
            print("Belum ada model di stage Production. Ini akan jadi model pertama.")
    except Exception as e:
        print(f"Pengecekan model production lama dilewati: {e}")

    THRESHOLD = 0.45 
    print("="*50)
    print(f"Evaluasi Komparatif Otomatis (LK-12 Closed-Loop)")
    print(f"Model Baru Run ID     : {run_id}")
    print(f"F1-Score Model Baru   : {new_f1_score:.4f} (Threshold Dasar: {THRESHOLD})")
    print(f"F1-Score Production   : {production_f1_score:.4f}")
    print("="*50)

    # 3. Validasi Kelayakan: Harus lolos threshold dasar DAN harus lebih baik/sama dengan model Production lama
    if new_f1_score >= THRESHOLD and new_f1_score >= production_f1_score:
        print("Status: LOLOS EVALUASI KOMPARATIF. Mendaftarkan ke Model Registry...")
        model_uri = f"runs:/{run_id}/model"
        model_details = mlflow.register_model(model_uri=model_uri, name=model_name)

        # Transisi otomatis langsung dipromosikan ke Production sesuai instruksi LK-12
        client.transition_model_version_stage(
            name=model_name,
            version=model_details.version,
            stage="Production",
            archive_existing_versions=True # Otomatis meng-archive model lama biar gak bentrok!
        )
        print(f"Sukses! Model versi {model_details.version} RESMI dipromosikan ke stage 'Production'.")
    else:
        print("Status: GAGAL EVALUASI KOMPARATIF.")
        if new_f1_score < THRESHOLD:
            print("Alasan: Performa model baru di bawah ambang batas minimal (Threshold).")
        else:
            print("Alasan: Performa model baru tidak lebih baik dari model Production yang ada saat ini.")
        print("Model baru ditolak untuk melindungi performa sistem di produksi.")
        exit(1) # Memaksa pipeline GitHub Actions berhenti berwarna merah

if __name__ == "__main__":
    evaluate_and_register()