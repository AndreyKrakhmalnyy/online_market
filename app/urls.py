from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from app import settings


urlpatterns = [
    path("", include("main.urls", namespace="main")),
    path("admin/", admin.site.urls),
    path("catalog/", include("goods.urls", namespace="catalog")),
    path("user/", include("users.urls", namespace="user")),
    path("cart/", include("carts.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    
    path("Jwt-token/", include("utils.auth.jwt-auth.urls")),
    path("swagger-api/", include("utils.api.swagger.urls")),
    path("goods-api/", include("goods.api.urls")),
    path("users-api/", include("users.api.urls")),
    path("orders-api/", include("orders.api.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"http://127.0.0.1:8000/admin"
"http://127.0.0.1:8000/swagger-api/endpoints/"
