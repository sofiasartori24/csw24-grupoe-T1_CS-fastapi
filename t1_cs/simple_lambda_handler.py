import os
import sys
import json
import logging
import traceback
from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from mangum import Mangum
from app.main import app

# Create a new FastAPI app for testing
test_app = FastAPI()

@test_app.get("/lambda-test")
def lambda_test():
    """Simple test endpoint directly in the Lambda handler"""
    return {"message": "Lambda test endpoint is working!"}

# Use the original app but add our test endpoint
app.mount("/test-lambda", test_app)

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
        logger.info(f"Route: {route.path}, Methods: {route.methods}, Name: {route.name}")

# Log environment variables for debugging (masking sensitive info)
logger.info("Environment variables:")
for key, value in os.environ.items():
    if key.startswith('DB_') and 'PASSWORD' in key:
        logger.info(f"  {key}: {'*' * 8}")
    else:
        logger.info(f"  {key}: {value}")

# Create a handler for AWS Lambda with proper configuration for API Gateway
handler = Mangum(
    app,
    lifespan="off",
    api_gateway_base_path="Prod",  # Set the base path to the stage name
    api_gateway_strip_base_path=True  # Strip the base path before passing to FastAPI
)

# Log Mangum configuration
logger.info("Mangum configuration:")
logger.info(f"  api_gateway_base_path: Prod")
logger.info(f"  api_gateway_strip_base_path: True")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Simple AWS Lambda handler that passes requests to FastAPI.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        Response dictionary
    """
    request_id = context.aws_request_id if hasattr(context, 'aws_request_id') else "unknown"
    logger.info(f"Request ID: {request_id}")
    
    try:
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
        
        # Check if the path exists in the FastAPI app
        path_exists = False
        for route in app.routes:
            if isinstance(route, APIRoute):
                # Remove the leading slash from the path for comparison
                route_path = route.path
                request_path = path
                
                # Strip the stage name if present
                if request_path.startswith('/Prod'):
                    request_path = request_path[5:]
                
                logger.debug(f"Comparing route path '{route_path}' with request path '{request_path}'")
                
                # Check if the route matches the request path
                if route_path == request_path:
                    path_exists = True
                    logger.info(f"Found matching route: {route_path}")
                    break
        
        if not path_exists:
            logger.warning(f"No matching route found for path: {path}")
        
        # Pass the event to the Mangum handler
        logger.info(f"Passing request to Mangum handler")
        response = handler(event, context)
        
        # Log the response status code
        status_code = response.get('statusCode', 'unknown')
        logger.info(f"Response status code: {status_code}")
        
        # Log the response body if it's a 404
        if status_code == 404 or status_code == '404':
            body = response.get('body', '{}')
            logger.warning(f"404 Not Found response: {body}")
        
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'traceback': traceback.format_exc()
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }