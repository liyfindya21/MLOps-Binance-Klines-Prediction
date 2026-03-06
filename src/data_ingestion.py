import requests
import json
import os

def fetch_binance_klines():
    # Menggunakan mirror data-api agar tidak terblokir di Indonesia
    url = "https://data-api.binance.vision/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 5
    }
    
    print(f"Mengambil data dari: {url}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Folder penyimpanan sesuai struktur LK 02
        save_path = "data/raw/btc_klines_raw.json"
        
        # Pastikan folder data/raw ada
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"Berhasil! Data disimpan di: {save_path}")
        print("Contoh data (5 baris terakhir):")
        for kline in data:
            print(kline)
    else:
        print(f"Gagal mengambil data. Status Code: {response.status_code}")

if __name__ == "__main__":
    fetch_binance_klines()