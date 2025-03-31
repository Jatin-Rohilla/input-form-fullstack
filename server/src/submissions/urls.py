from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormSubmissionViewSet

router = DefaultRouter()
router.register(r'submissions', FormSubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 