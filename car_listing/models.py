from django.db import models
from django.core.validators import (
    MinValueValidator, 
    MaxValueValidator,
    MaxLengthValidator
)
from django.forms import ValidationError

from auto_market.validators import validate_photo_size


class VehicleType(models.Model):
    title = models.CharField(max_length=4)
    
    def __str__(self):
        return self.title


class CarMake(models.Model):
    title = models.CharField(max_length=100)
    vehicle_types = models.ManyToManyField(
        VehicleType, related_name='car_make'
    )
    
    def __str__(self):
        return self.title
   

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    group_title = models.CharField(max_length=100)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title   
 

class CarCategory(models.Model):
    title = models.CharField(max_length=100)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    

class Feature(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class DriveType(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title


class Color(models.Model):
    color_code = models.CharField(max_length=7)
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    

class SaloonColor(models.Model):
    color_code = models.CharField(max_length=7)
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    
    
class SaloonMaterial(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title


class Location(models.Model):
    GROUP_CHOICES = [
        ('GE', 'Georgia'),
        ('SH', 'Shipping'),
        ('FR', 'Foreign'),
        ('OT', 'Other'),
    ] 
    
    group = models.CharField(
        max_length=2, 
        choices=GROUP_CHOICES, 
        blank=False, 
        null=False
    )
    flag = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title


class GearType(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    

class SteeringWheelType(models.Model):
    title = models.CharField(max_length=100)
    vehicle_type = models.ManyToManyField(
        VehicleType, related_name='gear_type'
    )
    
    def __str__(self):
        return self.title
    
    
class FuelType(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    

class MileageUnit(models.Model):
    title = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2)
    conversion_to_base = models.DecimalField(max_digits=7, decimal_places=5)
    base_unit = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
class DoorOption(models.Model):
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description
     

class CarMainFeatures(models.Model):    
    make = models.ForeignKey(
        CarMake, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    model = models.ForeignKey(
        CarModel, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
   
    category = models.ForeignKey(
        CarCategory, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    year = models.PositiveIntegerField(blank=False, null=False)
   
    registration_month = models.PositiveIntegerField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        blank=True,
        null=True
    )
    vin_code = models.CharField(max_length=17, blank=True)
    
    fuel_type = models.ForeignKey(
        FuelType, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    engine_volume = models.DecimalField(
        max_digits=5,  
        decimal_places=2,  
        validators=[
            MinValueValidator(0.05),  
            MaxValueValidator(15),   
        ],
        help_text="Engine volume in liters (between 0.05 and 15 liters)"
    )
    turbo = models.BooleanField(default=False)
    
    cylinders = models.PositiveIntegerField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        blank=False,
        null=False
    )
    mileage = models.PositiveIntegerField(blank=False, null=False)
    
    mileage_units = models.ForeignKey(
        MileageUnit, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    steering_wheel = models.ForeignKey(
        SteeringWheelType, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    transmission = models.ForeignKey(
        GearType, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    drive_wheels = models.ForeignKey(
        DriveType, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    doors = models.ForeignKey(
        DoorOption, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    catalyst = models.BooleanField(null=False, blank=False)
    
    airbags = models.PositiveIntegerField(
        choices=[(i, f"{i:02d}") for i in range(0, 13)],
        blank=False,
        null=False
    )
    
    color = models.ForeignKey(
        Color, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    saloon_material = models.ForeignKey(
        SaloonMaterial, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    
    saloon_color = models.ForeignKey(
        SaloonColor, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False
    )
    features = models.ManyToManyField(Feature, blank=True)
    description = models.TextField(
        blank=True, 
        validators=[MaxLengthValidator(5000)]
    )
    
    def __str__(self):
        return f"{self.make} {self.model} {self.year}"
    

class CarPrice(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('GEL', 'GEL'),
    ]
    
    price = models.PositiveIntegerField(blank=False, null=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  
    price_negotiable = models.BooleanField(default=False)  
    exchange_for_another_car = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.price} {self.currency}"
    
class CarListing(models.Model):
    author = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    main_features = models.OneToOneField(
        CarMainFeatures, 
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    is_cleared = models.BooleanField(default=False)
    is_inspected = models.BooleanField(default=False)
    price = models.ForeignKey(CarPrice, on_delete=models.CASCADE)
    photos = models.ManyToManyField('CarPhoto', blank=True)
    video_link = models.URLField(blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=False, null=False)
    contact_phone = models.CharField(max_length=15, blank=False, null=False)
    contact_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)  
        
    def save(self, *args, **kwargs):
        if self.photos.count() > 15:
            raise ValidationError("A maximum of 15 photos is allowed.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Car Listing {self.id} by {self.author}"
    
    
class CarPhoto(models.Model):
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='cars_photos/', 
        validators=[validate_photo_size]
    )

    def __str__(self):
        return f"Photo {self.id} for Car {self.car.id}"
        