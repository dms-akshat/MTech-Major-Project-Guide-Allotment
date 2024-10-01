from django.contrib import admin
from .models import Guide, Student, Date

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('guide_id','name', 'email', 'availability_status','date')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'roll_no', 'name','email', 'semester','cgpa','phone_number','date')

@admin.register(Date)
class Date(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date')
