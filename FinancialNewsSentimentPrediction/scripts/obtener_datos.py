import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# === CONFIGURACIÓN ===
API_KEY = "bcc4aeaa6f204631969a37f16e95ea33"  # Sustituye con tu clave real
EMPRESA = "Apple"  # Cambia por la empresa que te interese
FECHA_FIN = datetime.today().date()
FECHA_INICIO = (FECHA_FIN - timedelta(days=7))  # Últimos 7 días

URL = "https://newsapi.org/v2/everything"

def obtener_noticias(empresa, fecha_inicio, fecha_fin):
    """
    Obtiene titulares de noticias usando News API.
    """
    params = {
        "q": empresa,            # Palabra clave de búsqueda (ejemplo: "Apple", "Tesla")
        "from": fecha_inicio,    # Fecha de inicio del rango (YYYY-MM-DD)
        "to": fecha_fin,         # Fecha de fin del rango (YYYY-MM-DD)
        "language": "en",        # Idioma de las noticias (en = inglés, es = español)
        "sortBy": "publishedAt", # Ordenar por fecha de publicación (otras opciones: relevancia, popularidad)
        "apiKey": API_KEY,       # Tu clave personal para autenticarte con News API
        "pageSize": 100          # Máx. de artículos por página (límite máx. permitido = 100)
    }


    response = requests.get(URL, params=params)
    data = response.json()

    #    {
    #  "status": "ok",
    #  "totalResults": 71,
    #  "articles": [
    #      {
    #        "source": {"id": "cnbc", "name": "CNBC"},
    #        "author": "John Doe",
    #        "title": "Apple to unveil new iPhone...",
    #        "description": "The company announced...",
    #        "url": "https://www.cnbc.com/article",
    #        "publishedAt": "2025-07-20T10:15:00Z",
    #        ...
    #      },
    #      ...
    #  ]
    #}

    if data.get("status") == "ok":
        articulos = data["articles"]
        df = pd.DataFrame([{
            "fecha": art["publishedAt"][:10],
            "titulo": art["title"],
            "fuente": art["source"]["name"],
            "url": art["url"]
        } for art in articulos])
        return df
    else:
        print("Error:", data)
        return pd.DataFrame()
    
    #    df = pd.DataFrame([
    #    {
    #        "fecha": "2025-07-20",
    #        "titulo": "Apple to unveil new iPhone",
    #        "fuente": "CNBC",
    #        "url": "https://www.cnbc.com/article"
    #    },
    #    {
    #        "fecha": "2025-07-19",
    #        "titulo": "Why Apple stock jumped 3%",
    #        "fuente": "Bloomberg",
    #        "url": "https://www.bloomberg.com/article"
    #    }
    #])
    #print(df)


if __name__ == "__main__":
    df_noticias = obtener_noticias(EMPRESA, FECHA_INICIO, FECHA_FIN)
    print(df_noticias.head())

    if not os.path.exists("FinancialNewsSentimentPrediction/data"):
        os.makedirs("FinancialNewsSentimentPrediction/data")
    # Guardar el DataFrame en un archivo CSV

    df_noticias.to_csv(f"FinancialNewsSentimentPrediction/data/noticias_{EMPRESA}.csv", index=False)
    print(f"Guardado en FinancialNewsSentimentPrediction/data/noticias_{EMPRESA}.csv")
