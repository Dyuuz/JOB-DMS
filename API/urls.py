from django.urls import path
from API.views import (
    DocumentDeleteAPIView,
    JobStatusAPIView,
)

urlpatterns = [
    path('document/<int:id>/delete/', DocumentDeleteAPIView.as_view(), name='document_delete_api'),
    path('job/<int:id>/status/', JobStatusAPIView.as_view(), name='job_status_api'),
]
