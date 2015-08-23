from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

import celery
import pytz

from datetime import timedelta, datetime, timezone

from localflavor.us.models import PhoneNumberField
import string, random

def make_conf(length=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(length))

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')
        
        user = self.model(
            email = self.normalize_email(email), username=kwargs.get('username')
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = PhoneNumberField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=20, blank=True, null=True)
    tweet = models.BooleanField(default=False)
    call = models.BooleanField(default=True)
    text = models.BooleanField(default=False)
    email_me = models.BooleanField(default=False)
    
    TIME_ZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
    
    time_zone = models.CharField(max_length=70,
                                 choices=TIME_ZONE_CHOICES,
                                 default='UTC')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    def get_short_name(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        
    @property
    def current_streak(self):
        current_streak = []
        activities = self.activity_set.all().filter(
            is_open=False).order_by('-time')
        try:
            activities[0]
        except:
            return 0
        counter = 0
        now = datetime.now(timezone.utc)

        if now.date() - activities[0].time.date() > timedelta(hours=24):
            return 0

        
        for i in activities:
            if counter < len(activities) -1 :
                counter += 1

            if i.time.date() - activities[counter].time.date() > timedelta(1):
                if i.completed == True and i.time.date() not in current_streak:
                    current_streak.append(i.time.date())
                    break
                else:
                    break
            if i.completed == True and i.time.date() not in current_streak:
                current_streak.append(i.time.date())

            elif i.completed == True and i.time.date() in current_streak:

                pass
            else:

                break
        return len(current_streak)
    
    @property
    def longest_streak(self):
        peak_streak = 0
        sublist = []
        activities = self.activity_set.all().filter(is_open=False).order_by('time')
        try:
            activities[0]
        except:
            return 0
        
        counter = 0
        for i in activities:
            
            if i.completed == True and i.time.date() not in sublist:
                sublist.append(i.time.date())

                if len(sublist) > peak_streak:
                    peak_streak = len(sublist)
            elif i.completed == True and i.time.date() in sublist:
                pass
            if counter < len(activities) - 1:
                counter += 1
            if activities[counter].time.date() - i.time.date() > timedelta(hours=24):
                sublist = []
                

        return peak_streak
    
    @property
    def points(self):
        longest_streak = self.longest_streak
        checkins_points = len(self.activity_set.filter(completed=True))
        missed = len(self.activity_set.filter(is_open=False).filter(completed=False))
        checkins_score = checkins_points - missed if checkins_points > missed else 0
        streak_points = 2*longest_streak if longest_streak > 10 else longest_streak
        return checkins_score + streak_points
    
class TempData(models.Model):
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=20, blank=True, null=True)
    kill_time = models.DateTimeField()
    phone_conf = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email_conf = models.CharField(max_length=20, unique=True, blank=True, null=True)
    twitter_conf = models.CharField(max_length=20, unique=True, blank=True, null=True)
    user = models.OneToOneField(User)
    
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self.phone:
            self.phone_conf = make_conf()
        if self.email:
            self.email_conf = make_conf()
        if self.twitter_handle:
            self.twitter_conf = make_conf()
        self.kill_time = datetime.utcnow() + timedelta(minutes=30)
        if not self.twitter_handle and not self.phone and not self.email:
            raise ValueError('at least one field required.')
        super().save(*args, **kwargs)
    
from .tasks import delete_temp

def temp_handler(sender, instance, *args, **kwargs):
    delete_temp.apply_async(eta=instance.kill_time, kwargs={'obj_id': instance.id})

post_save.connect(temp_handler, sender=TempData)
