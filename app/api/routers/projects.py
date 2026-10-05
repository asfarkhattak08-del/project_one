from fastapi import APIRouter, Depends, HTTPException,status
from httpx import get
from sqlmodel import Session
from starlette.status import HTTP_404_NOT_FOUND
from app.db import session
from app.models import models
from app.api.routers import oauth2
from app.db.session import get_db
from app.schemas.project import CreateProject
from app.schemas.user import TokenData



router = APIRouter(tags=['Authentication'])


@router.post("/project")
def create_project(project_user: CreateProject,
                   current_user: TokenData = Depends(oauth2.get_current_user),
                   db: Session = Depends(get_db)):
    team = db.get(models.Team, project_user.team_id)
    if not team:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team not found")
    
    new_project = models.Project(owner_id=current_user.id, **project_user.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project




@router.get("/project/{project_id}")
def get_project( project_id : int ,db: session = Depends(get_db)):
    
    get_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    
    if not get_project:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Project with id: {id} do not exists")
    
    return get_project