# src/train_v2.py
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import os
import warnings
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, roc_auc_score
)

warnings.filterwarnings('ignore')

def create_features(df):
    df = df.copy()
    for col in ['close', 'high', 'low', 'volume', 'open']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['rsi_14'] = 100 - (100 / (1 + gain / loss))

    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    df['macd_diff'] = macd - macd.ewm(span=9, adjust=False).mean()

    bb_mid = df['close'].rolling(20).mean()
    bb_std = df['close'].rolling(20).std()
    df['bb_width'] = (bb_mid + 2*bb_std - (bb_mid - 2*bb_std)) / bb_mid

    df['vol_change'] = df['volume'].pct_change()

    if 'taker_buy_base' in df.columns:
        df['taker_ratio'] = pd.to_numeric(
            df['taker_buy_base'], errors='coerce') / df['volume']
    else:
        df['taker_ratio'] = 0.5

    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    return df

def train_and_register_v2():
    data_path = "data/processed/btc_klines_cleaned.csv"
    if not os.path.exists(data_path):
        print("[ERROR] File tidak ditemukan. Jalankan src/preprocess.py dulu.")
        return

    df = pd.read_csv(data_path)
    df = create_features(df)
    df = df.dropna()

    feature_cols = ['rsi_14', 'macd_diff', 'bb_width', 'vol_change', 'taker_ratio']
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    # === Parameter sedikit berbeda dari v1 untuk versioning ===
    params_v2 = {
        "model_type"    : "gradient_boosting",
        "n_estimators"  : 200,      # v1 = 150
        "learning_rate" : 0.08,     # v1 = 0.1
        "max_depth"     : 4,        # v1 = 5
    }

    model = GradientBoostingClassifier(
        n_estimators  = params_v2['n_estimators'],
        learning_rate = params_v2['learning_rate'],
        max_depth     = params_v2['max_depth'],
        random_state  = 42
    )

    EXP = "BTC-USDT-Price-Direction"
    mlflow.set_experiment(EXP)

    with mlflow.start_run(run_name="GB-n200-lr008-v2") as run:
        for k, v in params_v2.items():
            mlflow.log_param(k, v)
        mlflow.log_param("n_features", len(feature_cols))
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size",  len(X_test))

        model.fit(X_train_sc, y_train)

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

        mlflow.sklearn.log_model(model, artifact_path="model")

        run_id_v2 = run.info.run_id
        print(f"\nRun ID v2: {run_id_v2}")
        for k, v in metrics.items():
            print(f"  {k:<12}: {v:.4f}")

    # === Daftarkan sebagai v2 ke Model Registry ===
    model_uri = f"runs:/{run_id_v2}/model"
    registered = mlflow.register_model(
        model_uri = model_uri,
        name      = "BTC-Direction-Classifier"
    )
    print(f"\n✅ Model v2 berhasil didaftarkan!")
    print(f"   Nama   : {registered.name}")
    print(f"   Version: {registered.version}")

if __name__ == "__main__":
    train_and_register_v2()