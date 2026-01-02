from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


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

class WorkoutUpdate(BaseModel):
    user_id : Optional[int] = None
    title : Optional[str] = None
    workout_date : Optional[datetime] = None
    total_duration : Optional[int] = None
    notes : Optional[str] = None



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
    
class TokenData(BaseModel):
    id : Optional[int] = None