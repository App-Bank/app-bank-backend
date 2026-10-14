from pydantic import BaseModel, ConfigDict


class TimezoneBase(BaseModel):
    name: str
    offset: str


class TimezoneCreate(TimezoneBase):
    pass


class TimezoneResponse(TimezoneBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
