import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ta
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# --- Carga y features (pega aquí tu código de pasos 1 y 2) ---
ticker = 'AAPL'
start_date = '2000-01-01'
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
data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
data = data.iloc[:-1]

# --- Selecciona features y target ---
features = ['rsi', 'macd', 'macd_signal', 'bb_high', 'bb_low', 'return_1d', 'return_2d', 'return_3d']
X = data[features]
y = data['target']

# --- Divide en train/test respetando el orden temporal ---
split = int(0.8 * len(data))
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# --- Entrena el modelo XGBoost ---
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# --- Predicciones ---
y_pred = model.predict(X_test)

# --- Evaluación ---
print("\nAccuracy en el conjunto de prueba:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:\n", confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))


# --- Visualización de la importancia de los features ---
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8,5))
plt.title("Importancia de los features")
plt.bar(range(len(features)), importances[indices], align="center")
plt.xticks(range(len(features)), [features[i] for i in indices], rotation=45)
plt.tight_layout()
plt.show()