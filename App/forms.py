# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, UserProfile, CompanyProfile
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
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

    class Meta:
        model = UserProfile
        fields = [
            'existing_full_name','phone', 'DOB', 'company_name', 'job_title', 'start_date', 'end_date',
            'employment_type', 'highest_education_level', 'work_field', 'work_experience',
            'resume', 'ready_to_work', 'bio', 'skills', 'certifications'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter phone number'}),
            'DOB': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Enter date of birth'}),
            'company_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter company name'}),
            'job_title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter job title'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Select end date'}),
            'employment_type': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select employment type'}),
            'highest_education_level': forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select education level'}),
            'work_field': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter work field'}),
            'work_experience': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Enter work experience'}),
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
            'existing_full_name', 'existing_email','address', 'country', 'industry'
        ]
        widgets = {
            'address': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter phone number'}),
            'country': forms.DateInput(attrs={'type': 'date', 'class': 'input-field', 'placeholder': 'Enter country'}),
            'address': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter company name'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Catch the user from the view
        super().__init__(*args, **kwargs)

        if user:
            self.fields['existing_email'].initial = user.email
            self.fields['existing_full_name'].initial = user.full_name
