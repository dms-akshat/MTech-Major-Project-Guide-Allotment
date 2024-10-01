from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
import csv
from datetime import datetime
from io import StringIO
import os
import subprocess  # Import subprocess for running SQL scripts
from .utils import validate_csv_headers

# views.py

from .models import Guide,Student,Date  # Assuming you have a model for your CSV files


EXPECTED_GUIDE_HEADERS = ['guide_id', 'name', 'guide_mail', 'availability_status']
EXPECTED_STUDENT_HEADERS = ['student_id', 'roll_no', 'name', 'email', 'semester', 'backlogs', 'cgpa', 'phone_number']

def upload_csv(request):
    if request.method == "POST":
        guide_file = request.FILES.get('csv_file_guide')
        student_file = request.FILES.get('csv_file_student')
        start_date = request.POST.get('start_date')  # Expected format: YYYY-MM-DD
        end_date = request.POST.get('end_date')      # Expected format: YYYY-MM-DD

        # Validate dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date >= end_date:
                messages.error(request, "End date cannot be before start date")
                return redirect('upload_csv')
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect('upload_csv')

        # Read guide file content into memory
        guide_file_content = guide_file.read().decode('utf-8')
        # Read student file content into memory
        student_file_content = student_file.read().decode('utf-8')

        # Validate CSV headers for guide file
        if guide_file:
            if not validate_csv_headers(guide_file_content, EXPECTED_GUIDE_HEADERS):
                messages.error(request, "Invalid guide file headers. Expected headers: " + ", ".join(EXPECTED_GUIDE_HEADERS))
                return redirect('upload_csv')  # Redirect if headers are invalid
            
        # Validate CSV headers for student file
        if student_file:
            if not validate_csv_headers(student_file_content, EXPECTED_STUDENT_HEADERS):
                messages.error(request, "Invalid student file headers. Expected headers: " + ", ".join(EXPECTED_STUDENT_HEADERS))
                return redirect('upload_csv')  # Redirect if headers are invalid

        # Create a Date object after deleting the previous one
        Date.objects.all().delete()
        date_entry, _ = Date.objects.get_or_create(start_date=start_date, end_date=end_date)

        # Process guide CSV
        guide_data = csv.reader(StringIO(guide_file_content))
        next(guide_data)  # Skip the header
        for row in guide_data:
            guide_id, name, email, availability_status = row
            Guide.objects.get_or_create(
                guide_id=guide_id,
                defaults={
                    'name': name,
                    'email': email,
                    'availability_status': availability_status,
                }
            )

        # Process student CSV
        student_data = csv.reader(StringIO(student_file_content))
        next(student_data)  # Skip the header
        for row in student_data:
            student_id, roll_no, name, email, semester, backlogs, cgpa, phone_number = row
            # Add +91 to phone number if not already present
            if not phone_number.startswith("+91"):
                phone_number = "+91" + phone_number.strip()
            Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    'roll_no': roll_no,
                    'name': name,
                    'email': email,
                    'semester': semester,
                    'backlogs': backlogs,
                    'cgpa': cgpa,
                    'phone_number': phone_number,
                }
            )

        messages.success(request, "CSV files uploaded and processed successfully.")
        return redirect('csv_file_list')

    return render(request, 'my_admin_app/upload_csv.html')





