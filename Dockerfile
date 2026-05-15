# 1. Gunakan image Python versi ringan (slim) agar ukuran kontainer tidak terlalu besar
FROM python:3.12-slim

# 2. Atur direktori kerja di dalam kontainer ke /app
WORKDIR /app

# 3. Instal dependensi sistem yang mungkin dibutuhkan (seperti compiler untuk library ML)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Salin file requirements.txt ke dalam kontainer
# Langkah ini dipisah agar Docker bisa melakukan caching library yang sudah diinstal
COPY requirements.txt .

# 5. Instal semua library Python yang dibutuhkan (Flask, MLflow, Pandas, dll)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Salin seluruh isi proyek (termasuk folder src) ke dalam kontainer
COPY . .

# 7. Beritahu Docker bahwa kontainer ini akan menggunakan port 5001
EXPOSE 5001

# 8. Perintah untuk menjalankan API saat kontainer dinyalakan
CMD ["python", "src/inference_api.py"]