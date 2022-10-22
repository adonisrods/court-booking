from asyncio.windows_events import NULL
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
import os
import twilio
from twilio.rest import Client
from django.contrib import messages

from django.utils.safestring import mark_safe
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
        if User.objects.filter(phone_number=phone).exists() and User.objects.get(phone_number=phone).is_phone_verified==True:
            # user=User.objects.get(phone_number=phone)
            # if user.is_phone_verified==True:
                
            return redirect('dashbord',phone)
            
            
            
        else:
            otp_in=send_otp_to_phone(phone)
            print(user_name)
            print(phone)
            
            try:
                print("trying to create user")
                user = User.objects.create_user(
                username= request.POST.get('username'),
                phone_number = request.POST.get('phone_number'),
                otp=otp_in
            )
            except Exception as e:
                # try:
                    
                #     if user.is_phone_verified == True:
                #         context={"phone":phone}
                #         return redirect('dashbord',context) 
                # except Exception as e:
                    user=User.objects.get(phone_number=phone)
                    user.delete()
                    print("previous user deleted")
                    return redirect('login')
            
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
        print('found')
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
            messages.info(request, 'Invalid OTP!')
            # obj=User.objects.get(phone_number=phone)
            # obj.delete()
        
    return render(request,'accounts/verifyotp.html')

    
# def dashbord(request,phone):
#     try:
#         User.objects.get(phone_number=phone)
#         print('not found')
#     except Exception as e:
#             return redirect('login')
#     print("inside dashbord")
#     if request.method=='POST':
#         print("inside dashbord  post function")
#         date_today =str(date.today())
#         date_str=date_today[0]+date_today[1]+date_today[2]+date_today[3]+date_today[5]+date_today[6]+date_today[8]+date_today[9]
#         print(date_str)
#         return redirect('booking',phone,date_str)
#     context={"phone":phone}
#     return render(request,'accounts/dashbord.html',context)
    
def dashbord(request,phone):
    try:
        User.objects.get(phone_number=phone)
        print('not found')
    except Exception as e:
            return redirect('login')
    print("inside dashbord")
    
    print("inside dashbord  post function")
    date_today =str(date.today())
    date_str=date_today[0]+date_today[1]+date_today[2]+date_today[3]+date_today[5]+date_today[6]+date_today[8]+date_today[9]
    print(date_str)
    context={"phone":phone,"ground_name1":"SIMPLIZ TURF","ground_name2":"Test","date_today":date_str}
    return render(request,'accounts/dashbord.html',context)

def booking(request,phone,ground_name,date=date.today()):
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
        ground_name=ground_name
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
    context={'current_date':date_manipulated,"previous_date":prev_date,"next_date":next_date,"today_date":ttoday,'status': Slot_Details, "phone":phone, "ground_name":ground_name}
    
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
        try:
            account_sid ='AC185bf5a96805805d856a9361b586bb5f'
            auth_token ='449fa052023cef80aa7a4e78d75861ee'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                        body='Hi '+ p.username +' you have booked '+f.ground_name + ' at '+ f.slot_time +' on ' + str(f.date) + '. Thankyou ',
                                        from_='+1 205 691 3855',
                                        to='+918625877270'
                                        )
            messages.info(request, 'Booking Successfull!')
            print(message.sid)
        except Exception as e:
            return redirect('booked',phone)

        return redirect('dashbord',phone)
    f=booking_info.objects.get(id=id)
    p=User.objects.get(phone_number=phone)
    context={"booking_info": f ,"user_info":p}
    return render(request,'accounts/bookingconfirm.html',context)

def booked(request,phone):
    context={'phone':phone}
    return render(request,'accounts/booked.html',context)


def cancelconfirm(request,phone,id):
    try:
        User.objects.get(phone_number=phone)
        print('not found')
    except Exception as e:
            return redirect('login')
    print("inside booking confirmation")
    if request.method=='POST':
        print("inside cancel confirmation post method")
        f=booking_info.objects.get(id=id)
        print(f.slot_time)
        p=User.objects.get(phone_number=phone)
        f.phone_no_registered=NULL
        f.is_booked=False 
        f.save()
        # send_confirmation(p,f)
        # # url = "https://2factor.in/API/R1/"

        # # payload='module=TRANS_SMS&apikey=7e825d24-XXXX-XXXX-XXXX-0200cd936042&to={phone}&from=HEADER&msg=DLT%20Approved%20Message%20Text%20Goes%20Here'
        # # headers = {}

        # # response = requests.request("POST", url, headers=headers, data=payload)
        # account_sid ='AC185bf5a96805805d856a9361b586bb5f'
        # auth_token ='4b53a4c3bc0426e132cad5ca18922608'
        # client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #                             body='Hi '+ p.username +' you have booked '+f.ground_name + ' at '+ f.slot_time +' on ' + str(f.date) + '. Thankyou ',
        #                             from_='+12056913855',
        #                             to='+918625877270'
        #                             )

        # print(message.sid)


        return redirect('dashbord',phone)
    f=booking_info.objects.get(id=id)
    p=User.objects.get(phone_number=phone)
    context={"booking_info": f ,"user_info":p}
    return render(request,'accounts/cancelconfirm.html',context)