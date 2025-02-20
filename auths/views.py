import random
import string
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.timezone import now, make_aware, is_naive
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import (
    UserRegisterSerializer, LoginSerializer, UserSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer, PasswordChangeSerializer
)
from .tokens import email_activation_token

User = get_user_model()


def success_response(message, data, status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "statusCode": status_code,
        "message": message,
        "data": data
    }, status=status_code)


def failure_response(message, error, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "statusCode": status_code,
        "message": message,
        "error": error
    }, status=status_code)


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response("Profile updated successfully", serializer.data)


class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            # token = default_token_generator.make_token(user)
            token = email_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"http://127.0.0.1:8000/api/v1/auth/active/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                'confirm_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")

            email.send()

            return success_response('Check your email for confirmation', {'email': user.email})
        return failure_response('Something went wrong.', serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, UnicodeDecodeError):
        return redirect('verified_unsuccess')

    # Check token validity before proceeding
    if not email_activation_token.check_token(user, token):
        return redirect('verified_unsuccess')

    # Ensure token hasn't expired (6-hour limit)
    if user.last_login:
        token_created_at = user.last_login
    else:
        token_created_at = now()

    # Convert `last_login` to a timezone-aware datetime if it's naive
    if is_naive(token_created_at):
        token_created_at = make_aware(token_created_at)

    expiration_time = timedelta(hours=6)

    if now() - token_created_at > expiration_time:
        return redirect('verified_unsuccess')  # Token expired

    # Activate user if not already active
    if not user.is_active:
        user.is_active = True
        user.is_verified = True
        user.save()

    return redirect('verified_success')


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(self, user):
        refresh_token = super().for_user(user)

        # Add custom claims
        refresh_token.payload['username'] = user.username
        refresh_token.payload['email'] = user.email
        refresh_token.payload['role'] = user.role

        return refresh_token


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = CustomRefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Login successful',
                'data': {
                    'access': access_token,
                    'refresh': refresh_token,
                }
            })

            response.set_cookie('refresh_token', refresh_token,
                                httponly=True, secure=True)

            login(request, user)
            return response

        # Directly return a Response instead of using failure_response
        return Response({
            'success': False,
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'message': 'Invalid credentials',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success_response(
            message="You have access!",
            data={},
            status_code=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

                response = success_response("Logout successful")
                # Delete the refresh token cookie
                response.delete_cookie('refresh_token')
                return response
            return failure_response("Refresh token not provided")
        except Exception as e:
            return failure_response("Logout failed", str(e), status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                new_access = RefreshToken(refresh_token).access_token
                return success_response("Token refreshed successfully", {"access": str(new_access)}, status.HTTP_200_OK)
            except Exception as e:
                return failure_response("Failed to refresh token", str(e), status.HTTP_400_BAD_REQUEST)
        return failure_response("Refresh token not provided", {}, status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Check if the old password is correct
        if not user.check_password(old_password):
            return failure_response("Incorrect old password", {"detail": "Incorrect old password"}, status.HTTP_400_BAD_REQUEST)

        # Update password
        user.set_password(new_password)
        user.save()

        # Update session to prevent logout after password change
        update_session_auth_hash(request, user)

        return success_response({"message": "Password changed successfully"}, status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """Send OTP to user's email for password reset"""

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return failure_response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a random OTP of 6 characters, consisting of numbers and letters
        otp = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))

        # Save OTP in user profile
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.otp = otp
        user_profile.otp_created_at = timezone.now()
        user_profile.save()

        # Send OTP email
        email_subject = "Your OTP for Password Reset"
        email_body = render_to_string(
            'reset_password_email.html', {'otp': otp})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()

        return success_response("Please check your email for OTP.", {user.email}, status.HTTP_200_OK)


class ValidateOTPView(APIView):
    """Validate OTP before allowing password reset"""

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user_profile = UserProfile.objects.get(user__email=email)
        except UserProfile.DoesNotExist:
            return failure_response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if OTP matches and is not expired
        if user_profile.otp == otp:
            if user_profile.is_otp_expired():
                return failure_response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            return success_response("Successfully OTP Verified. Proceed with password reset.", {}, status.HTTP_200_OK)

        return failure_response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """Reset password using OTP"""

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        serializer = ResetPasswordSerializer(data=request.data)

        if not email or not otp:
            return failure_response({"message": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']

        try:
            user_profile = UserProfile.objects.get(user__email=email)
        except UserProfile.DoesNotExist:

            return failure_response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.otp == otp and not user_profile.is_otp_expired():
            user = user_profile.user
            user.password = make_password(new_password)  # Hash new password
            user.save()

            # Clear OTP after reset
            user_profile.otp = None
            user_profile.save()

            return success_response("Password reset successfully.", {}, status.HTTP_200_OK)

        return failure_response({"message": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)


# email success verify response
def successful(request):
    return render(request, 'successful.html')

# email confirm unsuccessful message


def unsuccessful(request):
    return render(request, 'unsuccessful.html')

# googel auth


class GoogleLoginView(APIView):
    def get(self, request):
        # Google OAuth authorization URL
        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code"
            f"&client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}"
            f"&redirect_uri={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI}"
            f"&scope=email%20profile"
        )
        return Response({"auth_url": google_auth_url})


def generate_random_username(length=8):
    # Generates a random username with the specified length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class GoogleAuthCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "No authorization code found."}, status=400)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        if token_response.status_code != 200:
            return Response({"error": "Failed to get access token."}, status=400)

        token_response_data = token_response.json()
        access_token = token_response_data.get("access_token")

        # Get user info from Google API using the access token
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_response = requests.get(
            user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user information."}, status=400)

        user_data = user_info_response.json()
        email = user_data.get("email")
        name = user_data.get("name")
        # username = email.split("@")[0]
        if email and '@' in email:
            username = email.split('@')[0]
        else:
            # If the email is invalid or missing, generate a random username
            username = generate_random_username()

        # Ensure user is retrieved or created without duplicate email issues
        user, created = User.objects.get_or_create(
            email=email, defaults={"username": username, "first_name": name})

        if not created and user.username != email:
            user.username = email
            user.save(update_fields=["username"])
        # ✅ Set the backend manually
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Create JWT token for the user
        refresh = CustomRefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        user.is_active = True

        response = Response({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Login successful',
            'data': {
                'access': access_token,
                'refresh': refresh_token,
            }
        })

        # Save the tokens in HttpOnly, Secure cookies
        # response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Strict')
        response.set_cookie('refresh_token', refresh_token,
                            httponly=True, secure=True, samesite='Strict')

        login(request, user)
        return response
