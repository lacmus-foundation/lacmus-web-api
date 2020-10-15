from pydantic import BaseModel
from typing import List
from typing import NewType
from uuid import UUID

JobID = NewType("JobID", UUID)

class Job(BaseModel):
    job: JobID

class JobArray(BaseModel):
    jobs: List[JobID]