from django.db import models
from cloudinary.models import CloudinaryField
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
        return self.role == 'company' and hasattr(self, 'companyprofile')

    def is_user(self):
        return self.role == 'user' and hasattr(self, 'userprofile')

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
    INDUSTRY = (
        ('FinTech', 'FinTech'),
        ('HealthTech', 'HealthTech'),
        ('EdTech', 'EdTech'),
        ('E-commerce', 'E-commerce'),
        ('Agritech', 'Agritech'),
        ('Logistics', 'Logistics'),
        ('Real Estate', 'Real Estate'),
        ('Telecommunications', 'Telecommunications'),
        ('Entertainment', 'Entertainment'),
        ('Travel and Tourism', 'Travel and Tourism'),
        ('Manufacturing', 'Manufacturing'),
        ('Energy', 'Energy'),
        ('Retail', 'Retail'),
        ('Media', 'Media'),
        ('Construction', 'Construction'),
        ('Consulting', 'Consulting'),
        ('Information Technology', 'Information Technology'),
        ('Food and Beverage', 'Food and Beverage'),
        ('Transportation', 'Transportation'),
        ('Non-profit', 'Non-profit'),
        ('Government', 'Government'),
        ('Fashion', 'Fashion'),
        ('Other', 'Other'),  # Add an option for other industries

    )
    WORK_MODE = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On site', 'On Site'),
    )
    STATUS = (
        ('Hiring', 'Hiring'),
        ('Applications Closed', 'Applications Closed'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hire_status = models.CharField(max_length=100,choices=STATUS, default='Hiring')
    company_reg_num = models.CharField(max_length=255,unique=True, blank=True, null=True)
    work_mode = models.CharField(max_length=255,choices=WORK_MODE, blank=True, null=True)
    founded = models.DateField(null=True, blank=True)
    parent_company = models.CharField(max_length=255, blank=True, null=True)
    headquarters = models.CharField(max_length=255, blank=True, null=True)
    annual_growth_rate = models.IntegerField(null=True, blank=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    tagline= models.CharField(max_length=255, blank=True, null=True)

    about_us = models.TextField(blank=True, null=True)
    mission_statement = models.TextField(blank=True, null=True)
    core_tech = models.TextField(help_text="Enter tech tools seperated by commas",blank=True, null=True)
    awards = models.TextField(help_text="Enter awards seperated by commas",blank=True, null=True)
    certifications = models.TextField(help_text="Enter awards seperated by commas",blank=True, null=True)

    industry = models.CharField(max_length=100,choices=INDUSTRY, blank=True)
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
    WORK_MODE = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On site', 'On Site'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(unique=True, max_length=20, blank=True)
    DOB = models.DateField(null=True, blank=True)
    user_country = models.CharField(max_length=255, blank=True)

    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    job_description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, blank=True)
    work_mode = models.CharField(max_length=20, choices=WORK_MODE)
    job_location = models.CharField(max_length=255, blank=True)

    highest_education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL, blank=True)
    work_field = models.CharField(max_length=100, blank=True)
    work_experience = models.IntegerField(null=True, blank=True)
    project = models.CharField(max_length=100, blank=True)
    ready_to_work = models.CharField(max_length=50, choices=START_DATE_READY, blank=True)

    bio = models.TextField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.full_name

class Employment(models.Model):
    EMPLOYMENT_TYPE = (
        ('Internship', 'Internship'),
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
        ('Contract', 'Contract'),
    )
    WORK_MODE = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On site', 'On Site'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='experience')
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=50)
    job_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE)
    work_mode = models.CharField(max_length=20, choices=WORK_MODE)
    job_location = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name


# Job model for storing job listings posted by companies
class Job(models.Model):
    EMPLOYMENT_TYPE = (
        ('Internship', 'Internship'),
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
        ('Contract', 'Contract'),
    )
    EXPERIENCE_LEVEL= (
        ('Entry Level', 'Entry Level'),
        ('Mid Level', 'Mid Level'),
        ('Senior Level', 'Senior Level'),
        ('Expert', 'Expert'),
    )
    WORK_MODE = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On site', 'On Site'),
    )
    CURRENCY = (
        ('NGN', 'NGN'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    STATUS = (
        ('Active', 'Active'),
        ('Draft', 'Draft'),
        ('Closed', 'Closed'),
    )
    DERPARTMENT = (
        ('Engineering', 'Engineering'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Human Resources', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Customer Support', 'Customer Support'),

        ('Design', 'Design'),
        ('Product Management', 'Product Management'),
        ('Operations', 'Operations'),

        ('Data Science', 'Data Science'),
        ('Content Creation', 'Content Creation'),
        ('Research and Development', 'Research and Development'),
        ('Quality Assurance', 'Quality Assurance'),

        ('Administration', 'Administration'),

        ('Business Development', 'Business Development'),
        ('Information Technology', 'Information Technology'),
        ('Project Management', 'Project Management'),

        ('Supply Chain Management', 'Supply Chain Management'),

        ('Public Relations', 'Public Relations'),
        ('Consulting', 'Consulting'),

        ('Other', 'Other'),
    )
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    department = models.CharField(max_length=255, choices=DERPARTMENT, default='Engineering')
    location = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=255, choices=EMPLOYMENT_TYPE, default='Full Time')
    min_salary = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    experience_level = models.CharField(max_length=50,choices=EXPERIENCE_LEVEL, default='Senior Level')
    currency = models.CharField(max_length=10,choices=CURRENCY, default='NGN')
    work_mode = models.CharField(max_length=255, choices=WORK_MODE, default='Remote')
    deadline = models.DateField()
    status = models.CharField(max_length=255, choices=STATUS, default='Active')
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.user.full_name}"

# Document model for storing documents uploaded by users and companies
class Document(models.Model):
    FILE_TYPE = (
        ('Resume', 'Resume'),
        ('Certification', 'Certification'),
        ('CV', 'CV'),
    )
    FILE_FORMAT = (
        ('pdf', 'pdf'),
        ('txt', 'txt'),
    )
    owner_user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='documents')
    owner_company = models.ForeignKey(CompanyProfile, null=True, blank=True, on_delete=models.CASCADE, related_name='documents')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='documents',null=True, blank=True)  # Linked to Job model
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE)
    file_format = models.CharField(max_length=50, choices=FILE_FORMAT, default=FILE_FORMAT[0][0])
    file = CloudinaryField(resource_type='raw', blank=True, null=True)  # Using Cloudinary for file storage
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name + " - " + self.file_type


# Application model for job applications submitted by job seekers
class Application(models.Model):
    STATUS = (
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
    )
    NEXT_STEP = (
        ('Awaiting response', 'Awaiting response'),
        ('Technical Interview', 'Technical Interview'),
        ('N/A', 'N/A'),
        ('Welcome aboard', 'Welcome aboard'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications', limit_choices_to={'role': 'user'})  # Link to CustomUser
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50,choices=STATUS, default='Applied')
    next_step = models.CharField(max_length=50, choices=NEXT_STEP, default='Awaiting response')
    submitted_at = models.DateTimeField(auto_now_add=True)

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    portfolio = models.CharField(max_length=255, blank=True)

    resume = models.ForeignKey(Document, on_delete=models.PROTECT, null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    experience = models.IntegerField(null=True, blank=True)
    current_salary = models.IntegerField(blank=True, null=True)
    expected_salary = models.IntegerField(blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True)

    resume_viewed = models.BooleanField(default=False)
    profile_viewed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'job'], name='unique_user_job_application')
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.job.title}"


# Feedback model for company feedback on applications
class Feedback(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='feedbacks')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.application.user.full_name}"
