from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.auth import verify_api_key
from app.database import get_db
from app.models.models import Course, Module, Lesson, Section
from app.schemas.schemas import CourseList, CourseDetail, ModuleList

router = APIRouter(prefix="/courses", tags=["courses"])

_eager_is_completed = (
    selectinload(Course.modules)
    .selectinload(Module.lessons)
    .selectinload(Lesson.sections)
    .selectinload(Section.slide)
)


@router.get("", response_model=List[CourseList])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    language: Optional[str] = None,
    course_type: Optional[str] = None,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Course)
        .options(_eager_is_completed)
        .filter(Course.organization_id == org_id)
    )
    if language:
        query = query.filter(Course.language == language)
    if course_type:
        query = query.filter(Course.course_type == course_type)
    return query.offset(skip).limit(limit).all()


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(
    course_id: int,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    course = (
        db.query(Course)
        .options(_eager_is_completed)
        .filter(Course.id == course_id, Course.organization_id == org_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/modules", response_model=List[ModuleList])
def list_course_modules(
    course_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.organization_id == org_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return (
        db.query(Module)
        .filter(Module.course_id == course_id)
        .order_by(Module.order)
        .offset(skip)
        .limit(limit)
        .all()
    )
