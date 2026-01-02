from fastapi import status,APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db
from ..oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/workouts',
    tags=['Workout']
)



@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.WorkoutResponse])
def get_workouts(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workouts = db.query(models.Workout).all()
    return workouts



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.WorkoutResponse)
def get_workout(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout with id {id} not found')
    return workout



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.WorkoutResponse)
def create_workout(workout:schemas.Workout,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout_data = models.Workout(**workout.dict())
    db.add(workout_data)
    db.commit()
    db.refresh(workout_data)
    return workout_data



@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.WorkoutResponse)
def update_workout(id:int,workout:schemas.WorkoutUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout_data = db.query(models.Workout).filter(models.Workout.id == id)
    existing_data = workout_data.first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout id with {id} not found')
    workout_data.update(workout.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_data = workout_data.first()
    return updated_data



@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.WorkoutResponse)
def update_workout(id:int,workout:schemas.Workout,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_workout = db.query(models.Workout).filter(models.Workout.id == id)
    existing_db = db_workout
    if existing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout with id {id} not found')
    db_workout.update(workout.dict(),synchronize_session=False)
    db.commit()
    updated_data = db_workout.first()
    return updated_data

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout with id {id} not found')
    db.delete(workout)
    db.commit()
    return {'message':'successfully deleted the workout'}