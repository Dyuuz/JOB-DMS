from django.http import HttpResponseForbidden

class UserPermissionMixin:
    """
    Mixin to restrict access ONLY to users with a UserProfile (job seekers).
    Denies access to:
    - Anonymous users
    - Users with CompanyProfile
    - Users with no profile at all
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this page.")

        if hasattr(request.user, 'companyprofile'):
            return HttpResponseForbidden("This page is only available to job seekers, not companies.")

        if not hasattr(request.user, 'userprofile'):
            return HttpResponseForbidden("This page is only available to job seekers, not companies.")

        return super().dispatch(request, *args, **kwargs)

class JobDetailPermissionMixin:

    def dispatch(self, request, *args, **kwargs):
        job = self.get_object()
        user = request.user

        # Allow access if job is public or user is the poster
        if job.is_public:
            return super().dispatch(request, *args, **kwargs)

        if job.company.user == request.user:
            return super().dispatch(request, *args, **kwargs)

        # Otherwise, redirect or raise 403
        return self.handle_no_permission()

    def handle_no_permission(self):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You do not have permission to view this job.")
