from rest_framework import serializers
from .models import Profile, Driver_Application
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User 
        fields = ['id','username','first_name','last_name']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    cars = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','username','email','first_name','last_name','phone','bio','image','is_driver','is_verified','created_on','updated_on','cars']  

    def get_cars(self, obj):
        if obj.is_driver:
            cars = obj.get_all_cars()
            return VehicleSerializer(cars, many=True).data
        else: 
            return None


        
    def update(self, instance, validated_data):
        print("updating...", validated_data, instance)
        if instance.user or instance.user != None:
            print("fetching...")
            instance.user.first_name = validated_data.get('user').get('first_name')
            instance.user.last_name =  validated_data.get('user').get('last_name')
            instance.user.save()
        instance.bio =  validated_data.get('bio',instance.bio)

         # Handle image field separately
        image = validated_data.get('image', None)
        if image:
            instance.image.delete()  # delete old image if it exists
            instance.image = image

        instance.save()
        return instance

class DriverApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Application 
        fields = '__all__'