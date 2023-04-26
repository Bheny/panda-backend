from django.shortcuts import render
from rest_framework import viewsets 
from .serializers import PackageSerializer 
from .models import Package 

class PackageViewSet(viewsets.ModelViewSet):
    serializer_class = PackageSerializer 
    queryset = Package.objects.all()
