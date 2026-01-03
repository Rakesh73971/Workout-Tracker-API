from fastapi import APIRouter,HTTPException,status,Depends,Response,Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import schemas,models
import math
from sqlalchemy import asc,desc


router = APIRouter(
    prefix='/workoutexercises',
    tags=['WorkoutExercises']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=schemas.PaginatedWorkoutExerciseResponse)
def get_workoutexercises(db:Session=Depends(get_db),current_user=Depends(get_current_user),limit:int=Query(10,ge=1,le=10),page:int=Query(1,ge=1),sort_by:str=Query('id'),order:str=Query('asc')):
    sort_fields = {
        'id' : models.WorkoutExercise.id,
        'sets' : models.WorkoutExercise.sets,
        'reps' : models.WorkoutExercise.reps,
        'weight' : models.WorkoutExercise.weight
    }
    total = db.query(models.WorkoutExercise).count()
    total_pages = math.ceil(total/limit)
    offset = (page-1) * limit
    sort_column = sort_fields.get(sort_by,models.WorkoutExercise.id)
    
    query = db.query(models.WorkoutExercise)
    if order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
        
    workoutexercises = query.limit(limit).offset(offset).all()
    return {
        'data':workoutexercises,
        'total':total,
        'page':page,
        'totalPages':total_pages
    }



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.WorkoutExerciseResponse)
def get_workoutexercise(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workoutexercise = db.query(models.WorkoutExercise).filter(models.WorkoutExercise.id == id).first()
    if workoutexercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout exercise with id {id} not found')
    return workoutexercise



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.WorkoutExerciseResponse)
def create_wokout_exercise(workout_exercise:schemas.WorkoutExerciseBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout_exercise_db = models.WorkoutExercise(**workout_exercise.dict())
    db.add(workout_exercise_db)
    db.commit()
    db.refresh(workout_exercise_db)
    return workout_exercise_db



@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.WorkoutExerciseResponse)
def update_workout_exercise(id:int,workout_exercise:schemas.WorkoutExerciseUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout_exercise_db = db.query(models.WorkoutExercise).filter(models.WorkoutExercise.id == id)
    existing_workout = workout_exercise_db.first()
    if existing_workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout exercise with id {id} not found')
    workout_exercise_db.update(workout_exercise.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_workout = workout_exercise_db.first()
    return updated_workout




@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.WorkoutExerciseResponse)
def update_workout_exercise_db(id:int,workout_exercise:schemas.WorkoutExerciseBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    exercise_db = db.query(models.WorkoutExercise).filter(models.WorkoutExercise.id == id)
    existing_exercise_db = exercise_db.first()
    if existing_exercise_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout exercise with id {id} not found')
    exercise_db.update(workout_exercise.dict(),synchronize_session=False)
    db.commit()
    updated_exercises = exercise_db.first()
    return updated_exercises



@router.delete('/{id}')
def delete_workout_exercise(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    workout_exercise = db.query(models.WorkoutExercise).filter(models.WorkoutExercise.id == id).first()
    if workout_exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'workout exercise with id {id} not found')
    db.delete(workout_exercise)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)