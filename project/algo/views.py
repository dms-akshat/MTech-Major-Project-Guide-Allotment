from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from algo.scripts.alloc_algo import alloc_algorithm
from my_admin_app.models import Date,Guide
from algo.models import AllocatedGuide
from datetime import date
from report.utils import dbToPDF,dbToPDFGuide

def index(request):
    return HttpResponse("Hello, world. You're at the allocation index.")

def status(request, email):
    try:
        # Check if there are no Date objects or if the current date is before the end date
        if Date.objects.count() == 0 or date.today() < Date.objects.first().end_date:
            messages.error(request, "Allocation has not finished yet...")
            return redirect('admin_page', email=email)

        # Call the allocation algorithm
        alloc_algorithm()
        running=True
        # Render the start algorithm template
        return render(request, 'algo/start_algorithm.html', {'email': email,'algorithm_complete':running})
    
    except Exception as e:
        # Handle exceptions and show an error message
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('admin_page', email=email)

def generate_report(request, email):
    # Generate initial report
    dbToPDF(email)

    # Fetch all guides
    guides = Guide.objects.all()
    for guide in guides:
        # Check if there are allocated students for the guide
        allocated_students = AllocatedGuide.objects.filter(guide=guide)
        if allocated_students.exists():
            print(f"Generating report for guide ID: {guide.guide_id}, Email: {guide.email}")
            dbToPDFGuide(guide.guide_id, guide.email)  # Use the provided email
        else:
            print(f"No students found for guide ID: {guide.guide_id}. Skipping PDF generation.")

    return render(request, 'algo/report_successful.html', {
        'message': 'Report generation successful! Report sent to your mail!',
        'email': email
    })
