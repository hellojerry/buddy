from django.shortcuts import render

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework import viewsets, serializers, permissions, mixins, status, generics
from rest_framework.response import Response

from buddy.permissions import IsOwnerOrReadOnly
from .serializers import ActivitySerializer, CheckInSerializer
from .models import Activity
from django.contrib.auth import get_user_model

import datetime
import pytz

User = get_user_model()


class ActivityViewSet(viewsets.ModelViewSet):
    authentication_classes = [JSONWebTokenAuthentication,
                              SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Activity.objects.filter(
            user__id=user_id).filter(
            is_open=True).filter(completed=False)


class CheckInAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication,
                              SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CheckInSerializer

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        now = datetime.datetime.now(pytz.UTC)
        back_bound = now - datetime.timedelta(hours=1)
        front_bound = now + datetime.timedelta(hours=1)
        obj = Activity.objects.filter(user=user).filter(
            is_open=True).filter(completed=False).filter(
            time__gte=back_bound).filter(
            time__lte=front_bound).first()

        if obj is not None:
            return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({
                'status': 'Nothing available',
                'message': 'There are no checkins at this time. Try later!'
                })
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
