from rest_framework import serializers
from .models import FormSubmission

class FormSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for form submissions"""
    class Meta:
        model = FormSubmission
        fields = ('id', 'name', 'email', 'country_code', 'phone_number', 'message', 'created_at')
        read_only_fields = ('id', 'created_at') 