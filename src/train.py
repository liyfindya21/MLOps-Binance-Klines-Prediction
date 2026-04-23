import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import os
import warnings
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, roc_auc_score
)

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────────
def create_features(df):
    """Membuat indikator teknis sebagai fitur prediksi."""
    df = df.copy()

    for col in ['close', 'high', 'low', 'volume', 'open']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # RSI-14
    delta = df['close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(14).mean()
    loss  = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['rsi_14'] = 100 - (100 / (1 + gain / loss))

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    macd  = ema12 - ema26
    df['macd_diff'] = macd - macd.ewm(span=9, adjust=False).mean()

    # Bollinger Bands Width
    bb_mid         = df['close'].rolling(20).mean()
    bb_std         = df['close'].rolling(20).std()
    df['bb_width'] = (bb_mid + 2*bb_std - (bb_mid - 2*bb_std)) / bb_mid

    # Volume Change
    df['vol_change'] = df['volume'].pct_change()

    # Taker Ratio
    if 'taker_buy_base' in df.columns:
        df['taker_ratio'] = pd.to_numeric(
            df['taker_buy_base'], errors='coerce') / df['volume']
    else:
        df['taker_ratio'] = 0.5   # fallback

    # Target: 1 jika harga berikutnya naik
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    return df


# ─────────────────────────────────────────────
# SATU EKSPERIMEN RUN
# ─────────────────────────────────────────────
def run_experiment(params: dict, experiment_name: str, run_name: str):
    data_path = "data/processed/btc_klines_cleaned.csv"

    if not os.path.exists(data_path):
        print(f"[ERROR] File tidak ditemukan: {data_path}")
        print("        Pastikan sudah menjalankan src/preprocess.py terlebih dahulu.")
        return

    df = pd.read_csv(data_path)
    df = create_features(df)
    df = df.dropna()

    feature_cols = ['rsi_14', 'macd_diff', 'bb_width', 'vol_change', 'taker_ratio']
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols]
    y = df['target']

    # Split tanpa shuffle agar urutan waktu terjaga
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    # Pilih algoritma
    model_type = params.get('model_type', 'random_forest')
    if model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators = params.get('n_estimators', 100),
            max_depth    = params.get('max_depth', 5),
            random_state = 42
        )
    else:  # gradient_boosting
        model = GradientBoostingClassifier(
            n_estimators  = params.get('n_estimators', 100),
            learning_rate = params.get('learning_rate', 0.1),
            max_depth     = params.get('max_depth', 3),
            random_state  = 42
        )

    # ── MLflow tracking ──
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name):

        # Log semua parameter
        for k, v in params.items():
            mlflow.log_param(k, v)
        mlflow.log_param("n_features", len(feature_cols))
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size",  len(X_test))

        # Latih model
        model.fit(X_train_sc, y_train)

        # Evaluasi
        y_pred = model.predict(X_test_sc)
        y_prob = model.predict_proba(X_test_sc)[:, 1]

        metrics = {
            "accuracy"  : accuracy_score(y_test, y_pred),
            "f1_score"  : f1_score(y_test, y_pred),
            "precision" : precision_score(y_test, y_pred),
            "recall"    : recall_score(y_test, y_pred),
            "roc_auc"   : roc_auc_score(y_test, y_prob),
        }

        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        # Simpan artefak model
        mlflow.sklearn.log_model(model, artifact_path="model")

        print(f"\n{'='*45}")
        print(f"  RUN  : {run_name}")
        print(f"{'='*45}")
        for k, v in metrics.items():
            print(f"  {k:<12}: {v:.4f}")
        print(f"{'='*45}")


# ─────────────────────────────────────────────
# MAIN — 3 VARIASI RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":

    EXP = "BTC-USDT-Price-Direction"

    # Run 1 — Random Forest kecil
    run_experiment(
        params    = {"model_type": "random_forest",
                     "n_estimators": 100, "max_depth": 5},
        experiment_name = EXP,
        run_name        = "RF-n100-depth5"
    )

    # Run 2 — Random Forest lebih dalam
    run_experiment(
        params    = {"model_type": "random_forest",
                     "n_estimators": 200, "max_depth": 10},
        experiment_name = EXP,
        run_name        = "RF-n200-depth10"
    )

    # Run 3 — Gradient Boosting learning rate rendah
    run_experiment(
        params    = {"model_type": "gradient_boosting",
                     "n_estimators": 100,
                     "learning_rate": 0.05, "max_depth": 3},
        experiment_name = EXP,
        run_name        = "GB-n100-lr005"
    )

    # Run 4 — Gradient Boosting agresif (opsional, nilai lebih)
    run_experiment(
        params    = {"model_type": "gradient_boosting",
                     "n_estimators": 150,
                     "learning_rate": 0.1, "max_depth": 5},
        experiment_name = EXP,
        run_name        = "GB-n150-lr01"
    )

    print("\n✅ Semua eksperimen selesai! Jalankan: mlflow ui")

