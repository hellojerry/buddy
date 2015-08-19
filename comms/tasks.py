from celery.decorators import task
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from accounts.models import User
from activities.models import Activity
from .calls import call_user, text_user
from .emails import send_conf_email
from .tweets import conf_tweet
from datetime import timezone, timedelta, datetime, time, tzinfo
import pytz

@shared_task
def private_message(recipient, conf):
    conf_tweet(recipient, conf)
    print('private message sent')

@shared_task
def make_text(phone, message):

    text_user(phone, message)
    print('conf text sent')
    
@shared_task
def call_list():
    now = datetime.datetime.now(pytz.UTC)
    back_bound = now - timedelta(minutes=10)
    front_bound = now + timedelta(minutes=10)
    flagged_activities = Activity.objects.filter(time__gte=back_bound).filter(
        time__lte=front_bound).filter(completed=False)
    for activity in flagged_activities:
        if activity.user.call != True or activity.user.phone == None:
            activity.is_open = False
            activity.save()
        else:
            activity.is_open = False
            print 
            call_user(activity.user.phone)
            activity.save()
            
    print('call list complete')
    
@shared_task
def send_email(temp_email, email_conf):
    print('email task received')
    print(temp_email)
    send_conf_email(temp_email, email_conf)
    print('email sent')
        