from pydantic import BaseModel, ConfigDict, EmailStr


# NOTE: User creation was never an explicit assignment for the project


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr