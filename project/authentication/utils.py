from django.conf import settings
from twilio.rest import Client
from .models import User
from django.core.mail import send_mail,EmailMessage
from django.shortcuts import render,get_object_or_404
import os

# Twilio credentials
account_sid = 'AC8af0bcbb930845f03e2eda42dd5bc71f'
auth_token = '209c487c768d4a78da05dbf23e1932db'
twilio_phone_number = '+13346001897'

client = Client(account_sid, auth_token)

def send_sms(to_phone_number,otp): # Generate a random OTP
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=twilio_phone_number,
        to=to_phone_number
    )
    return otp, message.sid  # Return OTP and message SID

def send_otp(email,received_otp):
    message=""
    subject='OTP'
    otp_message= 'The OTP is ' + str(received_otp)
    email_from='vnjain2004@gmail.com'
    recipient_list=[email]

    user_profile = get_object_or_404(User,email=email)
    phone_number=user_profile.phone_number
    send_sms(phone_number,received_otp)
    send_mail(subject,otp_message,email_from,recipient_list)
    message = "OTP Sent via Email and Phone!"
    
    return received_otp, message


def send_pdf(email, pdf_name):
    subject = 'PDF'
    email_from = 'vnjain2004@gmail.com'
    recipient_list = [email]
    message = "PDF Sent!"
    pdf_path = os.path.join(settings.BASE_DIR, 'pdfs', pdf_name)
    # Create the email object
    emailll = EmailMessage(subject, message, email_from, recipient_list)

    try:
        # Open the PDF file in binary mode
        with open(pdf_path, 'rb') as f:
            # Attach the PDF file to the email
            emailll.attach(pdf_name, f.read(), 'application/pdf')

        # Send email
        emailll.send()
        return "PDF sent successfully!"
    
    except Exception as e:
        return f"Error sending email: {e}"