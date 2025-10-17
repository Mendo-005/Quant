# Analizador de Salud Financiera para PYMES

Aplicación interactiva construida con Streamlit para demostrar en menos de cinco minutos cómo transformar un archivo financiero sencillo en un diagnóstico ejecutivo, análisis en profundidad y proyección de flujo de caja accionable.

## 🚀 Características clave

- **Carga amigable de datos**: soporte para CSV/Excel y botón de "Usar datos de ejemplo" listo para la demo.
- **Resumen ejecutivo**: índice de salud financiera con indicadores clave y alertas automáticas.
- **Diagnóstico interactivo**: pestañas con visualizaciones Plotly para rentabilidad, liquidez y endeudamiento.
- **Proyección predictiva**: modelo Prophet para flujo de caja a 3 meses con simulador *what-if*.

## 📦 Requisitos

- Python 3.9+
- Dependencias listadas en `requirements.txt`

## 🧪 Configuración local

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🗂️ Datos de ejemplo

El directorio `data/` incluye `sample_financials.csv` con las columnas requeridas:

- `Fecha`
- `Ventas`
- `Costes_Variables`
- `Costes_Fijos`
- `Activo_Corriente`
- `Pasivo_Corriente`
- `Deuda_Total`
- `Patrimonio_Neto`

## ☁️ Despliegue sugerido

La app está lista para subirse a [Streamlit Community Cloud](https://streamlit.io/cloud). Solo necesitas:

1. Crear un repositorio con estos archivos.
2. Conectar el repositorio en Streamlit Cloud.
3. Configurar `streamlit_app.py` como archivo principal y definir `requirements.txt`.

## 📈 Notas para la demo

1. Abre la app y muestra el botón **"Usar datos de ejemplo"** para cargar el dashboard al instante.
2. Recorre el **Resumen Ejecutivo** para explicar el índice y las alertas automáticas.
3. Cambia entre pestañas en **Diagnóstico Financiero** destacando las visualizaciones interactivas.
4. Juega con el slider en **Proyección de Flujo de Caja** para mostrar el escenario pesimista/optimista.

Listo: en menos de cinco minutos podrás narrar una historia financiera completa.
