

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet,ItemCreateView

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', ItemCreateView.as_view(), name='item_create'),  # POST: create new item
]
