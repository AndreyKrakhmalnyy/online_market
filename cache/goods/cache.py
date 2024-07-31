from django.views.decorators.cache import cache_page
from goods import views

cached_categories = cache_page(60*15)(views.CatalogView.as_view())
cached_products = cache_page(60*15)(views.ProductView.as_view())