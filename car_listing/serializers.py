from rest_framework import serializers
from .models import (
    CarListing, CarCategory, CarMake, CarModel, Feature, DriveType, 
    Color, SaloonColor,  SaloonMaterial, Location, GearType,
    SteeringWheelType, FuelType, MileageUnit, DoorOption
)


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'
        

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = '__all__'
        

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        

class DriveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveType
        fields = '__all__'
        

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SaloonColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaloonColor
        fields = '__all__'


class SaloonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaloonMaterial
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

class GearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GearType
        fields = '__all__'
        

class SteeringWheelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteeringWheelType
        fields = '__all__'
        

class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = '__all__'


class MileageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageUnit
        fields = '__all__'
        

class DoorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorOption
        fields = '__all__'