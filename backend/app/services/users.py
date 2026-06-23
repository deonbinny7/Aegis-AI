from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.users import User
from app.schemas.auth import UserCreate
from app.core.security import get_password_hash
from app.core.exceptions import ValidationError

class UserRepository(BaseRepository[User, UserCreate, UserCreate]):
    def __init__(self):
        super().__init__(User)

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        # Check if user exists
        # This is a stub for real implementation
        password_hash = get_password_hash(user_in.password)
        # We would create the user via the repository here
        # Return a mocked user for now since we just need the stubs
        return User(email=user_in.email, password_hash=password_hash, full_name=user_in.username)

user_service = UserService()

# Refactored for performance polish — 2026-06-23T11:33:20
