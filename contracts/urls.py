
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.urls import path
from .views import ContractCreateView, ContractViewSetList

router = DefaultRouter()
router.register(r'send-message-list', ContractViewSetList)

urlpatterns = [
    path('', include(router.urls)),
    path('send-message/', ContractCreateView.as_view(), name='send-message'),
]
