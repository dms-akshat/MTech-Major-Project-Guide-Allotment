from django.contrib.auth.hashers import check_password
from .models import User
from .forms import LoginForm
import random
from django.shortcuts import render, redirect, get_object_or_404
# views.py
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ChangePasswordForm
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from .validators import CustomPasswordValidator 
from .utils import send_otp

# Temporary OTP storage (in a production system, store it in cache or DB)
otp_store = {}

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)

                # Check if the password is correct
                if check_password(password, user.password):  # Ensure password is hashed in production
                    
                    # Check if the user has changed their password
                    if user.password_changed == 0:
                        return redirect('change_password_view', email=email)  # Redirect to password change

                    otp = str(random.randint(100000, 999999))
                    otp_store[email] = otp  # Store the OTP temporarily
                    send_otp(email,otp)
                    return redirect('otp_view', email=email)  # Redirect to the OTP view
                else:
                    return render(request, 'authentication/login.html', {'form': form, 'error': 'Invalid credentials'})
            except User.DoesNotExist:
                return render(request, 'authentication/login.html', {'form': form, 'error': 'User does not exist'})
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def otp_view(request, email):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        
        print(f"Entered OTP: {entered_otp}")  # Debug print
        print(f"Stored OTP: {otp_store.get(email)}")  # Debug print
        
        if otp_store.get(email) == entered_otp:  
            user = User.objects.get(email=email)
            otp_store.pop(email, None)  # Remove the OTP from the store after successful validation
            if user.role == 'student':
                return redirect('student_page', email=email)
            elif user.role == 'faculty':
                return redirect('faculty_page', email=email)
            elif user.role == 'admin':
                return redirect('admin_page', email=email)
        else:
            return render(request, 'authentication/otp.html', {'otp': otp_store.get(email), 'email': email, 'error': 'Invalid OTP'})
    
    else:
        otp = otp_store.get(email)
        return render(request, 'authentication/otp.html', {'otp': otp, 'email': email})

def student_page(request, email):
    user = User.objects.get(email=email)
    return render(request, 'authentication/student.html', {'user': user})

def faculty_page(request, email):
    user = User.objects.get(email=email)
    return render(request, 'authentication/faculty.html', {'user': user})

def admin_page(request, email):
    user = User.objects.get(email=email)
    return render(request, 'authentication/admin.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('login')

def change_password_view(request, email):
    user = get_object_or_404(User, email=email)  # Get the user by email
    password_validator = CustomPasswordValidator()  # Initialize the password validator

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            # Check if the old password matches the user's current password
            if check_password(old_password, user.password):
                try:
                    # Validate the new password using your custom validator
                    password_validator.validate(new_password)
                    
                    # If the password is valid, hash the new password and save it
                    user.password = make_password(new_password)
                    user.password_changed = 1  # Set password_changed to 1
                    user.save()

                    # Redirect based on user role
                    if user.role == 'student':
                        return redirect('student_page', email=user.email)
                    elif user.role == 'faculty':
                        return redirect('faculty_page', email=user.email)
                    elif user.role == 'admin':
                        return redirect('admin_page', email=user.email)

                except ValidationError as e:
                    # If password validation fails, show error messages
                    for error in e:
                        messages.error(request, error)

            else:
                messages.error(request, 'Incorrect old password.')
    else:
        form = ChangePasswordForm()

    return render(request, 'authentication/change_password.html', {'form': form, 'user': user})

