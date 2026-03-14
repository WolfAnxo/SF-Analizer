import pandas as pd

def get_advice(ingresos, gastos, ahorro):
 
    if ingresos <= 0:
        return "Aún no he detectado ingresos. ¡Sube tu nómina para empezar el análisis!"

    ratio_ahorro = (ahorro / ingresos) * 100

    if ratio_ahorro < 0:
        return "🚨 Estás gastando más de lo que ganas. Revisa urgentemente la pestaña de 'Datos Crudos'."
    elif ratio_ahorro < 10:
        return f"⚠️ Tu ahorro es del {ratio_ahorro:.1f}%. Según la regla 50/30/20, deberías intentar llegar al 20% reduciendo gastos variables."
    elif 10 <= ratio_ahorro <= 20:
        return "⚖️ ¡Buen trabajo! Estás en la zona media. ¿Has probado a revisar tus 'Suscripciones' para dar el salto al 20%?"
    else:
        return "🚀 ¡Nivel Pro! Tu capacidad de ahorro es excelente. Es un buen momento para pensar en inversión a largo plazo."

def detect_anomalies(df):
  
    df_gastos = df[df["cantidad"] < 0].copy()
    if df_gastos.empty:
        return "No hay suficientes gastos para detectar anomalías."

    # Calculamos la media y la desviación estándar de los gastos
    media_gastos = df_gastos["cantidad"].abs().mean()
    desviacion = df_gastos["cantidad"].abs().std()
    
    # Cualquier gasto que sea mayor a la media o un gasto que represente más del 50% de la media mensual
    umbral = media_gastos + (2 * desviacion)
    
    anomalias = df_gastos[df_gastos["cantidad"].abs() > umbral]

    if not anomalias.empty:
        total_anomalias = len(anomalias)
        mayor_sustazo = anomalias["cantidad"].abs().max()
        return f"🚨 Alerta: He detectado {total_anomalias} gastos fuera de lo normal. El mayor ha sido de {mayor_sustazo:.2f} €."
    
    return "✅ No he detectado gastos sospechosos fuera de tu patrón habitual."