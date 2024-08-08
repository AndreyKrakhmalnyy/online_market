from django.urls import path
from goods import views
from cache.goods.cache import cached_categories, cached_products

app_name = 'goods'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    # path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    # path('product/<slug:product_slug>', views.ProductView.as_view(), name='product'),
    path('<slug:category_slug>/', cached_categories, name='index'),
    path('product/<slug:product_slug>', cached_products, name='product'),
]

