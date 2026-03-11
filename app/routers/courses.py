from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Course, Module
from app.schemas.schemas import CourseList, CourseDetail, ModuleList

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=List[CourseList])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    language: Optional[str] = None,
    course_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Course)
    if language:
        query = query.filter(Course.language == language)
    if course_type:
        query = query.filter(Course.course_type == course_type)
    return query.offset(skip).limit(limit).all()


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/modules", response_model=List[ModuleList])
def list_course_modules(
    course_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.id == course_id).first()
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
