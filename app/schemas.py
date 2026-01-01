from pydantic import BaseModel,EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name : str
    email : EmailStr
    password : str
    age : int
    gender : str
    height : float
    weight : float

class UserResponse(BaseModel):
    id : int
    name : str
    email : str
    age : int
    gender : str
    height : float
    weight : float
    created_at : datetime

    class Config:
        from_attributes = True

class Workout(BaseModel):
    user_id : int
    title : str
    workout_date : datetime
    total_duration : int
    notes : str

class WorkoutResponse(Workout):
    id : int

    class Config:
        from_attributes = True

class ExerciseBase(BaseModel):
    name : str
    description : str
    category : str
    muscle_group : str
    equipment : str


class ExerciseResponse(ExerciseBase):
    id : int

    class Config:
        from_attributes = True
    
