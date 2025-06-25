from django.urls import path
from API.views import (
    DocumentDeleteAPIView,
)

urlpatterns = [
    path('document/<int:id>/delete/', DocumentDeleteAPIView.as_view(), name='document_delete_api'),
]
