import requests
import time
from my_admin_app.models import Guide

def send_clashmail(student_data, professor):
    # Deployment URL of the Google Apps Script Web App
    deployment_url = 'https://script.google.com/macros/s/AKfycbyZK-lh1tmi2_OWGe7Bw3wL89Cl4hT3tEb8-uTj7WN8rX5urIEcOwW3SUiF01dU7SR9Ug/exec'
    professor_email = professor #Guide.objects.get(professor).email

    payload = {
        'action': 'createForm',
        'students': student_data,
        'email': professor_email
    }

    print(student_data)

    # Send request to create the form
    response = requests.post(deployment_url, json=payload)
    print("Form Creation Response -> ", response.text)  # This will print the form URL

    # Wait for the professor to fill the form (e.g., 2 minutes)
    time.sleep(30)

    # Send GET request to retrieve the selected student
    payload = {'action': 'getFormResponse'}
    response = requests.post(deployment_url, json=payload)
    print("Form Response -> ", response.text)  # This will print the selected student

    selected_student = response.text

    payload = {'action' : 'resetForm'}
    response = requests.post(deployment_url, json=payload)
    print("Form has been reset/deleted!")

    return selected_student

    

    


