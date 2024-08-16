from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from goods.api.serializers import CategoriesSerializer, ProductsSerializer
from goods.models import Categories, Products

@extend_schema(tags=['Categories'])
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':  
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]

    @extend_schema(summary="Получение списка всех категорий товаров магазина.") 
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(summary="Получение категории по id.")   
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="Добавление категории.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Полное обновление данных о категории товаров (требует заполнения всех полей).")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="Частичное обновление данных о категории (позволяет заменить конкретное поле).")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="Удаление категории товаров по id.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@extend_schema(tags=['Products'])
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (IsAdminUser,)
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':  
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]
    
    @extend_schema(summary="Получение списка всех товаров магазина.") 
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(summary="Получение товара по id.")   
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="Добавление товара.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Полное обновление данных о товаре (требует заполнения всех полей).")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="Частичное обновление данных о товаре (позволяет заменить конкретное поле).")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="Удаление товара по id.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
