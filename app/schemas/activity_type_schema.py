from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ActivityTypeBase(BaseModel):
    name:Literal["debit", "credit"] = Field(...)


class ActivityTypeCreate(ActivityTypeBase):
    pass

    
class ActivityTypeResponse(ActivityTypeBase):
    id:int = Field(...)
    name:str = Field(...)

    model_config = ConfigDict(from_attributes=True)