from fastapi import FastAPI,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import database,models,utils,oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    
    access_token = oauth2.create_access_token(data={'user_id':user.id})
    return {'access_token':access_token,'token_type':'bearer'}
    
