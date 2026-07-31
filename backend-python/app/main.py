from fastapi import FastAPI, Request

# Phase 15.9 — CORS Configuration
from fastapi.middleware.cors import CORSMiddleware


from app.routers import users
from app.routers import auth
from app.routers import admin
from app.routers import permissions


app = FastAPI(
    title="My API",
    version="1.0.0"
)


# Phase 15.9 — CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=[
        "*"
    ],
    allow_headers=[
        "*"
    ],
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

app.include_router(
    permissions.router
)


@app.get("/")
def root():
    return {
        "message": "API is running"
    }


# Phase 15.13 — Production Environment Hardening
# Health check endpoint for monitoring/deployment tools
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "python-api"
    }