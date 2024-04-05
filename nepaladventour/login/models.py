from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class profile(AbstractUser):
    fullname = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    connect = models.CharField(max_length=10, choices=[('no', 'No'), ('yes', 'Yes')])
    social_media = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='hotel_pics/')

    def __str__(self):
        return self.name

class HotelReview(models.Model):
    description = models.TextField()
    rating = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return f'Review by {self.user.username} for {self.hotel.name}'

class Activity(models.Model):
    name = models.CharField(max_length=255)
    age_required = models.PositiveIntegerField()
    contact = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='activity_pics/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    place = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ActivityReview(models.Model):
    description = models.TextField()
    rating = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f'Review by {self.user.username} for {self.activity.name}'

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Recommendation for {self.user.username}'