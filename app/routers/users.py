from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_clerk_token
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
def get_current_user(
    clerk_id: str = Depends(verify_clerk_token),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.clerk_id == clerk_id)
        .filter(User.deleted_at.is_(None))
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
