from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransferBase(BaseModel):
    amount: Decimal
    concept: Optional[str] = None


class TransferCreate(TransferBase):
    recipient_account_id: int
    timezone_id: int
    amount: Decimal = Field(gt=0)


class TransferResponse(TransferBase):
    id: int
    sender_account_id: int
    recipient_account_id: int
    timezone_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)