# AI Resume Analyzer

A portfolio-grade resume screening and job-match application with PDF extraction, deterministic skill analysis, REST API, and browser dashboard.

## Features
- PDF resume upload and text extraction
- Skill detection and job-description matching
- Match score, matched skills, missing skills and recommendations
- Browser dashboard at `/`
- Swagger/OpenAPI at `/docs`
- Health and skill-catalog endpoints
- Automated API tests
- Docker-ready deployment

## Stack
Python · FastAPI · Streamlit · PyPDF · Pydantic · Docker

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/` for the dashboard or `/docs` for API documentation.

## API
`POST /analyze` accepts multipart PDF resume + job description.
`GET /health` returns service status.
`GET /skills` returns the supported skill catalog.

## Docker
```bash
docker build -t ai-resume-analyzer .
docker run -p 8000:8000 ai-resume-analyzer
```

> Educational/portfolio decision-support software. Resume scores should not be used as the sole basis for employment decisions.
