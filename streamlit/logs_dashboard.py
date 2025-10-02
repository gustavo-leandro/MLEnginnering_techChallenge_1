import streamlit as st
from datetime import date, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import plotly.express as px

from app.database import SessionLocal
from app.models import RequestLog

# --- Configurações da página ---
st.set_page_config(page_title="API Request Logs Dashboard", layout="wide")
st.title("API Request Logs Dashboard")

# --- Sidebar com filtros ---
st.sidebar.header("Filters")

# Intervalo de datas
start_default = date(2025, 9, 24)
end_default = date.today()
date_range = st.sidebar.date_input("Date range:", value=(start_default, end_default))
start_date, end_date = date_range
start_datetime = datetime.combine(start_date, time.min)
end_datetime = datetime.combine(end_date, time.max)

# Método HTTP
methods = ["All", "GET", "POST"]
selected_method = st.sidebar.selectbox("HTTP Method", methods, index=0)

# Endpoints
db: Session = SessionLocal()
endpoints = ["All"] + [row[0] for row in db.query(RequestLog.endpoint).distinct().all()]
selected_endpoint = st.sidebar.selectbox("Endpoint", endpoints, index=0)

# Status code
status_options = ["All", "2xx", "4xx", "5xx"]
selected_status = st.sidebar.selectbox("Status Code", status_options, index=0)

# --- Consulta no banco ---
query = db.query(RequestLog)

# Filtro por datas (comparando apenas a data)
query = query.filter(
    func.date(RequestLog.created_ts) >= start_datetime.date(),
    func.date(RequestLog.created_ts) <= end_datetime.date()
)

# Filtro por método
if selected_method != "All":
    query = query.filter(RequestLog.http_method == selected_method)

# Filtro por endpoint
if selected_endpoint != "All":
    query = query.filter(RequestLog.endpoint == selected_endpoint)

# Filtro por status
if selected_status != "All":
    if selected_status == "2xx":
        query = query.filter(RequestLog.status_code.between(200, 299))
    elif selected_status == "4xx":
        query = query.filter(RequestLog.status_code.between(400, 499))
    elif selected_status == "5xx":
        query = query.filter(RequestLog.status_code.between(500, 599))

logs = query.all()
db.close()

# --- Converter para DataFrame ---
df = pd.DataFrame([{
    "Method": log.http_method,
    "Path": log.endpoint,
    "Status": log.status_code,
    "Duration(ms)": log.duration_ms,
    "Created At": log.created_ts
} for log in logs])

if not df.empty:
    # --- Criar categorias de status ---
    def status_category(code):
        if 200 <= code < 300:
            return "2xx"
        elif 400 <= code < 500:
            return "4xx"
        elif 500 <= code < 600:
            return "5xx"
        else:
            return "Other"

    df["Status Category"] = df["Status"].apply(status_category)
    df["Date"] = df["Created At"].dt.date

    # --- Agrupar por dia e status ---
    df_grouped = df.groupby(["Date", "Status Category"]).size().reset_index(name="Count")

    # --- Gráfico diário por status com Plotly ---
    fig = px.bar(
        df_grouped,
        x="Date",
        y="Count",
        color="Status Category",
        barmode="group",
        title="Logs per day by Status",
        labels={"Count": "Number of Requests", "Date": "Date"},
        color_discrete_map={
            "2xx": "#328265",
            "4xx": "#FBC766",
            "5xx": "#E95F6B"
        },
        text="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

    df_avg = df.groupby("Path")["Duration(ms)"].mean().reset_index()
    df_avg = df_avg.sort_values("Duration(ms)", ascending=False)

    fig_avg = px.bar(
        df_avg,
        x="Path",
        y="Duration(ms)",
        text="Duration(ms)",  # adiciona os valores em cima das barras
        title="Average Response Time per Endpoint",
        labels={"Duration(ms)": "Average Duration (ms)", "Path": "Endpoint"},
        color="Duration(ms)",
        color_continuous_scale="Blues"  # tons de azul para visualização
    )

    fig_avg.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_avg.update_layout(xaxis_tickangle=-45)  # rotaciona labels se forem longos

    st.plotly_chart(fig_avg, use_container_width=True)

    st.dataframe(df.sort_values("Created At", ascending=False))
else:
    st.write("No logs found for the selected filters.")
