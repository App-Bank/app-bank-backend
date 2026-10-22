from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ActivityBase(BaseModel):
    
    amount: Decimal = Field(
        ...,
        max_digits=9, 
        decimal_places=2,
    )
    succeeded_in: datetime = Field(..., description="Date and time when the activity was successfully completed")
    transfer_id: int = Field(...)
    account_id: int = Field(...)
    activity_type_id: int = Field(...)
    
    
class ActivityCreate(ActivityBase):
    pass

    
class ActivityResponse(ActivityBase):
    id: int = Field(...)
    amount: Decimal = Field(...)
    succeeded_in: datetime = Field(...)
    transfer_id: int = Field(...)
    account_id: int = Field(...)
    activity_type_id: int = Field(...)
    account_iban: str

    
    model_config = ConfigDict(from_attributes=True)