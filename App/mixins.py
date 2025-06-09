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
            return HttpResponseForbidden("Please complete your job seeker profile to access this page.")

        return super().dispatch(request, *args, **kwargs)
