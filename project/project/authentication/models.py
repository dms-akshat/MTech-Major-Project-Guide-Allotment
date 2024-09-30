from django.db import models
from .validators import CustomPasswordValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField(primary_key=True)
    phone_number = models.CharField(max_length=15,default=000000)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('faculty', 'Faculty'), ('admin', 'Admin')])
    password_changed = models.BooleanField(default=False)  # Track if password has been changed

    def save(self, *args, **kwargs):
        password_validator = CustomPasswordValidator()

        # Validate the password
        try:
            password_validator.validate(self.password)
        except ValidationError as e:
            raise ValidationError(e)

        # Hash the password before saving if it's not already hashed
        if not self.password.startswith('pbkdf2_'):  # Check if the password is already hashed
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
