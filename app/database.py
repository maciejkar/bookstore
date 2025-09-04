from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5433/bookstore")
    
    class Config:
        env_file = ".env"

settings = Settings()

print(f"Using DATABASE_URL: {settings.DATABASE_URL}")

# Add connection parameters for better error handling
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # This will log SQL queries
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300  # Recycle connections every 5 minutes
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
