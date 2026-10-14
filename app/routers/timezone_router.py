from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controller import timezone_controller
from app.core.database import get_db
from app.schemas.timezone_schema import TimezoneResponse

router = APIRouter(prefix="/timezones", tags=["Timezones"])


@router.get("/", response_model=List[TimezoneResponse])
def list_timezones(db: Session = Depends(get_db)):
    return timezone_controller.get_all_timezones(db)
