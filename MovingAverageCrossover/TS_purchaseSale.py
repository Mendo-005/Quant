import yfinance as yf
import pandas as pd
import numpy as np # Necesitamos numpy para la lógica de señales
import matplotlib.pyplot as plt

# ... (código de los pasos 1 y 2 para descargar datos y calcular SMAs) ...
# 1. Descargar los datos
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-12-31'
data = yf.download(ticker, start=start_date, end=end_date)

# 3. Calcular las Medias Móviles
short_window = 40
long_window = 100
data['SMA_short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['SMA_long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# --------------------------------------------------------------------
# --- NUEVO CÓDIGO - PASO 3 ---
# --------------------------------------------------------------------

# 5. Generar las Señales de Trading
print("\nGenerando señales de compra y venta...")

# Creamos una columna 'Signal' que inicialmente no contiene ninguna señal (valor 0).
data['Signal'] = 0

# Creamos una columna 'Position' que es 1 si la SMA_short > SMA_long y 0 en caso contrario.
# Esto nos dice si, en un día dado, nuestra estrategia "quiere" estar en el mercado.
data['Position'] = np.where(data['SMA_short'] > data['SMA_long'], 1, 0)

# El cruce es la diferencia en la posición de un día para otro.
# .diff() calcula la diferencia entre el valor de 'Position' de hoy y el de ayer.
# Si ayer era 0 y hoy 1, la diferencia es 1 (Señal de Compra).
# Si ayer era 1 y hoy 0, la diferencia es -1 (Señal de Venta).
data['Signal'] = data['Position'].diff()

# Mostremos solo los días donde hubo una señal de compra (1) o venta (-1).
print("\n--- Días con Señales de Trading ---")
trading_signals = data[(data['Signal'] == 1) | (data['Signal'] == -1)]
print(trading_signals[['Close', 'SMA_short', 'SMA_long', 'Signal']])


# 6. Visualizar las señales en el gráfico
# Vamos a mejorar nuestro gráfico anterior añadiendo marcadores para las señales.
print("\nActualizando gráfico con señales de compra/venta...")

plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Precio de Cierre (AAPL)', alpha=0.5) # Hacemos el precio un poco transparente
plt.plot(data['SMA_short'], label=f'Media Móvil de {short_window} días')
plt.plot(data['SMA_long'], label=f'Media Móvil de {long_window} días')

# Añadimos marcadores de compra: un triángulo verde hacia arriba '^'
plt.plot(data[data['Signal'] == 1].index, 
         data['SMA_short'][data['Signal'] == 1], 
         '^', markersize=12, color='g', label='Señal de Compra')

# Añadimos marcadores de venta: un triángulo rojo hacia abajo 'v'
plt.plot(data[data['Signal'] == -1].index, 
         data['SMA_short'][data['Signal'] == -1], 
         'v', markersize=12, color='r', label='Señal de Venta')

plt.title('Estrategia de Cruce de Medias Móviles para AAPL')
plt.xlabel('Fecha')
plt.ylabel('Precio (USD)')
plt.legend()
plt.grid(True)
plt.show()
