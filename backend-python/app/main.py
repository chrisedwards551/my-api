from fastapi import FastAPI
from sqlalchemy import text
from .database import engine

app = FastAPI()

@app.get("/")
def root():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.scalar()

    return {
        "message": "FastAPI is connected!",
        "postgres": version
    }