from django import template
from carts.utils import get_user_carts
from carts.models import Cart

register = template.Library()


@register.simple_tag()
def user_carts(request):
    """Возвращает все позиции из корзины запрашиваемого авторизованного пользователя,
    используя метод 'get_user_carts' из 'carts/utils'.
    """

    return get_user_carts(request)
