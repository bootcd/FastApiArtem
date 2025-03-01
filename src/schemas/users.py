from pydantic import BaseModel, EmailStr


class UserPOST(BaseModel):
    email: EmailStr
    password: str


class UserGET(BaseModel):
    email: EmailStr
    id: int

    class Config:
        from_attributes = True

class UserWithHashedPassword(UserGET):
    password: str

    class Config:
        from_attributes = True
