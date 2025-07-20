import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt # Importamos matplotlib para graficar

# 1. Descargar los datos
ticker = 'GC=F'
start_date = '2001-01-01'
end_date = '2025-07-10'
print(f"Descargando datos para {ticker} desde {start_date} hasta {end_date}...")
data = yf.download(ticker, start=start_date, end=end_date)

# (El código de inspección de datos puede quedar aquí o lo puedes comentar)
# print("\n--- Primeras 5 filas de los datos ---")
# print(data.head())

# --------------------------------------------------------------------
# --- NUEVO CÓDIGO - PASO 2 ---
# --------------------------------------------------------------------

# 3. Calcular las Medias Móviles
# Definimos los períodos para nuestras medias móviles.
short_window = 40
long_window = 100

print(f"\nCalculando media móvil corta de {short_window} días y larga de {long_window} días...")

# Usamos la función .rolling() de Pandas.
# Esto crea una "ventana" deslizante del tamaño que especifiquemos.
# Luego, .mean() calcula el promedio de los valores dentro de esa ventana.
# Creamos dos nuevas columnas en nuestro DataFrame para almacenar estos valores.
data['SMA_short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['SMA_long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

print("\n--- Últimas 5 filas con las Medias Móviles calculadas ---")
print(data.tail())


# 4. Visualizar los datos y las medias móviles
# ¡Una imagen vale más que mil palabras! Graficar nos ayuda a entender lo que hemos hecho.
print("\nGenerando gráfico...")

plt.figure(figsize=(14, 7)) # Creamos una figura (un lienzo para el gráfico)
plt.plot(data['Close'], label='Precio de Cierre (AAPL)') # Graficamos el precio de cierre
plt.plot(data['SMA_short'], label=f'Media Móvil de {short_window} días') # Graficamos la media corta
plt.plot(data['SMA_long'], label=f'Media Móvil de {long_window} días') # Graficamos la media larga

plt.title('Precio de Cierre de AAPL y Medias Móviles')
plt.xlabel('Fecha')
plt.ylabel('Precio (USD)')
plt.legend() # Muestra las etiquetas de cada línea
plt.grid(True) # Añade una cuadrícula para facilitar la lectura
plt.show() # Muestra el gráfico
