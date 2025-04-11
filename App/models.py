from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model with roles for job seekers and companies
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Jobholder'),
        ('company', 'Company'),
    )
    full_name =  models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_company(self):
        return self.role == 'company'

    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.full_name

# Company profile model for additional company details
class CompanyProfile(models.Model):
    COUNTRY = (
        ('Nigeria', 'Nigeria'),
        ('Ghana', 'Ghana'),
        ('Kenya', 'Kenya'),
        ('South Africa', 'South Africa'),
    )
    WORK_MODE = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On site', 'On Site'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_id = models.CharField(max_length=255, blank=True, null=True)
    work_mode = models.TextField(choices=WORK_MODE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=255, choices=COUNTRY, blank=True)

    def __str__(self):
        return self.user.full_name

# User profile model for job seekers' additional information
class UserProfile(models.Model):
    EMPLOYMENT_TYPE = (
        ('Internship', 'Internship'),
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
        ('Contract', 'Contract'),
    )
    EDUCATION_LEVEL = (
        ('High School', 'High School'),
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Master's Degree", "Master's Degree"),
        ('PhD', 'PhD'),
    )
    START_DATE_READY = (
        ('Available immediately', 'Available immediately'),
        ('Requires notice period', 'Requires notice period'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    DOB = models.DateField(null=True, blank=True)
    user_country = models.CharField(max_length=255, blank=True)

    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    job_description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, blank=True)
    job_location = models.CharField(max_length=255, blank=True)

    highest_education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL, blank=True)
    work_field = models.CharField(max_length=100, blank=True)
    work_experience = models.IntegerField(null=True, blank=True)
    project = models.CharField(max_length=100, blank=True)
    resume = models.FileField(upload_to='media/', blank=True, null=True)
    ready_to_work = models.CharField(max_length=50, choices=START_DATE_READY, blank=True)

    bio = models.TextField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.full_name

# Job model for storing job listings posted by companies
class Job(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    deadline = models.DateField()
    is_public = models.BooleanField(default=False)  # Visibility control

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.user.full_name}"

# Application model for job applications submitted by job seekers
class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')  # Link to CustomUser
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, default='pending')
    resume_version = models.FileField(upload_to='resume_versions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.job.title}"

# Document model for storing documents uploaded by users and companies
class Document(models.Model):
    owner_user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='documents')
    owner_company = models.ForeignKey(CompanyProfile, null=True, blank=True, on_delete=models.CASCADE, related_name='documents')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='documents')  # Linked to Job model
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Feedback model for company feedback on applications
class Feedback(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='feedbacks')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.application.user.full_name}"
