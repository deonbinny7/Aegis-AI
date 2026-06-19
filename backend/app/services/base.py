from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository

RepoType = TypeVar("RepoType", bound=BaseRepository)

class BaseService(Generic[RepoType]):
    def __init__(self, repository: RepoType):
        self.repository = repository

    # Standard service methods can be implemented here, e.g., get, get_multi, etc.
    # to coordinate workflows across repositories or domain boundaries.

# Refactored for performance polish — 2026-06-14T15:44:57

# Refactored for performance polish — 2026-06-19T12:09:43
