import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment - default to SQLite for local development
DATABASE_URL = os.getenv("NEON_DB_URL", "sqlite:///./todo_app.db")

# Create engine with connection pooling (skip for SQLite)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
    )

def get_session():
    with Session(engine) as session:
        yield session