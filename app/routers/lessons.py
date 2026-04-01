from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.models import Lesson, Section, OpenQuestion, Module, Course
from app.schemas.schemas import LessonDetail, SectionList, OpenQuestionSchema

router = APIRouter(prefix="/lessons", tags=["lessons"])


def _get_lesson_in_org(db: Session, lesson_id: int, org_id: int) -> Lesson:
    lesson = (
        db.query(Lesson)
        .join(Module, Module.id == Lesson.module_id)
        .join(Course, Course.id == Module.course_id)
        .filter(Lesson.id == lesson_id, Course.organization_id == org_id)
        .first()
    )
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/{lesson_id}", response_model=LessonDetail)
def get_lesson(
    lesson_id: int,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    return _get_lesson_in_org(db, lesson_id, org_id)


@router.get("/{lesson_id}/sections", response_model=List[SectionList])
def list_lesson_sections(
    lesson_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    _get_lesson_in_org(db, lesson_id, org_id)
    return (
        db.query(Section)
        .filter(Section.lesson_id == lesson_id)
        .order_by(Section.order)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{lesson_id}/open-questions", response_model=List[OpenQuestionSchema])
def list_lesson_open_questions(
    lesson_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    _get_lesson_in_org(db, lesson_id, org_id)
    return (
        db.query(OpenQuestion)
        .filter(OpenQuestion.lesson_id == lesson_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
