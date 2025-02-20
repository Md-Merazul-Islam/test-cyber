from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
User = get_user_model()


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    rating = models.IntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(5)])  # Example: 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.user.username} - {self.rating}"
