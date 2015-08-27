
from django.conf.urls import include, url
from django.contrib import admin

from accounts.views import UserViewSet, TempDataCreateAPIView
from activities.views import ActivityViewSet, CheckInAPIView
from analytics.views import UserStreakAPIView
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
    url(r'^api/users/streaks/(?P<pk>\d+)/$',UserStreakAPIView.as_view(), name='streaks'),
    url(r'^confirm/(?P<conf>[\w-]+)/(?P<cat>[tep])/$', 'accounts.views.temp_data_verify', name='verify'),
    url(r'^api/records/(?P<pk>\d+)/$', 'analytics.views.record_api_view', name='records'),
    url(r'^api/calls/call_data/$', 'comms.views.call_response', name='call_response'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^.*$', BaseView.as_view()), 
    
    
]
