def calculate_balance(data):
    # Filtro los que son mayores a 0 (entradas de dinero) y los sumo uso .sum() de pandas que es más rápido que hacerlo a mano
    ingresos = data[data["cantidad"] > 0]["cantidad"].sum()
    
    # Aquí filtro los negativos. Ojo: los gastos ya vienen con el signo "-" así que al sumarlos python los resta automáticamente
    gastos = data[data["cantidad"] < 0]["cantidad"].sum()
    
    # El balance final. Como 'gastos' ya es negativo, uso el '+' para que se resten (ej: 1000 + (-400) = 600)
    ahorro = ingresos + gastos
    
    # Devuelvo los tres valores para usarlos en las cajitas de Streamlit
    return ingresos, gastos, ahorro