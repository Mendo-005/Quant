import yfinance as yf
import pandas as pd
import ta

# 1. Descargar datos
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2024-12-31'
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

# Forzar que 'Close' sea una Serie 1D (por si acaso)
close = data['Close']
if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]
else:
    close = close.squeeze()

# 2. Calcular indicadores técnicos (features)
data['rsi'] = ta.momentum.RSIIndicator(close=close).rsi()
macd = ta.trend.MACD(close=close)
data['macd'] = macd.macd()
data['macd_signal'] = macd.macd_signal()
bb = ta.volatility.BollingerBands(close=close)
data['bb_high'] = bb.bollinger_hband()
data['bb_low'] = bb.bollinger_lband()

# Lags de retornos
data['return_1d'] = close.pct_change(1)
data['return_2d'] = close.pct_change(2)
data['return_3d'] = close.pct_change(3)

# Drop filas NaN
data = data.dropna()

print(data.head())
# Guardar los datos procesados en un archivo CSV
data.to_csv('XgboostStep/datos_procesados.csv', index=True)
print("Datos procesados guardados en 'XgboostStep/datos_procesados.csv'")