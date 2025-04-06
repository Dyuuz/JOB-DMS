# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
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
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', })
    )
    class Meta:
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
