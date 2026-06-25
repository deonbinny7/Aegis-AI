from app.services.base import BaseService
from app.repositories.base import BaseRepository
from app.models.experiments import Experiment
from pydantic import BaseModel

class ExperimentRepository(BaseRepository[Experiment, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Experiment)

class ExperimentService(BaseService[ExperimentRepository]):
    def __init__(self):
        super().__init__(ExperimentRepository())

experiment_service = ExperimentService()
