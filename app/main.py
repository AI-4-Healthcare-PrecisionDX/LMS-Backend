from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.api import deps


def lifespan(app: FastAPI):
    # Startup event
    db: Session = SessionLocal()
    try:
        init_db(db)
        yield  # Application runs during this time
    finally:
        db.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
