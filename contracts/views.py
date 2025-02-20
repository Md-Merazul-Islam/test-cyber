from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ContractSerializer
from .models import Contract
from rest_framework import viewsets
from .permissions import IsAdminOrAuthenticatedCreateUpdateDelete
from rest_framework import pagination
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
def success_response(message, data=None, status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "statusCode": status_code,
        "message": message,
        "data": data
    }, status=status_code)

def failure_response(message, error=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "statusCode": status_code,
        "message": message,
        "error": error
    }, status=status_code)


class ContractCreateView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def perform_create(self, serializer):
        """Validate and save the contract with IP and hostname restrictions."""
        email = self.request.data.get('email')
        ip_address = self.request.data.get(
            'ip_address')  # Get IP from frontend
        hostname = self.request.data.get(
            'hostname', 'unknown-device')  # Optional hostname

        if not email or not ip_address:
            return failure_response("Email and IP address are required")

        # Check messages sent in the last 24 hours from this IP & Hostname
        time_threshold = timezone.now() - timedelta(days=1)
        message_count = Contract.objects.filter(
            ip_address=ip_address, created_at__gte=time_threshold
        ).count()

        if message_count >= 5:
            raise ValidationError(
                {"error": "Too many requests from this IP and hostname in the last 24 hours"})
        # Save validated data
        serializer.save(ip_address=ip_address, hostname=hostname)





class ContractViewSetList(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('-created_at')
    serializer_class = ContractSerializer
    permission_classes = [IsAdminOrAuthenticatedCreateUpdateDelete]
    pagination_class=CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Items fetched successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Item details fetched successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Item created successfully", serializer.data, status.HTTP_201_CREATED)
        return failure_response("Item creation failed", serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Item updated successfully", serializer.data)
        return failure_response("Item update failed", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response("Item deleted successfully", None, status.HTTP_204_NO_CONTENT)
