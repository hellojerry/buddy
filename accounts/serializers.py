from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import TempData
from buddy.keys import EMAIL_HOST_USER, SITE_URL

from django.template.loader import render_to_string

from comms.tasks import make_text, private_message, send_email

from django.core.mail import send_mail

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'created_at',
            'updated_at',
            'phone',
            'is_admin',
            'password',
            'twitter_handle',
            'time_zone',
            'tweet',
            'call',
            'text',
            'email_me'
        ]
        read_only_fields = ('created_at', 'updated_at', 'is_admin',)
        
    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
      
    def update(self, instance, validated_data):

        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        print(validated_data)
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class TempDataCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    phone = serializers.CharField(allow_blank=True, required=False)
    twitter_handle = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    
    class Meta:
        model = TempData
        fields = [
            'user',
            'phone',
            'email',
            'twitter_handle'
        ]
        
    def create(self, validated_data):
        temp = TempData(phone=validated_data['phone'],
                        user=validated_data['user'],
                        twitter_handle=validated_data['twitter_handle'],
                        email=validated_data['email']
        )
        temp.save()
        '''
        trigger confirmation email.
        '''
        if temp.email != '':
            from_email = 'mikesdjangosite@gmail.com'
            to_email = temp.email
            subject = 'Accountabillibuddy Email Address Change'
            
            context = {
                'email_conf': temp.email_conf
            }
            msg_plain = render_to_string('conf_email.txt', context)
            msg_html = render_to_string('conf_email.html', context)

            send_email.apply_async(eta=datetime.now(), kwargs={
                'temp_email': temp.email,
                'email_conf':temp.email_conf,

            })
        
        if temp.phone != '':
            message = '''
            ABB: Phone number changed.
            Click here to confirm:
            http://%s/confirm/%s/p/
            Please ignore if in error.
            ''' %(SITE_URL, temp.phone_conf)
            
            ##IMPORT MAKE_TEXT FROM COMMS.TASKS
            make_text.apply_async(eta=datetime.now(), kwargs={
                'phone': temp.phone,
                'message': message
                })
        if temp.twitter_handle != '':

            private_message.apply_async(eta=datetime.now(), kwargs={
                'recipient': temp.twitter_handle,
                'conf': temp.twitter_conf,
                })
        return temp
            