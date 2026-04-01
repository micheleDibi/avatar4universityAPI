from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.models import User, UserOrganization
from app.schemas.schemas import UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .join(UserOrganization, UserOrganization.user_id == User.id)
        .filter(
            UserOrganization.organization_id == org_id,
            User.deleted_at.is_(None),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
