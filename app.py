import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Importamos tus módulos (Asegúrate de que los nombres de archivo coincidan)
from data_loader import load_data
from expense_classifier import classify
from analytics import calculate_balance
from ia_ad import get_advice, detect_anomalies
from subscription_detector import find_subscriptions
from predictor import predict_next_month

# CONFIGURACIÓN DE LA INTERFAZ
st.set_page_config(
    page_title="Smart Finance Analyzer Pro", 
    page_icon="💰", 
    layout="wide"
)

# ESTILO PERSONALIZADO (Corregido para visibilidad)
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stMetricValue"] {
        color: #00ffcc !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Smart Finance Analyzer Pro")
st.write("Bienvenido a tu panel de control financiero. Desarrollado por **Anxo Pena Blanco**.")

# BARRA LATERAL (SIDEBAR)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1611/1611154.png", width=100)
st.sidebar.header("Configuración")
archivo_subido = st.sidebar.file_uploader("Sube tu archivo de gastos (.csv)", type=["csv"])

if archivo_subido:
    # Cargar datos
    df_raw = load_data(archivo_subido)
    
    # --- VALIDACIÓN PROFESIONAL ---
    if df_raw is not None:
        # Verificamos que existan las columnas necesarias antes de seguir
        columnas_necesarias = ["fecha", "descripcion", "cantidad"]
        if not all(col in df_raw.columns for col in columnas_necesarias):
            st.error(f"Error: El archivo debe contener las columnas: {columnas_necesarias}")
            st.stop() # Detiene la ejecución de forma limpia

        # --- FILTRO DE FECHAS (Toque Senior) ---
        st.sidebar.subheader("Filtro Temporal")
        min_date = df_raw["fecha"].min().to_pydatetime()
        max_date = df_raw["fecha"].max().to_pydatetime()
        
        rango_fechas = st.sidebar.date_input(
            "Selecciona rango de análisis",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        # Aplicar filtro si se seleccionan ambas fechas
        if len(rango_fechas) == 2:
            mask = (df_raw["fecha"].dt.date >= rango_fechas[0]) & (df_raw["fecha"].dt.date <= rango_fechas[1])
            df = df_raw.loc[mask].copy()
        else:
            df = df_raw.copy()

        # --- PROCESAMIENTO ---
        df["categoria"] = df["descripcion"].apply(classify)
        ingresos, gastos, ahorro = calculate_balance(df)

        # MÉTRICAS RÁPIDAS
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ingresos Totales", f"{ingresos:,.2f} €")
        with col2:
            st.metric("Gastos Totales", f"{abs(gastos):,.2f} €", delta_color="inverse")
        with col3:
            st.metric("Ahorro Neto", f"{ahorro:,.2f} €", 
                      delta=f"{(ahorro/ingresos)*100:.1f}%" if ingresos > 0 else "0%")

        st.divider()

        # PESTAÑAS PRINCIPALES
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Análisis Visual", 
            "🕵️ Suscripciones", 
            "🔮 Predicciones IA", 
            "📄 Datos Crudos"
        ])

        with tab1:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("Distribución de Gastos")
                df_gastos = df[df["cantidad"] < 0].copy()
                df_gastos["cantidad"] = df_gastos["cantidad"].abs()
                fig_pie = px.pie(df_gastos, values="cantidad", names="categoria", hole=0.4,
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_chart2:
                st.subheader("Balance Mensual Neto")
                # Agrupamos y calculamos el flujo de caja real
                df_time = df.groupby(df['fecha'].dt.strftime('%Y-%m'))['cantidad'].sum().reset_index()
                # Color dinámico: Verde si es positivo, Rojo si es negativo
                df_time['color'] = df_time['cantidad'].apply(lambda x: 'positivo' if x >= 0 else 'negativo')
                
                fig_line = px.bar(df_time, x='fecha', y='cantidad', color='color',
                                  color_discrete_map={'positivo': '#00ffcc', 'negativo': '#ff4b4b'},
                                  title="Ingresos vs Gastos por Mes")
                st.plotly_chart(fig_line, use_container_width=True)

        with tab2:
            st.subheader("Detección de Pagos Recurrentes")
            suscripciones = find_subscriptions(df)
            if suscripciones:
                st.success(f"He encontrado {len(suscripciones)} posibles suscripciones activas.")
                for sub in suscripciones:
                    st.write(f"💳 **{sub}** - Detectado como pago frecuente.")
            else:
                st.info("No se han detectado patrones de suscripción.")

        with tab3:
            st.subheader("Inteligencia Artificial aplicada")
            st.info(f"**Asesor Virtual:** {get_advice(ingresos, gastos, ahorro)}")
            
            try:
                # Usamos el DF original completo para tener más contexto en la predicción
                prediccion = predict_next_month(df_raw) 
                st.warning(f"🔮 **Predicción para el próximo mes:** Gasto estimado de **{prediccion:.2f} €**")
                st.caption("Modelo: Regresión Lineal de Scikit-learn.")
            except:
                st.error("Datos insuficientes para predecir el futuro.")
            
            st.divider()
            st.subheader("Alertas de Seguridad")
            st.write(detect_anomalies(df))

        with tab4:
            st.subheader("Historial Completo")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV Procesado", data=csv, 
                               file_name='analisis_gastos.csv', mime='text/csv')

else:
    st.info("Por favor, sube tu archivo CSV para comenzar el análisis.")
    st.image("https://img.freepik.com/free-vector/personal-finance-concept-illustration_114360-5491.jpg", width=500)

# PIE DE PÁGINA
st.markdown("---")
st.caption(f"Desarrollado por Anxo Pena Blanco | Versión 1.1 | {datetime.now().year}")