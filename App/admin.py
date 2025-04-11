from django.contrib import admin

from App.models import CustomUser, CompanyProfile, UserProfile, Job, Application, Feedback

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name','email',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','work_field', 'bio')

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user','company_id','work_mode','description','industry','country',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Feedback)
