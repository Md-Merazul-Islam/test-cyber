from django.db import models

class Contract(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=False, null=False)  # Store user IP
    hostname = models.CharField(max_length=255)  # Store user hostname
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} ({self.ip_address})"
