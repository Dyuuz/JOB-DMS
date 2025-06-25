# views.py
from rest_framework.generics import (
    DestroyAPIView,
)
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib import messages
from App.models import Document

class DocumentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def verify_member(self, obj):
        # Verify ownership
        if hasattr(self.request.user, 'companyprofile'):
            if obj.owner_company != self.request.user.companyprofile:
                raise PermissionDenied
        else:
            if obj.owner_user != self.request.user:
                raise PermissionDenied
        return True

    def delete(self, request, id):
        try:
            document = Document.objects.get(id=id)
            verify = self.verify_member(document)
            print(verify)

            if verify:
                document.delete()
                return Response({'success': 'Document deleted'}, status=status.HTTP_204_NO_CONTENT)

            messages.success(request, "Document deleted successfully!")
            return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': f"Error {e}"}, status=status.HTTP_400_BAD_REQUEST)
