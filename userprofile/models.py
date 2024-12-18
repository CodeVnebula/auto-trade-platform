from django.db import models
from django.conf import settings


class CompareListings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_listings = models.ManyToManyField(
        'car_listing.CarListing', related_name='compare_listings'
    )
    
    def __str__(self):
        return self.user.firstname
    
class FacouriteListings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_listings = models.ManyToManyField(
        'car_listing.CarListing', related_name='favourite_listings'
    )
    
    def __str__(self):
        return self.user.firstname