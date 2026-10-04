from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session
from pwdlib import PasswordHash
from app.api.routers import oauth2
from app.db import session
from app.db.session import get_db
from app.models import models
from app.schemas.user import CreateTeam, TokenData, UserCreate, UserResponse 


password_hash = PasswordHash.recommended()
router = APIRouter(tags=['Authentication'])


@router.post("/register" , status_code=status.HTTP_201_CREATED, response_model= UserResponse )
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=password_hash.hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/teams")
def create_team(team : CreateTeam ,db: session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    
    new_team = models.Team(owner_id = current_user.id, **team.dict())

    db.add(new_team)
    db.commit()
    db.refresh(new_team)
     
    return new_team