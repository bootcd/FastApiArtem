from pydantic import BaseModel, EmailStr


class UserPOST(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    email: EmailStr
    id: int

    class Config:
        from_attributes = True

class UserWithHashedPassword(User):
    password: str

    class Config:
        from_attributes = True
