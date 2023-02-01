from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from formbooking import settings
from django.utils import timezone
from datetime import date, timedelta
from .models import User, booking_info
import twilio
from twilio.rest import Client
#Sends mail to all users with a custom message
# @shared_task(bind=True)
# def send_mail_func(self):
#     users = User.objects.all()
#         #timezone.localtime(users.date_time) + timedelta(days=2)
#     for user in users:
#         print(user.name)
#         mail_subject = "Hi! "+ user.name
#         message = "hi this is sent to all users"
#         to_email = user.email
#         send_mail(
#             subject = mail_subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[to_email],
#             fail_silently=True,
#         )

#     return "sent to my database"

#sends mail to the user who has his birthday Today
@shared_task(bind=True)
def send_confirmation(self,p,f):
    print("inside conriemation task")
    print(p.phone_number)
    print(p.email)
    print(f.slot_time)
    mail_subject = "Hi! "+ p.username +", you have booked "+ f.ground_name +" at "+ f.slot_time
    print(mail_subject)
    message = "Booking successfull"+p.username + " phone:"+p.phone_number+ ", you have booked "+ f.ground_name +" at "+ f.slot_time +" date:"+ str(f.date)
    to_email = str(p.email)
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "sent to registered"

@shared_task(bind=True)
def send_cancel_confirmation(self,p,f):
    print("inside conriemation task")
    print(p.phone_number)
    print(p.email)
    print(f.slot_time)
    mail_subject = "Hi! "+ p.username +", you have booked "+ f.ground_name +" at "+ f.slot_time + " is canceled"
    print(mail_subject)
    message = "Booking Canceled"+p.username + " phone:"+p.phone_number+ ", you have booked "+ f.ground_name +" at "+ f.slot_time +" date:"+ str(f.date)
    to_email = str(p.email)
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "sent to registered"



@shared_task(bind=True)
def send_mail_to_booked(self,name=None):
    
    booking= booking_info.objects.get(date=date.today)
    user=User.objects.get(phone_number=booking.phone_no_registered)
    mail_subject = "Hi! "+ user.username
    message ='Hi '+ user.username +' this is a reminder you have booked '+ booking.ground_name + ' at '+ booking.slot_time +' on ' + str(user.date) + '. Thankyou '
    to_email = 'adonistheas@gmail.com'
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    # account_sid ='AC185bf5a96805805d856a9361b586bb5f'
    # auth_token ='4b53a4c3bc0426e132cad5ca18922608'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #                             body='Hi '+ user.username +' this is a reminder you have booked '+ booking.ground_name + ' at '+ booking.slot_time +' on ' + str(user.date) + '. Thankyou ',
    #                             from_='+12056913855',
    #                             to='+918625877270'
    #                             )

    # print(message.sid)
    return "sent to registered person"