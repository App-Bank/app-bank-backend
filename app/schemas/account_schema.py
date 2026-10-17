from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# TODO: adapt code to match auth feature (currently logged user GETs his linked account data)
class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    iban: str
    balance: Decimal = Field(description="Expected value is a NUMERIC one (n.nn) instead of an actual STRING")