from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ActivityBase(BaseModel):
    
    amount:float = Field(
        ...,
        max_digits=9, 
        decimal_places=2,
        ge=Decimal("-9999999.99"),  # Opcional: Valor mínimo permitido
        le=Decimal("9999999.99"),
        description="amount of money",
        examples=["100.50", "-50.75"]
    )

    succeeded_in:datetime = Field(...,
            description="Date and time when the movement was completed",
        )

    transfer_id:int = Field(
            ..., description="ID of transfer"
        )

    account_id:int = Field(
                ..., description="ID of account"
            )
    activity_type_id:str = Field(
                    ..., description="ID of activity type"
                )
    timezone_id:str = Field(
                        ..., description="ID of timezone"
                    )
    
    
class ActivityCreate(ActivityBase):
    pass



    
class ActivityResponse(ActivityBase):

    id:int = Field(...,description="PK database", examples=[1])
    amount:Decimal = Field(..., description="amount of money", examples=["100.50", "-50.75"])
    succeeded_in:datetime = Field(..., description="Date and time when the movement was completed")
    transfer_id:int = Field(..., description="ID of transfer")
    account_id:int = Field(..., description="ID of account")
    activity_type_id:str = Field(..., description="ID of activity type")
    timezone_id:str = Field(..., description="ID of timezone")

    model_config = ConfigDict(from_attributes=True)


    