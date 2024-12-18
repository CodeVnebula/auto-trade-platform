from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from car_listing.serializers import CarListingListSerializer

from .models import CompareListings, FacouriteListings
from .serializers import CompareListingsSerializer, ProfileInfoSerializer, ProfileInfoUpdateSerializer, DeactivateXDeleteAccountSerializer, UploadUserProfilePictureSerializer
from car_listing.models import CarListing
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Q, Sum


class CompareListingsView(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CompareListingsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        return CompareListings.objects.filter(user=self.request.user)

    @action(
        detail=False, 
        methods=['post'], 
        url_path='add/(?P<listing_id>[0-9]+)', 
        serializer_class=None
    )
    def add_listing(self, request, listing_id=None):
        car_listing = get_object_or_404(CarListing, id=listing_id)
        compare_list, _ = CompareListings.objects.get_or_create(user=request.user)
        if compare_list.car_listings.filter(id=car_listing.id).exists():
            return Response(
                {"message": "Car listing already exists in the compare list."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        compare_list.car_listings.add(car_listing)
        return Response(
            {"message": f"Car listing with ID {listing_id} added successfully."}, 
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=False, 
        methods=['delete'], 
        name='remove_listing', 
        url_path='remove/(?P<listing_id>[0-9]+)'
    )
    def remove_listing(self, request, listing_id=None):
        car_listing = get_object_or_404(CarListing, id=listing_id)
        compare_list = get_object_or_404(CompareListings, user=request.user)
        compare_list.car_listings.remove(car_listing)
        return Response(
            {"message": "Car listing removed successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['delete'], name='clear_all', url_path='clear')
    def clear_all(self, request):
        compare_list = get_object_or_404(CompareListings, user=request.user)
        compare_list.car_listings.clear()
        return Response(
            {"message": "All car listings cleared successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )


class ProfileView(GenericViewSet):
    serializer_class = ProfileInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']
    pagination_class = None
    
    def get_object(self):
        return self.request.user.profile

    @action(detail=False, methods=['get'], name='get_profile_data', url_path='info')
    def get(self, request):
        return Response(self.serializer_class(self.get_object()).data, status=status.HTTP_200_OK)
    
    from django.db.models import Sum, Count

    @action(detail=False, methods=['get'], name='get_profile_stats', url_path='stats')
    def get_profile_stats(self, request):
        user = request.user

        stats = CarListing.objects.filter(author=user).aggregate(
            active_listings_count=Count('id', filter=Q(is_active=True)),
            total_views=Sum('views'),
            total_listings_count=Count('id')
        )

        active_listings_count = stats.get('active_listings_count', 0)
        total_views = stats.get('total_views', 0)
        total_listings_count = stats.get('total_listings_count', 0)
        
        if total_views is None:
            total_views = 0
        if total_views > 1000:
            total_views = f"{total_views/1000}k"

        return Response({
            "active_listings_count": active_listings_count,
            "total_views": total_views,
            "total_listings_count": total_listings_count
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'], name='update_profile_data', url_path='info/update', serializer_class=ProfileInfoUpdateSerializer)
    def put(self, request):
        profile = self.get_object()
        
        serializer = self.serializer_class(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class UserListingsViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CarListingListSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        return CarListing.objects.filter(author=user)
    

class FavouriteListingsView(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CompareListingsSerializer
    permission_classes = [IsAuthenticated]
    page_size = 12

    def get_queryset(self):
        return FacouriteListings.objects.filter(user=self.request.user)

    @action(
        detail=False, 
        methods=['post'], 
        url_path='add/(?P<listing_id>[0-9]+)', 
        serializer_class=None
    )
    def add_listing(self, request, listing_id=None):
        car_listing = get_object_or_404(CarListing, id=listing_id)
        facourite_list, _ = FacouriteListings.objects.get_or_create(user=request.user)
        if facourite_list.car_listings.filter(id=car_listing.id).exists():
            return Response(
                {"message": "Car listing already exists in the favourite list."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        facourite_list.car_listings.add(car_listing)
        return Response(
            {"message": f"Car listing with ID {listing_id} added successfully."}, 
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=False, 
        methods=['delete'], 
        name='remove_listing', 
        url_path='remove/(?P<listing_id>[0-9]+)'
    )
    def remove_listing(self, request, listing_id=None):
        car_listing = get_object_or_404(CarListing, id=listing_id)
        facourite_list = get_object_or_404(FacouriteListings, user=request.user)
        facourite_list.car_listings.remove(car_listing)
        return Response(
            {"message": "Car listing removed successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['delete'], name='clear_all', url_path='clear')
    def clear_all(self, request):
        favourite_list = get_object_or_404(FacouriteListings, user=request.user)
        favourite_list.car_listings.clear()
        return Response(
            {"message": "All car listings cleared successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )
        

class ProfileSettingsViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileInfoSerializer
    http_method_names = ['get', 'put', 'post']

    def get_object(self):
        return self.request.user.profile
    
    @action(detail=False, methods=['get'], name='get_profile_settings', url_path='settings')
    def get_profile_data(self, request):
        return Response(self.serializer_class(self.get_object()).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'], name='update_profile_settings', url_path='settings/update')
    def update_profile_settings(self, request):
        profile = self.get_object()
        enable_messages = request.data.get('enable_messages')
        receive_messages = request.data.get('receive_messages')
        receive_emails = request.data.get('receive_emails')
        hide_phone = request.data.get('hide_phone')
        hide_email = request.data.get('hide_email')
        is_public = request.data.get('is_public')
        
        profile.enable_messages = enable_messages
        profile.receive_messages = receive_messages
        profile.receive_emails = receive_emails
        profile.hide_phone = hide_phone
        profile.hide_email = hide_email
        profile.is_public = is_public
        profile.save()
        return Response(self.serializer_class(profile).data, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=['put'],
        name='deactivate_account',
        url_path='settings/deactivate-account',
        serializer_class=DeactivateXDeleteAccountSerializer
    )
    def deactivate_account(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        
        user = request.user
        if not check_password(password, user.password):
            return Response(
                {"message": "Password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = False
        user.save()
        return Response(
            {"message": "Account deactivated successfully."},
            status=status.HTTP_200_OK
        )
    
    @action(
        detail=False,
        methods=['post'],
        name='delete_account',
        url_path='settings/delete-account',
        serializer_class=DeactivateXDeleteAccountSerializer
    )
    def delete_account(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        
        user = request.user
        if not check_password(password, user.password):
            return Response(
                {"message": "Password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.delete()
        return Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_200_OK
        )


class UploadUserProfilePictureView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadUserProfilePictureSerializer
    http_method_names = ['post']
    
    
    def get_object(self):
        return self.request.user.profile
    
    @action(detail=False, methods=['post'], name='upload_profile_picture', url_path='profile/upload-picture')
    def upload_profile_picture(self, request):
        profile = self.get_object()
        print(request.user.first_name)
        print(profile)
        print(request.data)
        serializer = self.serializer_class(instance=profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
