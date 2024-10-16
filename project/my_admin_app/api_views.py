# api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import Guide, Student, Date
from .serializers import GuideSerializer, StudentSerializer, DateSerializer
from .utils import validate_csv_headers
import csv
from io import StringIO
import os
from django.conf import settings
from datetime import datetime

UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'uploads')
EXPECTED_GUIDE_HEADERS = ['guide_id', 'name', 'guide_mail', 'availability_status']
EXPECTED_STUDENT_HEADERS = ['student_id', 'roll_no', 'name', 'email', 'semester', 'backlogs', 'cgpa', 'phone_number']

class UploadCSVAPI(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        guide_file = request.FILES.get('csv_file_guide')
        student_file = request.FILES.get('csv_file_student')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Validate dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date >= end_date:
                return Response({"error": "End date cannot be before start date."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate CSV headers
        guide_file_content = guide_file.read().decode('utf-8')
        student_file_content = student_file.read().decode('utf-8')

        if not validate_csv_headers(guide_file_content, EXPECTED_GUIDE_HEADERS):
            return Response({"error": "Invalid guide file headers. Expected headers: " + ", ".join(EXPECTED_GUIDE_HEADERS)}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validate_csv_headers(student_file_content, EXPECTED_STUDENT_HEADERS):
            return Response({"error": "Invalid student file headers. Expected headers: " + ", ".join(EXPECTED_STUDENT_HEADERS)}, status=status.HTTP_400_BAD_REQUEST)

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        guide_file_path = os.path.join(UPLOAD_DIR, guide_file.name)
        with open(guide_file_path, 'wb+') as destination:
            for chunk in guide_file.chunks():
                destination.write(chunk)

        student_file_path = os.path.join(UPLOAD_DIR, student_file.name)
        with open(student_file_path, 'wb+') as destination:
            for chunk in student_file.chunks():
                destination.write(chunk)

        # Create or update Date entry
        Date.objects.all().delete()
        date_entry, _ = Date.objects.get_or_create(start_date=start_date, end_date=end_date)
        date_entry.guide_file_name = guide_file.name
        date_entry.student_file_name = student_file.name
        date_entry.save()

        # Process guide CSV
        guide_data = csv.reader(StringIO(guide_file_content))
        next(guide_data)
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
        next(student_data)
        for row in student_data:
            student_id, roll_no, name, email, semester, backlogs, cgpa, phone_number = row
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

        return Response({"message": "CSV files uploaded and processed successfully."}, status=status.HTTP_201_CREATED)

class DownloadCSVAPI(APIView):
    def get(self, request, file_type):
        dates = Date.objects.first()
        if not dates:
            return Response({"error": "No date entry found."}, status=status.HTTP_404_NOT_FOUND)

        if file_type == 'guide':
            file_name = dates.guide_file_name
        elif file_type == 'student':
            file_name = dates.student_file_name
        else:
            return Response({"error": "Invalid file type requested."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
        else:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
