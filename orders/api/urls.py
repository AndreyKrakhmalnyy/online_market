from django.urls import path, include
from rest_framework import routers
from orders.api.views import OrderViewSet, OrderItemViewSet


router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"orders-item", OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]