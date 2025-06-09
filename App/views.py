from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .models import (
    CustomUser, CompanyProfile,
    UserProfile, Job, Application,
    Feedback, Document)
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth import login
from .forms import (
    CustomUserCreationForm,
    LoginForm,
    UserProfileForm,
    CompanyProfileForm,
    DocumentForm)
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .mixins import UserPermissionMixin
from .utils import get_company_name

# Create your views here.
class HomeView(View):
    """
    This view handles the landing page for anyone without requiring user authentication
    """
    template_name = 'layout.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        user_profile = UserProfile.objects.filter(user=request.user).first()
        company_role = CompanyProfile.objects.filter(user=request.user).first()
        return render(request, self.template_name,
        {
            'company_role': company_role,
            'user_profile': user_profile,
        })

class JobsAvailableView(View):
    """
    This view handles the page to display jobs available for job seekers
    """
    template_name = 'JobsAvailable.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class DashboardView(View):
    """
    This view handles the page to display jobs available for job seekers
    """
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        name_list = get_company_name(user.full_name)
        return render(request, self.template_name,
        {
            'user': user,
            'company_name': name_list,
        })

class WorkforceView(View):
    """
    This view handles the page to display jobs available for job seekers
    """
    template_name = 'workforce.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        name_list = get_company_name(user.full_name)
        return render(request, self.template_name,
        {
            'user': user,
            'company_name': name_list,
        })

class WorkSpaceView(View):
    """
    This view handles the page to display companies a user is working it, most importantly provided by the platform
    """
    template_name = 'WorkSpace.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class JobsAppliedView(View):
    """
    This view handles the page for jobs applied for n=by a job seeker
    """
    template_name = 'JobsApplied.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class DocumentUploadView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'DocumentUpload.html'
    success_url = reverse_lazy('documents')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Set the owner before saving
        instance = form.save(commit=False)
        instance.owner_user = self.request.user

        # if hasattr(self.request.user, 'companyprofile'):
        #     instance.owner_company = self.request.user.companyprofile
        # else:
        #     instance.owner_user = self.request.user

        instance.save()
        messages.success(self.request, f"'{instance.owner_user}' uploaded successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class DocumentListView(UserPermissionMixin, View):
    """
    This view handles the document page for both job seekers and companies
    It checks if the user is authenticated and retrieves their document information
    """
    template_name = 'Documents.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth-login')

        user_documents = Document.objects.filter(owner_user=request.user)

        for file in user_documents:
            file.size = round(file.file.size / ( 1024 * 1024 ), 2)
        return render(request, self.template_name, {
            'user_documents': user_documents,
            'has_documents': user_documents.exists()
        })


# class DocumentDeleteView(LoginRequiredMixin, DeleteView):
#     model = Document
#     template_name = 'documents/confirm_delete.html'
#     success_url = reverse_lazy('documents:list')

#     def get_object(self, queryset=None):
#         obj = get_object_or_404(Document, pk=self.kwargs['pk'])
#         # Verify ownership
#         if hasattr(self.request.user, 'companyprofile'):
#             if obj.owner_company != self.request.user.companyprofile:
#                 raise PermissionDenied
#         else:
#             if obj.owner_user != self.request.user:
#                 raise PermissionDenied
#         return obj

#     def delete(self, request, *args, **kwargs):
#         response = super().delete(request, *args, **kwargs)
#         messages.success(request, "Document deleted successfully!")
#         return response


class UserProfileUpdateView(UpdateView):
    """
    This view handles the profile update for both job seekers and companies
    It checks if the user is authenticated and retrieves their profile information
    which is then passed to the form for updating
    It uses a custom form to handle the profile update
    It redirects to the profile page after successful update
    """
    model = UserProfile
    template_name = 'ProfileUpdate.html'
    success_url = reverse_lazy('profile')

    # Override this method to get the object to be updated
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            try:
                # Try to get CompanyProfile if user is company
                if hasattr(self.request.user, 'role') and self.request.user.role == 'company':
                    if CompanyProfile.objects.filter(user=self.request.user).exists():
                        return self.request.user.companyprofile
                    return None
                # Otherwise get UserProfile
                if hasattr(self.request.user, 'role') and self.request.user.role == 'user':
                    if UserProfile.objects.filter(user=self.request.user).exists():
                        return self.request.user.userprofile
                    return None
            except AttributeError:
                return self.form_invalid(self.form)
        return redirect('auth-login')

    # Override this method to pass the user to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_role'] = self.request.user.is_company() if self.request.user.is_authenticated else False
        context['user_profile'] = self.request.user.is_user() if self.request.user.is_authenticated else False
        return context

    # Override this method to pass the user to the form.py
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass user to form
        return kwargs

    # Override this method to determine which form to use based on user role
    # This assumes I have defined a UserProfileForm and CompanyProfileForm forms.py
    def get_form_class(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'role'):
                if self.request.user.role == 'user':
                    return UserProfileForm
                return CompanyProfileForm
        return super().get_form_class()

    # Override this method to handle form submission
    # and save the profile data
    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure the profile is linked
        messages.success(self.request, f"Your profile has been updated.")
        return super().form_valid(form)

    # Override this method to handle form submission errors
    # and pass them to the template
    def form_invalid(self, form):
        # Pass form errors to the template
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))

class ProfileView(View):
    """
    This view handles the profile page for both job seekers and companies
    # It checks if the user is authenticated and retrieves their profile information
    """
    template_name = 'Profile.html'

    def get(self,  request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_auth = CustomUser.objects.get(email=request.user.email)
                user_profile = UserProfile.objects.filter(user=request.user).first()
                company_role = CompanyProfile.objects.filter(user=request.user).first()

                if user_profile or company_role:
                    if company_role:
                        return render(request, self.template_name, {'company_role': company_role, 'user_auth': user_auth,})

                    elif user_profile:
                        # Provided a variable to avoid hardcoding strings
                        available_immediately = 'Available immediately'
                        ready_to_work = (user_profile.ready_to_work == available_immediately) if user_profile.ready_to_work else False
                        return render(request, self.template_name, {'user_profile': user_profile, 'user_auth': user_auth, 'ready_to_work': ready_to_work,})

                return redirect('profile-update')
            except UserProfile.DoesNotExist:
                return HttpResponse("User profile does not exist.")

class SettingsView(View):
    """
    This view handles the settings page for both job seekers and companies
    """
    template_name = 'Settings.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class LogoutView(View):
    """
    This view handles user logout
    It logs out the user and redirects to the login page
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('auth-login')  # Redirect to the login page after logout

class RegisterView(FormView):
    """
    This view handles user registration
    It uses a custom user creation form to register users
    It checks if a user with the same email already exists
    and adds an error if so
    It redirects to the login page after successful signup
    """
    form_class = CustomUserCreationForm
    template_name = 'loginReg.html'
    success_url = reverse_lazy('auth-login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        user = form.save()
        # login(self.request, user)  # Log in the user

        # Set a temporary message for a successful login
        messages.success(self.request, f"You can now proceed to login")

        return super().form_valid(form)

    def form_invalid(self, form):
        # Pass form errors to the template
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))

class LoginView(FormView):
    """
    This view handles user login
    It uses a custom login form to authenticate usersx
    It redirects to the home page after successful login
    """
    form_class = LoginForm
    template_name = 'Login.html'
    success_url = reverse_lazy('home')  # Redirect to home page after successful login

    def form_valid(self, form):
        # Log in the user
        login(self.request, form.get_user(), backend='App.backends.EmailAuthBackend')

        # Get user's first name
        first_name = form.get_user().full_name.split()[0]

        # Set a temporary message for a successful login
        messages.success(self.request, f"Welcome back, {first_name}!")

        return super().form_valid(form)

    def form_invalid(self, form):
        # Pass form errors to the template
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))

    # def get(self):
    #     if self.request.user.is_authenticated:
    #         redirect('home')
