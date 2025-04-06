from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .models import CustomUser, CompanyProfile, UserProfile, Company, Job, Application, Feedback
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login


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

class ProfileView(View):
    template_name = 'Profile.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

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
    template_name = 'loginReg.html'  # Replace with your template path
    success_url = reverse_lazy('auth-login')  # Redirect to login page after successful signup

    def form_valid(self, form):
        # Check if a user with the same email already exists
        email = form.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        user = form.save()
        login(self.request, user)  # Log in the user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Pass form errors to the template
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))

class LoginView(View):
    template_name = 'Login.html'  # Replace with your login template path

    def get(self, request, *args, **kwargs):
        # Render the login form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle login logic
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            # Invalid credentials, pass error to the template
            return render(request, self.template_name, {'error': 'Invalid username or password'})
