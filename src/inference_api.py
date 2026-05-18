from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
import os
import glob

app = Flask(__name__)

# 1. Perbaikan typo jumlah garis miring (murni relative path dari /app)
mlflow.set_tracking_uri("sqlite:///mlruns/mlflow.db")

model = None
try:
    # Coba load lewat registry biasa dulu
    model_uri = "models:/BTC-Direction-Classifier/Production"
    print(f"📦 Memuat model dari Registry: {model_uri}...")
    model = mlflow.pyfunc.load_model(model_uri)
    print("✅ SEGAR! Model Production berhasil dimuat via Registry!")
except Exception as registry_error:
    print(f"⚠️ Jalur Registry terhalang perbedaan environment ({registry_error})")
    print("🔄 Mengaktifkan TRICK PAMUNGKAS: Mencari file model langsung di filesystem kontainer...")
    try:
        # Pindai folder /app/mlruns untuk mencari file biner model terbaru
        search_path = os.path.join("/app/mlruns", "**", "MLmodel")
        mlmodel_files = glob.glob(search_path, recursive=True)
        
        if mlmodel_files:
            # Urutkan berdasarkan waktu modifikasi berkas terbaru
            mlmodel_files.sort(key=os.path.getmtime, reverse=True)
            model_dir = os.path.dirname(mlmodel_files[0])
            print(f"📂 Menemukan file model biner di: {model_dir}")
            
            # Load langsung dari folder fisiknya (Bypass semua urusan jaringan/registry)
            model = mlflow.pyfunc.load_model(model_dir)
            print("✅ SEGAR KEMBALI! Model berhasil dimuat langsung dari folder lokal kontainer!")
        else:
            print("❌ Tidak menemukan file MLmodel di folder /app/mlruns")
    except Exception as fallback_error:
        print(f"❌ Gagal total memuat model: {fallback_error}")

@app.route('/', methods=['GET'])
def index():
    return "<h1>BTC Prediction API is Running!</h1><p>Use /predict endpoint for inference.</p>"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'status': 'error', 'message': 'Model tidak tersedia di server atau gagal dimuat.'}), 500
        
    try:
        data = request.json
        df = pd.DataFrame(data)
        prediction = model.predict(df)
        return jsonify({'status': 'success', 'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)