from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.urls import reverse  # Import reverse to generate URLs
from .models import User  # Import the User model
from .validators import CustomPasswordValidator  # Import the custom password validator

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'name', 'role','password_changed')  # Display fields in the list view (excluding password for security reasons)
    search_fields = ('email', 'phone_number', 'name')  # Allow searching by email and name
    fields = ('email','phone_number', 'name', 'password', 'role')  # Fields shown in the admin form (password is editable)

    def save_model(self, request, obj, form, change):
        password_validator = CustomPasswordValidator()

        # Check if the password is being entered or updated
        if 'password' in form.changed_data:
            new_password = form.cleaned_data['password']

            # Validate the new password
            try:
                password_validator.validate(new_password)
            except ValidationError as e:
                # Display validation errors on the admin form
                for error in e:
                    messages.error(request, error)

                # Clear the form fields to allow re-entry
                form.cleaned_data.clear()
                obj.password = None  # Clear the password field

                # Redirect to the Add User page
                return HttpResponseRedirect(reverse('admin:authentication_user_add'))

            # Hash the password if it's valid and not already hashed
            if not new_password.startswith('pbkdf2_'):
                obj.password = make_password(new_password)

        # Save the user only if there are no validation errors
        super().save_model(request, obj, form, change)

        # Show success message explicitly only when the user is saved
        messages.success(request, f"User '{obj.name}' added/updated successfully!")
