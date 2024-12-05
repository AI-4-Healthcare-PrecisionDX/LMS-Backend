from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal, force_reset_pool
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.api import deps
import logging


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
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# Health check endpoints
@app.get("/health")
async def health_check():
    """General health check endpoint"""
    return {"status": "healthy"}

@app.get("/health/db")
async def check_db_health(background_tasks: BackgroundTasks):
    """Database connection health check"""
    try:
        db = SessionLocal()
        try:
            # Test database connection
            db.execute(text("SELECT 1"))
            return {"status": "healthy"}
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            # If connection fails, trigger pool reset
            background_tasks.add_task(force_reset_pool)
            return {
                "status": "unhealthy",
                "message": "Resetting connection pool",
                "error": str(e)
            }
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Failed to create database session: {str(e)}")
        return {
            "status": "critical",
            "message": "Unable to establish database connection",
            "error": str(e)
        }

app.include_router(api_router, prefix=settings.API_V1_STR)
