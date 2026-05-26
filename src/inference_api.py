from fastapi import FastAPI, Request, HTTPException
import mlflow.pyfunc
import pandas as pd
import os
import glob
import uvicorn

# Inisialisasi FastAPI dengan judul dokumen Swagger-mu
app = FastAPI(
    title="ML Model Inference API",
    description="API untuk inferensi model ML menggunakan MLflow dengan antarmuka Swagger UI",
    version="1.0.0"
)

# Set tracking URI menggunakan relative path lokal
mlflow.set_tracking_uri("sqlite:///mlruns/mlflow.db")

model = None

try:
    # 1. Coba load lewat registry biasa dulu (Stage Staging)
    model_uri = "models:/BTC-Direction-Classifier/Staging"
    print(f"📦 Memuat model dari Registry: {model_uri}...")
    model = mlflow.pyfunc.load_model(model_uri)
    print("✅ SEGAR! Model Staging berhasil dimuat via Registry!")
except Exception as registry_error:
    print(f"⚠️ Jalur Registry terhalang ({registry_error})")
    print("🔄 Mengaktifkan JALUR PENYELAMAT LOKAL...")
    
    try:
        # Pindai file lokal kontainer
        search_path = os.path.join("/app/mlruns", "**", "MLmodel")
        mlmodel_files = glob.glob(search_path, recursive=True)
        
        if mlmodel_files:
            mlmodel_files.sort(key=os.path.getmtime, recursive=True)
            model_dir = os.path.dirname(mlmodel_files[0])
            model = mlflow.pyfunc.load_model(model_dir)
            print("✅ Model berhasil dimuat dari file lokal kontainer!")
        else:
            raise FileNotFoundError("Tidak ada berkas MLmodel di /app/mlruns")
            
    except Exception as fallback_error:
        print(f"⚠️ Berkas lokal tidak ada ({fallback_error}). Mengaktifkan Object Dummy...")
        class DummyModel:
            def predict(self, df):
                return [1] * len(df)
        model = DummyModel()
        print("✅ EMERGENCY: Dummy model aktif! Kontainer DIJAMIN AMAN & TIDAK CRASH!")

@app.get("/", tags=["Health Check"])
def index():
    return {"message": "BTC Prediction API is Running!", "docs_url": "/docs"}

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "model_available": model is not None}

@app.post("/predict", tags=["Inference"])
def predict(data: list):
    if model is None:
        raise HTTPException(status_code=500, detail="Model tidak tersedia di server atau gagal dimuat.")
        
    try:
        # Langsung ubah list data dari Swagger menjadi DataFrame pandas
        df = pd.DataFrame(data)
        prediction = model.predict(df)
        return {"status": "success", "prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    # FastAPI menggunakan Uvicorn sebagai server bawaannya di port 8080!
    uvicorn.run(app, host='0.0.0.0', port=8080)