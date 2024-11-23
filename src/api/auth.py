from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserPOST, User
from passlib.context import CryptContext

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/register")
async def create_hotel(user_data: UserPOST):
    async with async_session_maker() as session:
        user_data = User(email=user_data.email, password=pwd_context.hash(user_data.password))
        await UsersRepository(session=session).add(user_data)
        await session.commit()
    return {"status": "OK"}