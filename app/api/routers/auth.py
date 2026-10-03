from fastapi import APIRouter, Depends , status, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from sqlmodel import Session
from app import models
from app.db.session import get_db
from app import utils
from app.schemas.user import LoginResponse, UserResponse
from . import oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model = LoginResponse)
def register_user( user_credational: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credational.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f" invalide credationals")
    
    
    if not utils.verify(user_credational.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalide credationals")

    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})    
    
    
    return {
    "user": user,
    "token": {"access_token": access_token, "token_type": "bearer"},
}