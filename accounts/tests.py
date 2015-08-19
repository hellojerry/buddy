from django.test import TestCase

from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
import datetime
from activities.models import Activity
from .models import TempData
from pprint import pprint
from unittest import skip

User = get_user_model()

class UserModelTest(TestCase):

    def test_model_modified_save(self):
        '''
        validation preventing multiple users with same name
        '''
        user1 = User.objects.create(email='a@b.com')
        self.assertEqual(user1.username, 'a@b.com')
    
    
    def test_longest_streak(self):
        user = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        yesterday = now - datetime.timedelta(hours=24)
        two_days =  now - datetime.timedelta(hours=48)
        three_days = now - datetime.timedelta(hours=72)
        five_days = now - datetime.timedelta(hours=120)
        six_days = now - datetime.timedelta(hours=144)
        a = Activity.objects.create(user=user, time=yesterday,
                                    completed=True, is_open=False, name='a')
        b = Activity.objects.create(user=user, time=two_days,
                                    completed=True, is_open=False, name='b')
        c = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='c')
        e = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='f')
        d = Activity.objects.create(user=user, time=five_days,
                                    completed=True, is_open=False, name='d')
        j = Activity.objects.create(user=user, time=six_days,
                            completed=True, is_open=False, name='j')
        #should be equal to three days
        self.assertEqual(user.longest_streak, 3)
        
    def test_longest_streak_with_incomplete(self):
        user = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        yesterday = now - datetime.timedelta(hours=24)
        two_days =  now - datetime.timedelta(hours=48)
        three_days = now - datetime.timedelta(hours=72)
        five_days = now - datetime.timedelta(hours=120)
        six_days = now - datetime.timedelta(hours=144)
        a = Activity.objects.create(user=user, time=yesterday,
                                    completed=True, is_open=False, name='a')
        b = Activity.objects.create(user=user, time=two_days,
                                    completed=False, is_open=False, name='b')
        c = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='c')
        e = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='f')
        d = Activity.objects.create(user=user, time=five_days,
                                    completed=True, is_open=False, name='d')
        j = Activity.objects.create(user=user, time=six_days,
                            completed=True, is_open=False, name='j')
        self.assertEqual(user.longest_streak, 2)
    
    def test_current_streak(self):
        user = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        yesterday = now - datetime.timedelta(hours=24)
        two_days =  now - datetime.timedelta(hours=48)
        three_days = now - datetime.timedelta(hours=72)
        five_days = now - datetime.timedelta(hours=120)
        a = Activity.objects.create(user=user, time=yesterday,
                                    completed=True, is_open=False, name='a')
        b = Activity.objects.create(user=user, time=two_days,
                                    completed=True, is_open=False, name='b')
        c = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='c')
        e = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='f')
        d = Activity.objects.create(user=user, time=five_days,
                                    completed=True, is_open=False, name='d')

        #result should be three days
        self.assertEqual(user.current_streak, 3)
        
    def test_current_streak_with_incomplete(self):
        user = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        yesterday = now - datetime.timedelta(hours=24)
        two_days =  now - datetime.timedelta(hours=48)
        three_days = now - datetime.timedelta(hours=72)
        four_days = now - datetime.timedelta(hours=96)
        five_days = now - datetime.timedelta(hours=120)
        a = Activity.objects.create(user=user, time=yesterday,
                                    completed=True, is_open=False, name='a')
        b = Activity.objects.create(user=user, time=two_days,
                                    completed=True, is_open=False, name='b')
        c = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='c')
        e = Activity.objects.create(user=user, time=three_days,
                                    completed=True, is_open=False, name='f')
        f = Activity.objects.create(user=user, time=four_days,
                                    completed=False, is_open=False, name='g')
        d = Activity.objects.create(user=user, time=five_days,
                                    completed=True, is_open=False, name='d')
        self.assertEqual(user.current_streak, 3)
    
    def test_current_streak_nothing_today(self):
        user = User.objects.create(email='a@b.com')
        now = datetime.datetime.now(datetime.timezone.utc)
        two_days = now - datetime.timedelta(hours=48)
        a = Activity.objects.create(user=user, time=two_days,
                                    completed=True, is_open=False, name='a')

        self.assertEqual(user.current_streak, 0)
    



class UserViewSetTest(APITestCase):
    
    def test_user_registration_no_pw_throws_error(self):
        response = self.client.post('/api/users/',
                                    data = {
                                        'email': 'a@b.com'
                                    })
        self.assertEqual(response.data['error'],
                         'Password required.')
        
    def test_user_registration_with_pw(self):
        '''
        testing user creation without username.
        '''
        
        response = self.client.post('/api/users/',
                                    data = {
                                        'email': 'a@b.com',
                                        'password': 'abcd'
                                        })
        self.assertEqual(User.objects.all().first().username, 'a@b.com')
        

    def test_dupe_email(self):
        a = User.objects.create(email='a@b.com')
        response = self.client.post('/api/users/',
                                    data= {'email': 'a@b.com',
                                    'password': 'defg'})
        self.assertIn('account could not be created', response.data['message'])
        
        
class LoginTest(APITestCase):
    
    def test_modified_JWT_payload(self):
        '''
        A lot of the front-end makes kwargs
        to the API, and routes calls based upon
        a user id. We need a modified payload
        to account for this.
        '''
        
        user = self.client.post('/api/users/',
                                data = {
                                    'email': 'a@b.com',
                                    'password': 'abcd'
                                })
        self.assertEqual(User.objects.all().first().email, 'a@b.com')
        response = self.client.post('/api/auth/login/',
                                    data = {
                                        'email': 'a@b.com',
                                        'password': 'abcd'
                                    })
        self.assertEqual(response.data['user_id'], 1)
        self.assertEqual(response.data['username'], 'a@b.com')
        

class TempDataModelTest(TestCase):
    
    def test_save_functionality(self):
        user = User.objects.create(email='a@b.com')
        #b = TempData.objects.create(user=a)
        with self.assertRaises(ValueError):
            TempData.objects.create(user=user)

    #turn off skipping when celery is up.

    @skip
    def test_save_func_with_celery(self):
        user = User.objects.create(email='a@b.com')
        b = TempData.objects.create(user=user, phone='4259237012')
        self.assertEqual(TempData.objects.all().first().phone, '4259237012')
        

class TempDataCreateViewTest(APITestCase):
    
    def test_empty_post_throws_error(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/users/'+ str(user.id) + '/createtemp/',
                                    data = {})
        #print(response.data)
        self.assertIn('At least one field required.', response.data['message'])
        self.assertIn('Bad Request', response.data['status'])
    
    #turn off skipping when celery is up.
    
    @skip
    def test_post_creates_conf(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/users/' + str(user.id) + '/createtemp/',
                                    data = {
                                        'phone': '4259237012'
                                    })
        self.assertEqual(len(TempData.objects.all().first().phone_conf), 10)
    
class TempDataConfirmTest(TestCase):
    
    def test_raises_404_for_no_conf(self):
        response = self.client.get('/confirm/abcdefg/p/')
        self.assertEqual(response.status_code, 404)
        
    def test_updates_phone_with_conf(self):
        user = User.objects.create(email='a@b.com')
        temp = TempData.objects.create(user=user, phone='2234567890')
        response = self.client.get('/confirm/' + str(temp.phone_conf) + '/p/')
        self.assertEqual(User.objects.all().first().phone, '2234567890')
        
    def test_updates_email_with_conf(self):
        user = User.objects.create(email='a@b.com')
        temp = TempData.objects.create(user=user, email='b@c.com')
        response = self.client.get('/confirm/' + str(temp.email_conf) + '/e/')
        self.assertEqual(User.objects.all().first().email, 'b@c.com')
        
        
    def test_updates_twitter_with_conf(self):
        user = User.objects.create(email='a@b.com')
        temp = TempData.objects.create(user=user, twitter_handle='b')
        response = self.client.get('/confirm/' + str(temp.twitter_conf) + '/t/')
        self.assertEqual(User.objects.all().first().twitter_handle, 'b')
    
    
    def test_proper_template_used(self):
        user = User.objects.create(email='a@b.com')
        temp = TempData.objects.create(user=user, phone='2234567890')
        response = self.client.get('/confirm/' + str(temp.phone_conf) + '/p/')
        self.assertTemplateUsed(response, 'confirm.html')
