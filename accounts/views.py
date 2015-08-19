from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, status, views, viewsets, generics
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from buddy.permissions import IsOwnerOrReadOnly

from .serializers import UserSerializer


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JSONWebTokenAuthentication,]
    
    def get_permissions(self):
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