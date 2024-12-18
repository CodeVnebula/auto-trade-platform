from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    SignupSerializer,
    ResetPasswordSerializer,
    ResetPasswordRequestSerializer,
    SendConfirmationCodeSerializer
)

from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.tokens import default_token_generator

from .models import User


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'message': 'User created successfully. Check your email to activate your account.'
        }
        return response


class ResetPasswordRequestView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    http_method_names = ['post']
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "If the email exists, a password reset link has been sent."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    http_method_names = ['put']
    
    def get(self, _, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                return Response(
                    {'detail': 'Token is valid.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'detail': 'Invalid or expired token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'detail': f'Error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self, uidb64, token):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        print(self.kwargs)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                return user
        except Exception:
            return None

    def put(self, request, uidb64, token):
        instance = self.get_object(uidb64, token)
        print(instance)
        if not instance:
            return Response(
                {'detail': 'Invalid token or user not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.serializer_class(data=request.data, context={'user': instance})
        if serializer.is_valid():
            serializer.save(user=instance)
            return Response(
                {'detail': 'Password reset successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class EmailVerifyView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {'message': 'Email verified successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Invalid token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'message': f'Invalid token: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
class SendConfirmationCodeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendConfirmationCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()  
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    