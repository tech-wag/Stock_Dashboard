from fastapi import FastAPI
from app.models.schemas import HealthResponse, StockInsightRequest, StockInsightResponse
from app.services.stock_service import generate_stock_insight, get_recommendations

app = FastAPI(title="AI Stock Insight Dashboard API", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok", "message": "API is running"}


@app.post("/insights", response_model=StockInsightResponse)
def get_insight(payload: StockInsightRequest):
    return generate_stock_insight(payload.symbol, payload.period_days, payload.include_technical_analysis)


@app.get("/recommendations")
def recommendations(risk_mode: str = "moderate"):
    return get_recommendations(risk_mode)
