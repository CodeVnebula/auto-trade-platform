import datetime
import random
from django.core.mail import send_mail
from django.conf import settings

from django.core.validators import EmailValidator

from rest_framework import serializers
from .models import (
    CarListing, CarCategory, CarMake, CarModel, Feature, DriveType, 
    Color, SaloonColor,  SaloonMaterial, Location, GearType,
    SteeringWheelType, FuelType, MileageUnit, DoorOption,
    CarMainFeatures, CarPrice, CarPhoto
)
from authentication.models import EmailConfirmation
from rest_framework.exceptions import ValidationError
from authentication.models import User

from drf_yasg import openapi
from authentication.serializers import UserInfoSerializer, ConfirmationCodeSerializer


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'title']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'title']
        

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'title']
        

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title']
        

class DriveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveType
        fields = ['id', 'title']
        

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'title', 'color_code']


class SaloonColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaloonColor
        fields = ['id', 'title', 'color_code']


class SaloonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaloonMaterial
        fields = ['id', 'title', 'type']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'title', 'group', 'flag']
        

class GearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearType
        fields = ['id', 'title']
        

class SteeringWheelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteeringWheelType
        fields = ['id', 'title']
        

class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = ['id', 'title']


class MileageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageUnit
        fields = ['id', 'title', 'abbreviation', 'conversion_to_base', 'base_unit']
        

class DoorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorOption
        fields = ['id', 'description']
        

class CarMainFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMainFeatures
        fields = [
            'make', 'model', 'category', 'year', 'registration_month', 
            'vin_code', 'fuel_type', 'engine_volume', 'turbo', 'cylinders', 
            'mileage', 'mileage_units', 'steering_wheel', 'transmission', 
            'drive_wheels', 'doors', 'catalyst', 'airbags', 'color', 
            'saloon_material', 'saloon_color', 'features', 'description'
        ]

class CarMainFeaturesListSerializer(CarMainFeaturesSerializer):
    make = CarMakeSerializer()
    model = CarModelSerializer()
    category = CarCategorySerializer()
    fuel_type = FuelTypeSerializer()
    mileage_units = MileageUnitSerializer()
    steering_wheel = SteeringWheelTypeSerializer()
    transmission = GearTypeSerializer()
    drive_wheels = DriveTypeSerializer()
    doors = DoorOptionSerializer()
    color = ColorSerializer()
    saloon_material = SaloonMaterialSerializer()
    saloon_color = SaloonColorSerializer()
    features = FeatureSerializer(many=True)


class CarPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPrice
        fields = '__all__'
        

class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPhoto
        fields = ['id', 'photo']
        


        

class CarListingDetailSerializer(serializers.ModelSerializer):
    main_features = CarMainFeaturesListSerializer(required=True)
    price = CarPriceSerializer(required=True)
    location = LocationSerializer(required=True)
    author = UserInfoSerializer(read_only=True)
    photos = CarPhotoSerializer(many=True, read_only=True)
    

    class Meta:
        model = CarListing
        fields = [
            'id', 'main_features', 'location', 'is_cleared', 'is_inspected',
            'price', 'video_link', 'contact_name', 'contact_phone', 
            'contact_email', 'is_active', 'author', 'views', 'photos',
            'created_at'
        ]
        

class CarListingListSerializer(serializers.ModelSerializer):
    main_features = CarMainFeaturesListSerializer(required=True)
    price = CarPriceSerializer(required=True)
    location = LocationSerializer(required=True)
    author = serializers.StringRelatedField(read_only=True)
    first_photo = serializers.SerializerMethodField()

    class Meta:
        model = CarListing
        fields = [
            'id', 'main_features', 'location', 'is_cleared', 'is_inspected',
            'price', 'video_link', 'contact_name', 'contact_phone', 
            'contact_email', 'is_active', 'author', 'views', 'first_photo',
            'created_at'
        ]

    def get_first_photo(self, obj):
        photo = obj.photos.first()  
        if photo:
            return CarPhotoSerializer(photo).data
        return None
    
class CarListingSerializer(serializers.ModelSerializer):
    main_features = CarMainFeaturesSerializer(required=True)  
    price = CarPriceSerializer(required=True)  
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=True)
    confirmation_code = ConfirmationCodeSerializer(required=True, write_only=True)

    class Meta:
        model = CarListing
        fields = [
            'id', 'main_features', 'location', 'is_cleared', 'is_inspected',
            'price', 'video_link', 'contact_name', 'contact_phone', 
            'contact_email', 'is_active', 'confirmation_code'
        ]
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        confirmation_code = validated_data.pop('confirmation_code', None)
        contact_email = validated_data.get('contact_email')  

        try:
            confirmation = EmailConfirmation.objects.get(
                email=contact_email, 
                code=confirmation_code['code'], 
                user=self.context['request'].user
            )
        except EmailConfirmation.DoesNotExist:
            raise serializers.ValidationError({'confirmation_code': 'Invalid confirmation code'})
        
        if confirmation.is_expired():
            raise serializers.ValidationError({'confirmation_code': 'The confirmation code has expired'})
        
        confirmation.delete()
        
        main_features_data = validated_data.pop('main_features')
        price_data = validated_data.pop('price')
        location = validated_data.pop('location')
        author = self.context['request'].user

        car_make = main_features_data.get('make')
        car_model = main_features_data.get('model')

        main_features_data.pop('make')
        main_features_data.pop('model')
        features_data = main_features_data.pop('features', [])
        car_main_features = CarMainFeatures.objects.create(
            make=car_make,
            model=car_model,
            **main_features_data
        )
        car_main_features.save()
        car_main_features.features.set(features_data)

        car_price = CarPrice.objects.create(**price_data)

        validated_data.pop('author')
        car_listing = CarListing.objects.create(
            author=author,
            main_features=car_main_features,
            location=location,
            price=car_price,
            **validated_data
        )
        car_listing.save()

        return car_listing

    def validate(self, attrs):
        main_features = attrs.get('main_features', {})
        location = attrs.get('location')
        is_cleared = attrs.get('is_cleared', False)
        is_inspected = attrs.get('is_inspected', False)
        price_data = attrs.get('price', {})
        contact_name = attrs.get('contact_name', "")
        contact_email = attrs.get('contact_email', "")
        contact_phone = attrs.get('contact_phone', "")
        car_make = main_features.get('make')
        car_model = main_features.get('model')
        year = main_features.get('year')
        
        current_year = datetime.datetime.now().year
        max_year = current_year + 1 
        if year < 1886:  
            raise ValidationError(f"{year} is too old. Cars didn't exist before 1886.")
        if year > max_year:
            raise ValidationError(f"{year} is invalid. Future car models can only be up to {max_year}.")
        
        if not car_model or not car_make:
            raise serializers.ValidationError("Both car make and model are required.")

        if car_model.make.id != car_make.id:
            raise serializers.ValidationError(f"Car model {car_model} does not belong to the car make {car_make}.")

        # 1. Validate Location Group
        if location.group != 'GE' and is_cleared:
            raise serializers.ValidationError("Clearance can't be marked outside of Georgia.")

        # 2. Validate is_inspected depends on is_cleared
        if is_inspected and not is_cleared:
            raise serializers.ValidationError("Car must be cleared before it can be inspected.")

        # 3. Validate Email
        email_validator = EmailValidator()
        try:
            email_validator(contact_email)
        except:
            raise serializers.ValidationError("Invalid email address.")

        # 4. Validate Full Name
        if len(contact_name.split()) < 2:
            raise serializers.ValidationError("Contact name must include first and last names.")
        
        # Validate contact_name for non-alphabetic characters
        if not all(char.isalpha() or char.isspace() for char in contact_name):
            raise serializers.ValidationError("Contact name must contain only alphabetic characters.")

        # 5. Validate Price and Price Negotiable
        price = price_data.get('price', None)
        price_negotiable = price_data.get('price_negotiable', False)

        if price_negotiable:
            # If negotiable, price should be ignored
            attrs['price']['price'] = None
        elif price is None and not price_negotiable:
            raise serializers.ValidationError("Price is required if it's not negotiable.")

        # 6. Validate Phone Number
        if not contact_phone.isdigit() or len(contact_phone) < 9:
            raise serializers.ValidationError("Invalid phone number.")

        return attrs


class UploadCarListingPhotosSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(
        child=serializers.ImageField()
    )

    class Meta:
        model = CarPhoto
        fields = ['photos']

    def create(self, validated_data):
        photos = validated_data.get('photos')
        print("photos", photos)
        listing_id = self.context['listing_id']
        print("listing_id", listing_id)
        car_listing = CarListing.objects.get(id=listing_id)

        for photo in photos:
            CarPhoto.objects.create(
                car=car_listing,
                photo=photo
            )

        return car_listing    