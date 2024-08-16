from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from orders.api.serializers import OrderSerializer, OrderItemSerializer
from orders.models import Order, OrderItem

@extend_schema(tags=['Orders'])
class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заказами пользователей с аутентификацией по jwt-токену."""
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """Определяет доступ к методам ViewSet."""
        
        if self.action == 'list' or self.action == 'retrieve':  
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]
    
@extend_schema(tags=['OrderItem'])
class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet для управления товарами заказов пользователей с аутентификацией по jwt-токену."""
        
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """Определяет доступ к методам ViewSet."""
        
        if self.action == 'list' or self.action == 'retrieve':  
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]