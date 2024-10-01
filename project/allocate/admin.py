from django.contrib import admin

# Register your models here.
from .models import PreferenceOrder,AllocatedGuide

class AllocatedGuideAdmin(admin.ModelAdmin):
    list_display = ('guide_id', 'student_id')  # Add the fields you want to display

admin.site.register(AllocatedGuide, AllocatedGuideAdmin)


admin.site.register(PreferenceOrder)