from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def predict_next_month(df):

    df_gastos = df[df["cantidad"] < 0].copy()
    
    # Agrupamos por mes 
    df_gastos['mes'] = df_gastos['fecha'].dt.to_period('M')
    resumen_mensual = df_gastos.groupby('mes')['cantidad'].sum().abs().reset_index()

    # Si tenemos menos de 2 meses, no se calcula
    if len(resumen_mensual) < 2:
        raise ValueError("Se necesitan al menos 2 meses de datos para predecir.")
    
    # Convertimos a un rango
    X = np.arange(len(resumen_mensual)).reshape(-1, 1)
    y = resumen_mensual['cantidad'].values
    model = LinearRegression()
    model.fit(X, y)
    # El próximo mes es el índice inmediatamente superior al último que tenemos
    proximo_mes_idx = np.array([[len(resumen_mensual)]])
    prediccion = model.predict(proximo_mes_idx)
    
    return max(0, prediccion[0])