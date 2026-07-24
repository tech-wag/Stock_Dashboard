import unittest
import pandas as pd

from app.services.stock_service import _forecast_series, _prepare_chart_data, _parse_alpha_vantage_payload


class ForecastSeriesTests(unittest.TestCase):
    def test_forecast_series_returns_requested_length(self):
        series = pd.Series([10, 12, 14, 16, 18], dtype=float)
        forecast = _forecast_series(series, periods=3)
        self.assertEqual(len(forecast), 3)
        self.assertTrue(all(value >= 0 for value in forecast))

    def test_prepare_chart_data_contains_dates_and_prices(self):
        series = pd.Series([100.0, 101.0, 102.0], index=pd.date_range("2024-01-01", periods=3, freq="D"))
        payload = _prepare_chart_data(series)
        self.assertIn("dates", payload)
        self.assertIn("prices", payload)
        self.assertEqual(len(payload["dates"]), 3)
        self.assertEqual(len(payload["prices"]), 3)

    def test_parse_alpha_vantage_payload_returns_close_series(self):
        payload = {
            "Time Series (Daily)": {
                "2024-01-02": {"4. close": "101.0"},
                "2024-01-03": {"4. close": "102.0"},
            }
        }
        df = _parse_alpha_vantage_payload(payload)
        self.assertEqual(list(df["Close"]), [101.0, 102.0])


if __name__ == "__main__":
    unittest.main()
