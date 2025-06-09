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

# Create a handler for AWS Lambda with proper configuration for API Gateway
handler = Mangum(
    app,
    lifespan="off",
    api_gateway_base_path="Prod",  # Set the base path to the stage name
    api_gateway_strip_base_path=True  # Strip the base path before passing to FastAPI
)

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
    
    # Extract path for logging with more robust fallbacks
    path = event.get('path', event.get('rawPath', event.get('requestContext', {}).get('path', 'UNKNOWN')))
    method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method',
                       event.get('requestContext', {}).get('httpMethod', 'UNKNOWN')))
    
    # Handle API Gateway v2 format (HTTP API)
    if 'requestContext' in event and 'http' in event['requestContext']:
        path = event['requestContext']['http'].get('path', path)
        method = event['requestContext']['http'].get('method', method)
    
    logger.info(f"Processing request: {method} {path}")
    
    # Add more detailed logging for debugging path handling
    logger.debug(f"Full event: {json.dumps(event)}")
    logger.debug(f"Path from event: {path}")
    logger.debug(f"Method from event: {method}")
    logger.debug(f"Query string parameters: {event.get('queryStringParameters', {})}")
    logger.debug(f"Path parameters: {event.get('pathParameters', {})}")
    
    # Pass the event to the Mangum handler
    return handler(event, context)