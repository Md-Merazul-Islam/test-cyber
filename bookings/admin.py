from django.contrib import admin
from .models import BookingRequest


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'phone', 'service', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'service__name')
    list_filter = ('status',)
