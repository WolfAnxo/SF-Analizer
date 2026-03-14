import pandas as pd
import streamlit as st

def load_data(file):

    try:
        # Cargamos el CSV
        data = pd.read_csv(file)
        
        # Limpieza de nombres de columnas (quita espacios en blanco invisibles)
        data.columns = [col.strip().lower() for col in data.columns]
        
        # Validación de columnas
        columnas_necesarias = ["fecha", "descripcion", "cantidad"]
        if not all(col in data.columns for col in columnas_necesarias):
            st.error(f"⚠️ El CSV debe tener las columnas: {columnas_necesarias}")
            return None
        
        # Conversión de tipos con Pandas (El "motor" de tu análisis)
        # Usamos errors='coerce' para que si una fecha está mal, no rompa la app
        data["fecha"] = pd.to_datetime(data["fecha"], errors='coerce')
        
        # Eliminamos filas que hayan quedado con fecha o cantidad vacía
        data = data.dropna(subset=["fecha", "cantidad"])
        
        # Ordenamos por fecha para que las gráficas salgan bien
        data = data.sort_values("fecha")
        
        return data

    except Exception as e:
        st.error(f"❌ Error crítico al procesar el CSV: {e}")
        return None
