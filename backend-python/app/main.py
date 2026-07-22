from fastapi import FastAPI, Request

from app.routers import users
from app.routers import auth
from app.routers import admin


app = FastAPI(
    title="My API",
    version="1.0.0"
)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next
):

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'"
    )

    return response


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