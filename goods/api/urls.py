from django.urls import path, include
from rest_framework import routers
from goods.api.views import CategoriesViewSet, ProductsViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)

urlpatterns = [
    path('goods/', include(router.urls)),
]