# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, UserProfile
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
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'DOB', 'company_name', 'job_title', 'start_date', 'end_date',
            'employment_type', 'highest_education_level', 'work_field', 'work_experience',
            'resume', 'ready_to_work', 'bio', 'skills', 'certifications'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'DOB': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'highest_education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'work_field': forms.TextInput(attrs={'class': 'form-control'}),
            'work_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'ready_to_work': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
