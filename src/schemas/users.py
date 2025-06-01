from pydantic import BaseModel, EmailStr, ConfigDict


class UserPOST(BaseModel):
    email: EmailStr
    password: str


class UserGET(BaseModel):
    email: EmailStr
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(UserGET):
    password: str


