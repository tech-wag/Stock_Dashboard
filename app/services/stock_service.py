from typing import Dict, Any
import os
import requests
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf

from app.utils.config import ALPHA_VANTAGE_API_KEY


def _empty_payload(symbol: str, reason: str) -> Dict[str, Any]:
    return {
        "symbol": symbol.upper(),
        "summary": f"No market data returned for {symbol.upper()}: {reason}",
        "technical_analysis": {
            "status": "unavailable",
            "reason": reason,
            "source": "market-data",
        },
        "price": None,
        "data_status": "unavailable",
        "forecast": None,
        "recommendation": "WAIT",
    }


def _parse_alpha_vantage_payload(payload: Dict[str, Any]) -> pd.DataFrame:
    time_series = payload.get("Time Series (Daily)") or payload.get("Time Series (Daily Adjusted)") or {}
    if not time_series:
        raise ValueError("Alpha Vantage payload did not contain daily time series")
    rows = []
    for date_str, values in time_series.items():
        try:
            rows.append({"Date": pd.to_datetime(date_str), "Close": float(values["4. close"])})
        except Exception:
            continue
    if not rows:
        raise ValueError("Alpha Vantage payload had no usable rows")
    df = pd.DataFrame(rows).sort_values("Date")
    df.set_index("Date", inplace=True)
    return df[["Close"]]


def _load_real_history(symbol: str, period_days: int) -> pd.DataFrame:
    if period_days <= 0:
        raise ValueError("period_days must be positive")

    if ALPHA_VANTAGE_API_KEY:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol.upper(),
            "outputsize": "compact",
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()
        if "Error Message" not in payload and "Note" not in payload:
            hist = _parse_alpha_vantage_payload(payload)
            return hist.tail(period_days)

    end = pd.Timestamp.today().normalize()
    start = end - pd.Timedelta(days=max(period_days + 30, 90))
    candidates = [symbol.upper(), f"{symbol.upper()}.US", symbol.upper().replace('.', '-')]
    last_error = None
    for candidate in candidates:
        try:
            hist = pdr.get_data_stooq(candidate, start=start, end=end)
            if not hist.empty:
                hist = hist[["Close"]].dropna()
                hist.index = pd.to_datetime(hist.index)
                return hist.tail(period_days)
        except Exception as exc:
            last_error = exc
    try:
        hist = yf.download(symbol.upper(), start=start, end=end, progress=False, auto_adjust=True)
        if not hist.empty:
            hist = hist[["Close"]].dropna()
            hist.index = pd.to_datetime(hist.index)
            return hist.tail(period_days)
    except Exception as exc:
        last_error = exc
    raise ValueError(f"no rows returned: {last_error}")


def _forecast_series(series: pd.Series, periods: int = 5) -> list[float]:
    if series.empty:
        return []
    values = series.astype(float).tolist()
    if len(values) < 2:
        return [round(values[-1], 2)] * periods
    x = np.arange(len(values), dtype=float)
    y = np.array(values, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    forecast = []
    current = values[-1]
    for _ in range(periods):
        current = current + slope
        forecast.append(round(current, 2))
    return forecast


def _prepare_chart_data(series: pd.Series) -> Dict[str, Any]:
    return {
        "dates": [d.strftime("%Y-%m-%d") for d in series.index],
        "prices": [round(float(v), 2) for v in series.tolist()],
    }


def _generate_ai_summary(symbol: str, price: float, change: float, forecast: Dict[str, Any]) -> str:
    direction = "upward" if change >= 0 else "downward"
    trend = "bullish" if forecast["next_5_days"][-1] > price else "cautious"
    return (
        f"{symbol.upper()} is trading at ${price:.2f} with a {change:.2f}% {direction} move. "
        f"The short-term outlook appears {trend}, with a projected 5-day value of ${forecast['next_5_days'][-1]:.2f}."
    )


def get_recommendations(risk_mode: str = "moderate") -> Dict[str, Any]:
    profiles = {
        "aggressive": [
            {"symbol": "NVDA", "reason": "High momentum and strong growth narrative"},
            {"symbol": "AMD", "reason": "Technological upside with elevated volatility"},
            {"symbol": "TSLA", "reason": "Momentum-driven swing potential"},
        ],
        "moderate": [
            {"symbol": "AAPL", "reason": "Stable trend with solid fundamentals"},
            {"symbol": "MSFT", "reason": "Steady growth and strong balance sheet"},
            {"symbol": "KO", "reason": "Defensive profile with consistent demand"},
        ],
        "low": [
            {"symbol": "VTI", "reason": "Broad market exposure with lower single-stock risk"},
            {"symbol": "SCHD", "reason": "Dividend and quality tilt"},
            {"symbol": "XLP", "reason": "Defensive sector exposure"},
        ],
    }
    normalized = risk_mode.lower()
    return {
        "risk_mode": normalized,
        "top_stocks": profiles.get(normalized, profiles["moderate"]),
        "headline": "Top picks for this week",
    }


def generate_stock_insight(symbol: str, period_days: int = 30, include_technical_analysis: bool = True) -> Dict[str, Any]:
    try:
        hist = _load_real_history(symbol, period_days)
    except Exception as exc:
        return {
            **_empty_payload(symbol, f"provider error: {exc}"),
            "ai_summary": "Live market data is temporarily unavailable. The dashboard will show the latest available structure while the provider recovers.",
            "chart_data": {"dates": [], "prices": []},
        }

    if hist.empty:
        return {
            **_empty_payload(symbol, "the data provider returned no rows"),
            "ai_summary": "Live market data is temporarily unavailable. The dashboard will show the latest available structure while the provider recovers.",
            "chart_data": {"dates": [], "prices": []},
        }

    latest = hist.iloc[-1]
    previous = hist.iloc[-2] if len(hist) > 1 else latest
    change = ((latest["Close"] - previous["Close"]) / previous["Close"]) * 100

    technical_analysis = {}
    if include_technical_analysis:
        technical_analysis = {
            "trend": "up" if latest["Close"] >= previous["Close"] else "down",
            "change_percent": round(change, 2),
            "latest_close": round(float(latest["Close"]), 2),
        }

    forecast_5 = _forecast_series(hist["Close"], periods=5)
    forecast_10 = _forecast_series(hist["Close"], periods=10)
    forecast_30 = _forecast_series(hist["Close"], periods=30)
    recommendation = "BUY" if forecast_5[-1] > float(latest["Close"]) else "WAIT"
    chart_data = _prepare_chart_data(hist["Close"])
    ai_summary = _generate_ai_summary(symbol, float(latest["Close"]), float(change), {"next_5_days": forecast_5})

    return {
        "symbol": symbol.upper(),
        "summary": f"{symbol.upper()} closed at ${round(float(latest['Close']), 2)} with a {round(change, 2)}% change over the selected period.",
        "technical_analysis": technical_analysis,
        "price": round(float(latest["Close"]), 2),
        "data_status": "ready",
        "forecast": {
            "next_5_days": forecast_5,
            "next_10_days": forecast_10,
            "next_30_days": forecast_30,
            "method": "linear-regression",
        },
        "recommendation": recommendation,
        "chart_data": chart_data,
        "ai_summary": ai_summary,
    }
