from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model

import datetime
import pytz

from .models import Activity

User = get_user_model()


def next_weekday(day, weekday):
    days_ahead = weekday - day.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return day + datetime.timedelta(days_ahead)

available = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    provided_time = serializers.CharField(max_length=20)
    day_of_week = serializers.CharField(max_length=10)
    editable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id',
            'user',
            'name',
            'time',
            'local_time',
            'provided_time',
            'day_of_week',
            'editable'
        ]

        read_only_fields = ('time', 'id', 'user', 'editable',)

        # The create and update methods convert between
        # server time and user timezones.

    def create(self, validated_data):
        user = validated_data['user']
        name = validated_data['name']
        provided_time = validated_data['provided_time']
        weekday = validated_data['day_of_week']

        # lookup the next available day and assign that weekday to it.
        day = available[weekday]
        today = datetime.datetime.now(pytz.UTC)
        schedule_date = next_weekday(today, day)
        schedule_time = datetime.datetime.strptime(provided_time, '%H:%M')
        hour = schedule_time.hour
        minute = schedule_time.minute
        final_time = schedule_date.replace(hour=hour, minute=minute,
                                           second=0, microsecond=0)
        # the next available date and time are in UTC, so we need to
        # factor in the user's offset and save it at the proper time.
        local_tz = pytz.timezone(user.time_zone)
        offset_amt = local_tz.utcoffset(datetime.datetime.now())
        final_time -= offset_amt

        return Activity.objects.create(user=user, name=name,
                                       time=final_time, is_open=True)

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update',
                                                  self, validated_data)
        provided_time = validated_data['provided_time']
        weekday = validated_data['day_of_week']
        try:
            day = available[weekday]
        except KeyError:
            print("That's not a valid day.")
        today = datetime.datetime.now(pytz.UTC)
        schedule_date = next_weekday(today, day)
        schedule_time = datetime.datetime.strptime(provided_time, '%H:%M')
        hour = schedule_time.hour
        minute = schedule_time.minute
        final_time = schedule_date.replace(hour=hour, minute=minute,
                                           second=0, microsecond=0)

        local_tz = pytz.timezone(validated_data['user'].time_zone)
        offset_amt = local_tz.utcoffset(datetime.datetime.now())
        final_time -= offset_amt
        validated_data['time'] = final_time
        validated_data.pop('provided_time', None)
        validated_data.pop('day_of_week', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CheckInSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Activity
        fields = [
            'id',
            'user',
            'name',
            'completed',
            'time',
            'is_open',
            'local_time'
        ]
        read_only_fields = ('id', 'user', 'name', 'time')
