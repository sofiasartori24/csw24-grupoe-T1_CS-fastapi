import json
import logging
import sys
import os

# Configure logging
logger = logging.getLogger("simple_lambda_handler")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

def handler(event, context):
    """
    Simple AWS Lambda handler function for testing API Gateway integration.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        Response dictionary
    """
    try:
        # Log environment variables
        logger.debug("Environment variables:")
        for key, value in os.environ.items():
            logger.debug(f"  {key}: {value}")
        
        # Log the incoming request with full details
        logger.debug(f"Event: {json.dumps(event)}")
        logger.debug(f"Context: {context}")
        
        # Extract path and method with fallbacks
        path = event.get('path', event.get('rawPath', '/'))
        method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'GET'))
        
        logger.info(f"Request received: {method} {path}")
        
        # Special handling for health check endpoint
        if path == '/health' or path.endswith('/health'):
            logger.info("Handling health check endpoint")
            return {
                "statusCode": 200,
                "body": json.dumps({"status": "healthy"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        # Handle root endpoint
        if path == '/' or path == '' or path.endswith('/Prod'):
            logger.info("Handling root endpoint")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Hello, World!"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        # Log that we're returning a 404
        logger.info(f"No handler for path {path}, returning 404")
        
        # Handle any other endpoint
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Not Found", "path": path}),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        # Log any exceptions
        logger.error(f"Error handling request: {str(e)}", exc_info=True)
        
        # Return a 500 error
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }