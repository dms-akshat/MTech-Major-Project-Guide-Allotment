from django.contrib import admin
from .models import CSVFile

@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'start_date', 'end_date')
