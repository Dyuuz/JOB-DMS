from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .models import (
    CustomUser, CompanyProfile,
    UserProfile, Job, Application,
    Feedback, Document, Employment)
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth import login
from .forms import (
    CustomUserCreationForm,
    LoginForm,
    UserProfileForm,
    CompanyProfileForm,
    DocumentForm, ApplicationForm,
    JobForm, EmploymentForm)
from datetime import datetime
import requests
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .mixins import UserPermissionMixin, JobDetailPermissionMixin
from django.contrib.auth.decorators import login_required
from .utils import get_company_name, extract_site_name, get_time_countdown, get_download_url
import os


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


class JobsAvailableView(ListView):
    """
    This view handles the page to display jobs available for job seekers
    """
    model = Job
    context_object_name = 'jobs'
    template_name = 'JobsAvailable.html'

    def get_queryset(self):
        jobs = Job.objects.filter(is_public=True, status='Active').order_by('-created_at')
        return jobs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for job in context['jobs']:
            job.company_abbr = get_company_name(job.company.user.full_name)
            get_time = get_time_countdown(f"{job.created_at}")
            job.time = int(get_time)

        return context


class DashboardView(LoginRequiredMixin, ListView):
    """
    This view handles the page to display jobs available for job seekers
    """
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        name_list = get_company_name(user.full_name)
        job_list = Job.objects.filter(company__user=user).order_by('-created_at')
        active_jobs = len(Job.objects.filter(company__user=user, status='Active'))
        draft_jobs = len(Job.objects.filter(company__user=user, status='Draft'))
        applications = len(Application.objects.filter(job__company=user.companyprofile))
        interviews = len(Application.objects.filter(job__company=user.companyprofile, status='Interview'))


        for job in job_list:
            job.count = Application.objects.filter(job=job).count()

        return render(request, self.template_name, locals())


class ApplyJobView(CreateView):

    model = Application
    form_class = ApplicationForm
    template_name = 'apply_job.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('pk')  # Get from URL
        context['job'] = self.job
        return context

    def form_valid(self, form):
        app = form.save(commit=False)
        user = self.request.user
        app.user = user
        app.job = self.job

        # manually save contact info
        # app.full_name = user.full_name
        # app.phone = user.userprofile.phone
        # app.email = user.email

        app.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('jobs_applied')  # adjust to your success URL


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


class JobsAppliedView(ListView):
    """
    This view handles the page for jobs applied for n=by a job seeker
    """
    template_name = 'JobsApplied.html'

    def get(self, request, *args, **kwargs):
        applications = Application.objects.filter(user=request.user).order_by('-submitted_at')
        applied = len(Application.objects.filter(user=request.user, status='Applied'))
        interviews = len(Application.objects.filter(user=request.user, status='Interview'))
        offers = len(Application.objects.filter(user=request.user, status='Offer'))
        rejected = len(Application.objects.filter(user=request.user, status='Rejected'))

        return render(request, self.template_name, locals())

class JobFormView(UpdateView):
    """
    This view handles the page for jobs uploads by a company
    """
    template_name = 'JobForm.html'
    model = Job
    form_class = JobForm
    success_url = reverse_lazy('dashboard')

    # Override this method to get the object to be updated
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            try:
                # Try to get CompanyProfile if user is company
                if self.request.user.is_company():
                    pk = self.request.GET.get('update')
                    if pk:
                        return Job.objects.get(pk=pk)
                    else:
                        return None
                else:
                    reverse_lazy('jobs_available')
            except AttributeError:
                return self.form_invalid(self.form)
        return redirect('auth-login')

    # Override this method to pass the user to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_object'] = self.get_object()
        context['company'] = self.request.user.companyprofile
        return context

    # Override this method to handle form submission
    # and save the profile data
    def form_valid(self, form):
        form.instance.company = self.request.user.companyprofile

        obj = self.get_object()
        if obj is None:
            messages.success(self.request, f"Job successfully created")
        else:
            messages.success(self.request, f"Job successfully updated")

        return super().form_valid(form)

    # Override this method to handle form submission errors
    # and pass them to the template
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))


class JobDetailView(LoginRequiredMixin,JobDetailPermissionMixin, DetailView):
    model = Job
    template_name = 'jobdetails.html'
    context_object_name = 'job'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Job, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        get_time = get_time_countdown(f"{job.created_at}")
        job.time = int(get_time)
        job.count = Application.objects.filter(job=job).count()
        company_name = get_company_name(job.company.user.full_name)

        applied = True if self.request.user.role == 'user' and Application.objects.filter(job=job, user=self.request.user).first() else False

        context['job'] = job
        context['company_abbr'] = company_name
        context['applied'] = applied
        return context


class JobApplicantView(ListView):
    """
    This view handles the applicants page that applied to a job for companies
    It checks if the user is authenticated and retrieves their job information
    """
    template_name = 'JobApplicants_View.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth-login')

        pk = self.kwargs.get('pk')

        job = Job.objects.filter(pk=pk).first()

        if not job:
            messages.error(request, "Job not found.")
            return redirect('dashboard')

        applicants = Application.objects.filter(job=job)

        for applicant in applicants:
            applicant.element = applicant.status.lower()
            print(applicant.element)

        return render(request, self.template_name, {
            'applicants': applicants,
            'job_title': job.title,
            'job': job,
            'company_name': job.company.user,
            'company_abbr': get_company_name(job.company.user.full_name),
        })


class JobApplicantFormView(ListView):
    """

    """
    template_name = 'JobApplicants_Details.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth-login')

        pk = self.kwargs.get('pk')
        jd = self.kwargs.get('jd')

        # job = Job.objects.get(title=jd)

        userprofile = get_object_or_404(CustomUser, pk=pk)
        applicants = Application.objects.filter(job__pk=jd, user=userprofile).first()
        company_name = get_company_name(applicants.job.company.user.full_name)
        status = applicants.status.lower()

        return render(request, self.template_name, {
            'applicant': applicants,
            'job_title': applicants.job.title,
            'company_name': company_name,
            'status': status,
        })


class ApplicantProfileView(ListView):
    model = Job
    template_name = 'user_view.html'
    context_object_name = 'user_profile'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserProfile, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        experience = Employment.objects.filter(user=user_profile.user)
        ready_to_work = True if user_profile.ready_to_work == 'Available immediately' else False
        website_name = extract_site_name(user_profile.portfolio) if user_profile.portfolio else None

        context['user_profile'] = user_profile
        context['ready_to_work'] = ready_to_work
        context['experience'] = experience
        context['website_name'] = website_name
        return context


class ResumeView(ListView):
    """

    """
    template_name = 'Resume_View.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth-login')

        pk = self.kwargs.get('pk')
        document = Document.objects.filter(pk=pk).first()

        if not Document:
            messages.error(request, "Document not found.")
            return redirect('dashboard')

        return render(request, self.template_name, {
            'document': document,
        })


class DocumentUploadView(UserPermissionMixin, LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'DocumentUpload.html'
    success_url = reverse_lazy('documents')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Get unsaved instance
        instance = form.save(commit=False)
        instance.owner_user = self.request.user

        # Extract extension
        _, ext = os.path.splitext(instance.file.name)
        cleaned_ext = ext.lower().lstrip('.')

        valid_extensions = [choice[0] for choice in instance.FILE_FORMAT]

        if cleaned_ext in valid_extensions:
            instance.file_format = cleaned_ext
        else:
            form.add_error('file', f"Unsupported file format: .{cleaned_ext}")
            return self.form_invalid(form)

        # Save instance
        instance.save()
        messages.success(self.request, f"'{instance.name}' uploaded successfully!")

        # Set self.object so CBV knows the saved object
        self.object = instance

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
            response = requests.head(file.file.url)
            size = int(response.headers.get('Content-Length', 0))
            file.size = round(size / ( 1024 * 1024 ), 2)

            file.download_url = get_download_url(file.file.url, file.name)

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
                experience = Employment.objects.filter(user=request.user)

                if user_profile or company_role:
                    if company_role:
                        company_role.core_tech = company_role.core_tech.split(',') if company_role.core_tech else []
                        # company_role.awards = company_role.awards.split(',') if company_role.awards else []
                        company_role.certifications = company_role.certifications.split(',') if company_role.certifications else []
                        # employees =
                        website_name = extract_site_name(company_role.website) if company_role.website else None
                        return render(request, self.template_name,
                                {'company_role': company_role, 'user_auth': user_auth, 'website_name': website_name,})

                    elif user_profile:
                        # Provided a variable to avoid hardcoding strings
                        available_immediately = 'Available immediately'
                        ready_to_work = (user_profile.ready_to_work == available_immediately) if user_profile.ready_to_work else False
                        website_name = extract_site_name(user_profile.portfolio) if user_profile.portfolio else None
                        return render(request, self.template_name,
                            {'user_profile': user_profile, 'user_auth': user_auth, 'ready_to_work': ready_to_work, 'experience' : experience, 'website_name': website_name })

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

class EmploymentUpdateView(UpdateView):
    model = Employment
    form_class = EmploymentForm
    template_name = 'Employment.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            try:
                if self.request.user.is_user():
                    pk = self.request.GET.get('update')
                    if pk:
                        return Employment.objects.get(pk=pk)
                    else:
                        return None
                else:
                    reverse_lazy('profile')
            except AttributeError:
                return self.form_invalid(self.form)
        return redirect('auth-login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employment_object'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        obj = self.get_object()
        if obj is None:
            messages.success(self.request, f"'{obj.company_name}' successfully updated!")
        else:
            messages.success(self.request, f"Successfully created!")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
