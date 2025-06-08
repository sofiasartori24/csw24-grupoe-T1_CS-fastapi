import os
import sys
import json
import time
import logging
import traceback
from typing import Dict, Any, Optional
import pymysql
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError
from mangum import Mangum
from app.main import app

# Configure logging
logger = logging.getLogger("lambda_handler")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

# Maximum number of connection retries - aligned with database.py
MAX_RETRIES = 5
# Delay between retries (in seconds) - aligned with database.py
RETRY_DELAY = 1

def format_error_response(status_code: int, message: str, request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Format a standardized error response.
    
    Args:
        status_code: HTTP status code
        message: Error message
        request_id: AWS request ID for tracking
        
    Returns:
        Formatted error response dictionary
    """
    error_response = {
        "statusCode": status_code,
        "body": json.dumps({
            "error": {
                "message": message,
                "status_code": status_code
            }
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    
    if request_id:
        error_response["body"] = json.dumps({
            "error": {
                "message": message,
                "status_code": status_code,
                "request_id": request_id
            }
        })
    
    return error_response

# Create a handler for AWS Lambda with lifespan="off" to avoid initialization issues
handler = Mangum(app, lifespan="off")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function with improved error handling and database resilience.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        Response dictionary
    """
    request_id = context.aws_request_id if hasattr(context, 'aws_request_id') else None
    
    # Log the full event for debugging
    logger.debug(f"Full event: {json.dumps(event)}")
    
    # Extract path and method with more robust fallbacks for different API Gateway versions
    path = event.get('path', event.get('rawPath', event.get('requestContext', {}).get('path', 'UNKNOWN')))
    method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method',
                      event.get('requestContext', {}).get('httpMethod', 'UNKNOWN')))
    
    logger.info(f"Request received: {method} {path} (Request ID: {request_id})")
    
    # Log environment variables for debugging
    logger.debug("Environment variables:")
    for key, value in os.environ.items():
        if key.startswith('DB_'):
            # Mask sensitive information
            logger.debug(f"  {key}: {'*' * len(value)}")
        else:
            logger.debug(f"  {key}: {value}")
    
    # Special handling for health check endpoint to avoid database access
    if path == '/health' or path.endswith('/health'):
        logger.info("Handling health check endpoint")
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "healthy"}),
            "headers": {"Content-Type": "application/json"}
        }
    
    # Special handling for root endpoint
    if path == '/' or path == '' or path.endswith('/Prod') or path == '/Prod' or path == '/Prod/':
        logger.info("Handling root endpoint")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Hello, World!"}),
            "headers": {"Content-Type": "application/json"}
        }
    
    # Special handling for db-status endpoint
    if path == '/db-status' or path.endswith('/db-status'):
        logger.info("Handling db-status endpoint")
        try:
            # Import necessary modules
            from app.database import get_db_with_retry
            from sqlalchemy import text
            
            # Get a database connection
            db = get_db_with_retry()
            
            try:
                # Execute a simple query to test the connection
                result = db.execute(text("SELECT 1")).scalar()
                
                # Return success response
                return {
                    "statusCode": 200,
                    "body": json.dumps({"status": "connected", "result": result}),
                    "headers": {"Content-Type": "application/json"}
                }
            except Exception as e:
                logger.error(f"Database status check failed: {str(e)}")
                
                # Return error response
                return {
                    "statusCode": 500,
                    "body": json.dumps({"status": "disconnected", "error": str(e)}),
                    "headers": {"Content-Type": "application/json"}
                }
            finally:
                # Close the database connection
                db.close()
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            
            # Return error response
            return {
                "statusCode": 500,
                "body": json.dumps({"status": "disconnected", "error": str(e)}),
                "headers": {"Content-Type": "application/json"}
            }
    
    try:
        # Execute the handler with retry capability for database operations
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Executing handler (attempt {attempt+1}/{MAX_RETRIES})... (Request ID: {request_id})")
                return handler(event, context)
            except (OperationalError, DatabaseError, pymysql.OperationalError) as e:
                if attempt < MAX_RETRIES - 1:
                    # Calculate wait time with exponential backoff and some jitter
                    base_wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    jitter = base_wait_time * 0.2 * (0.5 - time.time() % 0.5)  # Add up to 20% jitter
                    wait_time = base_wait_time + jitter
                    
                    # Log detailed error information
                    db_host = os.environ.get("DB_HOST", "unknown")
                    db_name = os.environ.get("DB_NAME", "unknown")
                    
                    logger.warning(
                        f"Database operation failed (attempt {attempt+1}/{MAX_RETRIES}): {str(e)}. "
                        f"Host: {db_host}, Database: {db_name}. "
                        f"Retrying in {wait_time:.2f} seconds... (Request ID: {request_id})"
                    )
                    time.sleep(wait_time)
                else:
                    # Last attempt failed, re-raise the exception
                    logger.error(
                        f"All database connection retries ({MAX_RETRIES}) failed. "
                        f"Last error: {str(e)}. (Request ID: {request_id})"
                    )
                    raise
        
    except SQLAlchemyError as e:
        error_msg = f"Database error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}\n(Request ID: {request_id})")
        
        # Include more specific error message for the client
        db_host = os.environ.get("DB_HOST", "unknown")
        error_details = f"Database error with host {db_host}. Request ID: {request_id}"
        return format_error_response(500, error_details, request_id)
        
    except pymysql.Error as e:
        error_msg = f"MySQL error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}\n(Request ID: {request_id})")
        
        # Include more specific error message for the client
        db_host = os.environ.get("DB_HOST", "unknown")
        error_details = f"Database connection error with host {db_host}. Request ID: {request_id}"
        return format_error_response(500, error_details, request_id)
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}\n(Request ID: {request_id})")
        return format_error_response(500, "An unexpected error occurred", request_id)