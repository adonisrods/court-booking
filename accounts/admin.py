from django.contrib import admin
from .models import User,booking_info
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display= ('phone_number', 'username', 'is_phone_verified', 'email')

class booking_infoAdmin(admin.ModelAdmin):
    list_display= ('date', 'is_booked', 'phone_no_registered', 'slot_time', 'ground_name')
#hi test

admin.site.register(User,UserAdmin)
admin.site.register(booking_info,booking_infoAdmin)
