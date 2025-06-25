# views.py
from rest_framework.generics import (
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from App.models import Document

class DocumentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            document = Document.objects.get(id=id)
            document.delete()
            return Response({'success': 'Document deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
