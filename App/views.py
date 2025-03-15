from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .models import Client


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
