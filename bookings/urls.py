from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingRequestView, BookingRequestDetailView, BookingRequestViewSet

router = DefaultRouter()
router.register(r'bookings-list', BookingRequestViewSet, basename="bookings-list-view")

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/', BookingRequestView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingRequestDetailView.as_view(), name='booking-detail'),
]
