from cache.main.cache import cached_about
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', cached_about, name='about'),
]