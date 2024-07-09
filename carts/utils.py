from carts.models import Cart


def get_user_carts(request):
    """Возвращает все позиции из корзины запрашиваемого авторизованного пользователя."""
    
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)