from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional,List


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
    email : EmailStr
    age : int
    gender : str
    height : float
    weight : float
    created_at : datetime

    class Config:
        from_attributes = True

class WorkoutCreate(BaseModel):
    title : str
    workout_date : datetime
    total_duration : int
    notes : str

class WorkoutUpdate(BaseModel):
    title : Optional[str] = None
    workout_date : Optional[datetime] = None
    total_duration : Optional[int] = None
    notes : Optional[str] = None



class WorkoutResponse(WorkoutCreate):
    id : int
    owner_id :int

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

class WorkoutExerciseBase(BaseModel):
    workout_id : int
    exercise_id : int
    sets: int
    reps : int
    weight : float
    duration : int

class WorkoutExerciseUpdate(BaseModel):
    workout_id : Optional[int] = None
    exercise_id : Optional[int] = None
    sets : Optional[int] = None
    reps : Optional[int] = None
    weight : Optional[float] = None
    duration : Optional[int] = None
    
class WorkoutExerciseResponse(WorkoutExerciseBase):
    id : int

    class Config:
        from_attributes = True
    
class ExerciseLogBase(BaseModel):
    exercise_id : int
    date : datetime
    sets : int
    reps : int
    weight : float
    duration : int

class ExerciseLogUpdate(BaseModel):
    exercise_id : Optional[int] = None
    date : Optional[datetime] = None
    sets : Optional[int] = None
    reps : Optional[int] = None
    weight : Optional[float] = None
    duration : Optional[int] = None

class ExerciseLogResponse(ExerciseLogBase):
    id : int
    owner_id : int

    class Config:
        from_attributes = True

class BodyMeasurementBase(BaseModel):
    date : datetime
    weight : float
    chest : float
    waist : float
    arms : float
    thighs : float

class BodyMeasurementUpdate(BaseModel):
    date : Optional[datetime] = None
    weight : Optional[float] = None
    chest : Optional[float] = None
    waist : Optional[float] = None
    arms : Optional[float] = None
    thighs : Optional[float] = None

class BodyMeasurementResponse(BodyMeasurementBase):
    id : int
    owner_id : int

    class Config:
        from_attributes = True


class PaginatedExerciseResponse(BaseModel):
    data: List[ExerciseResponse]
    total: int
    page: int
    totalPages: int

    class Config:
        from_attributes = True

class PaginatedWorkoutResponse(BaseModel):
    data : List[WorkoutResponse]
    total : int
    page : int
    totalPages : int

    class Config:
        from_attributes = True

class PaginatedWorkoutExerciseResponse(BaseModel):
    data : List[WorkoutExerciseResponse]
    total : int
    page : int
    totalPages : int

    class Config:
        from_attributes = True

class PaginatedExerciseLogResponse(BaseModel):
    data : List[ExerciseLogResponse]
    total : int
    page : int
    totalPages : int

    class Config:
        from_attributes = True

class PaginatedBodyMeasuresResponse(BaseModel):
    data : List[BodyMeasurementResponse]
    total : int
    page : int
    totalPages : int

    class Config:
        from_attributes = True