from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from formbooking import settings
from django.utils import timezone
from datetime import date, timedelta
from .models import User

#Sends mail to all users with a custom message
@shared_task(bind=True)
def send_mail_func(self):
    users = User.objects.all()
        #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        print(user.name)
        mail_subject = "Hi! "+ user.name
        message = "hi this is sent to all users"
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )

    return "sent to my database"

#sends mail to the user who has his birthday Today
@shared_task(bind=True)
def send_confirmation(self,p,f):
    print("inside conriemation task")
    print(p.phone_number)
    print(f.slot_time)
    #user=User.objects.get(phone=date.today())
    mail_subject = "Hi! "+ p.username +", you have booked "+ f.ground_name +" at "+ f.slot_time
    print(mail_subject)
    message = "Booking successfull"
    to_email = 'adonistheas@gmail.com'
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "sent to birthday person"