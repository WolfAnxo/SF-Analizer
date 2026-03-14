import pandas as pd

def find_subscriptions(df):

    #Filtrar solo gastos
    gastos = df[df["cantidad"] < 0].copy()
    
    if gastos.empty:
        return []

    analisis = gastos.groupby("descripcion").agg(
        frecuencia=("cantidad", "count"),
        variacion_precio=("cantidad", "std"),
        precio_medio=("cantidad", "mean")
    ).reset_index()
    
    posibles_suscripciones = analisis[
        (analisis["frecuencia"] > 1) & 
        ((analisis["variacion_precio"] < 1.0) | (analisis["variacion_precio"].isna()))
    ]

    return posibles_suscripciones["descripcion"].tolist()