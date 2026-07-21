from fastapi import FastAPI

from app.routers import users
from app.routers import auth
from app.routers import admin


app = FastAPI(
    title="My API",
    version="1.0.0"
)


app.include_router(
    users.router
)

app.include_router(
    auth.router
)

app.include_router(
    admin.router
)


@app.get("/")
def root():
    return {
        "message": "API is running"
    }