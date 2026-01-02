from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException,APIRouter
from .. import models,schemas,utils


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {id} not found')
    return user

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserBase,db:Session=Depends(get_db)):
    hashed_password = utils.hashed(user.password)
    user.password = hashed_password
    user_data = models.User(**user.dict())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data