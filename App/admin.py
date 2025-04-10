from django.contrib import admin

from App.models import CustomUser, CompanyProfile, UserProfile, Job, Application, Feedback

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name','email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyProfile)
admin.site.register(UserProfile)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Feedback)
