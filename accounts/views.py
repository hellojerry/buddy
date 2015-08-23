from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework import permissions, status, views, viewsets, generics
from rest_framework.response import Response

#remove this at production
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .permissions import IsOwnerOrReadOnly

from .serializers import UserSerializer, TempDataCreateSerializer
from .models import TempData
from pprint import pprint

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JSONWebTokenAuthentication, BasicAuthentication, SessionAuthentication]
    
    def get_permissions(self):
        print('get permissions')
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        elif self.request.method == 'POST':
            return (permissions.AllowAny(),)
        
        else:
            return (IsOwnerOrReadOnly(),)
        
    def create(self, request):
        new_name = request.data['email']
        request.data['username'] = new_name
        try:
            request.data['password']
        except:
            return Response({
                'status': 'Bad Request',
                'message': 'Password required.',
                'error': 'Password required.',
                })
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
        return Response({
            'status': 'bad request',
            'message': 'account could not be created with this data',
            'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)



    #switch this to CreateAPIView at deployment - this is for testing.
class TempDataCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TempDataCreateSerializer
    authentication_classes = [JSONWebTokenAuthentication, BasicAuthentication, SessionAuthentication]
    queryset = TempData.objects.all()
    
    def post(self, request, *args, **kwargs):
        self.request.data['user'] = kwargs.get('pk')
        
        '''
        First, eliminate empty post requests
        '''
        if len(request.data) < 2:
            return Response({
                'status': 'Bad Request',
                'message': 'At least one field required.'
                
                }, status=status.HTTP_400_BAD_REQUEST)
        '''
        then let move to empty strings for conditional fields.
        '''
        print('a')
        try:
            self.request.data['phone']
        except:
            self.request.data['phone'] = ''
        try:
            self.request.data['email']
        except:
            self.request.data['email'] = ''
        try:
            self.request.data['twitter_handle']
            print(self.request.data['twitter_handle'])
        except:
            self.request.data['twitter_handle'] = ''
        return self.create(request, *args, **kwargs)
    
def temp_data_verify(request, conf, cat):
    if cat == 'e':
        try:
            temp = TempData.objects.get(email_conf=conf)
            user = temp.user
            user.email = temp.email
            user.save()
            context = {'item': 'email'}
        except:
            raise Http404('No conf available!')
    elif cat == 't':
        try:
            temp = TempData.objects.get(twitter_conf=conf)
            user = temp.user
            user.twitter_handle = temp.twitter_handle
            user.save()
            print(user.twitter_handle)
            context = {'item': 'twitter handle'}
        except:
            raise Http404('No conf available!')
    elif cat == 'p':
        try:
            temp = TempData.objects.get(phone_conf=conf)
            user = temp.user
            user.phone = temp.phone
            user.save()
            context = {'item': 'phone number'}
        except:
            raise Http404('No conf available!')
    else:
        raise Http404('No conf available!')
    
    
    return render(request, 'confirm.html', context)
    