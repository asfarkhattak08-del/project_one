from fastapi import APIRouter, Depends, HTTPException,status

from app import models
from app.api.routers import oauth2
from app.db import session
from app.models.models import Project
from app.schemas.task import TaskCreate
from app.schemas.user import TokenData

router = APIRouter(tags=['Authentication'])



@router.post("/task", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate ,db: session = Depends(session.get_db),
                current_user : TokenData = Depends(oauth2.get_current_user)):

    project = db.Project(models.Project).filter(
        models.Project.id == task_in.project_id,
        models.Project.owner_id == current_user.id
    )