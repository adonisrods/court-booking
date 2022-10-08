from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
#from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    username=models.CharField(max_length=12,unique=False )
    phone_number=models.CharField(max_length=12,unique=True)
    is_phone_verified = models.BooleanField(default=False)
    otp=models.CharField(max_length=6)
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS =['username',]
    # objects= UserManager()

    def __str__(self):
        
        return '{}  {}'.format(str(self.username), str(self.phone_number))

class booking_info(models.Model):
    date=models.DateField()
    is_booked =models.BooleanField(default=False)
    phone_no_registered=models.CharField(max_length=12)
    slot_time=models.CharField(max_length=5)
    ground_name=models.CharField(max_length=30)

    def __str__(self):
        return '{} {} {} {}'.format(str(self.slot_time), str(self.date), str(self.ground_name),str(self.phone_no_registered))
        

