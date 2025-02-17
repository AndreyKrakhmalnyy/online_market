from django.views.decorators.cache import cache_page
from main import views

cached_about = cache_page(60*15)(views.AboutView.as_view())
cached_delivery = cache_page(60*15)(views.DeliveryView.as_view())