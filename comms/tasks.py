from celery.decorators import task
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from accounts.models import User
from activities.models import Activity
from .calls import call_user, text_user
from .emails import send_conf_email, send_warning_email
from .tweets import conf_tweet, tweet_status
from datetime import timezone, timedelta, datetime, time, tzinfo
import pytz
from operator import itemgetter


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
    '''
    Makes calls to all non-checked-in users with an activity due.
    '''
    now = datetime.now(pytz.UTC)
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
            call_user(activity.user.phone)
            activity.save()

    print('call list complete')

@shared_task
def text_warnings():
    '''
    Text warnings are done 30 minutes in advance.

    '''
    now = datetime.now(pytz.UTC)
    back_bound = now + timedelta(minutes=20)
    front_bound = now + timedelta(minutes=40)
    flagged_activities = Activity.objects.filter(time__gte=back_bound).filter(
        time__lte=front_bound).filter(completed=False)
    print('text warnings fired')
    for activity in flagged_activities:
        if activity.user.text != True or activity.user.phone == None:
            pass
        else:
            phone = activity.user.phone
            message = '''
            ABB: Item due in 30 minutes!
            '''
            text_user(phone, message)
    print('text warnings sent')

@shared_task
def email_warnings():
    '''
    warnings are done 1 hour in advance.
    '''
    now = datetime.now(pytz.UTC)
    back_bound = now + timedelta(minutes=50)
    front_bound = now + timedelta(minutes=70)
    flagged_activities = Activity.objects.filter(time__gte=back_bound).filter(
        time__lte=front_bound).filter(completed=False)
    for activity in flagged_activities:
        if activity.user.email_me != True:
            pass
        else:
            send_warning_email(activity.user.email, activity.name)
    print('warnings sent')

# @shared_task
# def tweet_winners():
#     '''
#     tweets are done once a week.
#     15 maximum per the twitter API
#     '''
#     target_users = User.objects.filter(twitter_handle!=None).filter(
#         tweet=True)
#     # this isn't particularly quick, as we need to run through
#     # every user queried and get their values from a model method,
#     # and not a database field. That being said, this is a once-weekly
#     # activity and isn't critical to the functioning of the app.
#     scores = []
#     for user in target_users:
#         if user.points > 0:
#             scores.append({'user':user.twitter_handle, 'points': user.points})
#     ordered = sorted(scores, key=itemgetter('points'), reverse=True)
#     for handle in ordered[0:14]:



@shared_task
def send_email(temp_email, email_conf):

    send_conf_email(temp_email, email_conf)
    print('email sent')
