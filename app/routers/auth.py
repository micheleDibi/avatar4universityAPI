import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

CLERK_API_BASE = "https://api.clerk.com/v1"


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == body.email)
        .filter(User.deleted_at.is_(None))
        .first()
    )
    if not user or not user.clerk_id:
        return LoginResponse(status="error", message="Invalid credentials")

    resp = requests.post(
        f"{CLERK_API_BASE}/users/{user.clerk_id}/verify_password",
        headers={"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"},
        json={"password": body.password},
        timeout=10,
    )

    if resp.status_code == 200 and resp.json().get("verified"):
        return LoginResponse(status="ok")

    return LoginResponse(status="error", message="Invalid credentials")
