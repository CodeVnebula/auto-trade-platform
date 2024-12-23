import django_filters
from django_filters import rest_framework as filters
from .models import CarListing, CarMainFeatures, CarPrice

class CarListingFilter(filters.FilterSet):
    make = filters.CharFilter(field_name="main_features__make__title", lookup_expr="icontains")
    model = filters.CharFilter(field_name="main_features__model__title", lookup_expr="icontains")
    category = filters.CharFilter(field_name="main_features__category__title", lookup_expr="icontains")
    year = filters.RangeFilter(field_name="main_features__year")
    fuel_type = filters.CharFilter(field_name="main_features__fuel_type__title", lookup_expr="icontains")
    engine_volume = filters.RangeFilter(field_name="main_features__engine_volume")
    turbo = filters.BooleanFilter(field_name="main_features__turbo")
    cylinders = filters.NumberFilter(field_name="main_features__cylinders")
    min_mileage = filters.RangeFilter(field_name="main_features__mileage")
    steering_wheel = filters.CharFilter(field_name="main_features__steering_wheel__title", lookup_expr="icontains")
    transmission = filters.CharFilter(field_name="main_features__transmission__title", lookup_expr="icontains")
    drive_wheels = filters.CharFilter(field_name="main_features__drive_wheels__title", lookup_expr="icontains")
    doors = filters.CharFilter(field_name="main_features__doors__title", lookup_expr="icontains")
    catalyst = filters.BooleanFilter(field_name="main_features__catalyst")
    color = filters.CharFilter(field_name="main_features__color__title", lookup_expr="icontains")
    saloon_material = filters.CharFilter(field_name="main_features__saloon_material__title", lookup_expr="icontains")
    saloon_color = filters.CharFilter(field_name="main_features__saloon_color__title", lookup_expr="icontains")

    min_price = filters.NumberFilter(field_name="price__price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price__price", lookup_expr="lte")
    price_negotiable = filters.BooleanFilter(field_name="price__price_negotiable")
    exchange_for_another_car = filters.BooleanFilter(field_name="price__exchange_for_another_car")

    location = filters.CharFilter(field_name="location__title", lookup_expr="icontains")
    video_link = filters.CharFilter(field_name="video_link", lookup_expr="icontains")
    is_cleared = filters.BooleanFilter(field_name="is_cleared")
    is_inspected = filters.BooleanFilter(field_name="is_inspected")
    created_at = filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = CarListing
        fields = []
