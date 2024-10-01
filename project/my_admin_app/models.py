from django.db import models
from django.utils import timezone
from datetime import date
class Date(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"From {self.start_date} to {self.end_date}"

class Guide(models.Model):
    guide_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    availability_status = models.CharField(max_length=100)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)  # FK to Date model

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
    date = models.ForeignKey(Date, on_delete=models.CASCADE)  # FK to Date model

    def __str__(self):
        return self.name
