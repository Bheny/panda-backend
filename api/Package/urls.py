from django.urls import path, include 
from rest_framework import routers 
from .views import PackageViewSet


router = routers.DefaultRouter() 
router.register('', PackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]