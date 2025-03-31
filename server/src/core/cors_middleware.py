class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Get the request origin
        origin = request.headers.get('Origin', '')
        
        # List of allowed origins
        allowed_origins = [
            "https://property-station-frontend.onrender.com",
            "http://ec2-16-170-204-147.eu-north-1.compute.amazonaws.com",
            "http://localhost:5173",
            "http://localhost:3000",
            "https://input-form-fullstack.vercel.app"
        ]
        
        # Set CORS headers if origin is allowed
        if origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
            response["Access-Control-Allow-Credentials"] = "true"
        
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            response.status_code = 200
            return response
            
        return response 