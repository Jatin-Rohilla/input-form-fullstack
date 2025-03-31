from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import FormSubmission
from .serializers import FormSubmissionSerializer

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class FormSubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing form submissions"""
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new form submission"""
        # Log the raw request data for debugging
        try:
            if isinstance(request.data, dict):
                raw_data = request.data
            else:
                raw_data = json.loads(request.body.decode('utf-8')) if request.body else {}
            logger.info(f"Request data: {raw_data}")
        except Exception as e:
            logger.error(f"Error parsing request data: {str(e)}")
            
        logger.info(f"Request headers: {request.headers}")
            
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            # Log and return validation errors
            logger.error(f"Validation errors: {serializer.errors}")
            response = Response(
                {"detail": "Validation error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            # Add CORS headers
            response["Access-Control-Allow-Origin"] = "https://input-form-fullstack.vercel.app"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Allow-Credentials"] = "true"
            return response
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Add CORS headers explicitly
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response["Access-Control-Allow-Origin"] = "https://input-form-fullstack.vercel.app"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        
        return response
    
    def list(self, request, *args, **kwargs):
        """List all form submissions"""
        response = super().list(request, *args, **kwargs)
        
        # Add CORS headers explicitly
        response["Access-Control-Allow-Origin"] = "https://input-form-fullstack.vercel.app"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        
        return response
    
    def options(self, request, *args, **kwargs):
        """Handle preflight OPTIONS requests"""
        response = Response()
        response["Access-Control-Allow-Origin"] = "https://input-form-fullstack.vercel.app"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Max-Age"] = "86400"  # 24 hours
        
        return response 