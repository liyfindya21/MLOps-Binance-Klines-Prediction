import pandas as pd
import glob
import os

def run_preprocessing():
    # 1. Cari file mentah (.json) yang paling baru di folder data/raw/
    list_of_files = glob.glob('data/raw/*.json')
    if not list_of_files:
        print("Error: Tidak ada data mentah ditemukan di data/raw/")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Memproses data mentah terbaru: {latest_file}")
    
    # 2. Load data mentah
    df_raw = pd.read_json(latest_file)
    
    # 3. Beri nama kolom sesuai standar Binance 
    df_raw.columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ]
    
    # 4. Pembersihan Data (Cleaning) 
    # Hapus kolom yang tidak diperlukan
    df_cleaned = df_raw.drop(columns=['ignore'])
    
    # Konversi tipe data string ke numerik agar bisa dihitung
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'taker_buy_base']
    df_cleaned[numeric_cols] = df_cleaned[numeric_cols].apply(pd.to_numeric)
    
    # Hapus baris yang kosong (missing values) jika ada
    df_cleaned = df_cleaned.dropna()
    
    # 5. Simpan hasil ke data/processed/
    os.makedirs("data/processed", exist_ok=True)
    save_path = "data/processed/btc_klines_cleaned.csv"
    df_cleaned.to_csv(save_path, index=False)
    
    print(f"Berhasil! Data bersih disimpan di: {save_path}")

if __name__ == "__main__":
    run_preprocessing()