from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formbooking.settings')

app = Celery('formbooking')
#Disabling the UTC Time Zone
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-to-booked': {
        #Calling the Send mail to birthday user function
        'task': 'accounts.tasks.send_mail_to_booked',
        'schedule': crontab(hour=17, minute=26, day_of_month="*"),
        #we can also Send argumentsto function calls
        #'args': (user.name, user.date, msg)
    }
    
}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html
#discover tasks Automatically to Trigger
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')