from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import FormSubmission
from .serializers import FormSubmissionSerializer

@method_decorator(csrf_exempt, name='dispatch')
class FormSubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing form submissions"""
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new form submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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