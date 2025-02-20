from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('auths.urls')),
    path('api/v1/services/', include('services.urls')),
    path('api/v1/reviews/', include('reviews.urls')),
    path('api/v1/teams/', include('teams.urls')),
    path('api/v1/contract/', include('contracts.urls')),
    path('api/v1/booking/', include('bookings.urls')),
    
]
# In development, serve media files from MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
