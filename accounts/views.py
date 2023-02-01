
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .helpers import  send_otp_to_email
from .models import User,booking_info
from .utility import gen_next_date,gen_previous_date,gen_today
from twilio.rest import Client
from django.contrib import messages
from accounts.tasks import send_confirmation,send_cancel_confirmation
# Create your views here.
from datetime import date
@api_view(['GET', 'POST'])
def send_otp(request):
    if request.method=='POST':
        user_name = request.POST.get('username')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        if User.objects.filter(phone_number=phone).exists() and User.objects.get(phone_number=phone).is_phone_verified==True:
            return redirect('dashbord',phone)
            
            
            
        else:
            otp_in=send_otp_to_email(phone)
            try:
                user = User.objects.create_user(
                username= user_name,
                phone_number = phone,
                email = email,
                otp=otp_in

            )
            except Exception as e:
                user=User.objects.get(phone_number=phone)
                user.delete()
                return redirect('login')
            user.set_password("Adonis1234@")
            user.save()

            return redirect('verifyotp',phone=phone)
        #return render(request,'accounts/verifyotp.html',{"phone_number":phone,"otp":otp, "username":user_name})
    return render(request,'accounts/login.html')

@api_view(['GET', 'POST'])
def verify_otp(request,phone):
    try:
        User.objects.get(phone_number=phone)

    except Exception as e:
            return redirect('login')
    phone_num=str(phone)

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
        
    return render(request,'accounts/verifyotp.html')
def dashbord(request,phone):
    try:
        User.objects.get(phone_number=phone)
        print('not 1234'
              '121323e23dqwdxwqdx          '
              ''
              ''
              'd')
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
        if f.is_booked == False:
            print(f.slot_time)
            p=User.objects.get(phone_number=phone)
            f.phone_no_registered=phone
            f.is_booked=True 
            f.save()
            send_confirmation(p,f)

            # try:
            #     account_sid ='AC185bf5a96805805d856a9361b586bb5f'
            #     auth_token ='449fa052023cef80aa7a4e78d75861ee'
            #     client = Client(account_sid, auth_token)
            #
            #     message = client.messages.create(
            #                                 body='Hi '+ p.username +' you have booked '+f.ground_name + ' at '+ f.slot_time +' on ' + str(f.date) + '. Thankyou ',
            #                                 from_='+1 205 691 3855',
            #                                 to='+918625877270'
            #                                 )
            #     messages.info(request, 'Booking Successfull!')
            #     print(message.sid)
            #     return redirect('booked',phone)
            # except Exception as e:
            return redirect('booked',phone)
        else:
            return redirect('already_booked',phone)
        
    f=booking_info.objects.get(id=id)
    p=User.objects.get(phone_number=phone)
    context={"booking_info": f ,"user_info":p}
    return render(request,'accounts/bookingconfirm.html',context)

def booked(request,phone):
    context={'phone':phone}
    return render(request,'accounts/booked.html',context)

def already_booked(request,phone):
    context={'phone':phone}
    return render(request,'accounts/already_booked.html',context)

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
        f.phone_no_registered= ""
        f.is_booked=False
        send_cancel_confirmation(p, f)
        f.save()
        return redirect('canceled',phone)
    f=booking_info.objects.get(id=id)
    p=User.objects.get(phone_number=phone)
    context={"booking_info": f ,"user_info":p}
    return render(request,'accounts/cancelconfirm.html',context)


def canceled(request,phone):
    context={'phone':phone}
    return render(request,'accounts/canceled.html',context)
