from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# class AccountCreate(BaseModel):
#     user_id: int
#     iban: str = Field(min_length=1, max_length=34)
#     balance: Decimal = Field(max_digits=9, decimal_places=2)


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    iban: str
    balance: Decimal