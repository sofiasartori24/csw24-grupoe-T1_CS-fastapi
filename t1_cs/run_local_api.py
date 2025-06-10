#!/usr/bin/env python3
"""
Script to run the FastAPI application locally for testing.
"""

import uvicorn
import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("Starting FastAPI application locally...")
    print("You can access the API at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    # Run the FastAPI application
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)