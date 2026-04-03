import requests
import json
import os
from datetime import datetime

def ingest_binance_data():
    url = "https://data-api.binance.vision/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 1000 # Mengambil data lebih banyak untuk training
    }
    
    print(f"Mengambil data dinamis dari: {url}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # LOGIKA TIMESTAMP (Syarat LK 04 agar Non-Destruktif)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"data/raw/btc_klines_{timestamp}.json"
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"Berhasil! Data baru disimpan di: {save_path}")
    else:
        print(f"Gagal! Status Code: {response.status_code}")

if __name__ == "__main__":
    ingest_binance_data()