import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
