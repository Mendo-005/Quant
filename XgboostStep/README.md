# Predicción de Movimiento de Precios con XGBoost

Este proyecto utiliza Machine Learning (con XGBoost) para predecir si el precio de una acción subirá o bajará al día siguiente, usando indicadores técnicos (RSI, MACD, Bandas de Bollinger, retornos, etc.) como "features".

---

## Estructura del Proyecto

- **obtener_datos.py**: Descarga datos históricos y calcula los indicadores técnicos principales.
- **train.py**: Prepara los datos, crea la variable objetivo, divide en train/test, entrena el modelo XGBoost y evalúa su rendimiento.
- **visual_xgboost_estrategia.py**: Visualiza la importancia de features y simula la estrategia del modelo ML comparada con Buy & Hold.

---

## Detalle de Cada Archivo y Función

### 1. obtener_datos.py

**¿Qué hace?**
- Descarga los datos históricos de una acción (por ejemplo, AAPL) usando `yfinance`.
- Calcula indicadores técnicos con la librería `ta`:
  - **RSI (Relative Strength Index)**
  - **MACD (Moving Average Convergence Divergence) y su señal**
  - **Bandas de Bollinger (superior e inferior)**
- Calcula retornos pasados (lags) de 1, 2 y 3 días.
- Deja solo las filas completas (quita los valores NaN del DataFrame).

**Funciones principales:**
- Descargar datos con `yfinance`.
- Calcular indicadores técnicos usando la librería `ta`.
- Preparar el DataFrame con todas las features necesarias para el modelo.

---

### 2. train.py

**¿Qué hace?**
- Toma los datos ya procesados y genera la variable objetivo (`target`):
  - **target = 1:** si el precio de cierre del día siguiente es mayor al de hoy.
  - **target = 0:** si es menor o igual.
- Divide el dataset en un conjunto de entrenamiento y otro de prueba, respetando el orden temporal (para evitar "ver el futuro").
- Entrena un modelo de clasificación XGBoost usando las features calculadas.
- Evalúa el modelo utilizando:
  - **Accuracy** (precisión)
  - **Matriz de confusión**
  - **Reporte de clasificación** (precision, recall, f1-score)

**Funciones principales:**
- Crear la variable objetivo basada en el precio futuro.
- Dividir correctamente los datos en train/test.
- Entrenar el modelo `XGBClassifier`.
- Evaluar y mostrar métricas del modelo.

---

### 3. visual_xgboost_estrategia.py

**¿Qué hace?**
- Visualiza la importancia de cada feature (qué variables usa más el modelo).
- Simula una estrategia:
  - **Estrategia del modelo ML:** invierte solo cuando el modelo predice subida.
  - **Buy & Hold:** compra al inicio y mantiene.
- Compara visualmente el valor del portafolio con ambas estrategias.
- Muestra la señal diaria de predicción del modelo junto al precio real.

**Funciones principales:**
- Calcular la importancia relativa de los features del modelo.
- Simular el crecimiento del portafolio usando la señal del modelo.
- Graficar el resultado de la estrategia del modelo vs Buy & Hold.
- Graficar la señal del modelo respecto al precio real.

---

## Instalación de dependencias

```bash
pip install yfinance ta xgboost scikit-learn matplotlib pandas
```

---

## Ejecución recomendada

1. Ejecuta `obtener_datos.py` para calcular y guardar los datos con features.
2. Ejecuta `train.py` para entrenar y evaluar el modelo.
3. Ejecuta `visual_xgboost_estrategia.py` para ver la interpretación visual y simulación de la estrategia de trading.

---

## Notas

- El proyecto es didáctico, no constituye una recomendación de inversión.
- Puedes cambiar el ticker para analizar otras acciones.
- Prueba agregando nuevos indicadores o cambiando la forma de la variable objetivo para experimentar mejoras.

---