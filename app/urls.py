from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from app import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("", include("main.urls", namespace="main")),
    path("admin/", admin.site.urls),
    path("catalog/", include("goods.urls", namespace="catalog")),
    path("user/", include("users.urls", namespace="user")),
    path("cart/", include("carts.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path('api/', include('goods.api.urls')),
        path('jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('jwt-token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

