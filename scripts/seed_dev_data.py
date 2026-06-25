import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.db.session import async_session

async def main():
    print("Seeding initial development data (No AI related seed data)...")
    # This script will insert basic structural non-AI data when required.
    # Currently placeholder.
    async with async_session() as db:
        pass
    print("Dev data seeded successfully.")

if __name__ == "__main__":
    asyncio.run(main())
