from django.urls import include, path

from authentication.views import (
    SignupView,
    EmailVerifyView,
    ResetPasswordView,
    ResetPasswordRequestView
)

app_name = 'auth'

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

urlpatterns = [
    path('auth/', include(
            [
                path('signup/', SignupView.as_view(), name='signup'),
                path('login/', TokenObtainPairView.as_view(), name='login'),
                path('logout/', TokenBlacklistView.as_view(), name='logout'),
                path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
                path('reset-password-request/', ResetPasswordRequestView.as_view(), name='reset_password_request'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                path('email-verify/<uidb64>/<token>/', EmailVerifyView.as_view(), name='email_verify')
            ]
        )
    ),
]