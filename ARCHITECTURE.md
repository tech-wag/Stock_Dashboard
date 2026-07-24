# Architecture Overview

## Vision
The AI Stock Insight Dashboard is a lightweight full-stack application for analyzing stock symbols, showing a current price snapshot, and generating simple forecasts with a buy/wait recommendation.

## Current Stack
- Frontend: Streamlit
- Backend: FastAPI
- Data layer: local demo-history generator with statistical forecasting
- Language: Python
- Container/cloud readiness: planned for GCP later

## High-Level Architecture

```text
User -> Streamlit UI -> FastAPI API -> Stock Service -> Forecast Engine
```

## Components
### 1. Frontend
- Provides symbol input, period selection, and analysis controls.
- Displays summary cards, technical analysis, and forecast tabs.

### 2. Backend API
- Exposes a simple POST endpoint for stock insights.
- Validates incoming requests and returns structured analysis.

### 3. Stock Service
- Generates a synthetic but realistic historical price series for the requested symbol.
- Computes simple trend-based technical metrics.
- Produces 5-day, 10-day, and 30-day forecasts.
- Emits a recommendation: BUY or WAIT.

### 4. Future Enhancements
- Replace demo data with a real market-data provider.
- Add LangChain-based AI narrative generation.
- Add charts and interactive visualizations.
- Deploy to GCP with CI/CD.

## Design Principles
- Simple and modular architecture
- Fast local iteration
- Clear separation between UI, API, and analysis logic
- Ready for future cloud deployment

## Repository and Delivery Conventions
- Source files, tests, documentation, and dependency manifests are versioned in Git.
- Local secrets and generated artifacts are excluded through .gitignore so the repo stays clean and safe.
- Environment templates such as .env.example are committed to help other developers configure the app locally.
- Agent-assisted changes should follow the repository governance guidance in .github/skills/git-repo-guidance/SKILL.md.

## Notes on LangChain
This project currently does not use LangChain yet. The current implementation focuses on a clean FastAPI + Streamlit foundation and a built-in forecasting layer. LangChain can be added later for AI-generated market summaries and reasoning.
