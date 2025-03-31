from rest_framework import serializers
import logging
from .models import FormSubmission

logger = logging.getLogger(__name__)

class FormSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for form submissions"""
    class Meta:
        model = FormSubmission
        fields = ('id', 'name', 'email', 'country_code', 'phone_number', 'message', 'created_at')
        read_only_fields = ('id', 'created_at')
        
    def validate(self, data):
        """Custom validation for the form submission"""
        # Log the raw data for debugging
        logger.info(f"Validating form submission data: {data}")
        
        # Validate that all required fields are present
        required_fields = ['name', 'email', 'country_code', 'phone_number', 'message']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                raise serializers.ValidationError({field: f"This field is required."})
                
        return data
    
    def is_valid(self, raise_exception=False):
        """Override to add additional logging"""
        logger.info(f"Raw data received: {self.initial_data}")
        try:
            return super().is_valid(raise_exception=raise_exception)
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {e.detail}")
            raise 