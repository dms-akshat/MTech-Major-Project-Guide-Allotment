# serializers.py

from rest_framework import serializers
from .models import Guide, Student, Date

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ['guide_id', 'name', 'email', 'availability_status']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'roll_no', 'name', 'email', 'semester', 'backlogs', 'cgpa', 'phone_number']

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ['start_date', 'end_date', 'guide_file_name', 'student_file_name']
