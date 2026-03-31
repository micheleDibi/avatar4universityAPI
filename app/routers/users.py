from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .filter(User.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )
