from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user,oauth,workout,exercise_log,exercise,workout_exercise,body_measurement
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(workout.router)
app.include_router(exercise.router)
app.include_router(workout_exercise.router)
app.include_router(exercise_log.router)
app.include_router(body_measurement.router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        'redis://localhost:6379',
        encoding = "utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis),prefix="fastapi-cache")   
