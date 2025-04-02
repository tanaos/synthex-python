import enum
from pydantic import BaseModel
from datetime import datetime


class JobStatus(str, enum.Enum):
    ON_HOLD = "On Hold"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    

class JobResponseModel(BaseModel):
    id: str
    name: str
    description: str
    datapoint_num: int
    output_domain: str
    status: JobStatus
    created_at: datetime


class ListJobsResponseModel(BaseModel):
    total: int
    jobs: list[JobResponseModel]