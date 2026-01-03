from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models,schemas
from typing import List

router = APIRouter(
    prefix='/exerciselogs',
    tags=['ExerciseLogs']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.ExerciseLogResponse])
def get_exercise_logs(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exerciselogs = db.query(models.ExerciseLog).all()
    return exerciselogs


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ExerciseLogResponse)
def get_exercise_log(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise_log = db.query(models.ExerciseLog).filter(models.ExerciseLog.id == id).first()
    if exercise_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise log with id {id} not found')
    return exercise_log


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ExerciseLogResponse)
def create_exercise_logs(exercise_log:schemas.ExerciseLogBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_exerciselog = models.ExerciseLog(**exercise_log.dict())
    db.add(db_exerciselog)
    db.commit()
    db.refresh(db_exerciselog)
    return db_exerciselog


@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ExerciseLogResponse)
def update_exercise_log(id:int,exerciselog:schemas.ExerciseLogUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise_log = db.query(models.ExerciseLog).filter(models.ExerciseLog.id == id)
    existing_data = exercise_log.first()
    if exercise_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise log with id {id} not found')
    exercise_log.update(exerciselog.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_data = exercise_log.first()
    return updated_data

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ExerciseLogResponse)
def update_exercise_log(id:int,exerciselog:schemas.ExerciseLogBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_exercise_log = db.query(models.ExerciseLog).filter(models.ExerciseLog.id == id)
    existing_log = db_exercise_log.first()
    if existing_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise log with id {id} not found')
    db_exercise_log.update(exerciselog.dict(),synchronize_session=False)
    db.commit()
    updated_exercise_log = db_exercise_log.first()
    return updated_exercise_log

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise_log(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_exercise_log = db.query(models.ExerciseLog).filter(models.ExerciseLog.id == id).first()
    if db_exercise_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'exercise log with {id} not found')
    db.delete(db_exercise_log)
    db.commit()
    return {'message':'successfully deleted the exercise log'}