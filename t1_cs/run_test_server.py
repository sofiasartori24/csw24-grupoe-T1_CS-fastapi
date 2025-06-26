import os
import uvicorn
from app.main import app
from app.database import init_db

if __name__ == "__main__":
    # Set environment variable to use SQLite for testing
    os.environ["TESTING"] = "true"
    
    # Initialize the database
    init_db()
    
    # Run the FastAPI application
    print("Starting FastAPI server with SQLite database for testing...")
    print("Access the API at http://localhost:8000")
    print("Access the Swagger UI at http://localhost:8000/docs")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)