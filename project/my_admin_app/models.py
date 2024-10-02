from django.db import models
from django.utils import timezone
from datetime import date
class Date(models.Model):
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    guide_file_name = models.CharField(max_length=255, blank=True, null=True)
    student_file_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"From {self.start_date} to {self.end_date}"

class Guide(models.Model):
    guide_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    availability_status = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=100, unique=True)
    roll_no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    semester = models.IntegerField()
    backlogs = models.IntegerField()
    cgpa = models.FloatField()
    phone_number = models.CharField(max_length=15)
    cluster = models.IntegerField(default=0)
    allotment_status = models.CharField(max_length=30,default='Pending')
    allotment = models.CharField(max_length=30,default='',null=True)

    def __str__(self):
        return self.name
