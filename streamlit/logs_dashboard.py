"""
Streamlit dashboard for API request logs analytics.
Filters: created_ts, http_method, endpoint, status_code
Shows request volume (2xx vs non-2xx) and average response time per endpoint.
"""

import streamlit as st
from datetime import date, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import plotly.express as px
from app.database import SessionLocal
from app.models import RequestLog


def get_distinct_endpoints(db: Session) -> list:
    """
    Get all distinct endpoints from the request logs table.
    """
    return [row[0] for row in db.query(RequestLog.endpoint).distinct().all()]


def fetch_logs(
    db: Session,
    start_datetime: datetime,
    end_datetime: datetime,
    method: str,
    endpoint: str,
    status: str,
) -> list:
    """
    Fetch logs from the database applying all filters.
    """
    query = db.query(RequestLog)
    query = query.filter(
        func.date(RequestLog.created_ts) >= start_datetime.date(),
        func.date(RequestLog.created_ts) <= end_datetime.date(),
    )
    if method != "All":
        query = query.filter(RequestLog.http_method == method)
    if endpoint != "All":
        query = query.filter(RequestLog.endpoint == endpoint)
    if status != "All":
        if status == "2xx":
            query = query.filter(RequestLog.status_code.between(200, 299))
        elif status == "4xx":
            query = query.filter(RequestLog.status_code.between(400, 499))
        elif status == "5xx":
            query = query.filter(RequestLog.status_code.between(500, 599))
    return query.all()


def status_category(code: int) -> str:
    """
    Categorize status code as 2xx, 4xx, 5xx, or Other.
    """
    if 200 <= code < 300:
        return "2xx"
    elif 400 <= code < 500:
        return "4xx"
    elif 500 <= code < 600:
        return "5xx"
    else:
        return "Other"


def main():
    """
    Main function to render the Streamlit dashboard.
    """
    st.set_page_config(page_title="API Request Logs Dashboard", layout="wide")
    st.title("API Request Logs Dashboard")

    # Sidebar filters
    st.sidebar.header("Filters")
    start_default = date(2025, 9, 24)
    end_default = date.today()
    date_range = st.sidebar.date_input(
        "Date range:", value=(start_default, end_default)
    )
    start_date, end_date = date_range
    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date, time.max)

    methods = ["All", "GET", "POST"]
    selected_method = st.sidebar.selectbox("HTTP Method", methods, index=0)

    db: Session = SessionLocal()
    endpoints = ["All"] + get_distinct_endpoints(db)
    selected_endpoint = st.sidebar.selectbox("Endpoint", endpoints, index=0)

    status_options = ["All", "2xx", "4xx", "5xx"]
    selected_status = st.sidebar.selectbox("Status Code", status_options, index=0)

    logs = fetch_logs(
        db,
        start_datetime,
        end_datetime,
        selected_method,
        selected_endpoint,
        selected_status,
    )
    db.close()

    # Convert to DataFrame
    df = pd.DataFrame(
        [
            {
                "Method": log.http_method,
                "Path": log.endpoint,
                "Status": log.status_code,
                "Duration(ms)": log.duration_ms,
                "Created At": log.created_ts,
            }
            for log in logs
        ]
    )

    if not df.empty:
        df["Status Category"] = df["Status"].apply(status_category)
        df["Date"] = df["Created At"].dt.date

        # Request volume chart
        df_grouped = (
            df.groupby(["Date", "Status Category"]).size().reset_index(name="Count")
        )
        fig = px.bar(
            df_grouped,
            x="Date",
            y="Count",
            color="Status Category",
            barmode="group",
            title="Logs per day by Status",
            labels={"Count": "Number of Requests", "Date": "Date"},
            color_discrete_map={"2xx": "#328265", "4xx": "#FBC766", "5xx": "#E95F6B"},
            text="Count",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Average response time per endpoint
        df_avg = df.groupby("Path")["Duration(ms)"].mean().reset_index()
        df_avg = df_avg.sort_values("Duration(ms)", ascending=False)
        fig_avg = px.bar(
            df_avg,
            x="Path",
            y="Duration(ms)",
            text="Duration(ms)",
            title="Average Response Time per Endpoint",
            labels={"Duration(ms)": "Average Duration (ms)", "Path": "Endpoint"},
            color="Duration(ms)",
            color_continuous_scale="Blues",
        )
        fig_avg.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_avg.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_avg, use_container_width=True)

        st.dataframe(df.sort_values("Created At", ascending=False))
    else:
        st.write("No logs found for the selected filters.")


if __name__ == "__main__":
    main()
