from django.shortcuts import redirect, render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .models import CustomUser, CompanyProfile, UserProfile, Job, Application, Feedback
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import login
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm, CompanyProfileForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
