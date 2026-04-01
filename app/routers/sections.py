from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.models import Section, Lesson, Module, Course
from app.schemas.schemas import SectionDetail

router = APIRouter(prefix="/sections", tags=["sections"])


@router.get("/{section_id}", response_model=SectionDetail)
def get_section(
    section_id: int,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    section = (
        db.query(Section)
        .join(Lesson, Lesson.id == Section.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .join(Course, Course.id == Module.course_id)
        .filter(Section.id == section_id, Course.organization_id == org_id)
        .first()
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section
