import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Read the database URL from environment variable
# Falls back to a local URL for development without Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://maudan:REDACTED@localhost:5432/currencywise"
)

# The engine is the actual connection to the database
# pool_pre_ping=True checks if the connection is alive before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory — calling SessionLocal() gives you a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our database models will inherit from
class Base(DeclarativeBase):
    pass


def get_db():
    """
    FastAPI dependency — provides a database session to route handlers.
    The 'yield' makes this a generator: code before yield = setup, after yield = cleanup.
    The session is automatically closed after the request finishes, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()