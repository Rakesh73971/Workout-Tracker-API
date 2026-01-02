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

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    muscle_group: Optional[str] = None
    equipment : Optional[str] = None

class ExerciseResponse(ExerciseBase):
    id : int

    class Config:
        from_attributes = True
    
class TokenData(BaseModel):
    id : Optional[int] = None


class ExerciseLogBase(BaseModel):
    user_id : int
    exercise_id : int
    date : datetime
    sets : int
    reps : int
    weight : float
    duration : int

class ExerciseLogUpdate(BaseModel):
    user_id : Optional[int] = None
    exercise_id : Optional[int] = None
    date : Optional[datetime] = None
    sets : Optional[int] = None
    reps : Optional[int] = None
    weight : Optional[float] = None
    duration : Optional[int] = None

class ExerciseLogResponse(ExerciseLogBase):
    id : int

    class Config:
        from_attributes = True
