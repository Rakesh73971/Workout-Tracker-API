from fastapi import status,APIRouter,HTTPException,Depends,Query
from sqlalchemy.orm import Session
from sqlalchemy import asc,desc
from .. import models,schemas
from ..database import get_db
from ..oauth2 import get_current_user
from typing import Optional
import math

router = APIRouter(
    prefix='/workouts',
    tags=['Workouts']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=schemas.PaginatedWorkoutResponse)
def get_workouts(db:Session=Depends(get_db),current_user=Depends(get_current_user),limit:int=Query(10,ge=1,le=10),page:int=Query(1,ge=1),search:Optional[str]="",sort_by:str=Query('id'),order:str=Query('asc')):
    
    sort_fields={
        "id":models.Workout.id,
        'name':models.Workout.title
    }
    query = db.query(models.Workout).filter(models.Workout.title.contains(search),models.Workout.owner_id == current_user.id)
    total = query.count()
    total_pages = math.ceil(total/limit)
    offset = (page-1) * limit

    sort_column = sort_fields.get(sort_by,models.Workout.id)
    
    if order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    workouts = query.limit(limit).offset(offset).all()

    return {
        'data':workouts,
        'total':total,
        'page':page,
        'totalPages':total_pages
    }



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.WorkoutResponse)
def get_workout(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == id,models.Workout.owner_id == current_user.id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout with id {id} not found')
    return workout



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.WorkoutResponse)
def create_workout(workout:schemas.WorkoutCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout_data = models.Workout(**workout.dict(exclude_unset=True),owner_id=current_user.id)
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
    if workout_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized')
    workout_data.update(workout.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_data = workout_data.first()
    return updated_data



@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.WorkoutResponse)
def update_workout(id:int,workout:schemas.WorkoutCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_workout = db.query(models.Workout).filter(models.Workout.id == id)
    existing_db = db_workout
    if existing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout with id {id} not found')
    
    if db_workout.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized')
    db_workout.update(workout.dict(),synchronize_session=False)
    db.commit()
    updated_data = db_workout.first()
    return updated_data

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout with id {id} not found')
    
    if workout.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized')
    
    db.delete(workout)
    db.commit()
    return {'message':'successfully deleted the workout'}