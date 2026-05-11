# CurrencyWise 💱

Real-time currency converter built with FastAPI, vanilla JS, and Docker.

![CI](https://github.com/YOUR_USERNAME/currencywise/actions/workflows/ci.yml/badge.svg)

## Features
- Live exchange rates (updates every 10 minutes via caching)
- Supports 160+ currencies
- Clean, responsive UI
- Fully containerized with Docker
- Automated tests with CI/CD via GitHub Actions

## Tech Stack
FastAPI · Python · Docker · GitHub Actions · Nginx · Vanilla JS

## Quick Start

### With Docker (recommended):
\`\`\`bash
docker-compose up --build
\`\`\`
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Without Docker:
\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# Open frontend/index.html in your browser
\`\`\`

## Running Tests
\`\`\`bash
cd backend && pytest tests/ -v
\`\`\`

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/convert | Convert between currencies |
| GET | /api/currencies | List all supported currencies |
| GET | /health | Health check |
