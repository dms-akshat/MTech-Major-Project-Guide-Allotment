from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
import csv
from datetime import datetime
from io import TextIOWrapper
import os
import subprocess  # Import subprocess for running SQL scripts

# views.py

from .models import Guide,Student,Date  # Assuming you have a model for your CSV files

def upload_csv(request):
    if request.method == "POST":
        guide_file = request.FILES['csv_file_guide']
        student_file = request.FILES['csv_file_student']
        start_date = request.POST.get('start_date')  # Expected format: YYYY-MM-DD
        end_date = request.POST.get('end_date')      # Expected format: YYYY-MM-DD

        # Validate dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")

        # Create a Date object
        date_entry, created = Date.objects.get_or_create(start_date=start_date, end_date=end_date)

        # Process guide CSV
        guide_data = csv.reader(guide_file.read().decode('utf-8').splitlines())
        next(guide_data)  # Skip the header
        for row in guide_data:
            guide_id, name, email, availability_status = row
            Guide.objects.get_or_create(
                guide_id=guide_id,
                defaults={
                    'name': name,
                    'email': email,
                    'availability_status': availability_status,
                    'date': date_entry  # Associate with Date object
                }
            )

        # Process student CSV
        student_data = csv.reader(student_file.read().decode('utf-8').splitlines())
        next(student_data)  # Skip the header
        for row in student_data:
            student_id, roll_no, name, email, semester, backlogs, cgpa, phone_number = row
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
                    'date': date_entry  # Associate with Date object
                }
            )

        return HttpResponse("CSV files uploaded and processed successfully.")

    return render(request, 'my_admin_app/upload_csv.html',created)  # Render the upload template


# def csv_file_list(request):
#     # Get the first (and only) CSV file
#     csv_file = CSVFile.objects.first()
#     if request.method == 'POST':  # Handle download request
#         if csv_file:  # Check if a CSV file exists
#             # Prepare the response for downloading the file
#             response = HttpResponse(csv_file.file, content_type='text/csv')
#             response['Content-Disposition'] = f'attachment; filename="{csv_file.file.name}"'
#             return response
#         else:
#             messages.error(request, "No CSV file found to download.")
#             return redirect('csv_file_list')  # Redirect if no file found

#     return render(request, 'csv_list.html', {'csv_file': csv_file})


def execute_sql_script(db_file: str, sql_file: str) -> None:
    try:
        # Command to execute the SQL script using sqlite3
        command = ['sqlite3', db_file, f'.read {sql_file}']
        
        # Run the command
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        
        # Output the result
        if result.stdout:
            print("Output:", result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
        
        print("SQL script executed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the SQL script:", e)


