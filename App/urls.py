from django import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from App.views import (
    HomeView, JobsAvailableView,
    DocumentUploadView,JobsAppliedView,
    DocumentListView, ProfileView,
    SettingsView, LogoutView,
    RegisterView, LoginView,
    UserProfileUpdateView,
    WorkSpaceView, DashboardView,
    WorkforceView, JobDetailView, ApplyJobView,
    JobApplicantView, JobApplicantFormView,ResumeView,
    ApplicantProfileView, JobFormView, EmploymentUpdateView)
from .utils import suggest_cover_letter
from django.urls import include

auth_patterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('logout', LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('workforce', WorkforceView.as_view(), name='workforce'),
    path('job-details/<int:pk>', JobDetailView.as_view(), name='job_details'),
    path('jobs-available', JobsAvailableView.as_view(), name='jobs_available'),
    path('jobs-applied', JobsAppliedView.as_view(), name='jobs_applied'),
    path('job-form', JobFormView.as_view(), name='job_form'),
    path('applicant-profile/<int:pk>', ApplicantProfileView.as_view(), name='applicant_profile'),
    path('resume/<int:pk>/view', ResumeView.as_view(), name='view_resume'),
    path('jobs-applicants/<int:pk>/view', JobApplicantView.as_view(), name='jobs_applicants_view'),
    path('jobs-applicant/<int:jd><int:pk>/form', JobApplicantFormView.as_view(), name='jobs_applicant_form'),
    path('apply/<int:pk>', ApplyJobView.as_view(), name='apply_for_job'),
    path('suggest-cover-letter/', suggest_cover_letter, name='suggest_cover_letter'),
    path('documents', DocumentListView.as_view(), name='documents'),
    path('documents/upload', DocumentUploadView.as_view(), name='document-upload'),
    path('profile/update', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('workspace', WorkSpaceView.as_view(), name='workspace'),
    path('job-experience', EmploymentUpdateView.as_view(), name='employment'),
    path('', include(auth_patterns)),
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
