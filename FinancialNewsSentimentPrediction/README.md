# Estrategia de Medias Móviles y Sentimiento de Noticias para Trading (AAPL)

Este proyecto implementa una **estrategia de trading que combina análisis técnico (medias móviles) y análisis de sentimiento de noticias** para el activo AAPL (Apple Inc.). Descarga datos históricos, obtiene noticias financieras relevantes, analiza el sentimiento con un modelo de IA y hace backtesting comparando la estrategia con un enfoque de "Buy & Hold". Incluye visualización y exportación de resultados.

---

## Descripción del Script

### 1. Configuración Inicial
- Define el ticker (`AAPL`), período de análisis, capital inicial y tu clave de NewsAPI para descargar noticias relacionadas.
- Variables clave:  
  - `TICKER`, `FECHA_INICIO`, `FECHA_FIN`, `CAPITAL_INICIAL`, `NEWSAPI_KEY`.

### 2. Descarga de Precios
- Descarga precios históricos ajustados de la acción usando `yfinance`.
- Usa solo la columna `Close` para el análisis.

### 3. Descarga de Noticias
- Usa [NewsAPI](https://newsapi.org/) para obtener hasta 500 artículos relevantes sobre el ticker en el período de análisis.
- Guarda las noticias en un archivo CSV.

### 4. Análisis de Sentimiento
- Utiliza el modelo FinBERT (`ProsusAI/finbert`) de Hugging Face para analizar el sentimiento de cada título de noticia.
- El sentimiento se cuantifica: positivo (+), negativo (-), neutral (0).
- Calcula el **sentimiento promedio diario** y lo agrega al DataFrame de precios.

### 5. Señales de Trading
- Calcula dos medias móviles (40 y 100 días) para generar señales técnicas de trading.
- **Señal tradicional:** Compra cuando la media móvil corta cruza por encima de la larga.
- **Ajuste de sentimiento:** Si el sentimiento diario es negativo (< -0.2), se evita comprar aunque la señal técnica sea positiva.
- Genera la señal final de compra/venta.

### 6. Backtesting
- Simula la estrategia:
  - Invierte todo el capital cuando la señal indica compra y no se está invertido.
  - Vende todo cuando la señal indica venta.
- Guarda el valor del portafolio en cada fecha.

### 7. Resultados
- Compara el valor final de la estrategia con el enfoque de "Buy & Hold" (comprar y mantener desde el inicio).
- Exporta los resultados a archivos CSV (`portfolio.csv` y `data_con_sentimiento.csv`).

### 8. Visualización
- Grafica la evolución del portafolio para la **estrategia combinada** y para **Buy & Hold**.

---

## ¿Qué necesitas para correrlo?

### Dependencias

- yfinance
- pandas
- numpy
- matplotlib
- requests
- transformers (requiere también torch)
- Una clave de NewsAPI (regístrate gratis en [https://newsapi.org/](https://newsapi.org/))

Instala las dependencias con:

```bash
pip install yfinance pandas numpy matplotlib requests transformers torch
```

### Uso

1. Coloca tu propia clave de NewsAPI en la variable `NEWSAPI_KEY`.
2. Ejecuta el script:
   ```bash
   python script.py
   ```
3. Se descargan precios y noticias, se analiza el sentimiento, se realiza el backtesting y se muestran los resultados en consola y en un gráfico.

---

## Personalización

- **Cambia el activo:** Modifica `TICKER` (ejemplo, 'MSFT' para Microsoft).
- **Cambia las ventanas de medias móviles:** Ajusta `short_window` y `long_window`.
- **Ajusta el umbral de sentimiento:** Cambia el valor en `if data["sentiment"] < -0.2` para ser más o menos estricto.
- **Modifica las fechas de análisis:** Cambia `FECHA_INICIO` y `FECHA_FIN`.

---

## Notas Importantes

- El modelo de sentimiento puede tardar en ejecutarse la primera vez (descarga de modelos).
- El backtesting es didáctico: no considera comisiones, slippage ni impuestos.
- El rendimiento pasado no garantiza resultados futuros.
- Las noticias y su sentimiento son ejemplos y pueden no cubrir todas las noticias relevantes del mercado.

---