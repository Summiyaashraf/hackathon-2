import asyncio
from sqlalchemy import text
from backend.src.database.database import engine

async def test_db_connection():
    """Test database connection."""
    try:
        async with engine.begin() as conn:
            # Execute a simple query to test the connection
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(f"Query result: {result.fetchone()}")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    success = asyncio.run(test_db_connection())
    if success:
        print("✓ Database connection test passed")
    else:
        print("✗ Database connection test failed")