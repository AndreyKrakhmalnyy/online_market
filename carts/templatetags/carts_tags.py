from django import template
from carts.models import Cart

register = template.Library()


@register.simple_tag()
def user_carts(request):
    """Возвращает все позиции из корзины запрашиваемого авторизованного пользователя."""
    
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)