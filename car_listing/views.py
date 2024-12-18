from django.core.cache import cache
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated

from django.db.models import Prefetch
from rest_framework import status

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
    DoorOption,
    CarListing
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
    DoorOptionSerializer,
    CarListingSerializer,
    UploadCarListingPhotosSerializer,
    CarListingDetailSerializer,
    CarListingListSerializer
)

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .permissions import CanDeleteCarListing

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import CarListingFilter


class CarListingCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarListingSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save(author=request.user)  
            response_data = {
                'id': instance.id,  
                'message': 'Car listing created successfully',
                'data': serializer.data  
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UploadCarListingPhotosView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadCarListingPhotosSerializer
    
    def post(self, request, listing_id):
        print("asd",request.data)
        serializer = self.serializer_class(data=request.data, context={'listing_id': listing_id})
        if serializer.is_valid():
            serializer.save(car_listing_id=listing_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarMakeModelsList(generics.ListAPIView):
    serializer_class = CarModelSerializer
    pagination_class = None
    
    def get_queryset(self):
        return CarModel.objects.filter(make__id=self.kwargs['make_id'])
    
    
class CarListingDetailView(generics.RetrieveAPIView):
    queryset = CarListing.objects.all()
    serializer_class = CarListingDetailSerializer

    def get_object(self):
        listing_id = self.kwargs.get('pk')
        return get_object_or_404(CarListing, pk=listing_id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.serializer_class(instance, context={'request': request})
        return Response(serializer.data)
    

class CarListingDeleteView(generics.DestroyAPIView):
    queryset = CarListing.objects.all()
    serializer_class = CarListingDetailSerializer
    permission_classes = [IsAuthenticated, CanDeleteCarListing]
    
    def get_object(self):
        listing_id = self.kwargs.get('pk')
        return get_object_or_404(CarListing, pk=listing_id)
    

class CarListingListView(generics.ListAPIView):
    queryset = CarListing.objects.all()
    serializer_class = CarListingListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CarListingFilter
    ordering_fields = ['created_at', 'price', 'main_features__year'] 
    ordering = ['-created_at']
    page_size = 12
    max_page_size = 15

    def get_queryset(self):
        return CarListing.objects.filter(is_active=True)

    
class ConfigData(APIView):
    def get(self, request, *args, **kwargs):
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

from django.views.generic import TemplateView

class Template(TemplateView):
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config_data'] = cache.get('config_data')
        return context
    
class CarDetailView(DetailView):
    model = CarListing
    template_name = 'asd.html'
    context_object_name = 'car_listing'

    def get_object(self):
        listing_id = self.kwargs.get('pk')
        return get_object_or_404(CarListing, pk=listing_id)
