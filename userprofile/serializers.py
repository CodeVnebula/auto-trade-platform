from django.forms import ValidationError
from rest_framework import serializers
from auto_market.validators import validate_photo_size
from userprofile.models import CompareListings
from car_listing.models import  CarListing
from authentication.models import EmailConfirmation
from car_listing.serializers import CarListingListSerializer, ConfirmationCodeSerializer
from authentication.models import Profile, User
from messaging.models import UserChats

from authentication.serializers import UserInfoSerializer


class CompareListingsSerializer(serializers.ModelSerializer):
    car_listings = CarListingListSerializer(many=True, read_only=True)
    
    class Meta:
        model = CompareListings
        fields = ['id', 'user', 'car_listings']
        
        
class ProfileInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    chats_count = serializers.SerializerMethodField()

    def get_chats_count(self, obj):
        return obj.user.userchats.chats.count()
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'profile_picture', 'enable_messages', 
            'receive_messages', 'receive_emails', 'hide_phone', 
            'hide_email', 'is_public', 'chats_count'
        ]
        read_only_fields = ['user']
        

class ProfileInfoUpdateSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'profile_picture'
        ]
        read_only_fields = ['user']
        
    def validate(self, attrs):
        first_name = attrs.get('user').get('first_name')
        last_name = attrs.get('user').get('last_name')
        phone = attrs.get('user').get('phone')
        
        if not first_name:
            raise serializers.ValidationError('First name is required.')
        if not last_name:
            raise serializers.ValidationError('Last name is required.')
        
        if first_name.isnumeric():
            raise serializers.ValidationError('First name cannot be numeric.')
        if last_name.isnumeric():
            raise serializers.ValidationError('Last name cannot be numeric.')
        
        if phone:
            if not phone.isdigit():
                raise serializers.ValidationError('Phone number must be numeric.')
            if len(phone) != 9:
                raise serializers.ValidationError('Phone number is not valid.')
        
        return attrs
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)

        new_phone = user_data.get('phone', user.phone)
        if user.phone != new_phone:
            user.phone = new_phone

        new_address = user_data.get('address', user.address)
        if user.address != new_address:
            user.address = new_address
            
            user.save()
        
        instance.profile_picture = validated_data.get(
            'profile_picture', instance.profile_picture
        )
        instance.enable_messages = validated_data.get(
            'enable_messages', instance.enable_messages
        )
        instance.receive_messages = validated_data.get(
            'receive_messages', instance.receive_messages
        )
        instance.receive_emails = validated_data.get(
            'receive_emails', instance.receive_emails
        )
        instance.hide_phone = validated_data.get(
            'hide_phone', instance.hide_phone
        )
        instance.hide_email = validated_data.get(
            'hide_email', instance.hide_email
        )
        instance.is_public = validated_data.get(
            'is_public', instance.is_public
        )
        
        instance.save()
        
        return instance
    
    
from django.contrib.auth.hashers import check_password

class PasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    
    class Meta:
        fields = ['current_password', 'new_password1', 'new_password2']

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate(self, attrs):
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError({'new_password2': 'New passwords do not match.'})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password1 = self.validated_data['new_password1']
        user.set_password(new_password1)
        user.save()
        return user
    
    
class DeactivateXDeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        # Add any custom password validation if necessary
        if not value:
            raise serializers.ValidationError('Password is required.')
    

class UploadUserProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        
    def validate_profile_picture(self, value):
        validate_photo_size(value)
        return value
    
    def update(self, instance, validated_data):
        if 'profile_picture' not in validated_data:
            raise serializers.ValidationError(
                "profile_picture field is required. Don't send me that keyword"
            )
        
        if instance.profile_picture:
            instance.profile_picture.delete()
        instance.profile_picture = validated_data.get(
            'profile_picture', instance.profile_picture
        )
        instance.save()
        return instance
    