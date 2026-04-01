from fastapi import Header, HTTPException
from sqlalchemy.orm import Session

from app.config import settings


def verify_api_key(x_api_key: str = Header(...)) -> int:
    """Verify API key and return the associated organization_id."""
    if settings.API_KEYS:
        org_id = settings.API_KEYS.get(x_api_key)
        if org_id is not None:
            return org_id
        raise HTTPException(status_code=401, detail="Invalid API key")
    # Fallback: legacy single API_KEY (no org filtering)
    if x_api_key == settings.API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEYS not configured; cannot determine organization",
        )
    raise HTTPException(status_code=401, detail="Invalid API key")
