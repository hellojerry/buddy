from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime

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
    
