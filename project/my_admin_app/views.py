from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from .forms import CSVUploadForm
import csv
from datetime import datetime
from io import StringIO
import os
import subprocess  # Import subprocess for running SQL scripts
from .utils import validate_csv_headers
from django.conf import settings
from pathlib import Path

# views.py

from .models import Guide,Student,Date  # Assuming you have a model for your CSV files

UPLOAD_DIR = os.path.join(settings.BASE_DIR,'uploads')
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
            
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        guide_file_path = os.path.join(UPLOAD_DIR, guide_file.name)
        with open(guide_file_path, 'wb+') as destination:
            for chunk in guide_file.chunks():
                destination.write(chunk)
        print(f"Guide file saved at: {guide_file_path}")

        # Save the student file
        
        student_file_path = os.path.join(UPLOAD_DIR, student_file.name)
        with open(student_file_path, 'wb+') as destination:
            for chunk in student_file.chunks():
                destination.write(chunk)
        print(f"Student file saved at: {student_file_path}")

        # Create a Date object after deleting the previous one
        Date.objects.all().delete()
        date_entry, _ = Date.objects.get_or_create(start_date=start_date, end_date=end_date)
        date_entry.guide_file_name = guide_file.name
        date_entry.student_file_name = student_file.name
        date_entry.save()

        print(f"Guide file name saved in Date: {date_entry.guide_file_name}")
        print(f"Student file name saved in Date: {date_entry.student_file_name}")

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


def csv_file_list(request):
    # Fetch the first date entry (assuming you only have one)
    dates = Date.objects.first()

    guide_file_path = None
    student_file_path = None

    if dates:
        guide_file_path = os.path.join(UPLOAD_DIR, dates.guide_file_name) if dates.guide_file_name else None
        student_file_path = os.path.join(UPLOAD_DIR, dates.student_file_name) if dates.student_file_name else None

    # Check if files exist
    if guide_file_path and not os.path.exists(guide_file_path):
        messages.error(request, "Guide file not found.")
        guide_file_path = None  # Reset if not found

    if student_file_path and not os.path.exists(student_file_path):
        messages.error(request, "Student file not found.")
        student_file_path = None  # Reset if not found

    context = {
        'dates': dates,
        'guide_file_path': guide_file_path,
        'student_file_path': student_file_path,
    }

    return render(request, 'my_admin_app/csv_list.html', context)


def download_csv(request, file_type):
    # Determine which file to download based on file_type
    dates = Date.objects.first()  # Assuming only one Date entry exists

    if not dates:
        messages.error(request, "No date entry found.")
        return redirect('csv_file_list')

    if file_type == 'guide':
        file_name = dates.guide_file_name
    elif file_type == 'student':
        file_name = dates.student_file_name
    else:
        messages.error(request, "Invalid file type requested.")
        return redirect('csv_file_list')

    file_path = os.path.join(UPLOAD_DIR, file_name)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    else:
        messages.error(request, "File not found.")
        return redirect('csv_file_list')


