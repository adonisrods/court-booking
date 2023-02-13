import requests
import random
from django.core.mail import send_mail
from formbooking import settings
from rest_framework.response import Response
# def send_otp_to_phone(phone_number):
#     print("send_otp_to_phone")
#     try:
#         otp= random.randint(1000,9999)
#         print("otp is",otp)
#         url= f'https://2factor.in/API/V1/9dc3b4d8-399a-11ed-9c12-0200cd936042/SMS/{phone_number}/{otp}'
#         response =requests.get(url)
#         return otp
#     except Exception as e:
#         return Response({
#         'status':400,'message':'otp not sent'
#     })

def send_otp_to_email(email):
    try:
        otp= random.randint(1000,9999)
        print("otp is",otp)
        message = "Hi use the OTP: " + str(otp) + " to verify your account"
        mail_subject = "Hi! OTP verification for futbook"
        to_email = email


        #send_mail('Mail Subject', 'Mail content', settings.EMAIL_HOST_USER, ['rodriguesadonis25@gmail.com'], fail_silently=False)
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,

        )


        return otp
    except Exception as e:
        return Response({
        'Status':'null'
    })