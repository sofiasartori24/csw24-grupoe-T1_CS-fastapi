import os
import sys
import json
import logging
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.routing import APIRoute
from mangum import Mangum
from app.main import app

# Configure logging
logger = logging.getLogger("simple_lambda_handler")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

# Log all available routes for debugging
logger.info("Available FastAPI routes:")
for route in app.routes:
    if isinstance(route, APIRoute):
        logger.info(f"Route: {route.path}, Methods: {route.methods}")

# Create a simple handler for AWS Lambda
handler = Mangum(app)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Simple AWS Lambda handler that passes requests to FastAPI.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        Response dictionary
    """
    # Log the event for debugging
    logger.debug(f"Received event: {json.dumps(event)}")
    
    # Extract path for logging
    path = event.get('path', event.get('rawPath', 'unknown'))
    method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'unknown'))
    
    logger.info(f"Processing request: {method} {path}")
    
    # Pass the event to the Mangum handler
    return handler(event, context)