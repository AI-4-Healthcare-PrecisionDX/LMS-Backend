from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
from contextlib import contextmanager
import time  # Add this import for time.sleep()

if settings.IS_DEV:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

else:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=15,
        pool_timeout=60,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def force_reset_pool():
    """Emergency function to reset connection pool"""
    global engine
    engine.dispose()
    # Wait briefly to allow connections to close
    time.sleep(2)
    # Create new engine with same settings
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        poolclass=QueuePool,  # Added this back
        pool_size=10,
        max_overflow=15,
        pool_timeout=60,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={  # Fixed comma after 1800
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    )
