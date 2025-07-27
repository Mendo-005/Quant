# Estrategia de Medias Móviles para Trading con Backtesting en Python

Este proyecto implementa una **estrategia de trading basada en medias móviles** sobre el precio de cierre de Bitcoin (`BTC-USD`), realiza backtesting de las señales generadas y compara el rendimiento de la estrategia con el método tradicional de "Comprar y Mantener" (**Buy and Hold**). Además, guarda los resultados en archivos CSV y muestra visualizaciones para facilitar el análisis.

---

## Descripción del Script

### 1. Descarga de Datos
Utiliza `yfinance` para descargar datos históricos del precio de Bitcoin (u otro activo si cambias el ticker), desde el 01/01/2000 hasta el 20/07/2025.  
`data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)`

### 2. Cálculo de Medias Móviles
Calcula dos medias móviles simples (SMA):
- **SMA corta:** 40 días
- **SMA larga:** 100 días

Esto sirve para detectar cruces de medias, que generan señales de compra y venta.

### 3. Generación de Señales de Trading
- **Señal de compra:** Cuando la SMA corta cruza por encima de la larga.
- **Señal de venta:** Cuando la SMA corta cruza por debajo de la larga.
- `Position` es 1 si la estrategia está "dentro" (comprado), 0 si está "fuera".

### 4. Backtesting de la Estrategia
Simula la ejecución real de las señales:
- Comienza con un capital inicial de `$100,000`.
- Compra todo el activo cuando aparece una señal de compra.
- Vende todo cuando aparece una señal de venta.
- Calcula y guarda el valor total del portafolio en cada paso.

### 5. Cálculo de "Buy and Hold"
Calcula cuánto valdría el portafolio si simplemente hubieras comprado y mantenido el activo desde el inicio.

### 6. Resultados Finales
Muestra en consola:
- Capital inicial
- Valor final usando la estrategia de medias móviles
- Valor final usando Buy and Hold

### 7. Guardado de Resultados
Guarda los datos procesados (`data.csv`) y el portafolio (`portfolio.csv`) para análisis posterior.

### 8. Visualización
Grafica:
- El valor del portafolio usando la estrategia
- El valor del portafolio usando Buy and Hold

---

## Ejemplo de Ejecución

```bash
python script.py
```

La consola mostrará cada operación realizada (compra/venta), los resultados finales y se abrirá un gráfico comparativo.

---

## Dependencias

- yfinance
- pandas
- numpy
- matplotlib

Instálalas con:

```bash
pip install yfinance pandas numpy matplotlib
```

---

## Personalización

- **Cambiar el activo:** Modifica el valor de `ticker` (por ejemplo, `'ETH-USD'` para Ethereum).
- **Cambiar ventanas de medias móviles:** Ajusta `short_window` y `long_window` para experimentar con otras configuraciones.
- **Cambiar fechas:** Modifica `start_date` y `end_date` para acotar el análisis.

---

## Notas

- El backtesting no considera comisiones, deslizamientos ni impuestos.
- Ideal para uso educativo y de prototipado de estrategias.
- El rendimiento pasado no garantiza resultados futuros.

---