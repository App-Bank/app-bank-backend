from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ActivityTypeBase(BaseModel):
    name:Literal["debit", "credit"] = Field(
        ...,
        description="Name of the activity type",
        examples=["debit", "credit"]
    )


class ActivityTypeCreate(ActivityTypeBase):
    pass

    
class ActivityTypeResponse(ActivityTypeBase):
    id:int = Field(
        ...,
        description="PK database",
        examples=[1]
    )
    name:str = Field(
        ...,
        description="Name of the activity type",
        examples=["debit", "credit"]
    )
    model_config = ConfigDict(from_attributes=True)