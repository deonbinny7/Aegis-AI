from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import user_service
from app.schemas.auth import Token, UserCreate
from app.core.security import create_access_token
from app.core.exceptions import AuthenticationError

class AuthService:
    async def authenticate(self, db: AsyncSession, email: str, password: str) -> Token:
        # Stub implementation
        if email == "admin" and password == "admin":
            return Token(access_token=create_access_token({"sub": email}), token_type="bearer")
        raise AuthenticationError("Incorrect email or password")
        
    async def register(self, db: AsyncSession, user_in: UserCreate):
        return await user_service.create_user(db, user_in)

auth_service = AuthService()

# Refactored for performance polish — 2026-06-16T19:37:39
