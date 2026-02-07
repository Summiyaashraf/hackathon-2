import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.database import engine
from src.models.task_model import SQLModel

def init_db():
    """Initialize the database by creating all tables."""
    print("Initializing database...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()