from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import CSVFile
import csv,os
from io import TextIOWrapper
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def upload_csv(request):
    if request.method == 'POST':
        formss = CSVUploadForm(request.POST, request.FILES)
        if formss.is_valid():
            csv_file = request.FILES['csv_file']
            start_date = formss.cleaned_data['start_date']
            end_date = formss.cleaned_data['end_date']

            # Check if the uploaded file is a valid CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Invalid file type! Please upload a CSV file.")
                return render(request, 'upload_csv.html', {'formss': formss})  # Render with form errors
            
            try:
                # Convert file to text wrapper for CSV reading
                file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
                csv_reader = csv.reader(file_wrapper)
                headers = next(csv_reader)  # Read the first row as header

                # Define your expected headers
                expected_headers = ['Roll No', 'Name', 'Major CGPA', '1', '2', '3', '4' ,'5','6','7','8','9','10','11','12','13','14']

                # Validate the headers
                if headers != expected_headers:
                    messages.error(request, "Invalid CSV file format! Expected headers: " + ', '.join(expected_headers))
                    return render(request, 'upload_csv.html', {'formss': formss})  # Render with form errors

            except Exception as e:
                messages.error(request, "Error reading CSV file: " + str(e))
                return render(request, 'upload_csv.html', {'formss': formss})  # Render with form errors

            # Check if there's an existing CSV file
            existing_csv = CSVFile.objects.first()  # Get the first (and only) existing file
            if existing_csv:
                # Delete the existing file from the file system (optional)
                if existing_csv.file:
                    existing_csv.file.delete(save=False)  # Delete the file from storage
                # Remove the existing record from the database
                existing_csv.delete()

            # Save the new CSV file and dates to the database
            CSVFile.objects.create(file=csv_file, start_date=start_date, end_date=end_date)

            messages.success(request, "CSV file uploaded successfully!")
            return redirect('csv_file_list')  # Redirect to the list view after upload
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
