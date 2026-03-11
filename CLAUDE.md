# Avatar4University API

## Project Overview
Read-only FastAPI REST API exposing an SQLite database of AI-generated university courses.

## Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (`database.db`, ~500MB, read-only)
- **Auth**: API key via `X-API-Key` header (value from `.env`)

## Project Structure
```
app/
├── main.py          # FastAPI app entry point
├── config.py        # Settings from .env
├── database.py      # SQLAlchemy engine + session
├── auth.py          # API key verification dependency
├── models/models.py # ORM models (Course, Module, Lesson, Section, Slide)
├── schemas/schemas.py # Pydantic response schemas
└── routers/         # Endpoint routers (courses, modules, lessons, sections)
```

## Data Hierarchy
Course → Module → Lesson → Section → Slide (1:N at each level, Slide is 1:1 with Section)

## Running
```bash
pip install -r requirements.txt
cp .env.example .env  # then set API_KEY
uvicorn app.main:app --reload
```

## API Base URL
All endpoints are under `/api/v1/` and require the `X-API-Key` header.

## Key Conventions
- All endpoints are read-only (GET only)
- Pagination: `skip` and `limit` query params (default 0, 20)
- List endpoints return compact schemas; detail endpoints include nested children
- Ordered collections use the `order` column
