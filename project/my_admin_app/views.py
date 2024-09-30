from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import CSVFile
import csv
from io import TextIOWrapper
import os
import subprocess  # Import subprocess for running SQL scripts

def upload_csv(request):
    if request.method == 'POST':
        formss = CSVUploadForm(request.POST, request.FILES)
        if formss.is_valid():
            csv_file = request.FILES['csv_file']
            start_date = formss.cleaned_data['start_date']
            end_date = formss.cleaned_data['end_date']
            if(start_date >= end_date):
                messages.error(request, "End date cannot be before start date")
                return redirect('upload_csv')
            # Check the file extension (Allow only CSV or XLSX)
            
            request.session['start_date'] = str(start_date)  # Convert to string if needed
            request.session['end_date'] = str(end_date)
            file_extension = os.path.splitext(csv_file.name)[1].lower()
            if file_extension not in ['.csv', '.xlsx']:
                messages.error(request, "Unsupported file format! Please upload a CSV or XLSX file.")
                return redirect('upload_csv')

            # Replace old file if it exists
            existing_csv_file = CSVFile.objects.first()  # Assuming only one CSV file is saved
            if existing_csv_file:
                # Delete the old file
                existing_csv_file.file.delete(save=False)  # Delete the old file but keep the database entry

                # Update the existing entry with the new file and dates
                existing_csv_file.file = csv_file
                existing_csv_file.start_date = start_date
                existing_csv_file.end_date = end_date
                existing_csv_file.save()
            else:
                # No existing file, so create a new entry
                CSVFile.objects.create(file=csv_file, start_date=start_date, end_date=end_date)

            messages.success(request, "File uploaded successfully!")
            return redirect('csv_file_list')
        else:
            messages.error(request, "Form is invalid.")
    else:
        formss = CSVUploadForm()

    return render(request, 'upload_csv.html', {'formss': formss})

def csv_file_list(request):
    # Get the first (and only) CSV file
    csv_file = CSVFile.objects.first()
    if request.method == 'POST':  # Handle download request
        if csv_file:  # Check if a CSV file exists
            # Prepare the response for downloading the file
            response = HttpResponse(csv_file.file, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{csv_file.file.name}"'
            return response
        else:
            messages.error(request, "No CSV file found to download.")
            return redirect('csv_file_list')  # Redirect if no file found

    return render(request, 'csv_list.html', {'csv_file': csv_file})
