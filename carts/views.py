from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


def cart_add(request):
    """Добавляет товар в корзину авторизованного и анонимного пользователей.

    Если товар уже есть в корзине, то увеличивает его количество, иначе создаёт новую запись в корзине.

    Args:
        request: Запрос пользователя.

    Attributes:
        product: Запрашиваемый объект товара из БД по его id.
        product_id (str): id товара, получаемый из POST-запроса;

    Returns:
        JsonResponse: Ответ в формате JSON, содержащий:
            message (str): Сообщение об успешном удалении товара;
            cart_items_html (str): HTML-код, представляющий обновленный список товаров в корзине.
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

    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)


    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    """Удаляет товар по id корзины модели 'Cart' авторизованного пользователя.

    Args:
        request: Запрос пользователя.

    Attributes:
        cart: Запрашиваемый объект корзины из БД по его id;
        cart_id (str): id корзины, получаемый из POST-запроса;
        quantity (int): Количество товара в удаляемой корзине.

    Returns:
        JsonResponse: Ответ в формате JSON, содержащий:
            message (str): Сообщение об успешном удалении товара;
            cart_items_html (str): HTML-код, представляющий обновленный список товаров в корзине;
            quantity_deleted (int): Количество удаленного товара.
    """
    
    cart_id: str = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity: int = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар удалён из корзины",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)


def cart_change(request):
    """Отвечает за корректное изменение количества товаров в корзине.

    Args:
        request: Запрос пользователя.

    Attributes:
        cart_id (str): id корзины, получаемый из POST-запроса;
        quantity (str): Обновлённое количество товара, получаемое из POST-запроса.

    Returns:
        JsonResponse: Ответ в формате JSON, содержащий:
            message (str): Сообщение об успешном изменении количества товара;
            cart_items_html (str): HTML-код шаблона, представляющий обновленный список товаров в корзине;
            quantity (int): Обновленное количество товара в корзине.
    """
    
    cart_id: str = request.POST.get("cart_id")
    quantity: str = request.POST.get("quantity")

    cart: str = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    carts = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": carts}, request=request
    )

    response_data = {
        "message": "Количество товара изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)
