from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user,oauth,workout


app = FastAPI()

app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(workout.router)

models.Base.metadata.create_all(bind=engine)

