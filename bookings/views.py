from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import BookingRequest
from .serializers import BookingRequestSerializer
from .permissions import IsAdminOrAuthenticatedCreateUpdateDelete, IsAdminOrStaff
from rest_framework.pagination import PageNumberPagination

# Optimized pagination class
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Success and Failure Response Helper Functions
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

# View for listing and creating bookings
class BookingRequestView(generics.ListCreateAPIView):
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAdminOrAuthenticatedCreateUpdateDelete]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return BookingRequest.objects.all() if user.is_staff or user.role == 'admin' else BookingRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data.copy()
        data["email"] = user.email
        data.setdefault("first_name", user.first_name)
        data.setdefault("last_name", user.last_name)
        data.setdefault("phone", user.phone_number if hasattr(user, "phone_number") else "")
        data.setdefault("company_name", "Unknown")
        data.setdefault("country_or_address", user.address if hasattr(user, "address") else "")

        serializer.save(user=user, **data)
        return success_response("Booking request created successfully", serializer.data, status.HTTP_201_CREATED)

# View for retrieving, updating, and deleting a specific booking request
class BookingRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAdminOrAuthenticatedCreateUpdateDelete]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_staff and instance.user != request.user:
            return failure_response("You do not have permission to edit this booking.", status_code=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Booking request updated successfully", serializer.data)

        return failure_response("Failed to update booking request", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_staff and instance.user != request.user:
            return failure_response("You do not have permission to delete this booking.", status_code=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return success_response("Booking request deleted successfully", status_code=status.HTTP_204_NO_CONTENT)

# ViewSet for the BookingRequest model
class BookingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAdminOrStaff]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return BookingRequest.objects.all() if user.is_staff or user.role == 'admin' else BookingRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
