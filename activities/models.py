from django.db import models
from django.contrib.auth import get_user_model

import pytz
from datetime import datetime, timezone

from accounts.models import User

class Activity(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    time = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['time']
        
    @property
    def provided_time(self):
        '''
        This is a blank field for the serializer.
        '''
        return None
        
    @property
    def local_time(self):
        local_tz = pytz.timezone(self.user.time_zone)
        offset_amt = local_tz.utcoffset(datetime.now())
        local = self.time + offset_amt
        return local
    
    @property
    def day_of_week(self):
        '''
        to convert from datetime notation
        to human-readable for serializer.
        '''
        
        weekday = str(self.local_time.weekday())
        available = {
            '0':'Monday',
            '1':'Tuesday',
            '2':'Wednesday',
            '3':'Thursday',
            '4':'Friday',
            '5':'Saturday',
            '6':'Sunday',
        }
        return available[weekday]
    
    @property
    def editable(self):
        '''
        We don't want anything editable within 1 day.
        '''
        now = datetime.now(timezone.utc)

        if (self.time - now).total_seconds() <= 86400:

            return False
        else:
            return True
        
    
    def __str__(self):
        return self.name