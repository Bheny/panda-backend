from django.db import IntegrityError, models
from Profiles.models import Profile

from .services import *


# Create your models here.
class Ride(models.Model):
    departure_name= models.CharField(max_length=200, blank=True)
    destination_name= models.CharField(max_length=200, blank=True)
    departure_long= models.CharField(max_length=200, blank=True)
    destination_lat=   models.CharField(max_length=200, blank=True)
    conditions= models.TextField(blank=True)
    price= models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    seats= models.PositiveIntegerField(default=1)
    passengers = models.ManyToManyField(Profile, blank=True)
    is_active= models.BooleanField(default=True)  
    creator = models.ForeignKey(Profile, related_name="ride_creator", on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} to {}, created by {}'.format(self.departure_name,self.destination_name,self.creator.user.username)

    def get_pending_requests(self):
        passengers = []
        pending = self.request.filter(is_approved=False)
        for request in pending:
            passengers.append(request.passenger)
        return passengers
    


class Request(models.Model):
    request_id = models.CharField(max_length=100, unique=True)
    ride = models.ForeignKey(Ride, related_name="request", on_delete=models.CASCADE)
    passenger = models.ForeignKey(Profile, related_name="requests", on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(default="1")
    is_approved = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_id 
    

    def save(self, *args, **kwargs):
        #generate unique request id 
        if not self.request_id:
            self.request_id = unique_request_id_generator(self)
        # print(dir(self.ride.passengers))
        #add ppassengers
        
        if self.is_approved and self.ride.seats > 0:
            self.ride.passengers.add(self.passenger) #adds the approved requests passenger to the passengers of the ride.
         
            print(self.ride.passengers)
            self.ride.seats -= self.ride.passengers.count() # subtracts the total number of passengers on a ride from the seat number
            self.ride.save() # saves changes

        try:
            super(Request, self).save(*args, **kwargs)
        except IntegrityError:
            raise IntegrityError



