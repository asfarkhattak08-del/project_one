from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
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
        raise HTTPException(status_code=404, detail="Team not found")
    
    new_project = models.Project(owner_id=current_user.id, **project_user.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project