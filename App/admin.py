from django.contrib import admin

from App.models import Client, DocumentForm

# Register your models here.
admin.site.register(DocumentForm)
admin.site.register(Client)
