import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.db.session import async_session
from app.schemas.auth import UserCreate
from app.services.users import user_service

async def main():
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    async with async_session() as db:
        user_in = UserCreate(email=email, password=password, username="admin")
        await user_service.create_user(db, user_in=user_in)
        print(f"Admin user {email} created successfully.")

if __name__ == "__main__":
    asyncio.run(main())
