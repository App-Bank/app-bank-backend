# NOTE: There's no need to create `timezone` endpoints
from fastapi import APIRouter

router = APIRouter(prefix="/timezones", tags=["Timezones"])