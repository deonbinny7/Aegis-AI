from app.services.base import BaseService
from app.repositories.base import BaseRepository
from app.models.sessions import Session
from pydantic import BaseModel

class SessionRepository(BaseRepository[Session, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Session)

class SessionService(BaseService[SessionRepository]):
    def __init__(self):
        super().__init__(SessionRepository())

session_service = SessionService()
