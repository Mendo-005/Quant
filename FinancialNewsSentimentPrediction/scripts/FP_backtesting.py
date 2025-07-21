import os
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from transformers import pipeline

# ==============================
# 1. CONFIGURACIÓN INICIAL
# ==============================
TICKER = "AAPL"
FECHA_INICIO = "2024-07-01"
FECHA_FIN = "2025-07-21"
CAPITAL_INICIAL = 100000.0

# API KEY de NewsAPI (cambia por la tuya)
NEWSAPI_KEY = "bcc4aeaa6f204631969a37f16e95ea33"  # Sustituye con tu clave real

print(f"\nIniciando Backtesting con noticias para {TICKER} desde {FECHA_INICIO} hasta {FECHA_FIN}...")

# ==============================
# 2. DESCARGA DE PRECIOS
# ==============================
print("\nDescargando precios históricos...")
data = yf.download(TICKER, start=FECHA_INICIO, end=FECHA_FIN, auto_adjust=True)
data = data[["Close"]]  # Usamos Close porque auto_adjust=True ya ajusta dividendos y splits

# ==============================
# 3. DESCARGA DE NOTICIAS
# ==============================
def obtener_noticias(ticker, start_date, end_date):
    print("\nDescargando noticias desde NewsAPI (optimizado)...")
    url = "https://newsapi.org/v2/everything"
    noticias = []

    for page in range(1, 6):  # Máximo 5 páginas = 500 artículos
        params = {
            "q": ticker,
            "from": start_date,
            "to": end_date,
            "language": "en",
            "sortBy": "relevancy",
            "apiKey": NEWSAPI_KEY,
            "pageSize": 100,
            "page": page
        }
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            datos = resp.json()
            for art in datos["articles"]:
                noticias.append({
                    "date": art["publishedAt"][:10],
                    "title": art["title"],
                    "description": art["description"] if art["description"] else ""
                })
        else:
            print(f"Error en la página {page}: {resp.status_code}")
            break
    return pd.DataFrame(noticias)

df_noticias = obtener_noticias(TICKER, FECHA_INICIO, FECHA_FIN)
df_noticias.to_csv("noticias.csv", index=False)
print(f"{len(df_noticias)} noticias descargadas.")

# ==============================
# 4. ANÁLISIS DE SENTIMIENTO
# ==============================
print("\nAnalizando sentimiento de las noticias...")
sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analizar_sentimiento(texto):
    if not texto or len(texto.strip()) == 0:
        return 0
    resultado = sentiment_model(texto[:512])[0]  # Limite de tokens
    if resultado["label"] == "positive":
        return resultado["score"]
    elif resultado["label"] == "negative":
        return -resultado["score"]
    else:
        return 0

df_noticias["sentiment"] = df_noticias["title"].apply(analizar_sentimiento)

# Agregamos sentimiento diario promedio
sentiment_diario = df_noticias.groupby("date")["sentiment"].mean()
sentiment_diario = sentiment_diario.reindex(data.index.strftime("%Y-%m-%d")).fillna(0)
sentiment_diario.index = data.index
data["sentiment"] = sentiment_diario

# ==============================
# 5. SEÑALES DE TRADING
# ==============================
print("\nGenerando señales de trading...")
short_window = 40
long_window = 100

data["SMA_short"] = data["Close"].rolling(window=short_window).mean()
data["SMA_long"] = data["Close"].rolling(window=long_window).mean()
data.dropna(inplace=True)

# Señal técnica tradicional
data["Position"] = np.where(data["SMA_short"] > data["SMA_long"], 1, 0)

# Ajustamos señal con sentimiento: si sentimiento negativo fuerte -> no compramos
data["Position"] = np.where(data["sentiment"] < -0.2, 0, data["Position"])
data["Signal"] = data["Position"].diff()

# ==============================
# 6. BACKTESTING
# ==============================
print("\nIniciando backtesting...")
cash = CAPITAL_INICIAL
shares = 0.0
portfolio_values = []

for i in range(len(data)):
    precio = float(data["Close"].iloc[i])
    signal = data["Signal"].iloc[i]

    if not pd.isna(signal) and signal == 1 and cash > 0:
        shares = cash / precio
        cash = 0.0
        print(f"{data.index[i].date()}: COMPRA a ${precio:.2f}")

    elif not pd.isna(signal) and signal == -1 and shares > 0:
        cash = shares * precio
        shares = 0.0
        print(f"{data.index[i].date()}: VENTA a ${precio:.2f}")

    portfolio_values.append(cash + shares * precio)

portfolio = pd.DataFrame({"total": portfolio_values}, index=data.index)
portfolio["returns"] = portfolio["total"].pct_change()

# ==============================
# 7. RESULTADOS
# ==============================
data["buy_and_hold"] = CAPITAL_INICIAL * (data["Close"] / data["Close"].iloc[0])

print("\n--- RESULTADOS ---")
print(f"Capital Inicial: ${CAPITAL_INICIAL:,.2f}")
print(f"Valor Final Estrategia: ${portfolio['total'].iloc[-1]:,.2f}")
print(f"Valor Final Buy & Hold: ${data['buy_and_hold'].iloc[-1]:,.2f}")

portfolio.to_csv("portfolio.csv")
data.to_csv("data_con_sentimiento.csv")

# ==============================
# 8. VISUALIZACIÓN
# ==============================
plt.figure(figsize=(14, 7))
plt.plot(portfolio["total"], label="Estrategia con Sentimiento")
plt.plot(data["buy_and_hold"], label="Buy and Hold")
plt.title(f"Backtesting: {TICKER} (con noticias y sentimiento)")
plt.xlabel("Fecha")
plt.ylabel("Valor del Portafolio (USD)")
plt.legend()
plt.grid(True)
plt.show()
