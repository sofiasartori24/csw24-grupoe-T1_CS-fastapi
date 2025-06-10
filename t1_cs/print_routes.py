#!/usr/bin/env python3
"""
Script to print all available routes in the FastAPI application.
This helps diagnose routing issues.
"""

import os
import sys
import json
from fastapi.routing import APIRoute

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from app.main import app

def print_routes():
    """Print all available routes in the FastAPI application."""
    print("Available FastAPI routes:")
    
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            route_info = {
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods) if route.methods else [],
                "endpoint": route.endpoint.__name__ if hasattr(route.endpoint, "__name__") else str(route.endpoint)
            }
            routes.append(route_info)
            print(f"Route: {route.path}, Methods: {route.methods}, Name: {route.name}")
    
    # Save routes to a JSON file for reference
    with open("routes.json", "w") as f:
        json.dump(routes, f, indent=2)
    
    print(f"\nTotal routes: {len(routes)}")
    print("Routes have been saved to routes.json")

if __name__ == "__main__":
    print_routes()