import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Descargar los datos
ticker = 'BTC-USD '
start_date = '2000-01-01'
end_date = '2025-07-20'
print(f"Descargando datos para {ticker} desde {start_date} hasta {end_date}...")
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

# 2. Calcular las Medias Móviles
short_window = 40
long_window = 100
print(f"\nCalculando media móvil corta de {short_window} días y larga de {long_window} días...")
data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
data.dropna(inplace=True)

# 3. Generar las Señales de Trading
print("\nGenerando señales de compra y venta...")
data['Position'] = np.where(data['SMA_short'] > data['SMA_long'], 1, 0)
data['Signal'] = data['Position'].diff()

# 7. Backtesting de la Estrategia
print("\nIniciando backtesting de la estrategia...")
initial_capital = 100000.0
cash = initial_capital
shares = 0.0
portfolio_values = []

# Iteramos a través de los datos para simular el trading
for i in range(len(data)):
    current_price = float(data['Close'].iloc[i])
    signal = data['Signal'].iloc[i]
    
    # Si hay una señal de COMPRA y tenemos efectivo
    if not pd.isna(signal) and signal == 1 and float(cash) > 0:
        shares_to_buy = float(cash) / current_price
        shares += shares_to_buy
        cash = 0.0
        print(f"{data.index[i].date()}: COMPRA de {float(shares_to_buy):.2f} acciones a ${float(current_price):.2f}")

    # Si hay una señal de VENTA y tenemos acciones
    elif not pd.isna(signal) and signal == -1 and float(shares) > 0:
        cash_received = float(shares) * current_price
        cash = float(cash) + cash_received
        print(f"{data.index[i].date()}: VENTA de {float(shares):.2f} acciones a ${float(current_price):.2f}")
        shares = 0.0
    
    current_total_value = float(cash) + (float(shares) * current_price)
    portfolio_values.append(current_total_value)

# Después del bucle, creamos el DataFrame del portafolio
portfolio = pd.DataFrame({'total': portfolio_values}, index=data.index)
portfolio['returns'] = portfolio['total'].pct_change()

# 8. Calcular el rendimiento de "Buy and Hold"
data['buy_and_hold'] = initial_capital * (data['Close'] / data['Close'].iloc[0])

# 9. Resultados Finales
print("\n--- Resultados del Backtesting ---")
final_value_strategy = portfolio['total'].iloc[-1]
final_value_buy_hold = data['buy_and_hold'].iloc[-1]
print(f"Capital Inicial: ${initial_capital:,.2f}")
print(f"Valor Final (Estrategia): ${final_value_strategy:,.2f}")
print(f"Valor Final (Buy and Hold): ${final_value_buy_hold:,.2f}")

print("\n--- Guardando los datos y el portafolio en archivos CSV ---")
# Guardar los datos y el portafolio en archivos CSV
data.to_csv('data.csv')
portfolio.to_csv('portfolio.csv')

# 10. Visualización Final
plt.figure(figsize=(14, 7))
plt.plot(portfolio['total'], label='Rendimiento de la Estrategia')
plt.plot(data['buy_and_hold'], label='Rendimiento de Comprar y Mantener (Buy and Hold)')
plt.title('Rendimiento de la Estrategia vs. Buy and Hold')
plt.xlabel('Fecha')
plt.ylabel('Valor del Portafolio (USD)')
plt.legend()
plt.grid(True)
plt.show()

