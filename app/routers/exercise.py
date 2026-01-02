from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models,schemas
from typing import List


router = APIRouter(
    prefix='/exercises',
    tags=['Exercises']
)


@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.ExerciseResponse])
def get_exercises(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercises = db.query(models.Exercise).all()
    return exercises


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ExerciseResponse)
def get_exercise(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise with id {id} not found')
    return exercise



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ExerciseResponse)
def create_exercise(exercise:schemas.ExerciseBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise_data = models.Exercise(**exercise.dict())
    db.add(exercise_data)
    db.commit()
    db.refresh(exercise_data)
    return exercise_data


@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ExerciseResponse)
def update_exercise(id:int,exercise:schemas.ExerciseUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == id)
    existing_data = db_exercise.first()
    if existing_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise with id {id} not found')
    db_exercise.update(exercise.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_exercise = db_exercise.first()
    return updated_exercise

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ExerciseResponse)
def updated_exercise(id:int,exercise:schemas.ExerciseBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise_data = db.query(models.Exercise).filter(models.Exercise.id == id)
    existing_data = exercise_data.first()
    if existing_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise with id {id} not found')
    exercise_data.update(exercise.dict(),synchronize_session=False)
    db.commit()
    updated_data = exercise_data.first()
    return updated_data

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise_data = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if exercise_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise with id {id} not found')
    db.delete(exercise_data)
    db.commit()
    return {'message':'successfully deleted the exercise'}