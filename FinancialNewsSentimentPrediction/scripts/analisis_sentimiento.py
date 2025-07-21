from datetime import datetime, timedelta
import os
import pandas as pd
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# =============================
# 1. CONFIGURACIÓN INICIAL
# =============================

# Descargamos el lexicón de VADER (solo se hace una vez)
nltk.download("vader_lexicon")

# Configura tu API Key de NewsAPI
API_KEY = "bcc4aeaa6f204631969a37f16e95ea33"  # <-- Sustituye con tu API Key
URL = "https://newsapi.org/v2/everything"
FECHA_FIN = datetime.today().strftime("%Y-%m-%d")
FECHA_INICIO = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")


# Carpeta donde guardaremos los datos
if not os.path.exists("FinancialNewsSentimentPrediction/data"):
    os.makedirs("FinancialNewsSentimentPrediction/data")

# =============================
# 2. FUNCIÓN PARA OBTENER NOTICIAS
# =============================

def obtener_noticias(empresa, fecha_inicio, fecha_fin):
    noticias_totales = []
    pagina = 1

    while True:
        params = {
            "q": empresa,
            "from": fecha_inicio,
            "to": fecha_fin,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": API_KEY,
            "pageSize": 100,
            "page": pagina
        }

        response = requests.get(URL, params=params)
        data = response.json()

        if data.get("status") != "ok" or not data["articles"]:
            break  # No hay más artículos

        articulos = data["articles"]
        noticias_totales.extend(articulos)

        if len(articulos) < 100:
            break  # Última página
        pagina += 1

    if noticias_totales:
        df = pd.DataFrame([{
            "fecha": art["publishedAt"][:10],
            "titulo": art["title"],
            "fuente": art["source"]["name"],
            "url": art["url"]
        } for art in noticias_totales])
        return df
    else:
        return pd.DataFrame()



# =============================
# 3. FUNCIÓN PARA ANALIZAR SENTIMIENTO
# =============================

sia = SentimentIntensityAnalyzer()

def analizar_sentimiento(titulo):
    score = sia.polarity_scores(titulo)["compound"]
    if score >= 0.05:
        return "positivo"
    elif score <= -0.05:
        return "negativo"
    else:
        return "neutro"
#{
# 'neg': 0.0,      # Nivel de negatividad (0 a 1)
# 'neu': 0.419,    # Nivel de neutralidad
# 'pos': 0.581,    # Nivel de positividad
# 'compound': 0.875  # Score final (-1 = muy negativo, +1 = muy positivo)
#}


# =============================
# 4. PROGRAMA PRINCIPAL
# =============================

if __name__ == "__main__":
    empresa = "Apple"  # Cambia por la empresa que quieras
    fecha_inicio = FECHA_INICIO  # Formato YYYY-MM-DD
    fecha_fin = FECHA_FIN  # Formato YYYY-MM-DD

    print(f"Obteniendo noticias sobre {empresa}...")
    df = obtener_noticias(empresa, fecha_inicio, fecha_fin)

    print(f"Se encontraron {len(df)} noticias.")
    print(df["fecha"].value_counts())
      # Muestra las primeras filas

    if not df.empty:
        # Agregar columna con el sentimiento
        df["sentimiento"] = df["titulo"].apply(analizar_sentimiento)

        # Guardar en CSV
        ruta_archivo = f"FinancialNewsSentimentPrediction/data/noticias_{empresa}.csv"
        df.to_csv(ruta_archivo, index=False)
        print(f"\nNoticias analizadas y guardadas en: {ruta_archivo}\n")

        print(df.head())  # Muestra las primeras filas
    else:
        print("No se encontraron noticias.")

import pandas as pd

# ======================================
# 5. Convertir sentimientos a valores numéricos
# ======================================

def sentimiento_a_valor(sentimiento):
    if sentimiento == "positivo":
        return 1
    elif sentimiento == "negativo":
        return -1
    else:
        return 0

# Aplicamos la conversión
df["sentimiento_valor"] = df["sentimiento"].apply(sentimiento_a_valor)

# ======================================
# 6. Calcular el promedio diario
# ======================================

sentimiento_diario = df.groupby("fecha")["sentimiento_valor"].mean().reset_index()

# Renombramos la columna para mayor claridad
sentimiento_diario.rename(columns={"sentimiento_valor": "sentimiento_promedio"}, inplace=True)

# ======================================
# 7. Guardar y mostrar resultados
# ======================================

ruta_sentimiento = f"FinancialNewsSentimentPrediction/data/sentimiento_diario_{empresa}.csv"
sentimiento_diario.to_csv(ruta_sentimiento, index=False)

print(f"\nSentimiento diario guardado en: {ruta_sentimiento}\n")
print(sentimiento_diario)
