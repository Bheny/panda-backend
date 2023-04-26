from django.db import models
from Profiles.models import Profile


class Package(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    weight = models.FloatField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} created by {self.user.username}'