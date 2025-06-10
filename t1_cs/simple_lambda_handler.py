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

# Initialize logging
logger.info("FastAPI application initialized")

# Log important environment variables
logger.info("Environment check: Lambda execution environment ready")

# Configure Mangum handler for API Gateway integration
handler = Mangum(
    app,
    lifespan="off",
    api_gateway_base_path="Prod"
)

logger.info("Mangum configured with api_gateway_base_path=Prod")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for FastAPI application.
    
    Handles API Gateway integration and path normalization.
    
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
        
        # Log essential request details
        logger.debug(f"Path: {path}, Method: {method}")
        
        # Extract API stage from the path and set it as an environment variable
        # This helps FastAPI configure the correct OpenAPI URL
        if 'requestContext' in event and 'stage' in event['requestContext']:
            stage = event['requestContext']['stage']
            os.environ['API_STAGE'] = stage
            logger.info(f"Setting API_STAGE environment variable to: {stage}")
        elif path.startswith('/Prod/'):
            os.environ['API_STAGE'] = 'Prod'
            logger.info("Setting API_STAGE environment variable to: Prod (from path)")
        
        # Quick route validation
        request_path = path[5:] if path.startswith('/Prod') else path
        if request_path == '':
            request_path = '/'
            
        path_exists = any(
            isinstance(route, APIRoute) and route.path == request_path
            for route in app.routes
        )
        
        if not path_exists:
            logger.warning(f"No matching route found for path: {path}")
        
        # Handle API Gateway stage prefix in path
        if path.startswith('/Prod'):
            modified_event = event.copy()
            
            clean_path = path[5:] if path.startswith('/Prod') else path
            if clean_path == '':
                clean_path = '/'
                
            logger.info(f"Modifying path from '{path}' to '{clean_path}'")
            
            if 'path' in modified_event:
                modified_event['path'] = clean_path
            
            if 'rawPath' in modified_event:
                modified_event['rawPath'] = clean_path
                
            if 'requestContext' in modified_event:
                if 'path' in modified_event['requestContext']:
                    modified_event['requestContext']['path'] = clean_path
                
                if 'http' in modified_event['requestContext'] and 'path' in modified_event['requestContext']['http']:
                    modified_event['requestContext']['http']['path'] = clean_path
            
            logger.info(f"Using modified path: {clean_path}")
            response = handler(modified_event, context)
        else:
            logger.info(f"Using original path: {path}")
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
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }