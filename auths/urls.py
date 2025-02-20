from django.urls import path
from .views import (
    RegisterAPIView, LoginView, ProtectedView,
    LogoutView, RefreshTokenView, ForgotPasswordView, GoogleLoginView, GoogleAuthCallbackView, PasswordChangeView, ResetPasswordView, ProfileView, activate, successful, unsuccessful, ValidateOTPView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected-endpoint/', ProtectedView.as_view(), name='protected'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    # --- password_change
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    # --forgot_password
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('validate-otp/', ValidateOTPView.as_view(), name='validate_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    # --- email verification
    path('active/<str:uid64>/<str:token>/', activate, name='active'),
    path('successful-email-verified/', successful, name='verified_success'),
    path('unsuccessful-email-verified/', unsuccessful, name='verified_unsuccess'),

    # ---- google auth
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('google/callback/', GoogleAuthCallbackView.as_view(),name='google_callback'),
]
