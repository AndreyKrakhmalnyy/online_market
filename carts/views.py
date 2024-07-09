from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


def cart_add(request):
    """Добавляет товар в корзину авторизованного пользователя.

    Если товар уже есть в корзине, то увеличивает его количество, иначе создаёт новую запись в корзине.

    Args:
        request: Запрос пользователя.

    Attributes:
        product: Запрашиваемый объект из БД по его ID.

    Returns:
        HttpResponseRedirect: Перенаправление пользователя на предыдущую страницу.
    """

    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

def cart_remove(request):
    """Удаляет товар по id корзины модели 'Cart' авторизованного пользователя.

    Args:
        request: Запрос пользователя.
        cart_id: id конкретной корзины.

    Attributes:
        cart: Запрашиваемый объект из БД по его id.

    Returns:
        HttpResponseRedirect: Перенаправление пользователя на предыдущую страницу.
    """
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()
    
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар удалён",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)

def cart_change(request, product_slug):
    pass