# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from my_admin_app.models import Student,Guide

class PreferenceOrder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cgpa = models.FloatField(default=0.0)
    preference_order = models.JSONField()  # Store the guide IDs in order

    def save(self, *args, **kwargs):
        # Automatically update the cgpa to match the student's cgpa
        if self.student:
            self.cgpa = self.student.cgpa
        super().save(*args, **kwargs)

class AllocatedGuide(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
