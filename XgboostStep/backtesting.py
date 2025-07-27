import yfinance as yf
import pandas as pd
import ta
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import numpy as np

# --- Paso 1: Carga y features ---
ticker = 'AAPL'
start_date = '2000-01-01'
end_date = '2025-07-24'
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
data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
data = data.iloc[:-1]

features = ['rsi', 'macd', 'macd_signal', 'bb_high', 'bb_low', 'return_1d', 'return_2d', 'return_3d']
X = data[features]
y = data['target']

split = int(0.8 * len(data))
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

model = XGBClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# --- Paso 2: Visualización de líneas de precio real y predicción ---
test_dates = data.index[split:]
test_close = data['Close'].iloc[split:]
preds = pd.Series(y_pred, index=test_dates)
actuals = y_test

# Línea de predicción: crea un portafolio que invierte solo cuando el modelo predice "sube"
initial_capital = 100_000
portfolio = pd.DataFrame(index=test_dates)
portfolio['close'] = test_close
portfolio['signal'] = preds.values  # 1=compra, 0=fuera

# Simula la estrategia: solo invertido cuando signal == 1
cash = initial_capital
shares = 0
values = []

for date, row in portfolio.iterrows():
    price = row['close']
    signal = row['signal']
    # Si predice COMPRA y no estamos invertidos, compramos todo
    if signal == 1 and shares == 0:
        shares = cash / price
        cash = 0
    # Si predice VENTA y estamos invertidos, vendemos todo
    elif signal == 0 and shares > 0:
        cash = shares * price
        shares = 0
    values.append(cash + shares * price)

portfolio['modelo'] = values

# Buy & Hold para comparación
portfolio['buy_hold'] = initial_capital * (portfolio['close'] / portfolio['close'].iloc[0])

# --- Visualización ---
plt.figure(figsize=(15, 7))
plt.plot(portfolio.index, portfolio['buy_hold'], label='Buy & Hold', color='gray', linewidth=2, alpha=0.6)
plt.plot(portfolio.index, portfolio['modelo'], label='Estrategia Modelo ML', color='orange', linewidth=2)
plt.title('Valor del portafolio: Estrategia Modelo vs Buy & Hold')
plt.ylabel('Valor del Portafolio (USD)')
plt.xlabel('Fecha')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Además, muestra la señal como línea (0=baja, 1=sube) y el precio real ---
plt.figure(figsize=(15, 6))
plt.plot(test_dates, test_close, label='Precio de Cierre', color='blue')
plt.plot(test_dates, preds, label='Predicción Modelo (1=Sube, 0=Baja)', color='red', alpha=0.6)
plt.title('Precio real y señal de predicción del modelo')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Evaluación del modelo ---
print("\nEvaluación del modelo:")
print("\nAccuracy en el conjunto de prueba:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:\n", confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))
