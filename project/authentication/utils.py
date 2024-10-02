from django.conf import settings
from twilio.rest import Client
from .models import User
from django.core.mail import send_mail,EmailMessage
from django.shortcuts import render,get_object_or_404
import os

# Twilio credentials
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_phone_number = settings.TWILIO_PHONE_NUMBER

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

