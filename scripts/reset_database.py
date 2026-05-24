import asyncio
import sys
import os
from sqlalchemy import text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.db.session import engine
from app.models import Base

async def main():
    confirm = input("Are you sure you want to completely wipe the database? (y/N): ")
    if confirm.lower() != 'y':
        print("Aborting.")
        return

    print("Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Tables dropped.")
        
    print("Recreating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables recreated.")
        
    print("Database reset complete. Please run migrations manually to sync alembic version.")

if __name__ == "__main__":
    asyncio.run(main())
