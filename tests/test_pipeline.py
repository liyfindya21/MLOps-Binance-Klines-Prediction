import pandas as pd

def test_data_structure():
    """Verifikasi struktur data dasar untuk mencegah silent failures pada pipeline data"""
    # Simulasi data mentah dummy
    df = pd.DataFrame({
        'close': [60000, 61000, 62000],
        'high': [61000, 62000, 63000],
        'low': [59000, 60000, 61000],
        'volume': [100, 150, 200],
        'open': [59500, 60500, 61500]
    })

    assert not df.empty, "Dataframe tidak boleh kosong"
    assert 'close' in df.columns, "Kolom close wajib ada untuk target prediksi"
    assert 'volume' in df.columns, "Kolom volume wajib ada untuk indikator pasar"
    # test re-push