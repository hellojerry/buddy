from django.shortcuts import render

from .serializers import UserStreakSerializer

from django.http import JsonResponse

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from buddy.permissions import IsOwnerOrReadOnly

from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
import time
from datetime import datetime
import pytz
from django.contrib.auth import get_user_model
from activities.models import Activity

User = get_user_model()


class UserStreakAPIView(generics.RetrieveAPIView):
    authentication_classes = [JSONWebTokenAuthentication,
                              BasicAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserStreakSerializer
    queryset = User.objects.all()


def record_api_view(request, pk):
    '''
    This reformats a user's streak data into a format
    that 1) the cal-heatmap JS module can read
    2) takes into account user local time.
    '''
    user_id = pk
    local_tz = pytz.timezone(User.objects.get(id=user_id).time_zone)
    offset_amt = local_tz.utcoffset(datetime.now()).total_seconds()
    activities = Activity.objects.filter(
        user__id=user_id).filter(is_open=False).filter(completed=True)

    l = {}

    for i in activities:
        server_time = time.mktime(i.time.date().timetuple())
        local_time = server_time - offset_amt

        b = str(local_time)[:-2]

        try:
            l[b] += 1
        except:
            l[b] = 1

    return JsonResponse(l)
