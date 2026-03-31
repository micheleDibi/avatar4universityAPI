from fastapi import Depends, FastAPI

from app.auth import verify_api_key
from app.routers import courses, modules, lessons, sections, quizzes, users

app = FastAPI(
    title="Avatar4University API",
    description="Read-only API for Avatar4University course data",
    version="1.0.0",
)

api_key_deps = [Depends(verify_api_key)]

app.include_router(courses.router, prefix="/api/v1", dependencies=api_key_deps)
app.include_router(modules.router, prefix="/api/v1", dependencies=api_key_deps)
app.include_router(lessons.router, prefix="/api/v1", dependencies=api_key_deps)
app.include_router(sections.router, prefix="/api/v1", dependencies=api_key_deps)
app.include_router(quizzes.router, prefix="/api/v1", dependencies=api_key_deps)
app.include_router(users.router, prefix="/api/v1")


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
