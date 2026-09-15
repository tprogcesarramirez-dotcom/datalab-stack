import os
import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    """Retorna un motor de SQLAlchemy para PostgreSQL en la red Docker."""
    user = os.getenv("POSTGRES_USER", "datalab")
    password = os.getenv("POSTGRES_PASSWORD", "datalab_dev")
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "datalab")
    
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def load_dataframe(df: pd.DataFrame, table_name: str, schema: str = "raw", if_exists: str = "append"):
    """Escribe un DataFrame directamente en una tabla y esquema específico."""
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql(name=table_name, con=conn, schema=schema, if_exists=if_exists, index=False)
    print(f"Cargados {len(df)} registros en '{schema}.{table_name}'.")

def query_to_dataframe(sql_query: str) -> pd.DataFrame:
    """Ejecuta una consulta SQL y retorna un DataFrame de Pandas."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(sql_query, conn)
