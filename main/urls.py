from cache.main.cache import cached_about, cached_delivery
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', cached_about, name='about'),
    path('delivery/', cached_delivery, name='delivery'),
    # path('about/', views.AboutView.as_view(), name='about'),
    # path('delivery/', views.DeliveryView.as_view(), name='delivery'),
]