from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from fastapi_utils.session import FastAPISessionMaker
from analisys import DatabaseUpdater, FakePredictionsGenerator, CitiesGenerator

# Application separated routers.
from prediction.router import router as prediction_router


# Database models.
import prediction.model as prediction_model
import city.model as city_model

# Database settings.
from database import engine
from database import SessionLocal


# Creating models.
prediction_model.Base.metadata.create_all(bind=engine)
city_model.Base.metadata.create_all(bind=engine)

# Application instance.
app = FastAPI()


origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connecting separated routers.
app.include_router(
    prediction_router,
    prefix='/prediction',
    tags=['Прогнозы'],
    responses={404: {'description': 'Not found'}}
)

app.include_router(
    prediction_router,
    prefix='/city',
    tags=['Города'],
    responses={404: {'description': 'Not found'}}
)


database_url = 'sqlite:///./app.db'
sessionmaker = FastAPISessionMaker(database_url)


# @app.on_event("startup")
# @repeat_every(seconds=30)  # 1 hour
# async def remove_expired_tokens_task() -> None:
#     with sessionmaker.context_session() as db:
#         database_update(db)


@app.on_event("startup")
async def remove_expired_tokens_task() -> None:
    with sessionmaker.context_session() as db:
        CitiesGenerator(db)
        # FakePredictionsGenerator(db)
