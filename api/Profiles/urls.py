from django.urls import path, include
from rest_framework import routers 
from .views import *

router = routers.DefaultRouter() 
router.register('', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', ProfileList.as_view(), name='view_profiles'),
    # path('detail/<int:pk>', ProfileDetail.as_view(), name='view_profiles'),
    # path('update/<int:pk>', UpdateProfileDetail.as_view(), name='update profiles'),
    path('driver/apply/',Driver_Application.as_view(), name='apply'),
   
]