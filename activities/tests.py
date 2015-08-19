from django.test import TestCase

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from .models import Activity

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import datetime

from pprint import pprint

User = get_user_model()

class ActivityModelTest(TestCase):
    
    def test_offset_func(self):
        '''
        server is set to UTC. Los angeles to UTC is 7 hours.
        Items need to be transformed to user local time at rendering.
        '''
        
        a = User.objects.create(email='a@b.com', time_zone='America/Los_Angeles')
        act = Activity.objects.create(time=datetime.datetime.now(), user=a, name='test')
        self.assertEqual(act.time - datetime.timedelta(hours=7), act.local_time)
        
    def test_weekday_conversion(self):
        a = User.objects.create(email='a@b.com', time_zone='America/Los_Angeles')
        '''
        6 am UTC is a Tuesday.
        In Los Angeles time, thats a Monday.
        The method should return local times.
        '''
        act = Activity.objects.create(time=datetime.datetime(2015,8, 18, 6, 0, 0),
                                      name='test', user=a)
        self.assertEqual(act.day_of_week, 'Monday')

    def test_editable_threshhold(self):
        '''
        We don't want activities editable within
        1 day of them being due.
        '''
        a = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        in_18 = now + datetime.timedelta(hours=18)
        act = Activity.objects.create(time=in_18, name='test', user=a)
        self.assertFalse(act.editable)
        
    def test_still_editable(self):
        a = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        in_36 = now + datetime.timedelta(hours=36)
        act = Activity.objects.create(time=in_36, name='test', user=a)
        self.assertTrue(act.editable)
        
class ActivityViewTests(APITestCase):
    

    
    
    def test_activity_creation(self):
        user = User.objects.create(email='a@b.com', time_zone='America/Los_Angeles')
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/activities/' + str(user.id) + '/',
                                    data = {
                                    'day_of_week': 'Tuesday',
                                    'name': 'test',
                                    'provided_time': '08:00',
                                    'user': user.id
                                    })

        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(Activity.objects.all().first().name, 'test')
        self.assertEqual(Activity.objects.all().first().time - datetime.timedelta(hours=7),
              Activity.objects.all().first().local_time)
        
    def test_activity_update(self):
        user = User.objects.create(email='a@b.com', time_zone='America/Los_Angeles')
        self.client.force_authenticate(user=user)
        
        orig = self.client.post('/api/activities/' + str(user.id) + '/',
                                    data = {
                                    'day_of_week': 'Tuesday',
                                    'name': 'test',
                                    'provided_time': '08:00',
                                    'user': user.id
                                    })
        self.assertEqual(Activity.objects.all().first().time.hour, 15)
        self.assertEqual(Activity.objects.all().first().name, 'test')
        response = self.client.put('/api/activities/' + str(user.id) + '/'
                                   + '1' + '/',
                    data = {
                        'provided_time': '15:00',
                        'user': user.id,
                        'day_of_week': 'Tuesday',
                        'name': 'newtest'
                        })
        force_authenticate(response, user=user)
        self.assertEqual(Activity.objects.all().first().time.hour, 22)
        self.assertEqual(Activity.objects.all().first().name, 'newtest')
        
class CheckInTests(APITestCase):
    
    def test_checkin_grabs_proper_item(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_authenticate(user=user)
        now = datetime.datetime.now(datetime.timezone.utc)
        in_10 = now + datetime.timedelta(minutes=10)
        activity = Activity.objects.create(name='test', user=user, time=in_10)
        response = self.client.get('/api/users/checkin/' + str(user.id) + '/')
        force_authenticate(response, user=user)
        self.assertEqual(response.data['name'], 'test')
        
    def test_checkin_displays_empty(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_authenticate(user=user)
        now = datetime.datetime.now(datetime.timezone.utc)
        in_100 = now + datetime.timedelta(minutes=100)
        activity = Activity.objects.create(name='test', user=user, time=in_100)
        response = self.client.get('/api/users/checkin/' + str(user.id) + '/')
        self.assertIn('Try later!', response.data['message'])
        
        
    def test_checkin_checks_out_on_post(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_authenticate(user=user)
        now = datetime.datetime.now(datetime.timezone.utc)
        in_10 = now + datetime.timedelta(minutes=10)
        activity = Activity.objects.create(name='test', user=user, time=in_10)
        response = self.client.patch('/api/users/checkin/' + str(user.id) + '/',
                                     data = {
                                     'is_open': False,
                                     'completed': True
                                     })
        force_authenticate(response, user=user)

        self.assertEqual(Activity.objects.all().first().completed, True)
        self.assertEqual(Activity.objects.all().first().is_open, False)
                                           
        
        