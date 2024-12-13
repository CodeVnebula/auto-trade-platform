from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Prefetch


from .models import (
    VehicleType,
    CarMake,
    CarModel,
    CarCategory,
    Feature,
    DriveType,
    Color,
    SaloonColor,
    SaloonMaterial,
    Location,
    GearType,
    SteeringWheelType,
    FuelType,
    MileageUnit,
    DoorOption
)
from .serializers import (
    CarMakeSerializer,
    CarModelSerializer,
    CarCategorySerializer,
    FeatureSerializer,
    DriveTypeSerializer,
    ColorSerializer,
    SaloonColorSerializer,
    SaloonMaterialSerializer,
    LocationSerializer,
    GearTypeSerializer,
    SteeringWheelTypeSerializer,
    FuelTypeSerializer,
    MileageUnitSerializer,
    DoorOptionSerializer    
)

class CarMakeModelsList(generics.ListAPIView):
    serializer_class = CarModelSerializer
    pagination_class = None
    
    def get_queryset(self):
        return CarModel.objects.filter(make__id=self.kwargs['make_id'])
    

class ConfigData(APIView):
    def get(self, request, *args, **kwargs):
        cache.clear()
        data = cache.get('config_data')
        
        if not data:
            data = {
                'car_makes': CarMakeSerializer(
                    CarMake.objects.prefetch_related(
                        Prefetch('vehicle_types', queryset=VehicleType.objects.filter(title='CAR'))
                    ).all(), many=True
                ).data,
                'car_categories': CarCategorySerializer(
                    CarCategory.objects.prefetch_related(
                        Prefetch('vehicle_type', queryset=VehicleType.objects.filter(title='CAR'))
                    ).all(), many=True
                ).data,
                'features': FeatureSerializer(
                    Feature.objects.all(), many=True
                ).data,
                'drive_types': DriveTypeSerializer(
                    DriveType.objects.all(), many=True
                ).data,
                'colors': ColorSerializer(
                    Color.objects.all(), many=True
                ).data,
                'saloon_colors': SaloonColorSerializer(
                    SaloonColor.objects.all(), many=True
                ).data,
                'saloon_materials': SaloonMaterialSerializer(
                    SaloonMaterial.objects.all(), many=True
                ).data,
                'locations': LocationSerializer(
                    Location.objects.all(), many=True
                ).data,
                'gear_types': GearTypeSerializer(
                    GearType.objects.all(), many=True
                ).data,
                'steering_wheel_types': SteeringWheelTypeSerializer(
                    SteeringWheelType.objects.all(), many=True
                ).data,
                'fuel_types': FuelTypeSerializer(
                    FuelType.objects.all(), many=True
                ).data,
                'mileage_units': MileageUnitSerializer(
                    MileageUnit.objects.all(), many=True
                ).data,
                'door_options': DoorOptionSerializer(
                    DoorOption.objects.all(), many=True
                ).data,
            }        
            
            cache.set('config_data', data, 60 * 60 * 12) # 12 hours

        return Response(data)
