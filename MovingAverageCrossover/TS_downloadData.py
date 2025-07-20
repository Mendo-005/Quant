import yfinance as yf
import pandas as pd

# 1. Descargar los datos
# Usamos el "ticker" o símbolo de la acción, en este caso 'AAPL' para Apple.
# definimos el período de tiempo que queremos analizar.
# 'start' y 'end' definen el rango de fechas.
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2025-07-10'

print(f"Descargando datos para {ticker} desde {start_date} hasta {end_date}...")

# La función yf.download() hace todo el trabajo por nosotros.
# El resultado es un DataFrame de Pandas, que es la estructura de datos estándar para este tipo de análisis.
data = yf.download(ticker, start=start_date, end=end_date)

# 2. Inspeccionar los datos
# Es una buena práctica revisar siempre los datos que acabas de descargar.
# .head() nos muestra las primeras 5 filas.
# .tail() nos muestra las últimas 5 filas.
# .info() nos da un resumen de la estructura del DataFrame (tipos de datos, valores nulos, etc.).

print("\n--- Primeras 5 filas de los datos ---")
print(data.head())

print("\n--- Últimas 5 filas de los datos ---")
print(data.tail())

print("\n--- Información general del DataFrame ---")
data.info()
 
print("\n--- Estadísticas descriptivas ---")
print(data.describe())

# 3. Guardar los datos en un archivo CSV
data.to_csv('AAPL_data.csv')
