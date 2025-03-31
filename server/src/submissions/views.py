from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import FormSubmission
from .serializers import FormSubmissionSerializer

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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 