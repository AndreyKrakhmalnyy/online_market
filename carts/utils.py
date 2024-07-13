from carts.models import Cart


def get_user_carts(request):
    """Отвечает за отображение содержимого корзины для авторизованного и анонимного пользователей."""
    
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
    
    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key)
    