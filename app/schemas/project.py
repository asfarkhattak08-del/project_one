
import datetime
from typing import Optional
from pydantic import BaseModel


class CreateProject(BaseModel):
    title: str
    description: Optional[str] 
    team_id: int
    