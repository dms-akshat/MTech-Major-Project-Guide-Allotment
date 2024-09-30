from django.contrib import admin

# Register your models here.
from .models import Student,Guide,PreferenceOrder,AllocatedGuide

admin.site.register(Student)
class AllocatedGuideAdmin(admin.ModelAdmin):
    list_display = ('guide_id', 'student_id')  # Add the fields you want to display

admin.site.register(AllocatedGuide, AllocatedGuideAdmin)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('guide_id', 'name')  # Add the fields you want to display

admin.site.register(Guide, GuideAdmin)
admin.site.register(PreferenceOrder)