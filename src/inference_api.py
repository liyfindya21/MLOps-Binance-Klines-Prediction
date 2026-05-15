from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
import os

app = Flask(__name__)

# Menghubungkan ke layanan mlflow-server di network Docker
# Samakan dengan nama service di docker-compose
mlflow.set_tracking_uri("http://mlflow-server:5000")
@app.route('/', methods=['GET'])
def index():
    return "<h1>BTC Prediction API is Running!</h1><p>Use /predict endpoint for inference.</p>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Load model secara dinamis saat ada request
        model_uri = "models:/BTC-Direction-Classifier/latest"
        model = mlflow.pyfunc.load_model(model_uri)
        
        data = request.json
        df = pd.DataFrame(data)
        prediction = model.predict(df)
        return jsonify({'status': 'success', 'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)