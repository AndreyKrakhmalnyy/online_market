from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.api.serializers import UserSerializer
from users.models import User

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

