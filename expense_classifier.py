def classify(description):
    text = str(description).lower()
    
    categorias = {
        "Comida": ["mercadona", "burger", "carrefour", "lidl", "restaurante", "uber eats", "glovo"],
        "Compras": ["amazon", "aliexpress", "zara", "decathlon", "ikea", "ebay"],
        "Suscripciones": ["netflix", "spotify", "disney", "hbo", "dazn", "prime video", "apple"],
        "Transporte": ["uber", "gasolina", "repsol", "renfe", "taxi", "cabify", "parking"],
        "Ingresos": ["nomina", "transferencia recibida", "ingreso", "bizum"],
        "Vivienda": ["alquiler", "luz", "agua", "gas", "comunidad"],
        "Ocio": ["cine", "concierto", "bar", "copas", "teatro"]
    }

    # Recorremos el diccionario buscando coincidencias
    for categoria, palabras_clave in categorias.items():
        for palabra in palabras_clave:
            if palabra in text:
                return categoria
    
    return "Otros"