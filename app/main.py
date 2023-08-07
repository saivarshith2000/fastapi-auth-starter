from fastapi import FastAPI
from .routes import auth, protected

app = FastAPI(
    title="FastAPI Auth",
    description="OAuth2 Password Flow with FastAPI and Postgres",
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(protected.router, prefix="/api/v1")