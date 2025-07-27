import yfinance as yf
import pandas as pd
import ta

# (El código del Paso 1 aquí... puedes copiar de tu script anterior)
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2024-12-31'
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
close = data['Close'].squeeze()

data['rsi'] = ta.momentum.RSIIndicator(close=close).rsi()
macd = ta.trend.MACD(close=close)
data['macd'] = macd.macd()
data['macd_signal'] = macd.macd_signal()
bb = ta.volatility.BollingerBands(close=close)
data['bb_high'] = bb.bollinger_hband()
data['bb_low'] = bb.bollinger_lband()
data['return_1d'] = close.pct_change(1)
data['return_2d'] = close.pct_change(2)
data['return_3d'] = close.pct_change(3)
data = data.dropna()

# ---- PASO 2: Crear variable objetivo (target)
# Si el precio de cierre de mañana es mayor que el de hoy, target=1, sino 0
data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

# Elimina la última fila (no tiene target conocido)
data = data.iloc[:-1]

print(data[['Close', 'target']].tail())

# Guardar los datos procesados en un archivo CSV
data.to_csv('XgboostStep/datos_procesados.csv', index=True)
print("Datos procesados guardados en 'XgboostStep/datos_procesados.csv'")