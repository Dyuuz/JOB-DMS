from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from App.views import HomeView, JobsAvailableView, JobsAppliedView, DocumentView, ProfileView, SettingsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('jobs-available', JobsAvailableView.as_view(), name='jobs_available'),
    path('jobs-applied', JobsAppliedView.as_view(), name='jobs_applied'),
    path('documents', DocumentView.as_view(), name='documents'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('settings', SettingsView.as_view(), name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
