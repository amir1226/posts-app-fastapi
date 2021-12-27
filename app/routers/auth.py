from fastapi import Response, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..schemas import Token
from ..database import get_db
from .. import models, utils, oauth2

router=APIRouter(tags=['Authentication'])

@router.post('/login', response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter_by(email=user_credentials.username).first()
    
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    #Create token
    access_token = oauth2.create_access_token({"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

    