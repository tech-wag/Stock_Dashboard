import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import requests
from app.utils.config import API_BASE_URL

st.set_page_config(page_title="AI Stock Insight Dashboard", page_icon="📈", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI Stock Insight Dashboard")
st.caption("Professional stock insights, forecasts, and simple action guidance")

with st.sidebar:
    st.header("Analysis Controls")
    symbol = st.text_input("Stock Symbol", value="AAPL")
    period_days = st.slider("Historical period (days)", 7, 180, 30)
    include_technical_analysis = st.checkbox("Include technical analysis", value=True)
    risk_mode = st.selectbox("User Mode", ["aggressive", "moderate", "low"], index=1)
    run = st.button("Analyze", use_container_width=True)

if run:
    try:
        rec_response = requests.get(f"{API_BASE_URL}/recommendations", params={"risk_mode": risk_mode}, timeout=20)
        rec_response.raise_for_status()
        rec_data = rec_response.json()

        st.subheader("Recommended Picks")
        st.caption(rec_data.get("headline", "Top picks for this week"))
        for item in rec_data.get("top_stocks", []):
            st.write(f"- **{item['symbol']}**: {item['reason']}")

        response = requests.post(
            f"{API_BASE_URL}/insights",
            json={
                "symbol": symbol,
                "period_days": period_days,
                "include_technical_analysis": include_technical_analysis,
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

        col1, col2, col3 = st.columns(3)
        col1.metric("Symbol", data.get("symbol", symbol))
        col2.metric("Current Price", f"${data.get('price', 'n/a')}")
        col3.metric("Recommendation", data.get("recommendation", "WAIT"))

        st.success("Analysis complete")
        st.write(data.get("summary", ""))

        if data.get("data_status") != "ready":
            st.info("Live market data is currently unavailable. The dashboard is showing the structured fallback view.")

        if data.get("ai_summary"):
            with st.expander("AI Summary Panel"):
                st.write(data.get("ai_summary"))

        chart_data = data.get("chart_data", {})
        if chart_data and chart_data.get("dates"):
            st.subheader("Price Trend")
            st.line_chart({"Price": chart_data["prices"]})

        if include_technical_analysis:
            with st.expander("Technical Analysis"):
                st.json(data.get("technical_analysis", {}))

        forecast = data.get("forecast")
        if forecast:
            st.subheader("Forecast Outlook")
            c1, c2, c3 = st.columns(3)
            c1.metric("5 Day Forecast", f"${forecast.get('next_5_days', [{}])[-1]}")
            c2.metric("10 Day Forecast", f"${forecast.get('next_10_days', [{}])[-1]}")
            c3.metric("30 Day Forecast", f"${forecast.get('next_30_days', [{}])[-1]}")

            tab1, tab2, tab3 = st.tabs(["5 Day", "10 Day", "30 Day"])
            with tab1:
                st.write(f"Projected values: {forecast.get('next_5_days', [])}")
            with tab2:
                st.write(f"Projected values: {forecast.get('next_10_days', [])}")
            with tab3:
                st.write(f"Projected values: {forecast.get('next_30_days', [])}")

            st.caption(f"Method: {forecast.get('method', 'unknown')}")
    except Exception as exc:
        st.error(f"Request failed: {exc}")
else:
    st.info("Enter a symbol and click Analyze to generate a stock insight snapshot.")
