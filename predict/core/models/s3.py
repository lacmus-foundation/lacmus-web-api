from pydantic import BaseModel
from typing import List
from typing import NewType
from uuid import UUID

ProjectID = NewType("ProjectID", UUID)
FileID = NewType("FileID", UUID)

class Predict(BaseModel):
    project: ProjectID
    files: List[FileID]
