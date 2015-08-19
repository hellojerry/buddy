from django.test import TestCase

from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
import datetime
from activities.models import Activity

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
    pass
        
