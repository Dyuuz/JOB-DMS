# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, UserProfile, CompanyProfile, Document, Application
from django.contrib.auth import authenticate
import os

class CustomUserCreationForm(UserCreationForm):
    # resume = forms.CharField(
    #     widget=forms.TextInput(attrs={'placeholder': 'Enter full name'})
    # )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter full name'})
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-role'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email',})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'role']
        widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.role = self.cleaned_data['role']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Authenticate the user using email as the username
            self.user = authenticate(username=email, password=password)
            if not self.user:
                self.add_error(None, 'Invalid login credentials')
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

class UserProfileForm(forms.ModelForm):
    # This is a non-model field
    existing_email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'input-field',
    }))
    existing_full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'input-field',
    }))

    resume= forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'input-field',
        'placeholder': 'Upload resume',
    }))
    class Meta:
        model = UserProfile
        fields = [
            'existing_full_name','phone', 'DOB', 'user_country', 'company_name', 'job_title', 'job_description', 'start_date', 'end_date',
            'employment_type', 'job_location', 'highest_education_level', 'work_field', 'work_experience', 'project',
            'resume', 'ready_to_work', 'bio', 'skills', 'certifications'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter phone number'}),
            'DOB': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Enter date of birth'}),
            'user_country': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter your country'}),

            'company_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter company name'}),
            'job_title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter job title'}),
            'job_description': forms.Textarea(attrs={'class': 'input-field' , 'rows': 2, 'placeholder': 'Enter job description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Select end date'}),
            'employment_type': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select employment type'}),
            'job_location': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter job location'}),

            'highest_education_level': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select education level'}),
            'work_field': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter work field'}),
            'work_experience': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Enter work experience'}),
            'project': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Enter project names'}),
            'resume': forms.FileInput(attrs={'class': 'input-field', 'placeholder': 'Upload resume'}),
            'ready_to_work': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Check if ready to work'}),

            'bio': forms.Textarea(attrs={'class': 'input-field', 'rows': 3, 'placeholder': 'Enter career summary'}),
            'skills': forms.Textarea(attrs={'class': 'input-field', 'rows': 2, 'placeholder': 'Enter skills'}),
            'certifications': forms.Textarea(attrs={'class': 'input-field', 'rows': 2, 'placeholder': 'Enter certifications'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Catch the user from the view
        super().__init__(*args, **kwargs)

        if user:
            self.fields['existing_email'].initial = user.email
            self.fields['existing_full_name'].initial = user.full_name

class CompanyProfileForm(forms.ModelForm):
    # This is a non-model field
    existing_email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'input-field',
    }))
    existing_full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'input-field',
    }))

    class Meta:
        model = CompanyProfile
        fields = [
            'existing_full_name', 'existing_email','work_mode', 'tagline', 'country', 'industry',
            'hire_status', 'company_reg_num', 'founded', 'parent_company', 'headquarters', 'annual_growth_rate', 'website',
            'about_us', 'mission_statement', 'core_tech', 'awards', 'certifications',
        ]
        widgets = {
            'industry': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Enter industry'}),
            'tagline': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter description'}),
            'country': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Enter country'}),
            'work_mode': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select work mode'}),

            'hire_status': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select hire status'}),
            'company_reg_num': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter registration number'}),
            'founded': forms.DateInput(attrs={'type': 'date','class': 'input-field', 'placeholder': 'Enter description'}),
            'parent_company': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter parent company'}),
            'headquarters': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter headquarters location'}),
            'annual_growth_rate': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Enter annual growth rate'}),
            'website': forms.URLInput(attrs={'class': 'input-field', 'placeholder': 'Enter website URL'}),

            'about_us': forms.Textarea(attrs={'class': 'input-field', 'rows': 3, 'placeholder': 'Enter about us'}),
            'mission_statement': forms.Textarea(attrs={'class': 'input-field', 'rows': 3, 'placeholder': 'Enter mission statement'}),

            'core_tech': forms.Textarea(attrs={'class': 'input-field', 'rows': 2, 'placeholder': 'Enter core technologies seperated by commas'}),
            'awards': forms.Textarea(attrs={'class': 'input-field', 'rows': 2, 'placeholder': 'Enter awards'}),
            'certifications': forms.Textarea(attrs={'class': 'input-field', 'rows': 2, 'placeholder': 'Enter certifications seperated by commas'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Catch the user from the view
        super().__init__(*args, **kwargs)

        if user:
            self.fields['existing_email'].initial = user.email
            self.fields['existing_full_name'].initial = user.full_name

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file_type', 'file_format', 'file', 'job']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'doc-form-input'}),
            'file_type': forms.Select(attrs={'class': 'doc-form-input'}),
            'file_format': forms.Select(attrs={'class': 'doc-form-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Limit job choices to those relevant to the user
        # if self.request and hasattr(self.request.user, 'companyprofile'):
        #     self.fields['job'].queryset = Job.objects.filter(company=self.request.user.companyprofile)
        # elif self.request and self.request.user.is_authenticated:
        #     self.fields['job'].queryset = Job.objects.none()  # Or set appropriate queryset for regular users
        # else:
        #     self.fields['job'].queryset = Job.objects.none()

        # Make job field optional
        self.fields['job'].required = False

        # Remove owner fields completely - we'll handle them in the view
        self.fields.pop('owner_user', None)
        self.fields.pop('owner_company', None)
        self.fields.pop('job', None)

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            # File size validation (5MB limit)
            max_size = 2 * 1024 * 1024  # 2MB in bytes
            if file.size > max_size:
                raise forms.ValidationError("File too large. Maximum size is 2MB.")

            # File extension validation
            valid_extensions = ['.pdf', '.doc', '.docx', '.txt' ]
            ext = os.path.splitext(file.name)[1].lower()

            if ext not in valid_extensions:
                raise forms.ValidationError(
                    "Unsupported file extension. Only PDF, Word, and text documents are allowed."
                )

        return file

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set owner based on user type
        if hasattr(self.request.user, 'companyprofile'):
            instance.owner_company = self.request.user.companyprofile
        else:
            instance.owner_user = self.request.user

        if commit:
            instance.save()
        return instance


class ApplicationForm(forms.ModelForm):
    # full_name = forms.CharField(required=False)
    # phone = forms.CharField(required=False)

    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        # 'readonly': 'readonly',
        'class': 'applynow-form-control',
    }))
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'applynow-form-control',
    }))
    phone = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
        # 'readonly': 'readonly',
        'class': 'applynow-form-control',
    }))

    class Meta:
        model = Application
        exclude = ['user', 'job', 'status', 'next_step', 'submitted_at']

        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'applynow-form-control', 'placeholder': 'Enter job title'}),
            'company': forms.TextInput(attrs={'class': 'applynow-form-control', 'placeholder': 'Enter company name'}),
            'portfolio': forms.TextInput(attrs={'class': 'applynow-form-control', 'placeholder': 'Enter site link'}),
            'availability': forms.TextInput(attrs={'class': 'applynow-form-control', 'placeholder': 'Enter the time for interviews'}),
            'expected_salary': forms.NumberInput(attrs={'class': 'applynow-form-control', 'placeholder': 'Enter salary'}),
            'experience': forms.NumberInput(attrs={'class': 'applynow-form-control', 'placeholder': 'Enter years of experience'}),
            'resume': forms.Select(attrs={'class': 'applynow-form-control', 'placeholder': 'Select resume'}),
            'cover_letter': forms.Textarea(attrs={'id': 'id_cover_letter', 'class': 'applynow-form-control', 'placeholder': 'Input cover letter'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Catch the user from the view
        super().__init__(*args, **kwargs)

        if user:
            self.fields['resume'].queryset = Document.objects.filter(owner_user=user)
            self.fields['full_name'].initial = user.full_name
            self.fields['phone'].initial = user.userprofile.phone
            self.fields['email'].initial= user.email
