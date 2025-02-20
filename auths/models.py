from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
now = timezone.now()


class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MANAGER = 'manager', 'Manager'
    USER = 'user', 'User'


# class SubscriptionPlan(models.Model):
#     name = models.CharField(max_length=100)  # Add a name for better clarity
#     price = models.DecimalField(
#         max_digits=10, decimal_places=2, null=True, blank=True)  # Optional for paid plans
#     duration_in_months = models.PositiveIntegerField()
#     description = models.TextField()
#     subscription_type = models.CharField(
#         max_length=50,
#         choices=[
#             ('free', 'Free'),
#             ('paid', 'Paid'),
#             ('trial', 'Trial'),
#         ],
#         default='free'
#     )

#     def __str__(self):
#         return self.name  # Changed to 'name' instead of 'subscription_type'


# class UserSubscription(models.Model):
#     user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
#     subscription_plan = models.ForeignKey(
#         SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.email} - {self.subscription_plan.name}"

#     def update_subscription_status(self):
#         # Method to automatically update 'is_active' based on 'end_date'
#         if self.end_date and self.end_date < timezone.now():
#             self.is_active = False
#         else:
#             self.is_active = True
#         self.save()


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # subscription_plan = models.ForeignKey('UserSubscription', on_delete=models.SET_NULL, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    
    def is_otp_expired(self):
        if self.otp_created_at:
            return timezone.now() > self.otp_created_at + timezone.timedelta(minutes=10)
        return True
    
    def __str__(self):
        return f"Profile of {self.user.email}"