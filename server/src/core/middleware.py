import logging

logger = logging.getLogger(__name__)

class CORSDebugMiddleware:
    """
    Middleware to log CORS-related information for debugging.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Log incoming request headers related to CORS
        logger.info(f"Incoming request from origin: {request.headers.get('Origin', 'No origin')}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request path: {request.path}")
        
        # Process request and get response
        response = self.get_response(request)
        
        # Log outgoing response headers related to CORS
        cors_headers = {
            'Access-Control-Allow-Origin': response.get('Access-Control-Allow-Origin', 'Not set'),
            'Access-Control-Allow-Methods': response.get('Access-Control-Allow-Methods', 'Not set'),
            'Access-Control-Allow-Headers': response.get('Access-Control-Allow-Headers', 'Not set'),
            'Access-Control-Allow-Credentials': response.get('Access-Control-Allow-Credentials', 'Not set'),
        }
        logger.info(f"CORS response headers: {cors_headers}")
        
        return response 