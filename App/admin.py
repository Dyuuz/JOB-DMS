from django.contrib import admin

from App.models import CustomUser, CompanyProfile, UserProfile, Company, Job, Application, Feedback

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyProfile)
admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Feedback)
