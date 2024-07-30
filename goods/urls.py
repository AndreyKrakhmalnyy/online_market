from django.views.decorators.cache import cache_page
from django.urls import path
from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', cache_page(60*15)(views.CatalogView.as_view()), name='index'),
    path('product/<slug:product_slug>', cache_page(60*15)(views.ProductView.as_view()), name='product'),
]

