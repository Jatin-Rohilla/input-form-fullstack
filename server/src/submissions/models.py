from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class FormSubmission(models.Model):
    """Model for storing form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    country_code = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\+\d{1,4}$', message='Country code must start with + followed by 1-4 digits')]
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\d{7,15}$', message='Phone number must be between 7 and 15 digits')]
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.email})"
        
    def clean(self):
        """Validate the model data"""
        # Ensure country code starts with +
        if self.country_code and not self.country_code.startswith('+'):
            self.country_code = f"+{self.country_code}" 