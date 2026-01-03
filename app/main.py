from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user,oauth,workout,exercise_log,exercise,workout_exercise,body_measurement


app = FastAPI()

app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(workout.router)
app.include_router(exercise.router)
app.include_router(workout_exercise.router)
app.include_router(exercise_log.router)
app.include_router(body_measurement.router)

models.Base.metadata.create_all(bind=engine)

