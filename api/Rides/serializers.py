from rest_framework import serializers

from .models import Request, Ride

from Profiles.serializers import ProfileSerializer


class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride 
        fields = "__all__"
    
class SearchRideSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date  = serializers. DateField()
    start_time  = serializers.TimeField()
    end_time = serializers.TimeField()
    start_location  = serializers.CharField()
    stop_location  = serializers.CharField()

    class Meta:
        model = Ride 
        fields = '__all__'
        depth = 3
        search_fields = ['start_location', 'stop_location','start_date','stop_date','start_time','stop_time'] # specify fields to use for search
        lookup_fields = ['id'] # specify fields to use for lookup

class RideSerializer(serializers.ModelSerializer):
    pending_requests = serializers.SerializerMethodField()
    
    class Meta:
        model = Ride 
        fields = ['id','departure_name','destination_name','conditions','price','seats','passengers','is_active','creator','date','time','created_on','updated_on','pending_requests']
        depth = 3

    def get_pending_requests(self, obj):
        requests = obj.get_pending_requests()
        serializer = ProfileSerializer(requests, many=True)
        return serializer.data


class UpdateRideDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        


class RequestSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(default=False)
    class Meta:
        model = Request 
        fields = "__all__"
        depth = 3
        extra_kwargs = {
                       'request_id': {'read_only':True},
                       'seen': {'read_only':True},
                    #  'is_approved': {'read_only':True},
                       }

class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request 
        fields = ('seats','is_approved','seen','ride','passenger')
        extra_kwargs = {
                       'seen': {'read_only':True},
                       'is_approved': {'read_only':True},
                       }





class RequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request 
        fields = "__all__"
        depth = 3
