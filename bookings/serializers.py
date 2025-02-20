from rest_framework import serializers
from .models import BookingRequest

class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ['id','first_name',  'email', 'phone', 'company_name', 'country_or_address', 'status', 'service','start_date','end_date','created_at']
        read_only_fields = ['id','status',]  
