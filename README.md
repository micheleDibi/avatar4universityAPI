# Avatar4University API

Read-only REST API for accessing AI-generated university course data built with FastAPI.

## Data Hierarchy

**Course → Module → Lesson → Section → Slide**

- 119 courses, 495 modules, 3457 lessons, 17604 sections, 10040 slides

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set your API_KEY
```

## Run

```bash
uvicorn app.main:app --reload
```

Swagger docs available at `http://localhost:8000/docs`

## Authentication

All endpoints require the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-key" http://localhost:8000/api/v1/courses
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/courses` | List courses (paginated, filter by `language`, `course_type`) |
| GET | `/api/v1/courses/{id}` | Course detail with modules |
| GET | `/api/v1/courses/{id}/modules` | Modules of a course |
| GET | `/api/v1/modules/{id}` | Module detail with lessons |
| GET | `/api/v1/modules/{id}/lessons` | Lessons of a module |
| GET | `/api/v1/lessons/{id}` | Lesson detail with sections |
| GET | `/api/v1/lessons/{id}/sections` | Sections of a lesson |
| GET | `/api/v1/sections/{id}` | Section detail with slide |

### Pagination

Use `skip` (default: 0) and `limit` (default: 20, max: 100) query parameters on list endpoints.

### Filtering

`/api/v1/courses` supports:
- `language` — filter by language (e.g., `english`, `italian`)
- `course_type` — filter by type (e.g., `personal`, `organizational`)
