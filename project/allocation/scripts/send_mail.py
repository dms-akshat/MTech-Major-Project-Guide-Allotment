import requests
import time

def send_clashmail(student_data, professor):
    # Deployment URL of the Google Apps Script Web App
    deployment_url = 'https://script.google.com/macros/s/AKfycbzK-J_Lf6OBoV9wp1dmghns2-PeezeWyEeXvzhDMEhC-Ct5sYgLNVLsgNOxf89fkac_4w/exec'

    professor_email = 'rohithraichu@gmail.com'

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

    

    


