from django.contrib import admin

from App.models import CustomUser, CompanyProfile, UserProfile, Job, Application, Feedback, Document

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name','email',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','work_field', 'bio',)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('owner_user','name', 'file_type', 'file_format',)

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user','company_reg_num','work_mode','description','industry','country',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Feedback)
admin.site.register(Document, DocumentAdmin)
