from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .models import CustomUser, CompanyProfile, UserProfile, Company, Job, Application, Feedback
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import login
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
class HomeView(View):
    template_name = 'layout.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class JobsAvailableView(View):
    template_name = 'JobsAvailable.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class JobsAppliedView(View):
    template_name = 'JobsApplied.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class DocumentView(View):
    template_name = 'Documents.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class ProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'Profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Return the profile for the currently logged-in user
        if self.request.user.is_authenticated:
            try:
                return UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                return None
        return redirect('auth-login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_role'] = self.request.user.is_company() if self.request.user.is_authenticated else False
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure the profile is linked
        return super().form_valid(form)

class SettingsView(View):
    template_name = 'Settings.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('auth-login')  # Redirect to the login page after logout

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'loginReg.html'
    success_url = reverse_lazy('auth-login')  # Redirect to login page after successful signup

    def form_valid(self, form):
        # Check if a user with the same email already exists
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
