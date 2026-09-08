# AI Resume Analyzer

Professional AI-assisted resume screening and job-match platform.

## Features
- PDF resume text extraction
- Skill detection and job-description matching
- Match score with matched/missing skills
- REST API and Streamlit demo UI
- Health endpoint and automated tests
- Docker-ready deployment

## Stack
Python · FastAPI · Streamlit · scikit-learn · PyPDF · Docker

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/docs` for the API.

## API
`POST /analyze` accepts multipart PDF resume + job description.

> Demo project for portfolio/education. AI scores are decision-support only.
