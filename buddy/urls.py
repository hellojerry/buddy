"""buddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from accounts.views import UserViewSet, TempDataCreateAPIView
from activities.views import ActivityViewSet, CheckInAPIView
from .views import BaseView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'activities/(?P<user_id>\d+)', ActivityViewSet, 'Activity')

urlpatterns = [
    url(r'^api/auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^rest-framework/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/users/checkin/(?P<pk>\d+)/$', CheckInAPIView.as_view(), name='checkin'),
    url(r'^api/users/(?P<pk>\d+)/createtemp/$', TempDataCreateAPIView.as_view(), name='create_temp'),
    url(r'confirm/(?P<conf>[\w-]+)/(?P<cat>[tep])/$', 'accounts.views.temp_data_verify', name='verify'),
    url(r'^api/records/(?P<pk>\d+)/$', 'analytics.views.record_api_view', name='records'),
    url(r'^api/calls/call_data/$', 'comms.views.call_response', name='call_response'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^.*$', BaseView.as_view()), 
    
    
]
