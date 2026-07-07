from fastapi import FastAPI

from app.database import Base, engine
import app.models

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello World"}