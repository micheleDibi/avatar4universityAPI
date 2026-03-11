from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Section
from app.schemas.schemas import SectionDetail

router = APIRouter(prefix="/sections", tags=["sections"])


@router.get("/{section_id}", response_model=SectionDetail)
def get_section(section_id: int, db: Session = Depends(get_db)):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section
