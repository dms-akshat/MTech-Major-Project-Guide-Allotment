# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Student(models.Model):
    student_id = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    email = models.EmailField(default="student@mail.com")
    semester = models.IntegerField(default=0)
    backlogs = models.IntegerField(default=0)
    cgpa = models.FloatField(default=0.0)
    phone_number = models.CharField(max_length=15,default="+911234567890")
    # eligibility = models.BooleanField(default=True)

class Guide(models.Model):  
    guide_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    guide_mail = models.EmailField(default="guide@mail.com")
    availability_status = models.BooleanField(default=True)

class PreferenceOrder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cgpa = models.FloatField(default=0.0)
    preference_order = models.TextField()  # Store the guide IDs in order

    def save(self, *args, **kwargs):
        # Automatically update the cgpa to match the student's cgpa
        if self.student:
            self.cgpa = self.student.cgpa
        super().save(*args, **kwargs)

class AllocatedGuide(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
