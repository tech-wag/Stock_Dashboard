from pydantic import BaseModel
from typing import Optional, Dict, Any


class HealthResponse(BaseModel):
    status: str
    message: str


class StockInsightRequest(BaseModel):
    symbol: str
    period_days: int = 30
    include_technical_analysis: bool = True


class StockInsightResponse(BaseModel):
    symbol: str
    summary: str
    technical_analysis: Dict[str, Any]
    price: Optional[float] = None
    data_status: str
    forecast: Optional[Dict[str, Any]] = None
