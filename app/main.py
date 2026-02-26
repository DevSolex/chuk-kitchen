from fastapi import FastAPI
from .database import engine, Base
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chuks Kitchen API")

app.include_router(router)