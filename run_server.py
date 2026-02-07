import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the FastAPI server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"

    print(f"Starting server on {host}:{port}")
    print(f"Auto-reload: {reload}")

    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    main()