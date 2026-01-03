from .database import Base
from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(DECIMAL(5, 2), nullable=False)
    weight = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    workout_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    total_duration = Column(Integer, nullable=False)
    notes = Column(Text)
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    muscle_group = Column(String, nullable=False)
    equipment = Column(String)


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(DECIMAL(5, 2))
    duration = Column(Integer)


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(DECIMAL(5, 2))
    duration = Column(Integer)
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)


class BodyMeasurement(Base):
    __tablename__ = "body_measurements"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())
    weight = Column(DECIMAL(5, 2), nullable=False)
    chest = Column(DECIMAL(5, 2))
    waist = Column(DECIMAL(5, 2))
    arms = Column(DECIMAL(5, 2))
    thighs = Column(DECIMAL(5, 2))
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)