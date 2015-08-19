from django.test import TestCase

from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from activities.models import Activity
import datetime
import time

from pprint import pprint
import json
import random
User = get_user_model()

class APIHeatMapTest(TestCase):
    
    def test_returns_heatmap_data(self):
        '''
        The heatmap directive has unusual
        requirements. The record_api_view function
        amalgamates checkins by their dates.
        '''
        user = User.objects.create(email='a@b.com', time_zone='America/Los_Angeles')
        now = datetime.datetime.now(datetime.timezone.utc)
        time1 = now - datetime.timedelta(hours=24)
        time2 = now - datetime.timedelta(hours=48)
        time3 = now - datetime.timedelta(hours=72)
        a1 = Activity.objects.create(user=user, name='test1', time=time1,
                                     completed=True,
                                     is_open=False)
        a2 = Activity.objects.create(user=user, name='test2', time=time1,
                                     completed=True,
                                     is_open=False)
        a3 = Activity.objects.create(user=user, name='test3', time=time2,
                                     completed=True,
                                     is_open=False)
        a4 = Activity.objects.create(user=user, name='test4', time=time3,
                                     completed=True,
                                     is_open=False)
        
        response = self.client.get('/api/records/' + str(user.id) + '/')
        result = json.loads(response._container[0].decode(encoding='UTF-8'))
        #writing a test to get the result value back is simply reimplementing
        #the algorithm. It's not a worthwhile test.
        #we'll test that the values are aggregated properly.
        self.assertEqual(len(random.choice(list(result.keys()))), 10)
        self.assertEqual(len(result),3)
        
        
        
        
        
