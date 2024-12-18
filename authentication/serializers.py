import random
from django.conf import settings
from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User, Profile
from userprofile.models import CompareListings, FacouriteListings
from messaging.models import UserChats
from auto_market.utils import contains_prohibited_words
from .models import EmailConfirmation


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'password', 'password_2'
        )

    def validate(self, attrs):    
        password = attrs.get('password')
        password_2 = attrs.get('password_2')
        if password != password_2:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        if password and len(password) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long'
            )
        if password and not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                'Password must contain a digit'
            )
        if password and not any(char.isalpha() for char in password):
            raise serializers.ValidationError(
                'Password must contain a letter'
            )
        if password and not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                'Password must contain an uppercase letter'
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_2')
        user = User.objects.create(**validated_data)
        user.is_active = False
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        compare_listings = CompareListings.objects.create(user=user)
        compare_listings.save()
        facourite_listings = FacouriteListings.objects.create(user=user)
        facourite_listings.save()
        user_chat = UserChats.objects.create(user=user)
        user_chat.save()
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        request = self.context.get('request')
        verification_link = request.build_absolute_uri(
            reverse('auth:email_verify', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            subject='Verify your email',
            message=f'Click the link to verify your email: {verification_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return user
    

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'No user found with this email.'
            )
        return value
            
    def save(self, **kwargs):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        self.send_reset_email(user)

    def send_reset_email(self, user):
        """Generates and sends a password reset email."""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        request = self.context.get('request')
        reset_password_link = request.build_absolute_uri(
            reverse('auth:reset_password', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            subject='Reset your password',
            message=f'Click the link to reset your password: {reset_password_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
    
    
class ResetPasswordSerializer(SignupSerializer):
    
    class Meta:
        model = User
        fields = ('password', 'password_2')
        
    def validate(self, attrs):
        attrs = super().validate(attrs)
        password = attrs.get('password')
        user = self.context.get('user')
        if user and user.check_password(password):
            raise serializers.ValidationError(
                'New password must be different from the current password.'
            )

        return attrs
    
    def save(self, **kwargs):
        password = self.validated_data.get('password')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return user
    
    
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'address')
        

class SendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email']

    def create(self, validated_data):
        email = validated_data['email']
        user = self.context['request'].user  

        code = f"{random.randint(100000, 999999)}"

        EmailConfirmation.objects.create(email=email, code=code, user=user)

        send_mail(
            'Your Confirmation Code',
            f'Your confirmation code is {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return {'email': email, 'message': 'Confirmation code sent successfully'}
    
    
class ConfirmationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    class Meta:
        fields = ['code', 'email']