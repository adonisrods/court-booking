from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import  send_otp_to_phone
from .models import User,booking_info
from django.http import HttpRequest
from django.http import HttpResponse
from datetime import datetime, timedelta
from .utility import gen_next_date,gen_previous_date,gen_today
from django.contrib import messages
import requests
from .tasks import send_confirmation
#from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from accounts.tasks import send_confirmation
# Create your views here.
from datetime import date
@api_view(['GET', 'POST'])
def send_otp(request):
    if request.method== 'POST':
        user_name =  request.POST.get('username')
        phone =  request.POST.get('phone_number')
        otp_in=send_otp_to_phone(phone)
        print(user_name)
        print(phone)
        
        try:
            user = User.objects.create_user(
            username= request.POST.get('username'),
            phone_number = request.POST.get('phone_number'),
            otp=otp_in
        )
        except Exception as e:
            return render(request,'accounts/login.html')
        
        print("user created")
        user.set_password("Adonis1234@")
        user.save()
        print("otp sent")
        print("phone number is ",phone,user_name)
        return redirect('verifyotp',phone=phone)
        #return render(request,'accounts/verifyotp.html',{"phone_number":phone,"otp":otp, "username":user_name})
    return render(request,'accounts/login.html')

@api_view(['GET', 'POST'])
def verify_otp(request,phone):
    try:
        User.objects.get(phone_number=phone)
        print('not found')
    except Exception as e:
            return redirect('login')
    phone_num=str(phone)
    print("hi")
    count=0
    #if 'verifyotp' in request.POST:
    #if request.POST.get("verifyotp"):
    if request.method== 'POST':
        print("inside verify otp main clause")
        print("otp is",request.POST.get('otp'))
        user_obj = User.objects.get(phone_number = phone_num)
        print("found user")
        if user_obj.otp == request.POST.get('otp'):
            user_obj.is_phone_verified= True
            user_obj.save()
            print("otp matched")
            return redirect('dashbord',phone)
        else:
            print("invalid otp")
            
            # obj=User.objects.get(phone_number=phone)
            # obj.delete()
        
    return render(request,'accounts/verifyotp.html')

    
def dashbord(request,phone):
    try:
        User.objects.get(phone_number=phone)
        print('not found')
    except Exception as e:
            return redirect('login')
    print("inside dashbord")
    if request.method=='POST':
        print("inside dashbord  post function")
        date_today =str(date.today())
        date_str=date_today[0]+date_today[1]+date_today[2]+date_today[3]+date_today[5]+date_today[6]+date_today[8]+date_today[9]
        print(date_str)
        return redirect('booking',phone,date_str)
    context={"phone":phone}
    return render(request,'accounts/dashbord.html',context)

def booking(request,phone,date=date.today()):
    try:
        User.objects.get(phone_number=phone)
        print('not found')
    except Exception as e:
            return redirect('login')
    context={}
    print("inside dashbod function")
    date_manipulated=date[0]+date[1]+date[2]+date[3]+"-"+date[4]+date[5]+"-"+date[6]+date[7]
    for i in range(6,24):
        f=booking_info.objects.get_or_create(
        date=date_manipulated,
        slot_time= i,
        ground_name="SIMPLIZ TURF"
        )   
    Slot_Details=booking_info.objects.filter(date=date_manipulated)
    print(date_manipulated)
    prev_date=gen_previous_date(str(date_manipulated))
    next_date=gen_next_date(date_manipulated)
    ttoday=gen_today()
    is_book=Slot_Details[0].is_booked
    if is_book is False:
        is_book="available"
    else:
        is_book="Not Available"
    context={'current_date':date_manipulated,"previous_date":prev_date,"next_date":next_date,"today_date":ttoday,'status': Slot_Details, "phone":phone}
    
    return render(request,'accounts/booking.html',context)


def bookingconfirm(request,phone,id):
    try:
        User.objects.get(phone_number=phone)
        print('not found')
    except Exception as e:
            return redirect('login')
    print("inside booking confirmation")
    if request.method=='POST':
        print("inside booking confirmation post method")
        f=booking_info.objects.get(id=id)
        print(f.slot_time)
        p=User.objects.get(phone_number=phone)
        f.phone_no_registered=phone
        f.is_booked=True 
        f.save()
        send_confirmation(p,f)
        # url = "https://2factor.in/API/R1/"

        # payload='module=TRANS_SMS&apikey=7e825d24-XXXX-XXXX-XXXX-0200cd936042&to={phone}&from=HEADER&msg=DLT%20Approved%20Message%20Text%20Goes%20Here'
        # headers = {}

        # response = requests.request("POST", url, headers=headers, data=payload)



        return redirect('dashbord',phone)
    f=booking_info.objects.get(id=id)
    p=User.objects.get(phone_number=phone)
    context={"booking_info": f ,"user_info":p}
    return render(request,'accounts/bookingconfirm.html',context)