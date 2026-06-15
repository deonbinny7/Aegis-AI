from app.services.base import BaseService
from app.repositories.base import BaseRepository
from app.models.prompt_versions import PromptVersion
from pydantic import BaseModel

class PromptVersionRepository(BaseRepository[PromptVersion, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(PromptVersion)

class PromptVersionService(BaseService[PromptVersionRepository]):
    def __init__(self):
        super().__init__(PromptVersionRepository())

prompt_version_service = PromptVersionService()

# Refactored for performance polish — 2026-06-15T17:16:55
