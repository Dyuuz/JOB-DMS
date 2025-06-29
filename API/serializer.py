# serializers.py
from rest_framework import serializers
from App.models import TeamManagement, Application

class TeamMgtSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamManagement
        fields = ['id', 'user', 'job', 'joined']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
