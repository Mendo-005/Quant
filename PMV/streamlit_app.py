"""Streamlit aplicación para analizar la salud financiera de PYMES."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    data_path = Path(__file__).parent / "data" / "sample_financials.csv"
    df = pd.read_csv(data_path, parse_dates=["Fecha"])
    return df


@st.cache_data(show_spinner=False)
def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        raise ValueError("No se proporcionó archivo para cargar.")

    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file, parse_dates=["Fecha"])
        else:
            df = pd.read_excel(uploaded_file, parse_dates=["Fecha"])
    except Exception as exc:  # pragma: no cover - Streamlit warning message
        raise ValueError(
            "No se pudo leer el archivo. Verifique que el formato sea CSV o Excel "
            "y que contenga las columnas requeridas."
        ) from exc

    return df


def prepare_financials(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {
        "Fecha",
        "Ventas",
        "Costes_Variables",
        "Costes_Fijos",
        "Activo_Corriente",
        "Pasivo_Corriente",
        "Deuda_Total",
        "Patrimonio_Neto",
    }

    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(
            "Faltan columnas requeridas en el archivo: " "{}".format(", ".join(sorted(missing_cols)))
        )

    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df.sort_values("Fecha", inplace=True)
    df.reset_index(drop=True, inplace=True)

    df["Beneficio_Neto"] = df["Ventas"] - df["Costes_Variables"] - df["Costes_Fijos"]
    df["Margen_Neto"] = df["Beneficio_Neto"] / df["Ventas"].replace(0, pd.NA)
    df["Ratio_Liquidez"] = df["Activo_Corriente"] / df["Pasivo_Corriente"].replace(0, pd.NA)
    df["Nivel_Endeudamiento"] = df["Deuda_Total"] / (
        df["Deuda_Total"] + df["Patrimonio_Neto"].replace(0, pd.NA)
    )

    # Aproximación simple de flujo de caja operativo.
    working_capital_gap = df["Activo_Corriente"] - df["Pasivo_Corriente"]
    df["Flujo_Caja"] = df["Beneficio_Neto"] + 0.1 * working_capital_gap

    return df


def summarize_metrics(df: pd.DataFrame) -> Dict[str, float]:
    latest = df.iloc[-1]

    net_margin = float(latest["Margen_Neto"])
    liquidity_ratio = float(latest["Ratio_Liquidez"])
    debt_ratio = float(latest["Nivel_Endeudamiento"])

    margin_score = max(min(net_margin / 0.25 * 100, 100), 0)
    liquidity_score = max(min(liquidity_ratio / 2.0 * 100, 100), 0)
    debt_score = max(min((1 - debt_ratio) * 120, 100), 0)

    health_index = round((0.4 * margin_score + 0.35 * liquidity_score + 0.25 * debt_score), 1)

    return {
        "health_index": health_index,
        "net_margin": round(net_margin * 100, 1),
        "liquidity_ratio": round(liquidity_ratio, 2),
        "debt_ratio": round(debt_ratio, 2),
        "latest_cash_flow": float(latest["Flujo_Caja"]),
    }


def health_status_color(score: float) -> Tuple[str, str]:
    if score >= 70:
        return "#0f9d58", "Saludable"
    if score >= 45:
        return "#f4b400", "En observación"
    return "#db4437", "En riesgo"


def describe_liquidity(liquidity_ratio: float) -> str:
    if liquidity_ratio >= 1.5:
        tone = "Excelente capacidad para cubrir obligaciones de corto plazo."
    elif liquidity_ratio >= 1.0:
        tone = (
            "Liquidez aceptable, pero se recomienda reforzar caja para imprevistos "
            "y mantener el ratio por encima de 1.5."
        )
    else:
        tone = (
            "Liquidez insuficiente: por cada euro de deuda de corto plazo, hay menos "
            "de un euro disponible. Se requiere plan de acción inmediato."
        )
    return tone


def build_net_margin_gauge(margin: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=margin,
            number={"suffix": " %"},
            gauge={
                "axis": {"range": [0, 40]},
                "bar": {"color": "#0f9d58"},
                "steps": [
                    {"range": [0, 10], "color": "#ffe5e0"},
                    {"range": [10, 20], "color": "#fff4cc"},
                    {"range": [20, 40], "color": "#e0ffe5"},
                ],
                "threshold": {
                    "line": {"color": "#1a73e8", "width": 4},
                    "thickness": 0.75,
                    "value": 20,
                },
            },
        )
    )
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=10))
    return fig


def prophet_forecast(df: pd.DataFrame):
    from prophet import Prophet

    prophet_df = df[["Fecha", "Flujo_Caja"]].rename(columns={"Fecha": "ds", "Flujo_Caja": "y"})

    model = Prophet(seasonality_mode="multiplicative")
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=3, freq="M")
    forecast = model.predict(future)
    return forecast


def render_forecast_section(df: pd.DataFrame, metrics: Dict[str, float]) -> None:
    st.subheader("Proyección de Flujo de Caja a 3 Meses")
    sales_adjustment = st.slider(
        "Simula una variación en las ventas mensuales futuras (%)",
        min_value=-20,
        max_value=20,
        value=0,
        step=1,
        help=(
            "Ajusta la proyección según un escenario de caída o crecimiento en las ventas."
        ),
    )

    try:
        forecast = prophet_forecast(df)
    except Exception as exc:
        st.warning(
            "No fue posible generar la proyección con Prophet. "
            "Verifique que existan suficientes datos y que las dependencias estén instaladas."
        )
        st.exception(exc)
        return

    adjustment_factor = 1 + sales_adjustment / 100
    forecast.loc[forecast["ds"] > df["Fecha"].max(), "yhat"] *= adjustment_factor
    forecast.loc[forecast["ds"] > df["Fecha"].max(), "yhat_lower"] *= adjustment_factor
    forecast.loc[forecast["ds"] > df["Fecha"].max(), "yhat_upper"] *= adjustment_factor

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Fecha"],
            y=df["Flujo_Caja"],
            mode="lines+markers",
            name="Flujo de caja histórico",
            line=dict(color="#1a73e8"),
        )
    )

    forecast_future = forecast[forecast["ds"] > df["Fecha"].max()]
    fig.add_trace(
        go.Scatter(
            x=forecast_future["ds"],
            y=forecast_future["yhat"],
            mode="lines+markers",
            name="Proyección",
            line=dict(color="#111111", dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(forecast_future["ds"]) + list(forecast_future["ds"][::-1]),
            y=list(forecast_future["yhat_upper"]) + list(forecast_future["yhat_lower"][::-1]),
            fill="toself",
            fillcolor="rgba(17, 17, 17, 0.1)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="Intervalo 80%",
        )
    )

    zero_line = [0] * len(forecast_future)
    fig.add_trace(
        go.Scatter(
            x=forecast_future["ds"],
            y=zero_line,
            mode="lines",
            name="Punto de equilibrio",
            line=dict(color="#db4437", dash="dot"),
        )
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Flujo de caja (€)",
        margin=dict(l=20, r=20, t=20, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)

    future_risk = forecast_future["yhat"].min() < 0
    if future_risk:
        st.error(
            "⚠️ Riesgo detectado: la proyección muestra un déficit de caja en los próximos meses."
        )
    else:
        st.success(
            "✅ Proyección estable: no se detecta cruce por debajo de cero en los próximos meses."
        )


def render_executive_summary(df: pd.DataFrame, metrics: Dict[str, float]) -> None:
    st.subheader("Resumen Ejecutivo")

    color, label = health_status_color(metrics["health_index"])
    st.markdown(
        f"""
        <div style="background-color:#f8f9fa;border-radius:16px;padding:24px;text-align:center;">
            <span style="font-size:18px;color:#5f6368;">Índice de Salud Financiera</span>
            <div style="font-size:56px;font-weight:700;color:{color};margin:8px 0">{metrics['health_index']}/100</div>
            <span style="font-size:20px;font-weight:600;color:{color};">{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Margen de beneficio neto", f"{metrics['net_margin']}%", "+")
    kpi_cols[1].metric("Ratio de liquidez", metrics["liquidity_ratio"], "⚠" if metrics["liquidity_ratio"] < 1.5 else "")
    kpi_cols[2].metric("Nivel de endeudamiento", metrics["debt_ratio"], "✔")

    liquidity_text = (
        f"Su ratio de liquidez actual es {metrics['liquidity_ratio']}. {describe_liquidity(metrics['liquidity_ratio'])}"
    )
    st.info(
        "ALERTA: Aunque la rentabilidad es sólida, se debe monitorear de cerca la liquidez en los próximos 3 meses."
        if metrics["liquidity_ratio"] < 1.5
        else "Estado general positivos: mantener disciplina de costos y reforzar liquidez para crecer de manera sostenible."
    )
    st.write(liquidity_text)


def render_diagnostics_section(df: pd.DataFrame, metrics: Dict[str, float]) -> None:
    st.subheader("Diagnóstico Financiero Interactivo")
    rentabilidad_tab, liquidez_tab = st.tabs(["Rentabilidad", "Liquidez y Endeudamiento"])

    with rentabilidad_tab:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["Fecha"],
                y=df["Ventas"],
                mode="lines+markers",
                name="Ventas",
                line=dict(color="#1a73e8"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["Fecha"],
                y=df["Beneficio_Neto"],
                mode="lines+markers",
                name="Beneficio neto",
                line=dict(color="#34a853"),
            )
        )
        fig.update_layout(
            template="plotly_white",
            yaxis_title="€",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.plotly_chart(build_net_margin_gauge(metrics["net_margin"]), use_container_width=True)

    with liquidez_tab:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["Fecha"],
                y=df["Ratio_Liquidez"],
                mode="lines+markers",
                name="Ratio de liquidez",
                line=dict(color="#fbbc05"),
            )
        )
        fig.add_hline(y=1.0, line_dash="dot", line_color="#db4437", annotation_text="Umbral de riesgo")
        fig.update_layout(
            template="plotly_white",
            yaxis_title="Ratio",
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        debt_pct = metrics["debt_ratio"] * 100
        st.write(
            f"Su ratio de liquidez es de {metrics['liquidity_ratio']}. "
            f"Esto significa que por cada €1 de deuda a corto plazo, la empresa dispone de €{metrics['liquidity_ratio']:.2f} para cubrirla. "
            "Se recomienda mantenerlo por encima de 1.5."
        )
        st.write(
            f"El nivel de endeudamiento actual es {debt_pct:.1f}%. "
            "Valores por debajo del 60% suelen considerarse saludables para PYMES."
        )


def main() -> None:
    st.set_page_config(
        page_title="Analizador de Salud Financiera",
        page_icon="💹",
        layout="wide",
        menu_items={
            "About": "Aplicación de demostración para evaluar la salud financiera de PYMES en minutos.",
        },
    )

    st.title("Analizador de Salud Financiera para PYMES")
    st.caption("Suba sus datos financieros y obtenga un diagnóstico instantáneo y proyecciones de flujo de caja.")

    st.write(
        "El archivo debe contener las columnas: Fecha, Ventas, Costes_Variables, Costes_Fijos, "
        "Activo_Corriente, Pasivo_Corriente, Deuda_Total, Patrimonio_Neto."
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Suba su archivo CSV o Excel", type=["csv", "xlsx", "xls"])
    with col2:
        use_sample = st.button("Usar datos de ejemplo")

    df = None
    if use_sample:
        df = load_sample_data()
        st.success("Datos de ejemplo cargados correctamente.")
    elif uploaded_file is not None:
        try:
            df = load_uploaded_file(uploaded_file)
            st.success("Archivo cargado correctamente.")
        except ValueError as exc:
            st.error(str(exc))

    if df is None:
        st.info(
            "Cargue un archivo válido o utilice los datos de ejemplo para explorar el tablero interactivo."
        )
        return

    try:
        df = prepare_financials(df)
    except ValueError as exc:
        st.error(str(exc))
        return

    metrics = summarize_metrics(df)

    render_executive_summary(df, metrics)
    render_diagnostics_section(df, metrics)
    render_forecast_section(df, metrics)


if __name__ == "__main__":
    main()
