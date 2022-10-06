import requests
import random
from rest_framework.response import Response
def send_otp_to_phone(phone_number):
    print("send_otp_to_phone")
    try:
        otp= random.randint(1000,9999)
        print("otp is",otp)
        url= f'https://2factor.in/API/V1/9dc3b4d8-399a-11ed-9c12-0200cd936042/SMS/{phone_number}/{otp}'
        response =requests.get(url)
        return otp
    except Exception as e:
        return Response({
        'status':400,'message':'otp not sent'
    })

