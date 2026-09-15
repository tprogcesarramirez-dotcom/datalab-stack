import pandas as pd
import numpy as np
from src.utils.db import load_dataframe

def generate_and_ingest_sample():
    print("Iniciando pipeline de ingesta de prueba...")
    np.random.seed(42)
    df = pd.DataFrame({
        "id": range(1, 101),
        "producto_id": np.random.randint(100, 105, size=100),
        "monto": np.random.uniform(50.0, 500.0, size=100).round(2),
        "fecha_transaccion": pd.date_range(start="2026-09-01", periods=100, freq="h")
    })
    
    load_dataframe(df, table_name="transacciones_demo", schema="raw", if_exists="replace")

if __name__ == "__main__":
    generate_and_ingest_sample()
