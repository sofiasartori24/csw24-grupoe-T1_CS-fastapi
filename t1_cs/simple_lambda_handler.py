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
# Using only parameters supported by the installed Mangum version
handler = Mangum(
    app,
    lifespan="off",
    api_gateway_base_path="Prod"
)

# Log Mangum configuration
logger.info("Mangum configuration:")
logger.info(f"  api_gateway_base_path: Prod")
logger.info(f"  lifespan: off")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Simple AWS Lambda handler that passes requests to FastAPI.
    
    The Mangum handler is configured with api_gateway_base_path="Prod" to properly
    handle the API Gateway stage name. This ensures that requests with paths like
    "/Prod/users" are correctly routed to the FastAPI route "/users".
    
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
        
        # Extract API stage from the path and set it as an environment variable
        # This helps FastAPI configure the correct OpenAPI URL
        if 'requestContext' in event and 'stage' in event['requestContext']:
            stage = event['requestContext']['stage']
            os.environ['API_STAGE'] = stage
            logger.info(f"Setting API_STAGE environment variable to: {stage}")
        elif path.startswith('/Prod/'):
            os.environ['API_STAGE'] = 'Prod'
            logger.info("Setting API_STAGE environment variable to: Prod (from path)")
        
        # Check if the path exists in the FastAPI app
        path_exists = False
        for route in app.routes:
            if isinstance(route, APIRoute):
                # Remove the leading slash from the path for comparison
                route_path = route.path
                request_path = path
                
                # Strip the stage name if present (fallback mechanism)
                # Note: This should be handled by Mangum with api_gateway_base_path="Prod",
                # but we keep this as a safety check for route matching and debugging
                if request_path.startswith('/Prod'):
                    request_path = request_path[5:]
                    # Ensure root path is normalized to '/' instead of empty string
                    if request_path == '':
                        request_path = '/'
                
                logger.debug(f"Comparing route path '{route_path}' with request path '{request_path}'")
                
                # Check if the route matches the request path
                if route_path == request_path:
                    path_exists = True
                    logger.info(f"Found matching route: {route_path}")
                    break
        
        if not path_exists:
            logger.warning(f"No matching route found for path: {path}")
        
        # Modify the event to ensure the path is correctly formatted
        # This is a workaround for issues with the api_gateway_base_path parameter
        if path.startswith('/Prod'):
            # Create a copy of the event to avoid modifying the original
            modified_event = event.copy()
            
            # Extract the path without the /Prod prefix
            clean_path = path[5:] if path.startswith('/Prod') else path
            if clean_path == '':
                clean_path = '/'
                
            logger.info(f"Modifying path from '{path}' to '{clean_path}'")
            
            # Update the path in the event
            if 'path' in modified_event:
                modified_event['path'] = clean_path
            
            if 'rawPath' in modified_event:
                modified_event['rawPath'] = clean_path
                
            # Update the path in requestContext if present
            if 'requestContext' in modified_event:
                if 'path' in modified_event['requestContext']:
                    modified_event['requestContext']['path'] = clean_path
                
                if 'http' in modified_event['requestContext'] and 'path' in modified_event['requestContext']['http']:
                    modified_event['requestContext']['http']['path'] = clean_path
            
            # Pass the modified event to the Mangum handler
            logger.info(f"Passing modified event to Mangum handler with path: {clean_path}")
            response = handler(modified_event, context)
        else:
            # Pass the original event to the Mangum handler
            logger.info(f"Passing original event to Mangum handler with path: {path}")
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