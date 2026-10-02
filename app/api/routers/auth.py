from fastapi import APIRouter, Depends , status, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from sqlmodel import Session
from app import models
from app.db.session import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/register')
def register_user( user_credational: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.User)
    