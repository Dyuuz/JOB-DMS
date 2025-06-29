# views.py
from rest_framework.generics import (
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib import messages
from .serializer import ApplicationSerializer, TeamMgtSerializer
from App.models import Document,Job, Application, CompanyProfile, UserProfile, TeamManagement


class DocumentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def verify_member(self, obj):
        # Verify ownership
        if hasattr(self.request.user, 'companyprofile'):
            if obj.owner_company != self.request.user.companyprofile:
                return False
        else:
            if obj.owner_user != self.request.user:
                return False
        return True

    def delete(self, request, id):
        try:
            document = Document.objects.get(id=id)
            verify = self.verify_member(document)

            if verify:
                document.delete()
                return Response({'success': 'Document deleted'}, status=status.HTTP_204_NO_CONTENT)

            messages.success(request, "Document deleted successfully!")
            return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': f"Error string: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class JobStatusAPIView(UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        status_data = request.data.get("status")
        # print(f"Status data received: {status_data}")
        # print(instance.status)
        if instance.status == "Offer":
            return Response(
                {"error": "Cannot change status after it's set to '{instance.status}'."},
                status=status.HTTP_403_FORBIDDEN
            )

        elif instance.status == "Rejected":
            return Response(
                {"error": f"Cannot change status after it's set to '{instance.status}'."},
                status=status.HTTP_403_FORBIDDEN
            )

        elif instance.status == "Interview" and status_data == "Applied":
            return Response(
                {"error": f"Cannot change status to {status_data} after it's set to {instance.status}."},
                status=status.HTTP_403_FORBIDDEN
            )

        response = super().patch(request, *args, **kwargs)

        instance.refresh_from_db()

        # Conditional logic after patching
        if instance.status == "Rejected":
            instance.next_step = "N/A"
            instance.save()

        elif instance.status == "Interview":
            instance.next_step = "Technical Interview"
            instance.save()

        elif instance.status == "Applied":
            instance.next_step = "Awaiting Response"
            instance.save()

        elif instance.status == "Offer":
            instance.next_step = "Welcome aboard"
            instance.save()

        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Application status updated",
            "next_step": instance.next_step,
            "data": response.data
        }, status=response.status_code)
