import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

# Configuración de la página
st.set_page_config(
    page_title="DataLab Control Center",
    page_icon="📊",
    layout="wide"
)

# Título y encabezado
st.title("📊 DataLab Stack — Dashboard Analítico")
st.markdown("Plataforma integrada para consulta, análisis y visualización de datos en PostgreSQL.")
st.divider()

# Función con caché para conectar a la base de datos mediante SQLAlchemy
@st.cache_resource
def get_db_engine():
    # Conexión usando las credenciales internas del contenedor
    connection_string = "postgresql+psycopg://datalab:datalab_dev@postgres:5432/datalab"
    return create_engine(connection_string)

try:
    engine = get_db_engine()
    
    # Barra lateral de navegación
    st.sidebar.header("⚙️ Configuración")
    esquema_seleccionado = st.sidebar.selectbox(
        "Seleccionar Esquema",
        ["analytics", "staging", "raw", "public"]
    )
    
    # Métricas principales (KIPs)
    col1, col2, col3 = st.sidebar.columns(3)
    
    # 1. Sección de Estado de Conexión
    with st.container():
        st.subheader("🔌 Estado del Sistema")
        col_status1, col_status2 = st.columns(2)
        
        with col_status1:
            st.success("✅ Conexión con PostgreSQL: **Activa**")
        with col_status2:
            st.info(f"📁 Esquema activo: **{esquema_seleccionado}**")

    st.divider()

    # 2. Consultar Tablas Existentes en el Esquema Seleccionado
    query_tablas = text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = :esquema;
    """)
    
    with engine.connect() as conn:
        tablas_df = pd.read_sql(query_tablas, conn, params={"esquema": esquema_seleccionado})
    
    # 3. Vista Principal: Generar datos sintéticos si no hay tablas aún
    st.subheader(f"📋 Tablas en el esquema `{esquema_seleccionado}`")

    if tablas_df.empty:
        st.warning(f"No se encontraron tablas creadas en el esquema `{esquema_seleccionado}`. Mostrando datos de prueba interactivos.")
        
        # Generar DataFrame de prueba (Simulación de ventas/métricas)
        np.random.seed(42)
        fechas = pd.date_range(start="2026-01-01", periods=30, freq="D")
        datos_prueba = pd.DataFrame({
            "Fecha": fechas,
            "Categoría": np.random.choice(["Vinos", "Licores", "Promociones"], size=30),
            "Ventas_MXN": np.random.randint(1500, 12000, size=30),
            "Unidades": np.random.randint(5, 50, size=30)
        })

        # Mostrar tabla interactiva
        st.markdown("#### Vista previa de datos (Demo)")
        st.dataframe(datos_prueba, use_container_width=True)

        # Gráficos
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.markdown("#### 📈 Tendencia de Ventas (MXN)")
            st.line_chart(datos_prueba.set_index("Fecha")["Ventas_MXN"])

        with col_graf2:
            st.markdown("#### 📊 Distribución de Ventas por Categoría")
            ventas_cat = datos_prueba.groupby("Categoría")["Ventas_MXN"].sum()
            st.bar_chart(ventas_cat)

    else:
        # Si existen tablas reales, permitir seleccionar una para explorarla
        tabla_seleccionada = st.selectbox("Selecciona una tabla para explorar:", tablas_df["table_name"])
        
        if tabla_seleccionada:
            query_datos = text(f'SELECT * FROM "{esquema_seleccionado}"."{tabla_seleccionada}" LIMIT 500;')
            with engine.connect() as conn:
                df_real = pd.read_sql(query_datos, conn)
            
            st.markdown(f"#### Vista de la tabla `{tabla_seleccionada}` (Primeros 500 registros)")
            st.dataframe(df_real, use_container_width=True)
            
            # Auto-detectar columnas numéricas para graficar
            columnas_numericas = df_real.select_dtypes(include=[np.number]).columns.tolist()
            if columnas_numericas:
                st.markdown("#### 📉 Gráfico de columnas numéricas")
                col_eje = st.selectbox("Seleccionar columna para graficar:", columnas_numericas)
                st.line_chart(df_real[col_eje])

except Exception as e:
    st.error("❌ Error de conexión con la base de datos:")
    st.code(str(e))
