# AI Stock Insight Dashboard

The AI Stock Insight Dashboard is a lightweight web-based tool for exploring stock symbols, viewing a quick market snapshot, and generating simple forecasts with buy/wait guidance. It is useful for investors, students, and developers who want a fast way to prototype or demo an AI-assisted stock analysis experience.

## What this tool can be used for

- Quickly review a stock’s current price and recent change
- Explore short-term trend direction and technical signals
- Generate 5-day, 10-day, and 30-day price forecasts
- Get a simple recommendation such as BUY or WAIT
- Compare stock ideas using different risk profiles such as aggressive, moderate, or low risk
- Prototype a finance-focused web app with a FastAPI backend and Streamlit frontend

> This tool is intended for education, experimentation, and dashboard-style analysis. It should not be treated as financial advice.

## Key features

- Stock symbol input with a simple analysis workflow
- Current price, change percentage, and trend summary
- Technical analysis panel with the latest closing data and trend direction
- Forecast outlook using a lightweight linear regression approach
- AI-style summary text for quick interpretation of the results
- Recommended stock picks based on user-selected risk mode
- Built-in fallback behavior when live market data is unavailable

## Project structure

- app/api: FastAPI backend endpoints
- app/services: stock analysis and forecasting logic
- app/models: Pydantic schemas
- app/utils: configuration helpers
- frontend: Streamlit UI
- tests: service-level tests

## Run locally

### Backend

```bash
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
streamlit run frontend/app.py
```

## Git and repository hygiene

This repository should keep source code, tests, documentation, and dependency metadata in version control, while excluding local-only artifacts.

- Commit: app/, frontend/, tests/, README.md, ARCHITECTURE.md, requirements.txt, and .env.example
- Ignore: .env, virtual environments, Python cache folders, local logs, SQLite files, and editor-specific folders
- Use the agent skill in .github/skills/git-repo-guidance/SKILL.md when deciding what should be committed or ignored

## Next steps

- Connect to real market data providers for richer live data
- Add more advanced technical indicators and charting
- Expand the AI summary experience with richer prompts and explanations
- Prepare the app for deployment in a cloud environment
