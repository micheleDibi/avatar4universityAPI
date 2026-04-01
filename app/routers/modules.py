from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.models import Module, Lesson, Course
from app.schemas.schemas import ModuleDetail, LessonList

router = APIRouter(prefix="/modules", tags=["modules"])


def _get_module_in_org(db: Session, module_id: int, org_id: int) -> Module:
    module = (
        db.query(Module)
        .join(Course, Course.id == Module.course_id)
        .filter(Module.id == module_id, Course.organization_id == org_id)
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.get("/{module_id}", response_model=ModuleDetail)
def get_module(
    module_id: int,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    return _get_module_in_org(db, module_id, org_id)


@router.get("/{module_id}/lessons", response_model=List[LessonList])
def list_module_lessons(
    module_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    _get_module_in_org(db, module_id, org_id)
    return (
        db.query(Lesson)
        .filter(Lesson.module_id == module_id)
        .order_by(Lesson.order)
        .offset(skip)
        .limit(limit)
        .all()
    )
