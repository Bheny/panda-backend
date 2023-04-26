import datetime

from django.http import Http404
from Profiles.models import Profile
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Request, Ride
from .serializers import *


class RideSearch(generics.ListAPIView):
    """


        This end points take the following parameters:
        start_date
        end_date 
        start_time 
        end_time
        start_location 
        stop_location 

        ensure that you are sendinng a time and date no matter what.
        if the user does not input them your frontend should fetch their current time and date and fix
        it in
        {
            "start_date": ",
            "end_date" : ",
            "start_time" : ",
            "end_time": ",
            "start_location" : ",
            "stop_location" : "
        }
    """
    serializer_class = SearchRideSerializer

    def get(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        start_location = self.request.query_params.get('departure_name')
        stop_location = self.request.query_params.get('destination_name')

        queryset = Ride.objects.filter(departure_name__iexact=start_location, destination_name__iexact=stop_location)
        # Convert input strings to datetime objects
        if start_date and start_time and end_date and end_time:
            start_datetime = datetime.datetime.strptime(start_date + start_time, '%Y-%m-%d%H:%M')
            end_datetime = datetime.datetime.strptime(end_date + end_time, '%Y-%m-%d%H:%M')
            queryset.filter(date__range=(start_datetime.date(), end_datetime.date()), time__range=(start_datetime.time(), end_datetime.time()))
        
        
        return queryset


class CreateRide(generics.GenericAPIView):
    serializer_class = CreateRideSerializer 

    def post(self, request):
        #accepts and stores 
        serializer = CreateRideSerializer(data=request.data)
        profile = Profile.objects.get(id=request.data['creator'])
        print(profile)
        if serializer.is_valid():
            if profile.is_driver:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':"The creator of this ride is not a verified driver",}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideList(generics.GenericAPIView):
    """
    List all Rides or create new Rides
    """
    serializer_class = RideSerializer   
    def get(self, request):
        #get the ride for booking
        Rides = Ride.objects.all().order_by('-created_on')
        serializer = RideSerializer(Rides, many=True)
        return Response(serializer.data)

class RideDetail(generics.GenericAPIView):
    """
    Retrive, update or delete Ride
    """
    serializer_class = RequestSerializer

    def get_object(self, pk):
        try:
            return Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        Ride = self.get_object(pk)
        serializer = RideSerializer(Ride)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer_class = RideSerializer
        Ride = self.get_object(pk)
        serializer = RideSerializer(Ride, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk):
        Ride = self.get_object(pk)
        Ride.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class CreateRequest(generics.GenericAPIView):
    serializer_class = CreateRequestSerializer 

    def post(self, request):
        #accepts and stores 
        serializer = CreateRequestSerializer(data=request.data)
        # get the current request if it already exists
        try:
            request = Request.objects.get(ride=request.data["ride"], passenger=request.data['passenger'])
            serializer = RequestSerializer(request)
            data = {
                'message':"A request with this passenger already exists",
                'request': serializer.data
            }
            return Response(data)
        except Request.DoesNotExist:
            if serializer.is_valid():
                ride = Ride.objects.get(id=serializer.validated_data["ride"].id)
                # print(ride.passengers.contains(serializer.validated_data["passenger"]))
                if ride.passengers.filter(id=serializer.validated_data["passenger"].id).exists():
                    return Response({"message":"You are already a passenger on this list"})
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class RequestList(generics.GenericAPIView):
    """
    List all Request  Requests
    """
    serializer_class = RequestDetailSerializer   
    def get(self, request, pk=None, driver_id=None):
        serializer_class = RequestSerializer 
        #get the ride for booking
        Requests = Request.objects.all()
        if pk:
            Requests = Requests.filter(passenger__id=pk)
        elif driver_id:
            Requests = Requests.filter(ride__creator__id=driver_id)
        serializer = RequestSerializer(Requests, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     #accepts and stores 
    #     serializer = CreateRequestSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDetail(generics.GenericAPIView):
    """
    Retrive, update or delete Request
    """
    serializer_class = RequestSerializer
    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        Request = self.get_object(pk)
        serializer = RequestSerializer(Request)
        return Response(serializer.data)

    def put(self, request, pk):
        Request= self.get_object(pk)
        serializer = RequestSerializer(Request, data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            #Before data gets saved check if the passenger is not already approved
            print(Profile.objects.get(id=serializer.data['passenger']))
            if Request.ride.passengers.contains(Profile.objects.get(id=serializer.data['passenger'])):
                return Response({"message":"You are already a passenger on this list"})
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Request = self.get_object(pk)
        Request.delete()
        return Response(status.HTTP_204_NO_CONTENT)



class RequestApproval(APIView):
    """
    Retrive, update or delete Request
    """
    def post(self, request, pk):

        try:
            request= Request.objects.get(pk=pk)
            #checks if ride is not already approved .. if not aprove and save
            if not request.is_approved:
                request.is_approved = True 
                request.save()
                serializer =  RequestSerializer(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("This request has already been approved", status=status.HTTP_201_CREATED)
        except Request.DoesNotExist:
            raise Http404
        

class RequestCancel(APIView):
    """
    Retrive, update or delete Request
    """
    def post(self, request, pk):

        try:
            request= Request.objects.get(pk=pk)
            # ensure that the ride being cancelled belongs to the user performing the cancellation
            #checks if ride is not already approved .. if not aprove and save
            if not request.is_cancelled:
                request.is_cancelled = True 
                request.save()
                serializer =  RequestSerializer(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("This request has already been approved", status=status.HTTP_201_CREATED)
        except Request.DoesNotExist:
            raise Http404


class RequestCompleted(APIView):
    """
    Complete Request
    """
    def post(self, request, pk):

        try:
            request= Request.objects.get(pk=pk)
            # ensure that the ride being cancelled belongs to the user performing the cancellation
            #checks if ride is not already approved .. if not aprove and save
            if not request.is_completed:
                request.is_completed = True 
                request.save()
                serializer =  RequestSerializer(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("This request has already been approved", status=status.HTTP_201_CREATED)
        except Request.DoesNotExist:
            raise Http404
