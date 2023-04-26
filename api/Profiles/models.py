from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 


class Account(models.Model):
    title= models.CharField(max_length=100)
    description= models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)




class Profile(models.Model):
    image = models.ImageField(upload_to='images/profile/', blank=True)
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    phone = models.CharField(max_length=50, blank=True)
    is_driver = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def get_all_cars(self):
        cars = self.vehicle.all()
        return cars

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # print(instance.phone)
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)



class Driver_Application(models.Model):
    applicant  = models.ForeignKey(Profile, related_name="applicant_profile", on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} is requesting for Driver Verification..'.format(self.applicant.user.username)
    

class Driver(models.Model):
    profile = models.OneToOneField(Profile, related_name="Driver", on_delete=models.CASCADE)
    passport = models.ImageField(upload_to="driver/passport/", blank=True)
    id_card_front = models.ImageField(upload_to="driver/id_cards/", blank=True)
    id_card_back = models.ImageField(upload_to="driver/id_cards/", blank=True)



    def __str__(self):
        return f"{self.profile.user.username}'s Driver Info"
