# NOTE: There's no need to create `activity_type` endpoints
from fastapi import APIRouter

router = APIRouter(prefix="/activity_type", tags=["Activity Type"])